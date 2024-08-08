from django.urls import path

from db_connection import views

urlpatterns = [
    path('', views.connection, name='connection'),

]
