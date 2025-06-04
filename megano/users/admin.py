"""
Users app admin control panel module.
"""

from django.contrib import admin

from .models import Image, Profile, SiteSetting


class ImageInline(admin.StackedInline):
    """
    Inline form for an Image model.

    Attributes:
        model: The model which the inline is using.
        fields: Form fields
        extra: The number of extra forms the formset will display in addition to the initial forms.
        can_delete: Specifies whether the admin can delete inline objects or not.
    """
    model = Image
    fields = ['image', 'content']
    extra = 0
    can_delete = False


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin form for a Profile model.

    Attributes:
        inlines: Array of inlines forms.
        list_display: Array of fields that displays at the admin panel.
        list_display_links: Array of fields that redirects to update instance form.
        fieldsets: Array of fieldsets that determine form fields representation.
    """
    inlines = [
        ImageInline,
    ]
    list_display = 'fullName', 'email'
    list_display_links = 'fullName', 'email'
    fieldsets = [
        ('Customer', {
            "fields": ("fullName", 'email', 'phone'),
        }),
        ('User options', {
            'fields': ('user',),
            "classes": ("wide", "collapse"),
        }),
    ]


@admin.register(SiteSetting)
class SettingsAdmin(admin.ModelAdmin):
    """
    Admin form for a SiteSetting model.

    Attributes:
        list_display: Array of fields that displays at the admin panel.
        list_display_links: Array of fields that redirects to update instance form.
        fieldsets: Array of fieldsets that determine form fields representation.
    """
    list_display = 'key', 'value'
    list_display_links = 'key', 'value'
    fieldsets = [
        ('', {
            "fields": ("key", 'value'),
        }),
    ]
