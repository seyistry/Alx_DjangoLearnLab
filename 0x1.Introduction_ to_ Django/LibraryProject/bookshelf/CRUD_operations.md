```
>>> from bookshelf.models import Book
>>> new_book = Book.objects.create(
    title="Learning Django",
    author="Jane Doe",
    published_date="2023-08-11",
    isbn="9876543210123"
)
>>> print(books)
{'id': 1, 'title': '1984', 'author': 'George Orwell', 'publication_year': 1949}
>>> update_book = Book.objects.get(id=1)
>>> update_book.title = "Nineteen Eighty-Four"
>>> update_book.save()
>>> books = Book.objects.all().values().first()
>>> print(books)
{'id': 1, 'title': 'Nineteen Eighty-Four', 'author': 'George Orwell', 'publication_year': 1949}
>>> update_book.delete()
(1, {'bookshelf.Book': 1})
>>> books = Book.objects.all().values().first()
>>> print(books)
None
>>> 
```