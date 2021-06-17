from django.urls import path

from . import views

urlpatterns = [
    path(
        "v1/ingredients",
        views.GetIngredient.as_view({"get": "get"}),
        name="ingredients",
    ),
    path(
        "v1/favorites/",
        views.AddToFavorites.as_view(),
        name="add_favorite"
    ),
    path(
        "v1/favorites/<int:id>/",
        views.RemoveFromFavorites.as_view(),
        name="remove_favorite"
    ),
    path(
        "v1/subscriptions/",
        views.AddSubscriptions.as_view(),
        name="add_subscribe"
    ),
    path(
        "v1/subscriptions/<int:pk>/",
        views.RemoveSubscriptions.as_view(),
        name="remove_subscribe"
    ),
    path(
        "v1/purchases/",
        views.PurchaseView.as_view(),
        name="add_purchase"
    ),
    path(
        "v1/purchases/<int:pk>/",
        views.remove_purchase,
        name="delete_purchase"
    ),
]
