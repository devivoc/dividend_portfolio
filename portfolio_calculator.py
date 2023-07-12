import yfinance as yf
from datetime import datetime, timedelta
import pytz

def get_dividend_data(symbols):
    dividend_data = {}

    for symbol in symbols:
        stock = yf.Ticker(symbol)
        dividend_history = stock.dividends
        dividend_data[symbol] = dividend_history

    return dividend_data

def estimate_forward_dividend_yield(sym):
    stock = yf.Ticker(sym)

    try:
        dividends = filter_dividends_four_months(stock.dividends)
        if dividends.empty:
            return 0.0
        
        current_price = stock.history(period='1d').iloc[-1]['Close']
        forward_dividend_yield = dividends.iloc[-1] * 4 / current_price
        return forward_dividend_yield * 100
    except:
        print(sym, "error")

def filter_dividends_four_months(dividends):
    today = datetime.now(pytz.timezone('America/New_York'))
    four_months_ago = today - timedelta(days=4 * 30)

    filtered_dividends = dividends[dividends.index >= four_months_ago]
    return filtered_dividends

def filter_dividends_five_years(dividends):
    today = datetime.now(pytz.timezone('America/New_York'))
    five_years_ago = today - timedelta(days=365 * 5)

    filtered_dividends = dividends[dividends.index >= five_years_ago]
    return filtered_dividends

def get_dividend_cagr(symbol):
    stock = yf.Ticker(symbol)
    try:
        dividends = filter_dividends_five_years(stock.dividends)
        if len(dividends) < 2:
            return 0.0
        dividend_growth = (dividends.iloc[-1] / dividends.iloc[0]) ** (1 / (len(dividends)/4))
        return (dividend_growth - 1) * 100
    except:
        print(symbol, "Error")
        return 0.0

def recommend_stocks(symbols):

    for symbol in symbols:
        # for some reason once isnt enough
        stock = yf.Ticker(symbol) 

        forward_div_yield = estimate_forward_dividend_yield(symbol)
        dividend_cagr = get_dividend_cagr(symbol)

        if forward_div_yield > 3 and dividend_cagr > 10:
            print(f"Buy {symbol}%")
        elif forward_div_yield <= 1 or dividend_cagr < 5:
            print(f"Sell {symbol}%")

        print (f"Forward Dividend Yield: {forward_div_yield}%, 5-year Dividend CAGR: {dividend_cagr}%")
# Read symbols from file and populate the list
symbols_file = 'symbols.txt'
symbols = []

with open(symbols_file, 'r') as file:
    for line in file:
        symbols.append(line.strip())

recommend_stocks(symbols)


