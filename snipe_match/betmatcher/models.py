from django.db import models


class ScrapingResults(models.Model):
    bookmaker = models.TextField(blank=True, null=True)
    tournament = models.TextField(blank=True, null=True)
    betradarid = models.IntegerField(db_column='betRadarID', blank=True, null=True)  # Field name made lowercase.
    event = models.TextField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)
    bet = models.TextField(blank=True, null=True)
    betodd = models.FloatField(db_column='betOdd', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return f'{self.bookmaker} {self.tournament} {self.betradarid} {self.event} {self.bet} {self.betodd}'

    class Meta:
        # db_table = 'scraping_results'
        unique_together = (("bookmaker", "betradarid", "event", "bet"))
