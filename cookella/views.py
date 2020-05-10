from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import FoodType, FoodRecipe
from django.views.generic import (ListView,
                                  DetailView, CreateView)
from .forms import FoodTypeForm, FoodRecipeForm


# Create your views here.


def index(request):
    return render(request, 'cookella/index.html', {'title': 'home'})


def about(request):
    return render(request, 'cookella/about.html', {'title': 'about'})


class FoodListView(ListView):
    model = FoodType
    ordering = ['-date_added']
    paginate_by = 8
    
    def get_queryset(self):
        return FoodType.objects.filter(active=True).order_by('-date_added')


class FoodDetailView(DetailView):
    model = FoodType



@login_required
def contributor(request):
    if request.method == 'POST':
        f_form = FoodTypeForm(request.POST, request.FILES)
        r_form = FoodRecipeForm(request.POST)
        if f_form.is_valid() and r_form.is_valid():
            f_obj = f_form.save(commit=False)
            f_obj.contributor = request.user
            f_obj.save()
            r_obj = r_form.save(commit=False)
            r_obj.food_type = f_obj
            r_obj.save()
            foodname = f_form.cleaned_data.get('food_name')
            messages.success(request, f'Recipe for {foodname} added success')
            return redirect('dish_list')

    else:
        f_form = FoodTypeForm()
        r_form = FoodRecipeForm()
    context = {
        'f_form': f_form,
        'r_form': r_form,
    }
    return render(request, 'cookella/contributors_page.html', context)


@login_required
def recipeUpdateView(request, pk, slug):
    my_reverse = reverse('recipes', kwargs={'pk': pk, 'slug': slug})
    food = FoodType.objects.get(pk=pk)
    # throws error and redirect if user tries copying link to update and not a contributor
    if not request.user.username == food.contributor:
        messages.error(request, f"permission denied to update this Recipe")
        return redirect(my_reverse)

    else:
        if request.method == 'POST':
            f_form = FoodTypeForm(request.POST, request.FILES, instance=food)
            r_form = FoodRecipeForm(request.POST, instance=food.food_type)
            if f_form.is_valid() and r_form.is_valid():
                f_form.save()
                r_form.save()
                foodname = f_form.cleaned_data.get('food_name')
                messages.success(request, f'FoodRecipe for {foodname} updated')
                return redirect(my_reverse)

        else:
            f_form = FoodTypeForm(instance=food)
            r_form = FoodRecipeForm(instance=food.food_type)
    context = {
        'f_form': f_form,
        'r_form': r_form,
    }
    return render(request, 'cookella/update_recipe.html', context)
