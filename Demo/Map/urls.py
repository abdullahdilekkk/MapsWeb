from django.urls import path
from . import views
urlpatterns = [
    path('Turkey', views.turkey_only),
    path('<str:city>', views.cities_only, name="City_Page"),
    path('Categories/Turkey', views.categories_village_view, name="Deneme1kategori")
]
