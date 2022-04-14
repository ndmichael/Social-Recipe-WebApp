from django.contrib import admin
from .models import Post, Category

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "author",
        "date_published",
        "status",
    )
    search_fields = ("title", " author", "content")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "date_published"
