from rest_framework import status, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404, render, redirect

from recipes.models import FavoriteRecipes, Ingredient, Recipe, Follow, User, ShoppingList
from .serializers import IngredientSerializer, FavoriteSerializer


class AddSubscriptions(APIView):
    def post(self, request, format=None):
        Follow.objects.get_or_create(
            user=request.user,
            author_id=request.data['id'],
        )
        return Response({'success': True}, status=status.HTTP_200_OK)


class RemoveSubscriptions(APIView):
    def delete(self, request, pk, format=None):
        Follow.objects.filter(
            author_id=pk,
            user=request.user
        ).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class AddToFavorites(APIView):
    serializer_class = FavoriteSerializer

    def post(self, request):
        FavoriteRecipes.objects.get_or_create(
            user=request.user,
            favorite_id=int(request.data['id']),
        )

        return Response({'success': True}, status=status.HTTP_200_OK)


class RemoveFromFavorites(APIView):
    serializer_class = FavoriteSerializer

    def delete(self, request, id):
        FavoriteRecipes.objects.filter(
            favorite_id=id,
            user=request.user
        ).delete()

        return Response({'success': True}, status=status.HTTP_200_OK)


class PurchaseView(APIView):

    def post(self, request):
        recipe_id = request.data.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ShoppingList.objects.get_or_create(user=request.user, recipe=recipe)
        return Response({'success': True})


def remove_purchase(request, id):
    purchase = ShoppingList.objects.filter(user=request.user, recipe=id)
    purchase.delete()
    return Response({'success': True})


class GetIngredient(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        ingredient = self.request.query_params.get('query')
        if ingredient is not None:
            queryset = queryset.filter(title__startswith=ingredient)
        return queryset


@api_view(['POST'])
def add_to_favorites(request):
    user = request.user
    recipe_id = request.data['id']
    FavoriteRecipes.objects.get_or_create(
        user=user,
        recipe_id=recipe_id,
    )

    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_from_favorites(request, pk, format=None):
    FavoriteRecipes.objects.filter(pk=pk).delete()

    return Response(status=status.HTTP_200_OK)
