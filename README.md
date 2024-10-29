# dividend_portfolio

*** Disclaimer: This is not financial advice, it is a personal project

Strategy: 


Dividend Growth Portfolio

via Austin Hankwitz

Buy Rules

1) Buy a stock if its forward dividend yield is above 3% (twice the snp500 average)

AND

2) If its 5-year dividend CAGR is above 9.5%



Sell Rules

1) Sell the stock if its forward dividend yield drops to or below 1%

OR

2) If the stock's 5-year dividend compounded annual growth rate drops below 5%

OR 

3) The stock drops out of the S&P 500

* Only buy stocks within the S&P 500
* Rebalance every 8 weeks

Notes:

CAGR calculation here takes into account the most recent quarterly* dividends. For example, if we are in Q3, the CAGR calculation will include Y4Q3-Y5Q2. Charles Schwab will report CAGR where the V_final/result dividend is the sum total of the dividends in the past COMPLETE CALENDAR year (so Y4Q1-Y4Q4). It does not take the most recent quarters into consideration. This algo is used as the source of truth and not Schwab, because recent price changes in stocks should affect CAGR.

*the algo will deduce the dividend calendar, quarterly is the most common

Some stocks in the position were purchased March 17 2024 due to research using the Charles Schwab research tool. I found this to be unhelpful due to the above note, but since they have not since reached the criteria of sell, they will remain in the portfolio