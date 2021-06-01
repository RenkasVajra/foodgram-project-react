from django import forms
from django.forms import ModelForm

from .models import Recipe, Ingredient, Follow, FavoriteRecipes, ShoppingList


class RecipesForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ("title", "cook_time", "text", "image", "tags")
        labels = {
            "title": "Название",
            "text": "Текст",
            "ingredient": "Ингредиенты",
            "cook_time": "Время приготовления",
            "tags": "Теги",
        }

        widgets = {"tags": forms.CheckboxSelectMultiple()}


class IngredientsForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ("title", "unit")
        labels = {"title": "Название", "unit": "Единицы  измерения"}


class FollowForm(ModelForm):
    class Meta:
        model = Follow
        fields = ("author", "user")


class FavoriteRecipesForm(ModelForm):
    class Meta:
        model = FavoriteRecipes
        fields = ("favorite", "user")
        labels = {"favorite": "Избранный рецепт", "user": "Пользователь"}


class ShoppingListForm(ModelForm):
    class Meta:
        model = ShoppingList
        fields = ("recipe", "user")
        labels = {"recipe": "Рецепт", "user": "Пользователь"}
