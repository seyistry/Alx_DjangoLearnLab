```
from bookshelf.models import Book

# Creating a new Book instance
new_book = Book.objects.create(
    title="Learning Django",
    author="Jane Doe",
    published_date="2023-08-11",
    isbn="9876543210123"
)
```