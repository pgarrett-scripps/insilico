"""Validate a provenance record against the published schema, before writing it.

``npm run check:schema`` validates every record under ``docs/reviews`` with Ajv,
which is the gate on the repository. It runs after the fact. A record that the
engine's own output makes invalid, a guard status this schema does not list or a
transport it does not allow, was written into the published tree first and
caught afterwards, and the bundle had to be deleted by hand. Publish validates
the record here instead, before it writes a single file.

There is no JSON Schema library in either interpreter this repository runs on,
and adding one would mean a new pinned dependency for a file of a few hundred
lines. So the keywords this schema actually uses are implemented here, and an
unsupported keyword raises rather than passing quietly: a validator that
silently ignores what it does not understand is worse than no validator, because
it reports a record sound that nobody checked. If the schema grows a keyword,
this module fails loudly on the next run and asks to be taught it.

Ajv remains the authority. This is the same schema read the same way, early.
"""
from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

from review_paths import REPO

SCHEMA_PATH = REPO / "schemas" / "review-provenance.schema.json"

# Keywords that say nothing about whether a record is valid. They are read past
# rather than implemented.
ANNOTATIONS = frozenset(
    {
        "$schema",
        "$id",
        "$comment",
        "title",
        "description",
        "default",
        "examples",
        "deprecated",
        "readOnly",
        "writeOnly",
    }
)

# Keywords with an implementation below. Anything outside both sets stops the
# validator.
ASSERTIONS = frozenset(
    {
        "type",
        "enum",
        "const",
        "pattern",
        "minLength",
        "maxLength",
        "minimum",
        "maximum",
        "exclusiveMinimum",
        "exclusiveMaximum",
        "multipleOf",
        "minItems",
        "maxItems",
        "minProperties",
        "maxProperties",
        "items",
        "properties",
        "required",
        "additionalProperties",
        "allOf",
        "anyOf",
        "oneOf",
        "not",
        "if",
        "then",
        "else",
    }
)

TYPES: dict[str, object] = {
    "object": dict,
    "array": list,
    "string": str,
    "boolean": bool,
    "null": type(None),
}


class UnsupportedSchema(RuntimeError):
    """The schema uses a keyword this validator does not implement."""


class InvalidProvenance(ValueError):
    """The record does not satisfy the schema it declares."""


@lru_cache(maxsize=1)
def provenance_schema() -> dict:
    """The published schema, read once."""
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=None)
def _compiled(pattern: str) -> "re.Pattern[str]":
    """One schema pattern, compiled to mean what Ajv means by it.

    JSON Schema patterns are ECMAScript regular expressions, and Ajv runs them
    as such. Python's `$` is the one place the two disagree: it also matches
    just before a trailing newline, so `^[0-9a-f]{64}$` accepted a sha256 with a
    newline stuck on the end here and was refused by the repository's own gate
    afterwards. Worse, the record had already been written, and a hash with a
    newline in it is a hash nothing will ever match.

    So every `$` that is a real anchor, outside a character class and not
    escaped, is translated to `\\Z`, which means end of input and nothing else.
    `^` needs no translation: without the multiline flag, neither language lets
    it match anywhere but the start.
    """
    out: list[str] = []
    in_class = False
    index = 0
    while index < len(pattern):
        char = pattern[index]
        if char == "\\" and index + 1 < len(pattern):
            out.append(pattern[index : index + 2])
            index += 2
            continue
        if char == "[":
            in_class = True
        elif char == "]":
            in_class = False
        if char == "$" and not in_class:
            out.append(r"\Z")
        else:
            out.append(char)
        index += 1
    return re.compile("".join(out))


def _is_type(value: object, name: str) -> bool:
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    expected = TYPES.get(name)
    if expected is None:
        raise UnsupportedSchema(f"unknown type {name!r} in the provenance schema")
    if expected is bool:
        return isinstance(value, bool)
    if expected in (int, float):
        return isinstance(value, expected) and not isinstance(value, bool)
    return isinstance(value, expected)


def _problems(value: object, schema: object, path: str) -> list[str]:
    """Every way ``value`` fails ``schema``, each line naming where it failed."""
    if schema is True or schema == {}:
        return []
    if schema is False:
        return [f"{path or '/'} is not allowed here"]
    if not isinstance(schema, dict):
        raise UnsupportedSchema(f"a schema at {path or '/'} is neither an object nor a boolean")

    unknown = sorted(set(schema) - ANNOTATIONS - ASSERTIONS)
    if unknown:
        raise UnsupportedSchema(
            f"the provenance schema at {path or '/'} uses "
            f"{', '.join(unknown)}, which this validator does not implement. "
            "Teach it the keyword rather than letting a record through unchecked."
        )

    found: list[str] = []
    here = path or "/"

    if "type" in schema:
        names = schema["type"]
        names = [names] if isinstance(names, str) else list(names)
        if not any(_is_type(value, name) for name in names):
            found.append(f"{here} must be {' or '.join(names)}")
            # Every other keyword reads the value as that type, so stop.
            return found

    if "const" in schema and value != schema["const"]:
        found.append(f"{here} must be {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        allowed = ", ".join(repr(option) for option in schema["enum"])
        found.append(f"{here} must be one of {allowed}")

    if isinstance(value, str):
        if "pattern" in schema and not _compiled(schema["pattern"]).search(value):
            found.append(f"{here} must match {schema['pattern']}")
        if "minLength" in schema and len(value) < schema["minLength"]:
            found.append(f"{here} must be at least {schema['minLength']} character(s)")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            found.append(f"{here} must be at most {schema['maxLength']} character(s)")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            found.append(f"{here} must be >= {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            found.append(f"{here} must be <= {schema['maximum']}")
        if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
            found.append(f"{here} must be > {schema['exclusiveMinimum']}")
        if "exclusiveMaximum" in schema and value >= schema["exclusiveMaximum"]:
            found.append(f"{here} must be < {schema['exclusiveMaximum']}")
        if "multipleOf" in schema and schema["multipleOf"]:
            if value % schema["multipleOf"] != 0:
                found.append(f"{here} must be a multiple of {schema['multipleOf']}")

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            found.append(f"{here} must have at least {schema['minItems']} item(s)")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            found.append(f"{here} must have at most {schema['maxItems']} item(s)")
        if "items" in schema:
            for index, child in enumerate(value):
                found += _problems(child, schema["items"], f"{path}/{index}")

    if isinstance(value, dict):
        if "minProperties" in schema and len(value) < schema["minProperties"]:
            found.append(f"{here} must have at least {schema['minProperties']} field(s)")
        if "maxProperties" in schema and len(value) > schema["maxProperties"]:
            found.append(f"{here} must have at most {schema['maxProperties']} field(s)")
        for name in schema.get("required", ()):
            if name not in value:
                found.append(f"{here} is missing {name}")
        properties = schema.get("properties", {})
        for name, child in value.items():
            if name in properties:
                found += _problems(child, properties[name], f"{path}/{name}")
            elif "additionalProperties" in schema:
                extra = schema["additionalProperties"]
                if extra is False:
                    found.append(f"{here} has no field {name}")
                else:
                    found += _problems(child, extra, f"{path}/{name}")

    for schema_name in ("allOf", "anyOf", "oneOf"):
        if schema_name not in schema:
            continue
        results = [_problems(value, option, path) for option in schema[schema_name]]
        if schema_name == "allOf":
            for result in results:
                found += result
        else:
            passing = sum(1 for result in results if not result)
            if schema_name == "anyOf" and not passing:
                found.append(f"{here} satisfies none of the allowed shapes")
            if schema_name == "oneOf" and passing != 1:
                found.append(f"{here} must satisfy exactly one of the allowed shapes")

    if "not" in schema and not _problems(value, schema["not"], path):
        found.append(f"{here} has a shape the schema forbids")

    if "if" in schema:
        branch = "then" if not _problems(value, schema["if"], path) else "else"
        if branch in schema:
            found += _problems(value, schema[branch], path)

    return found


def provenance_problems(record: object, schema: dict | None = None) -> list[str]:
    """Every way this record fails the schema, in the order they were found."""
    return _problems(record, provenance_schema() if schema is None else schema, "")


def assert_valid_provenance(record: object, *, source: str = "provenance.json") -> None:
    """Refuse a record the repository's own schema check would reject later.

    A record with no ``schema_version`` is left alone, exactly as the Ajv gate
    leaves it: the schema describes the versioned record, and a file that claims
    no version is not one of them.
    """
    if not isinstance(record, dict) or record.get("schema_version") is None:
        return
    problems = provenance_problems(record)
    if problems:
        raise InvalidProvenance(f"{source}: invalid review provenance: {', '.join(problems)}")
