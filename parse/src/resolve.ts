// Resolves all $ref JSON pointers in a bundled document, producing a plain
// object with references inlined and bundle bookkeeping stripped.
//
// PR to upstream this into @scalar/json-magic/resolve:
// https://github.com/nicholasgasior/scalar/pull/XXX
//
// If merged, replace this file with:
//   import { resolve } from "@scalar/json-magic/resolve"

export function resolve(input: Record<string, unknown>): Record<string, unknown> {
  return inline(input, input) as Record<string, unknown>;
}

function inline(node: unknown, root: Record<string, unknown>): unknown {
  if (node === null || node === undefined) return node;
  if (typeof node !== "object") return node;

  if (Array.isArray(node)) {
    return node.map((item) => inline(item, root));
  }

  const obj = node as Record<string, unknown>;

  if (typeof obj.$ref === "string" && obj.$ref.startsWith("#/")) {
    const segments = obj.$ref
      .slice(2)
      .split("/")
      .map((s) => s.replace(/~1/g, "/").replace(/~0/g, "~"));

    let target: unknown = root;
    for (const seg of segments) {
      if (target === null || target === undefined || typeof target !== "object")
        return undefined;
      target = (target as Record<string, unknown>)[seg];
    }

    return inline(target, root);
  }

  const out: Record<string, unknown> = {};
  for (const key of Object.keys(obj)) {
    if (key === "x-ext" || key === "x-ext-urls") continue;
    out[key] = inline(obj[key], root);
  }
  return out;
}
