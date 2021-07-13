from django.contrib import admin

from .models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    Follow,
    ShoppingList,
    FavoriteRecipes,
    Tag,
)


class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ("title",)
    search_fields = ("title",)


class FavoriteRecpiesInline(admin.TabularInline):
    model = FavoriteRecipes
    extra = 1
    raw_id_fields = ("favorite",)
    list_filter = ("author",)
    search_fields = ("author", "title")


class MembershipInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    raw_id_fields = ("ingredient",)
    search_fields = ("title",)


class RecipeAdmin(admin.ModelAdmin):
    inlines = (
        MembershipInline,
        FavoriteRecpiesInline,
    )
    list_filter = ("author", "title", "tags", "ingredient", "cook_time")
    search_fields = ("author", "ingredient", "title", "tags")


class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = ("title", "unit")
    search_fields = ("title", "unit")


class FollowAdmin(admin.ModelAdmin):
    model = Follow
    list_display = ("author", "user")
    search_fields = ("author", "user")


class ShoppinglistAdmin(admin.ModelAdmin):
    model = ShoppingList
    list_display = ("recipe", "user")
    search_fields = ("recipe", "user")


admin.site.register(Tag, TagAdmin)
admin.site.register(FavoriteRecipes, )
admin.site.register(ShoppingList, ShoppinglistAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, )
admin.site.register(Follow, FollowAdmin)
