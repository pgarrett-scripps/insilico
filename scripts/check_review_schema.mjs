#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { assertValidProvenance } from "../src/lib/reviewSchema.js";

const root = path.resolve("docs/reviews");
let checked = 0;

function visit(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const target = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      visit(target);
    } else if (entry.name === "provenance.json") {
      const provenance = JSON.parse(fs.readFileSync(target, "utf8"));
      assertValidProvenance(provenance, path.relative(process.cwd(), target));
      checked += 1;
    }
  }
}

visit(root);
console.log(`Validated ${checked} review provenance record(s)`);
