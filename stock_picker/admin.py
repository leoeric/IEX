from django.contrib import admin
from stock_picker.models import Investor,InvestorAccount,Stock

# Register your models here.
admin.site.register(Investor)
admin.site.register(InvestorAccount)
admin.site.register(Stock)
