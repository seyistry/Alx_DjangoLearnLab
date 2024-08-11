```
from bookshelf.models import Book

# Retrieve and display all attributes of the book you just created.
books = Book.objects.all().values()
print(books)
```
