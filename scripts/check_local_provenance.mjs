#!/usr/bin/env node

// The provenance file now carries two record shapes. This checks the one the
// published corpus cannot: a locally generated review, which does not exist in
// docs/reviews yet, and the old records it has to keep accepting.
//
// The point of the version gate is that neither shape can be satisfied by
// filling the other one's fields with zeros. So these assertions are mostly
// about what the schema REFUSES. A version 3 record with no generator block, or
// one admitting a paid API key, is the exact thing that must not be publishable,
// and a schema that accepts it would quietly let the hosted path back in.

import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { assertValidProvenance } from "../src/lib/reviewSchema.js";

const HASH = "a".repeat(64);

function localRecord(overrides = {}) {
  return {
    schema_version: 3,
    generated_at: "2026-11-10T00:00:00+00:00",
    pipeline: { version: "0.7.0", sha: "" },
    insilico: { sha: "0".repeat(40) },
    generator: {
      kind: "local-claude-code",
      engine: { name: "peerreviewagents.engine", version: "0.7.0" },
      engine_fingerprint: { algorithm: "sha256", file_count: 42, sha256: HASH },
      transport: {
        provider: "claude-code",
        executable: "claude",
        version: "2.0.0",
        billing_policy: "claude-subscription-v1",
        auth_method: "claude.ai",
        subscription_type: "max",
        paid_api_key_used: false,
      },
      model_ids: { requested: "claude-sonnet-5-5", observed: ["claude-sonnet-5-5"] },
      input: { kind: "doi", identifier: "10.1101/2026.03.12.711120", sha256: HASH, bytes: 1024 },
      run: { workflow: "ensemble", reviewers: 2, literature_cutoff: "2026-11-10", findings: 7 },
      decision_source: "human_editor",
      attestation: {
        locally_generated: true,
        human_reviewed_before_merge: true,
        statement:
          "This review was generated locally on a Claude Code subscription, with no paid API key in the path.",
      },
    },
    review: { manuscript_version: 1, attempt: 1, lifecycle: "active", baseline_eligible: false },
    provider: "claude-code",
    model: "claude-sonnet-5-5",
    models: {},
    decision: "major",
    desk_rejected: false,
    round: 1,
    ingest: { format: "markdown", tool: "peerreviewagents.engine import" },
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
rejects(noGenerator, "a version 3 record must carry a generator block");

// The whole point of the retirement. A record that admits a paid key is not a
// local subscription review and cannot pass as one.
const paid = localRecord();
paid.generator.transport.paid_api_key_used = true;
rejects(paid, "a paid API key must not validate as a local review");

// The engine recommends no verdict, so nothing else may be named as the author
// of the decision.
const machineDecision = localRecord();
machineDecision.generator.decision_source = "engine";
rejects(machineDecision, "only a human editor may be recorded as deciding");

// A zero would read as a measured free run rather than an absent figure.
const zeroCost = localRecord();
zeroCost.total_cost_usd = 0;
rejects(zeroCost, "a subscription run records no dollar figure");

// A truncated hash is the failure mode of a hand-edited record.
const shortHash = localRecord();
shortHash.generator.engine_fingerprint.sha256 = "abc";
rejects(shortHash, "the engine fingerprint must be a full sha256");

// The hosted panel's records still have to validate exactly as before, and its
// obligations must not have leaked onto the local shape.
const published = [];
function visit(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const target = path.join(directory, entry.name);
    if (entry.isDirectory()) visit(target);
    else if (entry.name === "provenance.json") published.push(JSON.parse(fs.readFileSync(target, "utf8")));
  }
}
visit(path.resolve("docs/reviews"));

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

// And the site has to read a local bundle without an editorial status. One model
// wrote all of it, so it is a published experiment until an editor says
// otherwise, the same rule the single-model hosted runs get.
const root = fs.mkdtempSync(path.join(os.tmpdir(), "insilico-local-"));
const bundle = path.join(root, "2026", "fixture-paper", "v1", "r1");
fs.mkdirSync(bundle, { recursive: true });
fs.writeFileSync(path.join(bundle, "summary.md"), "# Review Summary\n");
fs.writeFileSync(path.join(bundle, "provenance.json"), JSON.stringify(localRecord()));
process.env.INSILICO_REVIEWS_DIR = root;
const { corpus } = await import("../src/lib/corpus.js");
const paper = corpus().find((entry) => entry.slug === "fixture-paper");
assert.ok(paper, "a local bundle should appear in the corpus");
assert.equal(paper.bundles.length, 1);
assert.equal(paper.bundles[0].graded, false, "an empty model table is not a graded panel");
assert.equal(paper.bundles[0].baselineEligible, false, "a local review is experimental by default");
assert.equal(paper.decisive, null, "nothing experimental may set the paper's status");
fs.rmSync(root, { recursive: true, force: true });

console.log("ok  local provenance validates, the paid path cannot, and older records still read");
