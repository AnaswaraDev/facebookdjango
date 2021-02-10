from django.urls import  path
from . import views


urlpatterns = [
    path('register', views.register, name='register'),
    path('home', views.home, name='home'),
    path("<int:id>/feedDetails",views.feedDetails, name="feedDetails"),

]