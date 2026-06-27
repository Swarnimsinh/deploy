from django.db import models

# Create your models here.
class BioData(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveBigIntegerField()
    city = models.CharField(max_length=100)