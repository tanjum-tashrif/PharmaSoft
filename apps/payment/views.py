from django.shortcuts import render
from apps.payment.models import Payment
from django.shortcuts import render, redirect
from apps.medicine.forms import MedicinAddForm, CategoryForm, UnitForm, TypeForm, LeafForm
from apps.medicine.models import Medicine, Category, Unit, Type, Leaf
from system.utils import paginate_data
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.contrib import messages
from apps.supplier.models import Supplier
# Create your views here.
def payment_list(request):
    if request.method == 'POST':
        data = Payment.objects.all()
        print('Payment data : ', data)
        response_data, page_data = paginate_data(Payment, data, request)
        count = 0
        for data in page_data:
            count += 1
            status_html = 'Failed'
            if data.status=='1':
                status_html = 'Success'
            response_data['data'].append({
                'count' : count,
                'id' : data.id,
                'customer_name' : data.customer_name,
                'invoice_number' : data.invoice_number,
                'transaction_type' : data.transaction_type,
                'transaction_id' : data.transaction_id,
                'amount_paid' : data.amount_paid,
                'status' : mark_safe(status_html),
                'action' : ''
            })
        return JsonResponse(response_data)
    return render(request, 'backend/main/payment/payment_list.html')