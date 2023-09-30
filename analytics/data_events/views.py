from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from analytics.data_events.models import Event, Purchase


@method_decorator(csrf_exempt, name='dispatch')
class EventCaptureView(View):
    def post(self, request, *args, **kwargs):
        session_id = request.POST.get('session_id')
        event_type = request.POST.get('event_type')
        url = request.POST.get('url')
        utm_source = request.POST.get('utm_source', '')
        utm_medium = request.POST.get('utm_medium', '')

        Event.objects.create(
            session_id=session_id,
            event_type=event_type,
            url=url,
            utm_source=utm_source,
            utm_medium=utm_medium,
        )

        return JsonResponse({"status": "success"})


@method_decorator(csrf_exempt, name='dispatch')
class PurchaseCaptureView(View):
    def post(self, request, *args, **kwargs):
        session_id = request.POST.get('session_id')
        product_id = request.POST.get('product_id')
        amount = float(request.POST.get('amount'))
        utm_source = request.POST.get('utm_source', '')
        utm_medium = request.POST.get('utm_medium', '')

        Purchase.objects.create(
            session_id=session_id,
            product_id=product_id,
            amount=amount,
            utm_source=utm_source,
            utm_medium=utm_medium,
        )

        return JsonResponse({"status": "success"})
