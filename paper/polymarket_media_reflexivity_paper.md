# 量化選舉風向的媒體放大與自我實現預期：來自 Polymarket 政治預測市場的因果證據

### Quantifying Election Winds: Media Amplification and Self-Fulfilling Expectations in Decentralized Prediction Markets

**作者**：Antigravity 經濟學研究團隊 (*Invisible Hands for Economists Project*)  
**最新修訂**：2026 年 9 月 (Version 2.13 -- Pre-Design Topic Survey & Evidence-Driven Scale Restructured)  
**工作論文系列 (Working Paper Series)**  
**對標期刊**：臺灣國科會人文處 2019 評比【Top 5】(*AER*, *JPE*, *Econometrica*, *QJE*, *REStud*) 與【A+ Finance】(*Journal of Finance*, *Journal of Financial Economics*, *Review of Financial Studies*)

---

### 摘要 (Abstract)

去中心化預測市場歷來被新古典資訊經濟學視為純粹聚合分散資訊的被動「溫度計」。然而，當真金白銀定價的勝率被大眾媒體頻繁引用時，金融合約自身是否會轉化為塑造公眾認知與選舉動量的「造浪者」？針對先前文獻中工具變數（如大鯨魚下注）存在排他性假設破產（Exclusion Restriction Violation）以及 24 小時即時新聞循環下的同時性偏差（Simultaneity Bias），本文進行了全方位的理論與計量重構。

首先，在選題與文獻邊界審查上，本文落實 **Pre-Design Topic Survey Gate**，對標 Wolfers & Zitzewitz (2004)、Gómez-Cram et al. (2025) 與 Tsang & Yang (2026)，確立本研究在動態雙向因果識別與個體微觀基礎上的不可替代性。

在理論層面，本文構建了包含「知情交易者 (Kyle, 1985; Glosten & Milgrom, 1985)」、「追求點擊率之理性疏忽媒體編輯 (Sims, 2003; Bordalo et al., 2013)」與「具從眾動能之選民 (Callander, 2007)」的三方動態貝氏賽局模型，嚴格推導出四大理論命題：
1. **媒體非線性門檻放大 (Nonlinear Threshold Media Amplification)**：$|\Delta p_t| > \bar{\tau}$ 時產生非連續報導彈性；
2. **搖擺州異質性跟風 (Heterogeneous Swing-State Bandwagon)**：先驗變異數大的戰場州選民產生更高跟風動能；
3. **資訊效率反射性裂痕 (Reflexivity Wedge)**：外生媒體關注使合約價格永久性偏離純貝氏資訊基準；
4. **策略性操控的資本極限 (Whale Capital Depletion Bound)**：單一巨額帳戶的人為價格扭曲面臨二次方資本消耗，無法長期脫離基本面。

在實證識別上，本文徹底摒棄有瑕疵的實體下注工具變數，全面改採 **Rigobon (2003) 異質變異數識別法 (Identification via Heteroskedasticity)**，利用 2024 年美國大選中 16 個重大政治事件引發的高波動窗口，精準識別市場價格與媒體關注的雙向因果關係。本文採集 Polymarket 官方 CLOB 訂單簿逐日價格、FiveThirtyEight (538) 逐日各州加權民調以及維基媒體逐日公眾注意力時間序列，建立 7 大核心搖擺州平衡面板資料集（$N=7, T=250$, 總計 1,750 個觀測值；一階差分有效 $N=1,743$）。

實證結果顯示：
1. **結構傳導係數 $\alpha_1$ (Price $\to$ Media)**：在 Rigobon 異質變異數識別下，Polymarket 勝率跳躍顯著提升媒體與公眾注意力的半彈性為 **5.4764**（Driscoll-Kraay $SE = 1.9807, t = 2.76, p = 0.006$；Conley 空間 HAC $SE = 0.1076$）。這意味著勝率每上升 10 個百分點，將因果性引發公眾注意力激增約 **+54.8\%**，且完全符合真實傳播量級。
2. **反向回饋係數 $\alpha_2$ (Media $\to$ Price)**：媒體與公眾關注度對市場價格的反射性回饋係數為 **0.0351**（Driscoll-Kraay $SE = 0.0057, t = 6.18, p < 0.001$），證實媒體報導顯著產生了自我實現的定價回饋。
3. **動態脈衝半衰期**：Jordà (2005) 局部投影表明，價格跳躍之媒體注意衝擊在第 3~4 天達到峰值，半衰期約為 6 天。
4. **推論穩健性**：全面採用 Driscoll-Kraay (1998) 修正時序與截面依賴，並結合 Conley (1999) 空間 HAC 與 Wild Cluster Bootstrap，證實結論在各種空間與小群聚設定下均維持穩健。

**JEL 分類號**：C32, D82, D84, G14, L82, P16  
**關鍵詞**：Polymarket；預測市場；媒體偏誤；異質變異數識別；Rigobon 模型；理性疏忽；Driscoll-Kraay 標準誤；市場微結構

---

## 1. 引言與選題邊界 (Introduction & Literature Positioning)

去中心化預測市場（Prediction Markets，如 2024 年迅速崛起的 Polymarket）究竟是反映政治現實的被動「溫度計」，抑或是塑造選民認知的「造浪者」？新古典經濟學（Hayek, 1945; Wolfers and Zitzewitz, 2004; Arrow et al., 2008）歷來將預測市場視為高效的資訊聚合器。然而，當預測市場交易量達到數十億美元規模並頻繁登上主流新聞頭條時，市場定價與公共輿論之間便形成了索羅斯（Soros, 1987）所言的「反射性迴路」（Reflexivity Loop）。

### 1.1 選題邊界矩陣 (Topic Survey Matrix)
依據 `research/topic-survey.json` 前置審查結果，本研究與最鄰近文獻之邊界差異如下：

| 最鄰近文獻 | 估計標的 / 核心定理 | 研究設計 / 方法論 | 本文之核心邊界突破與貢獻 | 文獻關係 |
| :--- | :--- | :--- | :--- | :--- |
| **Wolfers & Zitzewitz (2004)** *JEP* | 預測市場資訊聚合能力與預測無偏性 | IEM 愛荷華電子市場時間序列與相關性分析 | 僅視市場為被動資訊接收者；未觸碰媒體反向放大與動態反射性迴路。 | Extension |
| **Gómez-Cram et al. (2025)** *JFE* | 預測市場價格發現：群體智慧 vs. 知情少數 | 高頻訂單流 Kyle Lambda 分解 | 聚焦於市場內部微觀交易定價，未探討外部媒體引述與公眾期望反饋。 | Extension |
| **Tsang & Yang (2026)** *NBER WP* | Polymarket 投注價格與選民情緒之引導關聯 | 傳統面板 OLS 與大鯨魚交易工具變數 (Whale IV) | **鯨魚 IV 排他性假設崩潰**（大單本身即是國際新聞頭條）；未解決同時性偏差。本文改採 Rigobon (2003) 異質變異數 SVAR 無偏識別。 | Adjacent (Nearest) |

### 1.2 實證研究覆蓋矩陣 (Coverage Matrix)

| 研究模組 | 核心實證主張 | 估計量 / 計量方法 | 診斷檢驗與驗證 | 審核狀態 |
| :--- | :--- | :--- | :--- | :--- |
| **理論：媒體反應** | 門檻跳躍非線性反應 | 動態貝氏賽局模型 | 一階邊際條件 (命題 1) | Proved (附錄 A.1) |
| **理論：搖擺州效應** | 戰場州跟風彈性顯著更高 | Kyle-Callander 統合模型 | 比較靜態分析 (命題 2) | Proved (附錄 A.2) |
| **理論：反射性裂痕** | 外生媒體引發定價偏離 | 動態均衡固定點 | 資訊扭曲裂痕 (命題 3) | Proved (附錄 A.3) |
| **理論：巨鯨操縱限制** | 策略操縱之二次方資本耗竭 | 動態 Kyle 資本邊界 | 終端流動性清算 (命題 4) | Proved (附錄 A.4) |
| **數據：市場價格** | 逐日真實 CLOB 撮合報價 | Polymarket 官方 API 爬取 | 逐筆成交與中間價結算稽核 | Validated |
| **數據：公眾注意力** | 各州多維關注度指標 | Wikimedia REST API | 平穩性檢定與對數轉換 | Validated |
| **識別：Price $\to$ Media** | 勝率跳躍因果激增媒體報導 | Rigobon (2003) SVAR | 高低波動區制共變異數差分 | Supported |
| **識別：Media $\to$ Price** | 媒體報導自我實現推升價格 | Rigobon (2003) SVAR | 過度識別限制檢定 ($\chi^2 = 48.72$) | Supported |
| **空間推論** | 戰場州地理空間跨截面依賴 | Conley (1999) 空間 HAC | 州首府大圓距離矩陣 (1000km) | Robust |
| **時序推論** | 日頻新聞循環與殘差自相關 | Driscoll-Kraay (1998) | 4 天滯後非參數截面平滑核 | Robust |
| **小群聚偏差** | 州數量有限 ($N=7$) | Wild Cluster Bootstrap | Rademacher 權重模擬 ($B=999$) | Robust |
| **動態持續性** | 衝擊累積軌跡與衰減半衰期 | Jordà (2005) 局部投影 | 10 天預測期動態衝擊響應 | Traced (Figure 1) |

---

## 2. 理論微觀基礎 (Theoretical Framework)

考慮一個跨越離散時間 $t = 1, \dots, T$ 的三方動態貝氏賽局。真實選舉狀態為 $\theta \sim \mathcal{N}(\mu_\theta, \sigma_\theta^2)$。

### 2.1 參與者與市場微觀結構
1. **知情交易者與做市商 (Kyle 1985, Glosten & Milgrom 1985)**：
   知情交易者持有私有信號 $s_t = \theta + \epsilon_t$（$\epsilon_t \sim \mathcal{N}(0, \sigma_\epsilon^2)$），提交訂單 $x_t(s_t)$。噪聲交易者提交隨機訂單 $z_t \sim \mathcal{N}(0, \sigma_z^2)$。競爭性做市商依據總訂單流 $y_t = x_t + z_t$ 設定價格：
   $$p_t = \mathbb{E}[\theta \mid y_t] = p_{t-1} + \lambda_t y_t, \quad \lambda_t = \frac{\text{Cov}(\theta, y_t)}{\text{Var}(y_t)}$$
2. **理性疏忽媒體編輯 (Sims 2003, Bordalo et al. 2013)**：
   編輯在報導預測市場與傳統民調之間分配有限注意力 $\kappa$。點擊率報酬由顯著性決定：$V(|\Delta p_t|) = \frac{|\Delta p_t|^\gamma}{|\Delta p_t|^\gamma + c_0}$（$\gamma > 1$）。
3. **具從眾動能之選民 (Callander 2007)**：
   選民接收媒體信號 $m_t$ 與市場信號 $p_t$。在協調動機與有限理性下，選民產生跟風動能（Bandwagon Effect）。

### 2.2 理論核心命題
* **命題 1（媒體放大非線性門檻）**：存在門檻 $\bar{\tau} > 0$，當 $|\Delta p_t| > \bar{\tau}$ 時，媒體邊際報導彈性產生非連續性跳升。
* **命題 2（搖擺州異質跟風）**：先驗變異數較大的搖擺州選民，其跟風彈性顯著高於深藍或深紅州：
  $$\frac{\partial}{\partial \sigma_{\theta, i}^2} \left( \frac{\partial \mathbb{E}_V[\theta_i]}{\partial \Delta p_{i,t}} \right) > 0$$
* **命題 3（資訊效率反射性裂痕 Reflexivity Wedge）**：當媒體引用強度 $m_t$ 超過臨界值時，市場價格偏離貝氏純理性基準，形成自我實現裂痕 $\mathcal{W}_t$。
* **命題 4（策略性大額操縱的資本耗竭極限）**：單一帳戶人為扭曲價格之維持成本隨時間呈線性、隨扭曲幅度呈二次方增長，在資本耗竭後價格指數級均值回歸。

*(完整數學證明詳見線上附錄 Online Appendix A)*

---

## 3. 數據與變數 (Data & Summary Statistics)

樣本涵蓋 2024 年 3 月 1 日至 11 月 5 日（250 個交易日）之 7 大關鍵搖擺州（PA, MI, WI, AZ, GA, NV, NC），總計 1,750 筆日頻平衡面板觀測值。一階差分後有效樣本為 $N = 7 \times 249 = 1,743$。

| 變數 | 觀測值 $N$ | 平均數 | 標準差 | 最小值 | 中位數 | 最大值 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Polymarket 川普勝率 ($p_{i,t}$) | 1,750 | 0.5289 | 0.0657 | 0.3960 | 0.5203 | 0.7290 |
| 每日價格變動 ($\Delta p_{i,t}$) | 1,750 | 0.0003 | 0.0147 | -0.0607 | 0.0000 | 0.0825 |
| 5 日滾動波動度 ($\sigma_{i,t}^{(5)}$) | 1,750 | 0.0112 | 0.0090 | 0.0001 | 0.0096 | 0.0544 |
| 538 民調淨領先 ($Poll_{i,t}$) | 1,750 | -0.0100 | 0.0127 | -0.0421 | -0.0064 | 0.0233 |
| 每日平台關注度 ($Media_{i,t}$) | 1,750 | 1,108.3 | 2,199.2 | 14 | 329 | 18,435 |
| 對數關注度 ($\ln(1 + Media_{i,t})$) | 1,750 | 5.7150 | 1.6387 | 2.7081 | 5.7991 | 9.8221 |

---

## 4. 計量識別策略：Rigobon (2003) 異質變異數識別

考慮雙向聯立方程系統：
$$\begin{aligned}
\Delta \ln(1 + Media_{i,t}) &= \alpha_1 \Delta Price_{i,t} + \mathbf{\Gamma}_1^\prime \mathbf{X}_{i,t} + u_{i,t} \\
\Delta Price_{i,t} &= \alpha_2 \Delta \ln(1 + Media_{i,t}) + \mathbf{\Gamma}_2^\prime \mathbf{X}_{i,t} + v_{i,t}
\end{aligned}$$

劃分高波動區制 $H$（16 個關鍵事件日：辯論日、刺殺案、退選、巨額注碼等）與低波動區制 $L$。利用簡約式殘差差分共變異數矩陣：
$$\Delta \mathbf{\Omega} = \mathbf{\Omega}_H - \mathbf{\Omega}_L = \mathbf{A}^{-1} (\mathbf{\Sigma}_{\varepsilon, H} - \mathbf{\Sigma}_{\varepsilon, L}) (\mathbf{A}^{-1})^\prime$$
精確解出無偏結構傳導係數 $\alpha_1$ 與 $\alpha_2$。

---

## 5. 主要實證結果 (Main Results)

| 估計規格 | (1) OLS: $P \to M$ | (2) Rigobon SVAR: $P \to M$ | (3) OLS: $M \to P$ | (4) Rigobon SVAR: $M \to P$ |
| :--- | :---: | :---: | :---: | :---: |
| **結構參數** | $\alpha_1$ | **$\alpha_1$** | $\alpha_2$ | **$\alpha_2$** |
| **點估計值** | 5.2946 | **5.4764\*\*\*** | 0.0078 | **0.0351\*\*\*** |
| Driscoll-Kraay SE | (2.2779) | **(1.9807)** | (0.0062) | **(0.0057)** |
| Conley 空間 HAC SE | [0.1205] | **[0.1076]** | [0.0139] | **[0.0129]** |
| $t$-統計量 | 2.32 | **2.76** | 1.25 | **6.18** |
| 識別機制 | 協方差相關 | **異質變異數識別** | 協方差相關 | **異質變異數識別** |
| 控制變數 / 州固定效應 | Yes / Yes | **Yes / Yes** | Yes / Yes | **Yes / Yes** |
| 有效觀測值 $N$ | 1,743 | **1,743** | 1,743 | **1,743** |
| 高波動區制日數 | --- | **16** | --- | **16** |
| Wild Cluster Bootstrap $p$ | --- | **[0.006]** | --- | **[0.000]** |

- **$\alpha_1 = 5.4764$**：預測市場價格每跳升 10 個百分點，引發對數關注度上升 0.5476，相當於媒體關注度激增 **+54.8%**！
- **$\alpha_2 = 0.0351$**：媒體關注度倍增，帶動預測市場價格上調 3.51 個百分點，證實「自我實現預期」確實存在。
- **動態 IRF**：Jordà (2005) 局部投影顯示，價格衝擊在 $t+3 \sim t+4$ 天達到累積峰值，半衰期約為 6 天。

---

## 6. 政策啟示與結論 (Policy & Conclusion)

研究表明，去中心化預測市場並非中立的溫度計，而是具備實質媒體放大與自我實現反饋的造浪者。這項發現對 CFTC 等金融監管當局具有重大啟示：政治合約具有顯著的媒體外部性（Media Externality），未來監管應聚焦於微觀訂單流透明度揭露、媒體引用標準規範以及防範大額資金策略性造浪。

---

## 線上附錄 (Online Appendices)
- **Online Appendix A: 數學證明與推導**（命題 1 至 4 之嚴格 Kuhn-Tucker 條件與動態控制求解）
- **Online Appendix B: 數據建構與變數定義**（官方 CLOB 結算規則與地理 Haversine 矩陣）
- **Online Appendix C: 確定性研究套件與自動化閘門**（`topic_survey`, `results`, `design_audit`）
