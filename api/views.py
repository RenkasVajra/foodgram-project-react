from rest_framework import status, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from recipes.models import FavoriteRecipes, Ingredient, Recipe, RecipeIngredient, Follow, User
from .serializers import IngredientSerializer, FavoriteSerializer


def profile_follow(request, username):
    author = User.objects.get(username=username)
    following = author.following.exists()
    if request.user != author and not following:
        Follow.objects.get_or_create(user=request.user, author=author)
    return Response({'success': True}, status=status.HTTP_200_OK)


def profile_unfollow(request, username):
    author = User.objects.get(username=username)
    Follow.objects.get(user=request.user, author=author).delete()
    return Response({'success': True}, status=status.HTTP_200_OK)


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


class GetIngredient(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        ingredient = self.request.query_params.get('query')
        if ingredient is not None:
            queryset = queryset.filter(title__startswith=ingredient)
        return queryset

