from django.contrib import admin, messages
from . import models
import os, csv, io
from django.conf import settings
import glob
# Register your models here.


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
     list_display = ("name", "slug")
     prepopulated_fields = {"slug": ("name",)}












@admin.register(models.CityCSVUpload)
class CityCSVUploadAdmin(admin.ModelAdmin):
    list_display = ("file",)
    
    def save_model(self, request, obj, form, change):#ismi save_model olamak zorunda 
            super().save_model(request, obj, form, change)

            with obj.file.open("rb") as file:
                reader = csv.DictReader(io.TextIOWrapper(file))
      
                for row in reader:
                        country_obj, _ = models.Country.objects.get_or_create(name=row["country"])

                        models.City.objects.get_or_create(
                            name = row["name"],
                            qx = float(row["qx"]),
                            qy = float(row["qy"]),
                            is_metropolitan = True if row["is_metropolitan"] == "True" else False ,
                            country = country_obj
                        )



@admin.register(models.Country)
class CountriesAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(models.City)
class CitiesAdmin(admin.ModelAdmin):
    list_display = ("name", "qx", "qy", "is_metropolitan", "country")
    list_filter = ("name", "is_metropolitan", "country")
    search_fields = ("name", "country")
    


