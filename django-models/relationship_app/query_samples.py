from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author.
author_name = "author_name"
author = Author.objects.get(name=author_name)
author_books = author.objects.filter(author=author)

# List all books in a library.
library_name = Library.objects.books.all()
library_books = Library.objects.get(name=library_name)

# Retrieve the librarian for a library.
librarian = Librarian.objects.get(name='library_name')
