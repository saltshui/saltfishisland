from django.urls import path

from . import views

app_name = 'sendemail'
urlpatterns = [
    path('sendsubsemail/', views.SendSubEmail, name='sendemail'),
]