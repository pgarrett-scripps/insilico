/**
 * Holds the built site to the editorial allowlist.
 *
 * `docs/` is a working directory as well as a publication directory: it holds
 * protocols, study notes and half-finished plans alongside the handful of
 * Markdown files that are part of the site. A glob over `docs/*.md` published
 * all of them. src/lib/pages.js is now the list of what is public, and this
 * check reads the built output to confirm that the list is what actually
 * shipped: every listed page is there, and nothing else from `docs/` is.
 *
 * Run it after `npm run build`.
 */

import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { EDITORIAL_SLUGS } from "../src/lib/pages.js";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const docsDir = join(root, "docs");
const distDir = join(root, "dist");

if (!existsSync(distDir)) {
  console.error("no dist/ directory. Run npm run build first.");
  process.exit(1);
}

const failures = [];

/**
 * The loader itself, read as source.
 *
 * The route used to also throw on a file the collection held that the allowlist
 * did not name. It could never fire: the loader is handed the allowlist as its
 * glob, so an unlisted file never reaches the route in the first place. The real
 * risk is someone widening that glob back to a pattern, which would publish the
 * working notes again. A pattern cannot be caught by reading dist alone, since
 * the first build after the change is the one that leaks, so assert against the
 * config source that the pattern is still the list.
 */
const configSource = readFileSync(join(root, "src/content.config.ts"), "utf8");
const pagesAt = configSource.indexOf("const pages =");
const pagesCollection = pagesAt < 0 ? "" : configSource.slice(pagesAt);

if (!pagesCollection) {
  failures.push("src/content.config.ts no longer defines a pages collection.");
} else {
  if (!pagesCollection.includes("EDITORIAL_PATTERNS")) {
    failures.push(
      "the pages collection in src/content.config.ts no longer globs EDITORIAL_PATTERNS, "
        + "so src/lib/pages.js is not what decides which docs/ files are published.",
    );
  }
  if (/pattern:\s*\[?\s*["'`][^"'`]*\*/.test(pagesCollection)) {
    failures.push(
      "the pages collection in src/content.config.ts globs a literal wildcard pattern. "
        + "docs/ holds working notes, and a pattern cannot tell them from an editorial page.",
    );
  }
}

/** Every root-level Markdown file in docs/, by slug. */
const docSlugs = readdirSync(docsDir)
  .filter((name) => name.endsWith(".md"))
  .filter((name) => statSync(join(docsDir, name)).isFile())
  .map((name) => name.slice(0, -".md".length))
  .sort();

if (!docSlugs.length) {
  failures.push("docs/ holds no Markdown at all, so this check proved nothing.");
}

for (const slug of EDITORIAL_SLUGS) {
  if (!docSlugs.includes(slug)) {
    failures.push(`${slug}: listed in src/lib/pages.js but docs/${slug}.md does not exist.`);
    continue;
  }
  if (!existsSync(join(distDir, slug, "index.html"))) {
    failures.push(`${slug}: an editorial page that the build did not produce.`);
  }
}

const unlisted = docSlugs.filter((slug) => !EDITORIAL_SLUGS.includes(slug));

for (const slug of unlisted) {
  if (existsSync(join(distDir, slug, "index.html"))) {
    failures.push(
      `${slug}: docs/${slug}.md is not an editorial page but the build published it at /${slug}/.`,
    );
  }
}

if (failures.length) {
  console.error("published pages do not match the editorial allowlist:");
  for (const failure of failures) {
    console.error(`  ${failure}`);
  }
  process.exit(1);
}

console.log(
  `ok  ${EDITORIAL_SLUGS.length} editorial pages published, `
    + `${unlisted.length} other docs/ files held back`,
);
