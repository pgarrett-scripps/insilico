#!/usr/bin/env node

// The provenance file carries two record shapes. This checks the one the
// published corpus cannot: a review generated locally by the plugin inside
// peerreviewagents 0.9, which does not exist in docs/reviews yet, and the older
// records the schema has to keep accepting.
//
// The point of the version gate is that neither shape can be satisfied by
// filling the other one's fields with zeros. So these assertions are mostly
// about what the schema REFUSES. A version 4 record with no generator block,
// one admitting a paid API key, one naming a single model over a panel of
// agents that each ran on their own, or one whose stage ledger says a reader
// never reported, is the exact thing that must not be publishable, and a schema
// that accepted it would quietly let an overstated bundle onto the site.

import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { assertValidProvenance } from "../src/lib/reviewSchema.js";

const HASH = "a".repeat(64);
const PLUGIN_HASH = "b".repeat(64);
const WORKFLOW_HASH = "c".repeat(64);

const TRACKS = [
  "stats",
  "figures-tables",
  "methods-reporting",
  "citations",
  "consistency",
  "field",
];

function localRecord(overrides = {}) {
  return {
    schema_version: 4,
    generated_at: "2026-11-12T00:00:00+00:00",
    pipeline: { version: "0.9.0", sha: "" },
    insilico: { sha: "0".repeat(40) },
    generator: {
      kind: "local-claude-code-plugin",
      engine: { name: "peerreviewagents", version: "0.9.0" },
      engine_fingerprint: {
        algorithm: "sha256",
        file_count: 58,
        sha256: HASH,
        source: "run_manifest",
        matches_installed_engine: true,
      },
      plugin: {
        fingerprint: {
          algorithm: "sha256",
          file_count: 16,
          sha256: PLUGIN_HASH,
          source: "run_manifest",
        },
        workflow_sha256: WORKFLOW_HASH,
        workflow_version: "plugin-two-track-v1",
        finding_schema_version: "review-finding-v3",
        matches_installed_plugin: true,
      },
      transport: {
        provider: "claude-code",
        executable: "claude",
        version: "2.1.322",
        billing_policy: "claude-subscription-v1",
        login_verified: true,
        verified_by: "run_startup_probe",
        verified_at: "2026-11-12T09:14:02+00:00",
        paid_api_key_used: false,
      },
      agents: [
        {
          slot: "reviewer-1",
          role: "reviewer",
          track: "body",
          attempt: 1,
          tool_calls: 18,
          model: "claude-sonnet-5-5",
          state: "complete",
          tokens: 142000,
          findings: 12,
          none_found: false,
        },
        {
          slot: "audit-stats",
          role: "specialist",
          track: "stats",
          attempt: 1,
          tool_calls: 9,
          model: "claude-sonnet-5-5",
          findings: 4,
          none_found: false,
        },
        {
          slot: "editor",
          role: "editor",
          attempt: 1,
          tool_calls: 6,
          model: "claude-sonnet-5-5",
        },
        {
          slot: "recorder",
          role: "recorder",
          attempt: 1,
          model: "claude-haiku-5-5",
        },
      ],
      input: {
        kind: "doi",
        identifier: "10.1101/2026.03.12.711120",
        sha256: HASH,
        bytes: 1024,
        local_file: false,
        workspace_manifest_sha256: HASH,
      },
      run: {
        directory: "runs/local/2026/fixture-paper/review",
        arm: "full-two-track",
        provider: "claude-code",
        workflow_version: "plugin-two-track-v1",
        finding_schema_version: "review-finding-v3",
        reviewers: 3,
        specialist_tracks: TRACKS,
        paper_id: "fixture-paper",
        claude_code_version: "2.1.322",
        status: "complete",
        publishable: true,
        findings_source: "editor-package",
        review_guard_status: "clean",
        completeness: {
          required: ["reviewer-1", "reviewer-2", "reviewer-3", ...TRACKS, "editor"],
          reported: ["reviewer-1", "reviewer-2", "reviewer-3", ...TRACKS, "editor"],
          missing: [],
          none_found: ["consistency"],
          editor_accepted: true,
          attempts: { "reviewer-1": 1, "audit-stats": 2 },
          retried: ["audit-stats"],
        },
        findings: 8,
        appendix_findings: 45,
        escalated_in_bundle: 4,
        findings_delivered: 53,
        findings_submitted: 53,
        quarantined_findings_count: 0,
        escalated_count: 4,
        findings_by_track: { stats: 9, citations: 7 },
        wall_seconds: 246.5,
        tokens_total: 636299,
        errors: [],
      },
      advisory_verdict: {
        significance: "moderate",
        strength_of_evidence: "moderate",
      },
      decision_source: "human_editor",
      attestation: {
        locally_generated: true,
        human_reviewed_before_merge: true,
        rehearsal: false,
        editor: "fixture-editor",
        statement:
          "This review was generated locally on a Claude Code subscription, with no paid API key in the path.",
      },
    },
    review: {
      id: "docs/reviews/2026/fixture-paper/v1/r1",
      manuscript_version: 1,
      attempt: 1,
      kind: "review",
      lifecycle: "active",
      baseline_eligible: false,
      route: "v1/r1",
    },
    provider: "claude-code",
    models: {
      "reviewer-1": "claude-sonnet-5-5",
      "audit-stats": "claude-sonnet-5-5",
      editor: "claude-sonnet-5-5",
      recorder: "claude-haiku-5-5",
    },
    decision: "major",
    desk_rejected: false,
    round: 1,
    ingest: { format: "markdown", tool: "peerreviewagents import_paper" },
    panel: [],
    total_cost_usd: null,
    errors: [],
    preprint: {
      url: "https://www.biorxiv.org/content/10.1101/2026.03.12.711120v1",
      source: "biorxiv",
      title: "Fixture paper",
    },
    ...overrides,
  };
}

function rejects(record, why) {
  assert.throws(() => assertValidProvenance(record, "fixture"), /invalid review provenance/, why);
}

// The shape the local generator writes is publishable.
assertValidProvenance(localRecord(), "fixture");

// A record claiming to be local without saying how it was produced is not.
const noGenerator = localRecord();
delete noGenerator.generator;
rejects(noGenerator, "a version 4 record must carry a generator block");

// The whole point of the retirement. A record that admits a paid key is not a
// local subscription review and cannot pass as one.
const paid = localRecord();
paid.generator.transport.paid_api_key_used = true;
rejects(paid, "a paid API key must not validate as a local review");

// Where the transport claim came from. The run's own start-up probe is the only
// source: 0.9 proves a Claude Code session loaded the plugin and connected the
// MCP server before it spends anything, and writes that proof into startup.json.
// The publish-time probe asked the installed CLI who was logged in at the moment
// the bundle was written, which is a fact about the publishing machine, and 0.9
// exposes no authentication status to ask.
const probed = localRecord();
probed.generator.transport.verified_by = "publish_time_probe";
rejects(probed, "a login read on the publishing machine does not describe the run");

const confirmed = localRecord();
confirmed.generator.transport.verified_by = "run_billing_confirmation";
rejects(confirmed, "a login read from a file the engine never writes is not a source");

const unprobed = localRecord();
delete unprobed.generator.transport.verified_by;
rejects(unprobed, "a record must say where the transport claim was read");

const undated = localRecord();
delete undated.generator.transport.verified_at;
rejects(undated, "a record must say when the run's probe ran");

// This path publishes Claude Code runs only, and every claim the bundle makes
// about how the review was paid for is a claim about a Claude subscription.
const otherTransport = localRecord();
otherTransport.generator.transport.provider = "codex";
rejects(otherTransport, "a run on another transport must not carry the subscription claim");

const otherRunTransport = localRecord();
otherRunTransport.generator.run.provider = "codex";
rejects(otherRunTransport, "the run's own transport is checked as well as the record's");

// The engine offers an advisory judgement and recommends no verdict, so nothing
// else may be named as the author of the decision.
const machineDecision = localRecord();
machineDecision.generator.decision_source = "engine";
rejects(machineDecision, "only a human editor may be recorded as deciding");

// The judgement itself is published rather than discarded, so the record has to
// carry it even when the arm produced an empty one.
const noJudgement = localRecord();
delete noJudgement.generator.advisory_verdict;
rejects(noJudgement, "a record must carry the engine's advisory judgement");

const emptyJudgement = localRecord();
emptyJudgement.generator.advisory_verdict = {};
assertValidProvenance(emptyJudgement, "an arm that runs no editor produces no judgement");

// A zero would read as a measured free run rather than an absent figure.
const zeroCost = localRecord();
zeroCost.total_cost_usd = 0;
rejects(zeroCost, "a subscription run records no dollar figure");

// A truncated hash is the failure mode of a hand-edited record.
const shortHash = localRecord();
shortHash.generator.engine_fingerprint.sha256 = "abc";
rejects(shortHash, "the engine fingerprint must be a full sha256");

// The plugin is what reviews the paper in 0.9, and the engine release does not
// identify it: two runs can both say plugin-two-track-v1 over different agent
// prompts. Its own bytes, and the hash of the workflow that decides which
// agents run, are part of the record.
const noPlugin = localRecord();
delete noPlugin.generator.plugin;
rejects(noPlugin, "a plugin run must identify the plugin that ran");

const noWorkflow = localRecord();
delete noWorkflow.generator.plugin.workflow_sha256;
rejects(noWorkflow, "the record must say which workflow produced the review");

const shortWorkflow = localRecord();
shortWorkflow.generator.plugin.workflow_sha256 = "abc";
rejects(shortWorkflow, "the workflow hash must be a full sha256");

const unsourcedPlugin = localRecord();
delete unsourcedPlugin.generator.plugin.fingerprint.source;
rejects(unsourcedPlugin, "the plugin fingerprint must say where it was measured");

// The plugin pins a model inside each agent file, so the panel is a list of
// slots with their own models. One id at the top would describe a panel that did
// not sit, and an empty table would say nothing wrote the review.
const singleModel = localRecord();
singleModel.model = "claude-sonnet-5-5";
rejects(singleModel, "a plugin run must not name one model for the whole panel");

const noModels = localRecord();
noModels.models = {};
rejects(noModels, "a record naming no model does not say what wrote the review");

const noAgents = localRecord();
noAgents.generator.agents = [];
rejects(noAgents, "a review with no agent that ran is not a review");

const anonymousAgent = localRecord();
delete anonymousAgent.generator.agents[0].slot;
rejects(anonymousAgent, "an agent row must say which slot it was");

// An attestation is a claim about a person. Without the person it is a constant
// the generator wrote before anyone had read anything, which is what it used to
// be.
const anonymous = localRecord();
delete anonymous.generator.attestation.editor;
rejects(anonymous, "an attestation must name the editor who read the run");

const emptyEditor = localRecord();
emptyEditor.generator.attestation.editor = "";
rejects(emptyEditor, "an empty editor name is not an editor");

// A rehearsal says false here. It is not a publishable record.
const unread = localRecord();
unread.generator.attestation.human_reviewed_before_merge = false;
rejects(unread, "a run no editor has read must not validate as published");

// A rehearsal is a rehearsal wherever its folder ends up. Until the record said
// so, the only thing that distinguished one from a published review was which
// directory it sat in, and a directory can be copied.
const rehearsed = localRecord();
rehearsed.generator.attestation.rehearsal = true;
rejects(rehearsed, "a rehearsal must not validate as a published review");

const silentAboutRehearsal = localRecord();
delete silentAboutRehearsal.generator.attestation.rehearsal;
rejects(silentAboutRehearsal, "a record must say whether it was a rehearsal");

// The facts a hand-copied rehearsal gets wrong. Each one is refused on its own,
// so no single omission lets such a bundle through.
const unverifiedLogin = localRecord();
unverifiedLogin.generator.transport.login_verified = false;
rejects(unverifiedLogin, "an unverified login must not validate as published");

const silentAboutLogin = localRecord();
delete silentAboutLogin.generator.transport.login_verified;
rejects(silentAboutLogin, "a record must say whether the login was verified");

const noCliVersion = localRecord();
delete noCliVersion.generator.transport.version;
rejects(noCliVersion, "a record that cannot name the harness version did not come from a session");

const blockedRun = localRecord();
blockedRun.generator.run.status = "blocked";
rejects(blockedRun, "a run that stopped part way is not a review");

const silentAboutStatus = localRecord();
delete silentAboutStatus.generator.run.status;
rejects(silentAboutStatus, "a record must say that the run finished");

// The engine answers the publish question itself in 0.9, from read_run, and the
// record carries its answer rather than this repository's reading of the same
// files. A record that admits the engine refused the run, or that omits the
// flag, is not a bundle the gate let through.
const unpublishable = localRecord();
unpublishable.generator.run.publishable = false;
rejects(unpublishable, "a run the engine refused must not validate as published");

const silentAboutPublishable = localRecord();
delete silentAboutPublishable.generator.run.publishable;
rejects(silentAboutPublishable, "a record must carry the engine's own publish flag");

// Where the published findings came from. The engine rebuilds a pool from
// findings.jsonl when the editor package is missing or damaged, and that pool
// carries no editorial placement: no body, no appendix, no rulings. Publishing
// it would present the raw submissions as the editor's letter.
const rebuiltPool = localRecord();
rebuiltPool.generator.run.findings_source = "findings-ledger";
rejects(rebuiltPool, "findings rebuilt from the ledger are not the editor's review");

const silentAboutSource = localRecord();
delete silentAboutSource.generator.run.findings_source;
rejects(silentAboutSource, "a record must say where its findings came from");

// A review written before a rate limit stopped the session is complete and
// publishable, and the note is the only thing that says the session did not end
// cleanly, so it is published.
const noteworthy = localRecord();
noteworthy.generator.run.note =
  "the review was written and the run was marked blocked afterwards: the token ceiling was reached";
assertValidProvenance(noteworthy, "a run blocked after the review was written still publishes");

// The two fields the engine sets for a run it could not read as a whole. Neither
// can be true of a run it calls publishable, so a record carrying one is a
// record whose own explanation of its failure travelled with it.
const excused = localRecord();
excused.generator.run.cause = "the session ended before the editor wrote the review";
rejects(excused, "a published record must not carry the reason the run stopped");

const damaged = localRecord();
damaged.generator.run.problems = ["editor-package.json: truncated"];
rejects(damaged, "a published record must not carry a run file the engine could not read");

// The arm replaces 0.8's mode and review policy, and it is the single name for
// what the run was asked to do. A record without it cannot say whether three
// reviewers and six specialist tracks were even asked for.
const noArm = localRecord();
delete noArm.generator.run.arm;
rejects(noArm, "a record must name the arm the run used");

const noReviewerCount = localRecord();
delete noReviewerCount.generator.run.reviewers;
rejects(noReviewerCount, "a record must say how many reviewers read the paper");

// The stage ledger is the only thing that says whether the review is whole. A
// run can reach complete with a stage that never reported, when the editor agent
// accepted the pool without it, and a bundle describing readers that did not
// report is a claim about a panel that did not sit.
const incomplete = localRecord();
incomplete.generator.run.completeness.missing = ["audit-field"];
rejects(incomplete, "a review with a stage that never reported must not publish");

const noLedger = localRecord();
delete noLedger.generator.run.completeness;
rejects(noLedger, "a record must carry the ledger that says the review is whole");

const noneFound = localRecord();
noneFound.generator.run.completeness.none_found = TRACKS;
assertValidProvenance(noneFound, "a track that reported nothing to report answered");

// A review that read the manuscript end to end and raised nothing is a result,
// and the record of it is `complete` with `review_guard_status: clean` and no
// findings. It has to validate, or the corpus can never hold a sound paper.
const foundNothing = localRecord();
foundNothing.generator.run.review_guard_status = "clean";
foundNothing.generator.run.findings = 0;
foundNothing.generator.run.findings_delivered = 0;
assertValidProvenance(foundNothing, "fixture");

// `quarantined` is the engine's other guard word, and it means the guards took
// something, however much. A review that lost a finding whose quote could not
// be anchored still endorses the rest, so it validates and carries the count of
// what was held back.
const someLost = localRecord();
someLost.generator.run.review_guard_status = "quarantined";
someLost.generator.run.quarantined_findings_count = 3;
assertValidProvenance(someLost, "fixture");

// There is no third guard word. The two the engine writes are the whole enum,
// so a record carrying any other verdict was not written from a run this
// engine produced, whatever the word claims.
const inventedGuard = localRecord();
inventedGuard.generator.run.review_guard_status = "partially-quarantined";
rejects(inventedGuard, "a guard verdict the engine never writes must not validate");

// The engine's other finished state is not a review. It writes
// `complete-without-findings` when the editor delivered nothing, and such a
// record published as a clean result would tell the authors the reviewers
// recorded nothing against their paper, which is a different claim.
const everythingQuarantined = localRecord();
everythingQuarantined.generator.run.status = "complete-without-findings";
rejects(everythingQuarantined, "the quarantined outcome is not a review of a sound paper");

// Whether the reviewed bytes were fetched from the identifier or handed over
// from a local disk decides whether the hash means anything to a reader.
const noProvenanceOfBytes = localRecord();
delete noProvenanceOfBytes.generator.input.local_file;
rejects(noProvenanceOfBytes, "the record must say whether the PDF came from the identifier");

// A fingerprint of the publishing machine's installed engine is a different
// claim from a fingerprint of the code that ran, so the record has to say which.
const unsourcedFingerprint = localRecord();
delete unsourcedFingerprint.generator.engine_fingerprint.source;
rejects(unsourcedFingerprint, "the fingerprint must say where it was measured");

// A published record is read by people who do not have the machine that wrote
// it. An absolute path names a home directory on one laptop, which tells a
// reader nothing about the review and quite a lot about the author's disk.
const absoluteRunDirectory = localRecord();
absoluteRunDirectory.generator.run.directory = "/home/someone/Repos/insilico/runs/local/2026/fixture";
rejects(absoluteRunDirectory, "the run directory must be relative to the repository");

const absoluteReviewId = localRecord();
absoluteReviewId.review.id = "/home/someone/Repos/insilico/docs/reviews/2026/fixture-paper/v1/r1";
rejects(absoluteReviewId, "the bundle identifier must not be an absolute path");

// The shape the engine's deleted Python orchestration wrote. It was never
// published, and 0.9 cannot produce it: the modules behind the debate, the
// single requested model and the publish-time login probe are gone. A schema
// that still accepted it would accept a record no run can now back up.
const versionThree = localRecord({ schema_version: 3 });
rejects(versionThree, "the retired local shape must no longer validate");

// The hosted panel's records still have to validate exactly as before, and its
// obligations must not have leaked onto the local shape.
const published = [];
const publishedFiles = [];
function visit(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const target = path.join(directory, entry.name);
    if (entry.isDirectory()) visit(target);
    else if (entry.name === "provenance.json") {
      published.push(JSON.parse(fs.readFileSync(target, "utf8")));
      publishedFiles.push(target);
    }
  }
}
visit(path.resolve("docs/reviews"));

// The schema can only police the two fields that have carried a path so far.
// This is the standing rule underneath it, applied to every published record
// whatever shape it is: nothing in the corpus names a path on anybody's
// machine. It passes today and exists so that it stops being true loudly.
function localPaths(value, trail = "") {
  if (typeof value === "string") {
    return value.startsWith("/") || value.startsWith("file://") ? [`${trail} = ${value}`] : [];
  }
  if (Array.isArray(value)) return value.flatMap((item, index) => localPaths(item, `${trail}[${index}]`));
  if (value && typeof value === "object") {
    return Object.entries(value).flatMap(([key, item]) => localPaths(item, trail ? `${trail}.${key}` : key));
  }
  return [];
}
for (const [index, record] of published.entries()) {
  const leaks = localPaths(record);
  assert.equal(
    leaks.length,
    0,
    `${publishedFiles[index]} names a path on the machine that wrote it: ${leaks.join(", ")}`,
  );
}
assert.ok(
  localPaths(localRecord({ review: { id: "/home/someone/r1" } })).length === 1,
  "the path scan should see an absolute value when there is one",
);

const versionTwo = published.filter((p) => p.schema_version === 2);
assert.ok(versionTwo.length > 0, "there should still be published version 2 records to check");
for (const record of versionTwo) assertValidProvenance(record, "published");

const strippedPanel = JSON.parse(JSON.stringify(versionTwo[0]));
delete strippedPanel.total_cost_usd;
rejects(strippedPanel, "a version 2 record still owes the panel's full accounting");

// Records written before versioning existed are skipped rather than rewritten.
const unversioned = published.filter((p) => p.schema_version == null);
assert.ok(unversioned.length > 0, "the unversioned records should still be present");
for (const record of unversioned) assertValidProvenance(record, "legacy");
assertValidProvenance({ nonsense: true }, "legacy");

// And the site has to read a plugin bundle without an editorial status. The
// model table is per slot and real, so the heuristic that calls a bundle graded
// is satisfied, and the explicit flag in the record is what decides whether this
// review speaks for the paper. It does not, until an editor says so.
const root = fs.mkdtempSync(path.join(os.tmpdir(), "insilico-local-"));
const bundle = path.join(root, "2026", "fixture-paper", "v1", "r1");
fs.mkdirSync(bundle, { recursive: true });
fs.writeFileSync(path.join(bundle, "summary.md"), "# Review Summary\n");
fs.writeFileSync(path.join(bundle, "audit_stats.md"), "# Statistics audit\n");
fs.writeFileSync(path.join(bundle, "provenance.json"), JSON.stringify(localRecord()));
process.env.INSILICO_REVIEWS_DIR = root;
const { corpus } = await import("../src/lib/corpus.js");
const paper = corpus().find((entry) => entry.slug === "fixture-paper");
assert.ok(paper, "a local bundle should appear in the corpus");
assert.equal(paper.bundles.length, 1);
assert.equal(paper.bundles[0].graded, true, "a per-slot model table is a real model table");
assert.equal(
  paper.bundles[0].baselineEligible,
  false,
  "the record's own flag decides, and a local review is experimental by default",
);
assert.equal(paper.decisive, null, "nothing experimental may set the paper's status");
assert.deepEqual(
  paper.bundles[0].documents.audits.map((doc) => doc.file),
  ["audit_stats.md"],
  "a specialist report in the bundle should be listed as a report of its own",
);

// A track report is named by the question its specialist was asked, not by its
// filename with the underscore taken out. `Stats` would have been the label and
// it says nothing, so the mapping is asserted rather than left to a reader of
// the page to notice.
const stats = paper.bundles[0].documents.audits[0];
assert.equal(stats.label, "Statistics", `a track report carries its track's name: ${stats.label}`);
assert.ok(stats.blurb, "a track report says what its specialist read for");
assert.equal(paper.bundles[0].plugin, true, "a version 4 record is read as a plugin run");

// The arm asked for six tracks and the bundle holds one, so the page has five
// gaps to name. A reader cannot be expected to find them by counting headings.
assert.deepEqual(
  (paper.bundles[0].tracksAsked || []).filter(
    (track) => !paper.bundles[0].documents.audits.some((d) => d.file === `audit_${track}.md`),
  ),
  ["figures-tables", "methods-reporting", "citations", "consistency", "field"],
  "a track the arm asked for with no report in the bundle is a gap the page names",
);
fs.rmSync(root, { recursive: true, force: true });

console.log("ok  plugin provenance validates, the paid and retired paths cannot, and older records still read");
