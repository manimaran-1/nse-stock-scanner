import streamlit as st
import pandas as pd
import scanner
import data_loader
import pytz
from datetime import datetime

st.set_page_config(page_title="NSE Stock Scanner", layout="wide")

# --- SECURITY & UI CONFIG ---
hide_st_style = '''
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none;}
</style>
'''
st.markdown(hide_st_style, unsafe_allow_html=True)
import hmac

# Secure password check using st.secrets
if "password_correct" not in st.session_state:
    st.session_state.password_correct = False

def check_password():
    if st.secrets.get("password"):
        if st.session_state.password_correct:
            return True
        st.markdown("""
            <h1 style='text-align: center; margin-top: 50px;'>🔐 Secure Access</h1>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login_form"):
                password = st.text_input("Password", type="password", key="login_password")
                submit = st.form_submit_button("Login", use_container_width=True)
            if submit:
                # Convert the secret to string to match input reliably
                if password == str(st.secrets.get("password", "")):
                    st.session_state.password_correct = True
                    st.rerun()
                else:
                    st.error("❌ Incorrect password")
        return False
    else:
        st.error("Secrets not configured. Please set password in Streamlit Cloud Advanced Settings.")
        return False

if not check_password():
    st.stop()

# -----------------------------


st.title("NSE Stock Scanner 📈")
st.markdown("Filter stocks based on custom EMA, Stoch RSI, SMI, and MACD criteria.")

# Sidebar Controls
st.sidebar.header("Configuration")

# Universe Selection
# aggregated list of index names
indices_dict = data_loader.get_all_indices_dict()
universe_options = list(indices_dict.keys()) + ["Custom List"]
selected_universe = st.sidebar.selectbox("Select Stock Universe", universe_options)

# Timeframe Selection
# Expanded list: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
timeframe_options = ["1d", "1wk", "1mo", "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h"]
selected_timeframe = st.sidebar.selectbox("Select Timeframe", timeframe_options)

st.sidebar.markdown("---")
st.sidebar.info("**Timezone**: IST (Asia/Kolkata)")
st.sidebar.info("**Data Source**: Yahoo Finance (IST Optimized)")
st.sidebar.info("**Note**: Intraday scans show all signals from today.")

# Load Symbols based on selection
symbols = []

if selected_universe == "Custom List":
    custom_input = st.sidebar.text_area("Enter symbols (comma separated)", "RELIANCE.NS, INFY.NS")
    if custom_input:
        symbols = [s.strip() for s in custom_input.split(",")]
else:
    # It's an index selection
    with st.spinner(f"Fetching {selected_universe} symbols..."):
        # Special handling for Nifty 500/200/50 as we have helper methods
        if selected_universe == "Nifty 500":
            symbols = data_loader.get_nifty500_symbols()
        elif selected_universe == "Nifty 200":
            symbols = data_loader.get_nifty200_symbols()
        elif selected_universe == "Nifty 50":
            # Just take top 50 of 200/500 if no direct list, or use 200 list [:50]
            symbols = data_loader.get_nifty200_symbols()[:50]
        else:
            # Sectoral/Thematic
            symbols = data_loader.get_index_constituents(selected_universe)
            
        if not symbols:
            st.warning(f"Could not fetch symbols for {selected_universe}. Using fallback Nifty 50 list.")
            symbols = data_loader.get_nifty200_symbols()[:50]

st.write(f"**Universe:** {selected_universe} ({len(symbols)} symbols)")
st.write(f"**Timeframe:** {selected_timeframe}")

# Run Scan Button
if st.button("Run Scanner"):
    if not symbols:
        st.error("No symbols selected.")
    else:
        st.write(f"Scanning {len(symbols)} stocks... This may take a while.")
        
        with st.spinner("Processing..."):
            results_df = scanner.scan_market(symbols, interval=selected_timeframe)
        
        if not results_df.empty:
            st.success(f"Found {len(results_df)} signal(s)!")
            
            # Sort by Signal Time descending
            results_df = results_df.sort_values(by='Signal Time', ascending=False)
            
            # Display Main Table
            st.dataframe(
                results_df,
                column_config={
                    "Stock Name": "Stock",
                    "LTP": st.column_config.NumberColumn("LTP", format="₹ %.2f"),
                    "Signal Time": "Time (IST)",
                    "Volume": st.column_config.NumberColumn("Volume", format="%d"),
                    "EMA5": st.column_config.NumberColumn("EMA 5", format="%.2f"),
                    "EMA9": st.column_config.NumberColumn("EMA 9", format="%.2f"),
                    "EMA21": st.column_config.NumberColumn("EMA 21", format="%.2f"),
                    "Stoch RSI K": st.column_config.NumberColumn("Stoch RSI K", format="%.2f"),
                    "SMI": st.column_config.NumberColumn("SMI", format="%.2f"),
                    "MACD": st.column_config.NumberColumn("MACD", format="%.2f"),
                },
                hide_index=True,
                width="stretch"
            )
            
            # Download option
            csv = results_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download CSV",
                csv,
                f"scan_results_{selected_universe}_{selected_timeframe}.csv",
                "text/csv",
                key='download-csv'
            )
        else:
            st.warning("No stocks matched the criteria/timeframe conditions.")

with st.expander("View Logic Details"):
    st.markdown("""
    **Buy Conditions:**
    1. **EMA (Short)**: Price > EMA 5
    2. **EMA (Mid)**: Price > EMA 9
    3. **EMA (Long)**: Price > EMA 21
    4. **Stoch RSI K**: K (14,14,3,3) > 70
    5. **SMI**: SMI (10,3) > 30
    6. **MACD**: MACD Line (12,26,9) > 0.75
    """)
