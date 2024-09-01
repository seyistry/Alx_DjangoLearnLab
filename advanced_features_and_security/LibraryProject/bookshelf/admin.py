from django.contrib import admin

# Register your models here.

from .models import Book, CustomUser


class BookAdmin(admin.ModelAdmin):
    list_filter = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author', 'publication_year')


admin.site.register(Book, CustomUser)
