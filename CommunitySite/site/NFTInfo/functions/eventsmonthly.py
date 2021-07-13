from .shared.graphinfo import GraphInfo
from .shared.get_last30days import get_last30days
from ..models import Events

def get_last30daysevents():
    days = get_last30days()

    result = []
    for day,timestamp in days.items():
        ps = Events.objects.filter(timestampday=timestamp).count()
        result.append(GraphInfo(day,ps))

    result.reverse()
    return result


