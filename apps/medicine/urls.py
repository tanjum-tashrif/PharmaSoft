from django.urls import path
from apps.medicine.views import *

urlpatterns = [
    path("", medicine_details, name="medicine_details"), # medicine
    path("list/", medicine, name="medicine_list"), # medicine
    path("add/", medicine_add, name="medicine_add"), 
    path("category", category, name="category_list"), 
    path("category/add/", category_add, name="category_add"),
    path("unit", unit_list, name="unit_list"), 
    path("unit/add/", unit_add, name="unit_add"),
    path("type", type_list, name="type_list"), 
    path("type/add/", type_add, name="type_add"),
    path("leaf", leaf_list, name="leaf_list"), 
    path("leaf/add/", leaf_add, name="leaf_add"),
    
]