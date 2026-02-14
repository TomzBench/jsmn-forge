# Jsmn Forge

## Intro

jsmn-forge is a code generation project. jsmn-forge generates code by crawling
OpenAPI specifications and AsyncAPI specifications for "JSON Schemas". Code
generation must be explicitly declared via OpenAPI and AsyncAPI extension.

More details are in the design document. You should only need to consult the
design document when you are assigned a task.

## Code Structure

```
codegen/
  src/jsmn_forge/
    cli.py          # CLI entry point
    bundle.py       # Bundle logic for code generation
    codegen.py      # Core code generation
    spec/           # Spec parsing, diffing, sorting, and walking
  tests/
    fixtures/       # Test fixtures (templates, workspace specs)
    test_*.py       # Test modules
```
