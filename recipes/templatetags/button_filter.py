from django import template

from recipes.models import ShoppingList, Follow

register = template.Library()


@register.filter()
def shopping_card(recipe, user):
    return ShoppingList.objects.filter(user=user, recipe=recipe).exists()


@register.filter()
def shopping_counter(request, user_id):
    return ShoppingList.objects.filter(user=user_id).count()


@register.filter()
def is_following(author, user):
    return Follow.objects.filter(user=user, author=author).exists()
