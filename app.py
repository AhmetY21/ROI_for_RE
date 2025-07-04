import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Real Estate ROI Dashboard", layout="wide")

# --- Sidebar Inputs ---
st.sidebar.header("Investment Assumptions")

initial_investment = st.sidebar.slider("Initial Investment (TL)", 1_000_000, 10_000_000, 2_500_000, step=250_000)
monthly_rent = st.sidebar.slider("Initial Monthly Rent (TL)", 5_000, 50_000, 20_000, step=1_000)
rent_increase = st.sidebar.slider("Rent Increase Every 6 Months (%)", 0.0, 0.5, 0.15, step=0.01)

months = 24
month_labels = [f"M{i+1}" for i in range(months)]

# --- Interest and FX Assumptions ---
annual_rates = np.array([0.50]*6 + [0.40]*6 + [0.30]*6 + [0.25]*6)
dollar_rates = np.array([
    39.0, 39.2, 39.5, 39.8, 40.1, 40.4,
    40.6, 41.0, 41.3, 41.6, 42.0, 42.4,
    42.8, 43.1, 43.5, 43.8, 44.1, 44.4,
    44.7, 45.0, 45.2, 45.5, 45.7, 46.0
])

# --- Rent Schedule ---
rents = []
current_rent = monthly_rent
for i in range(months):
    if i > 0 and i % 6 == 0:
        current_rent *= (1 + rent_increase)
    rents.append(current_rent)
rents = np.array(rents)

# --- Interest Income ---
monthly_rates = (1 + annual_rates)**(1/12) - 1
interest_income = initial_investment * monthly_rates

# --- USD Conversion ---
rents_usd = rents / dollar_rates
interest_usd = interest_income / dollar_rates

# --- Summary Stats ---
avg_interest_annual = np.mean(annual_rates) * 100
avg_dollar_rate = np.mean(dollar_rates)
avg_monthly_rent = np.mean(rents)

# --- Plot 1: TL View ---
fig_tl = go.Figure()
fig_tl.add_trace(go.Bar(x=month_labels, y=rents, name="Rent Income (TL)", marker_color="royalblue"))
fig_tl.add_trace(go.Bar(x=month_labels, y=interest_income, name="Interest Income (TL)", marker_color="orange"))

fig_tl.update_layout(
    title="Monthly Rent vs Interest Income (in TL)",
    xaxis_title="Month",
    yaxis_title="Income (TL)",
    barmode='group',
    height=450,
    annotations=[
        dict(
            text=(
                f"<b>Investment:</b> {initial_investment:,.0f} TL<br>"
                f"<b>Avg Annual Interest:</b> {avg_interest_annual:.1f}%<br>"
                f"<b>Avg Rent:</b> {avg_monthly_rent:,.0f} TL<br>"
                f"<b>Rent Increase:</b> {int(rent_increase * 100)}%<br>"
                f"<b>Avg Dollar Rate:</b> {avg_dollar_rate:.2f}"
            ),
            showarrow=False,
            xref="paper", yref="paper",
            x=0.95, y=0.95,
            bordercolor="gray", borderwidth=1,
            bgcolor="lightyellow", opacity=0.8
        )
    ]
)

# --- Plot 2: USD View ---
fig_usd = go.Figure()
fig_usd.add_trace(go.Bar(x=month_labels, y=rents_usd, name="Rent Income (USD)", marker_color="seagreen"))
fig_usd.add_trace(go.Bar(x=month_labels, y=interest_usd, name="Interest Income (USD)", marker_color="tomato"))

fig_usd.update_layout(
    title="Monthly Rent vs Interest Income (in USD)",
    xaxis_title="Month",
    yaxis_title="Income (USD)",
    barmode='group',
    height=450,
    annotations=[
        dict(
            text=(
                f"<b>Investment:</b> {initial_investment:,.0f} TL<br>"
                f"<b>Avg Dollar Rate:</b> {avg_dollar_rate:.2f}<br>"
                f"<b>Rent Increase:</b> {int(rent_increase * 100)}%"
            ),
            showarrow=False,
            xref="paper", yref="paper",
            x=0.95, y=0.95,
            bordercolor="gray", borderwidth=1,
            bgcolor="lavenderblush", opacity=0.8
        )
    ]
)

# --- Streamlit Layout ---
st.title("🏘️ Real Estate ROI Simulator")
st.subheader("Visualize and Compare Rental Income vs Interest Earnings")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_tl, use_container_width=True)
with col2:
    st.plotly_chart(fig_usd, use_container_width=True)

st.markdown("---")
st.markdown("📈 Use the sliders in the sidebar to explore different investment scenarios.")

