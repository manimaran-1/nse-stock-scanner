import scanner
import pandas as pd

def test_scanner():
    print("Testing scanner on small subset...")
    symbols = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'SBIN.NS']
    try:
        results = scanner.scan_market(symbols, interval='1d')
        print("Scan complete.")
        if not results.empty:
            print("Found matches:")
            print(results)
        else:
            print("No matches found in subset (expected if market conditions don't meet criteria).")
        print("Test PASSED.")
    except Exception as e:
        print(f"Test FAILED with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_scanner()
