from .models import Ingredient


def validate_ingredients(request, form, ingredients):
    if len(ingredients) == 0:
        context = {
            "form": form,
            "error": "Введите как минимум 1 ингредиент"
        }
        return context

    for title in ingredients.keys():
        if not Ingredient.objects.filter(title=title):
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
