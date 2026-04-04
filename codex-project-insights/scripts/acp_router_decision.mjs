#!/usr/bin/env node

import fs from "node:fs/promises";
import { spawn } from "node:child_process";
import readline from "node:readline";

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) {
      continue;
    }
    const key = token.slice(2);
    if (i + 1 < argv.length && !argv[i + 1].startsWith("--")) {
      out[key] = argv[i + 1];
      i += 1;
      continue;
    }
    out[key] = "true";
  }
  return out;
}

function requestTimeoutMs(timeoutSec) {
  const n = Number(timeoutSec);
  if (!Number.isFinite(n) || n <= 0) {
    return 180000;
  }
  return Math.floor(n * 1000);
}

class RpcBridge {
  constructor(child, timeoutMs) {
    this.child = child;
    this.timeoutMs = timeoutMs;
    this.nextId = 1;
    this.pending = new Map();
    this.assistantChunks = [];
    this.stderrChunks = [];
    this.sessionUpdates = [];
    this._bindStreams();
  }

  _bindStreams() {
    const rl = readline.createInterface({ input: this.child.stdout });
    rl.on("line", (line) => {
      this._onLine(line);
    });
    this.child.stderr.on("data", (chunk) => {
      const text = String(chunk ?? "");
      if (text) {
        this.stderrChunks.push(text);
      }
    });
  }

  _onLine(line) {
    const raw = String(line ?? "").trim();
    if (!raw) {
      return;
    }
    let msg;
    try {
      msg = JSON.parse(raw);
    } catch {
      return;
    }

    if (Object.prototype.hasOwnProperty.call(msg, "id")) {
      const pending = this.pending.get(msg.id);
      if (pending && (Object.prototype.hasOwnProperty.call(msg, "result") || Object.prototype.hasOwnProperty.call(msg, "error"))) {
        this.pending.delete(msg.id);
        clearTimeout(pending.timer);
        if (msg.error) {
          pending.reject(new Error(`rpc ${pending.method} failed: ${JSON.stringify(msg.error)}`));
        } else {
          pending.resolve(msg.result);
        }
        return;
      }
    }

    if (msg.method === "session/update") {
      this._onSessionUpdate(msg);
      return;
    }

    if (msg.method === "session/request_permission" && Object.prototype.hasOwnProperty.call(msg, "id")) {
      this.send({
        jsonrpc: "2.0",
        id: msg.id,
        result: { outcome: { outcome: "cancelled" } },
      });
      return;
    }

    if (msg.method && Object.prototype.hasOwnProperty.call(msg, "id")) {
      this.send({
        jsonrpc: "2.0",
        id: msg.id,
        error: {
          code: -32601,
          message: `unsupported client method: ${msg.method}`,
        },
      });
    }
  }

  _onSessionUpdate(msg) {
    const params = msg.params ?? {};
    const update = params.update ?? {};
    this.sessionUpdates.push(update);
    if (update.sessionUpdate !== "agent_message_chunk") {
      return;
    }
    const content = update.content ?? {};
    if (content.type === "text" && typeof content.text === "string") {
      this.assistantChunks.push(content.text);
    }
  }

  send(obj) {
    if (!this.child.stdin.writable) {
      throw new Error("agent stdin is not writable");
    }
    this.child.stdin.write(`${JSON.stringify(obj)}\n`);
  }

  request(method, params) {
    const id = this.nextId;
    this.nextId += 1;
    const payload = {
      jsonrpc: "2.0",
      id,
      method,
      params,
    };
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error(`rpc timeout: ${method}`));
      }, this.timeoutMs);
      this.pending.set(id, { resolve, reject, timer, method });
      try {
        this.send(payload);
      } catch (err) {
        this.pending.delete(id);
        clearTimeout(timer);
        reject(err);
      }
    });
  }

  close() {
    for (const [id, pending] of this.pending.entries()) {
      clearTimeout(pending.timer);
      pending.reject(new Error(`rpc aborted: ${id}`));
      this.pending.delete(id);
    }
    try {
      this.child.stdin.end();
    } catch {
      // Ignore stream close errors.
    }
    if (!this.child.killed) {
      this.child.kill("SIGTERM");
    }
  }
}

function findConfigOption(configOptions, category, idRegex) {
  if (!Array.isArray(configOptions)) {
    return null;
  }
  for (const option of configOptions) {
    if (!option || typeof option !== "object") {
      continue;
    }
    if (category && option.category === category) {
      return option;
    }
  }
  for (const option of configOptions) {
    if (!option || typeof option !== "object") {
      continue;
    }
    const id = String(option.id ?? "");
    if (idRegex.test(id)) {
      return option;
    }
  }
  return null;
}

function findConfigValue(option, targetValue) {
  if (!option || typeof option !== "object") {
    return null;
  }
  const values = Array.isArray(option.options) ? option.options : [];
  if (!values.length) {
    return null;
  }
  const wanted = String(targetValue ?? "").trim();
  if (!wanted) {
    return null;
  }
  const exact = values.find((item) => String(item?.value ?? "") === wanted);
  if (exact) {
    return exact;
  }
  const lowered = wanted.toLowerCase();
  const insensitive = values.find((item) => String(item?.value ?? "").toLowerCase() === lowered);
  return insensitive ?? null;
}

async function setConfigOptionIfSupported(bridge, sessionId, configOptions, target) {
  const desired = String(target?.value ?? "").trim();
  if (!desired) {
    return { configOptions, applied: null };
  }

  const option = findConfigOption(
    configOptions,
    target.category,
    target.idRegex,
  );
  if (!option) {
    return { configOptions, applied: null };
  }

  const valueOption = findConfigValue(option, desired);
  if (!valueOption) {
    return { configOptions, applied: null };
  }

  const result = await bridge.request("session/set_config_option", {
    sessionId,
    configId: String(option.id),
    value: String(valueOption.value),
  });
  const updatedOptions = Array.isArray(result?.configOptions)
    ? result.configOptions
    : configOptions;
  return {
    configOptions: updatedOptions,
    applied: {
      configId: String(option.id),
      value: String(valueOption.value),
    },
  };
}

async function run() {
  const args = parseArgs(process.argv.slice(2));
  const requestPath = args.request;
  const outputPath = args.output;
  if (!requestPath || !outputPath) {
    throw new Error("usage: acp_router_decision.mjs --request <json> --output <json>");
  }

  const payload = JSON.parse(await fs.readFile(requestPath, "utf8"));
  const command = Array.isArray(payload.command) ? payload.command : [];
  if (!command.length) {
    throw new Error("request.command is empty");
  }

  const cwd = String(payload.cwd ?? process.cwd());
  const prompt = String(payload.prompt ?? "");
  const timeoutMs = requestTimeoutMs(payload.timeoutSec);

  const child = spawn(command[0], command.slice(1), {
    cwd,
    stdio: ["pipe", "pipe", "pipe"],
    env: process.env,
  });

  const bridge = new RpcBridge(child, timeoutMs);
  const killTimer = setTimeout(() => {
    if (!child.killed) {
      child.kill("SIGTERM");
    }
  }, timeoutMs);

  try {
    await bridge.request("initialize", {
      protocolVersion: 1,
      clientCapabilities: {},
      clientInfo: {
        name: "agents-self-evolve",
        title: "agents-self-evolve",
        version: "0.1.0",
      },
    });

    const newSessionResult = await bridge.request("session/new", {
      cwd,
      mcpServers: [],
    });
    const sessionId = String(newSessionResult?.sessionId ?? "");
    if (!sessionId) {
      throw new Error("session/new did not return sessionId");
    }

    let configOptions = Array.isArray(newSessionResult?.configOptions)
      ? newSessionResult.configOptions
      : [];
    const appliedConfig = [];

    const modelApply = await setConfigOptionIfSupported(
      bridge,
      sessionId,
      configOptions,
      {
        category: "model",
        idRegex: /(model)/i,
        value: payload.model,
      },
    );
    configOptions = modelApply.configOptions;
    if (modelApply.applied) {
      appliedConfig.push(modelApply.applied);
    }

    const reasoningApply = await setConfigOptionIfSupported(
      bridge,
      sessionId,
      configOptions,
      {
        category: "thought_level",
        idRegex: /(thought|reason|reasoning)/i,
        value: payload.reasoning,
      },
    );
    configOptions = reasoningApply.configOptions;
    if (reasoningApply.applied) {
      appliedConfig.push(reasoningApply.applied);
    }

    const promptResult = await bridge.request("session/prompt", {
      sessionId,
      prompt: [
        {
          type: "text",
          text: prompt,
        },
      ],
    });

    const response = {
      provider: String(payload.provider ?? ""),
      command,
      stopReason: String(promptResult?.stopReason ?? ""),
      assistant_output: bridge.assistantChunks.join(""),
      applied_config: appliedConfig,
      stderr: bridge.stderrChunks.join(""),
      update_count: bridge.sessionUpdates.length,
    };
    await fs.writeFile(outputPath, `${JSON.stringify(response)}\n`, "utf8");
  } finally {
    clearTimeout(killTimer);
    bridge.close();
  }
}

run().catch(async (err) => {
  const message = err instanceof Error ? err.message : String(err);
  try {
    const args = parseArgs(process.argv.slice(2));
    if (args.output) {
      await fs.writeFile(
        args.output,
        `${JSON.stringify({ error: message })}\n`,
        "utf8",
      );
    }
  } catch {
    // Ignore best-effort error output failures.
  }
  process.stderr.write(`${message}\n`);
  process.exit(1);
});
