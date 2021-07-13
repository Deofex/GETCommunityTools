from datetime import datetime, timedelta
from django.db.models import Count
from ..models import Events

def eventsthirtydays():
    t = datetime.now()
    tr = datetime(t.year,t.month,t.day)
    tt  = tr + timedelta(30)
    trt = int(tr.timestamp())
    ttt = int(tt.timestamp())
    events30daysdb = Events.objects.filter(
        starttime__range=[trt,ttt]).annotate(
            nfts=Count('psale')).order_by('-nfts').filter(nfts__gt=0).values(
                "eventname", "nfts","ticketeer","starttime")

    events30days = [{
        'eventname': d['eventname'] ,
        'nfts': d['nfts'],
        'ticketeer': d['ticketeer'],
        'date':datetime.fromtimestamp(d['starttime']).strftime("%d-%m-%Y")
    } for d in events30daysdb]
    return events30days