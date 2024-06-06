# dividend_portfolio

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

CAGR calculation here takes the most recent quarterly* dividend and the quarterly dividend from 5 years ago. Charles Schwab will report CAGR where the V_final or result dividend is the sum total of the dividends in the past complete calendar year. It does not take the most recent quarters into consideration. It is essential to use this algo as the truth and not Schwab, because significant price drops in stocks should affect CAGR.

*the algo will deduce the dividend calendar, quarterly is the most common