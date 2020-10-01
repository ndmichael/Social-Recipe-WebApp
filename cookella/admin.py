from django.contrib import admin
from .models import FoodType, FoodRecipe

# Register your models here.

#@admin.register(FoodTypes)
#admin.site.register(FoodTypes)
#admin.site.register(FoodDescription)


@admin.register(FoodType)
class FoodTypeAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'country', 'food_image', 'active',)
    prepopulated_fields = {"slug": ("food_name",)}


@admin.register(FoodRecipe)
class FoodRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'food_type', 'ingredient',)

