from django.shortcuts import render, redirect, get_object_or_404
from .models import City
# Create your views here.
import folium

# Create your views here.

def show_map(request, title, location, zoom=6):
    m = folium.Map(
        location=location,
        zoom_start=zoom,
        width="100%",
        height="100%"
    )
    html = m._repr_html_()
    return render(request, "Map/basicMap.html", {"map": html, "title": title})


def turkey_only(request):
    return show_map(request, "Turkey", [39.0, 35.0])
    # m = folium.Map(location=[39.0, 35.0], zoom_start=6, width="100%", height="600px")
    # html = m._repr_html_()
    # return render(request, "Map/Turkey.html", {"Turkey":html})

def cities_only(request, city):
    if City.objects.filter(name=city):
        obje_city = City.objects.get(name=city)
        if obje_city.is_metropolitan:
            if obje_city.name=="Istanbul":
                zoom = 10
            else: 
                zoom = 11
        else:
            zoom = 12
        return show_map(request, obje_city.name, [obje_city.qx, obje_city.qy], zoom=zoom)
    

def categories_village_view(request):
   villages = City.objects.all()
   return render(request, 'Categories/Turkey.html',{"villages":villages})