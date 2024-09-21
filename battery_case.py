import streamlit as st
import numpy as np
import plotly.graph_objs as go
from numpy_financial import irr, npv

def calculate_irr_npv(cash_flows, rate):
    # Calculate Internal Rate of Return (IRR)
    internal_rate_of_return = irr(cash_flows) if len(cash_flows) > 0 else 0
    # Calculate Net Present Value (NPV)
    net_present_value = npv(rate, cash_flows) if len(cash_flows) > 0 else 0
    return internal_rate_of_return, net_present_value

def calculate_annual_cash_flow(j_return, battery_size, cost_per_kWh, time_period, pooler_cut, c_rate, invest_grid):
    # Calculate the initial investment
    initial_investment = -battery_size * cost_per_kWh - invest_grid
    # Calculate the net annual return after Pooler Cut
    net_annual_return = j_return / 100 * c_rate * battery_size * (1 - pooler_cut / 100)
    # List of cash flows starting with the initial investment
    cash_flows = [initial_investment] + [net_annual_return for _ in range(time_period)]
    return cash_flows

def main():
    st.sidebar.image("MOTICS_LOGO-01.png", use_column_width=True)
    st.sidebar.title("Einstellungen")
    # Collecting user input from the sidebar 
    battery_size = st.sidebar.slider("Batteriegroesse (kWh)", 100, 1500, 800)
    c_rate = st.sidebar.slider("C-rate", 0.25, 1.5, 0.25, 0.25)
    invest_grid = st.sidebar.slider("Invest Netz", 0, 300000, 0, 10000)
    j_return = st.sidebar.slider("Return pro 100 kW (CHF)", 5000, 30000, 12500,2500)
    cost_per_kWh = st.sidebar.slider("Kosten pro kWh (CHF)", 100, 800, 250, 50)
    pooler_cut = st.sidebar.slider("Pooler Cut (%)", 0, 35, 20)
    rate_of_return = st.sidebar.slider("Rendite (%)", 0.0, 15.0, 7.5, step=0.1) / 100
    time_period = st.sidebar.slider("Betrachtungszeitraum (Jahre)", 0, 10, 5)

    if time_period > 0:
        cash_flows = calculate_annual_cash_flow(j_return, battery_size, cost_per_kWh, time_period, pooler_cut, c_rate, invest_grid)
        irr_value, npv_value = calculate_irr_npv(cash_flows, rate_of_return)
        
        # Calculate cumulative cash flow
        cumulative_cash_flows = np.cumsum(cash_flows)
        
        # Determine color based on values
        irr_color = "normal" if irr_value >= 0 else "inverse"
        npv_color = "normal" if npv_value >= 0 else "inverse"
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Interne Rendite (IRR)", value=f"{irr_value * 100:.2f} %", delta=None, delta_color=irr_color)
        with col2:
            st.metric(label="Netto-Gegenwartswert (NPV)", value=f"CHF {npv_value:.2f}", delta=None, delta_color=npv_color)
        
        # Creating a plot using Plotly
        fig = go.Figure()

        # Plotting annual cash flow
        fig.add_trace(go.Scatter(x=list(range(-1, time_period)), y=cash_flows, mode='lines+markers', name='Annual Cash Flow'))

        # Plotting cumulative cash flow
        fig.add_trace(go.Scatter(x=list(range(-1, time_period)), y=cumulative_cash_flows, mode='lines+markers', name='Cumulative Cash Flow'))

        fig.update_layout(title='Annual and Cumulative Cash Flow Over Time', xaxis_title='Years', yaxis_title='Cash Flow (CHF)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Bitte waehlen Sie einen Betrachtungszeitraum groesser als 0 Jahre.")

if __name__ == "__main__":
    main()
