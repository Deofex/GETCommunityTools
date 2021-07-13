from django.shortcuts import render
from .models import Prices
from .functions.nfttoday import ticketssoldlast24h, ticketsscannedlast24h, \
    eventslast24h
from .functions.nftmonthly import get_last30daysstatechanges
from .functions.eventsmonthly import get_last30daysevents


def page_home(request):
    return render(request, 'NFTInfo/home.html', {
        'ticketssoldlast24h': ticketssoldlast24h(),
        'ticketsscannedlast24h': ticketsscannedlast24h(),
        'eventsactivelast24h': eventslast24h(),
        'geteurprice': "{:.2f}".format(Prices.objects.get(pk='GET').price)
    })


def page_statechanges(request):
    return render(request, 'NFTInfo/statechanges.html', {
        'last30daysstatechanges': get_last30daysstatechanges()
    })


def page_events(request):
    return render(request, 'NFTInfo/events.html', {
        'last30daysevents': get_last30daysevents()
    })
