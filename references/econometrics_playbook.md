# 計量經濟學實證與因果推論實戰手冊 (Econometrics Playbook)

本手冊為 **Agent Skills for Economics Research** 的計量方法論與因果識別（Identification Strategy）核心依據。在審查任何研究設計、估計模型或研究結果時，所有 Agent 必須以此清單進行嚴格把關。

---

## 一、 內生性四大來源與防禦矩陣 (Endogeneity Taxonomy)

任何迴歸模型若未妥善處理內生性（$Cov(X, arepsilon) 
eq 0$），估計量將不具因果推論力：

| 內生性來源 | 典型情境 | 數學偏差方向 | 防禦與解決方案 |
| :--- | :--- | :--- | :--- |
| **遺漏變數偏差 (OVB)** | 能力未控制、地區文化、非觀測衝擊 | $	ext{plim} \hat{eta}_{OLS} - eta = \gamma rac{	ext{Cov}(X, W)}{	ext{Var}(X)}$ | 高維度固定效應 (Two-way FE)、Oster (2019) 係數穩定性檢定、工具變數 |
| **逆向因果 / 聯立性 (Reverse Causality)** | 治安支出與犯罪率、資料中心進駐與電價雙向影響 | 係數符號反轉或大幅高估 | 政策衝擊 (DiD)、外生天災衝擊、歷史沉沒成本/地理稟賦作為工具變數 |
| **選擇性偏差與分流 (Selection & Sorting)** | 企業自願申請補貼、高技能人口遷徙至特定城市 | 樣本自選擇導致殘差條件期望值非零 | Heckman 兩階段修正、邊界斷點 (Spatial RDD)、傾向評分配對 (PSM/CEM) |
| **衡量誤差 (Measurement Error)** | 調查收入低報、代理變數失真 | 古典誤差導致向零收縮衰減偏差 (Attenuation Bias) | 多指標整合、結構估計、高品質行政登記資料 (Administrative Data) |

---

## 二、 核心因果推論設計與診斷標準

### 1. 差異中之差異 (Difference-in-Differences, DiD) 與事件研究法 (Event Study)

#### (1) 平行趨勢假定 (Parallel Trends Assumption)
- 處理前（Pre-treatment）所有期數之估計係數必須在統計上不顯著異於零（即無領先效應）。
- 繪製事件研究圖（Event Study Plot）：$y_{it} = lpha_i + \lambda_t + \sum_{k 
eq -1} eta_k \cdot \mathbb{I}(t - E_i = k) + \mathbf{X}_{it}oldsymbol{\gamma} + arepsilon_{it}$。
- 推薦使用 Rambachan & Roth (2023) 的 **HonestDiD** 檢驗平行趨勢線性偏離時的敏感性邊界。

#### (2) 現代交錯處理 (Staggered Treatment) 必備修正
- **傳統 TWFE 致命缺陷**：Goodman-Bacon (2021) 證明，若各組介入時間不同且處理效果隨時間異質性變化，早期受處理組會成為晚期受處理組的對照組，產生「負權重 (Negative Weights)」導致係數符號完全相反。
- **必備前沿估計量 (Modern DiD Estimators)**：
  1. **Callaway & Sant’Anna (2021)**: 分組-時間平均處理效果 $ATT(g, t)$，以未受處理組或尚未受處理組作為對照組（R: `did`, Stata: `csdid`, Python: `csdid`）。
  2. **Sun & Abraham (2021)**: 交互加權估計量（Interaction Weighted Estimator，R: `fixest::sunab`）。
  3. **Borusyak, Jaravel, & Spiess (2024)**: 插補估計量（Imputation Estimator，`did_imputation`）。
  4. **de Chaisemartin & D’Haultfœuille (2020)**: `did_multiplegt` 異質性加權診斷。

---

### 2. 工具變數法 (Instrumental Variables / 2SLS)

#### (1) 相關性條件 (Relevance Condition)
- 第一階段 $F$ 檢定值檢驗：
  - 單一內生變數：傳統經驗法則為 $F > 10$；現代計量標準遵循 **Montiel Olea & Pflueger (2013)** 有效 $F$ 檢定，防範弱工具變數偏差。
- 弱工具變數救濟：使用 Anderson-Rubin (AR) 統計量或 Fuller-k 估計量。

#### (2) 外生性與排他性限制 (Exclusion Restriction)
- $Cov(Z, arepsilon) = 0$ 且工具變數 $Z$ 只能透過內生變數 $X$ 影響被解釋變數 $Y$。
- **Shift-Share / Bartik 工具變數診斷**：
  - 根據 Goldsmith-Pinkham, Sorkin, & Swift (2020)，需檢驗初始份額（Initial Shares）的外生性，並報告 Rotemberg 權重。
  - 根據 Borusyak, Hull, & Jaravel (2022)，若訴諸衝擊外生性，需檢驗衝擊在時間或行業上的準隨機性。

---

### 3. 迴歸斷點設計 (Regression Discontinuity Design, RDD)

#### (1) 連續性檢定 (Density Continuity Test)
- 檢驗分流變數（Running Variable）在門檻值（Cutoff）處是否存在人為操縱：
  - **McCrary (2008)** 密度檢定或 **Cattaneo, Jansson, & Ma (2020)** 的平滑度檢定。

#### (2) 局域隨機性與共變數平衡 (Covariate Balance)
- 檢驗所有在門檻前已決定的前定變數（Predetermined Covariates），在切點兩側不得有不連續跳躍。

#### (3) 最佳頻寬選取 (Optimal Bandwidth)
- 採用 **Calonico, Cattaneo, & Titiunik (2014, 2020)** `rdrobust` 算法：
  - 報告 MSE-optimal 頻寬與 CER-optimal 頻寬下的偏差修正估計量（Robust Bias-Corrected Inference）。
  - 同時報告頻寬乘上 0.5 倍與 2 倍的敏感性測試。

---

### 4. 合成對照法 (Synthetic Control & Synthetic DiD)

- **傳統 SCM** (Abadie, Diamond, & Hainmueller 2010, 2015)：僅單一處理單元，建構凸組合權重對照組；必須執行空間安慰劑（In-space placebo）與時間安慰劑（In-time placebo）。
- **Synthetic DiD** (Arkhangelsky, Athey, Hirshberg, Imbens, & Wager 2021)：結合 SCM 的單元加權與雙重差分的單元固定效應，放寬傳統 SCM 的無截距限制，極大提升追蹤資料估計精度（`synthdid`）。

---

## 三、 標準誤群聚與推論準則 (Standard Error Protocols)

1. **群聚層級 (Clustering Level)**：
   - 遵循 Abadie, Athey, Imbens, & Wooldridge (2023) 原則：**標準誤必須群聚在處理變數被指派（Assignment of Treatment）的層級**（例如州政策衝擊群聚在州，縣政策群聚在縣）。
2. **小群聚問題 (Few Clusters Problem)**：
   - 當群聚數目少於 30 至 50 個時，一般漸近標準誤會嚴重向下偏誤（導致過度拒絕虛無假設）。
   - 必須使用 **Cameron, Gelbach, & Miller (2008)** 的野群聚拔靴法 (Wild Cluster Bootstrap, `boottest`)。
3. **空間自相關 (Spatial Autocorrelation)**：
   - 地理鄰近單元之殘差若具外溢與相關性，採用 **Conley (1999)** 空間 HAC 標準誤。

---

## 四、 頂刊級穩健性檢驗清單 (Robustness Playbook)

任何實證論文要通過 Top 期刊 Referee 的考驗，必須在 Stage 4 中涵蓋以下穩健性檢定：

1. **Oster (2019) 係數穩定性檢定**：
   - 評估未觀測變數需達到觀測控制變數的幾倍相關度（$\delta$），才會使實證效果完全歸零。一般標準需達到 $\delta \ge 1$ (在 $R_{max} = 1.3 	imes 	ilde{R}$ 條件下)。
2. **安慰劑檢驗 (Placebo Tests)**：
   - 偽時間點（Fake timing）：將處理時間提前 2~3 年，驗證虛假政策不顯著。
   - 偽處理組（Fake treatment units）：隨機置換未受處理單元，進行 500-1000 次蒙地卡羅 Permutation Test。
3. **極端值與樣本敏感性 (Sensitivity to Outliers)**：
   - 逐一剔除主要城市/超級大廠（Leave-one-out Jackknife）。
   - 1% 與 99% 分位數 Winsorization / Trimming 比較。
4. **機制檢驗 (Mechanism & Channel Tests)**：
   - 檢驗中間傳遞媒介（Mediation Analysis），證明因果鏈條存在（而非黑盒子關聯）。
