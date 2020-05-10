from django.conf.urls import url
from django.urls import path
from .views import FoodListView, FoodDetailView
from . import views



urlpatterns = [
    path(r'', views.index, name='cookella-index'),
    path(r'about/', views.about, name='cookella-about'),
    path('dishes/', FoodListView.as_view(), name="dish_list"),
    path('dishes/<int:pk>/<slug>/', FoodDetailView.as_view(), name="recipes"),
    path(r'dishes/contributors/', views.contributor, name='cookella-contributors'),
    path(r'dishes/<int:pk>/<slug:slug>/update/', views.recipeUpdateView, name='contributors-update'),
]

