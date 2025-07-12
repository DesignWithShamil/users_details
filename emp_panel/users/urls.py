from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('users', views.users, name='users'),
    path('edit/<pk>', views.edit, name='edit'),
    path('delete/<pk>', views.delete, name='delete'),
    path('import/', views.impor, name='import'),
    path('export/', views.export_empinfo, name='export_empinfo'),
   

]