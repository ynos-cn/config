from utlis.utils import generate_urls
from django.urls import include, path
from .views import projcet

urlpatterns = [
    path("projcet/", include(generate_urls(projcet))),
]
