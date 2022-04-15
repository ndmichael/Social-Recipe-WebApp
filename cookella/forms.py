from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import FoodRecipe, FoodType, Category

categories = Category.objects.all().values_list("name", "name")
categories_list = [category for category in categories]


class FoodTypeForm(forms.ModelForm):
    category = forms.ChoiceField(initial="soup", choices=categories_list)

    class Meta:
        model = FoodType
        fields = ["category", "food_name", "country"]

        widgets = {}


class FoodRecipeForm(forms.ModelForm):
    class Meta:
        model = FoodRecipe
        fields = ["ingredient", "recipe", "note"]


class RecipeSearchForm(forms.Form):
    search = forms.CharField()
