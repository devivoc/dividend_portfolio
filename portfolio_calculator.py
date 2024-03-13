import yfinance as yf
from datetime import datetime, timedelta
import pytz
import statistics

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
        dividends = stock.dividends
        dividends = filter_dividends_five_years(dividends)
        div_per_year = get_dividend_count_per_year(dividends)
        dividends = filter_dividends_four_months(dividends)
        if dividends.empty or div_per_year == 0:
            return 0.0
        
        current_price = stock.history(period='1d').iloc[-1]['Close']
        div_recent = dividends.iloc[-1]
        forward_dividend_yield = div_recent * div_per_year / current_price
        return forward_dividend_yield * 100
    except:
        print(sym, "error")
        return 0.0

def get_dividend_count_per_year(dividends):
    if len(dividends) < 4:
        return 0.0
    
    year_counts = {}

    for i in range(len(dividends)):
        year = dividends.index[i].year
        year_counts[year] = year_counts.get(year, 0) + 1

    per_year_avg = statistics.mode(year_counts.values())
    per_year = round(per_year_avg)
    if per_year != 4:
        x = 0

    return per_year

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
        dividends = stock.dividends
        
        dividends = filter_dividends_five_years(dividends)
        div_per_year = get_dividend_count_per_year(dividends) 

        if dividends.empty or div_per_year == 0:
            return 0.0
        
        if len(dividends) / div_per_year < 4:
            return 0.0
        
        # need to account for potential different dividend periods, so need to group dividends by year
        recent_div_year = sum(dividends.iloc[-div_per_year:])
        original_div_year = sum(dividends.iloc[:div_per_year])

        most_recent_div = dividends.iloc[-1]
        oldest_div = dividends.iloc[0]

        dividend_growth = (most_recent_div / oldest_div) ** (1 / (len(dividends)/div_per_year))
        return (dividend_growth - 1) * 100
    except:
        print(symbol, "Error")
        return 0.0
    
def write_sell_and_buy(buy_stocks, sell_stocks, hold_stocks):
    with open("buy_stocks.txt", 'w') as buystockFile:
        for symbol in buy_stocks:
            buystockFile.write(f"{symbol} - Fdv = {buy_stocks[symbol]['forward_div_yield']}% 5y d CAGR = {buy_stocks[symbol]['dividend_cagr']}%\n")

    with open("sell_stocks.txt", 'w') as sellstockFile:
        for symbol in sell_stocks:
            sellstockFile.write(f"{symbol} - Fdv = {sell_stocks[symbol]['forward_div_yield']}% 5y d CAGR = {sell_stocks[symbol]['dividend_cagr']}%\n")

    with open("hold_stocks.txt", 'w') as holdstockFile:
        for symbol in hold_stocks:
            holdstockFile.write(f"{symbol} - Fdv = {hold_stocks[symbol]['forward_div_yield']}% 5y d CAGR = {hold_stocks[symbol]['dividend_cagr']}%\n")

def recommend_stocks(symbols):
    stock_data = {}
    buy_stocks = {}
    sell_stocks = {}
    hold_stocks = {}
    for symbol in symbols:
        
        stock_data[symbol] = yf.Ticker(symbol).info
        # for some reason once isnt enough
        stock = yf.Ticker(symbol) 

        forward_div_yield = estimate_forward_dividend_yield(symbol)
        dividend_cagr = get_dividend_cagr(symbol)

        if forward_div_yield > 3 and dividend_cagr > 9.5:
            print(f"Buy {symbol}")
            buy_stocks[symbol] = {}
            buy_stocks[symbol]["forward_div_yield"] = forward_div_yield
            buy_stocks[symbol]["dividend_cagr"] = dividend_cagr
        elif forward_div_yield <= 1 or dividend_cagr < 5:
            print(f"Sell {symbol}")
            sell_stocks[symbol] = {}
            sell_stocks[symbol]["forward_div_yield"] = forward_div_yield
            sell_stocks[symbol]["dividend_cagr"] = dividend_cagr
        else:
            print(f"Hold {symbol}")
            hold_stocks[symbol] = {}
            hold_stocks[symbol]["forward_div_yield"] = forward_div_yield
            hold_stocks[symbol]["dividend_cagr"] = dividend_cagr
        print (f"Forward Dividend Yield: {forward_div_yield}%, 5-year Dividend CAGR: {dividend_cagr}%")

    write_sell_and_buy(buy_stocks, sell_stocks, hold_stocks)

# Read symbols from file and populate the list
symbols_file = 'symbols.txt'
symbols = []

with open(symbols_file, 'r') as file:
    for line in file:
        symbols.append(line.strip())

recommend_stocks(symbols)


