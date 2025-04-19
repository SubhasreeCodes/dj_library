from django.contrib import admin

from backend.models import Genre, Author, Book, BookAuthor

# Register your models here.
admin.site.register(Genre)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name',)


class BookAuthorInline(admin.TabularInline):
    model = BookAuthor

    extra = 1  # Show 1 empty row to add new relationships
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'publication_date', 'copies_owned')

    inlines = [BookAuthorInline]

    search_fields = ('title',)

    list_filter = ('category', 'publication_date')