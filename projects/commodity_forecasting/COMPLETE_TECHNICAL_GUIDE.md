# 📚 TIME SERIES FORECASTING: Complete Technical Documentation

## Table of Contents
1. [Project Objectives](#project-objectives)
2. [Data Preprocessing](#data-preprocessing)
3. [Exploratory Data Analysis (EDA)](#exploratory-data-analysis)
4. [Stationarity & Testing](#stationarity-testing)
5. [Model Techniques](#model-techniques)
6. [Univariate vs Multivariate](#univariate-vs-multivariate)
7. [Challenges & Solutions](#challenges-solutions)
8. [Glossary of Terms](#glossary-of-terms)

---

## 🎯 Project Objectives

### Business Objective
**Optimize commodity hedging decisions for AB InBev to minimize procurement costs**

**Specific Goals:**
- Forecast commodity prices 90 days ahead with >85% accuracy
- Provide T-policy recommendations (when to lock futures contracts)
- Quantify expected savings from optimal timing
- Handle streaming data for real-time decisions

### Technical Objectives
1. **Multi-granularity data pipeline**: Hourly → Daily → Monthly → Yearly
2. **Comprehensive EDA**: Understand data structure before modeling
3. **Multiple model approaches**: Statistical (ARIMA, SARIMA) + ML (XGBoost)
4. **Production-ready system**: Automated retraining, monitoring, versioning

### Success Metrics
- **Forecast Accuracy**: MAPE < 5% for 30-day, < 10% for 90-day
- **Business Impact**: $2-5M annual savings per commodity
- **System Reliability**: 99.9% uptime, <100ms inference latency

---

## 📊 Data Preprocessing

### Multi-Granularity Approach

**Why multiple granularities?**
- Different stakeholders need different views (traders want hourly, executives want monthly)
- Some patterns only visible at certain frequencies
- Allows model comparison across time scales

#### 1. Hourly Data (Highest frequency)
```python
# Characteristics:
- 10 years × ~252 trading days × 8 hours = ~20,000 records
- Trading hours: 8 AM - 4 PM
- Captures intraday volatility
- Missing data: Weekends, holidays

# Use cases:
- High-frequency trading strategies
- Intraday volatility modeling
- Real-time price monitoring
```

**Challenges:**
- ❌ Large data volume (storage, computation)
- ❌ Many missing periods (non-trading hours)
- ❌ High noise-to-signal ratio
- ❌ Weekend/holiday handling

**Solutions:**
- ✅ Only store trading hours (reduce 67% of data)
- ✅ Forward-fill for short gaps (<3 hours)
- ✅ Aggregate to daily for modeling
- ✅ Use business day calendar

#### 2. Daily Data (Standard for forecasting)
```python
# Aggregation from hourly:
- Open: First hour (8 AM)
- High: Maximum during day
- Low: Minimum during day
- Close: Last hour (3 PM)
- Volume: Sum of all hours

# OHLC (Open-High-Low-Close) pattern:
- Standard in financial markets
- Captures full daily range
- Enables candlestick charts
```

**Why OHLC matters:**
- Shows daily price range (volatility)
- Open-Close: Daily trend direction
- High-Low: Intraday extremes
- Used in technical analysis

#### 3. Monthly Data (Business reporting)
```python
# Aggregation from daily:
- Month-end price: Last trading day
- Average price: Mean of all days
- Volatility: Standard deviation
- Total volume: Sum

# Use cases:
- Monthly P&L reporting
- Seasonal pattern analysis
- Budget planning
```

#### 4. Yearly Data (Strategic planning)
```python
# Aggregation from monthly:
- Year-end price
- Annual average
- Annual high/low
- Total annual volume

# Use cases:
- Long-term trend analysis
- Annual budgeting
- Strategic contracts
```

### Missing Value Handling

**Common causes in time series:**
1. Market closures (weekends, holidays)
2. System outages
3. Data collection failures
4. Sensor malfunctions

**Methods compared:**

| Method | Formula | When to Use | Pros | Cons |
|--------|---------|-------------|------|------|
| **Forward Fill** | `Y(t) = Y(t-1)` | Prices (persist) | Simple, realistic | Can't handle long gaps |
| **Backward Fill** | `Y(t) = Y(t+1)` | Future planning | Uses known future | Looks into future |
| **Linear Interpolation** | `Y(t) = Y(t-1) + (Y(t+1)-Y(t-1))/2` | Smooth trends | Smooth | Assumes linearity |
| **Mean/Median** | `Y(t) = mean(Y)` | Stable series | Simple | Ignores trend |
| **Seasonal Fill** | `Y(t) = Y(t-365)` | Strong seasonality | Uses pattern | Needs full cycle |

**Our approach: Forward Fill**
- Realistic for commodity prices (don't jump instantly)
- Max gap: 3 days (flag for review if longer)
- Production: Alert if gap > 1 day

---

## 🔍 Exploratory Data Analysis (EDA)

### Why EDA is Critical

**"Look at your data first!" - Every experienced data scientist**

EDA helps you:
1. Understand data structure
2. Identify patterns
3. Detect anomalies
4. Guide model selection
5. Set realistic expectations

### 1. Time Series Decomposition

**Objective: Break series into interpretable components**

#### Formula (Additive Model):
```
Y(t) = T(t) + S(t) + R(t)

Where:
Y(t) = Observed value
T(t) = Trend component
S(t) = Seasonal component
R(t) = Residual (noise)
```

#### Formula (Multiplicative Model):
```
Y(t) = T(t) × S(t) × R(t)

Use when seasonal variation proportional to level
```

#### Components Explained:

**TREND (T):**
- Long-term direction (up/down/flat)
- Driven by: Inflation, demand growth, technology
- For commodities: Often upward (inflation) with cycles
- Interview: "Overall directional movement over time"

**Visualization:**
```
Price
│     Trend →  ╱
│            ╱
│          ╱
│        ╱
└──────────────────→ Time
```

**SEASONALITY (S):**
- Repeating patterns at fixed intervals
- Period: Daily, weekly, monthly, yearly
- For commodities: **HARVEST CYCLES** (most important!)
- Interview: "Predictable patterns due to calendar effects"

**Commodity seasonality example:**
```
Corn Price Pattern (Yearly):

High │    ╱╲        Planting season
     │   ╱  ╲       (high demand)
     │  ╱    ╲
Low  │ ╱      ╲___  Harvest season
     │         ╲    (high supply)
     └──────────────────────────
     Jan  Mar  May  Jul  Sep  Nov
```

**RESIDUALS (R):**
- What's left after removing trend + seasonality
- Should look like **white noise** (random)
- If patterns remain → missing components!
- Interview: "Unexplained variation, should be random"

**How to interpret residuals:**
- ✅ Good: Random scatter around zero
- ❌ Bad: Patterns, autocorrelation, heteroscedasticity

### 2. Stationarity Testing

**What is Stationarity?**

A time series is **stationary** if its statistical properties don't change over time:

1. **Constant mean**: E[Y(t)] = μ (same for all t)
2. **Constant variance**: Var[Y(t)] = σ² (same for all t)  
3. **Constant autocovariance**: Cov[Y(t), Y(t-k)] depends only on k, not t

**Visual examples:**

```
STATIONARY:
Price
│  ~~~~·~·~~~·~~  Mean stays constant
│ ·           ·~   Variance stays constant
│·                
└────────────────→ Time

NON-STATIONARY:
Price
│              ·   Mean increases
│           · ·    Variance increases
│        ··
│    ··
│ ·
└────────────────→ Time
```

**Why stationarity matters:**

❌ **Non-stationary problems:**
- Mean reverts to changing level (unpredictable)
- Variance changes → confidence intervals meaningless
- Spurious correlations (two trending series look related)
- ARIMA models assume stationarity!

✅ **Stationarity benefits:**
- Stable statistical properties
- Reliable predictions
- Valid hypothesis tests
- Better model performance

### ADF Test (Augmented Dickey-Fuller)

**What it tests:**

```
Null Hypothesis (H0): Series has a UNIT ROOT → Non-stationary
Alternative (H1): Series is stationary
```

**Unit Root Explained:**

A unit root means shocks have **permanent effects**:

```python
# Unit root process (random walk):
Y(t) = Y(t-1) + ε(t)

# If ε is a shock, it persists forever!
# Today's shock affects all future values
```

**Mathematics:**
```
Test equation:
ΔY(t) = α + β·t + γ·Y(t-1) + δ₁·ΔY(t-1) + ... + ε(t)

If γ = 0 → Unit root → Non-stationary
```

**Interpretation:**

| p-value | Decision | Meaning |
|---------|----------|---------|
| < 0.01 | Reject H0 (99% confidence) | **Strongly stationary** |
| < 0.05 | Reject H0 (95% confidence) | **Stationary** |
| < 0.10 | Reject H0 (90% confidence) | Possibly stationary |
| > 0.10 | Fail to reject H0 | **Non-stationary** |

**ADF Statistic interpretation:**
- More negative = More stationary
- Compare to critical values (-1%, -5%, -10%)
- If ADF < Critical Value → Stationary

**Example output:**
```
ADF Statistic: -4.123
p-value: 0.001
Critical Values:
  1%: -3.43
  5%: -2.86
  10%: -2.57

Interpretation:
✅ -4.123 < -3.43 → Reject H0
✅ p-value = 0.001 < 0.05 → Stationary
```

### KPSS Test (Kwiatkowski-Phillips-Schmidt-Shin)

**Key difference from ADF:**

```
Null Hypothesis (H0): Series is STATIONARY
Alternative (H1): Series is non-stationary

NOTE: OPPOSITE of ADF!
```

**Why use both ADF and KPSS?**

| ADF Result | KPSS Result | Interpretation |
|------------|-------------|----------------|
| Stationary | Stationary | ✅ **Definitely stationary** |
| Non-stat | Non-stat | ❌ **Definitely non-stationary** |
| Stationary | Non-stat | 🤔 **Trend-stationary (differencing may not help)** |
| Non-stat | Stationary | 🤔 **Near unit root (borderline case)** |

**Interpretation table:**

| p-value | Decision | Meaning |
|---------|----------|---------|
| > 0.10 | Fail to reject H0 | **Stationary** |
| 0.05-0.10 | Borderline | Possibly stationary |
| < 0.05 | Reject H0 | **Non-stationary** |

**Example:**
```
KPSS Statistic: 0.123
p-value: 0.08
Critical Values:
  1%: 0.739
  5%: 0.463
  10%: 0.347

Interpretation:
✅ 0.123 < 0.347 → Stationary
✅ p-value = 0.08 > 0.05 → Fail to reject H0 → Stationary
```

### PP Test (Phillips-Perron)

**Similar to ADF but:**
- More robust to heteroskedasticity
- More robust to autocorrelation
- Uses non-parametric methods

**When to use:**
- Volatility clustering (GARCH effects)
- Structural breaks
- ADF gives ambiguous results

### How to Achieve Stationarity

If tests show non-stationarity, try:

#### 1. Differencing
```python
# First difference:
ΔY(t) = Y(t) - Y(t-1)

# Second difference (if needed):
Δ²Y(t) = ΔY(t) - ΔY(t-1)
```

**Effect:**
- Removes trend
- Makes mean constant
- This is the "I" (Integrated) in ARIMA!

#### 2. Log Transform
```python
Y'(t) = log(Y(t))
```

**Effect:**
- Stabilizes variance
- Converts multiplicative to additive
- Makes % changes constant

#### 3. Detrending
```python
# Remove linear trend:
Y'(t) = Y(t) - (a + b·t)

Where a, b from linear regression
```

---

## 📈 Moving Averages Analysis

### Simple Moving Average (SMA)

**Formula:**
```
MA(t, n) = [Y(t) + Y(t-1) + ... + Y(t-n+1)] / n
```

**Example (3-day MA):**
```
Day:   1    2    3    4    5
Price: 4.0  4.2  4.1  4.3  4.5
MA3:   -    -   4.1  4.2  4.3
              ↑
           (4.0+4.2+4.1)/3
```

**Window selection guide:**

| Window | Period | Use Case |
|--------|--------|----------|
| 7 | Week | Short-term trend |
| 30 | Month | Medium-term trend |
| 90 | Quarter | Seasonal pattern |
| 180 | Half-year | Long-term trend |
| 365 | Year | Annual cycle |

**Trading signals:**
- Price > MA → **Uptrend** (bullish)
- Price < MA → **Downtrend** (bearish)
- MA crossovers → **Trend change**

**Golden Cross:**
```
Short MA crosses above Long MA → Strong buy signal

Price
│        Short MA ╱
│              ╱ ╱ Long MA
│           ╱ ╱
│        ╱ ╱
│     ╱ ╱  ← Golden Cross
└────────────────→ Time
```

### Exponential Moving Average (EMA)

**Formula:**
```
EMA(t) = α·Y(t) + (1-α)·EMA(t-1)

Where α = smoothing factor (0 to 1)
```

**Weight decay:**
```
Weight(t-k) = α·(1-α)^k

Example with α = 0.3:
Today:     0.30
Yesterday: 0.21 (= 0.3 × 0.7)
2 days ago: 0.147 (= 0.3 × 0.7²)
3 days ago: 0.103
...
```

**Advantage over SMA:**
- More responsive to recent changes
- Smooth transition (no sudden jumps)
- Used in MACD indicator

---

## 🎯 Model Techniques

### 1. ARIMA Family

#### ARIMA(p,d,q)

**Components:**
- **AR(p)**: AutoRegressive
- **I(d)**: Integrated (Differencing)
- **MA(q)**: Moving Average

**Full equation:**
```
φ(B)·(1-B)^d·Y(t) = θ(B)·ε(t)

Where:
φ(B) = AR polynomial
θ(B) = MA polynomial
B = Backshift operator
ε(t) = White noise
```

**Expanded form:**
```
Y(t) = c + φ₁·Y(t-1) + φ₂·Y(t-2) + ... + φₚ·Y(t-p)
       + θ₁·ε(t-1) + θ₂·ε(t-2) + ... + θ_q·ε(t-q)
       + ε(t)
```

**How to choose p, d, q:**

1. **d (Differencing):**
   - Run ADF test
   - If non-stationary: d=1
   - If still non-stationary after 1st diff: d=2
   - Rarely need d>2

2. **p (AR order) - Look at PACF:**
   ```
   PACF cuts off at lag p → AR(p)
   
   Example:
   Lag:  1    2    3    4
   PACF: 0.8  0.4  0.05 0.02
         ↑    ↑    ↑
         Sig  Sig  Not sig → p=2
   ```

3. **q (MA order) - Look at ACF:**
   ```
   ACF cuts off at lag q → MA(q)
   
   Example:
   Lag: 1    2    3    4
   ACF: 0.7  0.3  0.02 0.01
        ↑    ↑    ↑
        Sig  Sig  Not sig → q=2
   ```

#### SARIMA(p,d,q)(P,D,Q,s)

**Adds seasonal component:**

```
SARIMA equation:
φ(B)·Φ(B^s)·(1-B)^d·(1-B^s)^D·Y(t) = θ(B)·Θ(B^s)·ε(t)

Where:
Φ(B^s) = Seasonal AR
Θ(B^s) = Seasonal MA
s = Seasonal period
```

**Seasonal periods:**
- Hourly data, daily pattern: s=24
- Daily data, weekly pattern: s=7
- Daily data, monthly pattern: s=30
- Daily data, yearly pattern: s=365
- Monthly data, yearly pattern: s=12

**Example: SARIMA(1,1,1)(1,1,1,12)**
```
Non-seasonal: (1,1,1)
- 1st order AR
- 1st order differencing
- 1st order MA

Seasonal: (1,1,1,12)
- 1st order seasonal AR
- 1st order seasonal differencing
- 1st order seasonal MA
- Period of 12 months
```

#### SARIMAX

**Adds exogenous variables:**

```
SARIMAX equation:
Y(t) = SARIMA_part + β·X(t) + ε(t)

Where:
X(t) = External variables
β = Coefficients
```

**Example exogenous variables for commodities:**
- Weather: Temperature, rainfall
- Economic: GDP, inflation, unemployment
- Energy: Crude oil price, natural gas
- Demand: Ethanol production, livestock feed demand
- Supply: Planted acres, yield forecasts
- Currency: USD strength (for international commodities)

**Critical requirement:**
❗ **Must have exogenous data for forecast period!**

---

### 2. Exponential Smoothing

#### Simple Exponential Smoothing

**Formula:**
```
ŷ(t+1|t) = α·y(t) + (1-α)·ŷ(t|t-1)
```

**Recursive form:**
```
ŷ(t+1|t) = ŷ(t|t-1) + α·[y(t) - ŷ(t|t-1)]
                        ↑
                   Forecast error
```

**Choosing α:**
- α near 0: Slow adaptation (smooth)
- α near 1: Fast adaptation (responsive)
- Optimize via MSE minimization

#### Holt's Method (Double Exponential)

**Adds trend:**

```
Level:  ℓ(t) = α·y(t) + (1-α)·[ℓ(t-1) + b(t-1)]
Trend:  b(t) = β·[ℓ(t) - ℓ(t-1)] + (1-β)·b(t-1)

Forecast: ŷ(t+h|t) = ℓ(t) + h·b(t)
```

#### Holt-Winters (Triple Exponential)

**Adds seasonality:**

**Additive model:**
```
Level:    ℓ(t) = α·[y(t) - s(t-m)] + (1-α)·[ℓ(t-1) + b(t-1)]
Trend:    b(t) = β·[ℓ(t) - ℓ(t-1)] + (1-β)·b(t-1)
Seasonal: s(t) = γ·[y(t) - ℓ(t)] + (1-γ)·s(t-m)

Forecast: ŷ(t+h|t) = ℓ(t) + h·b(t) + s(t+h-m)
```

**Multiplicative model:**
```
Forecast: ŷ(t+h|t) = [ℓ(t) + h·b(t)]·s(t+h-m)
```

---

### 3. Vector Models (Multivariate)

#### VARMA(p, q)

**Vector AutoRegressive Moving Average for k variables:**

```
Y(t) = c + A₁·Y(t-1) + A₂·Y(t-2) + ... + Aₚ·Y(t-p)
       + M₁·ε(t-1) + M₂·ε(t-2) + ... + M_q·ε(t-q)
       + ε(t)

Where:
Y(t) = [Y₁(t), Y₂(t), ..., Y_k(t)]' (k×1 vector)
A_i = k×k matrices
M_j = k×k matrices
ε(t) = k×1 error vector
```

**Example with k=2 (Corn, Wheat):**

```
Corn(t) = c₁ + a₁₁·Corn(t-1) + a₁₂·Wheat(t-1) + ε₁(t)
Wheat(t) = c₂ + a₂₁·Corn(t-1) + a₂₂·Wheat(t-1) + ε₂(t)

Cross-effects:
a₁₂: How wheat affects corn
a₂₁: How corn affects wheat
```

**Parameter count:**
```
Total parameters = k² × p + k² × q + k

For k=3, p=2, q=1:
= 3² × 2 + 3² × 1 + 3
= 18 + 9 + 3
= 30 parameters!
```

#### VARMAX

**Adds exogenous variables:**

```
Y(t) = c + A₁·Y(t-1) + ... + Aₚ·Y(t-p)
       + M₁·ε(t-1) + ... + M_q·ε(t-q)
       + B·X(t)  ← Exogenous
       + ε(t)
```

---

## 🔄 Univariate vs Multivariate

### Univariate Analysis

**Definition:** Model one variable using its own history

**Advantages:**
✅ Simpler to understand
✅ Fewer parameters
✅ Less data needed
✅ Faster to train
✅ Easier to interpret

**Disadvantages:**
❌ Ignores relationships with other variables
❌ May miss important drivers
❌ Separate model for each variable

**When to use:**
- One primary variable of interest
- Variables truly independent
- Limited data
- Need interpretability

**Models:**
- ARIMA, SARIMA, SARIMAX
- Exponential Smoothing
- Single-variable XGBoost

### Multivariate Analysis

**Definition:** Model multiple variables jointly

**Advantages:**
✅ Captures cross-variable dynamics
✅ One model for all variables
✅ Better when variables related
✅ Granger causality testing

**Disadvantages:**
❌ Complex
❌ Many parameters
❌ Needs more data
❌ Curse of dimensionality
❌ Harder to interpret

**When to use:**
- Variables influence each other
- Need joint forecasts
- Sufficient data
- System dynamics important

**Models:**
- VARMA, VARMAX
- Dynamic Factor Models
- Multivariate XGBoost

---

## ⚠️ Challenges & Solutions

### Challenge 1: Non-Stationarity

**Problem:**
```
Prices trend upward → Mean not constant → ARIMA fails
```

**Solutions:**
1. **Differencing:**
   ```python
   Y'(t) = Y(t) - Y(t-1)  # 1st difference
   ```

2. **Log transform:**
   ```python
   Y'(t) = log(Y(t))
   ```

3. **Detrending:**
   ```python
   Y'(t) = Y(t) - trend(t)
   ```

### Challenge 2: Seasonality

**Problem:**
```
Harvest cycles create strong patterns → ARIMA not enough
```

**Solutions:**
1. **Use SARIMA:**
   ```python
   SARIMA(1,1,1)(1,1,1,365)  # Yearly seasonality
   ```

2. **Seasonal differencing:**
   ```python
   Y'(t) = Y(t) - Y(t-365)
   ```

3. **Dummy variables:**
   ```python
   month_1, month_2, ..., month_12
   ```

### Challenge 3: Multiple Time Granularities

**Problem:**
```
Need hourly (trading), daily (analysis), monthly (reports)
```

**Solutions:**
1. **Hierarchical forecasting:**
   ```
   - Forecast daily
   - Disaggregate to hourly
   - Aggregate to monthly
   ```

2. **Store all granularities:**
   ```
   - Raw: Hourly
   - Modeling: Daily
   - Reporting: Monthly
   ```

### Challenge 4: Missing Data

**Problem:**
```
Holidays, weekends, system outages → Gaps in data
```

**Solutions:**
1. **Forward fill (our choice):**
   ```python
   df.fillna(method='ffill')
   ```

2. **Seasonal fill:**
   ```python
   df[t] = df[t-365]  # Last year same day
   ```

3. **Alert on long gaps:**
   ```python
   if gap > 3 days: send_alert()
   ```

### Challenge 5: Computational Cost

**Problem:**
```
10 years × 5 commodities × hourly = 350K rows
VARMAX with 5 variables × 100 parameters = Slow!
```

**Solutions:**
1. **Downsampling:**
   ```
   Train on daily instead of hourly
   ```

2. **Parallelization:**
   ```python
   joblib.Parallel(n_jobs=-1)
   ```

3. **Model selection:**
   ```
   Use simpler models (ARIMA) first
   Complex models (VARMAX) only if needed
   ```

---

## 📖 Glossary of Terms

### A
**ACF (AutoCorrelation Function):**
Correlation between series and its lagged values.

**ADF (Augmented Dickey-Fuller) Test:**
Statistical test for stationarity.

**AR (AutoRegressive):**
Model where current value depends on past values.

**ARIMA:**
AutoRegressive Integrated Moving Average model.

### D
**Differencing:**
Subtracting previous value to achieve stationarity.

### E
**Endogenous Variable:**
Variable predicted by the model using its own history.

**Exogenous Variable:**
External variable that influences target but isn't predicted.

**Exponential Smoothing:**
Forecasting method that weights recent observations more.

### G
**Granger Causality:**
Statistical test if one time series helps predict another.

### H
**Heteroskedasticity:**
Non-constant variance over time.

**Holt-Winters:**
Triple exponential smoothing with trend and seasonality.

### K
**KPSS Test:**
Stationarity test (null hypothesis: stationary).

### L
**Lag:**
Previous time period (lag 1 = yesterday).

### M
**MA (Moving Average in ARIMA context):**
Model based on past forecast errors.

**MAPE (Mean Absolute Percentage Error):**
Average absolute % error.

### P
**PACF (Partial AutoCorrelation Function):**
Correlation after removing intermediate effects.

### R
**Residuals:**
Difference between actual and predicted values.

### S
**SARIMA:**
Seasonal ARIMA.

**SARIMAX:**
SARIMA with exogenous variables.

**Seasonality:**
Repeating pattern at fixed intervals.

**Stationarity:**
Constant mean, variance, and covariance over time.

### T
**Trend:**
Long-term direction of series.

### U
**Unit Root:**
Series has permanent response to shocks (non-stationary).

### V
**VARMA:**
Vector AutoRegressive Moving Average (multivariate).

**VARMAX:**
VARMA with exogenous variables.

### W
**White Noise:**
Random series with zero mean, constant variance, no autocorrelation.

---

## 🎓 Interview Quick Reference

**Key points to mention:**

1. **Stationarity is critical** - Always test with ADF/KPSS
2. **Decomposition first** - Understand trend, seasonality, residuals
3. **Multiple models** - Compare ARIMA, SARIMA, Exp Smoothing
4. **Production considerations** - Retraining, monitoring, versioning
5. **Business value** - $2-5M savings, not just accuracy metrics
6. **Challenges handled** - Missing data, non-stationarity, seasonality

**Be ready to explain:**
- What is stationarity and why it matters
- Difference between AR and MA
- How to read ACF/PACF plots
- When to use multivariate vs univariate
- How to choose ARIMA parameters
- T-policy business logic

---

*This documentation is comprehensive and interview-ready!* 🚀
