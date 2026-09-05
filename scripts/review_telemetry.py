"""Collect model costs and research events while a panel runs."""
from __future__ import annotations

import contextlib
import sys
import threading
import time
from dataclasses import dataclass, field
from queue import Empty, Queue


@dataclass
class RunTelemetry:
    """What the bus said about a run, beyond the documents it produced."""

    # node -> USD spent
    costs: dict[str, float] = field(default_factory=dict)
    # node -> [{tool, query, hits, error?}], in the order the lookups happened
    research: dict[str, list[dict]] = field(default_factory=dict)


@contextlib.contextmanager
def _telemetry_recorder(run_id: str):
    """Collect per-agent spend and research lookups off the observability bus.

    The pipeline emits a ``usage`` event per model call and a ``tool`` event
    per research lookup, each carrying its node name, but only ever persists
    the run's cost total. Registering a queue for this run collects both
    breakdowns without touching the pipeline.

    The research half is the one a reader needs. A referee that cites prior
    work is making a different claim depending on whether it searched for that
    work or recalled it, and no other published field separates those: the
    tool-using agents cost more whether or not a tool was ever called.

    Drained on a thread as events arrive, and echoed to stderr, because the
    alternative was unusable. Draining only in the ``finally`` block meant a
    run that hung produced no record of how far it got: the events existed,
    in memory, unreachable until the thing that was not finishing finished.
    A stalled review printed `plan` and then nothing for as long as you left
    it, and the only way to find the responsible node was to SIGINT the
    process and read the traceback. Now the last line of the log names the
    last node that completed.

    Never fails the review, an accounting problem must not lose a completed
    panel, so the thread swallows its own errors and is a daemon: if it dies,
    the run still writes its bundle, one line poorer.
    """
    from peerreviewagents.observability import clear_observer, register_observer

    telemetry = RunTelemetry()
    queue: Queue = Queue()
    register_observer(queue, run_id)
    done = threading.Event()
    started = time.monotonic()

    def record(event) -> None:
        node = event.node or "unattributed"
        # `node_start` without a matching `node_end` is the whole point: on a
        # stalled run the last unpaired arrow names the agent that hung, which
        # previously took a SIGINT and a traceback to learn.
        if event.kind == "node_start":
            print(f"  {time.monotonic() - started:6.0f}s  -> {node}", file=sys.stderr)
        elif event.kind == "node_end":
            spent = telemetry.costs.get(node)
            print(
                f"  {time.monotonic() - started:6.0f}s  ok {node:<28} "
                f"{event.text:>7}"
                + (f"  ${spent:.4f}" if spent else ""),
                file=sys.stderr,
            )
        elif event.kind == "usage" and event.cost_usd:
            telemetry.costs[node] = round(
                telemetry.costs.get(node, 0.0) + event.cost_usd, 6
            )
        elif event.kind == "tool":
            call = {
                "tool": event.tool_name,
                "query": event.tool_query,
                "hits": event.tool_hits,
            }
            if event.tool_error:
                call["error"] = event.tool_error
            telemetry.research.setdefault(node, []).append(call)

    def drain() -> None:
        while not done.is_set():
            try:
                record(queue.get(timeout=0.5))
            except Empty:
                continue
            except Exception as exc:  # noqa: BLE001
                print(f"warning: run telemetry unavailable ({exc})", file=sys.stderr)
                return

    pump = threading.Thread(target=drain, name="telemetry", daemon=True)
    pump.start()
    try:
        yield telemetry
    finally:
        clear_observer(run_id)
        done.set()
        pump.join(timeout=2)
        # Anything the pump had not reached yet. The queue is unbounded and
        # the producer has stopped, so this terminates.
        try:
            while True:
                try:
                    record(queue.get_nowait())
                except Empty:
                    break
        except Exception as exc:  # noqa: BLE001
            print(f"warning: run telemetry unavailable ({exc})", file=sys.stderr)
