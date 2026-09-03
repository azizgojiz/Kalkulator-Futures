import streamlit as st

st.set_page_config(
    page_title="Kalkulator Futures",
    page_icon=":material/query_stats:",
    layout="wide",
)

"""
# :material/query_stats: Kalkulator Futures

Hitung leverage yang pas atau proyeksi PnL sebelum masuk posisi.
"""

""  # spacer

tab_leverage, tab_pnl = st.tabs(["📈 Kalkulator Leverage", "💹 Kalkulator PnL"])


def position_selector(state_key):
    """Segmented long/short buttons that stretch to fill the card width."""
    if state_key not in st.session_state:
        st.session_state[state_key] = "long"

    c1, c2 = st.columns(2)
    if c1.button(
        "long",
        key=f"{state_key}_btn_long",
        type="primary" if st.session_state[state_key] == "long" else "secondary",
        use_container_width=True,
    ):
        st.session_state[state_key] = "long"
    if c2.button(
        "short",
        key=f"{state_key}_btn_short",
        type="primary" if st.session_state[state_key] == "short" else "secondary",
        use_container_width=True,
    ):
        st.session_state[state_key] = "short"

    return st.session_state[state_key]


# =========================================================
# TAB 1: KALKULATOR LEVERAGE
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
            "profit": round(profit, 2),
            "loss": round(max_loss, 2),
            "leverage": round(leverage, 2),
            "coins": round(coin_amount, 2),
            "position_size": round(position_size, 2),
        }

    cols = st.columns([1, 1.4])

    input_cell = cols[0].container(border=True)
    with input_cell:
        st.markdown("**Input posisi**")
        position_type = position_selector("lev_position")
        entry_price = st.number_input("Harga Entry", value=0.01385, format="%.8f", key="lev_entry")
        target_price = st.number_input("Target (TP)", value=0.0162, format="%.8f", key="lev_tp")
        stoploss_price = st.number_input("Stop Loss (SL)", value=0.013385, format="%.8f", key="lev_sl")
        margin = st.number_input("Margin (USD)", value=1000.0, key="lev_margin")
        max_loss = st.number_input("Toleransi Kerugian Maksimum (USD)", value=500.0, key="lev_maxloss")

    result_cell = cols[1].container(border=True, height="stretch")
    with result_cell:
        st.markdown("**Hasil perhitungan**")
        result = risk_based_futures_calculator(
            entry_price, target_price, stoploss_price, margin, max_loss, position_type
        )

        if "error" in result:
            st.error(result["error"])
        else:
            m1, m2 = st.columns(2)
            m1.metric("Leverage", f"{result['leverage']}x")
            m2.metric("Ukuran posisi (USD)", f"${result['position_size']:,}")

            m3, m4 = st.columns(2)
            m3.metric("Profit jika TP tercapai", f"${result['profit']:,}")
            m4.metric("Kerugian jika SL tercapai", f"${result['loss']:,}")

            m5, m6 = st.columns(2)
            m5.metric("Jumlah koin", f"{result['coins']:,}")

# =========================================================
# TAB 2: KALKULATOR PnL
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
            "profit": round(profit, 2),
            "loss": round(loss, 2),
            "position_size": round(position_size, 2),
            "coins": round(coin_amount, 6),
        }

    cols = st.columns([1, 1.4])

    input_cell = cols[0].container(border=True)
    with input_cell:
        st.markdown("**Input posisi**")
        position_pnl = position_selector("pnl_position")
        entry = st.number_input("Entry Price", value=0.01, step=0.0001, format="%.10f", key="pnl_entry")
        tp = st.number_input("Target Price (TP)", value=0.02, step=0.0001, format="%.10f", key="pnl_tp")
        sl = st.number_input("Stop Loss (SL)", value=0.009, step=0.0001, format="%.10f", key="pnl_sl")
        margin_pnl = st.number_input("Margin (USDT)", value=1000.0, step=1.0, key="pnl_margin")
        leverage_pnl = st.number_input("Leverage (X)", value=5.0, step=1.0, key="pnl_leverage")

    result_cell = cols[1].container(border=True, height="stretch")
    with result_cell:
        st.markdown("**Hasil perhitungan**")
        result = futures_pnl_calculator(entry, tp, sl, margin_pnl, leverage_pnl, position_pnl)

        if "error" in result:
            st.error(result["error"])
        else:
            m1, m2 = st.columns(2)
            m1.metric("Profit jika TP tercapai", f"${result['profit']:,}")
            m2.metric("Kerugian jika SL kena", f"${result['loss']:,}")

            m3, m4 = st.columns(2)
            m3.metric("Ukuran Posisi (USDT)", f"${result['position_size']:,}")
            m4.metric("Jumlah Koin", f"{result['coins']:,}")
