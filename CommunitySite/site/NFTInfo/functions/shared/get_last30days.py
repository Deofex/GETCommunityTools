from datetime import datetime,timedelta

def get_last30days():
    t = datetime.now()
    tr = datetime(t.year,t.month,t.day)
    td = {}

    for i in range(0,30):
        day = (tr - timedelta(i))
        timestamp = int(day.timestamp())
        td[day.strftime("%d-%m-%Y")] = timestamp

    return td