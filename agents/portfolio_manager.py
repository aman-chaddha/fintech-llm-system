import json
import streamlit as st


# Load portfolio data from JSON file
def load_portfolio(username):
    try:
        with open(f'data/portfolio_data.json', 'r') as f:
            data = json.load(f)
            return data.get(username, {})
    except FileNotFoundError:
        return {}


# Save portfolio data to JSON file
def save_portfolio(username, portfolio_data):
    try:
        with open('data/portfolio_data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    data[username] = portfolio_data

    with open('data/portfolio_data.json', 'w') as f:
        json.dump(data, f)


# Example function to display and manage portfolio
def display_portfolio():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        username = st.session_state.username

        # Fetch user's portfolio
        portfolio = load_portfolio(username)

        # Display portfolio details
        if portfolio:
            st.subheader(f"{username}'s Portfolio")
            for stock, details in portfolio.items():
                st.write(f"{stock}: {details}")
        else:
            st.write("No portfolio data available.")

        # Option to add a new stock to the portfolio
        add_stock = st.text_input("Add stock to portfolio (e.g., AAPL, MSFT)")
        if st.button("Add Stock"):
            if add_stock:
                # Example: Adding stock price as a placeholder (you can extend this to include other details)
                portfolio[add_stock] = {"price": 150.00}
                save_portfolio(username, portfolio)
                st.success(f"Added {add_stock} to your portfolio.")

        # Option to remove a stock
        remove_stock = st.text_input("Remove stock from portfolio")
        if st.button("Remove Stock"):
            if remove_stock in portfolio:
                del portfolio[remove_stock]
                save_portfolio(username, portfolio)
                st.success(f"Removed {remove_stock} from your portfolio.")
            else:
                st.error(f"{remove_stock} not found in your portfolio.")
