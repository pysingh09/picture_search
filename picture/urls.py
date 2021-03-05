from django.contrib.auth import views as auth_views
from django.urls import path

from picture.views import PictureView, PicturesCatalogue, UserFavoriteList

urlpatterns = [
    path("", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("home/", PictureView.as_view(), name="home"),
    path("flicker-images/", PicturesCatalogue.as_view(), name="flicker-images"),
    path("favorite-images/", UserFavoriteList.as_view(), name="favorite-images"),
]
