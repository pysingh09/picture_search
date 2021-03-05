import reverse_geocoder as rg
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views import View
from django.views.generic.list import ListView
from flickrapi import FlickrAPI

from picture.models import Location, Favorite

# Global variables
FLICKR_PUBLIC = settings.FLICKR_PUBLIC  # flicker public key
FLICKR_SECRET = settings.FLICKR_SECRET  # flicker secret key
flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format="parsed-json")  # flicker instance
extras = "url_t,url_l,url_o"  # images url types required in response


class PictureView(LoginRequiredMixin, ListView):
    """
    To render home page with available locations
    """
    login_url = "/"
    template_name = "index.html"
    queryset = Location.objects.all()

    def get_context_data(self, **kwargs):
        """
        get the existing locations from database
        """
        context = super().get_context_data(**kwargs)
        obj_values = Location.objects.all().values_list("name", "latitude", "longitude")
        context["locations"] = obj_values
        return context


class PicturesCatalogue(LoginRequiredMixin, View):
    """
    To fetch the pictures using flicker api for given location
    store the location on database if not available
    store the search images to user favorite
    """
    login_url = "/"

    @staticmethod
    def get_location(latitude, longitude):
        """
        method to get location name from given latitude and longitude using reverse_geocoder package
        """
        address = rg.search((latitude, longitude))[0]
        address_list = [
            address.get("name", ""),
            address.get("admin1", ""),
            address.get("cc", ""),
        ]
        output = ", ".join(filter(None, address_list))
        return output

    def post(self, request, *args, **kwargs):
        """
        params: - latitude, longitude, page
        to fetch the images from flicker search api of provided page
        """
        latitude = self.request.POST.get("latitude")
        longitude = self.request.POST.get("longitude")
        page = self.request.POST.get("page")
        picture_list = flickr.photos.search(lat=latitude, lon=longitude, page=page, per_page=10, extras=extras)
        # check location already available in DB
        obj, created = Location.objects.get_or_create(latitude=latitude, longitude=longitude)
        if created:
            # get location name of given latitude and longitude
            obj.name = self.get_location(latitude, longitude)
            obj.save()
        # store photos to user favorite model
        for record in picture_list["photos"]["photo"]:
            Favorite.objects.get_or_create(
                user=self.request.user,
                image_url=record.get("url_t"),
                original_url=record.get("url_l") if record.get("url_l") else record.get("url_o"),
            )
        return JsonResponse({"records": picture_list}, status=200)


class UserFavoriteList(LoginRequiredMixin, ListView):
    """
    To render the user favorite list page as per searching
    """
    login_url = "/"
    model = Favorite
    paginate_by = 10
    template_name = "favorite.html"

    def get_context_data(self, **kwargs):
        """
        get user search images with pagination
        """
        context = super().get_context_data(**kwargs)
        objects = self.model.objects.filter(user=self.request.user).order_by("-created")
        paginator = Paginator(objects, self.paginate_by)
        page = self.request.GET.get("page", 1)
        try:
            car_list = paginator.page(page)
        except PageNotAnInteger:
            car_list = paginator.page(1)
        except EmptyPage:
            car_list = paginator.page(paginator.num_pages)
        context["object_list"] = car_list
        return context
