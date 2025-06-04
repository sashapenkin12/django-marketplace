"""
Products app admin control panel module.
"""

from django.contrib import admin

from .models import Product, ProductImage, Specification, Tag, Review, Category, Sale, Subcategory
from users.admin import ImageInline


class TagInline(admin.TabularInline):
    """
    Inline form for changing tags related with Product instance.

    Attributes:
        model: The model which the inline is using.
    """
    model = Product.tags.through

class ProductImageInline(admin.StackedInline):
    """
    Inline form for a ProductImage model.

    Attributes:
        model: The model which the inline is using.
    """
    model = ProductImage

class SpecificationInline(admin.StackedInline):
    """
    Inline form for a Specification model.

    Attributes:
        model: The model which the inline is using.
    """
    model = Specification

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin form for a Product model.

    Attributes:
        inlines: Array of inlines forms.
        list_display: Array of fields that displays at the admin panel.
        list_display_links: Array of fields that redirects to update instance form.
        ordering: Array of fields that define the sorting rules.
        search_fields: Array of fields used in the search.
        fieldsets: Array of field sets that define the presentation of form fields.
    """
    inlines = [
        TagInline,
        ProductImageInline,
        SpecificationInline,
    ]

    list_display = "pk", "title", "description", "price"
    list_display_links = "pk", "title"
    ordering = "-title", "pk"
    search_fields = "name", "description"
    fieldsets = [
        (None, {
           "fields": ("title", "description", 'fullDescription'),
        }),
        ("Price options", {
            "fields": ("price",),
            "classes": ("wide", "collapse"),
        }),
        ('Specs options', {
            'fields': ('category', ),
        }),
        ('Product status', {
            'fields': ('freeDelivery', 'available', 'limited')
        }),
        ('Sorting options', {
            'fields': ('index', )
        }),
        ('Rating', {
            'fields': ('rating',),
        }),
    ]

class TagProductInline(admin.TabularInline):
    """
    Inline form for changing products related with Tag instance.

    Attributes:
        model: The model which the inline is using.
    """
    model = Tag.products.through


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin form for a Tag model.

    Attributes:
        inlines: Array of inlines forms.
        list_display: Array of fields that displays at the admin panel.
        list_display_links: Array of fields that redirects to update instance form.
        fieldsets: Array of field sets that define the presentation of form fields.
    """
    inlines = [
        TagProductInline,
    ]
    list_display = 'pk', 'name'
    list_display_links = 'name',
    fieldsets = [
        (None, {
            "fields": ("name", 'category'),
        }),
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin form for a Category model.

    Attributes:
        inlines: Array of inlines forms.
        list_display: Array of fields that displays at the admin panel.
        list_display_links: Array of fields that redirects to update instance form.
        search_fields: Array of fields used in the search.
        fieldsets: Array of field sets that define the presentation of form fields.
    """
    inlines = [
        ImageInline,
    ]
    list_display = 'pk', 'title'
    list_display_links = 'title',
    search_fields = ('title',)
    fieldsets = [
        (None, {
            "fields": ("title",),
        }),
    ]

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    """
    Admin form for a Subcategory model.

    Attributes:
        inlines: Array of inlines forms.
        list_display: Array of fields that displays at the admin panel.
        list_display_links: Array of fields that redirects to update instance form.
        fieldsets: Array of field sets that define the presentation of form fields.
    """
    inlines = [
        ImageInline,
    ]
    list_display = 'pk', 'title'
    list_display_links = 'title',
    fieldsets = [
        (None, {
            "fields": ("title",),
        }),
        ('Category', {
            'fields': ('category',),
        }),
    ]


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """
    Admin form for a Sale model.

    Attributes:
        list_display: Array of fields that displays at the admin panel.
        list_display_links: Array of fields that redirects to update instance form.
        fieldsets: Array of field sets that define the presentation of form fields.
    """
    list_display = 'pk', 'dateFrom', 'dateTo'
    list_display_links = 'dateFrom', 'dateTo'
    fieldsets = [
        (None, {
            "fields": ("salePrice",),
        }),
        ('date', {
            'fields': ('dateFrom', 'dateTo'),
        }),
        (None, {
            'fields': ('product',),
        }),
    ]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin form for a Review model.

    Attributes:
        list_display: Array of fields that displays at the admin panel.
        list_display_links: Array of fields that redirects to update instance form.
        fieldsets: Array of field sets that define the presentation of form fields.
    """
    list_display = 'author', 'text', 'rate'
    list_display_links = 'author',
    fieldsets = [
        ('Author', {
            "fields": ("author", 'email'),
        }),
        ('data', {
            'fields': ('text', 'rate'),
        }),
        (None, {
            'fields': ('product',),
        }),
    ]
