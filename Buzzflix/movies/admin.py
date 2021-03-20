from django.contrib import admin

from .models import Category, Movie

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    pass

class MovieAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Movie, MovieAdmin)