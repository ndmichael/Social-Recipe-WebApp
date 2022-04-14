from django.contrib import admin
from .models import Category, FoodType, FoodRecipe, FoodImage
from django import forms
from mptt.admin import MPTTModelAdmin

# Register your models here.


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ("name", "parent", "slug", "is_active")
    prepopulated_fields = {"slug": ("name",)}


class FoodImageInline(admin.TabularInline):
    model = FoodImage


class FoodRecipeInline(admin.TabularInline):
    model = FoodRecipe


@admin.register(FoodType)
class FoodTypeAdmin(admin.ModelAdmin):
    list_display = (
        "food_name",
        "country",
        "active",
    )
    inlines = [FoodRecipeInline, FoodImageInline]
    prepopulated_fields = {"slug": ("food_name",)}


# @admin.register(FoodRecipe)
# class FoodRecipeAdmin(admin.ModelAdmin):
#     list_display = (
#         "recipe",
#         "food_type",
#         "ingredient",
#     )
