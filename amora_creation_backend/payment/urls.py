# urls.py
from django.urls import path
from .views import (
    PaymentInitiateView, 
    PaymentSimulateView, 
    payment_webhook_view,
)
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('initiate/', PaymentInitiateView.as_view(), name='payment-initiate'),
    path('simulate/', PaymentSimulateView.as_view(), name='payment-simulate'),
    path('webhook/', payment_webhook_view, name='payment-webhook'),
]