from django.urls import path

import posts.views

urlpatterns = [
    path("cpu/", posts.views.cpu),
    path("io_create/", posts.views.io_create),
    path("io_read/", posts.views.io_read),
]
