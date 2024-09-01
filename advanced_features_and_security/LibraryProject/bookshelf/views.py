from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import permission_required


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    return render(request, '<h1>View Books</h1>')

@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    return render(request, '<h1>Book created</h1>')

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request):
    return render(request, '<h1>Edit Book</h1>')

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request):
    return render(request, '<h1>Delete Book</h1>')
