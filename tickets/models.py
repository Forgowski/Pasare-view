import uuid
from django.db import models


class Order(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4 )
    your_name = models.CharField(max_length=100, default="null")
    whatsapp = models.CharField(max_length=100, default="null", blank=True)
    account_email = models.CharField(max_length=100, default="null")
    contact_email = models.CharField(max_length=100, default="null")
    trip_option = models.CharField(max_length=100, default="null")
    fly_class = models.CharField(max_length=100, default="null")
    fly_continent = models.CharField(max_length=100, default="null")
    city = models.CharField(max_length=100, default="null")
    target_city = models.CharField(max_length=100, default="null")
    other_cities = models.CharField(max_length=300, default="null", blank=True)
    number_of_passengers = models.IntegerField(default=0)
    out_date = models.CharField(max_length=100, default="null")
    back_date = models.CharField(max_length=100, default="null", null=True, blank=True)
    luggage = models.CharField(max_length=100, default="null")
    max_price = models.CharField(max_length=100, default="null")
    number_of_offers = models.IntegerField(default=2)
    additional_information = models.TextField(default="null")

    payment_advance_id = models.CharField(max_length=100)
    payment_advance_value = models.IntegerField(null=True, default=None)
    payment_advance_status = models.CharField(max_length=100, default='Nie zapłacone')

    payment_id = models.CharField(max_length=100, blank=True)
    payment_value = models.IntegerField(null=True, default=None, blank=True)
    payment_status = models.CharField(max_length=100, default='Nie określone')


# Create your models here.
class Offer(models.Model):
    name = models.CharField(max_length=100, default="null", primary_key=True)
    title = models.CharField(max_length=100, default="null")
    background = models.CharField(max_length=100, default="null")
    from_where = models.CharField(max_length=100, default="null")
    to_where = models.CharField(max_length=100, default="null")
    when = models.DateField(max_length=100, default="2020-01-01")
    return_date = models.DateField(max_length=100, default="2020-01-01")
    transfers = models.IntegerField(default=None)
    link = models.CharField(max_length=300, default="null")
