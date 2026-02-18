import data_loader
import indicators
import pandas as pd
import pytz
from datetime import datetime

IST = pytz.timezone('Asia/Kolkata')

def debug_stock(symbol, interval):
    print(f"\n--- Debugging {symbol} [{interval}] ---")
    df = data_loader.fetch_data(symbol, interval=interval)
    
    if df.empty:
        print("Dataframe is EMPTY!")
        return

    print(f"Dataframe Shape: {df.shape}")
    print(f"Last 3 Indices: {df.index[-3:]}")
    
    # Calculate Indicators
    close = df['close']
    ema5 = indicators.calculate_ema(df, 5)
    stoch_rsi_k = indicators.calculate_stoch_rsi(df)
    smi = indicators.calculate_smi(df)
    macd_line = indicators.calculate_macd(df)
    
    # Check "Intraday" logic
    is_intraday = False
    if len(df) > 1:
        time_diff = df.index[-1] - df.index[-2]
        if time_diff < pd.Timedelta(days=1):
            is_intraday = True
            
    print(f"Is Intraday? {is_intraday}")
    
    indices_to_check = []
    if is_intraday:
        now_ist = datetime.now(IST)
        today_date = now_ist.date()
        print(f"Current IST Date: {today_date}")
        
        # Mimic scanner logic
        candidates = df.index[-75:]
        indices_to_check = [idx for idx in candidates if idx.date() == today_date]
        print(f"Indices matching today: {len(indices_to_check)}")
        
        if not indices_to_check:
            print("WARNING: No data for today! This is why Intraday returns nothing.")
            # Check last available date
            last_date = df.index[-1].date()
            print(f"Last available date in data: {last_date}")
            
    else:
        indices_to_check = [df.index[-1]]
        
    # Check conditions for the last available candle to see if logic holds
    last_idx = df.index[-1]
    c = close.iloc[-1]
    e5 = ema5.iloc[-1]
    k = stoch_rsi_k.iloc[-1]
    s = smi.iloc[-1]
    m = macd_line.iloc[-1]
    
    print(f"\nLast Candle Values:")
    print(f"Close: {c}")
    print(f"EMA5: {e5} (Rule: > {e5}) -> {c > e5}")
    print(f"Stoch K: {k} (Rule: > 70) -> {k > 70}")
    print(f"SMI: {s} (Rule: > 30) -> {s > 30}")
    print(f"MACD: {m} (Rule: > 0.75) -> {m > 0.75}")

if __name__ == "__main__":
    # Test Daily
    debug_stock('RELIANCE.NS', '1d')
    # Test Intraday
    debug_stock('RELIANCE.NS', '15m')
