from django.urls import path
from apps.invoice.views import *
# from apps.payment.sslcommerz import sslcommerz_payment_gateway, sslcommerz_success
urlpatterns = [
    path('', invoice_list, name="ivnoice_list"),
    path("add/", invoice_add, name="add_invoice"),
    path('save_invoice_data/', save_invoice_data, name='save_invoice_data'),
    path('invoice_print/<str:invoice_no>/', invoice_print, name='invoice_print'),
    path('get_medicine_details/', get_medicine_details, name='get_medicine_details'),
]