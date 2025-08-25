from django.shortcuts import render, redirect, get_object_or_404
from .models import City, Country, Category
import folium, os, csv
from django.conf import settings
from pathlib import Path
from django.urls import reverse
import requests
from folium.plugins import HeatMap


country_cooridnates = {
    "turkey": {
        "center": [39.0, 35.0],
        "zoom": 10,
    },
    "germany": {
        "center": [51.0, 10.0],
        "zoom": 10,
    },
    "france": {
        "center": [46.0, 2.0],
        "zoom": 10,
    },
    "italy": {
        "center": [42.5, 12.5],
        "zoom": 10,
    },
    "spain": {
        "center": [40.0, -4.0],
        "zoom": 10,
    },
    "netherlands": {
        "center": [52.2, 5.3],
        "zoom": 11,
    },
    "united-kingdom": {
        "center": [55.0, -3.0],
        "zoom": 10,
    },
    "usa": {
        "center": [37.0, -95.0],
        "zoom": 6,
    },
    "canada": {
        "center": [56.0, -106.0],
        "zoom": 4,
    },
    "japan": {
        "center": [36.0, 138.0],
        "zoom": 4,
    },
    "greece": {
        "center": [39.0, 22.0],
        "zoom": 10,
    },
}




def show_map(request, title, location, zoom=6):
    m = folium.Map(
        location=location,
        zoom_start=zoom,
        width="100%",
        height="100%"
    )

    folium.TileLayer(tiles='OpenStreetMap').add_to(m)
    folium.TileLayer(tiles='Cartodb Positron').add_to(m)
    folium.TileLayer(tiles='Cartodb dark_matter').add_to(m)
    folium.TileLayer(tiles='OPNVKarte').add_to(m)
    folium.TileLayer(tiles='CyclOSM').add_to(m)
    folium.LayerControl().add_to(m)




    html = m._repr_html_()
    return render(request, "Categories/MarkerOne/Map.html", {"map": html, "title": title})



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
            href_country = reverse(
                "CountryPage",
                kwargs={"category_slug": category.slug, "country_slug": c.slug},
            )
            countries.append({"name":c.name, "href":href_country})


    elif category.slug == "weathers":
        for c in Country.objects.all().order_by("name"):

            if not c.categories.filter(pk=category.pk).exists():
                c.categories.add(category)

            href_weather = reverse(
                "WeatherPage",
                kwargs={"category_slug":category.slug, "country_slug":c.slug}

            )
            countries.append({"name":c.name, "href":href_weather})




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
    coordinate = country_cooridnates.get(country_slug.lower())["center"]

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







def weather_heatmap(request, category_slug, country_slug):
    category = get_object_or_404(Category, slug=category_slug)
    country  = get_object_or_404(Country, slug=country_slug, categories=category)

    key = country_slug.lower().replace("-", " ")
    geo = country_cooridnates.get(key)
    if not geo:
        return render(request, "Categories/MarkerOne/Map.html",
                      {"map": "<p>Bu ülke için koordinat bulunamadı.</p>", "title": country.name})

    lat0, lon0 = geo["center"]
    zoom = geo["zoom"]

    # 1) Baz harita
    m = folium.Map(location=[lat0, lon0], zoom_start=zoom, width="100%", height="100%")

    # 2) Ülkeyi ekrana sığdır
    bounds = {
        "turkey": (25.0, 35.8, 45.0, 42.3),
        "greece": (19.4, 34.6, 28.6, 41.8),
        "germany": (5.5, 47.2, 15.1, 55.1),
        "france": (-5.5, 41.0, 9.6, 51.2),
        "italy": (6.6, 36.6, 18.6, 47.1),
        "spain": (-9.4, 35.5, 3.3, 43.8),
        "netherlands": (3.2, 50.7, 7.3, 53.7),
        "united-kingdom": (-8.6, 49.9, 1.8, 60.9),
        "usa": (-125.0, 24.0, -66.5, 49.5),
        "canada": (-141.0, 41.7, -52.6, 83.1),
        "japan": (129.3, 31.0, 145.8, 45.6),
    }
    if key in bounds:
        L, B, R, T = bounds[key]
        m.fit_bounds([[B, L], [T, R]])

        iso3 = {
            "france": "FRA",
            "germany": "DEU",
            "italy": "ITA",
            "spain": "ESP",
            "netherlands": "NLD",
            "united-kingdom": "GBR",
            "turkey": "TUR",
            "greece": "GRC",
            "usa": "USA",
            "canada": "CAN",
            "japan": "JPN",
        }.get(key)

        if iso3:

            url = f"https://raw.githubusercontent.com/johan/world.geo.json/master/countries/{iso3}.geo.json"
            data = requests.get(url).json()

            folium.GeoJson(
                data,
                name=country.name,
                style_function=lambda _: {#style_function a bir method vermek zorundayız 
                    "color": "#2563eb",
                    "weight": 2,
                    "fillColor": "#60a5fa",
                    "fillOpacity": 0.1,
                },
            ).add_to(m)


    data = requests.get("https://api.rainviewer.com/public/weather-maps.json", timeout=5).json()
    past = data.get("radar").get("past")
    when = past[-1]["time"] if past else None   #list in en son eklenen elamanı yani (-1)
    if when:
        tiles = f"https://tilecache.rainviewer.com/v2/radar/{when}/256/{{z}}/{{x}}/{{y}}/2/1_1.png"
        folium.TileLayer(
            tiles=tiles,
            name="Yağış (Radar)",
            attr="© RainViewer",
            overlay=True,
            control=True,
            show=True,
            opacity=0.8
        ).add_to(m)


    html = m._repr_html_()
    return render(request, "Categories/MarkerOne/Map.html", {"map": html, "title": country.name})

