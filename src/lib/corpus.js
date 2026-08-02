/**
 * The published corpus, read straight out of `docs/reviews/`.
 *
 * The Python pipeline owns that directory and writes two kinds of thing into
 * each `<year>/<slug>/v<N>/` bundle: the referee documents as plain markdown,
 * and `provenance.json` as the machine-readable record of the run. This module
 * turns that on-disk layout into the shape the site renders from.
 *
 * Deliberately reading the pipeline's own output rather than a copy under
 * `src/`: a review bundle is the published artifact and the thing a citation
 * points at, so there must be exactly one of it. A build step that duplicated
 * bundles into the site tree would make "what did the panel actually say" a
 * question with two possible answers.
 *
 * Nothing here parses markdown. Astro renders the documents; this only walks
 * the tree and reads JSON, so a malformed report can never break the index.
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
export const REPO = path.resolve(HERE, "../..");
export const REVIEWS_DIR = path.join(REPO, "docs", "reviews");

export const VERDICT = {
  accept: "Accept",
  minor: "Minor revision",
  major: "Major revision",
  reject: "Reject",
};

/** Bundle documents, in the order a reader should meet them. */
const DOCUMENT_ORDER = [
  ["summary.md", "Summary", "The panel's assessment in brief."],
  ["decision_letter.md", "Decision letter", "The editor's verdict and what it requires."],
  ["integrity.md", "Submission integrity scan", "Deterministic scan for text concealed from human readers."],
  ["desk_screen.md", "Desk screen", "Whether the submission cleared the bar for full review."],
  ["meta_review.md", "Area chair synthesis", "Ten reports weighed into one assessment."],
  ["author_rebuttal.md", "Simulated author rebuttal", "The authors' side, argued for the editor to weigh."],
  ["debate_transcript.md", "Advocate / skeptic debate", "The case for and against, in full."],
  ["journal_recommendations.md", "Venue suggestions", "Where this might be submitted."],
];

const readJSON = (file) => {
  try {
    return JSON.parse(fs.readFileSync(file, "utf8"));
  } catch {
    return null;
  }
};

const readDirs = (dir) => {
  try {
    return fs.readdirSync(dir, { withFileTypes: true })
      .filter((e) => e.isDirectory())
      .map((e) => e.name);
  } catch {
    return [];
  }
};

/** Turn `review_data_analysis.md` into `Data analysis`. */
export function titleFromFilename(name) {
  const stem = name.replace(/\.md$/, "").replace(/^(review|audit)_/, "");
  const words = stem.replace(/_/g, " ");
  return words.charAt(0).toUpperCase() + words.slice(1);
}

/**
 * Every document in one bundle, split by the role it played.
 *
 * On a desk reject the pipeline writes the same body to decision_letter,
 * desk_screen and integrity, so those arrive byte-identical. Each distinct
 * body is listed once — a reader following a direct link still finds the file,
 * but the page doesn't show one text under three headings.
 */
function readDocuments(bundleDir) {
  const files = (() => {
    try {
      return fs.readdirSync(bundleDir).filter((f) => f.endsWith(".md"));
    } catch {
      return [];
    }
  })();

  const seen = new Set();
  const primary = [];
  for (const [file, label, blurb] of DOCUMENT_ORDER) {
    if (!files.includes(file)) continue;
    const body = fs.readFileSync(path.join(bundleDir, file), "utf8");
    const fingerprint = body.trim();
    if (seen.has(fingerprint)) continue;
    seen.add(fingerprint);
    primary.push({ file, label, blurb, slug: file.replace(/\.md$/, "") });
  }

  const byPrefix = (prefix) =>
    files
      .filter((f) => f.startsWith(prefix))
      .sort()
      .map((f) => ({
        file: f,
        label: titleFromFilename(f),
        slug: f.replace(/\.md$/, ""),
      }));

  return {
    primary,
    reviewers: byPrefix("review_"),
    audits: byPrefix("audit_"),
  };
}

/** One review of one revision: a `v<N>` directory. */
function readBundle(paperDir, versionName) {
  const dir = path.join(paperDir, versionName);
  const provenance = readJSON(path.join(dir, "provenance.json"));
  if (!provenance) return null;

  const round = readJSON(path.join(dir, "round.json"));
  const preprint = provenance.preprint || {};
  const revision = provenance.revision || {};

  return {
    version: versionName,
    versionNumber: Number(versionName.slice(1)),
    dir,
    provenance,
    preprint,
    revision,
    round: Number(provenance.round || 1),
    decision: provenance.decision || "unknown",
    deskRejected: Boolean(provenance.desk_rejected),
    meanScore: typeof provenance.mean_score === "number" ? provenance.mean_score : null,
    panel: Array.isArray(provenance.panel) ? provenance.panel : [],
    reviewedAt: String(provenance.generated_at || "").slice(0, 10),
    // How many revisions this round itself demanded. Read from the bundle's own
    // round record: the `revision` block in provenance describes the round this
    // one *followed*, so its counts belong to the previous round.
    requiredRevisions: Array.isArray(round?.required_revisions)
      ? round.required_revisions.length
      : null,
    hasRoundRecord: Boolean(round),
    documents: readDocuments(dir),
  };
}

/** One paper, with every review it has received, newest first. */
function readPaper(year, slug) {
  const paperDir = path.join(REVIEWS_DIR, year, slug);
  const bundles = readDirs(paperDir)
    .filter((name) => /^v\d+$/.test(name))
    .map((name) => readBundle(paperDir, name))
    .filter(Boolean)
    .sort((a, b) => b.versionNumber - a.versionNumber);

  if (!bundles.length) return null;

  const latest = bundles[0];
  return {
    year,
    slug,
    dir: paperDir,
    bundles,
    latest,
    title: latest.preprint.title || "Untitled submission",
    authors: Array.isArray(latest.preprint.authors) ? latest.preprint.authors : [],
    reviewCount: bundles.length,
  };
}

let cached = null;

/** Every published paper, newest review first. Cached for the build. */
export function corpus() {
  if (cached) return cached;
  const papers = [];
  for (const year of readDirs(REVIEWS_DIR).filter((d) => /^\d{4}$/.test(d))) {
    for (const slug of readDirs(path.join(REVIEWS_DIR, year))) {
      const paper = readPaper(year, slug);
      if (paper) papers.push(paper);
    }
  }
  papers.sort((a, b) => {
    const byDate = (b.latest.reviewedAt || "").localeCompare(a.latest.reviewedAt || "");
    return byDate !== 0 ? byDate : a.title.localeCompare(b.title);
  });
  cached = papers;
  return papers;
}

/** Read one bundle document's raw markdown. */
export function readDocument(bundleDir, file) {
  return fs.readFileSync(path.join(bundleDir, file), "utf8");
}

/** Corpus-wide figures for the home page. Counted, never estimated. */
export function statistics() {
  const papers = corpus();
  const reviews = papers.flatMap((p) => p.bundles);
  const scored = reviews.filter((r) => r.meanScore !== null);
  const byVerdict = {};
  for (const review of reviews) {
    const key = review.deskRejected ? "desk" : review.decision;
    byVerdict[key] = (byVerdict[key] || 0) + 1;
  }
  return {
    papers: papers.length,
    reviews: reviews.length,
    reports: reviews.reduce(
      (n, r) => n + r.documents.reviewers.length + r.documents.audits.length,
      0,
    ),
    meanScore: scored.length
      ? scored.reduce((n, r) => n + r.meanScore, 0) / scored.length
      : null,
    byVerdict,
  };
}
