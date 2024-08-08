from django.urls import path

from db_connection import views

urlpatterns = [
    path('', views.home, name='home'),

]
