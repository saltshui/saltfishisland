from django.urls import path
from . import views
 
app_name = 'users'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('basiclogin/', views.BasicLoginView.as_view(), name='basiclogin'),
    
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/emailsent/done', views.EmailConfirmDoneView.as_view(), name='email_confirm_done'),
    
    path('reactive/', views.ReactiveView.as_view(), name='reactive'),
    path('reactive/emailsent/done', views.EmailConfirmDoneView.as_view(), name='email_reactive_done'),
    
    path('activate/<str:token>',views.active_user,name='active_user'),
    
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/emailsent/done', views.ResetEmailDoneView.as_view(), name='reset_email_done'),
    path('password_reset/<str:token>',views.PasswordResetConfirmView.as_view(),name='reset_confirm'),
   
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),

]