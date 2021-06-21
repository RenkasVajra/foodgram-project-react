def validate_ingredients(request, form, ingredients):
    if ingredients is []:
        context = {
            "form": form,
            "error": "Введите как минимум 1 ингредиент"
        }
        return context
    for item in ingredients:
        if not ingredients[item].exists():
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
