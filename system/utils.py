from django.core.paginator import Paginator
import os
import json
from datetime import datetime

def paginate_data(model, data, request):
    if request.POST:
        search_value = request.POST.get('search[value]')
    else:
        search_value = request.GET.get('search[value]')


    if search_value:
        data = model.objects.search_by_data(search_value)

    order_column = int(request.GET.get('order[0][column]', 0))
    order_dir = request.GET.get('order[0][dir]', 'asc')

    if order_column:
        column_name = request.GET.get(f'columns[{order_column}][data]')
        reverse_data = False
        if order_dir == 'desc':
            reverse_data = True
        data = sorted(data, key=lambda p: getattr(p, column_name), reverse=reverse_data)
    if request.method == 'POST':
        start = request.POST.get('start')
        length = request.POST.get('length')
    else:
        start = request.GET.get('start')
        length = request.GET.get('length')

    if start and length:
        page = int(start) // int(length) + 1
    else:
        page = 0

    per_page = str(length if length else 25)
    paginator = Paginator(list(data), per_page)
    page_data = paginator.get_page(page)

    response_data = {
        'draw': request.GET.get('draw'),
        'recordsTotal': data.count(),
        'recordsFiltered': paginator.count,
        'data': []
    }
    if request.method == 'POST':
        response_data['draw'] = request.POST.get('draw')
    return response_data, page_data

def prepare_menu_item():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_file_path = os.path.join(base_dir, 'system', 'menu', 'main.json')

    with open(json_file_path, 'r') as menu_file:
        menu_data = json.load(menu_file)

    updated_menu = []
    # Logic for filtering based on user permissions would go here...

    for value in menu_data['menuItems']:
        updated_menu.append(value)  # Simplified for demonstration

    return updated_menu

def convert_date_string_to_django_date(date_string):
    date_formats = ['%d-%b-%Y', '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%b %d, %Y', '%b %d %Y', '%B %d, %Y', '%B %d %Y']
    for date_format in date_formats:
        try:
            date = datetime.strptime(date_string, date_format)
            return date.strftime('%Y-%m-%d')
            # Convert the date to Django model format and return it as a string
        except ValueError:
            pass


def convert_time_string_to_django_time(time_string):
    time_formats = ['%I:%M %p', '%H:%M:%S', '%I:%M:%S %p', '%H:%M']
    for time_format in time_formats:
        try:
            time = datetime.strptime(time_string, time_format)
            return time.strftime('%H:%M:%S')
            # Convert the time to Django model format and return it as a string
        except ValueError:
            pass
