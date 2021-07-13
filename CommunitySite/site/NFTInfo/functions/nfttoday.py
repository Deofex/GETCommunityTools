from datetime import datetime
from ..models import Psale, Ssale, Tscanned

def ticketssoldlast24h():
    ct = datetime.now()
    cd = datetime(ct.year,ct.month,ct.day)
    timestamp = cd.timestamp()

    ts = Psale.objects.filter(timestamp__gte=timestamp).count()
    return ts

def ticketsscannedlast24h():
    ct = datetime.now()
    cd = datetime(ct.year,ct.month,ct.day)
    timestamp = cd.timestamp()

    ts = Tscanned.objects.filter(timestamp__gte=timestamp).count()
    return ts

def eventslast24h():
    ct = datetime.now()
    cd = datetime(ct.year,ct.month,ct.day)
    timestamp = cd.timestamp()

    q1 = Psale.objects.filter(timestamp__gte=timestamp).values('eventaddress')
    q2 = Ssale.objects.filter(timestamp__gte=timestamp).values('eventaddress')
    q3 = Tscanned.objects.filter(timestamp__gte=timestamp).values('nftindex__eventaddress')

    s = []

    for q in q1.values('eventaddress'):
        s.append(q['eventaddress'])
    for q in q2.values('eventaddress'):
        s.append(q['eventaddress'])
    for q in q3.values('nftindex__eventaddress'):
        s.append(q['nftindex__eventaddress'])

    return len(set(s))