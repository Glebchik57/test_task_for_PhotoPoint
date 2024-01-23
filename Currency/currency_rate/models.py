from django.db import models


class Cost_of_currency(models.Model):
    value = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
