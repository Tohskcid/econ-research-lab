# Estimation Recipes and Publication Output

Read this reference when generating, reviewing, or debugging econometric estimation code. Do not let code availability dictate the research design; apply these recipes only after selecting the design in [method_router.md](method_router.md).

## Language and Environment Detection

Before issuing code:
1. Inspect available tools: Stata (`stata -b`), R (`Rscript`), Python (`python3`), or Julia (`julia`).
2. Adapt syntax to the available environment; never output syntax for an uninstalled interpreter without user approval.
3. Lock package versions and random seeds (`set.seed()`, `set seed`, `numpy.random.seed()`).

---

## 1. Staggered Difference-in-Differences & Dynamic Effects

Never use classic Two-Way Fixed Effects (TWFE) with staggered adoption without verifying that negative weighting is negligible (e.g., via Goodman-Bacon decomposition `bacondecomp`). Prefer heterogeneity-robust estimators:

### Callaway & Sant'Anna (2021)
- **Stata**:
  ```stata
  * Install: ssc install csdid, replace
  csdid outcome controls, ivar(id) time(year) gvar(first_treat_year) method(drimp) vce(cluster id)
  estat event, estore(cs_event)
  csdid_plot, title("CS Event Study")
  ```
- **R (`did` & `fixest`)**:
  ```r
  library(did)
  out <- att_gt(
    yname = "outcome", tname = "year", idname = "id", gname = "first_treat_year",
    xformla = ~ x1 + x2, data = df, control_group = "nevertreated",
    panel = TRUE, allow_unbalanced_panel = TRUE
  )
  es <- aggte(out, type = "dynamic")
  ggdid(es)
  ```
- **Python (`pyfixest` or `csdid`)**:
  ```python
  import pyfixest as pf
  # Or use dedicated csdid Python binding
  fit = pf.feols("outcome ~ i(year, treated, ref=base_year) | id + year", data=df, vcov={"CRV1": "id"})
  ```

### Sun & Abraham (2021) / Interaction-Weighted
- **Stata**: `eventstudyinteract outcome controls, cohorts(first_treat_year) control_cohort(never_treat) vce(cluster id)`
- **R (`fixest::sunab`)**:
  ```r
  library(fixest)
  feols(outcome ~ sunab(first_treat_year, year) + x1 | id + year, data = df, cluster = ~id)
  ```

### Borusyak, Jaravel & Spiess (2024) Imputation
- **Stata**: `did_imputation outcome id year first_treat_year, autosample horizons(0/5) pretrends(5)`
- **R (`didimputation`)**: `did_imputation(data = df, yname = "outcome", gname = "first_treat_year", tname = "year", idname = "id", horizons = 0:5, pretrends = TRUE)`

---

## 2. Regression Discontinuity Designs (RDD)

Never report polynomial orders greater than 2 without explicit justification. Always use robust bias-corrected confidence intervals (Calonico, Cattaneo, and Titiunik 2014).

- **Stata**:
  ```stata
  * Install: net install rdrobust, from(https://raw.githubusercontent.com/rdpackages/rdrobust/master/stata) replace
  * Density manipulation check (Cattaneo, Jansson, and Ma 2020)
  rddensity running_var, c(0)
  * Robust bias-corrected local polynomial RDD
  rdrobust outcome running_var, c(0) p(1) q(2) kernel(triangular) bwselect(mserd) vce(cluster cluster_id)
  rdplot outcome running_var, c(0) p(1) kernel(triangular)
  ```
- **R (`rdrobust`, `rddensity`)**:
  ```r
  library(rdrobust)
  library(rddensity)
  # Manipulation test
  dens_test <- rddensity(df$running_var, c = 0)
  summary(dens_test)
  # Local linear estimation
  rd_est <- rdrobust(y = df$outcome, x = df$running_var, c = 0, p = 1, kernel = "triangular", cluster = df$cluster_id)
  summary(rd_est)
  rdplot(y = df$outcome, x = df$running_var, c = 0)
  ```

---

## 3. Instrumental Variables (IV) & Weak Identification

A first-stage $F > 10$ is insufficient under non-homoskedastic errors or multiple instruments. Report Montiel Olea & Pflueger (2013) effective $F$-statistic and Anderson-Rubin confidence sets.

- **Stata**:
  ```stata
  * Install: ssc install ivreg2; ssc install weakivtest; ssc install weakiv
  ivreg2 outcome controls (treatment = instrument), cluster(cluster_id)
  * Effective F-test for weak instruments (tolerance: 10% worst-case bias)
  weakivtest
  * Weak-instrument-robust Anderson-Rubin confidence set
  weakiv
  ```
- **R (`fixest`)**:
  ```r
  library(fixest)
  iv_model <- feols(outcome ~ controls | id + year | treatment ~ instrument, data = df, cluster = ~cluster_id)
  summary(iv_model, stage = 1:2)
  # Report Wald test of first stage and Anderson-Rubin bounds
  fitstat(iv_model, type = c("ivf", "wh", "sargan"))
  ```

---

## 4. Spatial HAC & Conley Standard Errors

When unobserved shocks are geographically or serially dependent, standard cluster SEs fail if clusters are continuous across space.

- **Stata**:
  ```stata
  * Install: ssc install conleyreg
  conleyreg outcome treatment controls, lat(latitude) lon(longitude) distcutoff(100) lagcutoff(5)
  ```
- **R (`fixest`)**:
  ```r
  feols(outcome ~ treatment + controls, data = df, vcov = conley(cutoff = 100, distance = "spherical", lat = "lat", lon = "lon"))
  ```

---

## 5. Double Machine Learning (Chernozhukov et al. 2018)

Use Neyman orthogonal scores and honest sample splitting ($K$-fold cross-fitting) when adjusting for high-dimensional confounders.

- **Python (`DoubleML`)**:
  ```python
  import doubleml as dml
  from sklearn.ensemble import RandomForestRegressor
  data_dml = dml.DoubleMLData(df, y_col='outcome', d_cols='treatment', x_cols=['x1', 'x2', 'x3'])
  ml_l = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
  ml_m = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
  dml_plr = dml.DoubleMLPLR(data_dml, ml_l, ml_m, n_folds=5)
  dml_plr.fit()
  print(dml_plr.summary)
  ```

---

## 6. Publication-Ready Table Guidelines

Produce clean, self-contained LaTeX tables conforming to AER/QJE standards:
1. Use `booktabs` (`\toprule`, `\midrule`, `\bottomrule`); no vertical lines.
2. Parentheses under coefficients denote standard errors (never $t$-stats or $p$-values).
3. Always annotate:
   - Clustering level: `Standard errors clustered at the [unit] level in parentheses`.
   - Significance levels: `* p < 0.10, ** p < 0.05, *** p < 0.01`.
   - Dependent variable mean and standard deviation.
   - Observation counts and $R^2$ / pseudo-$R^2$ / effective $F$-statistic.
   - Indicator rows for Fixed Effects (`Unit FE: Yes/No`, `Time FE: Yes/No`).
4. Automated export:
   - Stata: `esttab using "output/tables/table1.tex", replace booktabs label se star(* 0.10 ** 0.05 *** 0.01) stats(N r2 F, labels("Observations" "$R^2$" "Effective F"))`
   - R: `modelsummary::modelsummary(models, output = "output/tables/table1.tex", stars = TRUE, gof_map = c("nobs", "r.squared"))`
