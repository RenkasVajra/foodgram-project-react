from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.db.models import Sum
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .forms import RecipesForm, IngredientsForm, FollowForm, FavoriteRecipesForm, ShoppingListForm
from .models import Recipe, Ingredient, Follow, FavoriteRecipes, ShoppingList, RecipeIngredient, User


class IsFavoriteMixin:

    def get_queryset(self):
        qs = super().get_queryset()
        qs = (
            qs
            .select_related('author')
            .with_is_favorite(user_id=self.request.user.id)
        )

        return qs


class BaseRecipeListView(IsFavoriteMixin, ListView):
    context_object_name = 'recipe_list'
    queryset = Recipe.objects.all()
    paginate_by = 6
    page_title = None

    def get_context_data(self, **kwargs):
        kwargs.update({'page_title': self._get_page_title(),
                       'shopping_list': self._get_shopping_list()})
        context = super().get_context_data(**kwargs)
        return context

    def _get_page_title(self):
        assert self.page_title, f"Attribute 'page_title' not set for {self.__class__.__name__}"  # noqa
        return self.page_title

    def _get_shopping_list(self):
        if self.request.user.is_authenticated:
            shopping_list = ShoppingList.objects.filter(user=self.request.user).all()
            return shopping_list


class FavouriteView(LoginRequiredMixin, BaseRecipeListView):
    page_title = 'Избранное'
    template_name = 'index.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_favorite=True)


class SubscriptionsView(LoginRequiredMixin, BaseRecipeListView):
    page_title = 'Подписки'
    template_name = 'myFollow.html'

    def get_queryset(self):
        user = self.request.user
        qs = user.following.all()
        print(qs)

        return qs


class ProfileView(BaseRecipeListView):

    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, username=kwargs.get('username'))

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.user).with_is_favorite(user_id=self.user.id)

        return qs

    def get_page_title(self):
        return self.user.get_full_name()


class RecipeDetailView(DetailView):
    queryset = Recipe.objects.all()
    template_name = 'recipePage.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.with_is_favorite(user_id=self.request.user.id)
        return qs


class FavoriteView(LoginRequiredMixin, BaseRecipeListView):
    page_title = 'Избранное'
    template_name = 'favorite.html'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        qs = qs.filter(favorite_recipe__user=self.request.user).with_is_favorite(user_id=user.id)
        return qs


class IndexView(BaseRecipeListView):
    page_title = 'Recipes'
    template_name = 'index.html'


def get_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            value_ingredient = key[15:]
            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + value_ingredient
            ]
    return ingredients


def new_recipe(request):
    form = RecipesForm(request.POST or None, files=request.FILES or None)
    ingredients = get_ingredients(request)

    if not form.is_valid():
        return render(
            request,
            'formRecipe.html',
            {'form': form,
             'is_new': True,
             },
        )

    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()

    RecipeIngredient.objects.filter(recipe=recipe).delete()
    objs = []

    for title, count in ingredients.items():
        ingredient = get_object_or_404(Ingredient, title=title)
        objs.append(RecipeIngredient(
            recipe=recipe,
            ingredient=ingredient,
            count=count
        )
        )
    RecipeIngredient.objects.bulk_create(objs)
    form.save_m2m()
    return redirect('index')


@login_required
def recipe_edit(request, id):
    recipe_base = get_object_or_404(Recipe, pk=id)
    form = RecipesForm(request.POST or None, files=request.FILES or None, instance=recipe_base)
    ingredients = get_ingredients(request)
    if not form.is_valid():
        return render(
            request,
            'formRecipe.html',
            {'form': form,
             'is_new': True,
             },
        )
    recipe = form.save(commit=False)
    recipe.user = request.user
    recipe.save()
    RecipeIngredient.objects.filter(recipe=recipe).delete()
    objs = []
    for title, count in ingredients.items():
        ingredient = get_object_or_404(Ingredient, title=title)
        objs.append(RecipeIngredient(
            recipe=recipe,
            ingredient=ingredient,
            count=count
        )
        )
    RecipeIngredient.objects.bulk_create(objs)
    form.save_m2m()
    return redirect('index')


def profile(request, username):
    author = get_object_or_404(User, username=username)
    page_obj = author.recipes.all()
    following = author.following.exists()
    context = {
        'author': author,
        'following': following,
        'page_obj': page_obj,
    }
    return render(request, 'authorRecipe.html', context)


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


def shopping_list_download(request):
    result = shopping_list_ingredients(request)
    response = HttpResponse(result, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename = download.txt'
    return response


def shopping_list(request):
    shopping_list = ShoppingList.objects.filter(user=request.user).all()
    return render(
        request,
        'shopList.html',
        {'shopping_list': shopping_list,},
    )


def shopping_list_ingredients(request):
    shopping_list = ShoppingList.objects.filter(user=request.user).all()
    ingredients = {}
    for item in shopping_list:
        for x in item.recipe.recipe.all():
            name = f'{x.ingredient.title} ({x.ingredient.unit})'
            units = x.count
            if name in ingredients.keys():
                ingredients[name] += units
            else:
                ingredients[name] = units
    download = []
    for key, units in ingredients.items():
        download.append(f'{key} - {units} \n')
    return download
