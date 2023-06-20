from account import Account
from MACDStrategy import MACD_Strategy
from Backtester import Backtester

class StockContainer:
    def __init__(self, account: Account, stocks: list[str]):
        """
        Initializes a StockContainer object.

        Args:
            account (Account): An instance of the Account class.
            stocks (list[str]): A list of stock symbols.
        """
        self.account = account
        self.stocks = stocks
        self.MACD_objects = []
        self.make_MACD_objects()
        self.backtester = Backtester(self.MACD_objects)
        self.execute_backtester()



    def execute_backtester(self):
        """
        Executes the backtester, removes stocks from the list if necessary,
        and sets the ratios.
        """
        self.backtester.execute()
        remove_stocks = self.backtester.remove_stocks
        for stock in remove_stocks:
            self.stocks.remove(stock.symbol)
        self.backtester.set_ratios()


    def make_MACD_objects(self):
        """
        Creates MACD_Strategy objects for each stock in the list.
        """
        self.MACD_objects = []
        for stock in self.stocks:
            self.MACD_objects.append(MACD_Strategy(self.account, stock))


    def execute(self):
        """
        Executes the backtester and MACD strategies.
        """
        self.backtester.execute()
        for MACD_object in self.MACD_objects:
            MACD_object.execute()
        return

    def add_stock(self, stock: str):
        """
        Adds a stock to the list and creates a corresponding MACD strategy object.

        Args:
            stock (str): The stock symbol to add.
        """
        if stock in self.stocks:
            print(stock + " is already in the list")
            return
        else:
            self.stocks.append(stock)
            self.MACD_objects.append(MACD_Strategy(self.account, stock))
            self.backtester.add_stock(self.MACD_objects[-1])
            print(stock + " has been added from the list")
            return
        

    
    def remove_stock(self, stock:str):
        """
        Removes a stock from the list and its corresponding MACD strategy object.

        Args:
            stock (str): The stock symbol to remove.
        """
        if stock in self.stocks:
            index = self.stocks.index(stock)
            self.stocks.remove(stock)
            self.MACD_objects.pop(index)
            print(stock + " has been removed from the list")
        else:
            print(stock + " is not in the list")

        
        