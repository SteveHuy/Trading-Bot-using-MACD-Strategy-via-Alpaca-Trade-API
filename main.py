import time
import schedule
from account import Account
from StockContainer import StockContainer
import os
from dotenv import load_dotenv


load_dotenv()

account = Account(os.getenv('API_KEY'), os.getenv('SECRET_KEY'), base_url='https://paper-api.alpaca.markets')

# example of using the code
stock_list = ['ABNB', 'ADP','AMZN' , 'TMUS', 'AAPL', 'TSLA', 'MSFT']

main = StockContainer(account, stock_list)


main.add_stock("NVDA")

schedule.every().day.at("10:00").do(main.execute)


while True:
    schedule.run_pending()
    time.sleep(1)