#this script is based on code in the following website
#https://pythonprogramming.net/sp500-company-price-data-python-programming-for-finance/?completed=/sp500-company-list-python-programming-for-finance/
#modifer: Hao-Lin Li


import bs4 as bs
import datetime as dt
import os
import pandas_datareader.data as web
import pickle
import requests

#read tickers of sp500 stocks into file
def save_sp500_tickers(file_name='sp500-tickers.txt'):
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    f = open(file_name,'w+')
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        ticker = ticker.rstrip()+" "
        f.write(ticker)
    f.close()
    return 


#sp500ticker=save_sp500_tickers()
#myfile = open('sp500_tickers.txt','w')
#for el in sp500ticker:
#    myfile.write(el)
#myfile.close()

# save_sp500_tickers()
def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500-tickers.txt", "r") as f:
            tickers = f.readline()
            tickers = tickers.rstrip()
            print(tickers)
            tickers = tickers.split(' ')
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2010, 1, 1)
    #end = dt.datetime.now()
    end = dt.datetime.now()
    for ticker in tickers:
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            print("***********  getting stock "+ticker+"  **********")
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))


get_data_from_yahoo()
