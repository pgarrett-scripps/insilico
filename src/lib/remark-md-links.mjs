/**
 * Rewrite `policy.md#anchor` into a real site URL at build time.
 *
 * The editorial pages link to each other the way a file on disk does, because
 * that is also how they read on GitHub. `policy.md#the-desk` resolves there,
 * and a repo whose docs only work once deployed is worse than one whose docs
 * work in both places. MkDocs used to rewrite those links on the way out;
 * Astro does not, so after the migration seven of them shipped pointing at
 * `/policy/submit.md` and returned 404 on the published site.
 *
 * Rewriting here rather than editing the links keeps both properties: the
 * source stays readable and correct on GitHub, and the built page gets a URL
 * that resolves. `ci.yml` asserts no `.md` href survives into `dist/`, so a
 * page added later cannot quietly reintroduce this.
 *
 * Only same-directory relative links are touched. Anything absolute, external,
 * or reaching into another directory is left exactly as written. This is a
 * convention-fixer, not a link rewriter.
 */

const RELATIVE_MD = /^(?!https?:|\/|#)([\w.-]+)\.md(#.*)?$/;

function walk(node, visit) {
  visit(node);
  for (const child of node.children || []) walk(child, visit);
}

export default function remarkMdLinks({ base = "" } = {}) {
  const prefix = base.replace(/\/$/, "");
  return (tree) => {
    walk(tree, (node) => {
      if (node.type !== "link" || typeof node.url !== "string") return;
      const match = RELATIVE_MD.exec(node.url);
      if (!match) return;
      const [, name, hash = ""] = match;
      // `index.md` is the directory itself, not a child of it.
      node.url = name === "index"
        ? `${prefix}/${hash}`
        : `${prefix}/${name}/${hash}`;
    });
  };
}
