import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";

/**
 * Content is read in place from `docs/`, which the Python pipeline owns and
 * writes. Nothing is copied into `src/`: a review bundle is the published
 * artifact, and having two copies would make "what did the panel say" a
 * question with two possible answers.
 */

// Every document inside a review bundle. `index.md` is excluded because the
// pipeline still writes a legacy landing page there; this site builds that
// page itself from provenance.json instead.
const reports = defineCollection({
  loader: glob({
    pattern: ["**/v[0-9]*/*.md", "**/v[0-9]*/r[0-9]*/*.md", "!**/index.md"],
    base: "./docs/reviews",
  }),
});

// The hand-written editorial pages.
const pages = defineCollection({
  loader: glob({ pattern: ["*.md", "!index.md"], base: "./docs" }),
});

export const collections = { reports, pages };
