# Flatten test fixtures

Test data for the C flatten pass. All YAML files are **pre-normalized** —
keys are in canonical order, set-like arrays are sorted, and refs are resolved.
This isolates flatten logic from normalize/merge/join concerns.
