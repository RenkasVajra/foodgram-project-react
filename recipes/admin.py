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
    list_filter = ("title",)
    search_fields = ("title",)


class FavoriteRecpiesInline(admin.TabularInline):
    model = FavoriteRecipes
    extra = 1
    raw_id_fields = ("favorite",)
    list_filter = ("author",)


class MembershipInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    raw_id_fields = ("ingredient",)


class RecipeAdmin(admin.ModelAdmin):
    inlines = (
        MembershipInline,
        FavoriteRecpiesInline,
    )
    list_filter = ("author", "title", "tags", "ingredient", "cook_time")
    search_fields = ("author", "ingredient", "title", "tags")


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("title", "unit")
    list_filter = ("title", "unit")
    search_fields = ("title",)


admin.site.register(Tag, TagAdmin)
admin.site.register(FavoriteRecipes)
admin.site.register(ShoppingList)
admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(Follow)
