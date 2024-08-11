```
from bookshelf.models import Book

# Delete the book you created and confirm the deletion by trying to retrieve all books again
book = Book.objects.get(id=1)
book.delete()
```
