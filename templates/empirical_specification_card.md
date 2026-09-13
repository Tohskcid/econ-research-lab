# 實證模型規格卡 (Empirical Specification Card)

> 用於跨 Agent 快速傳遞計量模型設定，嚴格限制長度於 300 Tokens 內。

---

## 1. 基準迴歸方程 (Baseline Equation)
$$Y_{it} = \beta \cdot D_{it} + \mathbf{X}_{it}^\prime \boldsymbol{\gamma} + \alpha_i + \lambda_t + \varepsilon_{it}$$

- **被解釋變數 ($Y_{it}$)**: `[變數名稱、定義、對數或比率型態]`
- **核心處理變數 ($D_{it}$)**: `[政策虛擬變數 / 連續暴露度量 / 設施進駐變數]`
- **核心參數 $\beta$ 意涵**: `[若 D 增加 1 單位，Y 變化之百分比或邊際效果]`

## 2. 固定效應與群聚推論 (Fixed Effects & Clustering)
- **個體固定效應 ($\alpha_i$)**: `[如: 縣級固定效應 (County FE) 吸納不隨時間變化的地理與文化特徵]`
- **時間固定效應 ($\lambda_t$)**: `[如: 年份固定效應 (Year FE) 或 州×年份固定效應 吸納總體宏觀衝擊]`
- **共變數矩陣 ($\mathbf{X}_{it}$)**: `[控制變數清單，注意避免放入壞控制變數 Bad Controls]`
- **標準誤群聚層級 (SE Clustering)**: `[如: Clustered at County level / State level]`

## 3. 識別假設與前置檢定 (Identification Diagnostics)
- **平行趨勢檢定**: `[事件研究法 Pre-trends p-value]`
- **交錯處理防禦**: `[採用 Callaway-Sant\x27Anna / Sun-Abraham 替代傳統 TWFE]`
- **工具變數 (若適用)**: `[第一階段 F 統計量、排他性邏輯論證]`

## 4. 必做穩健性清單 (Robustness Suite)
- `[ ]` Oster (2019) 係數穩定性檢定 ($\delta \ge 1$)
- `[ ]` 安慰劑時序檢定 (Fake Treatment Timing)
- `[ ]` 樣本極端值 Winsorization (1% / 99%)
- `[ ]` 剔除最大單元 (Leave-one-out Jackknife)
