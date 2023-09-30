from django.test import TestCase
from django.urls import reverse

from analytics.data_events.models import Purchase


class PurchaseCaptureViewTestCase(TestCase):
    def test_purchase_capture_view(self):
        # Set up test data
        session_id = "12345"
        product_id = "67890"
        amount = 9.99
        utm_source = "test_source"
        utm_medium = "test_medium"

        # Make a POST request to the PurchaseCaptureView with the test data
        response = self.client.post(
            reverse("data_events:capture_purchase"),
            {
                "session_id": session_id,
                "product_id": product_id,
                "amount": amount,
                "utm_source": utm_source,
                "utm_medium": utm_medium,
            },
        )

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that a new Purchase object was created with the test data
        purchase = Purchase.objects.get(
            session_id=session_id,
            product_id=product_id,
            amount=amount,
            utm_source=utm_source,
            utm_medium=utm_medium,
        )
        self.assertIsNotNone(purchase)
