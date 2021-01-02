# import pandas
# import urllib.request as urllib2
# import pytz
# import pandas_datareader.data as web
# import datetime
# from bs4 import BeautifulSoup
# import csv


# #### Section 1: Scrapes wikipedia page to get all tickers in the S&P 500

# thisurl = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies" # the wikipedia url containing list of S&P 500 companies
# # it helps to visit the webpage and take a look at the source to understand
# #    how the html is parsed.

# myPage = urllib2.urlopen(thisurl) # opens this url

# mySoup = BeautifulSoup(myPage, "html.parser") # parse html soup 

# table = mySoup.find('table', {'class': 'wikitable sortable'}) # finds wiki sortable table in webpage html

# sector_tickers = dict() # create a dictionary to store all tickers according to sector
# for row in table.findAll('tr')[1:]: # find every row in the table
#     col = row.findAll('td')[0].text # find every column in that row
#     if len(col) > 0: # if there are columns in that row
#         sector = str(col.strip()).lower().replace(' ', '_') # identify the sector in the row
#         ticker = row.findAll('td')[0].text # identify the ticker in the row
#         if sector not in sector_tickers: # if this sector is not a key in the dictionary
#             sector_tickers[sector] = list() # add this as a key to the dictionary
#         sector_tickers[sector].append(ticker) # add the ticker to right key in the dictionary

# #### Section 2: Queries Yahoo Finance for historical data on tickers

# # Start and end dates for historical data
# start = datetime.datetime(2010, 1, 1)  # start date
# end = datetime.datetime(2016, 12, 27) # end date

# myKeys = list(sector_tickers.keys()) # find all the sectors which are keys in the dictionary we created in Step 1

# for i in range(0,len(myKeys)): # for each key in the dictionary which represents a sector
#     myTickers = list(sector_tickers.keys()) # find the tickers in that list
#     for j in range(0,len(sector_tickers.keys())): # for each ticker
#         myData = web.DataReader(myTickers[j], "yahoo", start, end) # query the pandas datareader to pull data from Yahoo! finance
#         fileName = myTickers[j] + '.csv' # create a file
#         myData.to_csv(fileName) # save data to the file


import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests


def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class': 'wikitable sortable'})

    tickers = []

    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.strip()
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
        print(tickers)

    return tickers


def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2010, 1, 1)
    end = dt.datetime(2016, 12, 31)

    mykeys = list(save_sp500_tickers())
    for i in range(0,len(tickers)):
    	mytickers = list(tickers[mykeys[i]])
    	for j in range(0,len(mytickers)):
    		mydf = web.DataReader(mytickers[j],'yahoo',start, end)
    		filename = mytickers+'.csv'
    		mydf.to_csv(filename)


        # print(ticker)

        # if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
        #     try:
        #         df = web.DataReader(ticker, 'yahoo', start, end)
        #         df.to_csv('stock_dfs/{}.csv'.format(ticker))
        #     except Exception as ex:
        #         print('Error:', ex)
        # else:
        #     print('Already have {}'.format(ticker))


get_data_from_yahoo(True)