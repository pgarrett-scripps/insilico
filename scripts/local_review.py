"""Turn a local PeerReviewAgents run into a publishable review bundle.

The hosted panel is gone. A review is now produced on the editor's own machine,
on a Claude Code subscription, and arrives here as a pull request. No paid API
key exists anywhere in that path, and nothing in this file can create one.

The work splits in two, deliberately:

``prepare`` resolves the paper to a permanent identity, fetches the exact bytes
of that revision, hashes them, and decides where a review of it would belong. It
spends nothing and talks to no model.

``publish`` reads a finished engine run and writes the bundle: the documents, the
provenance record, and the manifest. It spends nothing either.

Between the two, the skill runs the engine itself. That is the only step that
costs anything, and keeping it outside this file means no command here can start
a review by accident.

One thing this module will not do is invent a verdict. The engine grades
findings, with a severity and a disposition each. It produces no accept or
reject, because deciding whether a paper should be published is not a thing it
was built to do. So ``--decision`` is the editor's, typed after reading the run,
and the provenance record says so in as many words.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib
import importlib.metadata
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fetch_preprint import Preprint, download, resolve  # noqa: E402
from review_paths import REPO, REVIEWS, ROUND_RECORD, RUNS  # noqa: E402
from review_plan import (  # noqa: E402
    CommandError,
    draft_number,
    find_paper_dir,
    paper_slug,
    plan_review,
)
from review_provenance import insilico_version, pipeline_version  # noqa: E402

ENGINE_PACKAGE = "peerreviewagents.engine"
PROVENANCE_SCHEMA = 3
GENERATOR_KIND = "local-claude-code"
TRANSPORT_PROVIDER = "claude-code"
DEFAULT_MODEL = "claude-sonnet-5-5"
DECISIONS = ("accept", "minor", "major", "reject")

# Carried in every version 3 record. It is the one claim in the file that no
# hash can back, so it is stated plainly rather than implied by a flag.
ATTESTATION = (
    "This review was generated locally on a Claude Code subscription, with no "
    "paid API key in the path. The named editor read the run and chose the "
    "decision before the review was merged, and merging is what publishes it."
)

# Written instead when the operator says nobody has read the run yet. Such a
# record cannot be published: the guard is in cmd_publish, and the statement
# exists so that a rehearsal bundle on disk cannot be mistaken for a reviewed
# one if somebody copies it by hand.
UNREAD_STATEMENT = (
    "This review was generated locally on a Claude Code subscription. No editor "
    "has attested to reading the run, so it is a rehearsal and must not be "
    "published."
)

# Documents a local bundle writes. Shorter than the hosted panel's list by
# design: there was no desk screen, no five-reviewer panel and no debate, so
# those files are absent rather than present and empty.
BUNDLE_DOCUMENTS = ("summary.md", "decision_letter.md", "manuscript_stats.md")
SEVERITY_ORDER = {"major": 0, "moderate": 1, "minor": 2}
REQUIRED_SEVERITIES = ("major", "moderate")

# The one state a review may be published from. `bundle.FINISHED_STATUSES`
# carries a second, `complete-without-findings`, and that is not a review here.
# The engine writes it in exactly one case: every finding the reviewers raised
# failed the evidence guards and was quarantined. See ensemble.py around the
# final progress write, reviewer.py's guard branch and api.py's
# manuscript_only_progress, all three of which set it only when
# review_guard_status is all-findings-quarantined.
#
# A run that read the manuscript end to end and genuinely raised nothing is
# `complete` with the guard status `clean`, and that publishes with an empty
# findings list, which is the honest record of a manuscript found sound. The
# quarantined case is the opposite claim, a review endorsing none of its own
# work, and publishing it under the same words would tell authors their paper
# drew no findings when every finding was thrown away.
FINISHED_STATUSES = ("complete",)
ALL_FINDINGS_QUARANTINED = "all-findings-quarantined"
WITHOUT_FINDINGS_STATUS = "complete-without-findings"

# insilico publishes Claude Code runs only. The engine still supports Codex
# behind `--provider codex`, and nothing here is written for it: the attestation
# names a Claude subscription, the login probe reads the Claude CLI and the
# billing policy below describes that account. A Codex run published through
# this path would carry all three claims about a transport it never used.
PUBLISHABLE_PROVIDERS = ("claude-code",)

# What the engine calls its bounded study budget, spelled out rather than
# imported: this module has to read a run with no engine installed, which is how
# CI runs the smoke suite. It is `review_policy.STUDY_POLICY_NAME`, and the
# policy that adds no protocol keys, so a run whose protocol names no policy ran
# under this one.
STUDY_POLICY_NAME = "standard-v1"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def engine():
    """Import the engine, or explain how to get one."""
    try:
        return importlib.import_module(ENGINE_PACKAGE)
    except ImportError as exc:
        raise CommandError(
            "PeerReviewAgents 0.8.0 or newer is not importable. Install it, or "
            "run this with the paper-workbench virtual environment on PATH."
        ) from exc


def engine_fingerprint() -> dict:
    """Hash the engine source tree, not just its version number.

    Two reviews can both claim engine 0.8.0 and have run different bytes, one
    from a release and one from a working tree. The file count and the hash of
    the whole manifest settle which.
    """
    module = engine()
    runtime = importlib.import_module(f"{ENGINE_PACKAGE}.model_runtime")
    root = Path(module.__file__).resolve().parent
    manifest = runtime.source_manifest(root)
    if not manifest:
        raise CommandError(f"The engine at {root} has no source files to fingerprint")
    return {
        "algorithm": "sha256",
        "file_count": len(manifest),
        "sha256": digest(canonical(manifest)),
    }


def engine_record() -> dict:
    module = engine()
    api = importlib.import_module(f"{ENGINE_PACKAGE}.api")
    version = getattr(module, "__version__", "") or importlib.metadata.version("peerreviewagents")
    return {
        "name": ENGINE_PACKAGE,
        "version": str(version),
        "api_version": str(getattr(api, "API_VERSION", "")),
    }


# What a Claude subscription login looks like to `claude auth status`. The
# engine accepts exactly these, in model_runtime.require_subscription, and this
# path has to accept the same set or it refuses accounts the engine would
# happily run on. `firstParty` is Anthropic's own name for the subscription
# route, so a truthy apiProvider is not by itself a paid key.
#
# Written out rather than imported. The engine spells the pair inline inside
# require_subscription and exports no constant, and the module that used to
# hold one is gone along with every billing gate, so there is nothing to read
# it from. The pair is asserted against the engine's own source in the smoke
# suite instead, which is where a drift would be caught.
SUBSCRIPTION_AUTH_METHODS = ("claude.ai", "oauth")
SUBSCRIPTION_API_PROVIDERS = (None, "", "firstParty")

# The route this pipeline bills on, named in every published record. The engine
# has no billing policy of its own any more: it runs on whatever subscription
# the Claude CLI is signed in to, and spends nothing else. So this is a
# statement about how the review was paid for, which the login probe below
# confirms, and not a value copied out of the engine.
BILLING_POLICY = "claude-subscription-v1"


def transport_from_status(status: dict, *, provider: str) -> dict:
    """Turn one `claude auth status` reading into the transport record.

    `provider` is the transport the run itself recorded, passed in rather than
    taken from a constant here, so the record cannot name one provider while the
    run asked another.

    Pure, so the refusals can be tested without a CLI. Three things have to hold
    before a review may run: somebody is logged in, the login is a subscription
    login rather than a key, and the account behind it is Anthropic's own rather
    than a cloud reseller. Each failure gets its own message, because the fix
    differs.
    """
    accepted = SUBSCRIPTION_AUTH_METHODS
    error = status.get("error")
    if error:
        raise CommandError(f"The Claude CLI could not report its login: {error}")
    if not status.get("loggedIn"):
        raise CommandError(
            "No Claude Code login. Run `claude /login` and sign in with the "
            "Claude subscription account before generating a review."
        )
    if status.get("authMethod") not in accepted:
        raise CommandError(
            f"The Claude CLI reports authMethod {status.get('authMethod')!r}, "
            f"which is not a subscription login. The engine accepts "
            f"{', '.join(accepted)}. Sign in again with the subscription account."
        )
    if status.get("apiProvider") not in SUBSCRIPTION_API_PROVIDERS:
        raise CommandError(
            f"The Claude CLI is authenticated against the {status.get('apiProvider')} "
            "API rather than an Anthropic subscription. Run `claude /login` and "
            "choose the subscription account before generating a review."
        )
    return {
        "provider": provider,
        "executable": "claude",
        "version": None,
        "billing_policy": BILLING_POLICY,
        "auth_method": str(status.get("authMethod")),
        "subscription_type": status.get("subscriptionType"),
        "api_provider": status.get("apiProvider") or "firstParty",
        "paid_api_key_used": False,
    }


def transport_record(*, provider: str, probe: bool = True) -> dict:
    """Which CLI ran the models, and on whose account.

    `provider` is the transport the run recorded, or, in the preflight where
    there is no run yet, the one this path publishes. Anything outside
    `PUBLISHABLE_PROVIDERS` is refused before the probe, so no second provider's
    CLI is ever executed from here and no bundle is written describing a
    transport this code knows nothing about.

    ``paid_api_key_used`` is a constant here and a constant in the schema. This
    path cannot reach a paid key, so the field is a statement about the design
    rather than a measurement, and a record needing it to be true is not a local
    review and has no business in this shape.

    Without a probe the login fields are absent rather than null, because an
    unprobed login is unknown and a null would read as a measured absence.

    The probe is the only source of the login now. The engine used to copy a
    billing confirmation into the run folder, naming the account that paid, and
    that record was preferred over this probe because it answered the stronger
    question. The engine writes no such file any more, so the honest claim is
    the narrower one this makes: who the Claude CLI was signed in as when the
    bundle was written.
    """
    provider = str(provider or "")
    if provider not in PUBLISHABLE_PROVIDERS:
        raise CommandError(
            f"This run used the {provider or 'unrecorded'} transport, and this "
            f"path records {', '.join(PUBLISHABLE_PROVIDERS)} runs only. Review "
            "the paper again on Claude Code, or publish it by another route."
        )
    if not probe:
        return {
            "provider": provider,
            "executable": "claude",
            "version": None,
            "billing_policy": BILLING_POLICY,
            "login_verified": False,
            "paid_api_key_used": False,
        }
    runtime = importlib.import_module(f"{ENGINE_PACKAGE}.model_runtime")
    return {**transport_from_status(runtime.auth_status(provider=provider), provider=provider),
            "login_verified": True,
            "verified_by": "publish_time_probe"}


def jsonl_rows(path: Path) -> list[dict]:
    rows = []
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError:
        return rows
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            rows.append(row)
    return rows


def observed_models(run_dir: Path) -> list[str]:
    """Model ids the transport actually reported, as opposed to the one asked for.

    The engine writes this as `models_observed`, a list, into every usage
    receipt: see model_runtime.assess_claude_stream, which fills it from the
    per-model usage Claude Code reports back. Looking for a scalar `model` key
    instead finds the requested id in protocol.json and calls it observed, which
    is how a substituted model would have gone unnoticed.
    """
    found: set[str] = set()
    for path in sorted(Path(run_dir).rglob("usage.jsonl")):
        for row in jsonl_rows(path):
            for name in row.get("models_observed") or []:
                if isinstance(name, str) and name:
                    found.add(name)
    for path in sorted(Path(run_dir).rglob("*.json")):
        try:
            payload = read_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        for key, value in _walk(payload):
            if key == "models_observed" and isinstance(value, list):
                found.update(name for name in value if isinstance(name, str) and name)
    return sorted(found)


def _walk(value: object):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key, child
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def model_matches(observed: str, requested: str) -> bool:
    """Is a served model id the model that was asked for, by the engine's rule.

    `model_runtime.same_model` accepts the requested id, a dated release of it
    and a bracketed variant of it, because those are the forms the transport
    reports back for one request. Comparing the strings exactly instead called
    `claude-sonnet-5-5-20260929` a substitution the engine had already
    accepted, so the drift banner fired on every run whose transport dated the
    id it served. The fallback is the engine's rule written out, so this stays
    testable without an engine installed and cannot quietly get looser.
    """
    observed = str(observed)
    requested = str(requested)
    try:
        runtime = importlib.import_module(f"{ENGINE_PACKAGE}.model_runtime")
    except ImportError:
        runtime = None
    same = getattr(runtime, "same_model", None)
    if callable(same):
        return bool(same(observed, requested))
    return observed == requested or observed.startswith((f"{requested}-", f"{requested}["))


def substituted_models(observed: list[str], requested: str) -> list[str]:
    """The served ids that are not the requested model, by the engine's rule."""
    return [name for name in observed if not model_matches(name, requested)]


def resolve_requested_model(run: dict, flag: str | None) -> str:
    """The model this run asked the transport for, taken from the run.

    It used to come from `--model`, whose default was sonnet. The skill lets the
    operator run opus, so an opus run published a record saying sonnet, and the
    summary went on to say every pass used that model. The run records what it
    asked for in protocol.json, so that is the only source here. `--model` is
    kept as an optional cross-check and a disagreement is a refusal, because one
    of the two is wrong and the script cannot tell which.
    """
    recorded = str(run.get("model") or "")
    if not recorded:
        raise CommandError(
            "This run records no model in protocol.json, so the record cannot "
            "say which model wrote the review. Point --run at the engine's "
            "review output folder."
        )
    if flag and not model_matches(recorded, str(flag)) and recorded != str(flag):
        raise CommandError(
            f"--model says {flag} but the run asked for {recorded}. The run is "
            "the one that happened. Drop --model, or point --run at the run you "
            "meant."
        )
    return recorded


def editor_package(run_dir: Path) -> dict:
    """The engine's final review, from wherever this workflow saved it."""
    run_dir = Path(run_dir)
    for candidate in (run_dir / "editor-package.json", run_dir / "core-run" / "editor-package.json"):
        if candidate.is_file():
            return read_json(candidate)
    artifact = run_dir / "core-artifact.json"
    if artifact.is_file():
        package = read_json(artifact).get("editor_package")
        if isinstance(package, dict):
            return package
    raise CommandError(
        f"No editor-package.json under {run_dir}. Point --run at the engine's "
        "review output folder."
    )


def maybe_json(path: Path) -> dict:
    path = Path(path)
    if not path.is_file():
        return {}
    try:
        value = read_json(path)
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _first(*values: object) -> object:
    """The first value that was actually recorded.

    An `or` chain would skip a recorded zero, and a tool limit of zero is a
    budget the synthesis call ran under rather than a missing value.
    """
    for value in values:
        if value not in (None, "", [], {}):
            return value
    return None


def stage_manifests(run_dir: Path) -> list[dict]:
    """The per-stage manifests an ensemble run writes beside its reviewers.

    An ensemble run has a folder per stage, `debate/` or `ordinary-synthesis/`
    for the synthesis and one per discovery reviewer, and each holds its own
    manifest. That is where the synthesis policy and its tool budget live. The
    run's top level manifest holds the paper id, the engine source and the
    plan, so looking there for either found nothing.
    """
    found = []
    for path in sorted(Path(run_dir).glob("*/manifest.json")):
        payload = maybe_json(path)
        if payload:
            found.append(payload)
    return found


def fingerprint_from_manifest(manifest: dict, source: str) -> dict:
    """Hash a recorded engine source manifest the same way everywhere.

    The engine writes `{relative path: sha256}` over its own source tree, both
    when a run starts and when this script asks for it directly. Hashing the
    canonical form of that mapping gives one comparable number, so a run's
    recorded bytes and the installed bytes can be checked against each other.
    """
    if not manifest:
        raise CommandError("An engine source manifest was recorded with no files in it")
    return {
        "algorithm": "sha256",
        "file_count": len(manifest),
        "sha256": digest(canonical(manifest)),
        "source": source,
    }


def read_run(run_dir: Path) -> dict:
    """Everything about the run that the run itself recorded.

    This is the fix for a provenance record that described a run nobody had
    looked at. The engine CLI writes `protocol.json` (provider, model, mode,
    reviewer count), `manifest.json` (the paper id and the engine source
    manifest, both captured when the call started), `editor-package.json` (the
    workflow version, the synthesis policy and the reviewer provenance),
    `progress.json` (final status and usage) and a usage receipt per call.
    `core-artifact.json` exists only when a caller went through
    `peerreviewagents.engine.api.run_review`, so nothing here may depend on it.

    Every key in the result was read from one of those files. A value the run
    did not record is left out, so a caller that needs it has to say so rather
    than silently inherit a default from the prepare step or a publish flag.
    """
    run_dir = Path(run_dir)
    protocol = maybe_json(run_dir / "protocol.json")
    manifest = maybe_json(run_dir / "manifest.json")
    progress = maybe_json(run_dir / "progress.json")
    artifact = maybe_json(run_dir / "core-artifact.json")
    # Reading provenance is not the same job as reading the review. A run with
    # no editor package is refused by cmd_publish, which asks for it directly,
    # and this function stays able to describe a run that failed.
    try:
        package = editor_package(run_dir)
    except CommandError:
        package = {}

    record: dict = {}
    # A published record is read by strangers, and an absolute path in it
    # describes the machine that wrote it rather than the review. The path is
    # recorded when it is inside this repository and left out otherwise.
    if run_dir.resolve().is_relative_to(REPO):
        record["directory"] = run_dir.resolve().relative_to(REPO).as_posix()

    def put(key: str, value: object) -> None:
        if value not in (None, "", [], {}):
            record[key] = value

    plan = manifest.get("plan")
    plan = plan if isinstance(plan, dict) else {}
    nested = manifest.get("protocol")
    nested = nested if isinstance(nested, dict) else {}
    stages = stage_manifests(run_dir)
    synthesis = package.get("synthesis_provenance")
    synthesis = synthesis if isinstance(synthesis, dict) else {}

    put("workflow", protocol.get("mode") or artifact.get("workflow"))
    put("workflow_version", package.get("workflow_version") or protocol.get("version"))
    put("model", protocol.get("model") or nested.get("model") or artifact.get("model_requested"))
    put("provider", protocol.get("provider") or nested.get("provider"))
    put("effort", protocol.get("effort") or nested.get("effort"))
    reviewers = package.get("reviewer_count")
    if not isinstance(reviewers, int):
        reviewers = protocol.get("reviewers")
    put("reviewers", reviewers if isinstance(reviewers, int) else None)
    # The synthesis call records its policy and its tool budget in the stage
    # folder it ran in, not in the run's top level manifest, which carries the
    # paper id, the engine source and the plan. Reading only the top level
    # found neither on any real run.
    put("synthesis_policy", _first(
        manifest.get("synthesis_policy"),
        plan.get("synthesis_policy"),
        package.get("synthesis_policy"),
        *(stage.get("synthesis_policy") for stage in stages),
    ))
    put("synthesis_tool_limit", _first(
        manifest.get("synthesis_tool_limit"),
        synthesis.get("tool_limit"),
        *(stage.get("synthesis_tool_limit") for stage in stages),
    ))
    # Only an ensemble manifest carries the paper id at the top level. The
    # independent and panel modes put it in protocol.json and nest the protocol
    # inside the manifest, so a run in either mode recorded no paper id here
    # and the binding check below it was skipped rather than enforced.
    put("paper_id", _first(
        manifest.get("paper_id"),
        protocol.get("paper_id"),
        nested.get("paper_id"),
    ))
    # What the reviewers were allowed to spend. The ensemble manifest names it
    # in its plan, and every policy but the study one also writes itself into
    # protocol.json: review_policy.protocol_overlay adds no keys for
    # `standard-v1` so that a run made under the engine's original limits keeps
    # a byte-identical protocol and stays resumable. So an absent key on a run
    # that recorded a protocol means the study policy, which is the engine's own
    # reading of it, and without this a five-finding standard-v1 review and a
    # thirty-call agentic-v1 review published indistinguishable records.
    put("review_policy", _first(
        plan.get("review_policy"),
        protocol.get("review_policy"),
        nested.get("review_policy"),
        STUDY_POLICY_NAME if protocol else None,
    ))
    put("engine_source", manifest.get("code"))
    put("status", progress.get("status"))
    # Kept because the status alone no longer distinguishes the two outcomes a
    # reader cares about: a manuscript nobody found fault with is `clean` with
    # no findings, and a review whose every finding was thrown away is
    # `all-findings-quarantined`.
    put("review_guard_status", progress.get("review_guard_status"))
    put("usage", progress.get("usage"))
    put("artifact_version", artifact.get("artifact_version"))

    for path in sorted(run_dir.rglob("tool-config.json")):
        cutoff = maybe_json(path).get("literature_cutoff")
        if cutoff:
            record["literature_cutoff"] = str(cutoff)
            break

    record["errors"] = run_errors(run_dir, progress)
    return record


def run_errors(run_dir: Path, progress: dict) -> list[str]:
    """What the run recorded going wrong, rather than an empty list by default.

    A blocked run says so in progress.json. A finding the engine refused to
    accept is quarantined with a reason instead of ending the run, so those are
    counted here: a reader deciding how much to trust a review should see that
    three of its findings were thrown away.

    Finishing with no findings is not one of these. A run that read the
    manuscript and raised nothing is `complete` with the guard status `clean`,
    and listing that as an error told a reader a review of a sound manuscript
    had gone wrong. Every finding quarantined is a different outcome and is
    listed, because the engine records it as `complete-without-findings` and the
    two read nothing alike.
    """
    errors = []
    if progress.get("error"):
        errors.append(str(progress["error"]))
    status = progress.get("status")
    if status and status not in FINISHED_STATUSES:
        errors.append(f"The run finished in state {status}.")
    # Said plainly, because the two readings are far apart: the reviewers
    # endorsed nothing because every finding they wrote failed the engine's
    # evidence guards, which is not the same as a manuscript they found sound.
    if progress.get("review_guard_status") == ALL_FINDINGS_QUARANTINED:
        errors.append(
            "Every finding this run produced was quarantined by the engine's "
            "evidence guards, so the review endorses none of them."
        )
    quarantined = sorted(Path(run_dir).rglob("*-quarantined.json"))
    if quarantined:
        errors.append(f"{len(quarantined)} quarantined reviewer response(s) in this run.")
    # The engine writes this inside the stage folder the synthesis ran in, so
    # looking for it at the top of the run found nothing and every validation
    # problem the synthesis recorded was dropped from the published record.
    for path in sorted(Path(run_dir).rglob("synthesis-validation.json")):
        for problem in maybe_json(path).get("problems") or []:
            errors.append(str(problem))
    return errors


def bind_run_to_input(prepared: dict, workspace: Path, run: dict) -> dict:
    """Refuse to publish a run of one paper under another paper's identity.

    Nothing else in this pipeline ties the three pieces together. `prepare`
    hashes a PDF, the engine imports some PDF into a workspace, and the run
    reviews some workspace. Each step records enough to check the next, and
    until this function existed none of it was checked, so a run of paper B
    could be published as a review of paper A and exit zero.

    The chain is: the hash prepare took of the fetched bytes, the hash the
    importer took of the bytes it was given, and the paper id the run recorded.
    """
    paper = maybe_json(Path(workspace) / "paper.json")
    if not paper:
        raise CommandError(
            f"No paper.json in {workspace}. Point --workspace at the folder the "
            "engine's import command wrote."
        )
    imported = str(paper.get("source_sha256") or "")
    expected = str(prepared["input"]["sha256"])
    if not imported:
        raise CommandError(
            "The workspace records no source hash, so this run cannot be tied "
            "to the paper that was prepared."
        )
    if imported != expected:
        raise CommandError(
            "This run reviewed different bytes than were prepared. The prepared "
            f"PDF hashes to {expected} and the imported manuscript hashes to "
            f"{imported}. Import the PDF that prepare fetched, or prepare the "
            "paper this workspace holds."
        )
    workspace_paper_id = str(paper.get("id") or "")
    run_paper_id = str(run.get("paper_id") or "")
    # Skipping the comparison when either side is missing is what made this
    # guard optional. A run in independent or panel mode records its paper id
    # in protocol.json rather than the manifest, and the manifest was the only
    # place this used to look, so the check passed by having nothing to check.
    if not workspace_paper_id:
        raise CommandError(
            f"The paper.json in {workspace} records no paper id, so this run "
            "cannot be tied to the manuscript that was imported. Import the "
            "paper again with the engine's import command."
        )
    if not run_paper_id:
        raise CommandError(
            "The run records no paper id, so there is nothing to compare "
            "against the workspace and no way to tell which paper it reviewed. "
            "The engine writes it to protocol.json or manifest.json when the "
            "call starts."
        )
    if run_paper_id != workspace_paper_id:
        raise CommandError(
            f"The run reviewed paper {run_paper_id} but --workspace holds paper "
            f"{workspace_paper_id}. Point --run and --workspace at the same review."
        )
    return {
        "workspace_manifest_sha256": digest((Path(workspace) / "manifest.json").read_bytes())
        if (Path(workspace) / "manifest.json").is_file()
        else None,
        "paper_id": workspace_paper_id or None,
    }


def sorted_findings(package: dict) -> list[dict]:
    findings = [f for f in package.get("findings") or [] if isinstance(f, dict)]
    return sorted(findings, key=lambda f: SEVERITY_ORDER.get(str(f.get("severity")), 9))


def severity_counts(findings: list[dict]) -> dict[str, int]:
    counts = {"major": 0, "moderate": 0, "minor": 0}
    for finding in findings:
        severity = str(finding.get("severity") or "")
        if severity in counts:
            counts[severity] += 1
    return counts


def _location(finding: dict) -> str:
    placement = finding.get("placement")
    if placement not in (None, "anchored"):
        return f"unplaced ({placement})"
    block = finding.get("block_id")
    return f"block {block}" if block else "not located"


def method_paragraph(run: dict, model: str) -> str:
    """Describe the run that happened, from what the run recorded.

    This used to be a fixed paragraph saying one model took one reading with no
    debate. The documented command runs an ensemble with two discovery
    reviewers and a debate synthesis, so the fixed text described a workflow
    nobody had run. Every clause below is now conditional on a recorded value,
    and an unrecorded one is admitted rather than assumed.
    """
    reviewers = run.get("reviewers")
    synthesis = str(run.get("synthesis_policy") or "")
    workflow = str(run.get("workflow") or "")

    if not isinstance(reviewers, int):
        shape = (
            "The run did not record how many reviewer passes it made, so this "
            "review cannot be described more precisely than that it was "
            f"produced by the engine's {workflow or 'review'} workflow."
        )
    elif reviewers <= 1:
        shape = (
            "One reviewer pass produced this review, so nothing checked the "
            "reviewer that was any better than the reviewer. Read it as one "
            "careful reading of the manuscript."
        )
    else:
        shape = (
            f"{reviewers} reviewer passes read the manuscript independently, and "
            "a further call combined them into the review below."
        )
        if synthesis == "debate":
            shape += (
                " That combining call ran under the debate policy, so each "
                "finding had to survive an argument against it before it was "
                "kept."
            )
        elif synthesis:
            shape += f" That combining call ran under the {synthesis} policy."

    return (
        f"{shape} Every pass used the same model, {model}, on a Claude Code "
        "subscription on the editor's own machine. There was no desk screen and "
        "no panel of differently briefed referees, and one model agreeing with "
        "itself is not independent corroboration."
    )


def attestation_paragraph(attestation: dict) -> str:
    """Who stands behind the decision, which depends on whether anyone read it.

    This sentence used to be unconditional, so a rehearsal written with
    `--human-reviewed no` claimed in its own summary that a named human editor
    had read the run. The record alongside it said the opposite.
    """
    editor = str(attestation.get("editor") or "the editor")
    if attestation.get("human_reviewed_before_merge"):
        return (
            f"The decision above was chosen by {editor}, a human editor, after "
            "reading the run. The engine grades findings and does not recommend "
            "a verdict."
        )
    return (
        f"{editor} typed the decision above without attesting to having read "
        "the run, so it stands on nothing and this bundle is a rehearsal that "
        "must not be published. The engine grades findings and does not "
        "recommend a verdict."
    )


def render_summary(preprint: Preprint, package: dict, provenance: dict, findings: list[dict]) -> str:
    counts = severity_counts(findings)
    generator = provenance["generator"]
    lines = [
        f"# Review Summary: {preprint.title or 'Untitled submission'}",
        "",
        f"**Decision:** {provenance['decision'].title()}",
        "**Target venue:** In Silico",
        f"**Generated by:** {generator['engine']['name']} {generator['engine']['version']}, "
        f"run locally on {generator['model_ids']['requested']}",
        f"**Findings:** {len(findings)} total "
        f"({counts['major']} major, {counts['moderate']} moderate, {counts['minor']} minor)",
        "",
        "## How this review was produced",
        "",
        method_paragraph(generator["run"], generator["model_ids"]["requested"]),
        "",
        attestation_paragraph(generator["attestation"]),
        "",
    ]
    summary = str(package.get("summary") or "").strip()
    if summary:
        lines += ["## Reviewer summary", "", summary, ""]
    if findings:
        lines += ["## Findings", ""]
        for number, finding in enumerate(findings, 1):
            title = str(finding.get("title") or "Untitled finding").strip()
            severity = str(finding.get("severity") or "unstated")
            lines.append(f"{number}. **{title}** ({severity}, {_location(finding)})")
        lines.append("")
    limitations = [str(v).strip() for v in package.get("limitations") or [] if str(v).strip()]
    if limitations:
        lines += ["## Stated limitations of this review", ""]
        lines += [f"- {item}" for item in limitations]
        lines.append("")
    return "\n".join(lines)


def render_decision_letter(preprint: Preprint, package: dict, provenance: dict, findings: list[dict]) -> str:
    required = [f for f in findings if str(f.get("severity")) in REQUIRED_SEVERITIES]
    optional = [f for f in findings if str(f.get("severity")) == "minor"]
    attestation = provenance["generator"]["attestation"]
    # Same defect as the summary's. The claim that the decision was taken after
    # reading the run was printed whether or not anybody said they had read it.
    if attestation.get("human_reviewed_before_merge"):
        standing = (
            "This letter reports one locally generated review. The decision is "
            "the editor's, taken after reading the run in full."
        )
    else:
        standing = (
            "This letter reports one locally generated review as a rehearsal. "
            "Nobody has attested to reading the run, so the decision above "
            "stands on nothing and this letter must not be published."
        )
    lines = [
        f"# Decision Letter: {preprint.title or 'Untitled submission'}",
        "",
        f"**Decision:** {provenance['decision'].title()}",
        "",
        f"{standing} Everything below it is the reviewer's, quoted or "
        "paraphrased from the saved output rather than rewritten.",
        "",
    ]
    summary = str(package.get("summary") or "").strip()
    if summary:
        lines += ["## Assessment", "", summary, ""]
    if required:
        lines += ["## Required changes", ""]
        for number, finding in enumerate(required, 1):
            lines += _letter_entry(f"R{number}", finding)
    if optional:
        lines += ["## Suggestions", ""]
        for number, finding in enumerate(optional, 1):
            lines += _letter_entry(f"S{number}", finding)
    if not findings:
        lines += [
            "## Findings",
            "",
            "The reviewer recorded no findings against this manuscript.",
            "",
        ]
    return "\n".join(lines)


def _letter_entry(label: str, finding: dict) -> list[str]:
    title = str(finding.get("title") or "Untitled finding").strip()
    severity = str(finding.get("severity") or "unstated")
    lines = [f"### {label}. {title}", "", f"**Severity:** {severity}  ", f"**Location:** {_location(finding)}", ""]
    quote = str(finding.get("quote") or "").strip()
    if quote:
        lines += ["Manuscript passage:", "", f"> {quote}", ""]
    comment = str(finding.get("comment") or "").strip()
    if comment:
        lines += [comment, ""]
    replacement = str(finding.get("replacement") or "").strip()
    if replacement:
        lines += ["Suggested replacement:", "", f"> {replacement}", ""]
    counter = str(finding.get("counterevidence") or "").strip()
    if counter:
        lines += [f"**Strongest counterpoint:** {counter}", ""]
    return lines


def render_stats(preprint: Preprint, ingest: dict, generator: dict) -> str:
    lines = [
        "# Manuscript Statistics",
        "",
        f"**Title:** {preprint.title or 'Untitled submission'}",
        f"**Source:** {preprint.source} {preprint.identifier}",
        f"**Revision reviewed:** v{preprint.version or 'unrecorded'}",
        "",
        "## Bytes reviewed",
        "",
        f"- PDF size: {generator['input']['bytes']} bytes",
        f"- PDF sha256: `{generator['input']['sha256']}`",
    ]
    manifest = generator["input"].get("workspace_manifest_sha256")
    if manifest:
        lines.append(f"- Workspace manifest sha256: `{manifest}`")
    chars = ingest.get("chars")
    if chars:
        lines.append(f"- Manuscript text: {chars} characters")
    if ingest.get("text_sha256"):
        lines.append(f"- Manuscript text sha256: `{ingest['text_sha256']}`")
    blocks = ingest.get("blocks")
    if blocks:
        lines.append(f"- Source blocks: {blocks}")
    lines += [
        "",
        "## How the text was read",
        "",
        f"Imported by {ingest.get('tool') or 'the engine importer'} into evidence-linked "
        "source blocks. Quotations in this review were validated against those "
        "blocks before the review was saved.",
        "",
    ]
    return "\n".join(lines)


def ingest_record(workspace: Path | None) -> dict:
    """What the reviewer was handed, measured off the workspace with no model."""
    record = {"format": "markdown", "tool": "peerreviewagents.engine import", "caveman": None}
    if workspace is None:
        return record
    workspace = Path(workspace)
    manuscript = workspace / "manuscript.md"
    if manuscript.is_file():
        text = manuscript.read_text(encoding="utf-8")
        record["chars"] = len(text)
        record["text_sha256"] = digest(text.encode())
    paper = workspace / "paper.json"
    if paper.is_file():
        try:
            blocks = read_json(paper).get("blocks")
        except (OSError, json.JSONDecodeError):
            blocks = None
        if isinstance(blocks, list):
            record["blocks"] = len(blocks)
    return record


def review_kind(plan_kind: str, baseline_eligible: bool) -> str:
    """The published label for this attempt, in the vocabulary the site reads.

    `review.kind` is printed on the provenance panel and read by Notices.astro,
    so this reuses the hosted panel's words rather than inventing one. The rule
    there is that an ungraded run is an experiment whatever else it is, and
    every run on this path is ungraded unless the editor claims it. A revision
    round keeps its own name, because what it is measured against matters more
    than how it was produced.
    """
    if plan_kind == "revision round":
        return "revision"
    if not baseline_eligible:
        return "experiment"
    if plan_kind == "same-draft re-review":
        return "editorial_rereview"
    return "initial"


def build_provenance(
    *,
    preprint: Preprint,
    prepared: dict,
    package: dict,
    run: dict,
    fingerprint: dict,
    decision: str,
    editor: str,
    human_reviewed: bool,
    route: str,
    draft: int,
    attempt: int,
    submitter: str,
    submitter_is_author: str,
    baseline_eligible: bool,
    ingest: dict,
    observed: list[str],
    requested_model: str,
    transport: dict,
    review_id: str,
    publishing: bool,
) -> dict:
    """The published record of what produced this review.

    Version 3. It carries the same identity fields as the hosted panel's version
    2 record, and in place of that panel's accounting it carries a generator
    block: the engine and its fingerprint, the transport and its billing policy,
    the model ids, the input hash, and the attestation that a person read the run
    before it was merged.
    """
    findings = sorted_findings(package)
    # Recorded only when somebody actually submitted the paper. A review an
    # editor started themselves was solicited by nobody, and writing an empty
    # claim for it would be read as a claim we failed to collect.
    attribution = (
        {"submitter": submitter, "submitter_is_author": submitter_is_author}
        if submitter
        else {}
    )
    kind = review_kind(str(prepared.get("plan_kind") or ""), baseline_eligible)
    if not editor:
        raise CommandError("An editor has to be named before a review can be attested")
    # The run's own record, with the finding count this bundle actually wrote
    # added. Nothing from the prepare step or the publish flags is folded in:
    # prepare states an intention and the run states what happened, and when the
    # two disagree the run is the one that is true.
    run_record = {key: value for key, value in run.items() if key != "engine_source"}
    run_record["findings"] = len(findings)
    # The provider is the run's too. It used to be a constant at the top level
    # and another constant inside the transport, so a record could say
    # claude-code twice over a run that had asked the engine for Codex, and
    # nothing in the file compared the two.
    provider = str(run.get("provider") or "")
    if not provider:
        raise CommandError(
            "This run records no provider, so the record cannot say which "
            "transport produced the review."
        )
    if str(transport.get("provider") or "") != provider:
        raise CommandError(
            f"The run used the {provider} transport and the login was read from "
            f"{transport.get('provider')}. A record that names two transports "
            "describes neither run."
        )
    generator = {
        "kind": GENERATOR_KIND,
        "engine": engine_record(),
        "engine_fingerprint": fingerprint,
        "transport": transport,
        "model_ids": {"requested": requested_model, "observed": observed},
        "input": prepared["input"],
        "run": run_record,
        "decision_source": "human_editor",
        "attestation": {
            "locally_generated": True,
            "human_reviewed_before_merge": human_reviewed,
            # Said outright, because the only thing that used to distinguish a
            # rehearsal from a published review was which folder it sat in, and
            # a folder can be copied. The schema requires false here.
            "rehearsal": not publishing,
            "editor": editor,
            "statement": ATTESTATION if human_reviewed else UNREAD_STATEMENT,
        },
    }
    # A model the operator asked for and a model the transport served are two
    # different claims. Saying which is which costs nothing and settles an
    # argument that would otherwise need the run directory.
    # An exact comparison here flagged a dated release of the requested model
    # as a substitution, which the engine itself accepts as the same model.
    if substituted_models(observed, requested_model):
        generator["model_ids"]["substituted"] = True
    return {
        "schema_version": PROVENANCE_SCHEMA,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "pipeline": pipeline_version(),
        "insilico": insilico_version(),
        "generator": generator,
        "review": {
            "id": review_id,
            "manuscript_version": draft,
            "attempt": attempt,
            "kind": kind,
            "lifecycle": "active",
            "baseline_eligible": baseline_eligible,
            "route": route,
        },
        "provider": provider,
        # One model wrote every word of this review. `models` is the per-stage
        # split, and claiming one here would describe a panel that did not run,
        # so it stays empty and `model` carries the single id. The site reads
        # exactly that pair as "nothing checked the reviewer".
        "model": requested_model,
        "models": {},
        "decision": decision,
        "desk_rejected": False,
        "round": 1,
        "ingest": ingest,
        "panel": [],
        # A subscription has no per-review price. Null says there is no figure,
        # where a zero would read as a measured free run.
        "total_cost_usd": None,
        "errors": [str(e) for e in run.get("errors") or []],
        "preprint": preprint.to_dict(),
        **attribution,
    }


def write_manifest(dest: Path) -> None:
    """Hash every file in the bundle, so a later edit to one is visible."""
    dest = Path(dest)
    files = {
        path.relative_to(dest).as_posix(): digest(path.read_bytes())
        for path in sorted(dest.rglob("*"))
        if path.is_file() and path.name != "manifest.json"
    }
    write_json(dest / "manifest.json", {"schema_version": 1, "files": files})


def write_round_record(dest: Path, preprint: Preprint, provenance: dict, findings: list[dict]) -> None:
    required = [
        {
            "id": f"R1-{number:02d}",
            "text": str(finding.get("comment") or finding.get("title") or "").strip(),
            "source_reviewer": "",
            "blocking": False,
        }
        for number, finding in enumerate(
            [f for f in findings if str(f.get("severity")) in REQUIRED_SEVERITIES], 1
        )
    ]
    write_json(
        dest / ROUND_RECORD,
        {
            "schema_version": 1,
            "round": 1,
            "manuscript_title": preprint.title,
            "decision": provenance["decision"],
            "required_revisions": required,
            "minor_suggestions": [
                str(f.get("comment") or f.get("title") or "").strip()
                for f in findings
                if str(f.get("severity")) == "minor"
            ],
            "manuscript_text_sha256": provenance["ingest"].get("text_sha256", ""),
            "manuscript_file_sha256": provenance["generator"]["input"]["sha256"],
            "desk_rejected": False,
        },
    )


def cmd_fingerprint(args: argparse.Namespace) -> int:
    """Preflight. Prints what would be recorded, and calls no model."""
    record = {
        "engine": engine_record(),
        "engine_fingerprint": engine_fingerprint(),
        # No run exists yet, so the preflight asks about the one transport this
        # path can publish. A review on anything else is refused later anyway.
        "transport": transport_record(provider=TRANSPORT_PROVIDER, probe=not args.offline),
    }
    print(json.dumps(record, indent=2))
    return 0


def cmd_prepare(args: argparse.Namespace) -> int:
    """Resolve the paper, fetch the exact bytes, and decide where a review goes."""
    out = Path(args.out).resolve()
    if out.exists() and any(out.iterdir()):
        raise CommandError(f"{out} already holds a prepared paper. Use a new folder.")
    out.mkdir(parents=True, exist_ok=True)

    preprint = None
    publishable = False
    if args.paper:
        preprint = resolve(args.paper)
        publishable = True

    if args.pdf:
        source = Path(args.pdf).resolve()
        if not source.is_file():
            raise CommandError(f"No PDF at {source}")
        pdf = out / "manuscript.pdf"
        shutil.copyfile(source, pdf)
        local_file = True
    elif preprint is not None:
        pdf = download(preprint, out)
        local_file = False
    else:
        raise CommandError("Pass --paper, or --pdf, or both.")

    data = pdf.read_bytes()
    if preprint is not None and not preprint.pdf_sha256:
        preprint.pdf_sha256 = digest(data)
        preprint.pdf_bytes = len(data)

    kind = "pdf" if preprint is None else ("arxiv" if preprint.source == "arxiv" else "doi")
    identifier = args.paper if preprint is None else (preprint.identifier or preprint.doi or preprint.url)
    record = {
        "publishable": publishable,
        "pdf": str(pdf),
        "workflow": args.workflow,
        "reviewers": args.reviewers,
        "literature_cutoff": args.literature_cutoff or dt.date.today().isoformat(),
        "input": {
            "kind": kind,
            "identifier": identifier,
            "sha256": digest(data),
            "bytes": len(data),
            "local_file": local_file,
        },
        "preprint": preprint.to_dict() if preprint is not None else None,
    }

    if publishable:
        paper_dir = find_paper_dir(preprint) or (
            REVIEWS / str(dt.date.today().year) / paper_slug(preprint, preprint.title)
        )
        draft = draft_number(preprint)
        plan = plan_review(paper_dir, draft, args.replace, publishing=True)
        record["destination"] = str(plan.dest)
        record["draft"] = plan.draft
        record["attempt"] = plan.attempt
        record["plan_kind"] = plan.kind
    else:
        record["destination"] = str(RUNS / f"local-{digest(data)[:12]}")
        record["draft"] = 1
        record["attempt"] = 1
        record["plan_kind"] = "unpublishable local run"

    write_json(out / "prepared.json", record)
    print(json.dumps(record, indent=2))
    if not publishable:
        print(
            "\nThis run cannot be published. A review has to name the exact "
            "revision it judged, and a bare PDF does not. Re-run prepare with "
            "--paper to publish.",
            file=sys.stderr,
        )
    return 0


def absolute_path_fields(value: object, trail: str = "") -> list[str]:
    """Where a record carries a path that only exists on the machine that wrote it.

    A published provenance record is read by people with no access to this
    disk, so an absolute path in it identifies the operator's filesystem rather
    than the review. Two fields leaked one: the run directory always, and the
    review id whenever the destination sat outside the repository.
    """
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            found += absolute_path_fields(child, f"{trail}.{key}" if trail else str(key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found += absolute_path_fields(child, f"{trail}[{index}]")
    elif isinstance(value, str) and (value.startswith("/") or value.startswith("file://")):
        found.append(trail or "(root)")
    return found


_DROPPED = object()

# The fields engine 0.8.0 fills with a path on the machine that ran the review.
# `source_review_path` is written once per reviewer in ensemble.py and again
# inside every entry of `candidate_origins`, which carries those same
# provenance dicts, so naming the leaf covers both. `memo_path` rides along
# with each focused evidence memo, from focused_investigation.py.
#
# This is a list of field names rather than a test on the value because the
# first version tested the value: any string beginning with a slash was taken
# for a path. A reviewer writing "/ 2 is the wrong denominator" had the comment
# silently deleted from the published package, and a path written inside a
# sentence was missed regardless. Review content is never rewritten now. What
# catches a path the engine starts recording in a field nothing here knows
# about is the leak scan over the written bundle, below.
PATH_FIELDS = frozenset({"source_review_path", "memo_path", "run_directory"})


def readable_path(text: str) -> object:
    """A path value as a reader can use it, or _DROPPED if they cannot.

    A path inside this repository is rewritten relative to it, because it still
    points at something a reader has. A path outside it names a directory on one
    machine, so the field goes rather than being published as noise. The hash
    beside it is what tied the file to its bytes, and that is kept.
    """
    raw = text[len("file://") :] if text.startswith("file://") else text
    raw = raw.strip()
    if raw.startswith("~"):
        return _DROPPED
    try:
        path = Path(raw)
        if not path.is_absolute():
            return text
        path = path.resolve()
    except (OSError, ValueError, RuntimeError):
        return _DROPPED
    if path.is_relative_to(REPO.resolve()):
        return path.relative_to(REPO.resolve()).as_posix()
    return _DROPPED


def without_local_paths(value: object, *, field: str = "") -> object:
    """The same JSON with the engine's path fields made repo relative or dropped.

    `editor-package.json` is the engine's own output copied into the bundle, and
    the engine records the absolute path of every reviewer package it read. That
    published one home directory per reviewer. Only the fields in `PATH_FIELDS`
    and dictionary keys that are themselves absolute paths are touched, so the
    review's own words reach the reader as the reviewer wrote them.
    """
    if isinstance(value, dict):
        scrubbed = {}
        for key, child in value.items():
            # `synthesis_provenance.shared_images` maps each attached figure's
            # absolute path to its hash, at api.py:229 by way of `_hash_files`,
            # so there the leak is the key. A key that is an absolute path is
            # never something a reviewer wrote.
            name = key
            if isinstance(key, str) and (key.startswith("/") or key.startswith("file://")):
                relative = readable_path(key)
                if relative is _DROPPED:
                    continue
                name = relative
            cleaned = without_local_paths(child, field=key if isinstance(key, str) else "")
            if cleaned is not _DROPPED:
                scrubbed[name] = cleaned
        return scrubbed
    if isinstance(value, list):
        return [
            cleaned
            for cleaned in (without_local_paths(child, field=field) for child in value)
            if cleaned is not _DROPPED
        ]
    if isinstance(value, str) and field in PATH_FIELDS:
        return readable_path(value)
    return value


def local_path_needles() -> list[str]:
    """The strings that reach a published file only by mistake.

    The first version of this scan looked for a leading slash in a JSON value,
    which both missed and over-matched: it read none of the Markdown, nothing
    keyed by a path, no `~/` or Windows form, and no path written inside a
    sentence, while flagging a reviewer's own arithmetic. These two strings are
    the operator's home directory and this checkout, in whatever shape they
    take on the machine doing the publishing. No review has a reason to contain
    either, and prose does not contain them by accident.
    """
    needles = {str(REPO.resolve())}
    try:
        needles.add(str(Path.home().resolve()))
    except (OSError, RuntimeError):
        pass
    return sorted(needle for needle in needles if needle not in ("", "/"))


def bundle_local_path_leaks(dest: Path) -> list[str]:
    """Every file in a written bundle that names the machine that wrote it.

    This reads what is on disk rather than what the code meant to write, which
    is the point: it is the guard that catches a path the engine started
    recording in a field nothing here knows about, in any file of the bundle.
    """
    needles = local_path_needles()
    found: list[str] = []
    for path in sorted(Path(dest).rglob("*")):
        if not path.is_file() or path.suffix.lower() not in (".json", ".jsonl", ".md", ".txt"):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for needle in needles:
            if needle in text:
                found.append(f"{path.relative_to(dest).as_posix()} names {needle}")
    return found


def publish_destination(prepared: dict, *, publishing: bool) -> Path:
    """Where this bundle is written, which depends on whether it is published.

    Without ``--publish`` the publishability and decision guards are relaxed, so
    the bundle is a rehearsal and must not land in the published tree. It used
    to: ``prepare`` records a destination under ``docs/reviews`` for any paper
    with a permanent identity, and ``publish`` wrote there whatever the flag
    said. A rehearsal therefore produced a complete, renderable bundle inside
    the directory the site builds from, and the only thing keeping it off the
    site was that nobody had committed it yet.

    Both destinations are resolved and then required to be inside the tree they
    belong to. Trusting the recorded destination on the publish path meant any
    string in prepared.json was written to, and building the rehearsal path out
    of unresolved parts let `..` segments through, which is why the refusal
    below it could never fire.
    """
    dest = Path(prepared["destination"]).expanduser().resolve()
    if publishing:
        if not dest.is_relative_to(REVIEWS.resolve()):
            raise CommandError(
                f"A published bundle has to be written inside {REVIEWS}, and "
                f"prepared.json points at {dest}. Prepare the paper again."
            )
        return dest
    rehearsal_root = (RUNS / "rehearsal").resolve()
    slug = dest.parent.parent.name or "unnamed"
    rehearsal = (rehearsal_root / slug / dest.parent.name / dest.name).resolve()
    if not rehearsal.is_relative_to(rehearsal_root):
        raise CommandError(
            f"A rehearsal bundle would be written outside {rehearsal_root}, at "
            f"{rehearsal}. Refusing. Pass --publish to publish deliberately."
        )
    return rehearsal


def bundle_identifier(dest: Path) -> str:
    """How a record names its own bundle, without naming the operator's disk.

    The repository relative path when there is one. A rehearsal written outside
    the repository keeps the last three segments, which is the slug and the
    route, because that identifies the bundle and nothing else about the
    machine it was written on.
    """
    dest = Path(dest).resolve()
    repo = REPO.resolve()
    if dest.is_relative_to(repo):
        return dest.relative_to(repo).as_posix()
    return "/".join(dest.parts[-3:])


def require_complete_run(run_dir: Path, run: dict) -> None:
    """A published review has to come from a run that finished.

    Publishing checked neither. A directory holding only an editor package, with
    no protocol.json and no progress.json, published with an empty error list,
    and so did a run whose progress.json said `blocked`. Both produced a record
    that read like a clean review.

    Finished means `complete`, and nothing else. A run that read the manuscript
    and raised no finding is `complete` with the guard status `clean`, and it
    publishes as a review with the empty findings list the reader should see.
    The engine's other finished state, `complete-without-findings`, is written
    only when every finding was quarantined, so it is refused here by name
    before the status check: that bundle's letter would tell the authors their
    paper drew no findings, when the truth is that the review endorses none of
    the findings it wrote.

    A blocked run is refused too, and the refusal repeats the cause the run
    itself recorded rather than only the state name, because the state name
    alone sent the operator back to a log to find out there was no Claude login.

    The transport is checked here as well. This path records Claude Code runs
    only, and the engine will run Codex for anyone who asks it to, so a Codex
    run reaching publish would otherwise be written up with a Claude
    subscription attestation it has no claim to.
    """
    protocol_path = Path(run_dir) / "protocol.json"
    if not protocol_path.is_file():
        raise CommandError(
            f"{run_dir} has no protocol.json, so there is no record of what was "
            "asked of the engine. Point --run at the engine's review output "
            "folder."
        )
    # Only the file's existence was checked, so a zero byte protocol.json
    # satisfied the guard while answering none of the questions it was added to
    # ask. The run has to say what was asked of the engine, not merely have a
    # file where that would be written.
    if not maybe_json(protocol_path):
        raise CommandError(
            f"{protocol_path} is empty or is not a JSON object, so the run "
            "records nothing about what was asked of the engine."
        )
    missing = [field for field in ("workflow", "model", "provider") if not run.get(field)]
    if missing:
        raise CommandError(
            f"{protocol_path} records no {', '.join(missing)}, so the published "
            "record could not say how the review was produced. Point --run at "
            "the engine's review output folder."
        )
    provider = str(run.get("provider") or "")
    if provider not in PUBLISHABLE_PROVIDERS:
        raise CommandError(
            f"This run recorded the {provider} transport, and this path "
            f"publishes {', '.join(PUBLISHABLE_PROVIDERS)} runs only. Every "
            "claim a published bundle makes about how the review was paid for "
            "is a claim about a Claude subscription, so a run on another "
            "transport cannot be published through it."
        )
    status = str(run.get("status") or "")
    if not status:
        raise CommandError(
            f"{run_dir} has no progress.json, so the run never recorded whether "
            "it finished. A review cannot be published from it."
        )
    # Named before the status, because this is the case the status describes
    # and the operator needs to be told which of the two it is.
    if run.get("review_guard_status") == ALL_FINDINGS_QUARANTINED or status == WITHOUT_FINDINGS_STATUS:
        raise CommandError(
            f"This run ended as {status} with guard status "
            f"{run.get('review_guard_status') or 'unrecorded'}, which the engine "
            "writes when every finding it produced was quarantined by the "
            "evidence guards. A review that endorses none of its own findings is "
            "not a manuscript found sound, and publishing it would say so to the "
            "authors. Read the quarantine reasons in the run, and re-run the "
            "engine or publish nothing."
        )
    if status not in FINISHED_STATUSES:
        cause = next((str(problem) for problem in run.get("errors") or [] if problem), "")
        raise CommandError(
            f"This run ended in state {status} rather than "
            f"{' or '.join(FINISHED_STATUSES)}, so it is not a review."
            + (f" The run recorded: {cause}" if cause else "")
            + " Re-run the engine, or drop --publish to keep the bundle as a "
            "rehearsal."
        )


def cmd_publish(args: argparse.Namespace) -> int:
    """Write the bundle from a finished engine run."""
    prepared_dir = Path(args.prepared).resolve()
    prepared = read_json(prepared_dir / "prepared.json")
    if args.publish and not prepared.get("publishable"):
        raise CommandError(
            "This paper was prepared from a local PDF with no permanent "
            "identifier, so it cannot be published. Prepare it again with "
            "--paper."
        )
    if args.decision not in DECISIONS:
        raise CommandError(f"--decision must be one of: {', '.join(DECISIONS)}")
    human_reviewed = args.human_reviewed == "yes"
    if args.publish and not human_reviewed:
        raise CommandError(
            "A review cannot be published unless the editor has read the run. "
            "Read it, then pass --human-reviewed yes."
        )
    # A rehearsal that carried a true attestation was a published record in
    # every respect except where it sat, so copying its folder into
    # docs/reviews by hand produced a review that passed every check. An
    # attestation is a claim attached to a publication, and a rehearsal makes
    # no publication, so the two cannot be asked for together.
    if human_reviewed and not args.publish:
        raise CommandError(
            "--human-reviewed yes is an attestation, which only a published "
            "review can carry. Add --publish to publish this run, or pass "
            "--human-reviewed no to rehearse the bundle."
        )
    # Publishing with the probe skipped wrote `login_verified: false` and no
    # auth fields at all, and the record validated. A published record has to
    # name the account the review was billed to.
    if args.publish and args.offline:
        raise CommandError(
            "--offline skips the login check, so the record would say the "
            "subscription login was never verified. Drop --offline to publish, "
            "or drop --publish to rehearse."
        )

    run_dir = Path(args.run).resolve()
    package = editor_package(run_dir)
    run = read_run(run_dir)
    requested_model = resolve_requested_model(run, args.model)
    if args.publish:
        require_complete_run(run_dir, run)
    workspace = Path(args.workspace).resolve()
    preprint_data = prepared.get("preprint")
    if preprint_data is None:
        raise CommandError("A bundle needs preprint metadata. Prepare with --paper.")
    preprint = Preprint(**preprint_data)

    # Before anything is written: is this a run of the paper that was prepared?
    binding = bind_run_to_input(prepared, workspace, run)
    if binding["workspace_manifest_sha256"]:
        prepared["input"]["workspace_manifest_sha256"] = binding["workspace_manifest_sha256"]
    ingest = ingest_record(workspace)

    # The fingerprint is the engine's own source manifest from the moment the
    # run started, not a re-hash of whatever is installed now. Taking it at
    # publish time recorded the bytes of the machine writing the bundle, which
    # is not the claim the record makes.
    engine_source = run.get("engine_source")
    if not isinstance(engine_source, dict) or not engine_source:
        raise CommandError(
            f"{run_dir} records no engine source manifest, so the code that "
            "produced this review cannot be identified. The engine writes it to "
            "manifest.json at the start of a run."
        )
    fingerprint = fingerprint_from_manifest(engine_source, "run_manifest")
    try:
        installed = engine_fingerprint()
    except CommandError:
        installed = None
    if installed is not None:
        fingerprint["matches_installed_engine"] = installed["sha256"] == fingerprint["sha256"]

    dest = publish_destination(prepared, publishing=args.publish)
    route = f"v{prepared['draft']}/r{prepared['attempt']}"
    review_id = bundle_identifier(dest)
    # The run's transport, so the login that is probed is the login the review
    # ran on, and a run on anything this path cannot publish is refused here
    # even when the bundle is only a rehearsal.
    transport = transport_record(provider=str(run.get("provider") or ""), probe=not args.offline)
    provenance = build_provenance(
        preprint=preprint,
        prepared=prepared,
        package=package,
        run=run,
        fingerprint=fingerprint,
        decision=args.decision,
        editor=args.editor,
        human_reviewed=human_reviewed,
        route=route,
        draft=int(prepared["draft"]),
        attempt=int(prepared["attempt"]),
        submitter=args.submitter,
        submitter_is_author=args.submitter_is_author,
        baseline_eligible=args.baseline_eligible,
        ingest=ingest,
        observed=observed_models(run_dir),
        requested_model=requested_model,
        transport=transport,
        review_id=review_id,
        publishing=args.publish,
    )

    # The engine's own output is copied into the bundle, and it records the
    # absolute path of each reviewer package it read. Scrubbing happens before
    # anything is written, so the manifest hashes the file a reader will get.
    published_package = without_local_paths(package) if args.publish else package

    if args.publish:
        leaked = absolute_path_fields(provenance)
        if leaked:
            raise CommandError(
                "This record would publish absolute local paths at "
                f"{', '.join(leaked)}. A published record may not name the "
                "operator's filesystem."
            )

    # Every document is rendered from the scrubbed package. Rendering from the
    # unscrubbed one put the paths back: a reviewer's `source_review_path` was
    # dropped from the JSON and then printed in decision_letter.md, where no
    # scan was looking for it.
    findings = sorted_findings(published_package)
    if dest.exists() and any(dest.iterdir()):
        raise CommandError(f"Refusing to overwrite an existing review bundle: {dest}")

    # The bundle is built outside the published tree and moved in once every
    # guard has passed. The guards used to run after six files had already been
    # written into docs/reviews, so a refusal left most of a bundle behind, with
    # no manifest and nothing saying it was rejected.
    with tempfile.TemporaryDirectory(prefix="local-review-bundle-") as staging:
        stage = Path(staging)

        (stage / "summary.md").write_text(
            render_summary(preprint, published_package, provenance, findings), encoding="utf-8"
        )
        (stage / "decision_letter.md").write_text(
            render_decision_letter(preprint, published_package, provenance, findings),
            encoding="utf-8",
        )
        (stage / "manuscript_stats.md").write_text(
            render_stats(preprint, ingest, provenance["generator"]), encoding="utf-8"
        )
        write_json(stage / "provenance.json", provenance)
        write_round_record(stage, preprint, provenance, findings)
        # Kept beside the documents so a reader can check a quotation against
        # the structured record the reviewer actually produced.
        write_json(stage / "editor-package.json", published_package)

        # Read back what is actually on disk before the manifest fixes it. This
        # is the check that cannot be fooled by a file nobody thought to scrub,
        # or by a field no version of this script knows the engine writes.
        if args.publish:
            leaked = bundle_local_path_leaks(stage)
            if leaked:
                raise CommandError(
                    "This bundle names the machine that produced it: "
                    f"{', '.join(leaked)}. Nothing was written to {dest}."
                )
        write_manifest(stage)

        dest.mkdir(parents=True, exist_ok=True)
        for path in sorted(stage.iterdir()):
            shutil.move(str(path), str(dest / path.name))

    print(f"bundle   {dest}")
    print(f"decision {provenance['decision']} (chosen by {args.editor})")
    print(f"findings {len(findings)}")
    print(f"baseline {'eligible' if provenance['review']['baseline_eligible'] else 'experimental only'}")
    observed = provenance["generator"]["model_ids"]["observed"]
    print(f"model    requested {requested_model}, observed {', '.join(observed) or 'not reported'}")
    if provenance["generator"]["model_ids"].get("substituted"):
        print("warning  the transport served a model other than the one requested")
    if not args.publish:
        print("rehearsal, written outside docs/reviews. Re-run with --publish to publish.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("fingerprint", help="Print the engine and transport record, calling no model")
    p.add_argument("--offline", action="store_true", help="Skip the CLI authentication probe")
    p.set_defaults(func=cmd_fingerprint)

    p = sub.add_parser("prepare", help="Resolve a paper, fetch its bytes, and plan the bundle path")
    p.add_argument("--paper", help="arXiv id, bioRxiv or medRxiv DOI, or an archive URL")
    p.add_argument("--pdf", help="Local PDF supplying the exact bytes for that identity")
    p.add_argument("--out", required=True, help="Empty folder for the fetched paper and the plan")
    p.add_argument("--workflow", default="ensemble")
    p.add_argument("--reviewers", type=int, default=2)
    p.add_argument("--literature-cutoff", default="")
    p.add_argument("--replace", action="store_true", help="Allow a new attempt on an already reviewed draft")
    p.set_defaults(func=cmd_prepare)

    p = sub.add_parser("publish", help="Write a review bundle from a finished engine run")
    p.add_argument("--prepared", required=True, help="The folder prepare wrote")
    p.add_argument("--run", required=True, help="The engine review output folder")
    p.add_argument(
        "--workspace",
        required=True,
        help="The imported manuscript workspace. Required: its paper.json is "
        "what ties this run to the paper that was prepared",
    )
    p.add_argument("--decision", required=True, choices=DECISIONS, help="The editor's decision, not the engine's")
    p.add_argument(
        "--editor",
        required=True,
        help="Who read the run and chose the decision. Published in the record, "
        "because an attestation with nobody behind it attests to nothing",
    )
    p.add_argument(
        "--human-reviewed",
        required=True,
        choices=("yes", "no"),
        help="Has the named editor read this run in full. There is no default. "
        "Answering no writes a rehearsal bundle that cannot be published",
    )
    p.add_argument(
        "--model",
        default="",
        help="Optional cross-check. The model is read from the run, and a "
        "value here that disagrees with it is a refusal rather than an override",
    )
    p.add_argument("--submitter", default="", help="GitHub login of the submitter, when there is one")
    p.add_argument(
        "--submitter-is-author",
        default="",
        choices=("", "yes", "no"),
        help="What the submitter claimed about their connection to the paper. "
        "Unverified either way, and recorded only with --submitter",
    )
    p.add_argument(
        "--baseline-eligible",
        action="store_true",
        help="Let this review set the paper's editorial status. Off by default, "
        "because one model wrote all of it",
    )
    p.add_argument("--publish", action="store_true", help="Write into docs/reviews rather than runs")
    p.add_argument("--offline", action="store_true", help="Skip the CLI authentication probe")
    p.set_defaults(func=cmd_publish)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except CommandError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
