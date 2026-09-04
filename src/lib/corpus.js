/**
 * The published corpus, read straight out of `docs/reviews/`.
 *
 * The Python pipeline owns that directory and writes two kinds of thing into
 * each `<year>/<slug>/v<N>/r<M>/` bundle: the referee documents as plain
 * markdown, and `provenance.json` as the machine-readable record of the run.
 * Legacy bundles directly under `v<N>` remain readable.
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
import { assertValidProvenance } from "./reviewSchema.js";

// Astro bundles server-side modules during a production build, so
// import.meta.url points into generated build output rather than src/lib.
// The build and development commands both run from the repository root.
export const REPO = process.cwd();
export const REVIEWS_DIR = process.env.INSILICO_REVIEWS_DIR
  || path.join(REPO, "docs", "reviews")

export const VERDICT = {
  accept: "Accept",
  minor: "Minor revision",
  major: "Major revision",
  reject: "Reject",
};

export function legacyScore100(meanScore) {
  return typeof meanScore === "number" ? Math.round(meanScore * 20) : null;
}

/**
 * In Silico accepts a paper the panel returns at accept or minor revision.
 * Papers returned for major revision appear publicly as needing revision.
 *
 * The editor is never told this rule. It returns one of the four standard
 * verdicts with nothing hanging on it, and the mapping is applied here,
 * afterwards. That separation is the only reason the split is worth trusting.
 * An editor told that "minor" means acceptance is an editor being asked to
 * gatekeep, and it would grant more minors.
 *
 * This binarises the editor's judgement, not the panel's arithmetic. The two
 * are not the same: minor bundles score 3.88 to 4.12 and major bundles 2.50 to
 * 4.00, and three majors sit at or above the lowest minor. A threshold on the
 * mean would classify those three differently, which is exactly the judgement
 * a score cannot see.
 *
 * The internal `declined` key remains stable for filters and corpus statistics.
 * The public label is constructive because some of these papers were submitted
 * by someone other than their authors.
 */
const ACCEPTED_VERDICTS = new Set(["accept", "minor"]);

export function isAccepted(review) {
  if (!review || review.deskRejected) return false;
  return ACCEPTED_VERDICTS.has(review.decision);
}

/** What In Silico did, as opposed to what the editor recommended. */
export const STATUS = {
  accepted: "Accepted",
  declined: "Revision needed",
  desk: "Desk reject",
  experimental: "Experimental only",
};

export function statusOf(review) {
  if (!review) return "experimental"
  if (review.deskRejected) return "desk";
  return isAccepted(review) ? "accepted" : "declined";
}

/** Bundle documents, in the order a reader should meet them. */
const DOCUMENT_ORDER = [
  ["summary.md", "Summary", "The panel's assessment in brief."],
  ["decision_letter.md", "Decision letter", "The editor's verdict and what it requires."],
  ["desk_screen.md", "Desk screen", "Whether the submission cleared the bar for full review."],
  ["debate_transcript.md", "Advocate / skeptic debate", "The case for and against, in full."],
  ["debate_synthesis.md", "Debate synthesis", "The condensed account of the debate the editor read."],
  ["journal_recommendations.md", "Venue suggestions", "Where this might be submitted."],
  // Last, and deliberately so: it is the only document with no opinion in it,
  // and it is here for the reader who wants to check that the text the panel
  // read is the text in the PDF.
  ["manuscript_stats.md", "Manuscript statistics", "Deterministic counts over the text the panel read."],
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
 * On a desk reject the pipeline writes the same body to decision_letter and
 * desk_screen, so those arrive byte-identical. Each distinct body is listed
 * once. A reader following a direct link still finds the file, but the page
 * doesn't show one text under two headings.
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

/** One immutable review attempt, normally a `v<N>/r<M>` directory. */
function readBundle(paperDir, versionName, attemptName = "") {
  const dir = path.join(paperDir, versionName, attemptName)
  const provenance = readJSON(path.join(dir, "provenance.json"));
  if (!provenance) return null;
  assertValidProvenance(provenance, path.join(dir, "provenance.json"));

  const round = readJSON(path.join(dir, "round.json"));
  const preprint = provenance.preprint || {};
  const revision = provenance.revision || {};
  const review = provenance.review || {}
  const attemptNumber = attemptName
    ? Number(attemptName.slice(1))
    : Number(review.attempt || 1)
  const route = attemptName ? `${versionName}/${attemptName}` : versionName
  const graded = Boolean(provenance.models && Object.keys(provenance.models).length)
  const lifecycle = String(review.lifecycle || "active")
  const baselineEligible = typeof review.baseline_eligible === "boolean"
    ? review.baseline_eligible
    : graded

  return {
    version: versionName,
    versionNumber: Number(versionName.slice(1)),
    attempt: attemptName || `r${attemptNumber}`,
    attemptNumber,
    route,
    label: attemptName ? `${versionName}/${attemptName}` : versionName,
    contentId: route,
    dir,
    provenance,
    preprint,
    revision,
    review,
    round: Number(provenance.round || 1),
    decision: provenance.decision || "unknown",
    deskRejected: Boolean(provenance.desk_rejected),
    // An empty model table means every agent ran on one model, with nothing
    // stronger checking the referees. Provenance.astro warns about it on the
    // page; readPaper uses it to decide which review speaks for the paper.
    graded,
    baselineEligible: baselineEligible && lifecycle === "active",
    lifecycle,
    // Derived here rather than at each call site so the rule has one home.
    // `decision` stays exactly as the editor wrote it; this sits beside it.
    get accepted() {
      return isAccepted(this);
    },
    get status() {
      return statusOf(this);
    },
    readinessScore: typeof provenance.readiness_score === "number"
      ? provenance.readiness_score
      : null,
    readinessBreakdown: provenance.readiness_breakdown || {},
    contributionProfile: provenance.contribution_profile || {},
    scoreDecisionRationale: String(provenance.score_decision_rationale || ""),
    // Older reviews predate the editorial readiness score. Their panel mean
    // remains visible as a legacy value and is never relabeled as readiness.
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
    .flatMap((name) => {
      const versionDir = path.join(paperDir, name)
      const nested = readDirs(versionDir)
        .filter((attempt) => /^r\d+$/.test(attempt))
        .map((attempt) => readBundle(paperDir, name, attempt))
      const legacy = readBundle(paperDir, name)
      return [...(legacy ? [legacy] : []), ...nested]
    })
    .filter(Boolean)
    .sort((a, b) =>
      b.versionNumber - a.versionNumber || b.attemptNumber - a.attemptNumber
    )

  if (!bundles.length) return null;

  const latest = bundles[0];
  // Which review carries In Silico's answer on this paper.
  //
  // Not simply the newest. A single-model run is a published experiment, not
  // an editorial decision. The review page says that nothing checked the
  // referees that was any better than the referees. One of these experiments
  // sits on top of a graded panel that reached a different
  // verdict. Letting it decide would hand a free model the casting vote over
  // the panel it was run to compare against.
  //
  // A paper with only experiments has a public record but no editorial status.
  const decisive = bundles.find((b) => b.baselineEligible) || null
  return {
    year,
    slug,
    dir: paperDir,
    bundles,
    latest,
    decisive,
    accepted: isAccepted(decisive),
    status: statusOf(decisive),
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
  const readinessScored = reviews.filter((r) => r.readinessScore !== null)
  const byVerdict = {};
  for (const review of reviews) {
    const key = review.deskRejected ? "desk" : review.decision;
    byVerdict[key] = (byVerdict[key] || 0) + 1;
  }
  // Counted over papers, not review bundles: a paper re-reviewed under a
  // changed pipeline would otherwise be accepted or declined twice.
  const accepted = papers.filter((p) => p.accepted).length;
  return {
    papers: papers.length,
    reviews: reviews.length,
    accepted,
    declined: papers.filter((p) => p.status === "declined").length,
    experimental: papers.filter((p) => p.status === "experimental").length,
    reports: reviews.reduce(
      (n, r) => n + r.documents.reviewers.length + r.documents.audits.length,
      0,
    ),
    meanScore: scored.length
      ? scored.reduce((n, r) => n + r.meanScore, 0) / scored.length
      : null,
    meanReadiness: readinessScored.length
      ? readinessScored.reduce((n, r) => n + r.readinessScore, 0) / readinessScored.length
      : null,
    byVerdict,
  };
}
