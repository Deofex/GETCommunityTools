from django.db import models


class Events(models.Model):
    eventaddress = models.TextField(primary_key=True)
    blocknumber = models.IntegerField()
    timestamp = models.IntegerField()
    timestampday = models.IntegerField()
    getused = models.IntegerField()
    ordertime = models.IntegerField()
    integratoraddress = models.TextField()
    underwriteraddress = models.TextField()
    eventname = models.TextField()
    shopurl = models.TextField()
    imageurl = models.TextField()
    longitude = models.TextField()
    latitude = models.TextField()
    currency = models.TextField()
    ticketeer = models.TextField()
    starttime = models.IntegerField()
    endtime = models.IntegerField()
    privateevent = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'events'


class Psale(models.Model):
    nftindex = models.IntegerField(unique=True)
    blocknumber = models.IntegerField()
    timestamp = models.IntegerField()
    timestampday = models.IntegerField()
    getused = models.IntegerField()
    ordertime = models.IntegerField()
    destinationaddress = models.TextField()
    eventaddress = models.ForeignKey(Events,to_field="eventaddress",db_column="eventaddress",on_delete=models.CASCADE)
    price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'psale'


class Ssale(models.Model):
    nftindex = models.IntegerField()
    blocknumber = models.IntegerField()
    timestamp = models.IntegerField()
    timestampday = models.IntegerField()
    getused = models.IntegerField()
    ordertime = models.IntegerField()
    destinationaddress = models.TextField()
    eventaddress = models.TextField()
    price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ssale'


class Tgids(models.Model):
    tgid = models.TextField(primary_key=True)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'tgids'


class Tinvalidated(models.Model):
    nftindex = models.IntegerField()
    blocknumber = models.IntegerField()
    timestamp = models.IntegerField()
    timestampday = models.IntegerField()
    getused = models.IntegerField()
    ordertime = models.IntegerField()
    originaddress = models.TextField()

    class Meta:
        managed = False
        db_table = 'tinvalidated'


class Tscanned(models.Model):
    nftindex = models.ForeignKey(Psale,to_field="nftindex",db_column="nftindex",on_delete=models.CASCADE)
    blocknumber = models.IntegerField()
    timestamp = models.IntegerField()
    timestampday = models.IntegerField()
    getused = models.IntegerField()
    ordertime = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tscanned'

class Prices(models.Model):
    token = models.TextField(primary_key=True)
    price = models.FloatField()

    class Meta:
        managed = False
        db_table = 'prices'