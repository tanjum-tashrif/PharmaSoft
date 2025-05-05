from django.shortcuts import render, redirect
from apps.supplier.models import Supplier
from apps.purchase.models import Purchase
from system.utils import paginate_data
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from apps.medicine.models import Medicine, Leaf
import json
from apps.payment.sslcommerz import sslcommerz_payment_gateway_purchase
from apps.payment.models import Payment
from apps.supplier.models import Supplier
from datetime import datetime
import random
import string              
from django.contrib.auth.decorators import login_required
from apps.user.models import User
from django.contrib import messages
from apps.medicine.models import Unit
from apps.medicine.models import MedicineBatch
# Create your views here.
def generate_invoice_no():
    # Get the current year (last two digits) and month
    current_year = datetime.now().strftime('%y')  # e.g., '24' for 2024
    current_month = datetime.now().strftime('%m')  # e.g., '11' for November

    # Retrieve the last Payment object's ID, default to 0 if no payments exist
    try:
        last_payment = Purchase.objects.latest('id')
        last_id = last_payment.id + 1
    except Payment.DoesNotExist:
        last_id = 1

    # Increment the last ID and pad it with leading zeros
    print('last id : ', last_id)
    new_id = last_id + 1
    padded_id = str(new_id).zfill(8)  # Ensures the ID is always 8 digits

    # Return the generated invoice number
    return f"PR-{current_year}{current_month}{padded_id}"

def purchase_list(request):
    if request.method == 'POST':
        data = Purchase.objects.all()
        print('Purchase data : ', data)
        response_data, page_data = paginate_data(Purchase, data, request)
        count = 0
        for data in page_data:
            count += 1
            action_html = f'<a href="/purchase/purchase_print/{data.invoice_no}/" style="margin-right: 5px; font-size: 22px;"><i class="fas fa-eye"></i></a>'
            response_data['data'].append({
                'count' : count,
                'id' : data.id,
                'supplier_name' : data.supplier.name,
                'invoice_no' : data.invoice_no,
                'medicine_info' : data.medicine_info.name,
                'batch_id' : data.batch_id,
                'expire_date' : data.expire_date,
                'total_quantity' : data.total_quantity,
                'supplier_price' : data.supplier_price,
                'total_price' : data.total_price,
                'paid_amount' : data.paid_amount,
                'due_amount' : data.due_amount,
                'action' : mark_safe(action_html),
            })
        return JsonResponse(response_data)
    return render(request, 'backend/main/purchase/purchase_list.html')

# add purchase
def add_purchase(request):
    context={}
    supplier = Supplier.objects.all()
    box_unit = Unit.objects.all()
    for name in box_unit: 
        print('unit name : ', name.name)
    leaf_unit = Leaf.objects.all()
   
    invoice_no = generate_invoice_no() 
    payment_types = {'1':'handcash', '2':'sslcommerz'}
    context = {
        'payment_type': payment_types,
        'suppliers': supplier,
        'invoice_no': invoice_no,
        'box_units': box_unit,
        'leaf_units': leaf_unit,
        'transaction_type': 'purchase'
    }
    print('purchase sessionkey : ', request.session.session_key)
    return render(request, 'backend/main/purchase/add_purchase.html', context=context)

def unique_transaction_id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@login_required
def purchase_process(request):
    print('purchase_process sessionkey : ', request.session.session_key)
    print('request purchase process : ', request.method)
    if request.user.is_authenticated : 
        print('--------authenticated user----------') 
    if request.method == 'POST':
        payment_type = request.POST.get('payment_type')
        customer_id = request.POST.get('supplier_name')
        invoice_no = request.POST.get('invoice_no')
        details = request.POST.get('details')
        paid_amount = request.POST.get('paid_amount')
        billing_type = request.POST.get('billing_type')
        print('billing type : ', billing_type)
        
        if customer_id : 
            customer = Supplier.objects.get( id= customer_id)
            customer_name = customer.name
            print('customer name : ', customer_name)
        else : 
            customer_name = 'walking_customer'

        print('---------payment info-----------')
        print('payment_type : ', payment_type)
        print('customer_name : ', customer_name)
        print('invoice_no : ', invoice_no)
        print('details : ', details)
        print('paid_amount : ', paid_amount)

        if payment_type == '1':  # Handcash
            print('handcash payment')
            messages.success = 'Purchase added successfully'
            return redirect('payment_list')
            
        if payment_type == '2':  # SSLCommerz
            transaction_id = unique_transaction_id_generator()
            transaction_data = {
                'customer_name': customer_name,
                'invoice_no': invoice_no,
                'details': details,
                'paid_amount': paid_amount,
                'transaction_id': transaction_id,
                'billing_type': billing_type,
                'payment_type': 'sslcommerz'
            }
            request.session['transaction_data'] = transaction_data

            return redirect(sslcommerz_payment_gateway_purchase(request, transaction_data))

    else :
        print('purchase process failed') 
        return redirect('dashboard')
    


@csrf_exempt
def purchase_success_view(request):
    print('------- payment success view ---------')
    print('purchase_success_view sessionkey : ', request.session.session_key)
    data = request.POST
    print('data -------', data)
    print('---------------------------'*30)
    print('status : ', data['status']) 
    if data['status'] == 'VALID':
        status = 1
    else : 
        status = 0
    
    customer_name = data.get('value_a', None)
    invoice_no = data.get('value_b', None)
    details = data.get('value_c', None)
    paid_amount = data.get('value_d', None)
    transaction_id = request.GET.get('value_e', None)
    payment_type = request.GET.get('value_f', None)
    transaction_type = request.GET.get('value_g', None)

    print(f'----------amount : {paid_amount} tranid : {transaction_id} pay_type: {payment_type}  tran_type : {transaction_type}------------')
    print(f"Payment Details: Amount: {paid_amount}, Transaction ID: {transaction_id}, "
          f"Payment Type: {payment_type}, Customer: {customer_name}, Invoice: {invoice_no}, "
          f"Details: {details}, Status: {status}")
    # user = request.user
    # print('user : ', user)
    # Save payment details
    payment = Payment.objects.create(
            customer_name=customer_name,
            invoice_number=invoice_no,
            payment_type=payment_type,
            transaction_type=transaction_type,
            transaction_id=transaction_id,
            amount_paid=float(paid_amount) if paid_amount else 0.0,
            status=status,
        )
    
    return redirect('payment_list')


def save_purchase_data(request):
    if request.method == "POST":
        # Retrieve form data from the request
        supplier_id = request.POST.get("supplier_name")
        invoice_no = request.POST.get("invoice_no")
        details = request.POST.get("details")
        payment_type = request.POST.get("payment_type")
        
        # Retrieve the totals data from the request
        sub_total = request.POST.get("sub_total")
        discount = request.POST.get("discount")
        grand_total = request.POST.get("grand_total")
        paid_amount = request.POST.get("paid_amount")
        due_amount = request.POST.get("due_amount")

        # Debug: Print the received totals
        print("Sub Total:", sub_total)
        print("Discount:", discount)
        print("Grand Total:", grand_total)
        print("Paid Amount:", paid_amount)
        print("Due Amount:", due_amount)

        # Retrieve and prepare the medicines data
        medicine_names = request.POST.getlist("medicine_name[]")
        batch_ids = request.POST.getlist("batch_id[]")
        expire_dates = request.POST.getlist("expire_date[]")
        box_units = request.POST.getlist("box_units[]") 
        # total_quantities = request.POST.getlist("total_quantity[]")
        box_quantities = request.POST.getlist("box_quantity[]")
        leaf_units = request.POST.getlist("leaf_units[]") 
        supplier_prices = request.POST.getlist("supplier_price[]")
        box_mrps = request.POST.getlist("box_mrp[]")
        total_prices = request.POST.getlist("total_price[]")


        # Debug: Print the received data
        print("Supplier ID : ", supplier_id)
        print("medicine_names : ", medicine_names)
        print("batch_ids : ", batch_ids)
        print("expire_dates :", expire_dates)
        print("box_units :", box_units)
        print("box_quantities :", box_quantities)
        print("leaf_units :", leaf_units)
        print("supplier_prices :", supplier_prices)
        print("box_mrps:", box_mrps)
        print("total_prices:", total_prices)
        print("Payment Type:", payment_type)

        # Get the supplier object
        try:
            supplier = Supplier.objects.get(id=supplier_id)
        except Supplier.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Supplier not found."})

        # Process each medicine batch
        for i in range(len(medicine_names)):
            try:
                medicine = Medicine.objects.get(id=medicine_names[i])
                box_unit = Unit.objects.get(id=box_units[i])
                leaf_unit = Leaf.objects.get(id=leaf_units[i])
            except (Medicine.DoesNotExist, Unit.DoesNotExist, Leaf.DoesNotExist) as e:
                return JsonResponse({"status": "error", "message": str(e)})

            # Calculate stock at the tablet level
            box_quantity = int(box_quantities[i])
            total_stock = box_quantity * box_unit.unit_value * leaf_unit.quantity

            # Check if a batch exists for the medicine and batch_id
            medicine_batch = MedicineBatch.objects.filter(
                medicine=medicine,
                batch=batch_ids[i]
            ).first()

            if medicine_batch:
                # Update stock and expiry if batch exists
                medicine_batch.stock += total_stock
                medicine_batch.expire_date = expire_dates[i]  # Update expiry if necessary
                medicine_batch.supplier_price = supplier_prices[i]
                medicine_batch.box_mrp = box_mrps[i]
                medicine_batch.save()
            else:
                # Create a new batch if it does not exist
                MedicineBatch.objects.create(
                    medicine=medicine,
                    batch=batch_ids[i],
                    expire_date=expire_dates[i],
                    stock=total_stock,
                    supplier_name=supplier,
                    supplier_price=supplier_prices[i],
                    box_mrp=box_mrps[i],
                    leaf = leaf_unit, 
                    unit = box_unit,
                    admin_id=User.objects.get(id=request.user.id)
                )

            # Save purchase record
            purchase = Purchase(
                supplier=supplier,
                invoice_no=invoice_no,
                details=details,
                payment_type=payment_type,
                medicine_info=medicine,
                batch_id=batch_ids[i],
                expire_date=expire_dates[i],
                box_quantity=box_quantity,
                supplier_price=supplier_prices[i],
                box_mrp=box_mrps[i],
                total_price=total_prices[i],
                paid_amount=paid_amount,
                due_amount=due_amount,
                admin_id=User.objects.get(id=request.user.id)
            )
            purchase.save()

        return redirect("purchase_print", invoice_no=invoice_no)

    return JsonResponse({"status": "error", "message": "Invalid request method."})


def fetch_medicines_by_supplier(request):
    supplier_id = request.GET.get('supplier_id')
    print('supplier id : ', supplier_id)
    if supplier_id:
        medicines = Medicine.objects.filter(supplier_name__id=supplier_id)
        
        medicine_list = [
            {"id": medicine.id, "name": medicine.name}
            for medicine in medicines
        ]
        print('medicine list : ', medicine_list)
        return JsonResponse({"medicines": medicine_list})
    
    return JsonResponse({"medicines": []})

def purchase_print(request, invoice_no):
    context = {}
    invoices = Purchase.objects.filter(invoice_no=invoice_no)
    print('purchase invoice : ', invoices)

    if invoices.exists():
        first_invoice = invoices.first()
        supplier = first_invoice.supplier  
        supplier_name = supplier.name if supplier else "N/A"
        supplier_phone = supplier.phone_no if supplier else "N/A"
        supplier_address = supplier.address if supplier else "N/A"
        created_at = first_invoice.created_at.strftime('%Y-%m-%d')

        invoice_items = []
        sub_total = 0
        for item in invoices:
            invoice_items.append({
                'medicine_name': item.medicine_info.name if item.medicine_info else "N/A",
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
            'supplier_name': supplier_name,
            'supplier_phone': supplier_phone,
            'supplier_address': supplier_address,
            'created_at': created_at,
            'invoice_items': invoice_items,
            'sub_total': sub_total,
            'paid_amount': paid_amount,
            'due_amount': due_amount,
            'today_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    return render(request, 'backend/main/purchase/purchase_print.html', context=context)





