from django.shortcuts import render, redirect, get_object_or_404
from .models import City, Country, Category
import folium, os, csv
from django.conf import settings
from pathlib import Path
from django.urls import reverse


country_cooridnates = {
    "turkey": [39.0, 35.0],
    "germany": [51.0, 10.0],
    "france": [46.0, 2.0],
    "italy": [42.5, 12.5],
    "spain": [40.0, -4.0],
    "netherlands": [52.2, 5.3],
    "united kingdom": [55.0, -3.0],#sorun olabilir boşluk ve slug 
    "usa": [37.0, -95.0],
    "canada": [56.0, -106.0],
    "japan": [36.0, 138.0],
    "greece": [39.0, 22.0], 
}

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
    category = get_object_or_404(Category, slug=category_slug)

    countries = []

    if category.slug == "metropolitans":
        base = Path(settings.BASE_DIR) / "MarkerOneCSV" / "metropolitans"
        
        for p in sorted(base.glob("*.csv")):    #glob oradaki (içindeki) dosyayı bulur
            #base de benim zaten dosya yolum yani dosya yolumun ordaki parantez içindeki dosyayla eşleşenler 
            slug = p.stem.lower()   
            # p.name    > "france.csv"
            # p.stem    > "france"
            # p.suffix  > ".csv"
            # p= bir yol misal Demo/MarkerOneCSV/metropolitans/france.csv

            country, _ = Country.objects.get_or_create(  
                #get_or_create her zaman tuple döndürürü(obj, created)  burada _ demek kullanılmıyor o demek 
                #obj =zaten country created de boolean döner ama kullanmıyoruz
                slug=slug, defaults={"name": slug.replace("-", " ").title()}
                #eğer slug=slug objesi yoksa defaults a göre oluşturur 
                #burada da sluguna değer veriyoruz slug=north-korea olarak gelir 
                #replace - gördğü yere space atar titlr da herkelimenin baş harfini büyütür 
                #böylece name = "North Korea"
            )


            if not country.categories.filter(pk=category.pk).exists():
                #manytomany ilişki var coutry ve category arasında ve modelde dedik ki country den related_name
                #olarak categories olarak erişsin dedik böylece 
                country.categories.add(category)
                # Eğer bu ülke zaten bu kategoriye bağlı değilse, kategoriye ekle
                #kast ettiğim category slug ile gelen yani metropolitans a itlya nın categorileri bağlı mı

            #from django.urls import reverse imporu ile çalışır 
            href = reverse(
                "metropolitanMapsPage",
                kwargs={"category_slug": category.slug, "country_slug": country.slug},
            )

            #reverse url oluşturucak misal urls de şöyel bir path var
            #path('deneme/<slug:birinci_slug>, views.method, name="page")

            #url = reverse(
            #   "page",
            #   kwargs={"birinci_slug":merhabalar}
            #)


            countries.append({"name": country.name, "href": href})

    elif category.slug == "basic-maps":

        for c in Country.objects.filter(categories=category).order_by("name"):
            href = reverse(
                "CountryPage",
                kwargs={"category_slug": category.slug, "country_slug": c.slug},
            )
            countries.append({"name": c.name, "href": href})

    return render(request, "Categories/CategoryDetails.html", {"category": category, "countries": countries},)


def country_details(request, category_slug, country_slug):
    category = get_object_or_404(Category, slug=category_slug)
    country  = get_object_or_404(Country, slug=country_slug, categories=category)

    # Bu ülkeye ait, bu kategoriye bağlı şehirler
    qs = City.objects.filter(country=country, category=category).order_by("name")

    cities = []
    for c in qs:
        href = reverse(
            "CityShowMap",
            kwargs={
                "category_slug": category.slug,
                "country_slug":  country.slug,
                "city_slug":     c.slug,
            },
        )
        cities.append({"name": c.name, "href": href})

    context = {"category": category, "country": country, "cities": cities}
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

def metropolitanMaps(request ,category_slug, country_slug):
    category_details, _ = Category.objects.get_or_create(
        slug=category_slug, defaults={"name": category_slug.capitalize()}
    )
    country, _ = Country.objects.get_or_create(
        slug=country_slug, defaults={"name": country_slug.capitalize()}
    )
    country.categories.add(category_details)

    csv_path = Path(settings.BASE_DIR) / "MarkerOneCSV" / category_slug / f"{country_slug}.csv"

    # 1) slug'ı lower ederek al
    coordinate = country_cooridnates.get(country_slug.lower())

    # 2) ülkeye göre sabit zoom (USA daha uzaktan)
    if country_slug.lower() == "usa":
        zoom = 4
    
    else:
        zoom = 6


    # 3) m'yi önce oluştur (else bloğunda kullanacağız)
    m = folium.Map(location=coordinate or [0, 0], zoom_start=zoom, width="100%", height="100%")

    fg_metro = folium.FeatureGroup(name="Metropolitan")
    fg_other = folium.FeatureGroup(name="Small City")

    if os.path.exists(csv_path):
        with open(csv_path) as file:
            for row in csv.DictReader(file):
                name = row["name"]
                qx = float(row["qx"])
                qy = float(row["qy"])
                is_metropolitan = row["is_metropolitan"].strip().lower() == "true"
                group = fg_metro if is_metropolitan else fg_other

                folium.CircleMarker(
                    location=[qx, qy],
                    radius=6,
                    popup=name,
                    fill=True,
                    fill_opacity=0.9
                ).add_to(group)
    else:
        # m artık var; burada güvenle kullanıyoruz
        folium.Marker(coordinate or [0, 0], popup=f"CSV bulunamadı: {csv_path}").add_to(m)

    fg_metro.add_to(m)
    fg_other.add_to(m)

    html = m._repr_html_()
    return render(request, "Categories/MarkerOne/Map.html", {"map": html, "title": country.name })
