from django.urls import path,re_path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.FrontView.as_view(), name='front'),
    path('contact', views.ContactView.as_view(), name='contact'),
    path('index', views.IndexView.as_view(), name='index'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archive'),
    path('categories/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('tags/<int:pk>/', views.TagView.as_view(), name='tag'),
]