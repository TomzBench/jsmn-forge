import { z, ZodError } from "zod";
import fs from "node:fs/promises";
import type { LoaderPlugin, ResolveResult } from "@scalar/json-magic/bundle";
import { join } from "@scalar/openapi-parser";
import YAML, { YAMLParseError } from "yaml";
import path from "node:path";

//! A Resource is a conditionally bundled named OpenAPI or AsyncAPI spec
export interface Resource {
  //! The name of the resource. Used when resolving cross referenced specifications
  name: string;
  //! The version number of the resource
  version: number;
  //! A list of OpenAPI specifications declared by this resource
  http: string[];
  //! A list of AsyncAPI specifications declared by this resource
  async: string[];
  //! A list of conditions for which this resource becomes enabled
  if: string[];
}

export interface Config {
  //! The name of the module which declares schemas for code jsmn-forge code generation
  name: string;
  //! A list of Resource entries
  resources: Resource[];
}

export const ResourceSchema: z.ZodType<Resource> = z.object({
  name: z.string(),
  version: z.number(),
  http: z.array(z.string()).default([]),
  async: z.array(z.string()).default([]),
  if: z.array(z.string()).default([]),
});

export const ConfigSchema: z.ZodType<Config> = z.object({
  name: z.string(),
  resources: z.array(ResourceSchema),
});

//! A map of resource components and their path locations. ie: common => path/to/common.openapi.spec
interface SchemaResources {
  openapi: Map<string, string[]>;
  asyncapi: Map<string, string[]>;
}

//! A single discovered schema entry
export interface SchemaEntry {
  module: string;
  resource: string;
  paths: string[];
}

//! A collection of module resources.
export class SchemaRegistry {
  resources = new Map<string, SchemaResources>();
  cache = new Map<string, ResolveResult>();
  errors: ConfigErrors[] = [];

  //! Iterate all discovered OpenAPI schemas
  *schemas(): Generator<SchemaEntry> {
    for (const [module, res] of this.resources) {
      for (const [resource, paths] of res.openapi) {
        yield { module, resource, paths };
      }
    }
  }

  //! Iterate all discovered AsyncAPI schemas
  *asyncSchemas(): Generator<SchemaEntry> {
    for (const [module, res] of this.resources) {
      for (const [resource, paths] of res.asyncapi) {
        yield { module, resource, paths };
      }
    }
  }

  //! Scan directories for jsmn-forge config files, parse them, and build a registry
  static async scanDirectories(paths: string[]): Promise<SchemaRegistry> {
    const parsed = await Promise.all(paths.map(parseWorkspace));
    const registry = new SchemaRegistry();
    for (const result of parsed) {
      if (result) registry.addConfig(result);
    }
    return registry;
  }

  //! Accumulate a parsed config into the registry, or push errors
  private addConfig(parsed: ParsedConfigResult): void {
    if (parsed.ok) {
      const openapi = new Map<string, string[]>();
      const asyncapi = new Map<string, string[]>();
      const dir = path.dirname(parsed.result.path);
      const resolver = (src: string) => path.resolve(dir, src);
      for (const r of parsed.result.resources) {
        if (r.http.length > 0) openapi.set(r.name, r.http.map(resolver));
        if (r.async.length > 0) asyncapi.set(r.name, r.async.map(resolver));
      }
      this.resources.set(parsed.result.name, { openapi, asyncapi });
    } else {
      this.errors.push(parsed.error);
    }
  }

  //! Resolve a jsmn-forge $ref, joining and caching specs on first access
  async resolve(value: string): Promise<ResolveResult> {
    // We assume specs exist because of validator driver (ok?)
    const reference = parseRef(value) as RefMatch;
    const cacheKey = `${reference.module}:${reference.resource}`;
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey) as ResolveResult;
    }
    const res = this.resources.get(reference.module) as SchemaResources;
    const paths = res.openapi.get(reference.resource) as string[];
    const specs = await Promise.all(paths.map((f) => fs.readFile(f, "utf8")));
    const yaml = specs.map(parseYaml);
    const joined = await join(yaml);
    if (joined.ok) {
      const result: ResolveResult = {
        data: joined.document,
        raw: JSON.stringify(joined.document),
        ok: true,
      };
      this.cache.set(cacheKey, result);
      return result;
    } else {
      // TODO pretty this up when we add logging?
      throw new Error(JSON.stringify(joined.conflicts));
    }
  }
}

//! All possible errors when parsing yaml configurations
type ConfigErrors = YAMLParseError | ZodError;

//! A parsed Config is decorated with metadata including the location of the config
interface ParsedConfig extends Config {
  //! The location of the configuration
  path: string;
}

//! Simple helper to parse yaml consistently
function parseYaml(path: string): any {
  return YAML.parse(path, { merge: true, maxAliasCount: 1e4 });
}

//! Simple return type for `parseConfig`
type ParsedConfigResult =
  | { ok: true; result: ParsedConfig }
  | { ok: false; error: ConfigErrors };

//! Extract a yaml any object and validate with Zod schema
async function parseConfig(path: string): Promise<ParsedConfigResult> {
  try {
    const file = await fs.readFile(path, "utf8");
    const yaml = parseYaml(file);
    const result = ConfigSchema.parse(yaml);
    return { ok: true, result: { path, ...result } };
  } catch (e) {
    return { ok: false, error: e as ConfigErrors };
  }
}

//! Regex helper for finding our config file
const configFileMatch = /^\.?(jsmnForge|JsmnForge|jsmn-forge).ya?ml$/;

//! For each directory, test if a jsmn-forge.yaml config exists, and return the
//! parsed config if it exists.
async function parseWorkspace(
  directory: string
): Promise<ParsedConfigResult | undefined> {
  const files = await fs.readdir(directory);
  const config = files.find((f) => configFileMatch.test(f));
  if (config) {
    return parseConfig(path.resolve(directory, config));
  } else {
    return undefined;
  }
}

//! Parsed module:resource ref. The bundler handles #/path navigation itself —
//! our plugin only sees the URI portion (e.g. "sdk:common").
interface RefMatch {
  module: string;
  resource: string;
}

//! Matches the "module:resource" URI that bundle() passes to loader plugins.
const refMatch = /^(?<module>[a-zA-Z0-9_]+):(?<resource>[a-zA-Z0-9_]+)$/;
function parseRef(value: string): RefMatch | undefined {
  const match = refMatch.exec(value);
  const groups = match && (match.groups as Partial<RefMatch>);
  if (groups && groups.module && groups.resource) {
    return { module: groups.module, resource: groups.resource };
  }
  return undefined;
}

//! return a function for validating jsmn-forge $ref. $ref must exist
function createValidateRef(
  registry: SchemaRegistry
): (value: string) => boolean {
  return function (value: string): boolean {
    const reference = parseRef(value);
    if (reference) {
      const module = registry.resources.get(reference.module);
      return module && module.openapi.get(reference.resource) ? true : false;
    } else {
      return false;
    }
  };
}

/**
 * Scan workspace root directories for `.jsmn-forge.yaml` configs, build a
 * scheme registry from all discovered modules, and return a `LoaderPlugin`
 * that resolves cross-module `$ref` URIs (e.g. `sdk:common#/components/schemas/DeviceStatus`).
 *
 * The returned plugin is passed directly to `@scalar/json-magic` `bundle()` alongside
 * the standard `readFiles()` and `parseYaml()` plugins.
 */
export function createPlugin(registry: SchemaRegistry): LoaderPlugin {
  const validate = createValidateRef(registry);
  return {
    type: "loader",
    validate,
    exec: (value) => registry.resolve(value),
  };
}
