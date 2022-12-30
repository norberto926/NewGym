from django.db import models

# Create your models here.

class Exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    equipment_needed = models.ManyToManyField(Eqipment)