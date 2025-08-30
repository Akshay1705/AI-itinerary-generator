from django.contrib import admin
from django.urls import path, include
from theme.views import home, about , generate_itinerary_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path("about/", about, name="about"),
    path("generate_itinerary/", generate_itinerary_view, name="generate_itinerary"),
    path("__reload__/", include("django_browser_reload.urls")),
]
