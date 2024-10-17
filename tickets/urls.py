from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_site, name="main-view"),
    path('oferta/', views.offer_site, name="offer"),
    path('formularz/', views.get_job_form, name='form'),
    path("webhook/stripe/", views.webhook, name="stripe-webhook"),
    path('payment_advance/<str:order_uuid>', views.payment_advance, name="payment_advance"),
    path('logout/', views.logout_view, name='logout'),
    path('profil/', views.profile_view, name='profile'),
    path('logowanie/', views.login_view, name='login'),
    path('admin-panel/', views.admin_panel, name='admin-panel'),
    path('set-price/<str:order_uuid>', views.set_payment_price, name='set_price'),
    path('payment/<str:order_uuid>', views.payment, name='payment'),
    path('kontakt/', views.contact, name='contact'),
    path('oferta/<str:offer_name>/', views.offer_detail, name='offer_detail'),
    path('źródła', views.source, name='source')
]
