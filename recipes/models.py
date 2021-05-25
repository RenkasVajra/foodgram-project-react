from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef
from typing import Optional


User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=300)
    unit = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.title}, {self.unit}'


class RecipeQuerySet(models.QuerySet):
    def with_is_favorite(self, user_id: Optional[int]):

        return self.annotate(is_favorite=Exists(
            FavoriteRecipes.objects.filter(
                user_id=user_id,
                favorite_id=OuterRef('pk'),
            ),
        ))


class Tag(models.Model):
    class ChoiceTag(models.TextChoices):
        breakfast = 'Завтрак'
        dinner = 'Обед'
        lunch = 'Ужин'

    title = models.CharField(
        verbose_name='Название тега',
        max_length=100,
        unique=True,
        choices=ChoiceTag.choices
    )
    display_name = models.CharField(max_length=20, verbose_name='Имя тега в шаблоне')
    color = models.CharField(max_length=50, verbose_name='Цвет тега')

    def __str__(self):
        return f'{self.title}'


class Recipe(models.Model):
    title = models.CharField(verbose_name='Название', max_length=300)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    text = models.TextField(max_length=3000, verbose_name='Текст рецепта')
    cook_time = models.PositiveIntegerField()
    ingredient = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты'
    )
    image = models.ImageField(
        upload_to='recipes/',
        null=True,
        blank=True
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipe_tags',
        verbose_name='Теги'
    )

    objects = RecipeQuerySet.as_manager()

    class Meta:
        ordering = ('-pub_date',)


class RecipeIngredient(models.Model):

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='recipe_ing')
    count = models.PositiveIntegerField()


class FavoriteRecipes(models.Model):

    favorite = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='Любимый рецепт'

    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_user',
        verbose_name='Пользователь'
    )

    def __str__(self):
        return f'{self.favorite} - избранный рецепт у {self.user}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'favorite'),
                name='unique_favorite_recipe'
            )
        ]


class ShoppingList(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_recipe',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_user',
        verbose_name='Пользователь'
    )

    document = models.FileField(upload_to='media/',)


class Follow(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Юзер, на которого подписываются'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )

    class Meta:
        models.UniqueConstraint(
            fields=('author', 'user'),
            name='following_unique'
        )


