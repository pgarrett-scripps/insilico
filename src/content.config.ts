import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";

import { EDITORIAL_PATTERNS } from "./lib/pages.js";

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

// The hand-written editorial pages, named one by one rather than globbed.
// `docs/` also holds working notes that are not part of the site, and a
// pattern cannot tell the difference. See src/lib/pages.js.
const pages = defineCollection({
  loader: glob({ pattern: EDITORIAL_PATTERNS, base: "./docs" }),
});

export const collections = { reports, pages };
