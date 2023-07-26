from django.contrib import admin

from .forms import LocationForm
from .models import *
# Register your models here.

@admin.register(Dairy)
class DairyAdmin(admin.ModelAdmin):
    list_display = ["name","user","location","is_verified"]
    search_fields = ["name"]

@admin.register(FatRate)
class FatRateAdmin(admin.ModelAdmin):
    list_display = ["id","fat_rate","dairy"]

@admin.register(MilkRecord)
class MilkRecord(admin.ModelAdmin):
    list_display = ["dairy","user","shift","date","created_at","updated_at"]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["location"]
    form = LocationForm
    add_form = LocationForm