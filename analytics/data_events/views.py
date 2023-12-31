from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from analytics.data_events.models import Event, Purchase


@method_decorator(csrf_exempt, name="dispatch")
class EventCaptureView(View):
    def post(self, request, *args, **kwargs):
        # Get the session ID, event type, URL, and UTM source and medium from the POST request
        session_id = request.POST.get("session_id")
        event_type = request.POST.get("event_type")
        user_id = request.POST.get("user_id", "")
        url = request.POST.get("url")
        utm_source = request.POST.get("utm_source", "")
        utm_medium = request.POST.get("utm_medium", "")

        # Create a new Event object with the captured data
        Event.objects.create(
            session_id=session_id,
            event_type=event_type,
            url=url,
            utm_source=utm_source,
            utm_medium=utm_medium,
            user_id=user_id,
        )

        # Return a success response
        return JsonResponse({"status": "success"})


@method_decorator(csrf_exempt, name="dispatch")
class PurchaseCaptureView(View):
    def post(self, request, *args, **kwargs):
        # Get the session ID, product ID, amount, and UTM source and medium from the POST request
        session_id = request.POST.get("session_id")
        product_id = request.POST.get("product_id")
        amount = float(request.POST.get("amount"))
        utm_source = request.POST.get("utm_source", "")
        utm_medium = request.POST.get("utm_medium", "")
        user_id = request.POST.get("user_id", "")

        # Create a new Purchase object with the captured data
        Purchase.objects.create(
            session_id=session_id,
            product_id=product_id,
            amount=amount,
            utm_source=utm_source,
            utm_medium=utm_medium,
            user_id=user_id,
        )

        # Return a success response
        return JsonResponse({"status": "success"})
