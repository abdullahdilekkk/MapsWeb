from django.db import models
# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=156)
    qx = models.FloatField()
    qy = models.FloatField()
    is_metropolitan = models.BooleanField(default=False)
    country = models.CharField(max_length=156)

    def __str__(self):
        return f"{self.name}-{self.country}"
