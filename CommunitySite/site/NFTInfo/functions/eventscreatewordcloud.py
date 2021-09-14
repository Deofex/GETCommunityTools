def create_eventscreateworldcloud(events):

    eventsum = {}
    for event in events:
        if event['eventname'] in eventsum:
            a = eventsum[event['eventname']]
            eventsum[event['eventname']] = eventsum[event['eventname']] + event['nfts']
        else:
            eventsum[event['eventname']] = event['nfts']
    eventsumsorted = list(sorted(eventsum.items(), key=lambda item: item[1], reverse=True))

    # Create wordcloud from events
    minsize = eventsumsorted[0][1] / 100

    wordcloudlist = [(
        d[0],
        str(int(d[1] / minsize))) for d in eventsumsorted]
    #wordcloud = {
    #    'list':wordcloudlist
    #}
    return wordcloudlist
