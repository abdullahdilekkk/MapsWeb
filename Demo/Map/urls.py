from django.urls import path
from . import views
urlpatterns = [
    path('Turkey', views.turkey_only, name="TurkeyPage"),
]
