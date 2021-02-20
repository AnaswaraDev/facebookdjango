from django.urls import  path
from . import views


urlpatterns = [
    path('register', views.register, name='register'),
    path('home', views.home, name='home'),
    path("<int:id>/feedDetails",views.feedDetails, name="feedDetails"),
    path("<int:pk>/like", views.like, name='like'),
    path("<int:pk>/dislike", views.dislike, name='dislike'),
    path("userProfile", views.userProfile, name="userProfile"),
    path("<int:id>/single",views.single, name="single"),
    path("<int:id>/follow", views.follow, name='follow'),
    path("<int:id>/unfollow", views.unfollow, name='unfollow'),
   
]