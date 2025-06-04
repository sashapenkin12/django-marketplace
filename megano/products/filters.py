"""
Module with filters for products app.
"""

from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import Product

class ProductFilter(filters.FilterSet):
    """
    Filterset for Product model.

    Attributes:
        name: Filter by contained data characters.
        minPrice: Filter at the lowest price.
        maxPrice: Filter by maximum price.
        freeDelivery: Filter by 'freeDelivery' value.
        available: Filter by 'available' value.
        category: Filter by category.
        tags: Filter by tags.

    Meta:
        model: Model of serializer.
        fields: Array of representing fields.
    """
    name = filters.CharFilter(field_name='title', lookup_expr='icontains')
    minPrice = filters.NumberFilter(field_name='price', lookup_expr='gte')
    maxPrice = filters.NumberFilter(field_name='price', lookup_expr='lte')
    freeDelivery = filters.BooleanFilter(field_name='freeDelivery')
    available = filters.BooleanFilter(field_name='available')
    category = filters.NumberFilter(field_name="category_id")
    tags = filters.AllValuesFilter(field_name='tags', lookup_expr='in')

    class Meta:
        model = Product
        fields = ['name', 'minPrice', 'maxPrice', 'freeDelivery', 'available', 'category']


class CustomFilterBackend(DjangoFilterBackend):
    """
    Custom filter backend.

    Custom filter backend that overrides the DjangoFilterBackend method specifically to parse data correctly.

    Methods:
        get_filterset_kwargs: Customised parent class method that parses data in a different way.
    """
    def get_filterset_kwargs(self, request, queryset, view) -> dict:
        """
        Overridden get_filterset_kwargs method that parses filter data specifically for a filterset.

        Params:
            request: Current HTTP request.
            queryset: Database queryset.
            view: Current view that handles request.

        Returns:
            result: Dict of parsed kwargs.
        """
        data = request.query_params.copy()
        flat_data = {key[7:-1]: value for key, value in data.items() if key.startswith('filter[')}
        kwargs = super().get_filterset_kwargs(request, queryset, view)
        result = kwargs.copy()
        result['data'] = flat_data
        for key, value in kwargs['data'].items():
            if key == 'tags[]':
                if 'tags' in result['data'].keys():
                    result['data']['tags'].append(value)
                else:
                    result['data']['tags'] = value
            elif not key.startswith('filter['):
                result['data'][key] = value

        return result


class CustomOrderingBackend(OrderingFilter):
    """
    Custom ordering filter backend.

    Custom filter backend that overrides the OrderingFilter method specifically to parse data correctly.

    Methods:
        get_ordering: Customised parent class method that parses ordering param in a different way.
    """
    def get_ordering(self, request, queryset, view):
        """
        Overridden get_ordering method that parses ordering param specifically for a filterset.

        Params:
            request: Current HTTP request.
            queryset: Database queryset.
            view: Current view that handles request.

        Returns:
            result: Array with ordering parameter.
        """
        data = request.query_params.copy()
        flat_data = {key: value for key, value in data.items() if key.startswith('sort')}
        if flat_data:
            result = ''
            for key, value in flat_data.items():
                if value == 'dec':
                    result = '-' + result
                elif value != 'inc':
                    result = value
            return [result]


        return self.get_default_ordering(view)
