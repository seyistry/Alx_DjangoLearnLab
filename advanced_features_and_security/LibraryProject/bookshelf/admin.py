from django.contrib import admin

# Register your models here.

from .models import Book, CustomUser


class BookAdmin(admin.ModelAdmin):
    list_filter = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author', 'publication_year')

# add custom user admin


class CustomUserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'date_of_birth')
    search_fields = ('email', 'date_of_birth')


admin.site.register(Book, BookAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
