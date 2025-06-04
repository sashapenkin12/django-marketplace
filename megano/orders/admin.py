from django.contrib import admin

from .models import Order

class OrderProductsInline(admin.TabularInline):
    """
    Inline form for changing products related with Order instance.

    Attributes:
        model: The model which the inline is using.
    """
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin form for an Order model.

    Attributes:
        inlines: Array of inlines forms.
        list_display: Array of fields that displays at the admin panel.
        list_display_links: Array of fields that redirects to update instance form.
        fieldsets: Array of field sets that define the presentation of form fields.
    """
    inlines = [
        OrderProductsInline,
    ]
    list_display = 'fullName', 'address', 'status'
    list_display_links = 'address',
    fieldsets = [
        ('Customer', {
            "fields": ("fullName", 'email', 'phone'),
        }),
        ('Order options', {
            'fields': ('deliveryType', 'paymentType'),
        }),
        ('Destination', {
            'fields': ('city', 'address')
        }),
    ]
