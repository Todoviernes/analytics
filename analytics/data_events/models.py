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
    session_id = models.CharField(max_length=255)

    def __str__(self):
        if self.user_id:
            return f"{self.user_id} - {self.event_type} - {self.url}"
        else:
            return f"{self.session_id} - {self.event_type} - {self.url}"


class Purchase(models.Model):
    user_id = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    product_id = models.CharField(max_length=255, null=True, blank=True)
    amount = models.FloatField()
    utm_source = models.CharField(max_length=255, blank=True)
    utm_medium = models.CharField(max_length=255, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        if self.user_id:
            return f"{self.user_id} - {self.product_id} - {self.utm_medium}"
        else:
            return f"{self.session_id} - {self.product_id} - {self.utm_medium}"

    def Meta(self):
        verbose_name_plural = "Purchases"
        Verbose_name = "Purchase"
