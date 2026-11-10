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
    "paid API key in the path. A human editor read the run and chose the "
    "decision before the review was merged, and merging is what publishes it."
)

# Documents a local bundle writes. Shorter than the hosted panel's list by
# design: there was no desk screen, no five-reviewer panel and no debate, so
# those files are absent rather than present and empty.
BUNDLE_DOCUMENTS = ("summary.md", "decision_letter.md", "manuscript_stats.md")
SEVERITY_ORDER = {"major": 0, "moderate": 1, "minor": 2}
REQUIRED_SEVERITIES = ("major", "moderate")


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
            "PeerReviewAgents 0.7.0 or newer is not importable. Install it, or "
            "run this with the paper-workbench virtual environment on PATH."
        ) from exc


def engine_fingerprint() -> dict:
    """Hash the engine source tree, not just its version number.

    Two reviews can both claim engine 0.7.0 and have run different bytes, one
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


def transport_record(*, probe: bool = True) -> dict:
    """Which CLI ran the models, and on whose account.

    ``paid_api_key_used`` is a constant here and a constant in the schema. This
    path cannot reach a paid key, so the field is a statement about the design
    rather than a measurement, and a record needing it to be true is not a local
    review and has no business in this shape.
    """
    billing = importlib.import_module(f"{ENGINE_PACKAGE}.billing")
    record = {
        "provider": TRANSPORT_PROVIDER,
        "executable": "claude",
        "version": None,
        "billing_policy": str(getattr(billing, "CLAUDE_POLICY", "claude-subscription-v1")),
        "auth_method": None,
        "subscription_type": None,
        "paid_api_key_used": False,
    }
    if not probe:
        return record
    runtime = importlib.import_module(f"{ENGINE_PACKAGE}.model_runtime")
    status = runtime.auth_status(provider=TRANSPORT_PROVIDER)
    record["auth_method"] = status.get("authMethod")
    record["subscription_type"] = status.get("subscriptionType")
    if status.get("apiProvider"):
        raise CommandError(
            "The Claude CLI is authenticated against a paid API provider rather "
            "than a subscription. Run `claude /login` and choose the "
            "subscription account before generating a review."
        )
    return record


def observed_models(run_dir: Path) -> list[str]:
    """Model ids the run actually reported, as opposed to the one requested.

    Read back out of the run rather than assumed. A transport that silently
    served a different model is exactly the thing a reader would want to know,
    and the only place it is recorded is the saved stream assessment.
    """
    found: set[str] = set()
    for path in sorted(Path(run_dir).rglob("*.json")):
        try:
            payload = read_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        for key, value in _walk(payload):
            if key in ("model", "model_id", "observed_model") and isinstance(value, str) and value:
                found.add(value)
    return sorted(found)


def _walk(value: object):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key, child
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


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


def run_artifact(run_dir: Path) -> dict:
    for candidate in (Path(run_dir) / "core-artifact.json", Path(run_dir) / "core-run" / "core-artifact.json"):
        if candidate.is_file():
            return read_json(candidate)
    return {}


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
        "One model wrote this review, start to finish, on a Claude Code "
        "subscription on the editor's own machine. There was no desk screen, no "
        "five-reviewer panel and no debate round, so nothing checked the "
        "reviewer that was any better than the reviewer. Read it as one careful "
        "reading of the manuscript rather than as a panel verdict.",
        "",
        "The decision above was chosen by a human editor after reading the run. "
        "The engine grades findings and does not recommend a verdict.",
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
    lines = [
        f"# Decision Letter: {preprint.title or 'Untitled submission'}",
        "",
        f"**Decision:** {provenance['decision'].title()}",
        "",
        "This letter reports one locally generated review. The decision is the "
        "editor's, taken after reading the run in full. Everything below it is "
        "the reviewer's, quoted or paraphrased from the saved output rather than "
        "rewritten.",
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
    artifact: dict,
    decision: str,
    route: str,
    draft: int,
    attempt: int,
    submitter: str,
    submitter_is_author: str,
    baseline_eligible: bool,
    ingest: dict,
    observed: list[str],
    requested_model: str,
    probe: bool,
    review_id: str,
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
    generator = {
        "kind": GENERATOR_KIND,
        "engine": engine_record(),
        "engine_fingerprint": engine_fingerprint(),
        "transport": transport_record(probe=probe),
        "model_ids": {"requested": requested_model, "observed": observed},
        "input": prepared["input"],
        "run": {
            "workflow": str(artifact.get("workflow") or prepared.get("workflow") or "ensemble"),
            "reviewers": int(prepared.get("reviewers") or 1),
            "literature_cutoff": str(prepared.get("literature_cutoff") or ""),
            "artifact_version": str(artifact.get("artifact_version") or ""),
            "findings": len(findings),
        },
        "decision_source": "human_editor",
        "attestation": {
            "locally_generated": True,
            "human_reviewed_before_merge": True,
            "statement": ATTESTATION,
        },
    }
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
        "provider": TRANSPORT_PROVIDER,
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
        "errors": [str(e) for e in artifact.get("errors") or []],
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
        "transport": transport_record(probe=not args.offline),
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
    if args.publish and args.decision not in DECISIONS:
        raise CommandError(f"--decision must be one of: {', '.join(DECISIONS)}")

    run_dir = Path(args.run).resolve()
    package = editor_package(run_dir)
    artifact = run_artifact(run_dir)
    workspace = Path(args.workspace).resolve() if args.workspace else None
    preprint_data = prepared.get("preprint")
    if preprint_data is None:
        raise CommandError("A bundle needs preprint metadata. Prepare with --paper.")
    preprint = Preprint(**preprint_data)

    ingest = ingest_record(workspace)
    if workspace is not None and (workspace / "manifest.json").is_file():
        prepared["input"]["workspace_manifest_sha256"] = digest(
            (workspace / "manifest.json").read_bytes()
        )

    dest = Path(prepared["destination"])
    route = f"v{prepared['draft']}/r{prepared['attempt']}"
    review_id = str(dest.relative_to(REPO)) if dest.is_relative_to(REPO) else str(dest)
    provenance = build_provenance(
        preprint=preprint,
        prepared=prepared,
        package=package,
        artifact=artifact,
        decision=args.decision,
        route=route,
        draft=int(prepared["draft"]),
        attempt=int(prepared["attempt"]),
        submitter=args.submitter,
        submitter_is_author=args.submitter_is_author,
        baseline_eligible=args.baseline_eligible,
        ingest=ingest,
        observed=observed_models(run_dir),
        requested_model=args.model,
        probe=not args.offline,
        review_id=review_id,
    )

    findings = sorted_findings(package)
    if dest.exists() and any(dest.iterdir()):
        raise CommandError(f"Refusing to overwrite an existing review bundle: {dest}")
    dest.mkdir(parents=True, exist_ok=True)

    (dest / "summary.md").write_text(
        render_summary(preprint, package, provenance, findings), encoding="utf-8"
    )
    (dest / "decision_letter.md").write_text(
        render_decision_letter(preprint, package, provenance, findings), encoding="utf-8"
    )
    (dest / "manuscript_stats.md").write_text(
        render_stats(preprint, ingest, provenance["generator"]), encoding="utf-8"
    )
    write_json(dest / "provenance.json", provenance)
    write_round_record(dest, preprint, provenance, findings)
    # Kept beside the documents so a reader can check a quotation against the
    # structured record the reviewer actually produced.
    write_json(dest / "editor-package.json", package)
    write_manifest(dest)

    print(f"bundle   {dest}")
    print(f"decision {provenance['decision']} (chosen by the editor)")
    print(f"findings {len(findings)}")
    print(f"baseline {'eligible' if provenance['review']['baseline_eligible'] else 'experimental only'}")
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
    p.add_argument("--workspace", help="The imported manuscript workspace")
    p.add_argument("--decision", required=True, choices=DECISIONS, help="The editor's decision, not the engine's")
    p.add_argument("--model", default=DEFAULT_MODEL, help="The model id requested for the run")
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
