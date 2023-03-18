import datetime
import yfinance as yf
import plotly.express as px
import pandas as pd

# Function to fetch historical exchange rates
def get_historical_rates(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)
    return data["Adj Close"]

# Fetch historical rates
start_date = datetime.date(2019, 1, 1)
end_date = datetime.date.today()
rates = get_historical_rates("HUF=X, EURHUF=X, GBP=X, AUD=X", start_date, end_date)

# Normalize rates
normalized_rates = []
for _, row in rates.iterrows():
    total = row['HUF=X'] + row['EURHUF=X'] + 1 + row['GBP=X'] + row['AUD=X']
    normalized_rates.append({
        'HUF': 1 / total,
        'USD': row['HUF=X'] / total,
        'EUR': row['EURHUF=X'] / total,
        'GBP': row['GBP=X'] / total,
        'AUD': row['AUD=X'] / total,
    })

# Convert end_date to Timestamp
end_date = pd.Timestamp(end_date)

# Calculate the number of days from today for each date
days_from_today = [(end_date - date).days for date in rates.index]

# Create a parallel coordinates plot
fig = px.parallel_coordinates(
    normalized_rates,
    dimensions=['HUF', 'USD', 'EUR', 'GBP', 'AUD'],
    labels={'HUF': 'HUF', 'USD': 'USD', 'EUR': 'EUR', 'GBP': 'GBP', 'AUD': 'AUD'},
    color=days_from_today,
    color_continuous_scale=px.colors.sequential.Viridis,
    color_continuous_midpoint=days_from_today[int(len(days_from_today) / 2)],
)

fig.update_layout(
    title="Historical Exchange Rates (2019-1-1 to Today)",
    font=dict(size=14),
)

fig.show()
