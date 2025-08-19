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

def istanbul_only(request):
    return show_map(request, "Istanbul", [41.0082, 28.9784], zoom=10)
    
   
