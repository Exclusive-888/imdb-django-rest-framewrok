from django.db.models import Count, TextField
from django.contrib import admin

from movies.models import Movie
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

# Register your models here.
class TransferAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('imdb_rating')

    ordering = ('-added_at', '-release_date', 'name')
    list_display = (
        'admin_thumbnail', 'name', 'release_date', 'age',
        'is_featured', 'imdb_rating', 'duration')
    list_display_links = ('name',)
    list_editable = ('is_featured',)

admin.site.register(Movie)




def age(self, obj):
    return obj.age
age.admin_order_field = 'release_date'


