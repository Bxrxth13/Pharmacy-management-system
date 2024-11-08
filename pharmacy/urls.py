from django.urls import path
from .views import (
    home,
    medicine_list,
    add_medicine,
    delete_medicine,
    edit_medicine,
    wanted_stock,
    add_stock  # Make sure to import add_stock here if it's defined in views
)

urlpatterns = [
    path('', home, name='home'),
    path('medicines/', medicine_list, name='medicine_list'),
    path('add/', add_medicine, name='add_medicine'),
    path('delete/<int:id>/', delete_medicine, name='delete_medicine'),
    path('edit/<int:id>/', edit_medicine, name='edit_medicine'),
    path('wanted-stock/', wanted_stock, name='wanted_stock'),  # Your existing wanted stock view
    path('add-stock/', add_stock, name='add_stock'),  # Make sure this view is defined
]
