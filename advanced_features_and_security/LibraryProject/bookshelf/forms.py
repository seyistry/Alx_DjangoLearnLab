from django import forms
from .models import Book

# create forms.py
class ExampleForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ['title', 'author', 'publication_year']