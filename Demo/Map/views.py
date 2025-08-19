from django.shortcuts import render, redirect

# Create your views here.
import folium

# Create your views here.
def turkey_only(request):
    m = folium.Map(location=[39.0, 35.0], zoom_start=6, width="100%", height="600px")
    html = m.get_root().render()
    return render(request, "Map/Turkey.html", {"Turkey":html})

def istanbul_only(request):
    m = folium.Map(location=[41.0082, 28.9784], zoom_start=10, width="100%", height="200px")
    html = m._repr_html_()
    return render (request, "Map/istanbul.html", {"Istanbul":html})

