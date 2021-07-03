from django.shortcuts import render
from .models import Prices
from .functions.nfttoday import ticketssoldlast24h, ticketsscannedlast24h, \
    eventslast24h

# Create your views here.
def page_home(request):

    eventslast24h()
    return render(request,'NFTInfo/home.html',{
        'ticketssoldlast24h': ticketssoldlast24h(),
        'ticketsscannedlast24h': ticketsscannedlast24h(),
        'eventsactivelast24h': eventslast24h(),
        'geteurprice': "{:.2f}".format(Prices.objects.get(pk='GET').price)
    })


