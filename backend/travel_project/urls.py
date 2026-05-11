from django.contrib import admin
from django.urls import path, include
from theme.views import home, about , generate_itinerary_view
from theme.views import generate_itinerary_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path("about/", about, name="about"),
    path("generate_itinerary/", generate_itinerary_view, name="generate_itinerary"),
    path(
    "api/generate-itinerary/",
    generate_itinerary_api,
    name="generate_itinerary_api"
),
]
