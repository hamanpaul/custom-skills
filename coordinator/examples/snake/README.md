# Coordinator Snake Demo

這是「可擴充、終端機、自動進行」的貪食蛇範例，用來驗證 multi-agent + coordinator relay 流程。

同時提供「開發流程版」腳本，模擬完整多 agent 開發：
- master 規劃 TODO
- 任務分派給多個 agents
- agents 協商邊界後各自開分支開發
- integrator 合併為可執行 snake 程式

## 目標

- 提供一個純 CLI、可重現（seed）、可測試的示例。
- 使用 `coordinator` 的 job/relay/stop 流程記錄 agent 協作。
- 保持擴充彈性：可替換 agent 策略、board 尺寸、步數、render 模式。

## 檔案

- `snake_core.py`：遊戲引擎（狀態、碰撞、食物生成、render）
- `snake_agents.py`：多 agent 決策鏈（`food-hunter -> safety-guard -> fallback-agent`）
- `snake_runner.py`：執行入口（可切 `--use-coordinator`）
- `snake_devflow.py`：master/worker/integrator 的多分支開發流程腳本

## 快速執行

### 1. 只跑自動遊戲（不接 coordinator）

```bash
python3 /home/paul_chen/.agents/skills/custom/coordinator/examples/snake/snake_runner.py \
  --steps 120 --seed 7
```

### 2. 用 coordinator 做 multi-agent 測試（自動 relay）

```bash
python3 /home/paul_chen/.agents/skills/custom/coordinator/examples/snake/snake_runner.py \
  --use-coordinator \
  --state-root /home/paul_chen/.agents/state/coordinator \
  --steps 80 --tick-ms 0 --no-render
```

### 3. 輸出 summary JSON

```bash
python3 /home/paul_chen/.agents/skills/custom/coordinator/examples/snake/snake_runner.py \
  --use-coordinator --tick-ms 0 --no-render \
  --summary-out /tmp/snake-summary.json
```

### 4. 跑「多 agent 開發流程」測試（master/todo/分支/整合）

在目標 git repo 內可零參數直接跑：

```bash
python3 /home/paul_chen/.agents/skills/custom/coordinator/examples/snake/snake_devflow.py
```

若不在目標 repo 目錄，才需要 `--repo-root`：

```bash
python3 /home/paul_chen/.agents/skills/custom/coordinator/examples/snake/snake_devflow.py \
  --repo-root /abs/path/to/target-repo \
  --state-root /home/paul_chen/.agents/state/coordinator \
  --topic snake-devflow-demo \
  --summary-out /tmp/snake-devflow-summary.json
```

流程內容：

1. 產生 `snake_demo/TODO.multiagent.json`（master 計畫 + 邊界）  
2. 建立 agent branches（`agent-core/agent-policy/agent-runner/agent-integrator`）  
3. 各 agent branch 各自提交對應模組  
4. 回 base branch 合併全部 agent branches  
5. 執行 smoke + generated unittest 驗證  
6. coordinator job 收斂為 `stopped`

## 協作訊號（relay）

每一回合會送出三筆 relay：

1. `food-hunter -> safety-guard`（`intent=propose`）
2. `safety-guard -> fallback-agent`（`intent=review`）
3. `fallback-agent -> coordinator`（`intent=answer`）

可用以下命令回放：

```bash
/home/paul_chen/.agents/skills/custom/coordinator/scripts/coordinator.sh \
  --state-root /home/paul_chen/.agents/state/coordinator \
  relay-replay <job-id> --trace-id <trace-id>
```

## 擴充方式

### 新增 agent

1. 在 `snake_agents.py` 新增類別（例如 `RiskAgent`）。
2. 實作決策方法（輸入 engine/snapshot，輸出 move + reason）。
3. 在 `MultiAgentPolicy.decide()` 串入該 agent。
4. 需要 relay 時，新增 `AgentMessage` 產生邏輯。

### 改決策策略

- `FoodHunterAgent`：主攻吃食物（manhattan 距離）
- `SafetyGuardAgent`：遇危險時改道
- `FallbackAgent`：最終保底

你可以替換任一層而不改動 `snake_core.py`。

## 測試

```bash
python3 -m unittest -v tests/test_snake_runner.py
python3 -m unittest -v tests/test_snake_devflow.py
```
