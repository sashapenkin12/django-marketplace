"""
Module with class-based views for products app
"""
from django.db.models import Count
from rest_framework import status, filters
from rest_framework.request import Request
from rest_framework.views import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from .models import Product, Tag, Category, Review, Sale
from .serializers import ProductSerializer, TagSerializer, CategorySerializer, ReviewSerializer, \
    ProductWithReviewsSerializer, SaleSerializer
from .filters import ProductFilter, CustomFilterBackend, CustomOrderingBackend
from .paginators import CatalogPaginator


class CatalogView(ListAPIView):
    """
    Get catalog of products.

    Attributes:
        queryset: Database queryset
        serializer_class: Items serializer
        filter_backends: Array of filter classes used on the queryset
        filterset_class: Filterset form that performs data filtering
        pagination_class: Pagination class
        ordering: Default ordering
    """
    queryset = Product.objects.prefetch_related(
        'tags', 'reviews'
    ).annotate(review_count=Count('reviews'))
    serializer_class = ProductSerializer

    filter_backends = (
        CustomFilterBackend,
        CustomOrderingBackend,
        filters.SearchFilter,
    )
    filterset_class = ProductFilter
    pagination_class = CatalogPaginator
    ordering = 'price'


class TagView(ListAPIView):
    """
    Get all tags.

    Attributes:
        queryset: Database queryset
        serializer_class: Items serializer

    Methods:
        list: Get filtered response
    """
    queryset = Tag.objects.annotate(
        num_products=Count('products')
    ).order_by('-num_products').all()
    serializer_class = TagSerializer

    def list(self, request: Request, *args, **kwargs):
        """
        Get response with category filtering.

        Args:
            request: Current HTTP request.

        Returns:
            Response: Response with filtered data.
        """
        queryset = self.filter_queryset(self.get_queryset())
        if request.query_params:
            queryset = queryset.filter(category=request.query_params.get('category'))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CategoryListView(ListAPIView):
    """
    Get all categories.

    Attributes:
        queryset: Database queryset
        serializer_class: Items serializer
    """
    queryset = (Category.objects
                .prefetch_related('subcategories')
                .select_related('image').all()
                )
    serializer_class = CategorySerializer


class ProductRetrieveView(RetrieveAPIView):
    """
    Retrieve product.

    Attributes:
        queryset: Database queryset
        serializer_class: Items serializer
    """
    queryset = Product.objects.prefetch_related(
        'tags', 'reviews'
    ).all()
    serializer_class = ProductWithReviewsSerializer


class CreateReviewView(CreateAPIView):
    """
    Create review on product.

    Attributes:
        serializer_class: Items serializer

    Methods:
        create: Create new review.
    """
    serializer_class = ReviewSerializer

    def create(self, request: Request, *args, **kwargs):
        """
        Create new review.

        Args:
            request: Current HTTP request.

        Returns:
            Response: Response with new review data.

        """
        product_id = kwargs.get('pk')
        if product_id is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        request.data['product'] = product_id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        reviews = Review.objects.filter(product_id=product_id).all()
        serializer = self.get_serializer(instance=reviews, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PopularProductsView(ListAPIView):
    """
    Get most popular by index parameter products.

    Attributes:
        queryset: Database queryset
        serializer_class: Items serializer
    """
    queryset = (Product.objects
                .prefetch_related(
        'images',
        'tags'
    ).order_by('index')[:8])
    serializer_class = ProductSerializer


class LimitedProductsView(ListAPIView):
    """
    Get limited products.

    Attributes:
        queryset: Database queryset
        serializer_class: Items serializer
    """
    queryset = (Product.objects
                .prefetch_related(
        'images',
        'tags'
    ).filter(limited=True)[:16])
    serializer_class = ProductSerializer


class BannersView(ListAPIView):
    """
    Get random product banners.

    Attributes:
        queryset: Database queryset
        serializer_class: Items serializer
    """
    queryset = Product.objects.order_by('?')[:3]
    serializer_class = ProductSerializer


class SalesView(ListAPIView):
    """
    Get all sales.

    Attributes:
        queryset: Database queryset
        pagination_class: Pagination class
        serializer_class: Items serializer
    """
    queryset = Sale.objects.all()
    pagination_class = CatalogPaginator
    serializer_class = SaleSerializer
