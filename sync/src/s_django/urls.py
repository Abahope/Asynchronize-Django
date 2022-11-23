from django.urls import path, include
from django.http import HttpResponse


urlpatterns = [
    path("", lambda r: HttpResponse("Hello, world.")),
    path("posts/", include("posts.urls")),
]
