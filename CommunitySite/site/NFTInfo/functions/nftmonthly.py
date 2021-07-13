from .shared.graphinfo import GraphInfo
from .shared.get_last30days import get_last30days
from ..models import Psale, Ssale, Tscanned,Tinvalidated

def get_last30daysstatechanges():
    days = get_last30days()

    result = []
    for day,timestamp in days.items():
        ps = Psale.objects.filter(timestampday=timestamp).count()
        ss = Ssale.objects.filter(timestampday=timestamp).count()
        ts = Tscanned.objects.filter(timestampday=timestamp).count()
        ti = Tinvalidated.objects.filter(timestampday=timestamp).count()

        t = ps + ss + ts + ti
        result.append(GraphInfo(day,t))

    result.reverse()
    return result


