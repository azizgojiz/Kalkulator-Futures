import streamlit as st

st.set_page_config(page_title="Kalkulator Futures", page_icon="📊", layout="centered")

st.title("📊 Kalkulator Futures")

tab_leverage, tab_pnl = st.tabs(["📈 Kalkulator Leverage", "💹 Kalkulator PnL"])

# =========================================================
# TAB 1: KALKULATOR LEVERAGE (dari kalkulator-futures-main)
# =========================================================
with tab_leverage:

    def risk_based_futures_calculator(entry_price, target_price, stoploss_price, margin, max_loss, position_type='long'):
        risk_per_unit = abs(entry_price - stoploss_price)
        if risk_per_unit == 0:
            return {"error": "SL tidak boleh sama dengan entry (risk per unit = 0)."}

        coin_amount = max_loss / risk_per_unit
        position_size = coin_amount * entry_price
        leverage = position_size / margin

        if position_type == 'long':
            profit = (target_price - entry_price) * coin_amount
        elif position_type == 'short':
            profit = (entry_price - target_price) * coin_amount
        else:
            return {"error": "Tipe posisi salah. Gunakan 'long' atau 'short'."}

        return {
            "Profit jika TP tercapai": round(profit, 2),
            "Kerugian jika SL tercapai": round(max_loss, 2),
            "Leverage (x)": f"{round(leverage, 2)}x",
            "Jumlah koin": round(coin_amount, 2),
            "Ukuran posisi (USD)": round(position_size, 2)
        }

    st.header("📈 Kalkulator Leverage")

    with st.form("leverage_form"):
        position_type = st.selectbox("Pilih posisi", ["long", "short"], key="lev_position")
        entry_price = st.number_input("Harga Entry", value=0.01385, format="%.8f", key="lev_entry")
        target_price = st.number_input("Target (TP)", value=0.0162, format="%.8f", key="lev_tp")
        stoploss_price = st.number_input("Stop Loss (SL)", value=0.013385, format="%.8f", key="lev_sl")
        margin = st.number_input("Margin (USD)", value=30.0, key="lev_margin")
        max_loss = st.number_input("Toleransi Kerugian Maksimum (USD)", value=6.2, key="lev_maxloss")

        submitted = st.form_submit_button("Hitung")

    if submitted:
        result = risk_based_futures_calculator(
            entry_price, target_price, stoploss_price, margin, max_loss, position_type
        )

        st.subheader("📊 Hasil Perhitungan")
        if "error" in result:
            st.error(result["error"])
        else:
            for key, val in result.items():
                st.write(f"**{key}**: ${val}")

# =========================================================
# TAB 2: KALKULATOR PnL (dari kalkulator-futures-PnL-main)
# =========================================================
with tab_pnl:

    def futures_pnl_calculator(entry_price, target_price, stoploss_price, margin, leverage, position_type='long'):
        position_size = margin * leverage
        coin_amount = position_size / entry_price

        if position_type == 'long':
            profit = (target_price - entry_price) * coin_amount
            loss = (entry_price - stoploss_price) * coin_amount
        elif position_type == 'short':
            profit = (entry_price - target_price) * coin_amount
            loss = (stoploss_price - entry_price) * coin_amount
        else:
            return {"error": "Invalid position type. Use 'long' or 'short'."}

        return {
            "Profit jika TP tercapai": round(profit, 2),
            "Kerugian jika SL kena": round(loss, 2),
            "Ukuran Posisi (USDT)": round(position_size, 2),
            "Jumlah Koin": round(coin_amount, 6)
        }

    st.header("💹 Kalkulator PnL")

    entry = st.number_input("📍 Entry Price", value=0.01, step=0.0001, format="%.10f", key="pnl_entry")
    tp = st.number_input("🎯 Target Price (TP)", value=0.02, step=0.0001, format="%.10f", key="pnl_tp")
    sl = st.number_input("🛑 Stop Loss (SL)", value=0.009, step=0.0001, format="%.10f", key="pnl_sl")
    margin_pnl = st.number_input("💰 Margin (USDT)", value=10.0, step=1.0, key="pnl_margin")
    leverage_pnl = st.number_input("📈 Leverage (X)", value=10.0, step=1.0, key="pnl_leverage")
    position_pnl = st.selectbox("📊 Jenis Posisi", ['long', 'short'], key="pnl_position")

    if st.button("🔍 Hitung", key="pnl_button"):
        result = futures_pnl_calculator(entry, tp, sl, margin_pnl, leverage_pnl, position_pnl)
        st.subheader("📋 Hasil Perhitungan:")
        for k, v in result.items():
            st.write(f"**{k}**: {v}")
