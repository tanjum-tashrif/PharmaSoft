from django.shortcuts import render
from apps.supplier.models import Supplier
from apps.medicine.models import Medicine, MedicineBatch
from datetime import timedelta
from django.utils.timezone import now
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from datetime import datetime
from dateutil.relativedelta import relativedelta 
# Create your views here.

def calculate_growth_and_progress(current_count, model, date_field="created_at"):
    last_month_start = (now() - timedelta(days=30)).replace(day=1)
    previous_count = model.objects.filter(**{f"{date_field}__lt": last_month_start}).count()

    if previous_count > 0:
        growth_percentage = ((current_count - previous_count) / previous_count) * 100
    else:
        growth_percentage = 100  

    progress_width = min(max((growth_percentage / 200) * 100, 0), 100)  # Scaled to 0-100%

    return round(growth_percentage, 1), round(progress_width, 1)


def dashboard(request):
    context = {}
    print('dashboard sessionkey : ', request.session.session_key)

    # Suppliers card
    suppliers = Supplier.objects.all().count()
    supplier_growth, supplier_progress = calculate_growth_and_progress(
        current_count=suppliers,
        model=Supplier,
        date_field="created_at"
    )

    # Medicines card
    medicines = Medicine.objects.all().count()
    medicine_growth, medicine_progress = calculate_growth_and_progress(
        current_count=medicines,
        model=Medicine,
        date_field="created_at"
    )

    # out of stock medicines 
    # out_of_stock_medicines = Medicine.objects.filter(stock=0).count()
    out_of_stock_medicines = MedicineBatch.objects.filter(stock=0).count()
    print('out_of_stock_medicines : ', out_of_stock_medicines)

    # expired medicines 
    # expired_medicines = Medicine.objects.filter(expire_date__lt=now()).count()
    expired_medicines = MedicineBatch.objects.filter(expire_date__lt=now()).count()
    # Context
    context = {
        'tota_suppliers': suppliers,
        'growth_percentage_supplier': supplier_growth,
        'progress_width_supplier': supplier_progress,
        'total_medicines': medicines,
        'growth_percentage_medicine': medicine_growth,
        'progress_width_medicine': medicine_progress,
        'out_of_stock_medicines': out_of_stock_medicines,
        'expired_medicines': expired_medicines,

    }

    print('context : ', context)
    return render(request, 'backend/dashboard/dashboard1.html', context=context)

def medicine_monthly_counts(request):
    # Get the current date
    print('call received of medicine_monthly_counts')
    end_date = datetime.now()
    # Create the start date (12 months back, including the current month)
    start_date = end_date - relativedelta(months=11)

    # Query medicines created in the range of the last 12 months
    medicines = Medicine.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    ).annotate(month=TruncMonth('created_at')) \
     .values('month') \
     .annotate(count=Count('id')) \
     .order_by('month')

    # Generate a list of all months in the range
    monthly_counts = {}
    for i in range(12):
        month_date = start_date + relativedelta(months=i)
        month_year = month_date.strftime("%B %Y")
        monthly_counts[month_year] = 0

    # Fill in counts for each month where data exists
    for entry in medicines:
        month_year = entry['month'].strftime("%B %Y")
        monthly_counts[month_year] = entry['count']

    # Return JSON response with keys (months) and values (counts)
    return JsonResponse({
        'keys': list(monthly_counts.keys()),
        'values': list(monthly_counts.values()),
    })