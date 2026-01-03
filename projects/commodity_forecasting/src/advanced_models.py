"""
Advanced Time Series Models
============================

This module implements:
1. SARIMAX (SARIMA with eXogenous variables)
2. Exponential Smoothing (Holt-Winters)
3. VARMA (Vector AutoRegressive Moving Average - Multivariate)
4. VARMAX (VARMA with eXogenous variables)

Both UNIVARIATE and MULTIVARIATE approaches
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.varmax import VARMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

class AdvancedTimeSeriesModels:
    """
    Advanced models for both univariate and multivariate time series
    
    Interview Explanation:
    ----------------------
    Progression of complexity:
    
    UNIVARIATE (Single variable):
    1. ARIMA → Basic
    2. SARIMA → Adds seasonality
    3. SARIMAX → Adds external variables
    4. Exp Smoothing → Alternative approach
    
    MULTIVARIATE (Multiple variables):
    1. VARMA → Multiple series together
    2. VARMAX → VARMA + external variables
    
    Why multivariate?
    - Corn price affects wheat price
    - Diesel price affects all commodity transport costs
    - Capture cross-variable relationships!
    """
    
    def __init__(self):
        self.models = {}
        self.predictions = {}
        self.performance = {}
        
        print("🚀 Advanced Time Series Models initialized")
    
    def train_sarimax(self, train_data, exog_train=None, order=(1,1,1), seasonal_order=(1,1,1,12)):
        """
        Train SARIMAX model
        
        Interview Explanation:
        ----------------------
        SARIMAX = SARIMA + eXogenous variables
        
        What are exogenous variables?
        - External factors that influence target
        - Not predicted by the model
        - Examples for commodities:
          * Weather data (temperature, rainfall)
          * Economic indicators (GDP, inflation)
          * Energy prices (crude oil for diesel)
          * Currency exchange rates (for international commodities)
        
        Model: SARIMAX(p,d,q)(P,D,Q,s)
        
        Non-seasonal: (p,d,q)
        - p: AR order
        - d: Differencing order
        - q: MA order
        
        Seasonal: (P,D,Q,s)
        - P: Seasonal AR
        - D: Seasonal differencing
        - Q: Seasonal MA
        - s: Seasonal period (12 for monthly, 365 for daily)
        
        Exogenous (X):
        - Additional predictors
        - Must be known for forecast period!
        
        When to use SARIMAX?
        ✅ Have external data that influences target
        ✅ External data available for forecast period
        ✅ Relationship between external → target is stable
        
        Interview: "SARIMAX lets us incorporate weather forecasts, economic indicators,
                   or related commodity prices as features."
        """
        
        print("\n📈 Training SARIMAX Model...")
        print(f"   Order (p,d,q): {order}")
        print(f"   Seasonal Order (P,D,Q,s): {seasonal_order}")
        
        if exog_train is not None:
            print(f"   Exogenous variables: {exog_train.shape[1]}")
            print(f"   Features: {list(exog_train.columns)}")
        else:
            print("   No exogenous variables (same as SARIMA)")
        
        # Fit model
        model = SARIMAX(
            train_data,
            exog=exog_train,
            order=order,
            seasonal_order=seasonal_order,
            enforce_stationarity=False,
            enforce_invertibility=False
        )
        
        fitted_model = model.fit(disp=False, maxiter=200)
        
        print(f"\n   ✅ Model fitted!")
        print(f"   AIC: {fitted_model.aic:.2f}")
        print(f"   BIC: {fitted_model.bic:.2f}")
        
        # Model summary
        print(f"\n   📊 Coefficient Summary:")
        print(f"   {fitted_model.summary().tables[1]}")
        
        self.models['SARIMAX'] = fitted_model
        
        return fitted_model
    
    def train_exponential_smoothing(self, train_data, seasonal_periods=12, trend='add', seasonal='add'):
        """
        Train Exponential Smoothing (Holt-Winters) model
        
        Interview Explanation:
        ----------------------
        EXPONENTIAL SMOOTHING - Alternative to ARIMA!
        
        Why "exponential"?
        - Recent observations weighted MORE than old ones
        - Weights decay exponentially: α, α(1-α), α(1-α)², ...
        
        THREE TYPES:
        
        1. SIMPLE EXPONENTIAL SMOOTHING:
           - No trend, no seasonality
           - Just smoothed level
           - Formula: ŷ(t+1) = α·y(t) + (1-α)·ŷ(t)
        
        2. HOLT'S METHOD (Double Exponential):
           - Adds trend
           - Level + Trend
           - Good for trending data
        
        3. HOLT-WINTERS (Triple Exponential):
           - Adds seasonality
           - Level + Trend + Seasonal
           - Perfect for commodities!
        
        Components:
        - Level (ℓ): Smoothed average
        - Trend (b): Rate of change
        - Seasonal (s): Repeating pattern
        
        Additive vs Multiplicative:
        
        ADDITIVE (trend='add', seasonal='add'):
        - Seasonal variation constant
        - Y(t) = Level + Trend + Seasonal
        - Use when: Range of seasonality doesn't change
        
        MULTIPLICATIVE (trend='mul', seasonal='mul'):
        - Seasonal variation proportional to level
        - Y(t) = Level × Trend × Seasonal
        - Use when: Seasonality grows with price level
        
        Advantages over ARIMA:
        ✅ Simpler to understand
        ✅ No stationarity required
        ✅ Automatic parameter estimation
        ✅ Fast to train
        
        Disadvantages:
        ❌ No statistical tests
        ❌ Less flexible than ARIMA
        ❌ Can't incorporate exogenous variables
        
        Interview: "Exponential Smoothing is great when you want simplicity
                   and interpretability. It's often as accurate as ARIMA
                   but much faster to implement."
        """
        
        print("\n📈 Training Exponential Smoothing (Holt-Winters)...")
        print(f"   Trend: {trend}")
        print(f"   Seasonal: {seasonal}")
        print(f"   Seasonal periods: {seasonal_periods}")
        
        model = ExponentialSmoothing(
            train_data,
            trend=trend,
            seasonal=seasonal,
            seasonal_periods=seasonal_periods
        )
        
        fitted_model = model.fit(optimized=True)
        
        print(f"\n   ✅ Model fitted!")
        print(f"   Smoothing Level (α): {fitted_model.params['smoothing_level']:.4f}")
        print(f"   Smoothing Trend (β): {fitted_model.params.get('smoothing_trend', 'N/A')}")
        print(f"   Smoothing Seasonal (γ): {fitted_model.params.get('smoothing_seasonal', 'N/A')}")
        
        print(f"\n   📝 Interpretation:")
        print(f"   α = {fitted_model.params['smoothing_level']:.4f}")
        if fitted_model.params['smoothing_level'] > 0.5:
            print(f"      → High α: Recent data weighted heavily (responsive to changes)")
        else:
            print(f"      → Low α: Smooth, less reactive to recent changes")
        
        self.models['Exponential_Smoothing'] = fitted_model
        
        return fitted_model
    
    def train_varma_multivariate(self, train_data_multi, order=(1,1)):
        """
        Train VARMA for multivariate time series
        
        Interview Explanation:
        ----------------------
        VARMA = Vector AutoRegressive Moving Average
        
        Multivariate vs Univariate:
        
        UNIVARIATE (ARIMA):
        - One variable predicts itself
        - Corn(t) = f(Corn(t-1), Corn(t-2), ...)
        
        MULTIVARIATE (VARMA):
        - Multiple variables predict each other
        - Corn(t) = f(Corn(t-1), Wheat(t-1), Diesel(t-1), ...)
        - Wheat(t) = f(Wheat(t-1), Corn(t-1), Diesel(t-1), ...)
        
        Why multivariate?
        ✅ Commodities are related (corn → ethanol → oil)
        ✅ Captures cross-variable dynamics
        ✅ Better forecasts when variables influence each other
        ✅ One model for all variables
        
        VARMA(p, q):
        - p: AR order (lags of ALL variables)
        - q: MA order (errors of ALL variables)
        
        Example with 3 variables (Corn, Wheat, Diesel):
        - Each variable has equation with lags of ALL 3
        - 3 equations estimated simultaneously
        - Captures: Corn affects Wheat, Diesel affects both, etc.
        
        Challenges:
        ❌ Many parameters (p × k² where k = # variables)
        ❌ Need long history (curse of dimensionality)
        ❌ All variables must be stationary
        ❌ Computationally expensive
        
        When to use:
        ✅ Variables clearly influence each other
        ✅ Sufficient data (100+ observations per variable)
        ✅ Need joint forecasts of multiple series
        
        Interview: "VARMA is powerful when commodities are interconnected.
                   For example, corn and wheat compete for farmland, so
                   price of one affects the other."
        """
        
        print("\n📈 Training VARMA (Multivariate) Model...")
        print(f"   Variables: {list(train_data_multi.columns)}")
        print(f"   Order (p, q): {order}")
        print(f"   Shape: {train_data_multi.shape}")
        
        # Check stationarity
        print("\n   ⚠️  Note: All variables must be stationary for VARMA!")
        
        model = VARMAX(
            train_data_multi,
            order=order,
            enforce_stationarity=False
        )
        
        fitted_model = model.fit(disp=False, maxiter=200)
        
        print(f"\n   ✅ Model fitted!")
        print(f"   AIC: {fitted_model.aic:.2f}")
        print(f"   BIC: {fitted_model.bic:.2f}")
        print(f"   Log Likelihood: {fitted_model.llf:.2f}")
        
        # Show Granger causality interpretation
        print(f"\n   📊 Cross-Variable Effects:")
        print(f"   (Check if Variable A 'Granger-causes' Variable B)")
        print(f"   → Coefficients show influence between variables")
        
        self.models['VARMA'] = fitted_model
        
        return fitted_model
    
    def train_varmax_multivariate(self, train_data_multi, exog_train=None, order=(1,1)):
        """
        Train VARMAX (VARMA with exogenous variables)
        
        Interview Explanation:
        ----------------------
        VARMAX = VARMA + eXogenous variables
        
        Combines:
        - Multiple endogenous variables (predict each other)
        - External exogenous variables (external drivers)
        
        Example:
        Endogenous: [Corn, Wheat, Diesel]
        Exogenous: [Temperature, Rainfall, Oil_Price, USD_Index]
        
        Model structure:
        - Corn(t) = f(Corn(t-1), Wheat(t-1), Diesel(t-1), Weather, Oil, USD)
        - Wheat(t) = f(Corn(t-1), Wheat(t-1), Diesel(t-1), Weather, Oil, USD)
        - Diesel(t) = f(Corn(t-1), Wheat(t-1), Diesel(t-1), Weather, Oil, USD)
        
        When to use:
        ✅ Multiple related time series
        ✅ External factors affect all series
        ✅ Want joint forecasts
        ✅ Have exogenous data for forecast period
        
        Challenges:
        ❌ VERY many parameters
        ❌ Needs lots of data
        ❌ Exogenous vars must be forecasted separately
        ❌ Can overfit easily
        
        Interview: "VARMAX is the most comprehensive approach - multiple
                   commodities influencing each other, plus external factors
                   like weather and oil prices."
        """
        
        print("\n📈 Training VARMAX (Multivariate + Exogenous) Model...")
        print(f"   Endogenous variables: {list(train_data_multi.columns)}")
        print(f"   Order (p, q): {order}")
        
        if exog_train is not None:
            print(f"   Exogenous variables: {exog_train.shape[1]}")
            print(f"   Features: {list(exog_train.columns)}")
        
        model = VARMAX(
            train_data_multi,
            exog=exog_train,
            order=order,
            enforce_stationarity=False
        )
        
        fitted_model = model.fit(disp=False, maxiter=200)
        
        print(f"\n   ✅ Model fitted!")
        print(f"   AIC: {fitted_model.aic:.2f}")
        print(f"   BIC: {fitted_model.bic:.2f}")
        
        self.models['VARMAX'] = fitted_model
        
        return fitted_model
    
    def forecast(self, model_name, steps=90, exog_forecast=None):
        """
        Generate forecasts from trained model
        
        Interview Explanation:
        ----------------------
        Forecasting challenges:
        
        1. UNIVARIATE (SARIMAX, Exp Smoothing):
           - Just predict target variable
           - Need exogenous data for forecast period
        
        2. MULTIVARIATE (VARMA, VARMAX):
           - Predict ALL variables simultaneously
           - Returns matrix of forecasts
           - Need exogenous data for all forecast steps
        
        Forecast horizon:
        - Short-term (1-7 days): Very accurate
        - Medium-term (30 days): Good
        - Long-term (90 days): Uncertain (use confidence intervals!)
        """
        
        print(f"\n🔮 Generating {steps}-step forecast with {model_name}...")
        
        model = self.models[model_name]
        
        if model_name in ['SARIMAX']:
            forecast = model.forecast(steps=steps, exog=exog_forecast)
        elif model_name in ['Exponential_Smoothing']:
            forecast = model.forecast(steps=steps)
        elif model_name in ['VARMA', 'VARMAX']:
            forecast = model.forecast(steps=steps, exog=exog_forecast)
        else:
            raise ValueError(f"Unknown model: {model_name}")
        
        self.predictions[model_name] = forecast
        
        print(f"   ✅ Forecast complete!")
        
        return forecast
    
    def evaluate(self, model_name, y_true, y_pred=None):
        """
        Evaluate model performance
        """
        
        if y_pred is None:
            y_pred = self.predictions[model_name]
        
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        
        self.performance[model_name] = {
            'MAE': mae,
            'RMSE': rmse,
            'MAPE': mape
        }
        
        print(f"\n📊 {model_name} Performance:")
        print(f"   MAE:  ${mae:.4f}")
        print(f"   RMSE: ${rmse:.4f}")
        print(f"   MAPE: {mape:.2f}%")
        
        return self.performance[model_name]


# Example usage with documentation
if __name__ == "__main__":
    print("=" * 70)
    print("  ADVANCED TIME SERIES MODELS")
    print("=" * 70)
    
    print("""
This module demonstrates:

1. UNIVARIATE MODELS:
   - SARIMAX: SARIMA + external variables
   - Exponential Smoothing: Holt-Winters method

2. MULTIVARIATE MODELS:
   - VARMA: Multiple series together
   - VARMAX: VARMA + external variables

3. KEY CONCEPTS:
   - Exogenous variables
   - Multivariate modeling
   - Cross-variable dynamics
   - Granger causality

Perfect for interview discussions on advanced forecasting!
    """)
