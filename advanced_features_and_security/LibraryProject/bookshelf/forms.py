from django import forms
from .models import Book

# create forms.py
class BookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ['title', 'author', 'genre', 'description']