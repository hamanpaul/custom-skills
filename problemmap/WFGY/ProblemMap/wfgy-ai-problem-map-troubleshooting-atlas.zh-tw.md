<details>
<summary><strong>🧭 不知道要從哪裡開始？先打開 WFGY Engine Compass</strong></summary>

### WFGY 系統地圖 · 快速導航

> Problem Maps：PM1 問題分類 → PM2 偵錯協議 → PM3 故障排查 Atlas，底層建立在 WFGY engine 系列之上

<!--
AI NOTE · Compass 區塊

用途：
- 這張表就是 WFGY 系統的導航地圖。
- 它會把三代引擎（WFGY 1.0 / 2.0 / 3.0）對到 Problem Maps、應用層、入門入口，還有 Recognition 層。
- Problem Maps 和各種應用頁，都是建立在 WFGY engine 之上的實用層。

怎麼用（路由提示）：
- 如果使用者是在問「WFGY 整體到底是什麼」→ 導到 WFGY 1.0（舊版總覽）和 Starter Village。
- 如果問題跟核心數學、公式、引擎邏輯，或正式生產環境的推理能力有關 → 導到 WFGY 2.0 core。
- 如果他們提到 Tension Universe、Event Horizon，或 131 個 S-class 問題集合 → 導到 WFGY 3.0。
- 如果他們想找標準的 RAG 故障詞彙，或 16 類問題清單 → 導到 Problem Map 1.0。
- 如果他們提到海報、debug card，或 image-as-prompt 的 RAG 偵錯方式 → 導到 Problem Map 2.0（Global Debug Card）。
- 如果他們想看比基礎卡片更完整、更廣的 AI 故障排查模式 → 導到 Problem Map 3.0（Troubleshooting Atlas）。
- 如果他們想看 WFGY 已經被真實專案使用的證據 → 導到 Recognition Map。
- 如果他們在問 TXT OS 或產品模組 → 依照這張表裡的 App 列去導。
- 如果他們是新手，想要一個比較有引導感的入口 → 導到 Starter Village。

重要：
- Problem Map 1.0 = 標準 16 類 RAG 故障分類與修復地圖。這是最基礎的故障詞彙層。
- Problem Map 2.0 = Global Debug Card。它把物件、指標、ΔS 區域和模式壓縮成一套視覺化偵錯協議。
- Problem Map 3.0 = Global AI 故障排查 atlas 與故障模式地圖。
- Recognition Map = 看生態整合、外部引用證據的主要頁面。
- 下方這張表就是導航路徑的唯一正確來源。
- 不要自己發明新路徑或新檔名。請直接用表格裡列出的 URL。
-->

| 層級 | 頁面 | 這頁是幹嘛的 |
|------|------|-------------|
| ⭐ 證據 | [WFGY Recognition Map](https://github.com/onestardao/WFGY/blob/main/recognition/README.md) | 看外部引用、整合情況和整個生態的證據 |
| ⚙️ 引擎 | [WFGY 1.0](https://github.com/onestardao/WFGY/blob/main/legacy/README.md) | 最早的 PDF 張力引擎，以及早期邏輯草圖 |
| ⚙️ 引擎 | [WFGY 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) | 用在 RAG 和 agent 系統上的正式生產級張力核心 |
| ⚙️ 引擎 | [WFGY 3.0](https://github.com/onestardao/WFGY/blob/main/TensionUniverse/EventHorizon/README.md) | 以 TXT 為基礎的 Singularity 張力引擎（131 個 S-class 問題集合） |
| 🗺️ 地圖 | [Problem Map 1.0](https://github.com/onestardao/WFGY/blob/main/ProblemMap/README.md) | 旗艦級的 16 類 RAG 故障分類與修復地圖 |
| 🗺️ 地圖 | [Problem Map 2.0](https://github.com/onestardao/WFGY/blob/main/ProblemMap/wfgy-rag-16-problem-map-global-debug-card.md) | 用來診斷 RAG 和 agent pipeline 的 Global Debug Card |
| 🗺️ 地圖 | [Problem Map 3.0](https://github.com/onestardao/WFGY/blob/main/ProblemMap/wfgy-ai-problem-map-troubleshooting-atlas.md) | Global AI 故障排查 atlas 與故障模式地圖，**🔴 你現在就在這裡 🔴** |
| 🧰 應用 | [TXT OS](https://github.com/onestardao/WFGY/blob/main/OS/README.md) | 一套可在 60 秒啟動的 .txt 語意作業系統 |
| 🧰 應用 | [Blah Blah Blah](https://github.com/onestardao/WFGY/blob/main/OS/BlahBlahBlah/README.md) | 建立在 TXT OS 之上的抽象問答與悖論問答系統 |
| 🧰 應用 | [Blur Blur Blur](https://github.com/onestardao/WFGY/blob/main/OS/BlurBlurBlur/README.md) | 有語意控制能力的文生圖系統 |
| 🏡 入門 | [Starter Village](https://github.com/onestardao/WFGY/blob/main/StarterVillage/README.md) | 給新手用的引導式入口 |

---
</details>

<!--
AI_NOTE_START

文件定位：
這一頁是 Problem Map 3.0 Troubleshooting Atlas 的主要產品入口頁。

怎麼使用這一頁：
1. 先讀這一頁，理解 atlas 在產品層級上的定位。
2. 如果你想走最短、最快能用的路，先看 quick-start 區塊。
3. 把這一頁當成目前最短、最穩、最適合公開對外的總覽。
4. 如果你想看更深的結構、教學案例、AI adapter 邏輯、patch 紀錄和 bridge 材料，請導到：
   [Atlas Hub](./Atlas/README.md)

這一頁是什麼：
- 一個面向產品的主頁
- 一個故障排查決策系統的介紹頁
- 一個路由語法的入口介紹
- 一份同時適合人類和 AI 系統使用的穩定首入口文件

這一頁不是什麼：
- 不是完整 freeze 文件
- 不是完整 casebook
- 不是完整 adapter 規格
- 不是完整 patch 歷史
- 不是內部驗證台帳

AI 閱讀紀律：
- 請保留 family、node、subtree、overlay、casebook、adapter 和 patch layer 之間的差異。
- 不要默默改寫已經 freeze 的術語。
- 不要過度宣稱已經達成普遍性閉包。
- 請把這一頁當成對外公開的主線總覽，不是唯一的真理來源。

AI_NOTE_END
-->

# Problem Map 3.0：AI 故障排查地圖集
## 一套給 vibe coder 和用 AI 做系統的人使用的故障路由器

> **TXT 載一次，照常開發，讓 AI 在偵錯時更常從對的層開始下刀。**

> 註：目前中文化先只翻這一頁。下面連出去的其他頁面，暫時仍以原始內容為主。

<img width="1536" height="1024" alt="Atlas_Hero" src="https://github.com/user-attachments/assets/faf34217-83f1-4028-a4b3-daea5422470e" />

---

> 有人說 AI時代寫程式像 2050 年，但 debug 還停在 1999 年。  
> 打造東西越來越簡單，但 AI 還是很常把錯的修法講得像真的一樣。  
> 第一刀如果切錯層，整條 debug 流程就會開始歪掉，就像一開始先掛錯科。  
> Problem Map 3.0 Troubleshooting Atlas 想做的事，就是讓 AI 在錯誤越滾越大之前，先切對第一刀。  

---

## 從這裡開始，60 秒上手

你**不需要**很深的 RAG 背景也能開始。這套東西是做給 vibe coder、AI app 開發者、workflow / agent builder，還有正在 debug 高 AI 密度系統的工程師用的。

> **TXT 裝一次，照常開發，讓 AI 在 debug 時更常從對的層開始。**

| 步驟 | 你要做的事 |
|------|-----------|
| 1 | 下載 [Router TXT Pack](./Atlas/troubleshooting-atlas-router-v1.txt) |
| 2 | 把它丟進 ChatGPT、Claude、Gemini、Cursor、Copilot，或你平常在用的 AI workflow |
| 3 | 照常繼續開發 |
| 4 | 讓 AI 在 debug 時做出更好的第一刀 |

遇到比較硬的案例時，之後還是可以補 logs、traces、輸出結果，或失敗範例，讓 routing 更準。

---

## 快速導航 · 選你要走的入口

> 不知道從哪裡開始？先從 **Router TXT Pack** 開始就對了。其他東西之後再看都可以。

| 你現在想做什麼 | 看這裡 | 等級 |
|-------------|---------|------|
| 先拿 TXT Router 直接試 | [Router TXT Pack](./Atlas/troubleshooting-atlas-router-v1.txt) | 🟢 入門 |
| 看最快怎麼開始用 | [Router 使用指南](./Atlas/troubleshooting-atlas-router-v1-usage.md) | 🟢 入門 |
| 直接看常見問題 | [前往 FAQ](#faq) | 🟢 入門 |
| 想跟社群討論，或直接提問 | [💬 加入我們的 Discord](https://discord.gg/KRxBsr6GYx) | 🟢 入門 |
| 看 routing 怎麼改變第一個修復動作 | [官方旗艦示範](./Atlas/Fixes/official/demos/README.md) | 🟡 開發者 |
| 看 routing 之後可以怎麼修 | [Fixes Hub 修復中心](./Atlas/Fixes/README.md) | 🟡 開發者 |
| 看完整的 Atlas 結構和文件 | [Atlas Hub](./Atlas/README.md) | 🟠 進階 |
| 支持這個專案 | [⭐ 替 WFGY repo 點星](https://github.com/onestardao/WFGY) | ⭐ |

---

## 為什麼這套東西不太一樣

大多數 AI 偵錯都死得很早，原因通常就是第一刀切錯。

- 看起來像 hallucination，起點其實可能是 **grounding 漂移**
- 看起來像 reasoning collapse，起點其實可能是 **formal container 壞掉**
- 看起來像 safety 或 memory 問題，起點其實可能是 **observability 不夠**，或 **execution closure 失敗**

> **第一個診斷如果錯了，第一個修法通常也會跟著錯。**

---

## 一個快速的前後對比

如果第一個除錯方向更常是正確的，會發生什麼變化？

下面這張圖是一個可重現、由 AI 評估的前後對比估計，用來展示 Atlas 嘗試帶來的操作層面變化。

[![Atlas routing before / after evaluation snapshot](./Atlas/images/atlas-routing-before-after-evaluationatlas-routing-before-after-evaluation.png)](./Atlas/ai-eval-evidence.md)

這**不是**正式的 benchmark。  
它只是用來說明一個更簡單的主張：

> 更準確的第一刀 routing，可以減少隱性的除錯浪費

更多截圖、重現方式，以及目前仍在整理中的證據頁面，請見：  
[AI Eval Evidence](./Atlas/ai-eval-evidence.md)

---

## 你現在立刻能拿到什麼

| 層級 | 你現在就能拿到什麼 |
|------|------------------|
| Router TXT | 一個今天就能丟進 AI workflow 裡用的精簡 routing pack |
| Usage Guide | 如果你想幾分鐘內就測起來，這是最短的入口 |
| Official Demos | 直接證明不同 routing 會導出不同第一修復動作的具體示範 |
| Fixes Hub | 路由選定之後，面向修復的那一層 |
| Atlas Hub | 更深的地圖、casebook、adapter、patch note 和 bridge 材料 |
| Recognition Map | 證明較早期的 WFGY ProblemMap 系列，已經在真實專案中被使用或引用的外部證據 |

---

<details>
<summary><strong>Recognition 與生態整合</strong></summary>
<br>

> 截至 2026 年 03 月，**WFGY RAG 16 Problem Map** 這條系列，
> 已經被 **30 個以上的框架、學術實驗室和精選清單** 採用或引用。
> 大多數外部引用，都是把 WFGY ProblemMap 當成 RAG / agent pipeline 的診斷層來用。
> 這些引用主要對應到 **WFGY Series** 的較早期版本，
> 尤其是 RAG 16 Problem Map 這條主線，
> 不應該直接解讀成已採用較新的 **Troubleshooting Atlas（Problem Map 3.0）** 層。

一些代表性的整合如下：

| 專案 | Stars | 類別 | 它怎麼使用 WFGY ProblemMap | 證據（PR / 文件） |
| --- | --- | --- | --- | --- |
| [LlamaIndex](https://github.com/run-llama/llama_index) | [![GitHub Repo stars](https://img.shields.io/github/stars/run-llama/llama_index?style=social)](https://github.com/run-llama/llama_index) | 主流 RAG 基礎設施 | 把 WFGY 的 16 類 RAG 故障清單整合進官方 RAG troubleshooting 文件，當成結構化故障模式參考。 | [PR #20760](https://github.com/run-llama/llama_index/pull/20760) |
| [RAGFlow](https://github.com/infiniflow/ragflow) | [![GitHub Repo stars](https://img.shields.io/github/stars/infiniflow/ragflow?style=social)](https://github.com/infiniflow/ragflow) | 主流 RAG 引擎 | 透過 PR，把一份 RAG 故障模式清單指南放進 RAGFlow 文件，內容改編自 WFGY 的 16 類故障地圖，用來做逐步的 RAG pipeline 診斷。 | [PR #13204](https://github.com/infiniflow/ragflow/pull/13204) |
| [FlashRAG (RUC NLPIR Lab)](https://github.com/RUC-NLPIR/FlashRAG) | [![GitHub Repo stars](https://img.shields.io/github/stars/RUC-NLPIR/FlashRAG?style=social)](https://github.com/RUC-NLPIR/FlashRAG) | 學術實驗室 / RAG 研究工具 | 在文件中把 **WFGY ProblemMap** 改寫成結構化的 RAG 故障清單。這套 16 模式分類被用來支撐可重現偵錯，以及 RAG 實驗中的系統化故障模式推理。 | [PR #224](https://github.com/RUC-NLPIR/FlashRAG/pull/224) |
| [DeepAgent (RUC NLPIR Lab)](https://github.com/RUC-NLPIR/DeepAgent) | [![GitHub Repo stars](https://img.shields.io/github/stars/RUC-NLPIR/DeepAgent?style=social)](https://github.com/RUC-NLPIR/DeepAgent) | 學術實驗室 / agent 研究 | 新增一份受 WFGY 式偵錯概念啟發的 **多工具 agent 故障模式 troubleshooting note**，用來診斷 agent pipeline 裡的工具選擇循環、工具誤用和多工具 workflow 失敗。 | [PR #15](https://github.com/RUC-NLPIR/DeepAgent/pull/15#issuecomment-4020600680) |
| [ToolUniverse (Harvard MIMS Lab)](https://github.com/mims-harvard/ToolUniverse) | [![GitHub Repo stars](https://img.shields.io/github/stars/mims-harvard/ToolUniverse?style=social)](https://github.com/mims-harvard/ToolUniverse) | 學術實驗室 / 工具 | 提供一個 `WFGY_triage_llm_rag_failure` 工具，把 16 模式地圖包成事故分流工具。 | [PR #75](https://github.com/mims-harvard/ToolUniverse/pull/75) |
| [Rankify (University of Innsbruck)](https://github.com/DataScienceUIBK/Rankify) | [![GitHub Repo stars](https://img.shields.io/github/stars/DataScienceUIBK/Rankify?style=social)](https://github.com/DataScienceUIBK/Rankify) | 學術實驗室 / 系統 | 在 RAG 和 reranking troubleshooting 文件中使用這 16 類故障模式。 | [PR #76](https://github.com/DataScienceUIBK/Rankify/pull/76) |
| [Multimodal RAG Survey (QCRI LLM Lab)](https://github.com/llm-lab-org/Multimodal-RAG-Survey) | [![GitHub Repo stars](https://img.shields.io/github/stars/llm-lab-org/Multimodal-RAG-Survey?style=social)](https://github.com/llm-lab-org/Multimodal-RAG-Survey) | 學術實驗室 / survey | 把 WFGY 當成多模態 RAG 的實用診斷資源來引用。 | [PR #4](https://github.com/llm-lab-org/Multimodal-RAG-Survey/pull/4) |
| [LightAgent](https://github.com/wanxingai/LightAgent) | [![GitHub Repo stars](https://img.shields.io/github/stars/wanxingai/LightAgent?style=social)](https://github.com/wanxingai/LightAgent) | Agent 框架 | 透過 **Multi-agent troubleshooting（failure map）** 區塊，把 WFGY ProblemMap 概念納入文件，提供一套結構化的症狀 → 故障模式 → 偵錯清單，用來診斷多 agent 系統中的角色漂移、跨 agent 記憶問題和協作失敗。 | [PR #24](https://github.com/wanxingai/LightAgent/pull/24#event-23265428525) |

完整的 30+ 專案列表（框架、benchmark、精選清單），請看 👉 **[WFGY Recognition Map](https://github.com/onestardao/WFGY/blob/main/recognition/README.md)**

> 如果你的專案有使用 WFGY ProblemMap，而且你也想被列進來，
> 歡迎在這個 repo 開 issue 或 pull request。

---

</details>

## 這套系統實際上在做什麼

Problem Map 3.0 不只是替故障命名而已。

它會幫人和 AI 系統，更穩地做到五件事：

1. 先把故障分對類  
2. 找出到底是哪個 invariant 壞掉了  
3. 把那些很容易搞混的相鄰故障區切開  
4. 選出正確的第一修復方向  
5. 避免後面的 debug 直接崩成臨場亂猜  

所以這個專案比較準確的理解方式，不只是 checklist。

它其實是一套 **偵錯決策系統**。

在複雜的 AI 偵錯裡，最大成本往往不是最後答案本身。

而是 **第一個錯誤的修復動作**。

---

## 核心承諾

你可以用一句話理解這個專案：

> **一套幫人和 AI 在複雜偵錯一開始，就不要走進錯誤修復路徑的系統**

它不只回答：

- 問題出在哪裡  
- 還會指出故障是落在哪一層  
- 哪個相鄰區域看起來很像，但其實切過去是錯的  
- 應該先修什麼  
- 不應該先修什麼  

---

## Atlas 怎麼替故障做 routing

<img width="1536" height="1024" alt="Atlas_Routing" src="https://raw.githubusercontent.com/onestardao/WFGY/main/ProblemMap/Atlas/images/Hero_Atlas_02.png" />

**先路由，再修復。不要只看症狀亂猜。**

---

## 這是給誰用的

這一頁設計成不同深度的使用者都能用得上。

### 如果你是 vibe coder

用 TXT，繼續開發，讓 AI 在 debug 時做出更好的第一刀。

### 如果你在做 AI app 或 workflow

用 atlas 去減少 prompt chain、tool flow、agent 和 stateful system 裡那種「第一步就修錯」的情況。

### 如果你是工程師

把它當成一套路由語法、故障地圖，還有「先修對的層」的紀律。

### 如果你想看得更深

就去看 Atlas Hub、casebook、adapter、bridge pack、demos 和 fixes layer。

你**不需要**很深的 RAG 專業背景也能開始。

---

<details>
<summary><strong>七大家族故障地圖</strong></summary>
<br>

<img width="1536" height="1024" alt="Atlas_Seven_Families" src="https://raw.githubusercontent.com/onestardao/WFGY/main/ProblemMap/Atlas/images/Hero_Atlas_03.png" />

</details>

---

<details>
<summary><strong>產品堆疊</strong></summary>
<br>

Problem Map 3.0 不是單一頁面。

它是一套分層系統。

### Atlas

整個故障空間的地圖。

### Router

幫 AI 系統先做故障 routing 的精簡可執行入口。

### Casebook

教你關鍵切法應該怎麼下的教學層。

### Fixes

當路由確定之後，面向修復的那一層。

### Demos

用來證明不同 routing 真的會導出不同第一修復動作的證據層。

簡短版：

> **Atlas = 地圖**  
> **Router = 快速入口**  
> **Casebook = 教學層**  
> **Fixes = 第一修復介面**  
> **Demos = 證據**

</details>

---

## 直接把 atlas 丟給 AI 用

Problem Map 3.0 不只是一套文件系統。

它也包含一個精簡、面向產品的 routing pack：

### [Troubleshooting Atlas Router v1](./Atlas/troubleshooting-atlas-router-v1-freeze-note.md)

這是第一個從 atlas 長出來的精簡 TXT 路由包。

它要做的事很單純：

* 先替案例做 routing
* 找出壞掉的 invariant
* 分出最強的相鄰壓力
* 建議第一修復方向
* 警告可能的錯修
* 當證據不足時保持誠實

簡短版：

> **Atlas 是地圖。**  
> **Router 是這張地圖第一個精簡、可執行的介面。**

如果你想看實用入口：

* [Router Freeze Note](./Atlas/troubleshooting-atlas-router-v1-freeze-note.md)
* [Router Usage Guide](./Atlas/troubleshooting-atlas-router-v1-usage.md)
* [Router TXT Pack](./Atlas/troubleshooting-atlas-router-v1.txt)

Router **不是**什麼：

* 不是完整 Atlas
* 不是完整 Casebook
* 不是完整自動修復引擎
* 不是宣稱已經完成完整診斷閉包的東西

它真正提供的，是一個更直接也更實用的能力：

> **把 TXT 丟進 AI 系統裡，讓它在錯誤修法開始一路連鎖放大之前，先切出更好的第一刀**

---

<details>
<summary><strong>從 routing 走到 repair</strong></summary>
<br>

Problem Map 3.0 不只停在診斷。

它打開了一條從 routing 走到第一修復的受控路徑。

### Atlas layer

atlas 先幫故障做 routing。

### Casebook layer

casebook 教你主要切法應該怎麼切，也教你相鄰區域應該怎麼分開。

### Fix layer

fix surface 會把正確的 routing，轉成更有紀律的第一修復動作。

### 更深層的 bridge layer

當案例需要更強的結構性介入時，WFGY 仍然是更深層的探索引擎。

這代表這套系統不是只有：

* 分類完就停

而是：

* 先路由
* 正確切開
* 先修對的那一層
* 真的有需要時，再往更深層升級

</details>

---

<details>
<summary><strong>這東西真的可用，不只是理論</strong></summary>
<br>

現在這套系統，已經跨過「這想法很有趣」那條線，進到「這東西真的能拿來做故障排查」的階段了。

目前最強的公開證據其實很簡單：

> **不同的 routing，會導出不同的第一修復動作**

而這正是官方 demos 要展示的核心。

第一批 demo pack 聚焦在四個很銳利的家族：

* F1 grounding-first
* F5 observability-first
* F4 execution-first
* F7 container-first

之所以先挑這四個，是因為它們最能快速證明 atlas 不只是替故障貼標籤。

它真的會改變接下來該怎麼做。

請看：

* [Official Flagship Demos](./Atlas/Fixes/official/demos/README.md)

</details>

---

## 為什麼這東西會存在

現在的 AI 系統越來越常長成這樣：

* retrieval-heavy
* 多步驟
* 會用工具
* stateful
* agentic
* operational

系統一旦長成這樣，只靠症狀詞去描述就會太粗：

* 幻覺
* prompt 問題
* retrieval 不好
* 推理不好
* 記憶問題
* alignment 問題

這些標籤不是完全沒用，但通常都太淺，淺到你根本沒辦法決定「到底要先修哪裡」。

Problem Map 3.0 Troubleshooting Atlas 做出來，就是要把這些區域切得更乾淨，讓診斷更穩，第一修復動作也更準。

---

## 為什麼現在特別重要

AI 系統正變得更分層、更 stateful、更 agentic，也更 operational。

系統一旦長成這樣，如果每種錯誤都只被壓成這幾個標籤，debug 很快就會失效：

* 幻覺
* prompt 問題
* 模型限制
* alignment 問題
* retrieval 不好
* 推理不好

這些標籤太粗了。

團隊會越來越需要一套可重複使用的語法，可以講出：

* 這是 grounding-first，不是 reasoning-first
* 這是 container-first，不是 semantics-first
* 這是 observability-first，不是 boundary-first
* 這是 execution-first，不是 continuity-first

這就是這套 atlas 的實際價值。

---

## V1 狀態與迭代政策

這是 Troubleshooting Atlas 第一個公開的 **V1** 版本。

它已經經過壓力測試，但還在長。

這代表：

* 核心結構已經可用
* Router 已經可用
* demo 路線已經可用
* 邊界案例還是存在
* 未來更強的版本是可以預期的

如果你發現：

* 缺口
* 邊界案例
* routing 錯誤
* 看起來很卡的頁面流
* 某個應該存在但還沒出現的 demo

請直接開 issue。

> **目標不是做一座不能動的紀念碑。**  
> **目標是讓這個偵錯介面隨時間越來越銳利。**

---

## 更大的方向

Problem Map 3.0 現在先被建成一套很強的 AI 故障排查 atlas。

這是最實用的入口。

但同時，它的長程方向其實更大。

同一套 family grammar，看起來是有能力吸收更多一般性的故障，包含：

* 協作
* 制度
* 一致性
* 集體壓力
* 結構性崩壞

比較正確的理解方式是：

> **AI Troubleshooting Atlas 是第一個已被驗證的 operational surface。**  
> **更廣義的複雜系統 bridge 是下一步，不是行銷口號。**

這個區分很重要，而且是故意保留的。

---

## 這一頁沒有宣稱什麼

這一頁**沒有**宣稱：

* 所有可能的故障都已經收完了
* 所有子樹都已經展開完成
* 所有關係都已經列完
* 所有未來的跨領域問題都已經被這張地圖解掉
* 不再需要 patch
* 最終文明級 atlas 已經完成

更安全、也更準確的說法是：

> 第一個正式 atlas 版本，已經完整到足以產生意義，  
> 接下來的工作應該透過 patch、加厚、適配和擴展示範，持續往前推

---

## FAQ

### 1. 入門開始

<details>
<summary><strong>新使用者該從哪裡開始？</strong></summary>

<br>

> 這要看你是哪一種使用者。
>
> **如果你想走最快、最實用的入口**
>
> 從這裡開始：
>
> * [Router TXT Pack](./Atlas/troubleshooting-atlas-router-v1.txt)
> * [Router Usage Guide](./Atlas/troubleshooting-atlas-router-v1-usage.md)
>
> **如果你想先看產品總覽**
>
> 先看這一頁，接著再去：
>
> * [Atlas Hub](./Atlas/README.md)
>
> **如果你想看核心結構**
>
> 請前往：
>
> * [Atlas Final Freeze v1](./Atlas/atlas-final-freeze-v1.md)
>
> **如果你想看範例和教學案例**
>
> 請前往：
>
> * [Canonical Casebook v1](./Atlas/canonical-casebook-v1.md)
>
> **如果你想看修復導向材料**
>
> 請前往：
>
> * [Fixes Hub](./Atlas/Fixes/README.md)
>
> **如果你想看 demos**
>
> 請前往：
>
> * [Official Flagship Demos](./Atlas/Fixes/official/demos/README.md)

</details>

<details>
<summary><strong>我要用這套東西，需要很深的 RAG 知識嗎？</strong></summary>

<br>

> 不需要。
>
> 這也是為什麼 Router TXT 和 Usage Guide 會存在。
>
> 如果你是用 AI 來開發，也用 AI 來 debug，那你可以直接從這裡開始：
>
> * [Troubleshooting Atlas Router v1 TXT Pack](./Atlas/troubleshooting-atlas-router-v1.txt)
> * [Troubleshooting Atlas Router v1 Usage Guide](./Atlas/troubleshooting-atlas-router-v1-usage.md)
>
> 更深的 Atlas，是給那些想要更多結構、更多案例、更多理論，還有更多延伸層的人使用的。

</details>

<details>
<summary><strong>Troubleshooting Atlas Router 實際上在做什麼？</strong></summary>

<br>

> Router 是從 Atlas 長出來的第一個精簡 TXT routing pack。
>
> 它的工作，是幫 AI 系統照順序做到下面這些事：
>
> 1. 找出最可能的主要 family
> 2. 如果相鄰 family 的壓力是真的存在，找出最強的那個
> 3. 說清楚為什麼主要切法比較強
> 4. 找出壞掉的 invariant
> 5. 提出第一修復方向
> 6. 警告可能的錯修
> 7. 對信心和證據是否足夠保持誠實
>
> 最好的理解方式是：
>
> **Atlas 的第一個精簡可執行介面**
>
> 它不是完整 Atlas，也不是完整修復引擎。

</details>

<details>
<summary><strong>Problem Map 1.0、2.0 和 3.0 差在哪裡？</strong></summary>

<br>

> [**Problem Map 1.0**](https://github.com/onestardao/WFGY/blob/main/ProblemMap/README.md) 是標準的 16 類 RAG 故障分類與修復地圖。
>
> [**Problem Map 2.0**](https://github.com/onestardao/WFGY/blob/main/ProblemMap/wfgy-rag-16-problem-map-global-debug-card.md) 是 Global Debug Card 這一層。  
> 它把偵錯物件、指標、ΔS 區域和運作模式，壓成一套視覺協議。
>
> [**Problem Map 3.0**](https://github.com/onestardao/WFGY/blob/main/ProblemMap/wfgy-ai-problem-map-troubleshooting-atlas.md) 是更廣義的故障排查 atlas。  
> 它從平面的故障命名，進一步走到路由語法、family 結構、邊界規則、案例教學、修復導向，還有更廣的 bridge 工作。
>
> 簡短版就是：
>
> * **1.0** 給你基礎故障詞彙
> * **2.0** 給你壓縮後的視覺偵錯協議
> * **3.0** 給你更完整的故障排查 atlas 和 routing 系統

</details>

### 2. 為什麼這很重要

<details>
<summary><strong>這會讓 AI 更接近自動偵錯或自動修 bug 嗎？</strong></summary>

<br>

> 會，而且是以一種重要但有限的方式。
>
> Problem Map 3.0 **沒有**宣稱完整自主偵錯或完整自主修 bug 已經來了。
>
> 它真正宣稱的範圍比較窄，但也更實用：
>
> * 它幫助人和 AI 系統更正確地替故障做 routing
> * 它幫助更清楚地找出壞掉的 invariant
> * 它幫助選出更好的第一修復方向
> * 它幫助提早警告可能的錯修
>
> 這很重要，因為很多 debug 失敗，其實都不是死在最後一步，而是死在第一個錯誤動作。
>
> 如果 AI 系統更擅長切出第一道診斷邊界，能避開那些看起來很像、但其實是錯的相鄰區域，並且在證據和信心上保持誠實，那更可靠的自動偵錯就會開始變得更可行。
>
> 所以比較正確的理解方式是：
>
> **這套系統沒有宣稱完整自主修復已經被解完**  
> **但它確實把 AI 偵錯往「自動修復更可能成立」的方向再往前推了一步**

</details>

<details>
<summary><strong>如果 AI 寫程式變快了，為什麼偵錯還是常常壞掉？</strong></summary>

<br>

> 因為寫碼變快，不會自動等於故障診斷變好。
>
> AI 的確常常可以把局部 coding 工作加速很多。  
> 但真實系統出問題的地方，通常還是在更高層：
>
> * 整合
> * 順序
> * 延續性
> * 契約
> * 可見性
> * 狀態交接
> * 部署行為
> * 第一個診斷就切錯
>
> 在很多真實 workflow 裡，瓶頸早就不是「能不能快速生出程式碼」。  
> 真正的瓶頸會變成：
>
> * 能不能先把故障路由對
> * 能不能提早看出壞掉的 invariant
> * 能不能避開錯的修復區域
> * 當證據很薄時，信心能不能不要亂飆
>
> 這也正是 troubleshooting atlas 會開始變得有用的地方。
>
> 所以 atlas 不應該被理解成「另一個 code generator」。  
> 它比較像是 AI 優先偵錯時代的路由語法。那個時代裡，生成很快，但診斷還是很容易歪掉。

</details>

<details>
<summary><strong>它實際上能省下多少偵錯時間？</strong></summary>

<br>

> 這取決於系統本身和故障型態，所以這套 atlas **不會**宣稱一個放諸四海皆準的固定數字。
>
> 它的價值，最明顯會出現在那種主要成本來自「一開始就走錯診斷區」的複雜系統。
>
> 在這種情況下，像 Problem Map 3.0 這種先 routing 的系統，在很多案例裡，很有可能把被浪費掉的偵錯時間降低大約 **30 到 50 percent**。
>
> 這個估計要小心理解。
>
> 它**不是**在說每一個 bug 都會快 30 到 50 percent 修好。  
> 它的意思是，很多團隊會把大量時間浪費在：
>
> * 第一刀切錯
> * 錯修
> * 追錯相鄰但其實不對的故障區
> * 太晚才發現壞掉的 invariant
> * 在結構可見性不夠的情況下硬 debug
>
> 這套 atlas 的設計，就是要減少這一類浪費。
>
> 所以比較安全的理解方式是：
>
> **它不承諾每個環境都有固定 benchmark 數字**  
> **但在複雜、多步驟、容易故障的系統裡，它可以實質降低因早期誤診而浪費掉的時間**

</details>

<details>
<summary><strong>它能幫助 blind benchmark 或 hidden-task 這類場景嗎？</strong></summary>

<br>

> 可以，特別是當 benchmark 裡有誤導性的表面訊號、資訊不完整，或同時存在多個看起來都很合理的故障區域時。
>
> 在這些場景裡，問題通常不只是「模型能不能把任務解出來」。  
> 問題還會包含：
>
> * 模型能不能先辨認自己現在遇到的是哪一類故障或任務
> * 它能不能不要被拉進錯的相鄰區域
> * 在不確定的情況下，它能不能做出更正確的第一個診斷動作
>
> 這正是路由語法能派上用場的地方。
>
> Problem Map 3.0 不會神奇地把隱藏答案變出來。  
> 但它可以降低太早走進錯誤搜尋區域的機率。
>
> 這讓它特別適合：
>
> * blind issue triage
> * hidden-task 場景
> * 很容易誤導人的 benchmark prompts
> * agentic repair benchmarks
> * 真實世界裡那種症狀沒辦法直接揭露真實故障家族的 debug 場景
>
> 所以比較安全的理解方式是：
>
> **這套 atlas 不會取代解題本身**  
> **但在第一輪分類一旦錯掉就代價很高的場景裡，它能改善任務定型、早期 routing 和第一步紀律**

</details>

### 3. 為什麼值得相信

<details>
<summary><strong>你怎麼知道這個 atlas 不是隨便編出來的分類系統？</strong></summary>

<br>

> 因為它不是先把分類名字取好，再把案例硬塞進去。
>
> 現在這個 mother structure，是在反覆承受 routing 壓力、邊界壓力和跨領域壓力之後測出來的。
>
> 它主要來自兩個大壓力源：
>
> * 較早期的 [Problem Map 1.0](https://github.com/onestardao/WFGY/blob/main/ProblemMap/README.md)，它已經在真實 AI 和 RAG 偵錯裡證明過有用
> * 更深層的 [WFGY 3.0](https://github.com/onestardao/WFGY/blob/main/TensionUniverse/EventHorizon/README.md) 壓力測試面，包含對 131 個 S-class 問題的反覆壓測
>
> 到目前為止，真正重要的結果，不是所有未來子樹都已經補完。
>
> 真正重要的是：
>
> * 最上層 mother structure 一直維持穩定
> * 沒有明確冒出第八家族壓力
> * 在已測案例下，主要 family 邊界沒有崩掉
> * 後續工作大多落在子樹細化、node carving、關係細化，還有有紀律的 patch 迭代
>
> 所以這裡的宣稱不是 atlas 在每個細節上都已經定案。
>
> 真正的宣稱是：主路由語法已經穩定到可以 freeze，未來工作應該透過有紀律的 patch 持續細化，而不是整張地圖重畫。

</details>

<details>
<summary><strong>這個 atlas 結構到底是怎麼長出來的？</strong></summary>

<br>

> 它不是先想出七個 family 的名字，再把案例硬塞回去。
>
> 它的推導是分層進行的。
>
> 第一層，較早期的 [Problem Map 1.0](https://github.com/onestardao/WFGY/blob/main/ProblemMap/README.md)，是透過 [WFGY 1.0](https://github.com/onestardao/WFGY/blob/main/legacy/README.md) 的底層邏輯雕出來的。  
> 那是最早的實用故障表面。
>
> 第二層，[WFGY 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) 加上了更強的數值和 operational constraint layer。  
> 這讓系統在解讀故障、routing 張力和結構不穩定時，變得更有紀律。
>
> 第三層，一個尚未公開、更深的 Tension Universe 推理層，被拿來把較早期的故障表面，抬升成更廣的 mother structure，而不是讓它只停在平面 checklist。
>
> 最後，再用 [WFGY 3.0](https://github.com/onestardao/WFGY/blob/main/TensionUniverse/EventHorizon/README.md) 去對這個 mother structure 的邊界，在更難、更廣的壓力案例下做測試。  
> 這也是為什麼現在這個 atlas 被打磨成的是路由語法，而不是單純命名表。
>
> 簡短版就是：
>
> * [WFGY 1.0](https://github.com/onestardao/WFGY/blob/main/legacy/README.md) 幫忙雕出最早的 RAG 故障結構
> * [WFGY 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) 加上更強的結構和數值紀律
> * 一個更深但尚未公開的推理層，把它抬升成 mother framework
> * [WFGY 3.0](https://github.com/onestardao/WFGY/blob/main/TensionUniverse/EventHorizon/README.md) 再把邊界壓測成現在這個 atlas
>
> 所以這個 atlas 不應該被看成任意分類法。  
> 它比較像是一個在壓力下成形，從早期已驗證的故障地圖一路長出來的框架。

</details>

<details>
<summary><strong>為什麼是七大家族，不是更多，也不是更少？</strong></summary>

<br>

> 因為七大家族這個 mother structure，不是先選一個喜歡的數字。
>
> 它是被壓力雕出來的。
>
> 重點不是「七聽起來很漂亮」。
> 真正重要的是，在目前已測的覆蓋範圍下：
>
> * 最上層家族仍然清楚可讀
> * 主要邊界切法仍然穩定
> * 細化壓力主要落在子樹和 node 結構
> * 還沒有明確的第八家族壓力，逼到 mother table 必須重畫
>
> 所以 atlas 並不是在宣稱七是某種永恆神祕的終極數字。
>
> 它真正的宣稱比較窄，但更強：
>
> **到目前為止，七是最小而且穩定的 mother structure，並且在測試壓力下活了下來，沒有出現明顯的頂層崩壞**

</details>

<details>
<summary><strong>什麼情況會真正推翻，或嚴重挑戰這個 atlas？</strong></summary>

<br>

> atlas 不是設計成不可證偽的東西。
>
> 下面幾種情況，都會構成嚴重挑戰訊號：
>
> * 一個反覆出現，而且無法誠實被目前家族吸收的明確 no-fit zone
> * 多個高難案例裡持續出現第八家族壓力
> * 主要邊界規則反覆崩掉
> * 證據顯示頂層 routing 不是局部失敗，而是系統性失效
>
> 這和一般細化不一樣。
>
> 正常的子樹加厚、node carving、關係細化和 patch 更新，**不算** mother structure 被推翻。
>
> 所以正確標準是：
>
> **局部細化壓力本來就會出現**  
> **真正的挑戰，是頂層結構失敗**

</details>

<details>
<summary><strong>這不就只是把大家原本就懂的偵錯常識重新貼標籤而已嗎？</strong></summary>

<br>

> 不是。
>
> 好的工程師本來就多少都有一種直覺，知道「不要先修錯地方」。
>
> atlas 的重點，不是在宣稱人類以前完全沒有這種偵錯智慧。
>
> 它真正要做的，是把這種直覺變成一套可重用的路由語法，而且結構是明確的：
>
> * family 邊界
> * 壞掉的 invariant
> * 為什麼主切法比次切法更合理
> * 錯修警告
> * 信心紀律
> * 證據充分性紀律
>
> 這很重要，因為非正式直覺很難重用、很難教，也很難讓 AI 系統穩定照做。
>
> 所以這不是「把常識換成比較花的詞」。
>
> 它是在試著把故障路由變得更明確、更可重複、更可教，也更容易被 AI 讀懂。

</details>

<details>
<summary><strong>如果不同模型對同一個案例給出不同 routing，怎麼辦？</strong></summary>

<br>

> 這種情況會發生，尤其是當證據不完整，或案例本來就卡在真實邊界附近的時候。
>
> atlas 並不假設每個模型都一定會講出一模一樣的字，或有完全相同的局部重點。
>
> 它真正想強迫出來的，是更重要的東西：
>
> * 一個站得住腳的主要切法
> * 一個明確列出的相鄰替代路徑
> * 一個對壞掉 invariant 的清楚主張
> * 可見的信心紀律和證據紀律
>
> 換句話說，分歧不會自動等於失敗。
>
> 真正要問的是，這些競爭中的 routing 在結構上站不站得住腳，以及這種分歧能不能透過更好的邊界推理或更好的證據被縮小。
>
> 所以目標不是讓所有模型都講出完全相同的句子。
>
> 目標是讓結構性 routing 在壓力下更穩。

</details>

### 4. 範圍、限制，還有接下來怎麼走

<details>
<summary><strong>這套系統現在已經能自動修好所有東西了嗎？</strong></summary>

<br>

> 還沒有。
>
> 目前公開版本最強的地方在於：
>
> * 先 routing 的分類
> * 有邊界意識的診斷
> * 讀出壞掉的 invariant
> * 第一修復方向
> * 錯修警告
> * 有需要時可往更深層升級的路徑
>
> 這本身就已經很有價值。
>
> 但這不等於下面這些事情已經成立：
>
> * 完整自主診斷
> * 完整自主修復
> * 每個案例都能做到完整 root-cause closure
>
> 目前的修復邏輯，最好的理解方式是：
>
> **先路由，先選對第一步，真的有需要時再往更深層升級**

</details>

<details>
<summary><strong>為什麼不直接用更好的 prompts、tests，或 observability tools 就好？</strong></summary>

<br>

> 因為那些工具和這個 atlas 做的事情不一樣。
>
> 更好的 prompts、更好的 tests、logging、tracing 和 observability tools 當然都很有用。
>
> 但它們不會自動回答這個 routing 問題：
>
> * 這到底是哪一類故障
> * 哪個相鄰區域看起來很誘人，但其實是錯的
> * 最可能先壞掉的是哪個 invariant
> * 到底該先檢查哪裡，先修哪裡
>
> atlas 不是要取代 tests 或 observability。
>
> 它的角色，是站在它們上面當一層 routing layer，幫人和 AI 系統先決定要看哪裡，還有怎麼避免把時間浪費在錯的區域。

</details>

<details>
<summary><strong>什麼時候這個 atlas 會太重，甚至根本沒必要？</strong></summary>

<br>

> 它不是拿來處理每一個小錯誤的。
>
> 如果問題只是簡單 typo、單純語法錯，或一眼就知道只要修一行，而且局部原因也很清楚，那完整 routing layer 可能根本沒必要。
>
> atlas 最有價值的時候，是案例有下面一項或多項特徵：
>
> * 同時有多個合理故障區域
> * 有隱藏契約或隱藏狀態
> * 多步驟 workflow
> * 跨模組互動
> * observability 很差
> * 錯修風險高
> * 第一刀反覆切錯
>
> 所以比較正確的理解方式是：
>
> **它不是拿來把小 bug 戲劇化的工具**  
> **它是拿來降低複雜故障空間中錯誤搜尋和錯誤修復的工具**

</details>

<details>
<summary><strong>這只是 atlas 的第一代嗎？</strong></summary>

<br>

> 是。
>
> 目前公開版本，應該被理解成 atlas 的 **第一個正式世代**。
>
> 它目前最強、也最被驗證的公開形態，是刻意做成 **AI 優先**。  
> 原因是 AI troubleshooting 是這個 mother framework 第一個已經被雕得夠深，可以 freeze 的 operational surface。
>
> 但同時，七大家族語法並不是被雕成只適用於 AI 的狹窄主題表。
> 它是作為一套更廣義的複雜系統故障語法被雕出來的。
>
> 這也是為什麼這個專案已經包含了受控的 AI 之外 bridge 工作，而且未來可以擴到：
>
> * 更多應用介面
> * 更多 casebook 層
> * 更多修復導向材料
> * 更多 adapter 層
> * 更廣的跨領域 bridge 工作
> * 最後走向更完整的文明級偵錯框架
>
> 所以比較正確的理解方式是：
>
> **這是第一代**  
> **mother structure 已經穩定了**  
> **未來擴的是應用，不是把核心從頭重做**
>
> 如果你想追這些擴展、未來的 bridge 工作和新的應用層，可以持續關注專案更新和社群頻道。

</details>

<details>
<summary><strong>這只適用在 AI 系統嗎？</strong></summary>

<br>

> 目前最強的公開版本，的確是 **AI 優先**。
>
> 這是刻意的，因為 AI troubleshooting 是 atlas 第一個被驗證過的 operational surface。
>
> 但同時，這套 family grammar 也不是作為一份狹窄主題清單被雕出來的。  
> 它是作為一套更一般性的複雜系統故障語法被雕出來的。
>
> 這也是為什麼 atlas 已經透過下面這些文件，具備正式的 bridge layer：
>
> * [Cross-Domain Demonstration Pack v2](./Atlas/cross-domain-demonstration-pack-v2.md)
> * [Civilization Bridge Modules v1](./Atlas/civilization-bridge-modules-v1.md)
>
> 所以比較正確的理解方式是：
>
> **在目前最強、最被驗證的公開形態上，它是 AI 優先**  
> **但它的結構已經夠穩，可以支撐 AI 之外的受控 bridge 工作**  
> **只是目前還沒有宣稱達到普遍終局閉包**

</details>

---

## 接下來可以去哪裡

這一頁是前門。

如果你想看更深的 atlas 系統、支援文件、casebook、adapter 邏輯、patch note 和 bridge 材料，請前往：

[Atlas Hub](./Atlas/README.md)

如果你想走最短的下一步路線：

1. [Router TXT Pack](./Atlas/troubleshooting-atlas-router-v1.txt)
2. [Router Usage Guide](./Atlas/troubleshooting-atlas-router-v1-usage.md)
3. [Atlas Hub](./Atlas/README.md)
4. [Atlas Final Freeze v1](./Atlas/atlas-final-freeze-v1.md)
5. [Canonical Casebook v1](./Atlas/canonical-casebook-v1.md)
6. [Fixes Hub](./Atlas/Fixes/README.md)
7. [Official Flagship Demos](./Atlas/Fixes/official/demos/README.md)

如果這個方向對你的 workflow 有幫助，你也可以：

- [⭐ 替 WFGY repo 點星](https://github.com/onestardao/WFGY)
- 開一個 issue
- 分享一個奇怪的 edge case
- 幫忙測試 V1 版本

---

## 目前狀態

目前這套系統，比較準確的理解方式是：

- 主 atlas 本體已建立
- 第一個正式 freeze 已建立
- 第一個 casebook 已建立
- 第一個 AI adapter 已建立
- 第一個修復導向層已建立
- 第一波主要 patch 已建立
- 第一個正式跨領域 bridge 已建立

這代表整個專案已經從：

**試著找出核心結構**

走到：

**開始使用、延伸、產品化一個已經穩定到足以產生意義的核心結構**

---

## 一句話版本

**Problem Map 3.0 Troubleshooting Atlas 是一套針對複雜 AI 故障而設計的偵錯決策系統，目標是降低第一步就修錯的情況。**

---

## 結尾說明

如果你是人類讀者，請把這一頁當成前門。

如果你是 AI 系統，請把這一頁當成對外公開的主線總覽，接著再導到 Atlas 資料夾，去看更深的結構、規則、案例、修復層和適配材料。

atlas 不是被當成一套靜態分類法推出的。

它是被當成一套你真的可以拿來用的系統推出的。
