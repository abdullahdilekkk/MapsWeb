from django.urls import path
from . import views
urlpatterns = [
    path('', views.turkey_only, name="TurkeyPage"),
]
