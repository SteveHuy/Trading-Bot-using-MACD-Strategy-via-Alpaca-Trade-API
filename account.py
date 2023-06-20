import alpaca_trade_api as tradeapi
import datetime
from tabulate import tabulate


class Account:
    """
    Class representing the trading account.

    Attributes:
        api (tradeapi.REST): Alpaca Trade API object.
        account (tradeapi.entity.Account): Account information.

    Methods:
        get_account_info(): Get account information.
        get_account_balance(): Get the account balance.
        get_portfolio_value(): Get the portfolio value.
        get_positions(): Get the current positions.
        get_position(symbol): Get the position for a specific symbol.
        buy_stock(symbol, qty): Place a market buy order for a stock.
        sell_stock(symbol, qty): Place a market sell order for a stock.
        long_stock(symbol, qty, EMA, stop_loss_percentage, profit_ratio, notional): Place a long order for a stock with stop-loss and take-profit.
        get_qty(symbol): Get the quantity of a specific stock held.
        get_barset_day(symbol): Get the daily barset for a symbol.
        get_barset_day_close(symbol): Get the closing prices from the daily barset for a symbol.
        get_barset_day_close_and_date(symbol): Get the closing prices and dates from the daily barset for a symbol.
     """

    def __init__(self, api_key: str, secret_key: str, base_url: str):
        """
        Initialize the Account object with Alpaca Trade API credentials.

        Args:
            api_key (str): Alpaca API key.
            secret_key (str): Alpaca secret key.
            base_url (str): Alpaca base URL.

        Returns:
            None.
        """
        self.api = tradeapi.REST(api_key, secret_key, base_url, api_version='v2')

        self.account = self.api.get_account() #retrieve all account information 


    def get_account_info(self):
        """
        Get the account information.

        Returns:
            tradeapi.entity.Account: Account information.
        """
        return self.account
    

    def get_account_balance(self):
        """
        Get the account balance.

        Returns:
            float: Account balance.
        """
        return float(self.account.cash)
    
    def get_portfolio_value(self):
        """
        Get the portfolio value.

        Returns:
            float: Portfolio value.
        """
        return float(self.account.portfolio_value)
    
    def get_positions(self):
        """
        Get the current positions.

        Returns:
            list: List of tradeapi.entity.Position objects representing the positions.
        """
        return self.api.list_positions()

    def get_position(self, symbol: str):
        """
        Get the position for a specific symbol.

        Args:
            symbol (str): Stock symbol.

        Returns:
            tradeapi.entity.Position: Position object for the symbol.
        """
        return self.api.get_position(symbol)
    
    def buy_stock(self, symbol: str, qty: int):
        """
        Place a market buy order for a stock.

        Args:
            symbol (str): Stock symbol.
            qty (int): Quantity to buy.

        Returns:
            None.
        """
        try:
            self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            print("Order placed successfully.")
            print("You have purchased " + str(qty) + " stocks of " + symbol)

        except tradeapi.rest.APIError as e:
            print(f"Error placing order: {e}")


    def sell_stock(self, symbol: str, qty: int):
        """
        Place a market sell order for a stock.

        Args:
            symbol (str): Stock symbol.
            qty (int): Quantity to sell.

        Returns:
            None.
        """
        try:
            self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side='sell',
                type='market',
                time_in_force='day'
            )
            print("Order placed successfully.")
            print("You have sold " + str(qty) + " stocks in " + symbol)

        except tradeapi.rest.APIError as e:
            print(f"Error placing order: {e}")
    
    def long_stock(self, symbol: str, qty: int , EMA: int, stop_loss_percentage: int, profit_ratio: int, notional: int):
        """
        Place a long order for a stock with stop-loss and take-profit.

        Args:
            symbol (str): Stock symbol.
            qty (int): Quantity to buy.
            EMA (int): Exponential Moving Average value.
            stop_loss_percentage (int): Stop-loss percentage relative to EMA.
            profit_ratio (int): Profit ratio relative to stop-loss.
            notional (int): Notional value.

        Returns:
            None.
        """
        stop_loss = round(stop_loss_percentage * EMA, 2)
        take_profit = round(stop_loss * profit_ratio, 2)

        res = [["Stock", symbol],
               ["Quantity", qty],
               ["Notional", notional],
               ["Take Profit", take_profit],
               ["Stop Loss", stop_loss]
        ]
        try:
            self.api.submit_order(
                symbol = symbol,
                qty = qty,
                type = 'stop_limit',
                time_in_force = 'day',
                limit_price = take_profit,
                stop_price = stop_loss
            )  
            print("Order placed successfully.")
            print(tabulate(res))
        except tradeapi.rest.APIError as e:
            print(f"Error placing order: {e}")
        return 
            



    def get_qty(self, symbol: str):
        """
        Get the quantity of a specific stock held.

        Args:
            symbol (str): Stock symbol.

        Returns:
            int: Quantity of the stock held.
        """
        try:
            self.api.get_position(symbol).qty
        except:
            print("You currently have no " + symbol + " stocks")
            return
        return self.api.get_position(symbol).qty


    """
    returns the daily barset from up to the last 6 years
    """
    def get_barset_day(self, symbol: str):
        """
        Get the daily barset for a symbol.

        Args:
            symbol (str): Stock symbol.

        Returns:
            list: List of tradeapi.entity.Bar objects representing the barset.
        """
        # free subscription has a 15 minute delay
        end_date = datetime.datetime.now()
        end_date = end_date - datetime.timedelta(days = 1)
        start_date = end_date - datetime.timedelta(days = 1825)

        end_date = end_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        start_date = start_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        

        return self.api.get_bars(symbol, '1Day', limit=10000, start=start_date, end=end_date)
    

    def get_barset_day_close(self, symbol: str):
        """
        Get the closing prices from the daily barset for a symbol.

        Args:
            symbol (str): Stock symbol.

        Returns:
            list: List of closing prices.
        """
        # free subscription has a 15 minute delay
        end_date = datetime.datetime.now()
        end_date = end_date - datetime.timedelta(days = 1)
        start_date = end_date - datetime.timedelta(days = 1825)

        end_date = end_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        start_date = start_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        barset = self.api.get_bars(symbol, '1Day', limit=10000, start=start_date, end=end_date)

        close_prices = []
        for bar in barset:
            close_prices.append(bar.c)

        return close_prices

    def get_barset_day_close_and_date(self, symbol):
        """
        Get the closing prices and dates from the daily barset for a symbol.

        Args:
            symbol (str): Stock symbol.

        Returns:
            tuple: Tuple containing a list of closing prices and a list of dates.
        """
        # free subscription has a 15 minute delay
        end_date = datetime.datetime.now()
        end_date = end_date - datetime.timedelta(days = 1)
        start_date = end_date - datetime.timedelta(days = 1825) # past 5 years

        end_date = end_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        start_date = start_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        barset = self.api.get_bars(symbol, '1Day', limit=10000, start=start_date, end=end_date)

        close_prices = []
        dates = []
        for bar in barset:
            close_prices.append(bar.c)
            dates.append(bar.t)


        return close_prices, dates