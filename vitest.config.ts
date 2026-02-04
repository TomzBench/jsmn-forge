import { defineConfig } from "vitest/config";
export default defineConfig({
  test: {
    environment: "node",
    include: ["parse/tests/**/*.test.ts", "parse/src/**/*.test.ts"],
  },
});
