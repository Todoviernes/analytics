from django.http import JsonResponse
from django.views import View
from .models import Event, Purchase


class CaptureEventView(View):
    def get(self, request, *args, **kwargs):
        event = Event.objects.create(
            event_type=request.GET.get('event_type'),
            user_id=request.GET.get('user_id'),
            url=request.GET.get('url'),
            utm_source=request.GET.get('utm_source', ''),
            utm_medium=request.GET.get('utm_medium', '')
        )
        return JsonResponse({"status": "success"})


class CapturePurchaseView(View):
    def get(self, request, *args, **kwargs):
        purchase = Purchase.objects.create(
            user_id=request.GET.get('user_id'),
            product_id=request.GET.get('product_id'),
            amount=float(request.GET.get('amount', 0)),
            utm_source=request.GET.get('utm_source', ''),
            utm_medium=request.GET.get('utm_medium', '')
        )
        return JsonResponse({"status": "success"})
