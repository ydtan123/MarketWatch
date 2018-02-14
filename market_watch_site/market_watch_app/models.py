from django.db import models

class ScrapeLog(models.Model):
    response_body = models.TextField(max_length=5000)
    tick = models.CharField(max_length=20, default='')
    create_date = models.DateTimeField('date created')
