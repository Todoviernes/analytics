from django.contrib import admin

# Register your models here.
from analytics.data_events.models import Event, Purchase


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("event_type", "user_id", "url", "utm_source", "utm_medium", "session_id")


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("name", "user_id", "product_id", "amount", "utm_source", "utm_medium", "session_id")

    def name(self, obj):
        if obj.user_id:
            return f"{obj.user_id} - {obj.product_id} - {obj.utm_medium}"
        else:
            return f"{obj.session_id} - {obj.product_id} - {obj.utm_medium}"
