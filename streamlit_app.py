import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter


def calculate_cost(monthly_users, price_0_to_100=0, price_101_to_500=9.30, price_501_to_1000=5.00,
                   price_1001_to_2000=3.50, price_above_2000=2.25):
    if monthly_users <= 100:
        total = monthly_users * price_0_to_100
    elif monthly_users <= 500:
        total = 100 * price_0_to_100 + (monthly_users - 100) * price_101_to_500
    elif monthly_users <= 1000:
        total = 100 * price_0_to_100 + 400 * price_101_to_500 + (monthly_users - 500) * price_501_to_1000
    elif monthly_users <= 2000:
        total = 100 * price_0_to_100 + 400 * price_101_to_500 + 500 * price_501_to_1000 + (
                    monthly_users - 1000) * price_1001_to_2000
    else:
        total = 100 * price_0_to_100 + 400 * price_101_to_500 + 500 * price_501_to_1000 + 1000 * price_1001_to_2000 + (
                    monthly_users - 2000) * price_above_2000
    return total, total * 12


def calculate_price(cost, profit_margin_percent):
    return cost + (cost * profit_margin_percent / 100)


def dollars(x, pos):
    'The two args are the value and tick position'
    return f'${x:.2f}'


st.title('Looker Embed Cost/Pricing Model')

# Display table with pricing tiers
st.write("""
| Monthly Users | Cost |
|---------------|------|
| 0 - 100       | $0.00 |
| 101 - 500     | $9.30 |
| 501 - 1000    | $5.00 |
| 1001 - 2000   | $3.50 |
| 2000+         | $2.25 |
""")

# User input for monthly users and profit margin
monthly_users = st.number_input('Enter the number of monthly users', min_value=0)
profit_margin = st.slider('Select the profit margin (%)', min_value=0, max_value=200)

# Calculate monthly and annualized cost
monthly_cost, annualized_cost = calculate_cost(monthly_users)
st.write(f"Monthly cost: ${monthly_cost:.2f}")
st.write(f"Annualized cost: ${annualized_cost:.2f}")

# Calculate price with profit margin
price_with_profit_margin = calculate_price(monthly_cost, profit_margin)
st.write(f"Price per user with a {profit_margin}% profit margin: ${price_with_profit_margin:.2f}")

# Generate a range of monthly users for plot
users = np.arange(0, 3000, 50)

# Calculate costs and prices for each number of users
costs = [calculate_cost(u)[0] for u in users]
prices = [calculate_price(cost, profit_margin) for cost in costs]

# Plot the results
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(users, costs, label='Cost')
ax.plot(users, prices, label='Price with Profit Margin')

# Add vertical line to highlight the estimated
ax.axvline(x=monthly_users, color='r', linestyle='--', label=f'Estimated Monthly Users: {monthly_users}')

ax.legend()

# Format y axis as dollars
formatter = FuncFormatter(dollars)
ax.yaxis.set_major_formatter(formatter)

plt.xlabel('Monthly Users')
plt.ylabel('Cost/Price')
plt.title('Cost and Price as a Function of Monthly Users')
plt.grid(True)
st.pyplot(fig)
