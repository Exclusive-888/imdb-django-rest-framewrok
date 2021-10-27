from django.contrib import admin
from django.utils.translation import gettext_lazy as _

class BaseAdmin(admin.ModelAdmin):

    """Base admin for all models using NameSlugStampedModel model"""
    readonly_fields = (
        'added_at', 'added_by', 'updated_at', 'updated_by', 'slug')
