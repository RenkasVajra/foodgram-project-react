from django.urls import path, include

from . import views
from .views import AddSubscriptions, RemoveSubscriptions


urlpatterns = [
    path(
        "v1/ingredients",
        views.GetIngredient.as_view({"get": "get"}),
        name="ingredients",
    ),
    path(
        "v1/favorites/",
        views.AddToFavorites.as_view()
    ),
    path(
        "v1/favorites/<int:id>/",
        views.RemoveFromFavorites.as_view()
    ),
    path(
        "v1/subscriptions/",
        AddSubscriptions.as_view()
    ),
    path(
        "v1/subscriptions/<int:pk>/",
        RemoveSubscriptions.as_view()
    ),
    path(
        "v1/purchases/",
        views.PurchaseView.as_view()
    ),
    path(
        "v1/purchases/<int:pk>/",
        views.remove_purchase,
        name="delete_purchase"
    ),
]
