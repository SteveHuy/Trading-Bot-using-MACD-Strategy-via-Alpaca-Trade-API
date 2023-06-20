from MACDStrategy import MACD_Strategy

class Backtester:
    """
    Represents a backtesting tool for evaluating MACD trading strategies.

    Attributes:
        stocks (list[MACD_Strategy]): List of MACD trading strategies to backtest.
        profit_ratios (list[float]): List of profit ratios to test.
        stop_ratios (list[float]): List of stop ratios to test.
        optimal_profit_ratio (list[float]): List of optimal profit ratios for each strategy.
        optimal_risk_ratio (list[float]): List of optimal risk ratios for each strategy.
        winrates (list[float]): List of win rates for each strategy.
        money_made (list[float]): List of money made for each strategy.
    """
    def __init__(self, stocks: list[MACD_Strategy]):
        """
        Initializes a Backtester object.

        Args:
            stocks (list[MACD_Strategy]): List of MACD trading strategies to backtest.
        """
        self.stocks = stocks
        self.profit_ratios = [1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3]
        self.stop_ratios = [0.95, 0.96, 0.97, 0.98, 0.99, 1] #in relationship to the EMA given in the MACD strategy

        self.optimal_profit_ratio = []
        self.optimal_risk_ratio = []

        self.winrates = []
        self.money_made =[]

        self.remove_stocks = []


    def execute(self):
        """
        Executes the backtesting process for each MACD strategy.
        """
        self.optimal_profit_ratio = []
        self.optimal_risk_ratio = []

        self.winrates = []
        self.money_made = []
        self.remove_stocks = []
        for stock in self.stocks:
            self.add_data(stock)
        
        for remove in self.remove_stocks:
            self.stocks.remove(remove)


        return

    def add_data(self, stock: MACD_Strategy):
        """
        Calculates the optimal profit ratio, optimal risk ratio, win rate, and money made for each strategy.
        And removes any of the stocks which make negative money
        """


        stock_data = stock.get_data()
        signals = stock_data.loc[stock_data['Long_Position'] == 1].index


        greatest_accuracy = 0
        greatest_money = 0

        for stop in self.stop_ratios:

            for profit in self.profit_ratios:
                current_wins = 0
                current_money = 0
                for signal in signals:
                    # lets figure out the stop loss first
                    EMA = stock_data['EMA'].iloc[signal]
                    stop_loss = self.get_stop_loss(stop, EMA)

                    money_lost = stock_data['Close'].iloc[signal] - stop_loss # money is lost when stop_loss is taken

                    # lets now figure out the take_profit
                    take_profit = self.get_take_profit(profit, stop_loss)

                    # lets make the moving signal to check when either the stop loss or take profit is reached
                    moving_signal = signal
                    while moving_signal != len(stock_data):
                        if stock_data['Close'].iloc[moving_signal] >= take_profit:
                            current_wins += 1
                            current_money += take_profit
                            break

                        elif stock_data['Close'].iloc[moving_signal] <= stop_loss:
                            current_money -= money_lost
                            break
                        else:
                            moving_signal += 1

                accuracy = current_wins / len(signals)
                if (accuracy > greatest_accuracy) or (current_money >= greatest_money): # as we begin to iterate through the higher ratios the accuracy WILL decrease so we also check money
                    greatest_accuracy = accuracy
                    greatest_money = current_money
                    best_profit_ratio = profit
                    best_stop_ratio = stop
        if greatest_accuracy != 0:
            self.optimal_profit_ratio.append(best_profit_ratio)
            self.optimal_risk_ratio.append(best_stop_ratio)
            self.winrates.append(greatest_accuracy)
            self.money_made.append(greatest_money)
        else:
            self.remove_stocks.append(stock)
        return


            
    def set_ratios(self):
        """
        Sets the optimal profit ratio, optimal risk ratio, and win rate for each strategy.

        Note:
            This method should be called after executing the backtester.
        """
        if len(self.optimal_profit_ratio) == 0:
            print("Backtester has not been executed so ratios have not been calculated")
        else:
            for i in range(len(self.stocks)):
                self.stocks[i].set_profit_ratio(self.optimal_profit_ratio[i])
                self.stocks[i].set_stop_loss_ratio(self.optimal_risk_ratio[i])
                self.stocks[i].set_winrate(self.winrates[i])

    def get_stop_loss(self, ratio: int, EMA: int):
        """
        Calculates the stop loss based on the ratio and EMA.

        Args:
            ratio (int): The stop ratio.
            EMA (int): The EMA value.

        Returns:
            float: The stop loss value.
        """
        stop_loss = ratio * EMA
        return stop_loss

    def get_take_profit(self, ratio: int, stop_loss: int):
        """
        Calculates the take profit based on the ratio and stop loss.

        Args:
            ratio (int): The take profit ratio.
            stop_loss (int): The stop loss value.

        Returns:
            float: The take profit value.
        """
        take_profit = ratio * stop_loss
        return take_profit

    def add_stock(self, stock: MACD_Strategy):
        """
        Adds a new stock into the list

        Args:
            stock (MACD_Strategy): The new stock that is added
        """
        self.add_data(stock)
        self.stocks[-1].set_profit_ratio(self.optimal_profit_ratio[-1])
        self.stocks[-1].set_stop_loss_ratio(self.optimal_risk_ratio[-1])
        self.stocks[-1].set_winrate(self.winrates[-1])
        return
    
    def remove_stock(self, index: int):
        """
        Adds a new stock into the list

        Args:
            stock (MACD_Strategy): The new stock that is added
        """
        self.winrates.pop(index)
        self.optimal_profit_ratio.pop(index)
        self.optimal_risk_ratio.pop(index)
        self.money_made.pop(index)
        return
    

    def get_optimal_profit_ratio(self):
        """
        Returns the optimal profit ratio.

        Returns:
            list: The optimal profit ratio.
        """
        return self.optimal_profit_ratio
    
    def get_optimal_risk_ratio(self):
        """
        Returns the optimal risk ratio.

        Returns:
            list: The optimal risk ratio.
        """
        return self.optimal_risk_ratio
    
    def get_winrates(self):
        """
        Returns the win rates.

        Returns:
            list: A list of win rates.
        """
        return self.winrates
    
    def get_money_made(self):
        """
        Returns the amount of money made.

        Returns:
            list: The amount of money made.
        """
        return self.money_made
    
