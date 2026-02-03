import { describe, it, expect } from "vitest";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
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

const __dirname = dirname(fileURLToPath(import.meta.url));
function fixture(...segs: string[]): string {
  return resolve(__dirname, "fixtures", ...segs);
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

    // no async schemas in this fixture
    expect([...registry.asyncSchemas()]).toHaveLength(0);
  });

  it("should plugin", async () => {
    const workspace = ["sdk", "network", "sensors"].map((p) =>
      fixture("workspace", p)
    );
    const registry = await SchemaRegistry.scanDirectories(workspace);
    const plugin = createPlugin(registry);
    console.log(registry);
    console.log(plugin);
  });
});
