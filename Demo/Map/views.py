from django.shortcuts import render, redirect

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
    cities = {
        "Istanbul": [41.0082, 28.9784],
        "Ankara": [39.925533, 32.866287],
        "Izmir": [38.4192, 27.1287],
        "Adana": [37.0, 35.3213],
        "Antalya": [36.8969, 30.7133],
        "Bursa": [40.1828, 29.0669],
        "Kayseri": [38.7333, 35.4833],
        "Konya": [37.8716, 32.4846],
        "Gaziantep": [37.0662, 37.3833],
        "Mersin": [36.8121, 34.6415],
        "Sanliurfa": [37.1591, 38.7969],
        "Diyarbakir": [37.9100, 40.2367],
        "Eskisehir": [39.7767, 30.5206],
        "Denizli": [37.7833, 29.0947],
        "Sakarya": [40.7731, 30.3949],
        "Samsun": [41.2867, 36.33],
        "Ordu": [40.9839, 37.8764],
        "Trabzon": [41.0015, 39.7178],
        "Malatya": [38.3552, 38.3095],
        "Van": [38.4946, 43.3832],
        "Manisa": [38.6191, 27.4289],
        "Kahramanmaras": [37.5736, 36.9371],
        "Aydin": [37.8450, 27.8396],
        "Mugla": [37.2153, 28.3636],
        "Balikesir": [39.6484, 27.8826],
        "Tekirdag": [40.9781, 27.5110],
        "Hatay": [36.2028, 36.1600],
        "Adiyaman": [37.7648, 38.2763],
    }

    if city in cities:
        return show_map(request, city, cities[city], zoom=10)
    