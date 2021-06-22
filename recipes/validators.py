from django.shortcuts import get_object_or_404

from .models import Ingredient


def validate_ingredients(request, form, ingredients):
    if ingredients is []:
        context = {
            "form": form,
            "error": "Введите как минимум 1 ингредиент"
        }
        return context

    for title in ingredients.items():
        ing_exists = Ingredient.objects.filter(title=title).exists()
        if ing_exists:
            context = {
                "form": form,
            }
        context = {
            "form": form,
            "error": "Такой ингредиент не существует"
        }
        return context

    for amount in ingredients.values():
        if int(amount) <= 0:
            context = {
                "form": form,
                "error":
                    "Единицы измерения ингредиента не могу быть отрицательными"
            }
            return context
