import { readFileSync, writeFileSync } from "node:fs";

const target = "dist/cli.js";
const src = readFileSync(target, "utf8");
if (!src.startsWith("#!")) {
  writeFileSync(target, "#!/usr/bin/env node\n" + src);
}
