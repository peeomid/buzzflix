from django.contrib import admin

from .models import Tracking

# Register your models here.
class TrackingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tracking, TrackingAdmin)