<<<<<<< HEAD
from django.urls import path, include

urlpatterns = [
    path('users', include('users.urls'))
=======
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path("", include("users.urls")),
>>>>>>> main
]
