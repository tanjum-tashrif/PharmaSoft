from django.urls import path, include
from apps.user.views import *

urlpatterns = [
    path('', user_list, name='user_list'), #user/
    path('add/', user_add, name='user_add'),
    path('edit/<int:id>', user_edit, name='user_edit'),
    path('delete/<int:id>', user_delete, name='user_edit'),
    path('role/', role, name='role_list'),
    path('role_json/', role_json, name='role_json'),
    path('role/add/', role_add, name='role_add'),
    path('role/edit/<int:id>', role_edit, name='role_edit'),
    path('role/delete/<int:id>', role_delete, name='role_delete'),
]