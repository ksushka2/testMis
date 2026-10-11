from django.urls import path

from core.views import (
    access_denied,
    home,
    request_create,
    request_detail,
    request_list,
)

urlpatterns = [
    path("", home, name="home"),
    path("requests/", request_list, name="request_list"),
    path("requests/new/", request_create, name="request_create"),
    path("requests/<int:pk>/", request_detail, name="request_detail"),
    path("access-denied/", access_denied, name="access_denied"),
]
