from django.shortcuts import render, redirect, get_object_or_404
from .models import City, Country, Category
# Create your views here.
import folium, os, csv
from django.conf import settings

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



def categories_get(request):
    categories = Category.objects.all().order_by("name")
    return render(request, "Categories/MainCategory.html", {"categories":categories})

    


def category_details_get(request, category_slug):
    category_details = get_object_or_404(Category, slug=category_slug)

    countries = Country.objects.filter(categories=category_details).order_by("name")

    context = {
        "category":category_details,
        "countries":countries
    }

    return render(request, "Categories/CategoryDetails.html", context)


def country_details(request, category_slug, country_slug):

    category = get_object_or_404(Category, slug=category_slug)
    country = get_object_or_404(Country, slug=country_slug, categories=category)
    # Bu ülkeye ait, bu kategoriye bağlı şehirler
    cities = City.objects.filter(country=country, category=category).order_by("name")

    context = {
        "category": category,
        "country":country,
        "cities":cities
    }

    return render(request, "Categories/CountryDetails.html", context) 

def city_show_map(request, category_slug, country_slug, city_slug):

    country = get_object_or_404(Country, slug=country_slug)#county deki aynı isimli cityler hata vermesin diye
    city = get_object_or_404(City, country=country, slug=city_slug)

    if city.is_metropolitan:
        if city.name=="Istanbul":
            zoom = 10
        else: 
            zoom = 11
    else:
        zoom = 12
    return show_map(request, city.name, [city.qx, city.qy], zoom=zoom)


def turkeyMetropolitan(request):
    path = os.path.join(settings.BASE_DIR, "MarkerOne", "turkey_cities.csv")

    m = folium.Map(location=[39.0, 35.0], zoom_start = 6)

    fg_metropolitan = folium.FeatureGroup(name = "Metroplitan")
    fg_other = folium.FeatureGroup(name = "Other")

    with open(path) as file:

        for row in csv.DictReader(file):
            name = row["name"]
            qx = float(row["qx"])
            qy = float(row["qy"])
            is_metropolitan = row["is_metropolitan"].strip().lower() == "true"
            group = fg_metropolitan if is_metropolitan else fg_other



            folium.CircleMarker(
                location=[qx, qy],
                radius=6,    #Dairenin yarıçapı
                popup=name,  #daireye tıklanınca çıkacak şey misal burada isim çıkıyor 
                fill = True,
                fill_opacity=0.9
            ).add_to(group)
    
    fg_metropolitan.add_to(m)   
    fg_other.add_to(m)
    #BUARAYA LAYERCONTROL EKLİYİCEM 

    html = m._repr_html_()


    return render (request, 'Categories/MarkerOne/turkey_metropolitan.html', {"map":html})