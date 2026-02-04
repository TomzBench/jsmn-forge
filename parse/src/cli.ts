import { cac } from "cac";
import { createConsola } from "consola";
import fs from "node:fs/promises";
import { bundle } from "@scalar/json-magic/bundle";
import { readFiles, parseYaml } from "@scalar/json-magic/bundle/plugins/node";
import { resolve } from "./resolve.ts";
import { join } from "@scalar/openapi-parser";
import YAML from "yaml";
import { SchemaRegistry, createPlugin } from "./discover.ts";

const log = createConsola({ defaults: { tag: "jsmn-forge" } });
const cli = cac("jsmn-forge");

cli
  .command("parse [...dirs]", "Discover and bundle workspace OpenAPI specs")
  .option("--out <file>", "Write output to file instead of stdout")
  .action(async (dirs: string[], options: { out?: string }) => {
    if (dirs.length === 0) {
      log.error("No directories specified");
      process.exit(1);
    }

    const registry = await SchemaRegistry.scanDirectories(dirs);
    const plugin = createPlugin(registry);
    const plugins = [plugin, readFiles(), parseYaml()];

    const specs: Record<string, unknown>[] = [];
    for (const entry of registry.schemas()) {
      const bundled = await bundle(
        { $ref: entry.paths[0]! },
        { plugins, treeShake: false },
      );
      specs.push(resolve(bundled as Record<string, unknown>));
    }

    const joined = await join(specs);
    if (!joined.ok) {
      log.error("Conflicting paths across resources", joined.conflicts);
      process.exit(1);
    }

    const output = YAML.stringify(joined.document);
    if (options.out) {
      await fs.writeFile(options.out, output);
      log.success(`Wrote ${options.out}`);
    } else {
      process.stdout.write(output);
    }
  });

cli.help();
cli.version("0.0.0");
cli.parse();
