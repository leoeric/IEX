from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
# Create your models here.

class Stock(models.Model):
    symbol = models.CharField(max_length=254,primary_key=True)
    company_name = models.CharField(max_length=254,blank=True,default="")
    ref_date = models.DateField(null=True)
    # will be true if the symbol is enabled for trading on IEX
    isEnabled = models.BooleanField(null=True)
    # AD - ADR
    # RE - REIT
    # CE - Closed end fund
    # SI - Secondary Issue
    # LP - Limited Partnerships
    # CS - Common Stock
    # ET - ETF
    type = models.CharField(max_length=8,blank=True,default="")
    iexId = models.IntegerField(null=True)

    exchange = models.CharField(max_length=254,blank=True,default="")
    industry = models.CharField(max_length=254,blank=True,default="")
    sector = models.CharField(max_length=254,blank=True,default="")
    website = models.URLField(blank=True,default="")
    description =  models.TextField(default="")
    # Stock.objects.filter(tags__contains=['Technology'])
    # tag to link the similar stocks
    tags = ArrayField(models.CharField(max_length=200), null=True)
    # the last 4 most recent record
    earnings_details = JSONField(blank=True,default=dict)
    # the last 4 quarter financial results
    financials_details = JSONField(blank=True,default=dict)
    market_cap = models.BigIntegerField(null=True)
    beta = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    week52high = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    week52low = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    dividend_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    dividend_yield = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ex_dividend_date = models.DateField(null=True)
    latest_EPS = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    latest_EPS_date = models.DateField(null=True)
    shares_outstanding = models.BigIntegerField(null=True)
    # (Trailing twelve months)
    return_on_equity = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    # (Most recent quarter)
    consensus_EPS = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    # (Most recent quarter)
    number_of_estimates_EPS = models.IntegerField(null=True)
    EBITDA = models.BigIntegerField(null=True)
    revenue = models.BigIntegerField(null=True)
    gross_profit = models.BigIntegerField(null=True)
    cash_flow = models.BigIntegerField(null=True)
    debt = models.BigIntegerField(null=True)
    ttmEPS = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    return_on_assets = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    return_on_capital = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    profit_margin = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_to_book = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    day200_moving_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    day50_moving_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    insider_percent = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    # image url
    logo = models.URLField(blank=True, default='')
    # all peer companies
    peers = ArrayField(models.CharField(max_length=200), null=True)

    def __str__(self):
        return self.symbol + ': ' + self.company_name

class Investor(models.Model):
    investor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    nick_name = models.CharField(max_length=128,unique=True)
    email = models.EmailField(max_length=254,unique=True)
    created_date = models.DateField(null=True)

    def __str__(self):
        return self.nick_name

class InvestorAccount(models.Model):
    account_id = models.AutoField(primary_key=True)
    investor_name = models.ForeignKey(Investor,on_delete=models.CASCADE)
    stock_list = ArrayField(models.CharField(max_length=10), blank=True)
    updated_date = models.DateField(null=True)
    created_date = models.DateField(null=True)

    def __str__(self):
        return self.investor_name + "'s account: " + self.account_id
