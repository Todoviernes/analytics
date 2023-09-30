from django.db import models

# Create your models here.


class Event(models.Model):
    TYPE_CHOICES = [('page_view', 'Page View'), ('click', 'Click')]
    event_type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    user_id = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    url = models.URLField()
    utm_source = models.CharField(max_length=255, blank=True)
    utm_medium = models.CharField(max_length=255, blank=True)


class Purchase(models.Model):
    user_id = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    product_id = models.CharField(max_length=255)
    amount = models.FloatField()
    utm_source = models.CharField(max_length=255, blank=True)
    utm_medium = models.CharField(max_length=255, blank=True)
