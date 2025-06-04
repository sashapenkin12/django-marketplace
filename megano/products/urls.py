"""
Module with urlpatterns for products app.

Attributes:
    urlpatterns: List of url paths that are available for products app.
"""
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import CatalogView, ProductRetrieveView, CreateReviewView, TagView, CategoryListView, LimitedProductsView, \
    PopularProductsView, BannersView, SalesView

urlpatterns: list[path] = [
    path('catalog/', cache_page(60 * 3)(CatalogView.as_view()), name='catalog'),
    path('product/<int:pk>/', cache_page(60 * 3)(ProductRetrieveView.as_view()), name='product_retrieve'),
    path('product/<int:pk>/reviews', CreateReviewView.as_view(), name='create_review'),
    path('tags/', cache_page(60 * 3)(TagView.as_view()), name='tags_list'),
    path('categories/', cache_page(60 * 3)(CategoryListView.as_view()), name='category_list'),
    path('products/limited', cache_page(60 * 3)(LimitedProductsView.as_view()), name='limited-products'),
    path('products/popular', cache_page(60 * 3)(PopularProductsView.as_view()), name='popular-products'),
    path('banners', cache_page(60 * 3)(BannersView.as_view()), name='banners'),
    path('sales', cache_page(60 * 3)(SalesView.as_view()), name='sales'),
]
