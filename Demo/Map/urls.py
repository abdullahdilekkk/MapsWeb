from django.urls import path
from . import views
urlpatterns = [
    path('category/', views.categories_get, name="CategoryPage"),#kategorileri gösteren en parent
    path('category/<slug:category_slug>/', views.category_details_get, name="CategoryDetailsPage"),
    path('category/<slug:category_slug>/<slug:country_slug>/', views.country_details, name="CountryPage"),
    path('category/<slug:category_slug>/<slug:country_slug>/<slug:city_slug>/', views.city_show_map, name="CityShowMap"),




]








    # path('category/<slug:country_slug>', )






    # path('BasicMaps/', ),
    # path('BasicMaps/<slug:country_slug>', ),
    # path('<str:city>', views.cities_only, name="City_Page"),

    # path('Turkey', views.turkey_only),