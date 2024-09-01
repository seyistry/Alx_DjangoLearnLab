from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import permission_required
from .forms import ExampleForm
from .models import Book


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    return render(request, 'bookshelf/book_list.html', {'books': Book})


@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    return render(request, 'bookshelf/book_list.html', {'books': Book})


@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request):
    return render(request, 'bookshelf/book_list.html', {'books': Book})


@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request):
    return render(request, 'bookshelf/book_list.html', {'books': Book})


@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request):
    return render(request, 'bookshelf/book_list.html', {'books': Book})


def example_form(request):
    form = ExampleForm()
    return render(request, 'bookshelf/form_example', {'form': form})
