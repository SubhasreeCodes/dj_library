from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from backend.forms import CustomUserCreationForm, CustomUserChangeForm
from backend.models import CustomUser, AuthorUser, MemberUser, AdminUser
from django.utils.html import format_html

from backend.models import Genre, Book, BookAuthor

# Register your models here.
@admin.register(CustomUser)
class BaseCustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('email', 'gender', 'image_tag', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'gender', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'gender', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )


    def image_tag(self, obj):
        return format_html('<img src ="{}" width ="150" height="150" />'.format(obj.image.url))
    image_tag.short_description = 'Image'

    @admin.register(AuthorUser)
    class AuthorAdmin(BaseCustomUserAdmin):

        def get_queryset(self, request):
            return super().get_queryset(request).filter(groups__name='Author')


@admin.register(MemberUser)
class MemberAdmin(BaseCustomUserAdmin):

    def get_queryset(self, request):
        return super().get_queryset(request).filter(groups__name='Member')


@admin.register(AdminUser)
class AdminUserAdmin(BaseCustomUserAdmin):

    def get_queryset(self, request):
        return super().get_queryset(request).filter(groups__name='Admin')

admin.site.register(Genre)

class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1  # Show 1 empty row to add new relationships

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'author':
            # Filter only users in the "Author" group
            kwargs["queryset"] = CustomUser.objects.filter(groups__name='Author')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'publication_date', 'copies_owned')
    inlines = [BookAuthorInline]
    search_fields = ('title',)
    list_filter = ('category', 'publication_date')