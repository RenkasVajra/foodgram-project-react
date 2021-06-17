from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status, mixins
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import (
    FavoriteRecipes,
    Ingredient,
    Recipe,
    Follow,
    ShoppingList,
)
from .serializers import IngredientSerializer, FavoriteSerializer


class AddSubscriptions(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        Follow.objects.get_or_create(
            user=request.user,
            author_id=request.data.get("id"),
        )
        return Response({"success": True}, status=status.HTTP_200_OK)


class RemoveSubscriptions(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk, format=None):
        follow_obj = get_object_or_404(
            Follow,
            user=request.user,
            author_id=pk)
        follow_obj.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)


class AddToFavorites(APIView):
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        FavoriteRecipes.objects.get_or_create(
            user=request.user,
            favorite_id=request.data.get("id"),
        )
        return Response({"success": True}, status=status.HTTP_200_OK)


class RemoveFromFavorites(APIView):
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, id):
        favorite_recipe = get_object_or_404(
            FavoriteRecipes, user=request.user, favorite_id=id
        )
        favorite_recipe.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)


class PurchaseView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        recipe_id = request.data.get("id")
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ShoppingList.objects.get_or_create(user=request.user, recipe=recipe)
        return Response({"success": True})


@api_view(["DELETE", "GET"])
@permission_classes([IsAuthenticated])
def remove_purchase(request, pk):
    purchase = get_object_or_404(
        ShoppingList,
        user=request.user,
        recipe=pk
    )
    purchase.delete()
    return Response({"success": True}, status=status.HTTP_200_OK)


class GetIngredient(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        query = request.GET.get("query")
        queryset = list(
            Ingredient.objects.filter(
                title__startswith=query
            ).values("title", "unit")
        )
        return JsonResponse(queryset, safe=False)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_favorites(request):
    user = request.user
    recipe_id = request.data.get("id")
    FavoriteRecipes.objects.get_or_create(
        user=user,
        recipe_id=recipe_id,
    )
    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
def delete_from_favorites(request, pk, format=None):
    favorite_recipe = get_object_or_404(FavoriteRecipes, pk=pk)
    favorite_recipe.delete()

    return Response(status=status.HTTP_200_OK)
