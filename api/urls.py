from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


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
    path('follow/', views.profile_follow, name='follow'),
    path('follow/{profile_id}/', views.profile_unfollow, name='unfollow'),
]
