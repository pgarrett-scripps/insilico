import assert from "node:assert/strict"
import { createMarkdownProcessor } from "@astrojs/markdown-remark"
import remarkSafeMarkdown from "../src/lib/remark-safe-markdown.mjs"

const processor = await createMarkdownProcessor({
  remarkPlugins: [remarkSafeMarkdown],
})

const hostile = [
  "<script>document.body.dataset.compromised = 'yes'</script>",
  '<img src="x" onerror="alert(1)">',
  "[unsafe](javascript:alert(2))",
  "[obscured](java\\nscript:alert(3))",
  "![unsafe image](data:text/html;base64,PHNjcmlwdD4=)",
  "[safe](https://example.org/paper)",
].join("\n\n")

const rendered = await processor.render(hostile)
const html = rendered.code.toLowerCase()

assert.equal(html.includes("<script"), false)
assert.equal(html.includes("<img"), false)
assert.equal(html.includes('href="javascript:'), false)
assert.equal(html.includes('src="data:'), false)
assert.equal(html.includes('href="https://example.org/paper"'), true)

console.log("Generated Markdown cannot emit active HTML or unsafe URLs")
