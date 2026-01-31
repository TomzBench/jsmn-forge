// Runtime constants with compile-time validation against @scalar/openapi-types
import type { OpenAPIV3, OpenAPIV3_1 } from "@scalar/openapi-types";

type SchemaTypeValue =
  | OpenAPIV3_1.NonArraySchemaObjectType
  | OpenAPIV3_1.ArraySchemaObjectType;

// Schema types
export const SCHEMA_TYPE = {
  BOOLEAN: "boolean",
  INTEGER: "integer",
  NUMBER: "number",
  STRING: "string",
  ARRAY: "array",
  OBJECT: "object",
  NULL: "null",
} as const satisfies Record<string, SchemaTypeValue>;

export type SchemaType = (typeof SCHEMA_TYPE)[keyof typeof SCHEMA_TYPE];

// Number formats (integer + number types)
export const NUMBER_FORMAT = {
  INT8: "int8",
  INT16: "int16",
  INT32: "int32",
  INT64: "int64",
  INT128: "int128",
  UINT8: "uint8",
  UINT16: "uint16",
  UINT32: "uint32",
  UINT64: "uint64",
  UINT128: "uint128",
  FLOAT: "float",
  DOUBLE: "double",
} as const;

export type NumberFormat = (typeof NUMBER_FORMAT)[keyof typeof NUMBER_FORMAT];

// String formats
export const STRING_FORMAT = {
  DATE: "date",
  DATE_TIME: "date-time",
  PASSWORD: "password",
  UUID: "uuid",
  URI: "uri",
  EMAIL: "email",
  HOSTNAME: "hostname",
  IPV4: "ipv4",
  IPV6: "ipv6",
} as const;

export type StringFormat = (typeof STRING_FORMAT)[keyof typeof STRING_FORMAT];

// Binary formats
export const BINARY_FORMAT = {
  BYTE: "byte",
  BINARY: "binary",
} as const;

export type BinaryFormat = (typeof BINARY_FORMAT)[keyof typeof BINARY_FORMAT];

export type SchemaFormat = NumberFormat | StringFormat | BinaryFormat;

// HTTP methods
export const HTTP_METHOD = {
  GET: "get",
  POST: "post",
  PUT: "put",
  DELETE: "delete",
  PATCH: "patch",
  HEAD: "head",
  OPTIONS: "options",
  TRACE: "trace",
} as const satisfies Record<string, OpenAPIV3.HttpMethods>;

export type HttpMethod = (typeof HTTP_METHOD)[keyof typeof HTTP_METHOD];

// Parameter locations
export const PARAM_IN = {
  QUERY: "query",
  HEADER: "header",
  PATH: "path",
  COOKIE: "cookie",
} as const satisfies Record<string, OpenAPIV3.ParameterLocation>;

export type ParamIn = (typeof PARAM_IN)[keyof typeof PARAM_IN];
