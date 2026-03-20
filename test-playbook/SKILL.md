---
name: test-playbook
description: 將架構、風險、debug 線索與 ProblemMap 轉成可執行的測試策略與測試案例。適用於 test plan、test matrix、stress/recovery/concurrency 測試、debug workflow、ProblemMap 驅動驗證。
---

# Test Playbook

把「系統怎麼壞、怎麼觀察、怎麼恢復」整理成一套可重用的測試設計流程，特別適合：

- 要從零建立測試策略與 test case
- 需要把 debug 經驗萃取成 regression tests
- 系統含有狀態機、非同步、競爭、持久化、裝置/網路重綁
- 手上已有 ProblemMap、troubleshooting atlas、事故筆記、support log
- 需要同時規劃 unit / integration / e2e / stress / functional 測試

---

## 核心原則

1. **先畫系統，再寫測試**
   - 先找出元件、狀態、資料流、外部依賴、持久化與非同步邊界。
   - 沒有架構圖與狀態機，就很容易只寫 happy path。

2. **先找風險，再補 coverage**
   - 測試不是平均分配，而是集中在最容易出事故的地方：
     - 狀態轉移
     - timeout / cancel
     - race condition
     - 資源釋放
     - durability / replay
     - recover / degrade path

3. **debug 不該只停在分析，要回灌成 test**
   - 每次定位出 root cause，都應問：
     - 這個問題可否穩定重現？
     - 是否能變成 unit test？
     - 若不行，至少是否能變成 integration / func-test？

4. **優先重用現有 harness**
   - 先找專案既有 test runner、fake target、fixture、CLI harness、daemon harness。
   - 非必要不要新增測試框架；沿用既有 build / test 命令。

5. **非同步測試要 deterministic**
   - 用 `Event`、barrier、gate、fake clock、可控 fake peer，避免用大量 `sleep()` 硬等。
   - `sleep()` 只可當最後一道防抖，不可當主要同步機制。

6. **文件 / usage 也屬於驗證表面**
   - 實作變更後，要回查 README / spec / func-test usage 是否仍對齊。
   - 若文件本來就對齊，不要為了「看起來有做事」而硬改文件。

---

## 標準工作流

### 第 1 階段：盤點系統與可觀測性

至少回答下面問題：

- 主程式是 CLI、daemon、library、service，還是混合？
- 主要 actor 有哪些？例如：
  - agent
  - human
  - daemon
  - worker
  - target / device / server
- 真正的寫入者 / side-effect owner 是誰？
- 持久化資料有哪些？
  - state file
  - event log
  - DB
  - queue
- 狀態機有哪些？
  - session state
  - command lifecycle
  - login / handshake
  - lease / ownership
- 哪些地方是非同步邊界？
  - thread
  - process
  - RPC
  - socket
  - device I/O
  - callback

### 第 2 階段：把 ProblemMap / debug 線索轉成測試輸入

若你有 ProblemMap、故障地圖、troubleshooting atlas、support case 筆記，先抽出以下欄位：

- **症狀**：使用者看到什麼
- **可觀測訊號**：log、state、metric、error code、檔案
- **系統層**：CLI / RPC / state machine / I/O / persistence / external peer
- **觸發條件**：timeout、拔插、壞命令、資源耗盡、重複操作
- **恢復手段**：retry、recover、detach、rebind、relogin、clear state
- **不變量**：什麼一定不能壞

把每一條 ProblemMap 節點轉成其中一種測試：

- regression test
- exploratory charter
- stress scenario
- recovery scenario
- documentation assertion

### 第 3 階段：建立風險矩陣

至少覆蓋下列風險面：

| 類型 | 典型問題 | 常見測試 |
|---|---|---|
| Correctness | 輸出錯、狀態錯 | unit / contract |
| Timeout | 等不到 prompt / response | timeout / hard timeout |
| Cancel | 執行中取消 / 排隊取消 | command lifecycle |
| Concurrency | 多 agent / 多人競爭 | arbiter / ownership |
| Recovery | recover 後回不到穩定狀態 | degrade / relogin / retry |
| Durability | rotate / replay / crash recovery | log / WAL / state reload |
| Resource lifecycle | FD leak / stale handle / orphan worker | attach / detach / cleanup |
| Rebinding | 裝置改路徑 / reconnect / hotplug | hotplug / reattach |
| Human-in-loop | CLI 與 human 互相干擾 | functional / scenario |
| Usage drift | README / spec 與程式不一致 | doc audit |

### 第 4 階段：選測試層

不要把所有問題都丟給 E2E。用最便宜但足夠的層級驗證：

#### 1. Unit
- 純邏輯
- parser / classifier / state transition
- 小型 durability 邏輯

#### 2. Component / Integration
- 真實元件 + fake peer
- 例如：
  - queue + worker
  - session manager + fake bridge
  - RPC handler + in-memory backend

#### 3. E2E
- 真 daemon / 真 CLI / 假 target
- 驗證跨層 wiring、命令介面、行為一致性

#### 4. Functional / Scenario
- YAML / DSL / 黑箱步驟
- 適合多人協作、human-agent 共用、故障劇本

#### 5. Stress / Resilience
- 連續高頻提交
- 多 actor 同時競爭
- queue backpressure
- log flood / RX flood
- crash / unplug / reconnect

### 第 5 階段：先做 harness，再做案例

優先建立或重用這些測試基礎設施：

- **Fake external peer**
  - PTY fake target
  - fake socket server
  - fake device
  - fake RPC endpoint

- **Deterministic gates**
  - `threading.Event`
  - barrier
  - controllable callback
  - explicit queue drain point

- **State isolation**
  - temp dir
  - temp state file
  - temp log dir
  - per-test profile/config

- **CLI / daemon harness**
  - spawn helper
  - stdout/json parser
  - process cleanup

### 第 6 階段：用固定順序落地

建議實作順序：

1. 先補最穩定、最基礎的 unit / component tests
2. 再補 recovery / timeout / cancel
3. 再補 multi-actor race
4. 再補 stress / flood / backpressure
5. 最後補 functional scenario 與文件對齊

原因：
- 先把 deterministic 邏輯層穩住
- 再把容易 flaky 的併發/壓力測試建立在穩定地基上

### 第 7 階段：驗證與收尾

至少做：

- 跑目標測試檔
- 跑全套既有測試
- 檢查文件 / usage 是否 drift
- 清理暫存檔
- 若某個 review 點是 false positive，要明確記錄「為什麼不改」

---

## 可重用測試模式庫

### A. Gate-controlled async test

適合：
- cancel during execution
- worker queue ordering
- race window 控制

做法：
- callback 一進入就 `started.set()`
- 真正完成前卡在 `gate.wait()`
- 測試主執行緒在 `started.wait()` 後做 cancel / status / competing submit
- 最後 `gate.set()` 讓 worker 收尾

### B. Fake peer / PTY E2E

適合：
- CLI → daemon → worker → target 全鏈路
- shell / serial / terminal / socket 類系統

做法：
- 真實啟動 daemon / server
- 外部 peer 用 PTY / fake socket 模擬
- 讓 fake peer 可配置：
  - boot banner
  - prompt
  - partial response
  - hang
  - garbled output
  - delayed prompt

### C. Append-only durability test

適合：
- WAL
- event log
- rotate / replay
- crash recovery

最少要測：
- rotate 後 archive 存在
- seq / offset 連續
- corrupt line 可跳過
- restart 後可接續 append
- mirror / sidecar 同步寫入

### D. Hotplug / rebind test

適合：
- USB device
- network reconnect
- socket path rebound

最少要測：
- remove → detached
- same identity new path → reattach
- recover with device
- recover without device

### E. Multi-actor contention test

適合：
- multi-agent queue
- agent vs human interactive ownership
- priority / fairness

最少要測：
- A 慢，B 不亂序
- queued cancel 不影響 running
- human 被 suspend 後可 resume
- multi-agent 交錯好/壞命令仍可繼續

### F. Scenario DSL / func-test

適合：
- 要讓測試案例可被產品 / QA / 支援人員看懂
- human-in-the-loop 或流程導向系統

最常見步驟：
- wait_ready
- submit / status / result_tail
- attach_console / read / write / detach
- inject fault
- assert state / assert log / assert output

---

## ProblemMap 導向測試設計法

當你拿到 ProblemMap 或 troubleshooting atlas 時，用下面流程：

### 1. 切分節點

每個節點只保留一件事：

- 症狀
- 假設
- 觀測點
- 排查命令
- recover 手段

### 2. 分類

把每個節點分成：

- **已驗證 root cause** → 必須回灌 regression test
- **高風險假設** → 應建立 exploratory / stress test
- **操作手冊類** → 應轉成 functional scenario 或 usage doc

### 3. 轉成測試問題

把敘述改寫成可驗證句型：

- 當 `X` 發生時，`Y` 狀態是否維持不變？
- 當 `X` timeout 時，是否進入 `Z` fallback？
- 當 `A` 與 `B` 競爭時，誰有 ownership？
- 當裝置重綁後，是否仍能回到可操作狀態？

### 4. 補齊 oracle

每個測試一定要有明確 oracle：

- status
- error code
- output
- state file
- event seq
- side-effect

沒有 oracle 的測試，多半只是「跑過去」而不是驗證。

---

## 建立測試計畫時建議輸出

至少產出：

1. **架構摘要**
   - 元件
   - 狀態機
   - 寫入者 / side-effect owner

2. **風險矩陣**
   - surface
   - risk
   - layer
   - harness

3. **test backlog**
   - 先做 deterministic，再做 race/stress

4. **驗證命令**
   - 單檔
   - 全套

5. **文件對齊結論**
   - 哪些要改
   - 哪些其實不用改

---

## Prompt Scaffold

當你想讓 agent 幫你規劃別的專案測試，可直接用這個骨架：

```text
請先盤點這個專案的：
1. build / test 指令
2. 主要元件與資料流
3. 狀態機與非同步邊界
4. 持久化 / log / queue / external peer

再依風險分成：
- correctness
- timeout / cancel
- recovery
- concurrency
- durability
- resource lifecycle
- usage / doc drift

然後：
1. 給我一份 test matrix
2. 指出應優先重用的 existing harness
3. 分成 unit / integration / e2e / stress / functional
4. 把 ProblemMap 或 debug 線索轉成可執行 test cases
5. 最後列出建議實作順序與驗證命令
```

---

## Guardrails

- 不要為了測試方便而先大改 production code；先找現有 seam
- 不要把 `sleep()` 當主要同步手段
- 不要只補 happy path
- 不要新增 repo 原本沒有的測試框架，除非真的必要
- 不要因為 review 指出問題就機械式修改；先判斷是否是 false positive
- 不要忽略文件 / usage drift

---

## 伴隨模板

請搭配同目錄下列模板使用：

- `templates/test-matrix-template.md`
- `templates/problemmap-intake-template.md`
