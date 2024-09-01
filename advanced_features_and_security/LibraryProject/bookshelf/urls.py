# urls for or view path

from django.urls import path

from . import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.create_book, name='create_book'),
    path('books/edit/', views.edit_book, name='edit_book'),
    path('books/delete/', views.delete_book, name='delete_book'),
    path('example_form/', views.example_form, name='example_form'),
]
