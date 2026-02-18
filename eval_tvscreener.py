from tvscreener import StockScreener, StockField

def evaluate():
    print("Evaluating tvscreener capabilities...")
    
    # 1. Search for SMI fields
    smi_fields = StockField.search("smi")
    print(f"Found {len(smi_fields)} SMI-related fields:")
    for f in smi_fields:
        print(f"  - {f}")
        
    # 2. Search for Stoch RSI fields
    stoch_fields = StockField.search("stoch")
    print(f"\nFound {len(stoch_fields)} Stoch-related fields (first 5):")
    for f in stoch_fields[:5]:
        print(f"  - {f}")

    # 3. Try to fetch data for RELIANCE
    # Assuming we can filter by symbol to get just one
    ss = StockScreener()
    # We can try to use standard filters if possible, but let's just get top 5 to see structure
    df = ss.get()
    print(f"\nFetched {len(df)} rows. Columns: {df.columns.tolist()[:10]}...")
    
    # Check if we can get historical data (unlikely based on docs, but checking method availability)
    print("\nChecking for history methods...")
    print(f"Has history method? {'history' in dir(ss)}")
    
if __name__ == "__main__":
    evaluate()
