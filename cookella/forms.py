from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import FoodRecipe, FoodType


class FoodTypeForm(forms.ModelForm):
    class Meta:
        model = FoodType
        fields = ["food_name", "country"]


class FoodRecipeForm(forms.ModelForm):
    class Meta:
        model = FoodRecipe
        fields = ["ingredient", "recipe", "note"]


class RecipeSearchForm(forms.Form):
    search = forms.CharField()
