import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms.job_form import JobForm
from .forms.contact_form import ContactForm
from django.core.mail import send_mail
from .models import Order, Offer
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .payments.advance_payment_creator import AdvancePaymentCreator
from .payments.payment_creator import PaymentCreator
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core import serializers


def main_site(request):
    return render(request, "tickets/main_site.html")


def offer_site(request):
    data = "oferta"
    return render(request, "tickets/offer.html", context={"data": data})


# Create your views here.
@login_required()
def get_job_form(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        price = request.POST.get("js_price_value")
        if form.is_valid():
            fly_continent = form.cleaned_data['trip_target']
            name = form.cleaned_data['your_name']
            whatsapp = form.cleaned_data['whatsapp']
            account_email = request.user.email
            contact_email = form.cleaned_data['email']
            trip_option = form.cleaned_data['trip_option']
            city = form.cleaned_data['city']
            target_city = form.cleaned_data['target_city']
            other_cities = form.cleaned_data['cities']
            number_of_passengers = form.cleaned_data['number_of_people']
            out_date = form.cleaned_data['out_date']
            back_date = form.cleaned_data['back_date']
            luggage = form.cleaned_data['luggage']
            fly_class = form.cleaned_data['fly_class']
            max_price = form.cleaned_data['max_price']
            number_of_offers = form.cleaned_data['number_of_offers']
            additional_information = form.cleaned_data['additional_information']

            order = Order(
                fly_continent=fly_continent,
                your_name=name,
                account_email=account_email,
                contact_email=contact_email,
                whatsapp=whatsapp,
                trip_option=trip_option,
                city=city,
                target_city=target_city,
                other_cities=other_cities,
                number_of_passengers=number_of_passengers,
                out_date=out_date,
                back_date=back_date,
                luggage=luggage,
                fly_class=fly_class,
                max_price=max_price,
                number_of_offers=number_of_offers,
                additional_information=additional_information,
                payment_advance_value=price,

            )
            order.save()
            send_mail(
                'Zamówienie',
                f"Kontynent: {fly_continent}\nImie: {name}\nemail: {contact_email}\nwhatsapp: {whatsapp}\nJedna czy dwie strony: {trip_option}\nMiasto: {city}\n"
                f"Miasto docelowe: {target_city}\nInne miasta: {other_cities}\nLiczba osób: {number_of_passengers}\nData wylotu: {out_date}\nData powrotu: {back_date}\nBagaż: {luggage}\n"
                f"Klasa lotu: {fly_class}\nMax cena: {max_price}\nLiczba ofert:{number_of_offers}\nDodatkowe informacje: {additional_information}\n",
                account_email,
                ['cheapticketspl123@gmail.com'],
            )
            return redirect('payment_advance', order.uuid)
    else:
        form = JobForm()
    return render(request, "tickets/job_form.html", {"form": form})


def payment_advance(request, order_uuid):
    order = Order.objects.get(uuid=order_uuid)
    advance_payment_creator = AdvancePaymentCreator(order)
    stripe_payment = advance_payment_creator.create()
    return render(request, "tickets/payment_advance.html", {"stripe_payment": stripe_payment})


def payment(request, order_uuid):
    order = Order.objects.get(uuid=order_uuid)
    payment_creator = PaymentCreator(order)
    stripe_payment = payment_creator.create()
    return render(request, "tickets/payment_advance.html", {"stripe_payment": stripe_payment})


endpoint_secret = settings.ENDPOINT_SECRET


@csrf_exempt
@require_POST
def webhook(request):
    event = None
    payload = request.body

    try:
        event = json.loads(payload)
    except Exception as e:
        print('⚠️ Webhook error while parsing basic request.' + str(e))
        return JsonResponse({'success': False})

    if endpoint_secret:
        # Only verify the event if there is an endpoint secret defined
        # Otherwise use the basic event deserialized with json
        sig_header = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except stripe.error.SignatureVerificationError as e:
            print('⚠️ Webhook signature verification failed.' + str(e))
            return JsonResponse({'success': False})

    # Handle the event
    if event and event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        print('Payment for {} succeeded'.format(payment_intent['amount']))
        print(payment_intent)
        order_id = payment_intent["id"]
        if Order.objects.filter(payment_advance_id=order_id):
            order = Order.objects.get(payment_advance_id=order_id)
            order.payment_advance_status = "Zapłacone"
            order.save()
        elif Order.objects.get(payment_id=order_id):
            order = Order.objects.get(payment_id=order_id)
            order.payment_status = "Zapłacone"
            order.save()
        # Then define and call a method to handle the successful payment intent.
        # handle_payment_intent_succeeded(payment_intent)
    elif event['type'] == 'payment_method.attached':
        payment_method = event['data']['object']  # contains a stripe.PaymentMethod
        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)
    else:
        # Unexpected event type
        print('Unhandled event type {}'.format(event['type']))

    return JsonResponse({'success': True})


def logout_view(request):
    logout(request)
    return redirect("main-view")


def login_view(request):
    return render(request, "tickets/login.html")


@login_required()
def profile_view(request):
    try:
        orders = Order.objects.filter(account_email=request.user.email).order_by('-id')
        json_serializer = serializers.get_serializer("json")()
        json_orders = json_serializer.serialize(Order.objects.filter(account_email=request.user.email).order_by('-id'))

    except Order.DoesNotExist:
        return render(request, "tickets/profile.html")

    return render(request, "tickets/profile.html", context={"orders": orders, "json_orders": json_orders})


@staff_member_required()
@login_required()
def admin_panel(request):
    orders = Order.objects.all().order_by('-id')

    return render(request, "tickets/admin_panel.html", context={"orders": orders})


def set_payment_price(request, order_uuid):
    if request.method == 'POST':
        try:
            order = Order.objects.get(uuid=order_uuid)

            new_price = request.POST.get('price')
            order.payment_status = "Nie zapłacone"
            order.payment_value = new_price
            order.save()

        except Order.DoesNotExist:
            pass

    return redirect("admin-panel")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        name = form['name'].value()
        whatsapp = form['whatsapp'].value()
        email = form['email'].value()
        message = form['message'].value()
        send_mail(
            'Formularz kontaktowy',
            f"Imie: {name}\nemail: {email}\nwhatsapp: {whatsapp}\nwiadomość: {message}",
            'cheapticketspl123@gmail.com',
            ['cheapticketspl123@gmail.com'],
        )
        return redirect('contact')
    else:
        form = ContactForm()
        return render(request, "tickets/contact.html", {"form": form})


def offer_detail(request, offer_name):
    offer = Offer.objects.get(name=offer_name)
    return render(request, "tickets/offer_detail.html", {"offer": offer})


def source(request):
    return render(request, 'tickets/source.html')
