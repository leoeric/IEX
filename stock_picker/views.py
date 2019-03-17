from django.shortcuts import render
from stock_picker.models import Investor,InvestorAccount,Stock

# Create your views here.
def index(request):
    return render(request,'stock_picker/index.html')

def stock_init(request):
    return render(request,'stock_picker/index.html')
