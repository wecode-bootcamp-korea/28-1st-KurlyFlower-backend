from django.urls import path, include

urlpatterns = [
    path("", include("users.urls")),
    path("", include("products.urls")),
]
