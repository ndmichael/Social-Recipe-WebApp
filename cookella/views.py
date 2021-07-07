from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import FoodType, FoodRecipe
from blog.models import Post
from django.views.generic import ListView, DetailView, CreateView
from .forms import FoodTypeForm, FoodRecipeForm
from django.http import HttpResponse
from .forms import RecipeSearchForm
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery


def index(request):
    ft_recipes = FoodType.objects.all().order_by("date_added")[:4]
    posts = Post.objects.all().order_by("-like_count")[:6]
    return render(
        request,
        "cookella/index.html",
        {"title": "home", "ft_recipes": ft_recipes, "posts": posts},
    )


def about(request):
    return render(request, "cookella/about.html", {"title": "about"})


class FoodListView(ListView):
    model = FoodType
    ordering = ["-date_added"]
    paginate_by = 8

    def get_queryset(self):
        return FoodType.objects.filter(active=True).order_by("-date_added")


class FoodDetailView(DetailView):
    model = FoodType


# before saving i override the save method and added the user as contributor,
# and food type both on the fly
@login_required
def contributor(request):
    if request.method == "POST":
        f_form = FoodTypeForm(request.POST, request.FILES)
        r_form = FoodRecipeForm(request.POST)
        if f_form.is_valid() and r_form.is_valid():
            f_obj = f_form.save(commit=False)
            f_obj.contributor = request.user
            f_obj.save()
            r_obj = r_form.save(commit=False)
            r_obj.food_type = f_obj
            r_obj.save()
            foodname = f_form.cleaned_data.get("food_name")
            messages.success(request, f"Recipe for {foodname} added successfully")
            return redirect("dish_list")

    else:
        f_form = FoodTypeForm()
        r_form = FoodRecipeForm()
    context = {
        "f_form": f_form,
        "r_form": r_form,
    }
    return render(request, "cookella/addrecipe_page.html", context)


@login_required
def recipeUpdateView(request, pk, slug):
    my_reverse = reverse(
        "recipes", kwargs={"pk": pk, "slug": slug}
    )  # i create a reverse since it can take parameters
    food = FoodType.objects.get(pk=pk)
    # throws error and redirect if user tries copying link to update and not a contributor
    if not request.user.username == food.contributor:
        messages.error(request, f"permission denied to update this Recipe")
        return redirect(my_reverse)  # then pass the reverse to the redirect
    else:
        if request.method == "POST":
            f_form = FoodTypeForm(request.POST, request.FILES, instance=food)
            r_form = FoodRecipeForm(request.POST, instance=food.food_type)
            if f_form.is_valid() and r_form.is_valid():
                f_form.save()
                r_form.save()
                foodname = f_form.cleaned_data.get("food_name")
                messages.success(request, f"FoodRecipe for {foodname} updated")
                return redirect(my_reverse)

        else:
            f_form = FoodTypeForm(instance=food)
            r_form = FoodRecipeForm(instance=food.food_type)
    context = {
        "f_form": f_form,
        "r_form": r_form,
    }
    return render(request, "cookella/update_recipe.html", context)


def recipe_search(request):
    form = RecipeSearchForm()
    q = ""
    results = []
    if "search" in request.GET:
        form = RecipeSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data["search"]
            results = FoodType.objects.annotate(
                search=SearchVector(
                    "food_name",
                ),
            ).filter(search=SearchQuery(q))
    context = {
        "form": form,
        "q": q,
        "results": results,
    }
    return render(request, "cookella/search.html", context)
