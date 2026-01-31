// IR Descriptors — output of the flatten pass, input to codegen

import type { NumberFormat } from "./flatten.ts";

// Discriminated union of all descriptor kinds. Each variant carries only the
// fields relevant to its kind — switch on `kind` to narrow.

export type Descriptor =
  | NullDescriptor
  | BoolDescriptor
  | NumberDescriptor
  | StringDescriptor
  | ArrayDescriptor
  | ObjectDescriptor;

export interface NullDescriptor {
  kind: "null";
  name: string;
}

export interface BoolDescriptor {
  kind: "bool";
  name: string;
}

export interface NumberDescriptor {
  kind: "number";
  name: string;
  format: NumberFormat;
  minimum?: Bound;
  maximum?: Bound;
}

export interface StringDescriptor {
  kind: "string";
  name: string;
  maxLength: number;
  minLength?: number;
  pattern?: string;
}

export interface ArrayDescriptor {
  kind: "array";
  name: string;
  items: FieldType;
  dims: Dim[];
}

export interface ObjectDescriptor {
  kind: "object";
  name: string;
  fields: Field[];
}

// A single field within an ObjectDescriptor.
export interface Field {
  name: string;
  type: FieldType;
  required: boolean;
}

// Inclusive or exclusive bound for numeric range validation.
export type Bound =
  | { exclusive: false; value: number }
  | { exclusive: true; value: number };

// Array dimension — one level in a (possibly multi-dimensional) array.
// Outer-to-inner order: dims[0] is the outermost array.
export interface Dim {
  min: number;
  max: number;
}

// Field value types. When dims is present, the field is an array (possibly
// multi-dimensional) of the base type. When absent, it is a scalar.
export type FieldType =
  | { kind: "bool"; dims?: Dim[] }
  | { kind: "null"; dims?: Dim[] }
  | {
      kind: "number";
      format: NumberFormat;
      minimum?: Bound;
      maximum?: Bound;
      dims?: Dim[];
    }
  | {
      kind: "string";
      maxLength: number;
      minLength?: number;
      pattern?: string;
      dims?: Dim[];
    }
  | { kind: "ref"; to: string; dims?: Dim[] };
