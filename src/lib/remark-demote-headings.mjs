/**
 * Push every heading in a rendered markdown document down one level.
 *
 * Each markdown file on this site is embedded in a page that has already
 * emitted its own `<h1>`. Review documents sit under a header naming the
 * document and its paper, the editorial pages under their page title. The
 * markdown then opens with its own `#`, so every one of those pages shipped
 * two `<h1>` elements: "Methodology" from the page, "Methodology Reviewer"
 * from the document.
 *
 * Two h1s is not a style preference. A screen reader announces the first as
 * the page's subject; the second contradicts it, and the document outline a
 * user navigates by has two competing roots. Demoting here rather than editing
 * the markdown keeps the source correct on its own terms: a referee report
 * opening with `# Methodology Reviewer` is right when read as a file on
 * GitHub, and right again once nested under a page heading here.
 *
 * h6 stays h6 because there is no h7. Silently emitting one would trade a
 * duplicate-heading problem for an invalid-element one.
 */
export default function remarkDemoteHeadings() {
  return (tree) => {
    const walk = (node) => {
      if (node.type === "heading") node.depth = Math.min(node.depth + 1, 6);
      for (const child of node.children || []) walk(child);
    };
    walk(tree);
  };
}
