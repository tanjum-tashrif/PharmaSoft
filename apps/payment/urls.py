from django.urls import path
from apps.purchase.views import *
from apps.payment.views import *
from apps.payment.sslcommerz import *
urlpatterns = [
    # path('', sslcommerz_payment_gateway, name='sslcommerz_payment_gateway'), #payment/
    # path('success/', sslcommerz_success, name='sslcommerz_success'),
    path('', payment_list, name='payment_list'),
    path('cancel/', payment_cancel, name='payment_cancel'),
    path('fail/', payment_fail, name='payment_fail'),
]
