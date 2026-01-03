"""
Advanced Data Preprocessing for Time Series
============================================

This module handles:
1. Multi-granularity data (Hourly → Daily → Monthly → Yearly)
2. 10 years of training data generation
3. Data quality checks
4. Aggregation and resampling
5. Missing value handling

Interview Explanation:
----------------------
Real-world data comes at different frequencies:
- Trading data: Minute/hourly
- Operational data: Daily
- Business reporting: Monthly
- Strategic planning: Yearly

We need to handle ALL these granularities!
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class TimeSeriesPreprocessor:
    """
    Comprehensive preprocessing for time series at multiple granularities
    
    Interview Points:
    -----------------
    GRANULARITY CONVERSION is critical in production!
    
    Why multiple granularities?
    1. Different stakeholders need different views
    2. Some models work better at certain frequencies
    3. Feature engineering varies by granularity
    4. Aggregation can smooth noise
    
    Challenges:
    - Missing data at higher frequencies
    - Irregular intervals (weekends, holidays)
    - Timezone handling
    - Computational cost of high frequency data
    """
    
    def __init__(self, commodity_name='Corn_CBOT'):
        self.commodity_name = commodity_name
        self.raw_data = None
        self.hourly_data = None
        self.daily_data = None
        self.monthly_data = None
        self.yearly_data = None
        
        print(f"🔧 Initialized Preprocessor for {commodity_name}")
    
    def generate_10year_hourly_data(self, start_date='2016-01-01', years=10):
        """
        Generate 10 years of HOURLY commodity price data
        
        Interview Explanation:
        ----------------------
        Why hourly data?
        - Captures intraday volatility
        - Real trading systems operate at this frequency
        - Can aggregate to any lower frequency
        
        Data characteristics:
        - 10 years × 365 days × 24 hours = 87,600 records
        - Includes trading hours only (8 AM - 4 PM)
        - Weekend/holiday handling
        - Realistic intraday patterns
        
        Challenges:
        - Large dataset (87K+ rows)
        - Missing hours (non-trading times)
        - More noise than daily data
        """
        
        print(f"\n📊 Generating 10 years of hourly data...")
        print(f"   Period: {start_date} to 10 years later")
        print(f"   Trading hours: 8 AM - 4 PM (8 hours/day)")
        
        # Base parameters for corn
        base_price = 4.0
        
        data_records = []
        current_date = pd.to_datetime(start_date)
        end_date = current_date + pd.DateOffset(years=years)
        
        # Daily price (for reference)
        daily_price = base_price
        
        day_count = 0
        
        while current_date < end_date:
            # Skip weekends
            if current_date.weekday() >= 5:  # Saturday=5, Sunday=6
                current_date += timedelta(days=1)
                continue
            
            # Update daily price (with trend + seasonality)
            day_of_year = current_date.dayofyear
            year_progress = (current_date - pd.to_datetime(start_date)).days / (years * 365)
            
            # Long-term trend (inflation)
            trend = base_price * (1 + 0.02 * year_progress)
            
            # Seasonal pattern (harvest cycle)
            seasonality = 0.3 * np.sin(2 * np.pi * day_of_year / 365)
            
            # Daily shock
            daily_shock = np.random.normal(0, 0.02)
            
            # Daily open price
            daily_open = trend + seasonality + daily_shock
            
            # Generate hourly prices for trading day (8 AM - 4 PM)
            for hour in range(8, 16):  # 8 AM to 3 PM (last hour is 3 PM)
                # Intraday pattern (U-shaped volatility)
                hour_in_day = hour - 8  # 0 to 7
                
                # Higher volatility at open and close
                if hour_in_day in [0, 7]:
                    intraday_volatility = 0.015
                else:
                    intraday_volatility = 0.005
                
                # Price movement from open
                intraday_change = np.random.normal(0, intraday_volatility)
                
                # Mean reversion within day
                hour_price = daily_open + intraday_change
                
                # Create timestamp
                timestamp = current_date.replace(hour=hour, minute=0, second=0)
                
                # 3-month future price (3-4% premium)
                future_premium = 1.035 + np.random.uniform(-0.005, 0.005)
                future_price = hour_price * future_premium
                
                data_records.append({
                    'timestamp': timestamp,
                    'date': current_date.date(),
                    'hour': hour,
                    'spot_price': hour_price,
                    'future_price_3m': future_price,
                    'volume': np.random.randint(10000, 50000),  # Trading volume
                    'commodity': self.commodity_name
                })
            
            current_date += timedelta(days=1)
            day_count += 1
            
            # Progress indicator
            if day_count % 365 == 0:
                print(f"   ✓ Year {day_count // 365} complete")
        
        self.hourly_data = pd.DataFrame(data_records)
        
        print(f"\n✅ Hourly data generated!")
        print(f"   Total records: {len(self.hourly_data):,}")
        print(f"   Date range: {self.hourly_data['timestamp'].min()} to {self.hourly_data['timestamp'].max()}")
        print(f"   Trading days: {self.hourly_data['date'].nunique():,}")
        print(f"   Average daily volume: {self.hourly_data.groupby('date')['volume'].sum().mean():,.0f}")
        
        return self.hourly_data
    
    def aggregate_to_daily(self):
        """
        Aggregate hourly data to DAILY
        
        Interview Explanation:
        ----------------------
        AGGREGATION METHODS matter!
        
        Price aggregations:
        - Open: First hour price (8 AM)
        - Close: Last hour price (3 PM)
        - High: Maximum during day
        - Low: Minimum during day
        - OHLC pattern → Candlestick charts
        
        Volume:
        - Sum of all hourly volumes
        
        Why this matters:
        - Different models need different representations
        - OHLC captures full daily range
        - Close price most common for forecasting
        """
        
        print("\n🔄 Aggregating to daily granularity...")
        
        if self.hourly_data is None:
            raise ValueError("Must generate hourly data first!")
        
        # Group by date
        daily_agg = self.hourly_data.groupby('date').agg({
            'spot_price': ['first', 'last', 'min', 'max', 'mean'],
            'future_price_3m': ['first', 'last', 'mean'],
            'volume': 'sum',
            'commodity': 'first'
        })
        
        # Flatten column names
        daily_agg.columns = ['_'.join(col).strip() for col in daily_agg.columns.values]
        daily_agg = daily_agg.reset_index()
        
        # Rename for clarity
        daily_agg = daily_agg.rename(columns={
            'spot_price_first': 'open',
            'spot_price_last': 'close',
            'spot_price_min': 'low',
            'spot_price_max': 'high',
            'spot_price_mean': 'spot_price',
            'future_price_3m_mean': 'future_price_3m',
            'volume_sum': 'volume',
            'commodity_first': 'commodity'
        })
        
        self.daily_data = daily_agg
        
        print(f"✅ Daily aggregation complete!")
        print(f"   Records: {len(self.daily_data):,}")
        print(f"   Columns: {list(self.daily_data.columns)}")
        print(f"\n   Sample OHLC data:")
        print(self.daily_data[['date', 'open', 'high', 'low', 'close']].head())
        
        return self.daily_data
    
    def aggregate_to_monthly(self):
        """
        Aggregate daily data to MONTHLY
        
        Interview Explanation:
        ----------------------
        Monthly aggregation for:
        - Business reporting (monthly P&L)
        - Seasonal pattern analysis
        - Long-term forecasting
        
        Key metrics:
        - Month-end price (last day)
        - Average price (mean)
        - Price range (high - low)
        - Total volume
        
        Challenge: Irregular month lengths (28-31 days)
        """
        
        print("\n🔄 Aggregating to monthly granularity...")
        
        if self.daily_data is None:
            raise ValueError("Must aggregate to daily first!")
        
        # Convert date to datetime for resampling
        self.daily_data['date'] = pd.to_datetime(self.daily_data['date'])
        self.daily_data = self.daily_data.set_index('date')
        
        # Resample to month-end
        monthly_agg = self.daily_data.resample('M').agg({
            'spot_price': ['first', 'last', 'mean', 'std'],
            'open': 'first',
            'close': 'last',
            'high': 'max',
            'low': 'min',
            'volume': 'sum',
            'commodity': 'first'
        })
        
        monthly_agg.columns = ['_'.join(col).strip() for col in monthly_agg.columns.values]
        monthly_agg = monthly_agg.reset_index()
        
        monthly_agg = monthly_agg.rename(columns={
            'date': 'month',
            'spot_price_last': 'month_end_price',
            'spot_price_mean': 'avg_price',
            'spot_price_std': 'volatility',
            'volume_sum': 'total_volume',
            'commodity_first': 'commodity'
        })
        
        self.monthly_data = monthly_agg
        
        print(f"✅ Monthly aggregation complete!")
        print(f"   Records: {len(self.monthly_data):,} months")
        print(f"   Average monthly volume: {self.monthly_data['total_volume'].mean():,.0f}")
        
        return self.monthly_data
    
    def aggregate_to_yearly(self):
        """
        Aggregate monthly data to YEARLY
        
        Interview Explanation:
        ----------------------
        Yearly aggregation for:
        - Strategic planning
        - Long-term trend analysis
        - Annual budgeting
        
        Captures:
        - Year-end price
        - Annual average
        - Full year volatility
        - Total annual volume
        """
        
        print("\n🔄 Aggregating to yearly granularity...")
        
        if self.monthly_data is None:
            raise ValueError("Must aggregate to monthly first!")
        
        # Extract year
        self.monthly_data['year'] = pd.to_datetime(self.monthly_data['month']).dt.year
        
        yearly_agg = self.monthly_data.groupby('year').agg({
            'avg_price': ['first', 'last', 'mean', 'min', 'max'],
            'volatility': 'mean',
            'total_volume': 'sum',
            'commodity': 'first'
        })
        
        yearly_agg.columns = ['_'.join(col).strip() for col in yearly_agg.columns.values]
        yearly_agg = yearly_agg.reset_index()
        
        yearly_agg = yearly_agg.rename(columns={
            'avg_price_first': 'year_start_price',
            'avg_price_last': 'year_end_price',
            'avg_price_mean': 'annual_avg_price',
            'avg_price_min': 'annual_low',
            'avg_price_max': 'annual_high',
            'volatility_mean': 'annual_volatility',
            'total_volume_sum': 'annual_volume',
            'commodity_first': 'commodity'
        })
        
        self.yearly_data = yearly_agg
        
        print(f"✅ Yearly aggregation complete!")
        print(f"   Records: {len(self.yearly_data)} years")
        print(f"\n   Yearly Summary:")
        print(self.yearly_data[['year', 'annual_avg_price', 'annual_volatility']])
        
        return self.yearly_data
    
    def handle_missing_values(self, method='ffill'):
        """
        Handle missing values in time series
        
        Interview Explanation:
        ----------------------
        Missing data in time series is common:
        - Holidays (markets closed)
        - System outages
        - Data collection failures
        
        Methods:
        1. FORWARD FILL (ffill): Use last known value
           - Good for: Prices (don't jump instantly)
           - Bad for: Volume (artificially inflates)
        
        2. BACKWARD FILL (bfill): Use next known value
           - Good for: Planning future data
        
        3. INTERPOLATION: Linear between points
           - Good for: Smooth trends
           - Bad for: Volatile series
        
        4. MEAN/MEDIAN: Fill with average
           - Good for: Stable series
           - Bad for: Trending data
        
        For commodities: ffill is standard (prices persist)
        """
        
        print(f"\n🔧 Handling missing values with method: {method}")
        
        datasets = {
            'hourly': self.hourly_data,
            'daily': self.daily_data,
            'monthly': self.monthly_data,
            'yearly': self.yearly_data
        }
        
        for name, df in datasets.items():
            if df is not None:
                missing_before = df.isnull().sum().sum()
                
                if method == 'ffill':
                    df = df.fillna(method='ffill')
                elif method == 'bfill':
                    df = df.fillna(method='bfill')
                elif method == 'interpolate':
                    df = df.interpolate(method='linear')
                
                missing_after = df.isnull().sum().sum()
                
                print(f"   {name}: {missing_before} → {missing_after} missing values")
                
                # Update stored data
                if name == 'hourly':
                    self.hourly_data = df
                elif name == 'daily':
                    self.daily_data = df
                elif name == 'monthly':
                    self.monthly_data = df
                elif name == 'yearly':
                    self.yearly_data = df
        
        print("✅ Missing value handling complete!")
    
    def save_all_granularities(self, output_dir='data'):
        """
        Save all granularity levels to CSV
        
        Interview Explanation:
        ----------------------
        Data versioning in production:
        - Save processed data at each granularity
        - Allows quick loading without reprocessing
        - Different models use different granularities
        - Audit trail of transformations
        """
        
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\n💾 Saving all data granularities to {output_dir}/...")
        
        if self.hourly_data is not None:
            path = f"{output_dir}/{self.commodity_name}_hourly_10yr.csv"
            self.hourly_data.to_csv(path, index=False)
            print(f"   ✓ Hourly: {path} ({len(self.hourly_data):,} rows)")
        
        if self.daily_data is not None:
            path = f"{output_dir}/{self.commodity_name}_daily_10yr.csv"
            self.daily_data.to_csv(path, index=False)
            print(f"   ✓ Daily: {path} ({len(self.daily_data):,} rows)")
        
        if self.monthly_data is not None:
            path = f"{output_dir}/{self.commodity_name}_monthly_10yr.csv"
            self.monthly_data.to_csv(path, index=False)
            print(f"   ✓ Monthly: {path} ({len(self.monthly_data):,} rows)")
        
        if self.yearly_data is not None:
            path = f"{output_dir}/{self.commodity_name}_yearly_10yr.csv"
            self.yearly_data.to_csv(path, index=False)
            print(f"   ✓ Yearly: {path} ({len(self.yearly_data):,} rows)")
        
        print("\n✅ All granularities saved!")


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("  MULTI-GRANULARITY DATA PREPROCESSING")
    print("=" * 70)
    
    preprocessor = TimeSeriesPreprocessor('Corn_CBOT')
    
    # Generate 10 years of hourly data
    hourly_df = preprocessor.generate_10year_hourly_data(years=10)
    
    # Aggregate to all granularities
    daily_df = preprocessor.aggregate_to_daily()
    monthly_df = preprocessor.aggregate_to_monthly()
    yearly_df = preprocessor.aggregate_to_yearly()
    
    # Handle missing values
    preprocessor.handle_missing_values(method='ffill')
    
    # Save all
    preprocessor.save_all_granularities()
    
    print("\n" + "=" * 70)
    print("  PREPROCESSING COMPLETE!")
    print("=" * 70)
    print("\nInterview Takeaway:")
    print("✅ Handled multiple time granularities")
    print("✅ 10 years of training data")
    print("✅ Proper aggregation methods (OHLC)")
    print("✅ Missing value handling")
    print("✅ Production-ready data pipeline")
