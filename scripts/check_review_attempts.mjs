import assert from "node:assert/strict"
import fs from "node:fs"
import os from "node:os"
import path from "node:path"

const root = fs.mkdtempSync(path.join(os.tmpdir(), "insilico-attempts-"))
const paper = path.join(root, "2026", "paper")

function writeAttempt(paperDir, number, eligible) {
  const bundle = path.join(paperDir, "v1", `r${number}`)
  fs.mkdirSync(bundle, { recursive: true })
  fs.writeFileSync(path.join(bundle, "summary.md"), "# Summary\n")
  fs.writeFileSync(path.join(bundle, "provenance.json"), JSON.stringify({
    generated_at: `2026-01-0${number}T00:00:00Z`,
    decision: number === 3 ? "accept" : "major",
    models: eligible ? { reviewer: { model: "graded" } } : {},
    review: {
      attempt: number,
      baseline_eligible: eligible,
      lifecycle: "active",
    },
    preprint: {
      title: "Fixture paper",
      identifier: "fixture",
      version: "1",
    },
  }))
}

try {
  writeAttempt(paper, 1, true)
  writeAttempt(paper, 2, true)
  writeAttempt(paper, 3, false)
  writeAttempt(path.join(root, "2026", "experiment"), 1, false)
  process.env.INSILICO_REVIEWS_DIR = root
  const { corpus } = await import("../src/lib/corpus.js")
  const found = corpus().find((entry) => entry.slug === "paper")
  const experiment = corpus().find((entry) => entry.slug === "experiment")

  assert.deepEqual(found.bundles.map((bundle) => bundle.label), [
    "v1/r3",
    "v1/r2",
    "v1/r1",
  ])
  assert.equal(found.latest.label, "v1/r3")
  assert.equal(found.decisive.label, "v1/r2")
  assert.equal(found.status, "declined")
  assert.equal(found.bundles[0].route, "v1/r3")
  assert.equal(experiment.decisive, null)
  assert.equal(experiment.status, "experimental")
  console.log("Nested review attempts preserve the latest eligible baseline")
} finally {
  fs.rmSync(root, { recursive: true, force: true })
}
