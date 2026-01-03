"""
Comprehensive Time Series EDA (Exploratory Data Analysis)
==========================================================

This module performs:
1. Time series decomposition (Trend, Seasonality, Residuals)
2. Stationarity testing (ADF, KPSS, PP tests)
3. Moving averages analysis
4. ACF/PACF plots
5. Seasonal patterns identification
6. Volatility clustering detection

Interview Focus: Understanding time series STRUCTURE before modeling
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, kpss, acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class TimeSeriesEDA:
    """
    Comprehensive EDA for time series data
    
    Interview Explanation:
    ----------------------
    Before building ANY time series model, you MUST understand:
    
    1. TREND: Long-term increase/decrease
       - Is price generally going up or down?
       - Linear or non-linear trend?
    
    2. SEASONALITY: Repeating patterns
       - Monthly, quarterly, yearly cycles?
       - For commodities: harvest seasons!
    
    3. RESIDUALS: What's left after removing trend + seasonality
       - Should look like white noise
       - If not → missing patterns
    
    4. STATIONARITY: Statistical properties constant over time
       - Critical assumption for ARIMA models!
       - Test with ADF (Augmented Dickey-Fuller)
    
    This is the FOUNDATION of time series modeling!
    """
    
    def __init__(self, data, target_col='spot_price', date_col='date'):
        self.data = data.copy()
        self.target_col = target_col
        self.date_col = date_col
        
        # Ensure date column is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.data[date_col]):
            self.data[date_col] = pd.to_datetime(self.data[date_col])
        
        # Set date as index
        self.data = self.data.set_index(date_col).sort_index()
        
        print(f"📊 EDA initialized for {target_col}")
        print(f"   Data shape: {self.data.shape}")
        print(f"   Date range: {self.data.index.min()} to {self.data.index.max()}")
    
    def plot_time_series(self, figsize=(15, 5)):
        """
        Basic time series visualization
        
        Interview Explanation:
        ----------------------
        ALWAYS start with a simple plot!
        
        What to look for:
        1. Overall trend (up/down/flat)
        2. Obvious seasonality (repeating peaks/troughs)
        3. Volatility changes (variance increases over time?)
        4. Outliers (sudden spikes/drops)
        5. Structural breaks (regime changes)
        
        This visual inspection guides modeling choices!
        """
        
        print("\n📈 Plotting time series...")
        
        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(self.data.index, self.data[self.target_col], linewidth=1, alpha=0.8)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel(f'{self.target_col} ($/bushel)', fontsize=12)
        ax.set_title(f'Time Series Plot: {self.target_col}', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('outputs/01_time_series_plot.png', dpi=300, bbox_inches='tight')
        print("   ✓ Saved: outputs/01_time_series_plot.png")
        plt.show()
    
    def decompose_time_series(self, model='additive', period=365):
        """
        Decompose time series into Trend + Seasonality + Residuals
        
        Interview Explanation:
        ----------------------
        TIME SERIES DECOMPOSITION - One of the MOST important EDA steps!
        
        Formula: Observed = Trend + Seasonal + Residual
        
        ADDITIVE MODEL (default):
        - Use when seasonal variation is constant
        - Y(t) = T(t) + S(t) + R(t)
        
        MULTIPLICATIVE MODEL:
        - Use when seasonal variation increases with level
        - Y(t) = T(t) × S(t) × R(t)
        
        Components:
        
        1. TREND (T):
           - Long-term direction
           - Captures inflation, demand growth
           - Interview: "Overall upward movement in prices"
        
        2. SEASONAL (S):
           - Repeating patterns
           - For commodities: Harvest cycles (yearly)
           - Interview: "Prices drop in September (harvest), rise in March (planting)"
        
        3. RESIDUAL (R):
           - What's left over
           - Should look random (white noise)
           - If patterns remain → missing features!
        
        Period:
        - Daily data, yearly pattern → period=365
        - Monthly data, yearly pattern → period=12
        - Hourly data, daily pattern → period=24
        
        Why this matters:
        - Detrending → Stationarity
        - Deseasonalizing → Cleaner patterns
        - Understanding drivers → Better features
        """
        
        print(f"\n🔍 Decomposing time series (model={model}, period={period})...")
        
        # Perform decomposition
        decomposition = seasonal_decompose(
            self.data[self.target_col],
            model=model,
            period=period,
            extrapolate_trend='freq'
        )
        
        # Plot
        fig, axes = plt.subplots(4, 1, figsize=(15, 12))
        
        # Original
        axes[0].plot(self.data.index, self.data[self.target_col], linewidth=1)
        axes[0].set_ylabel('Observed', fontsize=11)
        axes[0].set_title('Time Series Decomposition', fontsize=14, fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        
        # Trend
        axes[1].plot(decomposition.trend.index, decomposition.trend, color='orange', linewidth=2)
        axes[1].set_ylabel('Trend', fontsize=11)
        axes[1].grid(True, alpha=0.3)
        axes[1].annotate('Long-term direction', xy=(0.02, 0.9), xycoords='axes fraction',
                        fontsize=10, style='italic', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # Seasonal
        axes[2].plot(decomposition.seasonal.index, decomposition.seasonal, color='green', linewidth=1)
        axes[2].set_ylabel('Seasonal', fontsize=11)
        axes[2].grid(True, alpha=0.3)
        axes[2].annotate('Repeating patterns (harvest cycle)', xy=(0.02, 0.9), xycoords='axes fraction',
                        fontsize=10, style='italic', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
        
        # Residual
        axes[3].plot(decomposition.resid.index, decomposition.resid, color='red', linewidth=0.5, alpha=0.7)
        axes[3].set_ylabel('Residual', fontsize=11)
        axes[3].set_xlabel('Date', fontsize=12)
        axes[3].grid(True, alpha=0.3)
        axes[3].annotate('Should look random (white noise)', xy=(0.02, 0.9), xycoords='axes fraction',
                        fontsize=10, style='italic', bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig('outputs/02_decomposition.png', dpi=300, bbox_inches='tight')
        print("   ✓ Saved: outputs/02_decomposition.png")
        plt.show()
        
        # Store components
        self.trend = decomposition.trend
        self.seasonal = decomposition.seasonal
        self.residual = decomposition.resid
        
        print("\n✅ Decomposition complete!")
        print(f"   Trend strength: {1 - (decomposition.resid.var() / decomposition.trend.var()):.2%}")
        print(f"   Seasonal strength: {1 - (decomposition.resid.var() / decomposition.seasonal.var()):.2%}")
        
        return decomposition
    
    def test_stationarity_adf(self):
        """
        Test stationarity using ADF (Augmented Dickey-Fuller) test
        
        Interview Explanation:
        ----------------------
        STATIONARITY - Critical concept for time series!
        
        What is stationarity?
        - Mean is constant over time
        - Variance is constant over time
        - Covariance depends only on lag, not time
        
        Why does it matter?
        - Many models (ARIMA) REQUIRE stationarity
        - Non-stationary = unpredictable long-term
        - Makes statistical inference valid
        
        ADF TEST (Augmented Dickey-Fuller):
        
        What it tests:
        - H0 (Null): Series has unit root → NON-stationary
        - H1 (Alt): Series is stationary
        
        How to interpret:
        - p-value < 0.05 → Reject H0 → STATIONARY ✅
        - p-value > 0.05 → Fail to reject H0 → NON-STATIONARY ❌
        
        Unit Root:
        - Root = 1 in characteristic equation
        - Means shocks have permanent effect
        - Need differencing to remove
        
        If non-stationary, try:
        1. Differencing: Y'(t) = Y(t) - Y(t-1)
        2. Log transform: log(Y(t))
        3. Detrending: Remove linear trend
        
        Interview: "ADF tests if series is stationary. If p < 0.05, it's stationary.
                   For ARIMA, we difference until stationary."
        """
        
        print("\n🧪 Testing Stationarity - ADF Test...")
        print("=" * 60)
        
        # Perform ADF test
        result = adfuller(self.data[self.target_col].dropna(), autolag='AIC')
        
        adf_stat = result[0]
        p_value = result[1]
        critical_values = result[4]
        
        print(f"\n📊 ADF Test Results:")
        print(f"   ADF Statistic: {adf_stat:.6f}")
        print(f"   p-value: {p_value:.6f}")
        print(f"\n   Critical Values:")
        for key, value in critical_values.items():
            print(f"      {key}: {value:.6f}")
        
        print(f"\n📝 Interpretation:")
        if p_value < 0.05:
            print(f"   ✅ STATIONARY (p-value = {p_value:.6f} < 0.05)")
            print(f"   → Reject null hypothesis")
            print(f"   → Series does NOT have unit root")
            print(f"   → Safe to use ARIMA models without differencing")
        else:
            print(f"   ❌ NON-STATIONARY (p-value = {p_value:.6f} > 0.05)")
            print(f"   → Fail to reject null hypothesis")
            print(f"   → Series HAS unit root")
            print(f"   → Need differencing or detrending!")
        
        print("\n" + "=" * 60)
        
        return {
            'adf_statistic': adf_stat,
            'p_value': p_value,
            'critical_values': critical_values,
            'is_stationary': p_value < 0.05
        }
    
    def test_stationarity_kpss(self):
        """
        Test stationarity using KPSS test
        
        Interview Explanation:
        ----------------------
        KPSS TEST (Kwiatkowski-Phillips-Schmidt-Shin)
        
        Difference from ADF:
        - ADF: H0 = non-stationary
        - KPSS: H0 = stationary (OPPOSITE!)
        
        Why use both?
        - ADF has low power against near-unit-root
        - KPSS complements ADF
        - Use BOTH for confirmation!
        
        Interpretation:
        - p-value > 0.05 → Fail to reject H0 → STATIONARY ✅
        - p-value < 0.05 → Reject H0 → NON-STATIONARY ❌
        
        Interview: "KPSS is opposite of ADF - null is stationarity.
                   We use both tests to be confident."
        """
        
        print("\n🧪 Testing Stationarity - KPSS Test...")
        print("=" * 60)
        
        result = kpss(self.data[self.target_col].dropna(), regression='ct')
        
        kpss_stat = result[0]
        p_value = result[1]
        critical_values = result[3]
        
        print(f"\n📊 KPSS Test Results:")
        print(f"   KPSS Statistic: {kpss_stat:.6f}")
        print(f"   p-value: {p_value:.6f}")
        print(f"\n   Critical Values:")
        for key, value in critical_values.items():
            print(f"      {key}: {value:.6f}")
        
        print(f"\n📝 Interpretation (Note: KPSS has OPPOSITE null!):")
        if p_value > 0.05:
            print(f"   ✅ STATIONARY (p-value = {p_value:.6f} > 0.05)")
            print(f"   → Fail to reject null hypothesis")
            print(f"   → Series is trend-stationary")
        else:
            print(f"   ❌ NON-STATIONARY (p-value = {p_value:.6f} < 0.05)")
            print(f"   → Reject null hypothesis")
            print(f"   → Series has deterministic trend or unit root")
        
        print("\n" + "=" * 60)
        
        return {
            'kpss_statistic': kpss_stat,
            'p_value': p_value,
            'critical_values': critical_values,
            'is_stationary': p_value > 0.05
        }
    
    def calculate_moving_averages(self, windows=[7, 30, 90, 180]):
        """
        Calculate and visualize moving averages
        
        Interview Explanation:
        ----------------------
        MOVING AVERAGES (MA) - Smoothing technique
        
        Simple Moving Average (SMA):
        MA(t) = (Y(t) + Y(t-1) + ... + Y(t-n+1)) / n
        
        Why use multiple windows?
        - Short MA (7-day): Captures recent trends
        - Medium MA (30-day): Monthly patterns
        - Long MA (90-180 day): Long-term trends
        
        Trading signals:
        - Price > MA → Uptrend
        - Price < MA → Downtrend
        - Short MA crosses Long MA → Trend change!
        
        For forecasting:
        - MA smooths noise
        - Helps identify trend direction
        - Baseline model comparison
        
        Interview: "I use multiple MA windows to capture trends at different time scales.
                   Crossovers signal trend changes."
        """
        
        print(f"\n📊 Calculating moving averages: {windows}")
        
        fig, ax = plt.subplots(figsize=(15, 6))
        
        # Plot original series
        ax.plot(self.data.index, self.data[self.target_col], 
                label='Original', linewidth=1, alpha=0.6, color='gray')
        
        # Calculate and plot MAs
        colors = ['blue', 'green', 'orange', 'red']
        for window, color in zip(windows, colors):
            ma = self.data[self.target_col].rolling(window=window).mean()
            ax.plot(self.data.index, ma, 
                   label=f'{window}-day MA', linewidth=2, color=color, alpha=0.8)
            
            # Store in data
            self.data[f'ma_{window}'] = ma
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price ($/bushel)', fontsize=12)
        ax.set_title('Moving Averages Analysis', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('outputs/03_moving_averages.png', dpi=300, bbox_inches='tight')
        print("   ✓ Saved: outputs/03_moving_averages.png")
        plt.show()
        
        print("✅ Moving averages calculated!")
    
    def plot_acf_pacf(self, lags=40):
        """
        Plot ACF and PACF
        
        Interview Explanation:
        ----------------------
        ACF & PACF - Critical for choosing ARIMA parameters!
        
        ACF (AutoCorrelation Function):
        - Correlation between Y(t) and Y(t-k) for different lags k
        - Includes INDIRECT correlations
        - Shows if past values predict future
        
        PACF (Partial AutoCorrelation Function):
        - Correlation between Y(t) and Y(t-k) AFTER removing intermediate correlations
        - Shows DIRECT relationship only
        
        How to use for ARIMA(p,d,q):
        
        AR(p) - Look at PACF:
        - Sharp cutoff at lag p → AR(p)
        - PACF significant up to lag 3 → p=3
        
        MA(q) - Look at ACF:
        - Sharp cutoff at lag q → MA(q)
        - ACF significant up to lag 2 → q=2
        
        Blue shaded area = 95% confidence interval
        - Spikes outside = statistically significant
        
        Interview: "ACF/PACF help determine AR and MA orders.
                   PACF shows AR order, ACF shows MA order."
        """
        
        print(f"\n📊 Plotting ACF and PACF (lags={lags})...")
        
        fig, axes = plt.subplots(2, 1, figsize=(15, 8))
        
        # ACF
        plot_acf(self.data[self.target_col].dropna(), lags=lags, ax=axes[0], alpha=0.05)
        axes[0].set_title('AutoCorrelation Function (ACF)', fontsize=12, fontweight='bold')
        axes[0].set_xlabel('Lag', fontsize=11)
        axes[0].set_ylabel('ACF', fontsize=11)
        axes[0].annotate('Look for MA(q) order\nCutoff at lag q', 
                        xy=(0.7, 0.8), xycoords='axes fraction',
                        fontsize=10, style='italic',
                        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
        
        # PACF
        plot_pacf(self.data[self.target_col].dropna(), lags=lags, ax=axes[1], alpha=0.05)
        axes[1].set_title('Partial AutoCorrelation Function (PACF)', fontsize=12, fontweight='bold')
        axes[1].set_xlabel('Lag', fontsize=11)
        axes[1].set_ylabel('PACF', fontsize=11)
        axes[1].annotate('Look for AR(p) order\nCutoff at lag p', 
                        xy=(0.7, 0.8), xycoords='axes fraction',
                        fontsize=10, style='italic',
                        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
        
        plt.tight_layout()
        plt.savefig('outputs/04_acf_pacf.png', dpi=300, bbox_inches='tight')
        print("   ✓ Saved: outputs/04_acf_pacf.png")
        plt.show()
    
    def seasonal_patterns(self):
        """
        Analyze seasonal patterns
        
        Interview Explanation:
        ----------------------
        SEASONALITY in commodities is CRITICAL!
        
        Why seasonality matters:
        - Harvest cycles (predictable supply changes)
        - Weather patterns (demand for heating oil in winter)
        - Agricultural calendar (planting → harvest)
        
        Patterns to look for:
        - Monthly: Which months have high/low prices?
        - Quarterly: Q3 (harvest) vs Q1 (planting)
        - Day of week: Monday effect?
        
        Interview: "Corn prices drop in September/October (harvest),
                   rise in February/March (pre-planting demand)."
        """
        
        print("\n📅 Analyzing seasonal patterns...")
        
        # Extract month
        self.data['month'] = self.data.index.month
        
        # Monthly average
        monthly_avg = self.data.groupby('month')[self.target_col].mean()
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # Box plot by month
        month_data = [self.data[self.data['month'] == m][self.target_col].values 
                     for m in range(1, 13)]
        axes[0].boxplot(month_data, labels=['Jan','Feb','Mar','Apr','May','Jun',
                                            'Jul','Aug','Sep','Oct','Nov','Dec'])
        axes[0].set_ylabel('Price ($/bushel)', fontsize=11)
        axes[0].set_xlabel('Month', fontsize=11)
        axes[0].set_title('Price Distribution by Month', fontsize=12, fontweight='bold')
        axes[0].grid(True, alpha=0.3, axis='y')
        axes[0].annotate('Harvest season\n(low prices)', 
                        xy=(9, axes[0].get_ylim()[0] + 0.1), 
                        fontsize=9, style='italic', ha='center',
                        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
        
        # Line plot of monthly averages
        axes[1].plot(monthly_avg.index, monthly_avg.values, marker='o', linewidth=2, markersize=8)
        axes[1].set_ylabel('Average Price ($/bushel)', fontsize=11)
        axes[1].set_xlabel('Month', fontsize=11)
        axes[1].set_title('Average Price by Month', fontsize=12, fontweight='bold')
        axes[1].set_xticks(range(1, 13))
        axes[1].set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun',
                                'Jul','Aug','Sep','Oct','Nov','Dec'])
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('outputs/05_seasonal_patterns.png', dpi=300, bbox_inches='tight')
        print("   ✓ Saved: outputs/05_seasonal_patterns.png")
        plt.show()
    
    def generate_full_report(self):
        """
        Generate comprehensive EDA report
        """
        
        print("\n" + "=" * 70)
        print("  COMPREHENSIVE TIME SERIES EDA REPORT")
        print("=" * 70)
        
        import os
        os.makedirs('outputs', exist_ok=True)
        
        # 1. Time series plot
        self.plot_time_series()
        
        # 2. Decomposition
        self.decompose_time_series(period=365)
        
        # 3. Stationarity tests
        adf_result = self.test_stationarity_adf()
        kpss_result = self.test_stationarity_kpss()
        
        # 4. Moving averages
        self.calculate_moving_averages()
        
        # 5. ACF/PACF
        self.plot_acf_pacf()
        
        # 6. Seasonal patterns
        self.seasonal_patterns()
        
        print("\n" + "=" * 70)
        print("  EDA COMPLETE - ALL VISUALIZATIONS SAVED TO outputs/")
        print("=" * 70)
        
        return {
            'adf_test': adf_result,
            'kpss_test': kpss_result
        }


# Example usage
if __name__ == "__main__":
    print("Loading data...")
    df = pd.read_csv('data/corn_cbot_prices.csv')
    
    eda = TimeSeriesEDA(df, target_col='spot_price', date_col='date')
    results = eda.generate_full_report()
    
    print("\n✅ All EDA complete! Check outputs/ folder for visualizations.")
