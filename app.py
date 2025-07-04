import numpy as np
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Real Estate ROI Dashboard", layout="wide")

# --- Sidebar Inputs ---
st.sidebar.header("Investment Assumptions")

initial_investment = st.sidebar.slider("Initial Investment (TL)", 1_000_000, 10_000_000, 2_500_000, step=250_000)
monthly_rent = st.sidebar.slider("Initial Monthly Rent (TL)", 5_000, 50_000, 20_000, step=1_000)
rent_increase = st.sidebar.slider("Rent Increase Every 6 Months (%)", 0.0, 0.5, 0.15, step=0.01)

months = 24
month_labels = [f"M{i+1}" for i in range(months)]

# --- Editable Inputs for Interest and FX ---
default_annual_rates = [0.50]*6 + [0.40]*6 + [0.30]*6 + [0.25]*6
default_dollar_rates = [
    39.0, 39.2, 39.5, 39.8, 40.1, 40.4,
    40.6, 41.0, 41.3, 41.6, 42.0, 42.4,
    42.8, 43.1, 43.5, 43.8, 44.1, 44.4,
    44.7, 45.0, 45.2, 45.5, 45.7, 46.0
]

editable_df = pd.DataFrame({
    "Month": month_labels,
    "Annual Interest Rate (%)": [r * 100 for r in default_annual_rates],
    "Dollar Rate (TL/USD)": default_dollar_rates
})

st.sidebar.markdown("📊 **Adjust Interest and FX Expectations**")
edited_df = st.sidebar.data_editor(
    editable_df,
    use_container_width=True,
    hide_index=True,
    num_rows="fixed"
)

# Convert edited data to arrays
annual_rates = np.array(edited_df["Annual Interest Rate (%)"]) / 100
dollar_rates = np.array(edited_df["Dollar Rate (TL/USD)"])


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
    margin=dict(t=30, b=30, l=10, r=10),
    font=dict(size=12)
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
    margin=dict(t=30, b=30, l=10, r=10),
    font=dict(size=12)
)

# --- Streamlit Layout ---
st.title("🏘️ ROI Simulator")
st.subheader("Ev Almak vs Parayi Faize Koymak")

st.markdown(f"""
**💰 Summary:**
- Initial Investment: `{initial_investment:,.0f}` TL  
- Avg. Interest Rate: `{avg_interest_annual:.2f}%`  
- Avg. Monthly Rent: `{avg_monthly_rent:,.0f}` TL  
- Avg. Dollar Rate: `{avg_dollar_rate:.2f}` TL/USD  
- Rent Increase Every 6 Months: `{int(rent_increase*100)}%`
""")

st.plotly_chart(fig_tl, use_container_width=True)
st.plotly_chart(fig_usd, use_container_width=True)

st.markdown("---")
# Data table
rates_df = pd.DataFrame({
    "Month": month_labels,
    "Annual Interest Rate": [f"{rate*100:.2f}%" for rate in annual_rates],
    "Dollar Rate (TL/USD)": dollar_rates
})

st.markdown("---")
st.subheader("📉 Scenario Inputs by Month")
st.dataframe(rates_df.style.format(precision=2), use_container_width=True)

# Interest Rate Trend
fig_rate = go.Figure()
fig_rate.add_trace(go.Scatter(
    x=month_labels,
    y=annual_rates * 100,
    line=dict(color="orange"),
    name="Annual Interest Rate (%)",
    mode="lines+markers",
    marker=dict(size=6)
))
fig_rate.update_layout(
    title="Annual Interest Rate by Month",
    xaxis_title="Month",
    yaxis_title="Interest Rate (%)",
    height=350
)
st.plotly_chart(fig_rate, use_container_width=True)

# Dollar Rate Trend
fig_fx = go.Figure()
fig_fx.add_trace(go.Scatter(
    x=month_labels,
    y=dollar_rates,
    line=dict(color="green"),
    name="Dollar Rate (TL/USD)",
    mode="lines+markers",
    marker=dict(size=6)
))
fig_fx.update_layout(
    title="Expected Dollar Exchange Rate by Month",
    xaxis_title="Month",
    yaxis_title="TL per USD",
    height=350
)
st.plotly_chart(fig_fx, use_container_width=True)
