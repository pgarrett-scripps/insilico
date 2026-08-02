// @ts-check
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

// GitHub Pages serves this repo from a subpath. `base` has to match or every
// absolute asset URL 404s on the deployed site while working locally.
export default defineConfig({
  site: "https://pgarrett-scripps.github.io",
  base: "/insilico",
  trailingSlash: "always",
  outDir: "./dist",
  integrations: [sitemap()],
  markdown: {
    // The panel writes plain markdown. Smartypants turns its quotes and dashes
    // into typographic ones, which matters when the output is set in a serif
    // reading column rather than a docs theme.
    smartypants: true,
    shikiConfig: { theme: "github-dark-default", wrap: true },
  },
  build: { format: "directory" },
});
