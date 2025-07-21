from django.urls import path
from . import views

urlpatterns = [
    path('', views.imp, name='importpunch'),
    path('conversion_excel/', views.conversion_excel, name='conversion_excel'),
    path('delete/<pk>', views.delete_conv, name='delete_conv'),
    path('edit/<pk>', views.edit_conv, name='edit_conv'),
    path('employees/', views.emp_details, name='emp_details')

]