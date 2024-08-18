from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author.
author_books = Book.objects.filter(name='author_name')

# List all books in a library.
library_books = Library.objects.books.all()

# Retrieve the librarian for a library.
# librarian = Library.objects.get(name="library_name")
librarian = Library.objects.get(name="library_name")
