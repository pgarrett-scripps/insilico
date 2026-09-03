import fs from "node:fs";
import path from "node:path";
import Ajv2020 from "ajv/dist/2020.js";

const schema = JSON.parse(
  fs.readFileSync(path.resolve("schemas/review-provenance.schema.json"), "utf8"),
);

const validateCurrent = new Ajv2020({ allErrors: true, strict: true }).compile(schema);

export function assertValidProvenance(provenance, source = "provenance.json") {
  if (provenance?.schema_version == null) return;
  if (validateCurrent(provenance)) return;
  const details = validateCurrent.errors
    .map((error) => `${error.instancePath || "/"} ${error.message}`)
    .join(", ");
  throw new Error(`${source}: invalid review provenance: ${details}`);
}
