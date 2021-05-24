from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('recipes/', views.new_recipe, name='recipe_add'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('favorite/', views.FavoriteView.as_view(), name='favorites'),
    path('<str:username>/',  views.profile, name='profile'),
    path('<str:username>/follow/', views.profile_follow, name='profile_follow'),
    path('<str:username>/unfollow/', views.profile_unfollow, name='profile_unfollow'),
    path('<str:username>/<int:recipe_id>/edit/', views.recipe_edit, name='recipe_edit'),
    path("recipes/<int:pk>/", views.RecipeDetailView.as_view(), name="recipe"),

]
