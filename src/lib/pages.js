/**
 * The editorial pages, listed one by one.
 *
 * `docs/` is a working directory as much as a publication directory. The
 * pipeline writes review bundles into `docs/reviews/`, and the people running
 * this journal keep protocols, study notes and half-finished plans as Markdown
 * next to the four pages that are actually part of the site. A glob over
 * `docs/*.md` cannot tell those apart, so it published whatever was on disk:
 * ninety-odd internal notes went into the build, and the only thing standing
 * between them and the live site was that most of them were untracked.
 *
 * So publishing is explicit. A file reaches the site because its slug is in
 * this list, and for no other reason. Adding a page is one line here, which is
 * the point: it is a decision someone makes rather than a side effect of
 * where a file was saved.
 *
 * `title` and `lede` live here too, because a page with no title block was the
 * other half of the same bug. There is nowhere to add a slug and forget them.
 *
 * `scripts/check_published_pages.mjs` holds this to the built output.
 */

export const EDITORIAL_PAGES = [
  {
    slug: "submit",
    title: "Submit a preprint",
    lede: "A preprint URL is all you need to request a review.",
  },
  {
    slug: "criteria",
    title: "What the panel looks for",
    lede: "The panel's rubric and review method.",
  },
  {
    slug: "policy",
    title: "Editorial policy",
    lede: "Editorial scope, authority, publication, removal, data, and governance.",
  },
  {
    slug: "development",
    title: "Running it yourself",
    lede: "Building the site, running a review on your own machine, and reviewing a paper before you submit it anywhere.",
  },
];

/** The files the content collection is allowed to load, relative to `docs/`. */
export const EDITORIAL_PATTERNS = EDITORIAL_PAGES.map((page) => `${page.slug}.md`);

export const EDITORIAL_SLUGS = EDITORIAL_PAGES.map((page) => page.slug);

export function editorialPage(slug) {
  return EDITORIAL_PAGES.find((page) => page.slug === slug) || null;
}
