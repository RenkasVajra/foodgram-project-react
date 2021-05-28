from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('recipes/', views.new_recipe, name='recipe_add'),
    path('subscriptions/', views.SubscriptionsView.as_view(), name='subscriptions'),
    path('favorite/', views.FavoriteView.as_view(), name='favorites'),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe'),
    path('recipes/edit/<int:id>/', views.recipe_edit, name='recipe_edit'),
    path('shopping_list/', views.shopping_list, name='shopping_list'),
    path('download_shoplist/', views.shopping_list_download, name='download_shoplist'),
    path('<str:username>/',  views.profile, name='profile'),

]
