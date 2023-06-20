from ta.trend import MACD
from account import Account
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 



class MACD_Strategy:
    """
    Represents a MACD trading strategy.

    Attributes:
        account (Account): The trading account associated with the strategy.
        symbol (str): The symbol of the stock being traded.
        ratio (float): The risk-to-reward ratio.
        stop_loss_percentage (float): The percentage of the EMA used as the stop loss.
        winrate (float): The win rate of the strategy (default is 1).
    """
    def __init__(self, account: Account, symbol: str):
        """
        Initializes a MACD_Strategy object.

        Args:
            account (Account): The trading account associated with the strategy.
            symbol (str): The symbol of the stock being traded.
        """

        self.account = account
        self.symbol = symbol

        self.ratio = 1.5 # risk to reward ratio
        self.stop_loss_percentage = 0.95 # % of the EMA. So 95% of the EMA when the purchase was made (backtest needed)
        self.winrate = 1 #if it has not been set


    def execute(self):
        """
        Executes the MACD trading strategy.

        Args:
            notional (int): The amount of money to trade.

        Returns:
            None
        """
        notional = self.account.get_account_balance() * 0.1 * self.winrate # wager amount equal to 10% of current balance and winrate during backtest

        df = self.get_data()
        current_cost = self.account.api.get_latest_bar(self.symbol).c
        
        buy_qty = notional / current_cost

        if df['Long_Position'].iloc[-1]: #if there was a signal in the previous day
            self.account.long_stock(self.symbol, buy_qty, df['EMA'], self.stop_loss_percentage, self.ratio, notional)
            return # make a LONG
        elif df['Short_Position'].iloc[-1]:
            print("A Short Position has been detected")
            return #make a short
        else: 
            print("No signal was detected for " + self.symbol)
            return
        


    def plot(self):
        """
        Plots the MACD strategy.

        Returns:
            None
        """
        df = self.get_data()




        # Plotting
        plt.figure(figsize=(12, 6))
        plt.plot(df['Close'], label='Close Price', color='blue')

        # MACD line and Signal
        plt.plot(df['MACD'], label='MACD Line', color='green')
        plt.plot(df['Signal_line'], label='MACD Signal', color='red')

        # EMA
        plt.plot(df['EMA'], label = 'EMA', color = 'cyan')

        # Histogram
        plt.hist(df.index , weights = df['Diff'], bins = len(df['Diff']), label='Histogram')

        # Signal
        plt.plot(df[df['Long_Position'] == 1].index,  df['Close'][df['Long_Position'] == 1],  '^', markersize = 5, color = 'green', label = 'Long')
        plt.plot(df[df['Short_Position'] == 1].index,  df['Close'][df['Short_Position'] == 1],  'v', markersize = 5, color = 'red', label = 'Short')


        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title(f'{self.symbol} - MACD')
        plt.legend()
        plt.grid(True)
        plt.show()

        return
    


    def MACD(self):
        """
        Calculates the MACD line, MACD signal line, and MACD histogram.

        Returns:
            list: A list containing the MACD line, MACD signal line, and MACD histogram.
        """
        close_prices = self.account.get_barset_day_close(self.symbol)

        df = pd.DataFrame(close_prices, columns = ['Close'])

        macd_data = MACD(df['Close'])

        res = [macd_data.macd(),macd_data.macd_signal(),macd_data.macd_diff()]
        return res
    

    def get_data(self):
        """
        Gets the historical data for the symbol and calculates the MACD indicators.
        Also calculates where the signals are

        Returns:
            pd.DataFrame: The dataframe containing the historical data and MACD indicators.
        """
        close_prices, dates = self.account.get_barset_day_close_and_date(self.symbol)

        df = pd.DataFrame(close_prices, columns = ['Close'])

        df['dates'] = dates
        df.set_index('dates')


        macd_line, macd_signal, macd_diff = self.MACD()
         
        df['MACD'] = macd_line
        df["Signal_line"] = macd_signal
        df["Diff"] = macd_diff

        ema = df['Close'].ewm(span=100, adjust=False).mean() #n = 100, for 100 EMA

        df['EMA'] = ema

        df['Signal_Long'] = 0.0

        df['Signal_Long'] = np.where((df['MACD'] < 0) & (df['MACD'] > df['Signal_line']) & (df['Close'] > df['EMA'])  , 1.0, 0.0)

        df['Long_Position'] = df['Signal_Long'].diff()

        df['Signal_Short'] = 0.0

        df['Sigial_Short'] = np.where((df['MACD'] > 0) & (df['MACD'] < df['Signal_line']) & (df['Close'] < df['EMA'])  , 1.0, 0.0)

        df['Short_Position'] = df['Sigial_Short'].diff()

        return df
    
    def set_profit_ratio(self, ratio: int):
        """
        Sets the risk-to-reward ratio for the strategy.

        Args:
            ratio (int): The risk-to-reward ratio.

        Returns:
            None
        """
        self.ratio = ratio
        return
    
    def set_stop_loss_ratio(self, ratio: int):
        """
        Sets the stop loss percentage for the strategy.

        Args:
            ratio (int): The stop loss percentage.

        Returns:
            None
        """
        self.stop_loss_percentage = ratio
        return
    
    def set_winrate(self, winrate: int):
        """
        Sets the win rate for the strategy.

        Args:
            winrate (int): The win rate.

        Returns:
            None
        """
        self.winrate = winrate
        return

    def get_profit_ratio(self):
        """
        Returns the risk-to-reward ratio.

        Returns:
            float: The risk-to-reward ratio.
        """
        return self.ratio
    
    def get_stop_loss_ratio(self):
        """
        Returns the stop loss percentage.

        Returns:
            float: The stop loss percentage.
        """
        return self.stop_loss_percentage
    
    def get_winrate(self):
        """
        Returns the win rate.

        Returns:
            float: The win rate.
        """
        return self.winrate