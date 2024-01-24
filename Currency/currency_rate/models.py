from django.db import models


class Cost_of_currency(models.Model):
    value = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        ordering = ['-date']
