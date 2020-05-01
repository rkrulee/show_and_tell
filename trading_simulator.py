import pandas as pd
import pandas_datareader as web
import numpy as np
import datetime as dt
import math
import warnings
warnings.filterwarnings("ignore")

def now(msg):
    t = dt.datetime.now().strftime("%H:%M:%S")
    print(t + ': ' + msg)

def get_price(date, ticker):
    global prices
    return prices.loc[date][ticker]

def transaction(id, ticker, amount, price, type, info):
    global transaction_id
    if type == "buy":
        exp_date = today + dt.timedelta(days=14)
        transaction_id += 1
        print("buy")
    else:
        exp_date = today
    if type == "sell":
        data = {"id":id, "ticker":ticker, "amount":amount, "price":price,"date":today, "type":type,"exp_date":exp_date,
                "info":info}
        print("sell")
    elif type == "buy":
        data = {"id":transaction_id, "ticker":ticker, "amount":amount, "price":price,"date":today, "type":type,
                "exp_date":exp_date, "info":info}
        active_log.append(data)
        print("buy")
    transaction_log.append(data)

def buy(interest_list, allocated_money):
    global money, portfolio
    for item in interest_list:
        price = get_price(today,item)
        print(price)
        if not np.isnan(price):
            quantity = math.floor(allocated_money/price)
            money -= quantity*price
            portfolio[item] += quantity
            transaction(0, item, quantity, price, "buy", "")

def sell():
    global money, portfolio, prices, today
    items_to_remove = []
    for i in range(len(active_log)):
        log = active_log[i]
        if log["exp_date"] <= today and log["type"] == "buy":
            tick_price = get_price(today, log["ticker"])
            print(tick_price)
            if not np.isnan(tick_price):
                money += log["amount"]*tick_price
                portfolio[log["ticker"]] -= log["amount"]
                transaction(id=log["id"],ticker=log["ticker"], amount=log["amount"], price=tick_price, type="sell", info=log["info"])
                items_to_remove.append(i)
            else:
                log["exp_date"] += dt.timedelta(days=1)
    items_to_remove.reverse()
    for elem in items_to_remove:
        active_log.remove(active_log[elem])

def simulation():
    global today, volume_changes, money
    start_date = today - dt.timedelta(days=14)
    series = volume_changes.loc[start_date:today].mean()
    interest_list = series[series > 100].index.tolist()
    sell()
    if len(interest_list) > 0:
        money_to_allocate = 500000/len(interest_list)
        buy(interest_list, money_to_allocate)

def get_indices():
    global tickers
    f = open("/Users/robertkrulee/Desktop/stock_abbr.csv", "r")
    for line in f:
        tickers.append(line.strip())
    f.close()

def trading_day():
    global prices, today
    return np.datetime64(today) in list(prices.index.values)

def current_value():
    global money, portfolio, today, prices
    value = money
    for ticker in tickers:
        tick_price = get_price(today, ticker)
        if not np.isnan(tick_price):
            value += portfolio[ticker]*tick_price
    return int(value*100)/100

def main():
    global today
    get_indices()
    for ticker in tickers:
        portfolio[ticker] = 0
    while today < simend:
        while not trading_day():
            today += dt.timedelta(days=1)
        simulation()
        current_p_value = current_value()
        print(current_p_value, today)
        today += dt.timedelta(days=7)


if __name__ == '__main__':
    #read in stock symbols
    stocks = []
    f = open("/Users/robertkrulee/Desktop/stock_abbr.csv", "r")
    for line in f:
        stocks.append(line.strip())
    f.close()
    #read in relevant financial information about our stocks from yahoo Finance
    web.DataReader(stocks, "yahoo", start="2019-1-1", end='2019-12-31')["Adj Close"].to_csv("/Users/robertkrulee/Desktop/adj_close.csv")
    now("adjusted close data per stock read in from yahoo finance, written out to desktop")

    web.DataReader(stocks, "yahoo", start="2019-1-1", end='2019-12-31')["Volume"].to_csv("/Users/robertkrulee/Desktop/volume.csv")
    now("volume data per stock read in from yahoo, written out to desktop")

    #define global variables
    prices = pd.read_csv("/Users/robertkrulee/Desktop/adj_close.csv", index_col = "Date", parse_dates=True)
    now("read in adjusted close data")

    volume_changes = pd.read_csv("/Users/robertkrulee/Desktop/volume.csv", index_col = "Date", parse_dates=True)
    now("read in adjusted close data")

    #dates, today = starting point, simend = end of simulation
    today = dt.date(2019,6,1)
    simend = dt.date(2019,12,31)

    #array for all sysmbols we can trade AAL (american airlines), or CCL (Carnival Cruise lines)
    tickers = []

    #open/close position
    transaction_id = 0

    #cash on hand
    money = 1000

    #records all symbols and dollar amounts we currently have in said port
    portfolio = {}

    #tracking for our transactions
    active_log = []
    transaction_log= []

    #execute code
    main()
