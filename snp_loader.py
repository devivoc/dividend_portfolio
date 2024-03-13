import yfinance as yf
import pandas as pd

# Download the S&P 500 index components from Wikipedia
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
tables = pd.read_html(url)
sp500_df = tables[0]

# Extract the stock symbols from the dataframe
symbols = sp500_df['Symbol'].tolist()

with open("symbols.txt", 'w') as symbolsOut:
    for symbol in symbols:
        symbolsOut.write(f"{symbol}\n")

# Create a dictionary to store the stock data
stock_data = {}

# Loop through each symbol and fetch the stock data using yfinance
for symbol in symbols:
    try:
        stock_data[symbol] = yf.Ticker(symbol).info
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")

# Display the stock data (you can customize this part based on your requirements)
for symbol, data in stock_data.items():
    print(f"Symbol: {symbol}, Company: {data.get('longName', 'N/A')}, Industry: {data.get('industry', 'N/A')}")
