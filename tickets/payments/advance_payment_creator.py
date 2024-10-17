import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class AdvancePaymentCreator:
    def __init__(self, order):
        self.order = order

    def create(self):
        if self.order.payment_advance_id:
            payment_intent = stripe.PaymentIntent.retrieve(
                self.order.payment_advance_id,
            )
            return payment_intent

        else:
            payment_intent = stripe.PaymentIntent.create(
                amount=self.order.payment_advance_value,
                currency='PLN',
            )
            self.order.payment_advance_id = payment_intent.id
            self.order.save()
            return payment_intent
