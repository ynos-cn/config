from utlis.utils import generate_urls
from django.urls import include, path
from .views import org, role, user

urlpatterns = [
    path("org/", include(generate_urls(org))),
    path("role/", include(generate_urls(role))),
    path("user/", include(generate_urls(user))),
]
