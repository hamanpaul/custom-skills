#!/usr/bin/env node
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";

function parseArgs(argv) {
  const args = {
    provider: "codex",
    prompt: "",
    cwd: process.cwd(),
    model: "",
    reasoning: "",
    configDir: "",
    jsonOut: "",
    copilotSdkEntry: "",
    probeSdk: false,
    includeEvents: false,
    delegateCmdTemplate: "",
  };

  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i];
    const next = argv[i + 1];
    const needValue = [
      "--provider",
      "--prompt",
      "--cwd",
      "--model",
      "--reasoning",
      "--config-dir",
      "--json-out",
      "--copilot-sdk-entry",
      "--delegate-cmd-template",
    ];
    if (needValue.includes(key)) {
      if (!next || next.startsWith("--")) {
        throw new Error(`missing value for ${key}`);
      }
      i += 1;
      if (key === "--provider") args.provider = next;
      if (key === "--prompt") args.prompt = next;
      if (key === "--cwd") args.cwd = next;
      if (key === "--model") args.model = next;
      if (key === "--reasoning") args.reasoning = next;
      if (key === "--config-dir") args.configDir = next;
      if (key === "--json-out") args.jsonOut = next;
      if (key === "--copilot-sdk-entry") args.copilotSdkEntry = next;
      if (key === "--delegate-cmd-template") args.delegateCmdTemplate = next;
      continue;
    }
    if (key === "--probe-sdk") {
      args.probeSdk = true;
      continue;
    }
    if (key === "--include-events") {
      args.includeEvents = true;
      continue;
    }
    if (key === "--help" || key === "-h") {
      printHelp();
      process.exit(0);
    }
    throw new Error(`unknown argument: ${key}`);
  }

  return args;
}

function printHelp() {
  const text = `
copilot_sdk_orchestrator.mjs

Options:
  --provider <codex|copilot|gemini>   Provider selector (default: codex)
  --prompt <text>                     Prompt text
  --cwd <path>                        Working directory (default: current cwd)
  --model <name>                      Model override
  --reasoning <level>                 Reasoning override
  --config-dir <path>                 Copilot config directory
  --copilot-sdk-entry <path>          Override @github/copilot/sdk entry (index.js)
  --delegate-cmd-template <text>      Shell template for non-copilot providers
                                       placeholders:
                                       {provider},{model},{reasoning},{cwd},{prompt}
                                       shell-safe:
                                       {provider_q},{model_q},{reasoning_q},{cwd_q},{prompt_q}
  --probe-sdk                         Probe SDK loading only
  --include-events                    Include raw SDK events in output
  --json-out <path>                   Write output JSON to file
  --help                              Show this help
`.trim();
  console.log(text);
}

function uniquePush(list, value) {
  if (!value) return;
  if (!list.includes(value)) list.push(value);
}

function versionTuple(name) {
  const match = String(name || "").match(/^v?(\d+)\.(\d+)\.(\d+)$/);
  if (!match) return [-1, -1, -1];
  return match.slice(1).map((part) => Number.parseInt(part, 10));
}

function compareVersionDesc(a, b) {
  const aa = versionTuple(a);
  const bb = versionTuple(b);
  for (let i = 0; i < aa.length; i += 1) {
    if (aa[i] !== bb[i]) return bb[i] - aa[i];
  }
  return 0;
}

function resolveCopilotSdkEntry(overrideEntry) {
  const candidates = [];
  if (overrideEntry) uniquePush(candidates, path.resolve(overrideEntry));

  const home = os.homedir();
  if (home) {
    const nodeVersionsRoot = path.join(home, ".nvm", "versions", "node");
    if (fs.existsSync(nodeVersionsRoot)) {
      const versions = fs
        .readdirSync(nodeVersionsRoot, { withFileTypes: true })
        .filter((d) => d.isDirectory())
        .map((d) => d.name)
        .sort(compareVersionDesc);
      for (const ver of versions) {
        uniquePush(
          candidates,
          path.join(
            nodeVersionsRoot,
            ver,
            "lib",
            "node_modules",
            "@github",
            "copilot",
            "sdk",
            "index.js",
          ),
        );
      }
    }

    uniquePush(
      candidates,
      path.join(
        home,
        ".nvm",
        "versions",
        "node",
        process.version,
        "lib",
        "node_modules",
        "@github",
        "copilot",
        "sdk",
        "index.js",
      ),
    );
  }

  const req = createRequire(import.meta.url);
  try {
    uniquePush(candidates, req.resolve("@github/copilot/sdk"));
  } catch (_err) {
    // ignore
  }

  try {
    const npmRoot = spawnSync("npm", ["root", "-g"], {
      encoding: "utf-8",
      stdio: ["ignore", "pipe", "ignore"],
    });
    if (npmRoot.status === 0) {
      const root = npmRoot.stdout.trim();
      uniquePush(candidates, path.join(root, "@github", "copilot", "sdk", "index.js"));
    }
  } catch (_err) {
    // ignore
  }

  for (const c of candidates) {
    if (c && fs.existsSync(c)) {
      return c;
    }
  }
  throw new Error("copilot sdk entry not found; set --copilot-sdk-entry explicitly");
}

function trimText(text, limit = 4000) {
  const value = String(text ?? "").trim();
  if (value.length <= limit) return value;
  const marker = "...<trimmed>...";
  const keep = Math.max(0, limit - marker.length);
  const head = Math.floor(keep / 2);
  const tail = keep - head;
  return `${value.slice(0, head)}${marker}${value.slice(value.length - tail)}`;
}

function shellQuote(value) {
  const text = String(value ?? "");
  return `'${text.replaceAll("'", "'\"'\"'")}'`;
}

function extractEventText(value, out, depth = 0) {
  if (depth > 6 || value == null) return;
  if (typeof value === "string") return;
  if (Array.isArray(value)) {
    for (const item of value) extractEventText(item, out, depth + 1);
    return;
  }
  if (typeof value !== "object") return;

  if (typeof value.text === "string") out.push(value.text);
  if (typeof value.content === "string") out.push(value.content);
  if (typeof value.message === "string") out.push(value.message);

  const keys = [
    "content",
    "message",
    "delta",
    "chunk",
    "value",
    "parts",
    "payload",
    "event",
    "data",
    "update",
  ];
  for (const key of keys) {
    if (Object.prototype.hasOwnProperty.call(value, key)) {
      extractEventText(value[key], out, depth + 1);
    }
  }
}

async function runCopilotViaSdk(args, sdkEntry) {
  const moduleUrl = pathToFileURL(sdkEntry).href;
  const mod = await import(moduleUrl);
  const sdk = mod.default ?? mod;
  const query = sdk.query ?? mod.query;
  if (typeof query !== "function") {
    throw new Error("copilot sdk query() not found in loaded module");
  }

  if (!args.prompt) {
    throw new Error("--prompt is required for provider=copilot");
  }

  const options = {
    prompt: args.prompt,
    workingDirectory: args.cwd,
  };
  if (args.model) options.model = args.model;
  if (args.reasoning) options.reasoningEffort = args.reasoning;
  if (args.configDir) options.configDir = args.configDir;

  const events = [];
  const chunks = [];
  for await (const event of query(options)) {
    events.push(event);
    const found = [];
    extractEventText(event, found, 0);
    for (const txt of found) chunks.push(txt);
  }

  return {
    ok: true,
    provider: "copilot",
    backend: "copilot-sdk",
    sdk_entry: sdkEntry,
    event_count: events.length,
    text: trimText(chunks.join("\n")),
    events: args.includeEvents ? events : undefined,
  };
}

function runDelegateShell(args) {
  const template = String(args.delegateCmdTemplate || "").trim();
  if (!template) {
    throw new Error(
      "provider requires --delegate-cmd-template (supported placeholders: {provider},{model},{reasoning},{cwd},{prompt},{provider_q},{model_q},{reasoning_q},{cwd_q},{prompt_q})",
    );
  }
  const values = {
    provider: args.provider,
    model: args.model || "",
    reasoning: args.reasoning || "",
    cwd: args.cwd,
    prompt: args.prompt || "",
    provider_q: shellQuote(args.provider),
    model_q: shellQuote(args.model || ""),
    reasoning_q: shellQuote(args.reasoning || ""),
    cwd_q: shellQuote(args.cwd),
    prompt_q: shellQuote(args.prompt || ""),
  };
  let cmd = template;
  for (const [k, v] of Object.entries(values)) {
    cmd = cmd.replaceAll(`{${k}}`, v);
  }

  const proc = spawnSync("/bin/bash", ["-lc", cmd], {
    cwd: args.cwd,
    encoding: "utf-8",
    stdio: ["ignore", "pipe", "pipe"],
  });
  const rc = proc.status ?? 2;
  return {
    ok: rc === 0,
    provider: args.provider,
    backend: "delegate-shell",
    command: cmd,
    returncode: rc,
    stdout: trimText(proc.stdout || ""),
    stderr: trimText(proc.stderr || ""),
  };
}

function writeOutput(args, payload) {
  if (args.jsonOut) {
    const outPath = path.resolve(args.jsonOut);
    fs.mkdirSync(path.dirname(outPath), { recursive: true });
    fs.writeFileSync(outPath, `${JSON.stringify(payload, null, 2)}\n`, "utf-8");
  }
  process.stdout.write(`${JSON.stringify(payload)}\n`);
}

async function main() {
  try {
    const args = parseArgs(process.argv.slice(2));
    if (args.probeSdk) {
      const sdkEntry = resolveCopilotSdkEntry(args.copilotSdkEntry);
      const payload = { ok: true, backend: "copilot-sdk", sdk_entry: sdkEntry, provider: args.provider };
      writeOutput(args, payload);
      return;
    }

    let payload;
    if (args.provider === "copilot") {
      const sdkEntry = resolveCopilotSdkEntry(args.copilotSdkEntry);
      payload = await runCopilotViaSdk(args, sdkEntry);
    } else if (args.provider === "codex" || args.provider === "gemini") {
      payload = runDelegateShell(args);
    } else {
      throw new Error(`unsupported provider: ${args.provider}`);
    }
    writeOutput(args, payload);
    process.exit(payload.ok ? 0 : 2);
  } catch (err) {
    const payload = {
      ok: false,
      backend: "copilot-sdk",
      error: String(err?.message || err),
    };
    process.stdout.write(`${JSON.stringify(payload)}\n`);
    process.exit(2);
  }
}

await main();
