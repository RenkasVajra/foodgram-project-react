from rest_framework import status, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from recipes.models import FavoriteRecipes, Ingredient, Recipe, Follow, User, ShoppingList
from .serializers import IngredientSerializer, FavoriteSerializer


class AddSubscriptions(APIView):
    def post(self, request, format=None):
        if self.request.user.is_authenticated:
            Follow.objects.get_or_create(
                user=request.user,
                author_id=request.data['id'],
            )
            return Response({'success': True}, status=status.HTTP_200_OK)
        return redirect('login')


class RemoveSubscriptions(APIView):
    def delete(self, request, pk, format=None):
        if self.request.user.is_authenticated:
            get_object_or_404(
                Follow,
                user=request.user,
                author_id=pk
            )
            Follow.objects.filter(
                author_id=pk,
                user=request.user
            ).delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        return redirect('login')


class AddToFavorites(APIView):
    serializer_class = FavoriteSerializer

    def post(self, request):
        if self.request.user.is_authenticated:
            FavoriteRecipes.objects.get_or_create(
                user=request.user,
                favorite_id=int(request.data['id']),
            )

            return Response({'success': True}, status=status.HTTP_200_OK)
        return redirect('login')


class RemoveFromFavorites(APIView):
    serializer_class = FavoriteSerializer

    def delete(self, request, id):
        if self.request.user.is_authenticated:
            get_object_or_404(
                FavoriteRecipes,
                user=request.user,
                favorite_id=id
            )
            FavoriteRecipes.objects.filter(
                favorite_id=id,
                user=request.user
            ).delete()

            return Response({'success': True}, status=status.HTTP_200_OK)
        return redirect('login')


class PurchaseView(APIView):

    def post(self, request):
        if self.request.user.is_authenticated:
            recipe_id = request.data.get('id')
            recipe = get_object_or_404(Recipe, id=recipe_id)
            ShoppingList.objects.get_or_create(user=request.user, recipe=recipe)
            return Response({'success': True})
        return redirect('login')


@login_required
def remove_purchase(request, pk):
    if request.user.is_authenticated:
        purchase = get_object_or_404(ShoppingList, user=request.user, recipe=pk)
        purchase.delete()
        return redirect('shopping_list')
    return redirect('login')


class GetIngredient(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = IngredientSerializer

    def get(self, request):
        query = request.GET.get('query')
        queryset = list(
            Ingredient.objects.filter(title__startswith=query).values(
                'title',
                'unit'
            )
        )
        return JsonResponse(queryset, safe=False)


@api_view(['POST'])
def add_to_favorites(request):
    if request.user.is_authenticated:
        user = request.user
        recipe_id = request.data.get('id')
        FavoriteRecipes.objects.get_or_create(
            user=user,
            recipe_id=recipe_id,
        )

        return Response(status=status.HTTP_200_OK)
    return redirect('login')


@api_view(['DELETE'])
def delete_from_favorites(request, pk, format=None):
    get_object_or_404(
        Follow,
        pk=pk
    )
    FavoriteRecipes.objects.filter(pk=pk).delete()

    return Response(status=status.HTTP_200_OK)
