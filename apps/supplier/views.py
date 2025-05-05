from django.shortcuts import render, redirect, get_object_or_404
from apps.supplier.forms import SupplierForm, SupplierEditForm
from apps.supplier.models import Supplier
from system.utils import paginate_data
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.contrib import messages
# Create your views here.
def supplier(request):
    if request.method == 'POST':
        data = Supplier.objects.all()
        print('Supplier data : ', data)
        response_data, page_data = paginate_data(Supplier, data, request)
        count = 0
        for data in page_data:
            count += 1
            action_html = f'<a href="/supplier/edit/{data.id}" style="margin-right: 5px; font-size: 22px;"><i class="fas fa-edit"></i></a>'            
            # Delete link with a space before and after
            # action_html += f'<a href="/user/delete/{data.id}" style="margin-left: 5px; font-size: 22px;"><i class="fa-solid fa-trash"></i></a>'
            status_html = 'InActivate'
            if data.status=='1':
                status_html = 'Activate'
            response_data['data'].append({
                'count' : count,
                'id' : data.id,
                'name' : data.name,
                'phone' : data.phone_no,
                'email' : data.email,
                'address' : data.address,
                'city' : data.city,
                'state' : data.state,
                'balance' : data.balance,
                'status' : mark_safe(status_html),
                'action' : mark_safe(action_html),
            })
        return JsonResponse(response_data)
    return render(request, 'backend/main/supplier/supplier_list.html')

def add(request):
    context = {}
    if request.method == 'POST':
        form = SupplierForm(request.POST, request=request)
        if form.is_valid():
            print('data : ', form.cleaned_data)
            form.save(commit=True)
            messages.success(request, f'Supplier has been added successfully.')
            return redirect('supplier_list')  
        else:
            print('Form Errors: ', form.errors)  
    else:
        form = SupplierForm(request=request)  
    
    context['form'] = form
    return render(request, 'backend/main/supplier/add.html', context=context)

def edit(request, id=None):
    context = {}
    print('supplier id : ', id)
    supplier = get_object_or_404(Supplier, id=id) if id else None
    
    if request.method == 'POST':
        form = SupplierEditForm(request.POST, instance=supplier)
        if form.is_valid():
            print('edit : ', form.cleaned_data)
            form.save()  
            messages.success(request, f'Supplier "{supplier.name}" has been edit successfully.')
            return redirect('supplier_list') 
    else:
        form = SupplierEditForm(instance=supplier)  
        
    context['form'] = form
    context['supplier'] = supplier
    context['user_data'] = Supplier.objects.all()  
    
    return render(request, 'backend/main/supplier/edit.html', context)


