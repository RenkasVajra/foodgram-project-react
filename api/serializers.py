from rest_framework import serializers

from recipes.models import Ingredient, FavoriteRecipes


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('title', 'unit')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecipes
        fields = '__all__'
