import { describe, it, expect } from "vitest";
import { dereference } from "@scalar/openapi-parser";

const sampleSpec = {
  openapi: "3.1.0",
  info: { title: "Test API", version: "1.0.0" },
  paths: {
    "/users/{id}": {
      get: {
        operationId: "getUser",
        parameters: [
          {
            name: "id",
            in: "path",
            required: true,
            schema: { type: "integer", format: "int64" },
          },
          {
            name: "include",
            in: "query",
            schema: { type: "array", items: { type: "string" } },
          },
        ],
        responses: {
          "200": {
            description: "Success",
            content: {
              "application/json": {
                schema: { $ref: "#/components/schemas/User" },
              },
            },
          },
        },
      },
      post: {
        operationId: "updateUser",
        requestBody: {
          content: {
            "application/json": {
              schema: { $ref: "#/components/schemas/UserUpdate" },
            },
          },
        },
        responses: {
          "200": { description: "Success" },
        },
      },
    },
  },
  components: {
    schemas: {
      User: {
        type: "object",
        required: ["id", "name"],
        properties: {
          id: { type: "integer", format: "int64" },
          name: { type: "string" },
          email: { type: "string", format: "email" },
          age: { type: "integer", format: "uint8" },
          active: { type: "boolean" },
          tags: { type: "array", items: { type: "string" } },
          metadata: {
            type: "object",
            additionalProperties: { type: "string" },
          },
        },
      },
      UserUpdate: {
        type: "object",
        properties: {
          name: { type: "string" },
          email: { type: "string", format: "email" },
        },
      },
    },
  },
};

describe("parse", () => {
  it("should dereference spec and show structure", () => {
    const result = dereference(sampleSpec);

    console.log("\n=== DEREFERENCED SPEC ===\n");
    console.log(JSON.stringify(result, null, 2));

    expect(result.schema).toBeDefined();
  });

  it("should show schema structure", () => {
    const result = dereference(sampleSpec);
    const schemas = result.schema?.components?.schemas;

    console.log("\n=== SCHEMAS ===\n");
    console.log(JSON.stringify(schemas, null, 2));

    expect(schemas?.User).toBeDefined();
  });

  it("should show path/operation structure", () => {
    const result = dereference(sampleSpec);
    const paths = result.schema?.paths;

    console.log("\n=== PATHS ===\n");
    console.log(JSON.stringify(paths, null, 2));

    expect(paths?.["/users/{id}"]).toBeDefined();
  });
});
