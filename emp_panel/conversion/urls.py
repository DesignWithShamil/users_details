from django.urls import path
from . import views

urlpatterns = [
    path('', views.imp, name='importpunch'),
    

]