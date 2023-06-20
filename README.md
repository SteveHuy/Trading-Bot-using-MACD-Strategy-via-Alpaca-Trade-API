# Trading Bot using MACD Strategy via Alpaca Trade API
This is a trading bot using the Alpaca Trade API which uses the MACD Strategy.
The MACD line is (12 - day EMA - 26 day EMA) and the signall line is the 9 day EMA of the MACD line.
The program can determine long and short signals in the chosen stocks. The code contains a dynamic backtesting tool which will pick a take-profit margin and stop-loss based on the winrate and money earned of the previous 5 years of market conditions. However, currently the code only makes Long Orders as shorting is a riskier strategy which requires more back testing.
This can be hosted on an Azure or AWS server to conduct schedule executions everyday placing orders based on the conditions of the market.

Furthermore, you can plot the past 5 years of market activity for a stock and look at when the long and short signals occur.
