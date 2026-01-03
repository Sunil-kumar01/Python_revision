"""
AB InBev Commodity Price Data Generator

This script generates realistic historical commodity prices for:
- Corn (CBOT - Chicago Board of Trade)
- Corn (BMF - Brazilian Mercantile & Futures Exchange)
- Wheat
- Barley
- Diesel

The data includes:
- 5 years of daily historical prices
- Spot prices (current market price)
- Future prices (3-month forward contracts)
- Seasonal patterns
- Market trends
- Price volatility

For interview explanation: This simulates real commodity market data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)

def generate_commodity_prices(
    commodity_name,
    base_price,
    start_date='2021-01-01',
    periods=1825,  # 5 years of daily data
    trend=0.0001,
    seasonality_amplitude=0.05,
    seasonality_period=365,
    volatility=0.02,
    future_premium=0.03
):
    """
    Generate realistic commodity price time series
    
    Parameters:
    -----------
    commodity_name : str
        Name of the commodity (e.g., 'Corn_CBOT')
    base_price : float
        Starting price in USD per unit
    start_date : str
        Start date for the time series
    periods : int
        Number of days to generate
    trend : float
        Daily trend factor (0.0001 = 0.01% daily growth)
    seasonality_amplitude : float
        Seasonal variation amplitude (0.05 = 5% variation)
    seasonality_period : int
        Period of seasonality in days (365 = annual)
    volatility : float
        Daily price volatility (0.02 = 2% standard deviation)
    future_premium : float
        Premium for 3-month futures vs spot (0.03 = 3% higher)
    
    Returns:
    --------
    pd.DataFrame with columns: date, spot_price, future_price_3m
    
    Interview Explanation:
    ----------------------
    TREND: Long-term price movement (inflation, demand growth)
    SEASONALITY: Recurring patterns (harvest seasons, weather)
    VOLATILITY: Random daily fluctuations (news, supply shocks)
    FUTURE PREMIUM: Cost of locking price in advance (storage, interest)
    """
    
    # Generate date range
    dates = pd.date_range(start=start_date, periods=periods, freq='D')
    
    # Initialize prices array
    prices = np.zeros(periods)
    prices[0] = base_price
    
    # Generate price series with components
    for i in range(1, periods):
        # TREND COMPONENT (long-term growth/decline)
        # Interview: "Prices generally increase due to inflation and demand"
        trend_component = trend * i
        
        # SEASONAL COMPONENT (harvest cycles, weather patterns)
        # Interview: "Corn prices typically drop after harvest (Sept-Nov)"
        # Using sine wave: high in summer (planting), low after harvest
        seasonal_component = seasonality_amplitude * np.sin(
            2 * np.pi * i / seasonality_period
        )
        
        # RANDOM WALK COMPONENT (daily volatility)
        # Interview: "Daily news, weather, policy changes cause random movements"
        random_shock = np.random.normal(0, volatility)
        
        # Combine all components
        # Price(t) = Price(t-1) * (1 + trend + seasonal + random)
        prices[i] = prices[i-1] * (
            1 + trend_component + seasonal_component + random_shock
        )
        
        # Add occasional price spikes (supply shocks, droughts, etc.)
        # Interview: "Events like droughts can cause sudden price jumps"
        if np.random.random() < 0.02:  # 2% chance of shock
            shock_magnitude = np.random.uniform(0.05, 0.15)  # 5-15% spike
            prices[i] *= (1 + shock_magnitude)
    
    # Generate 3-month future prices
    # Future prices = Spot prices + premium (storage, interest, risk)
    # Interview: "Futures cost more because you're paying for price certainty"
    future_prices = prices * (1 + future_premium + np.random.normal(0, 0.01, periods))
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': dates,
        'commodity': commodity_name,
        'spot_price': prices,
        'future_price_3m': future_prices
    })
    
    return df


def generate_all_commodities():
    """
    Generate data for all AB InBev commodities
    
    Interview Context:
    ------------------
    "At AB InBev, we track multiple commodities for beer production:
    - CORN: Primary ingredient (brewing), tracked on CBOT (US) and BMF (Brazil)
    - WHEAT & BARLEY: Alternative grains for different beer types
    - DIESEL: Transportation costs for distribution
    
    We need to hedge these to control costs and maintain profit margins."
    """
    
    print("🌾 Generating AB InBev Commodity Price Data...")
    print("=" * 60)
    
    # 1. CORN (CBOT) - Chicago Board of Trade
    # Most liquid corn futures market globally
    # Base price: ~$4.00 per bushel
    print("Generating Corn (CBOT) prices...")
    corn_cbot = generate_commodity_prices(
        commodity_name='Corn_CBOT',
        base_price=4.00,
        trend=0.00005,  # Slight upward trend
        seasonality_amplitude=0.08,  # 8% seasonal variation
        volatility=0.025,  # 2.5% daily volatility
        future_premium=0.035  # 3.5% futures premium
    )
    
    # 2. CORN (BMF) - Brazilian Exchange
    # Similar to CBOT but with Brazil-specific factors
    # Typically 10-15% cheaper due to local production
    print("Generating Corn (BMF) prices...")
    corn_bmf = generate_commodity_prices(
        commodity_name='Corn_BMF',
        base_price=3.50,  # Cheaper than CBOT
        trend=0.00006,
        seasonality_amplitude=0.09,  # More volatile
        volatility=0.03,  # Higher volatility (emerging market)
        future_premium=0.04  # Higher premium (more risk)
    )
    
    # 3. WHEAT
    # Alternative grain, less used but important for specialty beers
    # Base price: ~$5.50 per bushel
    print("Generating Wheat prices...")
    wheat = generate_commodity_prices(
        commodity_name='Wheat',
        base_price=5.50,
        trend=0.00004,
        seasonality_amplitude=0.07,
        volatility=0.028,
        future_premium=0.03
    )
    
    # 4. BARLEY
    # Primary ingredient for malting (beer flavor)
    # Base price: ~$4.80 per bushel
    print("Generating Barley prices...")
    barley = generate_commodity_prices(
        commodity_name='Barley',
        base_price=4.80,
        trend=0.00003,
        seasonality_amplitude=0.10,  # High seasonality
        volatility=0.022,
        future_premium=0.032
    )
    
    # 5. DIESEL
    # Critical for transportation/distribution
    # Base price: ~$2.80 per gallon
    print("Generating Diesel prices...")
    diesel = generate_commodity_prices(
        commodity_name='Diesel',
        base_price=2.80,
        trend=0.00008,  # Higher trend (oil prices)
        seasonality_amplitude=0.12,  # Seasonal demand
        volatility=0.035,  # High volatility
        future_premium=0.045  # Higher premium
    )
    
    # Combine all commodities
    all_data = pd.concat([corn_cbot, corn_bmf, wheat, barley, diesel], ignore_index=True)
    
    # Add derived features for modeling
    print("\nAdding features for time series modeling...")
    all_data['year'] = all_data['date'].dt.year
    all_data['month'] = all_data['date'].dt.month
    all_data['day_of_year'] = all_data['date'].dt.dayofyear
    all_data['quarter'] = all_data['date'].dt.quarter
    
    # Price difference (Spot vs Future)
    # Interview: "The spread between spot and futures indicates market expectations"
    all_data['spot_future_spread'] = all_data['future_price_3m'] - all_data['spot_price']
    all_data['spot_future_spread_pct'] = (
        (all_data['future_price_3m'] - all_data['spot_price']) / all_data['spot_price'] * 100
    )
    
    # Save data
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    
    # Save combined data
    all_data.to_csv(f'{output_dir}/commodity_prices_all.csv', index=False)
    print(f"\n✅ Saved: {output_dir}/commodity_prices_all.csv")
    
    # Save individual commodity files
    for commodity in all_data['commodity'].unique():
        commodity_df = all_data[all_data['commodity'] == commodity].copy()
        filename = f"{output_dir}/{commodity.lower()}_prices.csv"
        commodity_df.to_csv(filename, index=False)
        print(f"✅ Saved: {filename}")
    
    # Print summary statistics
    print("\n" + "=" * 60)
    print("📊 DATA SUMMARY")
    print("=" * 60)
    print(f"Total records: {len(all_data):,}")
    print(f"Date range: {all_data['date'].min()} to {all_data['date'].max()}")
    print(f"Commodities: {all_data['commodity'].nunique()}")
    print("\nPrice Statistics by Commodity:")
    print("-" * 60)
    
    for commodity in all_data['commodity'].unique():
        commodity_data = all_data[all_data['commodity'] == commodity]
        spot_mean = commodity_data['spot_price'].mean()
        spot_std = commodity_data['spot_price'].std()
        future_mean = commodity_data['future_price_3m'].mean()
        
        print(f"\n{commodity}:")
        print(f"  Spot Price:   ${spot_mean:.2f} ± ${spot_std:.2f}")
        print(f"  Future Price: ${future_mean:.2f}")
        print(f"  Avg Premium:  {(future_mean - spot_mean):.2f} ({(future_mean/spot_mean - 1)*100:.1f}%)")
    
    print("\n" + "=" * 60)
    print("🎯 Ready for Time Series Modeling!")
    print("=" * 60)
    
    return all_data


if __name__ == "__main__":
    # Generate all commodity data
    data = generate_all_commodities()
    
    # Preview data
    print("\n📋 Sample Data Preview:")
    print(data.head(10).to_string())
    
    print("\n✨ Data generation complete!")
    print("\nNext steps:")
    print("1. Load data: pd.read_csv('data/commodity_prices_all.csv')")
    print("2. Explore trends and seasonality")
    print("3. Build time series models (ARIMA, Prophet, LSTM)")
    print("4. Create forecasting pipeline")
    print("5. Deploy dashboard with T-policy recommendations")
