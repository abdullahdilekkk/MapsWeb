from django.contrib import admin
from . import models
import os, csv
from django.conf import settings
# Register your models here.

@admin.register(models.City)
class CitiesAdmin(admin.ModelAdmin):
    list_display = ("name", "qx", "qy", "is_metropolitan", "country")
    list_filter = ("name", "is_metropolitan", "country")
    search_fields = ("name", "country")
    actions = ["loadCSV"]

    def loadCSV(self, request, queryset):   
            path = os.path.join(settings.BASE_DIR, "turkey_cities.csv")
            with open(path) as file:
                for row in csv.DictReader(file):
                    models.City.objects.get_or_create(
                        name = row["name"],
                        qx = float(row["qx"]),
                        qy = float(row["qy"]),
                        is_metropolitan = True if row["is_metropolitan"] == "True" else False ,
                        country = row["country"]
                    )
    

    
    loadCSV.short_description = "Cities Load"


