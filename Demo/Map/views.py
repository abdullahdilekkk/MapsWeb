from django.shortcuts import render, redirect, get_object_or_404
from .models import City, Country, Category
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



def categories_get(request):
    categories = Category.objects.all().order_by("name")
    return render(request, "Categories/MainCategory.html", {"categories":categories})

    


def category_details_get(request, category_slug):
    category_details = get_object_or_404(Category, slug=category_slug)

    if category_details.slug == "basic-maps":
        countries = Country.objects.all().order_by("name")

    else:#şu anlık boş atıyorum zamanla maps türleri ile dolucak
        return redirect('CategoryPage')

    context = {
        "category":category_details,
        "countries":countries
    }

    return render(request, "Categories/CategoryDetails.html", context)


def country_details(request, category_slug, country_slug):
    country = get_object_or_404(Country, slug=country_slug)
    cities = country.cities.all().order_by("name")

    context = {
        "category_slug":category_slug,
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


