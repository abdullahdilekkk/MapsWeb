from django.urls import path
from . import views


urlpatterns = [
   path('signup/', views.signup_details, name="signup"),
   path('logout/', views.logout_details, name='logout'),
#    path('login/', views.login_details, name='login'), zaten bu default django auth den geşiyor 

]
