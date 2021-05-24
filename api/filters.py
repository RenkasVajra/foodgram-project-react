from django_filters import rest_framework as filters

from recipes.models import Ingredient


class IngredientFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    unit = filters.CharFilter(field_name='unit', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('title', 'unit')
