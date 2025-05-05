from django.shortcuts import render, redirect
from apps.supplier.models import Supplier
from apps.purchase.models import Purchase
from system.utils import paginate_data
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from apps.medicine.models import Medicine, Leaf, Unit, Category, Type, MedicineBatch
import json
from apps.payment.sslcommerz import sslcommerz_payment_gateway_purchase
from apps.payment.models import Payment
from apps.supplier.models import Supplier
from apps.invoice.models import Invoice
from datetime import datetime
from django.contrib import messages

def generate_invoice_no():
    # Get the current year (last two digits) and month
    current_year = datetime.now().strftime('%y')  # e.g., '24' for 2024
    current_month = datetime.now().strftime('%m')  # e.g., '11' for November

    # Retrieve the last Payment object's ID, default to 0 if no payments exist
    try:
        last_payment = Invoice.objects.latest('invoice_no') 
        last_id = last_payment.id
    except Payment.DoesNotExist:
        last_id = 0

    # Increment the last ID and pad it with leading zeros
    new_id = last_id + 1
    padded_id = str(new_id).zfill(8)  # Ensures the ID is always 8 digits

    # Return the generated invoice number
    return f"IN-{current_year}{current_month}{padded_id}"

# Create your views here.
def invoice_list(request):
    if request.method == 'POST':
        data = Invoice.objects.all()
        print('Invoice data : ', data)
        response_data, page_data = paginate_data(Invoice, data, request)
        count = 0
        for data in page_data:
            count += 1
            action_html = f'<a href="/invoice/invoice_print/{data.invoice_no}/" style="margin-right: 5px; font-size: 22px;"><i class="fas fa-eye"></i></a>'
            response_data['data'].append({
                'count' : count,
                'id' : data.id,
                'customer_name' : data.customer_name,
                'invoice_no' : data.invoice_no,
                'medicine_info' : data.medicine_info.medicine.name,
                'quantity' : data.box_quantity,
                'sell_price' : data.sell_price,
                'total_price' : data.total_price,
                'paid_amount' : data.paid_amount,
                'due_amount' : data.due_amount,
                'action' : mark_safe(action_html)
            })
        return JsonResponse(response_data)
    return render(request, 'backend/main/invoice/invoice_list.html')

def invoice_add(request):
    context={}
    # print('purchase sessionkey : ', request.session.session_key)
    medicines = MedicineBatch.objects.filter(stock__gt=0)
    print('medicines : ', medicines)
    medicine_name_batch_list = []
    for med in medicines:
        medicine_name = med.medicine.name
        medicine_batch = med.batch
        medicine_name_batch = {
            'id': med.id,
            'name': f'{medicine_name} - {medicine_batch}',
        }
        print('medicine_name_batch : ', medicine_name_batch)
        medicine_name_batch_list.append(medicine_name_batch)
    leaf = Leaf.objects.all()
    invoice_no = generate_invoice_no()
    payment_types = {'1':'handcash', '2':'sslcommerz'}
    context = {
        'medicine_name_batch_list' : medicine_name_batch_list,
        'payment_type': payment_types,
        'invoice_no': invoice_no,
        'leaf': leaf,
        'transaction_type': 'invoice'
    }
    return render(request, 'backend/main/invoice/add_invoice.html', context=context)

def get_medicine_details(request):
    medicine_id = request.GET.get('medicine_id')
    print('get medicine details medicine id : ', medicine_id)
    if not medicine_id:
        return JsonResponse({'error': 'Medicine ID not provided'}, status=400)

    try:
        medicine_batch = MedicineBatch.objects.get(id=medicine_id)
        data = {
            'price': medicine_batch.box_mrp/medicine_batch.leaf.quantity,
            'expire_date': medicine_batch.expire_date.strftime('%Y-%m-%d') if medicine_batch.expire_date else None,
        }
        return JsonResponse(data)
    except MedicineBatch.DoesNotExist:
        return JsonResponse({'error': 'Medicine not found'}, status=404)
    
def save_invoice_data(request):
    if request.method == "POST":
        # Retrieve form data from the request
        customer_name = request.POST.get("name")
        print('customer name : ', customer_name)
        invoice_no = request.POST.get("invoice_no")
        details = request.POST.get("details")
        payment_type = request.POST.get("payment_type")
        
        # Retrieve the totals data from the request
        sub_total = request.POST.get("sub_total")
        discount = request.POST.get("discount")
        grand_total = request.POST.get("grand_total")
        paid_amount = request.POST.get("paid_amount")
        due_amount = request.POST.get("due_amount")
        quantity = request.POST.get("quantity")

        # Debug: Print the received totals
        print("Sub Total:", sub_total)
        print("Discount:", discount)
        print("Grand Total:", grand_total)
        print("Paid Amount:", paid_amount)
        print("Due Amount:", due_amount)

        # Retrieve and prepare the medicines data
        medicine_name_batch = request.POST.getlist("medicine_name[]")
        # medicine_batch = 
        quantities = request.POST.getlist("quantity[]")
        prices = request.POST.getlist("price[]")
        total_prices = request.POST.getlist("total_price[]")

        # Debug: Print the received data
        print("medicine_names:", medicine_name_batch)
        print("total_prices :", total_prices)
        # print("Details:", details)
        # print("Payment Type:", payment_type)
        print("Medicine Quantity: ", quantities)


        # Store the purchase data
        for i in range(len(medicine_name_batch)):
            try:
                # Get related Medicine and Leaf objects
                medicine_obj = MedicineBatch.objects.get(id = medicine_name_batch[i])
                medicine_name = medicine_obj.medicine.name
                print('save invoice medicine name : ', medicine_name)
                
        #         # Create a new Purchase record
                invoice = Invoice(
                    customer_name=customer_name,
                    invoice_no=invoice_no,
                    details=details,
                    payment_type=payment_type,
                    medicine_info=medicine_obj,
                    box_quantity=quantities[i],
                    sell_price=prices[i],
                    total_price=total_prices[i],
                    paid_amount=paid_amount,
                    due_amount=due_amount
                )

        #         # Save the purchase to the database
                invoice.save()

                medicine_obj.stock -= int(quantities[i])
                medicine_obj.save()
                messages.success(request, "Invoice Add Successfully")
            except medicine_obj.DoesNotExist:
                return JsonResponse({"status": "error", "message": f"Medicine with ID {medicine_name_batch[i]} not found."})

        # Return a response after saving the data
        # messages.success(request, 'Invoice added successfully')
        # return redirect('invoice_print', invoice_no=invoice_no)
        return redirect('add_invoice')

    # If not a POST request, return an error
    return JsonResponse({"status": "error", "message": "Invalid request method."})

def invoice_print(request, invoice_no):
    context = {}
    invoices = Invoice.objects.filter(invoice_no=invoice_no)
    print('invoice invoice : ', invoices)

    if invoices.exists():
        first_invoice = invoices.first()
        customer_name = first_invoice.customer_name  
        created_at = first_invoice.created_at.strftime('%Y-%m-%d')

        invoice_items = []
        sub_total = 0
        for item in invoices:
            invoice_items.append({
                'medicine_name': item.medicine_info.medicine.name if item.medicine_info else "N/A",
                'medicine_expire': item.medicine_info.expire_date if item.medicine_info else "N/A",
                'quantity': getattr(item, 'box_quantity', 0),
                'supplier_price': getattr(item, 'supplier_price', 0),
                'total_price': getattr(item, 'total_price', 0),
            })
            sub_total += item.total_price
            paid_amount = item.paid_amount
            due_amount = item.due_amount

        # Context data
        context = {
            'invoice_no': invoice_no,
            'user_name': request.user.name,
            'user_phone': request.user.phone_no,
            'customer_name': customer_name,
            'created_at': created_at,
            'invoice_items': invoice_items,
            'sub_total': sub_total,
            'paid_amount': paid_amount,
            'due_amount': due_amount,
            'today_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    return render(request, 'backend/main/invoice/invoice_print.html', context=context)



