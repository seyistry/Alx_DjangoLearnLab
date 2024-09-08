from django.urls import path
from .views import ListBookView, DetailBookView, CreateBookView, UpdateBookView, DeleteBookView

urlpatterns = [
	path('books/', ListBookView.as_view(), name='book-list'),
	path('books/<int:pk>/', DetailBookView.as_view(), name='book-detail'),
	path('books/create/', CreateBookView.as_view(), name='book-create'),
	path('books/update/<int:id>/', UpdateBookView.as_view(), name='book-update'),
	path('books/delete/<int:id>/', DeleteBookView.as_view(), name='book-delete')
]