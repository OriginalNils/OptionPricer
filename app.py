import streamlit as st
import numpy as np
from scipy.stats import norm

# --- 1. The Black-Scholes Calculation Function ---
def black_scholes(S, K, T, r, sigma):
    """
    Calculates the price of European Call and Put options.
    
    S: Current stock price
    K: Strike price
    T: Time to expiration (in years)
    r: Risk-free interest rate (as a decimal)
    sigma: Volatility (as a decimal)
    """
    # d1 and d2 calculations
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # N(d1) and N(d2) using the cumulative distribution function (CDF)
    N_d1 = norm.cdf(d1)
    N_d2 = norm.cdf(d2)
    
    # N(-d1) and N(-d2) for the Put option
    N_minus_d1 = norm.cdf(-d1)
    N_minus_d2 = norm.cdf(-d2)
    
    # Calculate Call and Put prices
    call_price = (S * N_d1 - K * np.exp(-r * T) * N_d2)
    put_price = (K * np.exp(-r * T) * N_minus_d2 - S * N_minus_d1)
    
    return call_price, put_price

# --- 2. The Streamlit Web App ---

st.set_page_config(page_title="Option Pricer", layout="centered")
st.title("Black-Scholes Option Price Calculator 🧮")

# --- Sidebar for User Inputs ---
st.sidebar.header("Input Parameters")

S = st.sidebar.number_input("Current Stock Price (S)", min_value=1.0, value=100.0, step=0.5)
K = st.sidebar.number_input("Strike Price (K)", min_value=1.0, value=100.0, step=0.5)
T_days = st.sidebar.slider("Time to Expiration (Days)", min_value=1, max_value=365, value=90)
r = st.sidebar.slider("Risk-Free Interest Rate (r %)", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
sigma = st.sidebar.slider("Annual Volatility (σ %)", min_value=1.0, max_value=100.0, value=20.0, step=0.5)

# --- Convert inputs to the format required by the formula ---
T_years = T_days / 365.0
r_decimal = r / 100
sigma_decimal = sigma / 100

# --- Main Panel for Displaying Results ---
st.header("Results")

if st.button("Calculate Option Prices"):
    if T_years == 0 or sigma_decimal == 0:
        st.error("Time to Expiration and Volatility must be greater than zero.")
    else:
        call_result, put_result = black_scholes(S, K, T_years, r_decimal, sigma_decimal)

        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Price of Call Option",
                value=f"€ {call_result:,.4f}"
            )
        
        with col2:
            st.metric(
                label="Price of Put Option",
                value=f"€ {put_result:,.4f}"
            )
        
        st.info("This calculator is for European options and does not account for dividends.")