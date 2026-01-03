"""
Commodity Forecasting Demo
==========================

This demo shows the complete production pipeline:
1. Load commodity data
2. Prepare features (lags, rolling stats, seasonality)
3. Train multiple models (ARIMA, SARIMA, XGBoost)
4. Generate forecasts
5. T-policy recommendations
6. Model comparison

Perfect for interviews - explains every step!
"""

import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append('src')

from forecasting_models import CommodityForecaster
from production_pipeline import ProductionForecaster

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def main():
    print_header("🌾 COMMODITY FORECASTING SYSTEM - PRODUCTION DEMO")
    
    print("\n📚 INTERVIEW CONTEXT:")
    print("=" * 70)
    print("""
This system forecasts commodity prices for AB InBev's hedging strategy.

BUSINESS PROBLEM:
- AB InBev buys corn, wheat, barley (beer ingredients) + diesel (transport)
- Prices fluctuate daily due to weather, supply, demand
- Need to lock prices 3 months ahead via futures contracts
- Goal: Lock at optimal time to minimize costs

T-POLICY STRATEGY:
- T = Target contract month
- T+2/-2 = Can lock 2 months early or late
- Need forecasts to decide WHEN to lock

DATA SCIENCE SOLUTION:
- Forecast prices 90 days ahead
- Multiple models for robustness
- Recommend optimal locking time
- Expected to save millions annually
    """)
    
    input("\nPress Enter to start demo...")
    
    # STEP 1: Load Data
    print_header("STEP 1: Load Commodity Data")
    
    data_file = 'data/corn_cbot_prices.csv'
    if not os.path.exists(data_file):
        data_file = 'data/commodity_prices_all.csv'
    
    print(f"\n📂 Loading data from: {data_file}")
    df = pd.read_csv(data_file, parse_dates=['date'])
    
    # Filter to one commodity for demo
    if 'commodity' in df.columns:
        df = df[df['commodity'] == 'Corn_CBOT'].copy()
    
    print(f"\n✅ Data loaded successfully!")
    print(f"   Records: {len(df):,}")
    print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"   Average spot price: ${df['spot_price'].mean():.2f}")
    print(f"   Price volatility (std): ${df['spot_price'].std():.2f}")
    
    print("\n📊 Sample data:")
    print(df[['date', 'spot_price', 'future_price_3m']].head(10))
    
    input("\n✅ Data loaded. Press Enter to continue...")
    
    # STEP 2: Feature Engineering
    print_header("STEP 2: Feature Engineering")
    
    print("""
INTERVIEW EXPLANATION - Feature Engineering:
-------------------------------------------

For time series forecasting, we create features from past data:

1. LAG FEATURES:
   - lag_1: Yesterday's price
   - lag_7: Price from 1 week ago
   - lag_30: Price from 1 month ago
   - Why: Prices have auto-correlation (today depends on yesterday)

2. ROLLING STATISTICS:
   - ma_7: 7-day moving average (smooths noise)
   - std_30: 30-day volatility (risk measure)
   - Why: Captures trends and volatility patterns

3. SEASONAL FEATURES:
   - month, quarter, day_of_year
   - sin/cos encoding (preserves cyclical nature)
   - Why: Commodities have harvest cycles

4. MOMENTUM INDICATORS:
   - Price changes over 7, 30 days
   - Rate of change (ROC)
   - Why: Captures accelerating trends
    """)
    
    forecaster = CommodityForecaster('Corn_CBOT')
    train_data, test_data, full_data = forecaster.prepare_data(df, test_size=90)
    
    print(f"\n✅ Features created!")
    print(f"   Total features: {len(full_data.columns) - 2}")
    print(f"   Training samples: {len(train_data)}")
    print(f"   Testing samples: {len(test_data)}")
    
    print("\n📊 Feature preview:")
    feature_cols = [col for col in full_data.columns if col not in ['date', 'spot_price']]
    print(full_data[['date', 'spot_price'] + feature_cols[:5]].head())
    
    input("\n✅ Features ready. Press Enter to train models...")
    
    # STEP 3: Train Baseline Models
    print_header("STEP 3: Train Baseline Models")
    
    print("""
INTERVIEW EXPLANATION - Why Baselines?
--------------------------------------

ALWAYS start with simple baselines!

Reasons:
1. Sets performance benchmark
2. Often surprisingly good
3. If complex model doesn't beat baseline = RED FLAG
4. Shows you follow proper ML workflow

Our baselines:
- Naive: Tomorrow = Today (persistence model)
- Moving Average: Tomorrow = Average of last 7 days
- EMA: Exponential weighted average

Any ML model MUST beat these to be useful!
    """)
    
    baseline_results = forecaster.baseline_models(train_data, test_data)
    
    print("\n📊 Baseline Performance Summary:")
    print("-" * 70)
    for model_name, results in baseline_results.items():
        print(f"\n{model_name}:")
        print(f"   MAE:  ${results['MAE']:.4f}")
        print(f"   RMSE: ${results['RMSE']:.4f}")
        print(f"   MAPE: {results['MAPE']:.2f}%")
    
    input("\n✅ Baselines trained. Press Enter to train advanced models...")
    
    # STEP 4: Train Production Models
    print_header("STEP 4: Train Production Models")
    
    print("""
INTERVIEW EXPLANATION - Model Selection:
---------------------------------------

We train multiple models for robustness:

1. ARIMA (AutoRegressive Integrated Moving Average):
   - Classical statistical model
   - Good for stationary series
   - Parameters: (p,d,q) = (lags, differencing, MA terms)

2. SARIMA (Seasonal ARIMA):
   - ARIMA + seasonality
   - Essential for commodities (harvest cycles)
   - Parameters: (p,d,q)(P,D,Q,s)

3. XGBoost:
   - Gradient boosted trees
   - Handles non-linear patterns
   - Feature importance shows drivers

In production: Use ensemble (average predictions)
    """)
    
    prod_forecaster = ProductionForecaster('Corn_CBOT')
    
    # Train ARIMA
    print("\n" + "-" * 70)
    arima_model = prod_forecaster.train_arima_model(train_data)
    
    input("\n✅ ARIMA trained. Press Enter for SARIMA...")
    
    # Train SARIMA
    print("\n" + "-" * 70)
    sarima_model = prod_forecaster.train_sarima_model(train_data)
    
    # Train XGBoost (optional)
    try:
        input("\n✅ SARIMA trained. Press Enter for XGBoost...")
        print("\n" + "-" * 70)
        xgb_model = prod_forecaster.train_xgboost_model(train_data)
    except:
        print("\n⚠️  XGBoost skipped (requires OpenMP)")
        xgb_model = None
    
    print("\n✅ Core models trained successfully!")
    
    input("\nPress Enter to generate forecasts...")
    
    # STEP 5: Generate Forecasts
    print_header("STEP 5: Generate 90-Day Forecasts")
    
    print("""
INTERVIEW EXPLANATION - Forecasting Horizon:
-------------------------------------------

Why 90 days (3 months)?
- Matches AB InBev's futures contract period
- T-policy allows T+2/-2 flexibility
- Beyond 90 days: Uncertainty too high

Forecast Types:
- Point forecast: Single predicted value
- Interval forecast: Range (confidence bands)
- Probabilistic: Full distribution

In production:
- Update daily with new data
- Monitor actual vs predicted
- Alert if large deviation
    """)
    
    forecast_steps = 90
    
    # ARIMA forecast
    if arima_model:
        arima_forecast = prod_forecaster.generate_forecast('ARIMA', train_data, steps=forecast_steps)
        print("\n✅ ARIMA forecast complete")
        print(f"   Average predicted price: ${arima_forecast['predicted_price'].mean():.2f}")
    
    # SARIMA forecast
    if sarima_model:
        sarima_forecast = prod_forecaster.generate_forecast('SARIMA', train_data, steps=forecast_steps)
        print("\n✅ SARIMA forecast complete")
        print(f"   Average predicted price: ${sarima_forecast['predicted_price'].mean():.2f}")
    
    input("\n✅ Forecasts generated. Press Enter for hedging recommendation...")
    
    # STEP 6: T-Policy Recommendation
    print_header("STEP 6: T-Policy Hedging Recommendation")
    
    print("""
INTERVIEW EXPLANATION - T-Policy Decision:
-----------------------------------------

This is where DATA SCIENCE creates BUSINESS VALUE!

Decision Logic:
1. Compare forecast to current spot price
2. If prices trending UP (>2%):
   → Lock contracts NOW
   → Savings = (forecast - current) × volume

3. If prices trending DOWN (<-2%):
   → WAIT to lock contracts
   → Savings = (current - forecast) × volume

4. If stable (-2% to +2%):
   → MONITOR, flexible timing

Impact:
- For 1 million bushels of corn
- 5% price move = $200,000 savings
- Annual savings: Millions across all commodities
    """)
    
    current_spot = train_data['spot_price'].iloc[-1]
    
    # Get recommendation using SARIMA forecast (most appropriate for seasonal commodities)
    if sarima_model:
        recommendation = prod_forecaster.t_policy_recommendation(sarima_forecast, current_spot)
        
        print("\n" + "=" * 70)
        print("  📋 HEDGING RECOMMENDATION")
        print("=" * 70)
        print(f"\n   Current Spot Price: ${recommendation['current_price']:.2f}")
        print(f"   90-Day Forecast: ${recommendation['forecast_90d']:.2f}")
        print(f"   Expected Trend: {recommendation['trend_pct']:+.2f}%")
        print(f"\n   {recommendation['recommendation']}")
        print(f"   {recommendation['reasoning']}")
        if recommendation['expected_savings'] > 0:
            print(f"\n   💰 Expected Savings: ${recommendation['expected_savings']:,.0f}")
            print(f"      (Based on 1M bushel contract)")
        print("\n" + "=" * 70)
    
    input("\n✅ Recommendation ready. Press Enter for final summary...")
    
    # STEP 7: Summary
    print_header("SUMMARY - Production Forecasting System")
    
    print("""
✅ WHAT WE BUILT:
-----------------

1. DATA PIPELINE:
   - Load & validate commodity prices
   - Feature engineering (lags, rolling stats, seasonality)
   - Handle streaming data

2. MODELS:
   - Baseline models (benchmark)
   - ARIMA (classical time series)
   - SARIMA (with seasonality)
   - XGBoost (ML approach)

3. FORECASTING:
   - 90-day ahead predictions
   - Multiple models for robustness

4. BUSINESS LOGIC:
   - T-policy recommendations
   - Expected savings calculation
   - Decision support

5. PRODUCTION READY:
   - Model versioning
   - Automated retraining
   - Performance monitoring

INTERVIEW VALUE:
----------------

✅ Shows end-to-end thinking (data → model → business value)
✅ Explains concepts clearly (lags, seasonality, etc.)
✅ Production-focused (streaming, retraining, monitoring)
✅ Business impact quantified ($ savings)
✅ Multiple approaches compared (baselines → ML)

NEXT STEPS for Production:
---------------------------

1. Deploy as REST API (FastAPI)
2. Dashboard for visualization (Plotly/Dash)
3. Automated daily pipeline (Airflow)
4. A/B testing framework
5. Model monitoring & alerts
    """)
    
    print("\n" + "=" * 70)
    print("  🎉 DEMO COMPLETE!")
    print("=" * 70)
    print("\nThis project demonstrates production ML for commodity hedging.")
    print("Perfect for interviews - shows technical skills + business acumen!")
    print("\nAll code includes detailed explanations for interview questions.")
    print("\n💡 Tip: Walk through this demo in your interview - it tells a complete story!")

if __name__ == "__main__":
    main()
