import { describe, it, expect } from "vitest";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { bundle } from "@scalar/json-magic/bundle";
import { readFiles, parseYaml } from "@scalar/json-magic/bundle/plugins/node";
import { resolve } from "../src/resolve.ts";
import { join } from "@scalar/openapi-parser";
import YAML from "yaml";
import { createPlugin, SchemaRegistry } from "../src/discover.ts";

//   workspace/
//   ├── sdk/
//   │   ├── .jsmn-forge.yaml              name: sdk
//   │   └── schemas/
//   │       ├── common.openapi.yaml       device_status (bool + uint32)
//   │       └── auth.openapi.yaml         auth_token (string + uint32)
//   ├── network/
//   │   ├── .jsmn-forge.yaml              name: network
//   │   └── schemas/
//   │       ├── ethernet.openapi.yaml     ethernet_config → sdk:common#device_status
//   │       └── wifi.openapi.yaml         wifi_config → sdk:common#device_status
//   └── sensors/
//       ├── .jsmn-forge.yaml              name: sensors
//       └── schemas/
//           ├── temperature.openapi.yaml  temperature_reading → sdk:common#device_status
//           └── humidity.openapi.yaml     humidity_reading → sdk:auth#auth_token

const __dirname = path.dirname(fileURLToPath(import.meta.url));
function fixture(...segs: string[]): string {
  return path.resolve(__dirname, "fixtures", ...segs);
}

describe("plugin", () => {
  it("should detect all schemas", async () => {
    const workspace = ["sdk", "network", "sensors"].map((p) =>
      fixture("workspace", p)
    );
    const registry = await SchemaRegistry.scanDirectories(workspace);

    const schemas = [...registry.schemas()];
    const keys = new Set(schemas.map((s) => `${s.module}:${s.resource}`));
    expect(keys).toEqual(
      new Set([
        "sdk:common",
        "sdk:auth",
        "network:ethernet",
        "network:wifi",
        "sensors:temperature",
        "sensors:humidity",
      ])
    );

    // every declared spec path should be present
    const allPaths = new Set(schemas.flatMap((s) => s.paths));
    expect(allPaths).toEqual(
      new Set([
        fixture("workspace", "sdk", "schemas", "common.openapi.yaml"),
        fixture("workspace", "sdk", "schemas", "auth.openapi.yaml"),
        fixture("workspace", "network", "schemas", "ethernet.openapi.yaml"),
        fixture("workspace", "network", "schemas", "wifi.openapi.yaml"),
        fixture("workspace", "sensors", "schemas", "temperature.openapi.yaml"),
        fixture("workspace", "sensors", "schemas", "humidity.openapi.yaml"),
      ])
    );

    // TODO add some async fixtures
    expect([...registry.asyncSchemas()]).toHaveLength(0);
  });
});

describe("parse pipeline", () => {
  it("bundles, resolves, and joins all workspace specs", async () => {
    const workspace = ["sdk", "network", "sensors"].map((p) =>
      fixture("workspace", p)
    );
    const registry = await SchemaRegistry.scanDirectories(workspace);
    const plugin = createPlugin(registry);
    const plugins = [plugin, readFiles(), parseYaml()];

    const specs: Record<string, unknown>[] = [];
    for (const entry of registry.schemas()) {
      const bundled = await bundle(
        { $ref: entry.paths[0]! },
        { plugins, treeShake: false }
      );
      specs.push(resolve(bundled as Record<string, unknown>));
    }

    const joined = await join(specs);
    expect(joined.ok).toBe(true);
    const doc = joined.document as Record<string, any>;

    // all 6 paths present
    expect(Object.keys(doc.paths)).toHaveLength(6);

    // required arrays preserved
    const ethernetSchema = doc.components.schemas.ethernet_config;
    expect(Array.isArray(ethernetSchema.required)).toBe(true);
    expect(ethernetSchema.required).toContain("ip");

    // cross-module $ref resolved to inline object
    const deviceStatus = ethernetSchema.properties.status;
    expect(deviceStatus).toHaveProperty("type");
    expect(deviceStatus).not.toHaveProperty("$ref");

    // no bundle bookkeeping in output
    for (const spec of specs) {
      expect(spec).not.toHaveProperty("x-ext");
      expect(spec).not.toHaveProperty("x-ext-urls");
    }

    // YAML round-trip preserves structure
    const output = YAML.stringify(doc);
    const reparsed = YAML.parse(output);
    expect(
      Array.isArray(reparsed.components.schemas.ethernet_config.required)
    ).toBe(true);
  });
});
