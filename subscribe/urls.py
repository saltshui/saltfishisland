from django.urls import path

from . import views

app_name = 'subscribe'
urlpatterns = [
    path('list', views.SubscribeListView.as_view(), name='list'),
    path('update/', views.SubscribeUpdateView.as_view(), name='update'),
]