import pandas as pd
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath("/home/mohan/.gemini/antigravity/scratch/reversal_pro_v3"))

import data_loader
import indicators

def debug_alkem():
    symbol = "ALKEM.NS"
    print(f"Fetching data for {symbol}...")
    
    # User image shows 15m timeframe, roughly Feb 11 - Feb 18
    # Let's fetch 1 month of 15m data
    df = data_loader.fetch_data(symbol, interval="15m", period="1mo")
    
    if df.empty:
        print("No data fetched.")
        return

    print(f"Fetched {len(df)} bars.")
    
    # Settings from Image:
    # Sensitivity: Medium
    # Confirmation: Confirmed Only (Default)
    # ATR Mult: 2.0 (Medium default)
    # Calculation Method: Average (Default)
    
    print("Running Reversal V3 Logic (Medium, Average)...")
    res = indicators.calculate_reversal_v3(
        df, 
        sensitivity="Medium", 
        calculation_method="average"
    )
    
    # Filter for Signals
    signals = res[res['Signal'] != 0].copy()
    
    print(f"\nAll Signals Found in last {len(df)} bars (approx 1 month):")
    
    # We want to see the rows where signals happened
    cols = ['open', 'high', 'low', 'close', 'Signal', 'Pivot_Time', 'Signal_Price', 'Trend']
    
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_rows', None) # Show all rows
    
    print(signals[cols])
    
    # Also print the last few rows of data to check timestamps
    print("\nLast 5 rows of data:")
    print(res[cols].tail(5))

if __name__ == "__main__":
    debug_alkem()
