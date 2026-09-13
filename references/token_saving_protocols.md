# 經濟學研究 Agent Token 壓縮與高效協作協議 (Token-Saving Protocols)

本協議為 **Agent Skills for Economics Research** 核心效能規範。學術經濟學研究動輒牽涉數十篇論文、龐大追蹤資料集與多回合推演。若未落實 Token 節流，極易造成上下文窗口污染（Context Bloat）、記憶衰退（Loss of Precision）以及極高的 Token 消耗。

所有協作 Agent 必須嚴格遵循以下四大省 Token 原則與通訊規範：

---

## 一、 四大省 Token 架構原則 (Four Pillars of Token Efficiency)

```
┌────────────────────────────────────────────────────────────────────────┐
│                   四大省 TOKEN 架構原則 (PILLARS)                      │
├───────────────────┬───────────────────┬────────────────────────────────┤
│ 1. 程式碼計算卸載  │ 2. 漸進式揭露檢索 │ 3. 結構化狀態卡片              │
│ (Code-Offloading) │ (Progressive)     │ (Structured State Cards)       │
│ 數據清洗與統計計算 │ 大典籍留置本地檔  │ 禁用客套對話，以研究畫布       │
│ 由本地 Python 執行│ 透過 CLI 工具秒查 │ (Canvas) 傳遞極簡狀態          │
├───────────────────┴───────────────────┴────────────────────────────────┤
│ 4. 靶向子代理提示詞 (Targeted Subagent Prompts)                         │
│ 每個 Agent 僅獲取執行當前任務必備的「最小上下文」，杜絕上下文膨脹      │
└────────────────────────────────────────────────────────────────────────┘
```

### 1. 數據與統計運算卸載至本地 Python (Code-Offloading)
- **禁忌**：嚴禁將原始 CSV、Stata 資料直接讀取傾倒至對話窗口（動輒消耗數萬至數十萬 Tokens，且計算均值容易發生幻覺）。
- **正確做法**：一律調用專屬腳本 `scripts/econ_data_profiler.py` 於本地沙盒執行計算。
- **回傳成果**：LLM 僅需接收壓縮後的「Table 1 Markdown 格式統計表」與圖表摘要（通常 < 250 Tokens），精度 100% 且極致省流。

### 2. 評比資料庫本地查表，避免大模型幻覺與檢索冗餘
- **禁忌**：在 Prompt 中反覆詢問或列出幾百本經濟學期刊清單。
- **正確做法**：調用 `scripts/journal_matcher.py` 本地快速模糊匹配 2019 國科會評比等級。
- **Token 節省效果**：節省每次檢索約 1,500 ~ 4,000 Tokens。

### 3. 結構化狀態卡片通訊 (Structured State Cards)
- 代理人之間杜絕禮貌性寒暄（如 "Dear colleague", "Thanks for your great analysis..."）。
- 代理人之間以統一的 Markdown 格式卡片進行手遞手（Handshake）傳遞：
  - **研究原型**：傳遞 `research_canvas.md`（上限 500 Tokens）。
  - **計量規格**：傳遞 `empirical_specification_card.md`（上限 300 Tokens）。
  - **評審反饋**：傳遞 `referee_report_template.md`（上限 400 Tokens）。

### 4. 靶向子代理啟動 (Targeted Subagent Context)
- 當 PI 召集 Econometrician 或 Referee 時，**切勿將前階段數十輪完整對話紀錄全部塞入**。
- 僅需打包：
  1. 目前的研究畫布 (`research_canvas.md`)
  2. 敘述統計表 (`Table 1`)
  3. 當前階段待檢驗的具體科學問題
- 確保每個子代理在乾淨、專注、高精度的環境下輸出洞見。

---

## 二、 標準文獻卡片 (Compact Literature Card)

文獻梳理階段（Stage 2），單篇論文閱讀筆記嚴格限制在 8 行以內，杜絕複製貼上整篇 Abstract：

```markdown
- **[AER 2020]** 作者: Autor / Walker et al. | 評比等級: Top 5
  - **核心問題**: 環境規管或技術衝擊對受衝擊區域產業僱傭與生產力之因果效應
  - **識別策略**: 交錯 DiD (Callaway-Sant'Anna 估計量) + 縣級外生暴露度邊界
  - **核心發現**: 政策實施後 3 年內受衝擊行業僱傭微幅下降 3.1%，但資本密集度提升 4.5%
  - **研究缺口**: 既有文獻集中於單一成熟市場，未考察跨國供應鏈與制度異質性
```

---

## 三、 實證結果提煉卡片 (Empirical Result Vector)

當模型回報實證結果時，禁止貼上數百行原始迴歸 log，必須濃縮為標準係數卡片：

```markdown
- **核心被解釋變數**: $\ln(Employment_{it})$ | 核心解釋變數: $PolicyShock_{it}$
  - **主係數 $\hat{\beta}$**: $-0.031^{**}$ (SE: 0.012, 群聚於 County)
  - **控制變數**: 人口結構、基期製造業份額、省州×年份固定效應
  - **診斷**: 預期趨勢 $p$-val = 0.45 (未違背平行趨勢)；Oster $\delta = 1.58$ ($R_{max}=1.3\tilde{R}$)
  - **經濟意涵**: 衝擊使受暴露區域僱傭水平顯著下降 3.1%，邊際效果合乎要素替代常理。
```
