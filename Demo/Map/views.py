from django.shortcuts import render, redirect

# Create your views here.
import folium

# Create your views here.
def turkey_only(request):
    m = folium.Map(location=[39.0, 35.0], zoom_start=6, width="50%", height="100px")
    html = m.get_root().render()
    return render(request, "Map/Turkey.html", {"Turkey":html})