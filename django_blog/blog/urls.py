from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView
from . import views  # for custom views like registration and profile

urlpatterns = [
    # Django built-in login/logout views
    path('', TemplateView.as_view(template_name='blog/base.html'), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('posts/', views.postsListView.as_view(), name='posts'),
    path('post/new/', views.PostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>', views.postDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', views.postUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.postDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/comment/new/', views.CommentCreateView.as_view(), name='comment_new'),
    path('post/<int:pk>/comment/<int:pk2>/update/', views.CommentUpdateView.as_view(), name='comment_edit'),
    path('post/<int:pk>/comment/<int:pk2>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),

    # Custom views for registration and profile
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'), # profile view
	
]
