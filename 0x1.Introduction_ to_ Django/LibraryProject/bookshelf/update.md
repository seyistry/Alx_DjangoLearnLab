```
from bookshelf.models import Book

# Update the title of “1984” to “Nineteen Eighty-Four” and save the changes
book = Book.objects.get(id=1)
book.title = "Nineteen Eighty-Four"
book.save()
```
