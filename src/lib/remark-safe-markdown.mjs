/**
 * Treat review Markdown as untrusted text.
 *
 * Astro intentionally supports raw HTML in Markdown. Review documents are
 * written by models that read an untrusted manuscript, so allowing raw HTML
 * would let manuscript text become active markup on the published site.
 * Preserve the text for auditability, but never interpret it as HTML.
 */

const CONTROL_OR_SPACE = /[\u0000-\u0020]+/g
const SCHEME = /^[a-z][a-z0-9+.-]*:/i
const LINK_SCHEMES = new Set(["http:", "https:", "mailto:"])
const IMAGE_SCHEMES = new Set(["http:", "https:"])

function safeUrl(value, image = false) {
  const url = String(value || "").trim()
  if (!url) return true

  const compact = url.replace(CONTROL_OR_SPACE, "")
  const match = SCHEME.exec(compact)
  if (!match) return true

  const allowed = image ? IMAGE_SCHEMES : LINK_SCHEMES
  return allowed.has(match[0].toLowerCase())
}

function textOf(node) {
  if (typeof node.value === "string") return node.value
  if (typeof node.alt === "string") return node.alt
  return (node.children || []).map(textOf).join("")
}

function replaceWithText(node) {
  const value = textOf(node)
  for (const key of Object.keys(node)) delete node[key]
  node.type = "text"
  node.value = value
}

export default function remarkSafeMarkdown() {
  return (tree) => {
    const walk = (node) => {
      if (node.type === "html") {
        replaceWithText(node)
        return
      }

      if (node.type === "link" && !safeUrl(node.url)) {
        replaceWithText(node)
        return
      }

      if (node.type === "image" && !safeUrl(node.url, true)) {
        replaceWithText(node)
        return
      }

      if (node.type === "definition" && !safeUrl(node.url)) {
        node.url = ""
        node.title = null
      }

      for (const child of node.children || []) walk(child)
    }

    walk(tree)
  }
}

export { safeUrl }
