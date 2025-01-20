from utils.utils import generate_urls
from django.urls import include, path
from .views import project

urlpatterns = [
    path("project/", include(generate_urls(project))),
]
