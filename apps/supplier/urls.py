from django.urls import path
from apps.supplier.views import supplier, add, edit

urlpatterns = [
    path("", supplier, name="supplier_list"), # supplier
    path("add/", add, name="supplier_add"),
    path("edit/<int:id>/", edit, name="supplier_edit"),
    
]