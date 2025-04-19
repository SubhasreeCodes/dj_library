from django.contrib import admin

from backend.models import Genre, Author

# Register your models here.
admin.site.register(Genre)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name',)