from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import AddSubscriptions, RemoveSubscriptions

router = DefaultRouter(trailing_slash=False)


router.register(
    r'ingredients',
    views.GetIngredient,
    basename='ingredients'
)


urlpatterns = [
    path('', include(router.urls)),
    path('favorites/', views.AddToFavorites.as_view()),
    path('favorites/<int:id>/', views.RemoveFromFavorites.as_view()),
    path('subscriptions/', AddSubscriptions.as_view()),
    path('subscriptions/<int:pk>/', RemoveSubscriptions.as_view()),
    path('purchases/', views.PurchaseView.as_view()),
    path('purchases/<int:id>/', views.remove_purchase, name='delete_purchase'),
]
