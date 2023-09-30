from django.urls import path

from analytics.data_events.views import EventCaptureView, PurchaseCaptureView

app_name = "data_events"

urlpatterns = [
    path("capture_event/", EventCaptureView.as_view(), name="capture_event"),
    path("capture_purchase/", PurchaseCaptureView.as_view(), name="capture_purchase"),
]
