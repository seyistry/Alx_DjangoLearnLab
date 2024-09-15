from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView
from . import views  # for custom views like registration and profile

urlpatterns = [
    # Django built-in login/logout views
    path('', TemplateView.as_view(template_name='blog/base.html'), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Custom views for registration and profile
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]