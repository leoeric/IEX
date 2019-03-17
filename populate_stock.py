import os
import requests
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE','IEX.settings')

import django
django.setup()

from stock_picker.models import Stock

IEX_BASE_URL = 'https://api.iextrading.com/1.0/stock/'
SECTOR_URL = 'https://api.iextrading.com/1.0/stock/market/sector-performance'
BATCH_SIZE = 100;

# generate api script to populate all stocks from nasdaq and store in DB
def add_stock(N=10000):
    '''
    populate the latest stocks
    '''
    i=0
    '''
    with open('static/ext_data/nasdaq/nasdaqlisted.txt', 'r') as reader:
        for line in reader.readlines():
            if i!=0:
                print (str(i) + ':')
                print(line.split('|')[0])

                # create new stock
                stock= Stock.objects.get_or_create(symbol=line.split('|')[0])[0]
            if i==N:
                break
            i=i+1
    '''
    symbol_ref_url='https://api.iextrading.com/1.0/ref-data/symbols'
    # get symbol profile
    rsp = requests.get(symbol_ref_url)
    data = rsp.json()
    print("total stock count:")
    print(len(data))
    size = len(data)

    for symbol_instance in data:
        # print(data[i]['symbol'])

        stock = Stock.objects.get_or_create(symbol=data[i]['symbol'])[0]
        stock.company_name = data[i]['name']
        stock.ref_date = datetime.strptime(data[i]['date'],'%Y-%m-%d')
        stock.isEnabled = data[i]['isEnabled']
        stock.type = data[i]['type']
        stock.iexId = data[i]['iexId']

        stock.save()

        if i>=size:
            break
        i=i+1

# add attributes to stock
def get_iex_stock_details():
    i=0

    del_count = 0
    for stock_instance in Stock.objects.all():
        i = i + 1

        try:
            if stock_instance.week52high is None:
                stock_stats_url = IEX_BASE_URL+stock_instance.symbol+'/stats'
                company_stats_url = IEX_BASE_URL+stock_instance.symbol+'/company'
                logo_url = IEX_BASE_URL+stock_instance.symbol+'/logo'

                # get company basic profile
                rsp = requests.get(company_stats_url)
                data = rsp.json()

                print('populate company #:')
                print(i, '.', stock_instance.symbol)

                if data['exchange'] != None:
                    stock_instance.exchange = data['exchange']
                if data['industry'] != None:
                    stock_instance.industry = data['industry']
                if data['sector'] != None:
                    stock_instance.sector = data['sector']
                if data['website'] != None:
                    stock_instance.website = data['website']
                if data['description'] != None:
                    stock_instance.description = data['description']
                if data['tags'] != None:
                    stock_instance.tags = data['tags']

                # get company logo URL
                rsp = requests.get(logo_url)
                data = rsp.json()
                stock_instance.logo = data['url']

                # get json data from API
                rsp = requests.get(stock_stats_url)
                data = rsp.json()

                print('populate stats #:')
                print(i, '.', stock_instance.symbol)

                stock_instance.company_name = data['companyName']
                stock_instance.market_cap = data['marketcap']
                stock_instance.beta = data['beta']
                stock_instance.week52high = data['week52high']
                stock_instance.week52low = data['week52low']
                stock_instance.dividend_rate = data['dividendRate']
                stock_instance.dividend_yield = data['dividendYield']
                #print('before conversion:', data['exDividendDate'])
                if data['exDividendDate'] != 0:
                    stock_instance.ex_dividend_date = datetime.strptime(data['exDividendDate'],'%Y-%m-%d %H:%M:%S.%f')
                #print('after conversion:', stock_instance.ex_dividend_date)
                stock_instance.latest_EPS = data['latestEPS']
                #print('before conversion eps date:', data['latestEPSDate'])
                if data['latestEPSDate'] != 0:
                    stock_instance.latest_EPS_date = datetime.strptime(data['latestEPSDate'],'%Y-%m-%d')
                #print('after conversion:', stock_instance.latest_EPS_date)
                stock_instance.shares_outstanding = data['sharesOutstanding']
                stock_instance.return_on_equity = data['returnOnEquity']
                stock_instance.consensus_EPS = data['consensusEPS']
                stock_instance.number_of_estimates_EPS = data['numberOfEstimates']
                stock_instance.EBITDA = data['EBITDA']
                stock_instance.revenue = data['revenue']
                stock_instance.gross_profit = data['grossProfit']
                stock_instance.cash_flow = data['cash']
                stock_instance.debt = data['debt']
                stock_instance.ttmEPS = data['ttmEPS']
                stock_instance.return_on_assets = data['returnOnAssets']
                stock_instance.return_on_capital = data['returnOnCapital']
                stock_instance.profit_margin = data['profitMargin']
                stock_instance.price_to_book = data['priceToBook']
                stock_instance.day200_moving_avg = data['day200MovingAvg']
                stock_instance.day50_moving_avg = data['day50MovingAvg']
                stock_instance.insider_percent = data['insiderPercent']

                stock_instance.save()
        except:
            print('an error occur')
            print(stock_instance.week52high)
            print(stock_instance)

            del_count = del_count + 1

    print('deleted: ', del_count)

def get_stock(symbol_in):
    print(Stock.objects.filter(symbol=symbol_in)[0])



if __name__ == '__main__':
    print("Populating the databases...Please Wait")
    # add_stock()
    get_iex_stock_details()
    # get_stock('AABA')
    print('Populating Complete')
