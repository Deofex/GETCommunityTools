from django.shortcuts import render
from .models import Prices
from .functions.nfttoday import ticketssoldlast24h, ticketsscannedlast24h, \
    eventslast24h
from .functions.nftmonthly import get_last30daysinteractions
from .functions.eventsmonthly import get_last30daysevents
from .functions.eventsthirtydays import eventsthirtydays
from .functions.eventscreatewordcloud import create_eventscreateworldcloud


def page_home(request):
    return render(request, 'NFTInfo/home.html', {
        'ticketssoldlast24h': ticketssoldlast24h(),
        'ticketsscannedlast24h': ticketsscannedlast24h(),
        'eventsactivelast24h': eventslast24h(),
        'geteurprice': "{:.2f}".format(Prices.objects.get(pk='GET').price)
    })


def page_interactions(request):
    last30dayssc = get_last30daysinteractions()
    last30daysscperiodnames = [d.periodname for d in last30dayssc]
    last30daysscvalues = [d.value for d in last30dayssc]
    return render(request, 'NFTInfo/interactions.html', {
        'last30daysscperiodnames': last30daysscperiodnames,
        'last30daysscvalues': last30daysscvalues
    })


def page_events(request):
    # Select info for the upcoming 30 days event graph (2 lists, 1 with periods,
    # 1 with values)
    thirtydaysevents = get_last30daysevents()
    last30daysperiodnames = [d.periodname for d in thirtydaysevents]
    last30daysvalues = [d.value for d in thirtydaysevents]

    # Select last 30 days events
    events30days = eventsthirtydays()

    # Create word cloud data
    eventswordcloudlist = create_eventscreateworldcloud(events30days)

    return render(request, 'NFTInfo/events.html', {
        'last30daysperiodnames': last30daysperiodnames,
        'last30daysvalues': last30daysvalues,
        'events30days': events30days,
        'eventswordcloudlist': eventswordcloudlist
    })
