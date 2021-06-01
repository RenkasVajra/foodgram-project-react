from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from rest_framework import status

from foodgram import settings
from .forms import (
    RecipesForm,
)
from .models import (
    Recipe,
    Ingredient,
    ShoppingList,
    RecipeIngredient,
    User,
)


class IsFavoriteMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("author").with_is_favorite(
            user_id=self.request.user.id)
        return qs


class BaseRecipeListView(IsFavoriteMixin, ListView):
    context_object_name = "recipe_list"
    queryset = Recipe.objects.all()
    paginate_by = settings.POSTS_PER_PAGE
    page_title = None

    def get_context_data(self, **kwargs):
        kwargs.update(
            {
                "page_title": self._get_page_title(),
                "shopping_list": self._get_shopping_list(),
            }
        )
        context = super().get_context_data(**kwargs)
        return context

    def _get_page_title(self):
        return self.page_title

    def _get_shopping_list(self):
        if self.request.user.is_authenticated:
            shopping_list = ShoppingList.objects.filter(
                user=self.request.user).all()
            return shopping_list

    def get_queryset(self):

        qs = super().get_queryset()
        tags = self.request.GET.getlist("tag")
        if tags:
            qs = qs.filter(tags__display_name__in=tags).distinct()
        return qs


class FavouriteView(LoginRequiredMixin, BaseRecipeListView):
    page_title = "Избранное"
    template_name = "index.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_favorite=True)


class SubscriptionsView(LoginRequiredMixin, BaseRecipeListView):
    page_title = "Подписки"
    template_name = "myFollow.html"

    def get_queryset(self):
        return self.request.user.following.all()


class ProfileView(BaseRecipeListView):
    template_name = "authorRecipe.html"

    def get(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, username=kwargs.get("username"))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(author=self.user)
        return qs

    def get_context_data(self, **kwargs):
        kwargs.update({"author": self.user})
        context = super().get_context_data(**kwargs)
        return context

    def _get_page_title(self):
        return self.user.get_full_name()


class RecipeDetailView(DetailView):
    queryset = Recipe.objects.all()
    template_name = "recipePage.html"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.with_is_favorite(user_id=self.request.user.id)
        return qs


class FavoriteView(LoginRequiredMixin, BaseRecipeListView):
    page_title = "Избранное"
    template_name = "favorite.html"

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        qs = qs.filter(
            favorite_recipe__user=self.request.user
        ).with_is_favorite(
            user_id=user.id
        )
        return qs


class IndexView(BaseRecipeListView):
    page_title = "Recipes"
    template_name = "index.html"


def get_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startswith("nameIngredient"):
            value_ingredient = key[15:]
            ingredients[request.POST[key]] = request.POST[
                "valueIngredient_" + value_ingredient
                ]
    return ingredients


def new_recipe(request):
    form = RecipesForm(request.POST or None, files=request.FILES or None)
    ingredients = get_ingredients(request)

    if not form.is_valid():
        return render(
            request,
            "formRecipe.html",
            {
                "form": form,
                "is_new": True,
            },
        )

    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()

    RecipeIngredient.objects.filter(recipe=recipe).delete()
    objs = []

    for title, count in ingredients.items():
        ingredient = get_object_or_404(Ingredient, title=title)
        objs.append(
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient,
                count=count
            )
        )
    RecipeIngredient.objects.bulk_create(objs)
    form.save_m2m()
    return redirect("index")


@login_required
def recipe_edit(request, id):
    recipe_base = get_object_or_404(Recipe, pk=id)
    form = RecipesForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe_base
    )
    ingredients = get_ingredients(request)
    if not form.is_valid():
        return render(
            request,
            "formRecipe.html",
            {
                "form": form,
                "is_new": True,
            },
        )
    recipe = form.save(commit=False)
    recipe.user = request.user
    recipe.save()
    RecipeIngredient.objects.filter(recipe=recipe).delete()
    objs = []
    for title, count in ingredients.items():
        ingredient = get_object_or_404(Ingredient, title=title)
        objs.append(
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient,
                count=count
            )
        )
    RecipeIngredient.objects.bulk_create(objs)
    form.save_m2m()
    return redirect("index")


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=status.HTTP_404_NOT_FOUND,
    )


def server_error(request):
    return render(
        request,
        "misc/500.html",
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


def shopping_list_download(request):
    result = shopping_list_ingredients(request)
    response = HttpResponse(result, content_type="text/plain")
    response["Content-Disposition"] = "attachment; filename = download.txt"
    return response


def shopping_list(request):
    shopping_list = ShoppingList.objects.filter(user=request.user).all()
    return render(
        request,
        "shopList.html",
        {"shopping_list": shopping_list},
    )


def shopping_list_ingredients(request):
    shopping_list = Recipe.objects.filter(shopping_list__user=request.user)
    ingredients = shopping_list.order_by("ingredient__title").values(
        "ingredient__title", "ingredient__unit").annotate(
        total_count=Sum("recipe__count"))
    download = []
    for ingredient in ingredients:
        download.append(
            f'{ingredient["ingredient__title"]} '
            f'- {ingredient["total_count"]}'
            f'{ingredient["ingredient__unit"]} \n'
        )
    return download
