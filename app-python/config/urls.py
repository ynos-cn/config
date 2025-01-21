from utils.utils import generate_urls
from django.urls import include, path
from .views import project, env_info

urlpatterns = [
    path("project/", include(generate_urls(project))),
    path("env/", include(generate_urls(env_info))),
]
