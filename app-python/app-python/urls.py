"""
URL configuration for app-python project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.contrib import admin
from django.urls import include, path
from django.conf.urls import handler400, handler403, handler404, handler500
from .views import custom_404_view, custom_500_view, custom_400_view, custom_403_view

# api 版本
# version = "v1"
prefix = "api/"

urlpatterns = [
    path(f"{prefix}login/", include("login.urls")),
    path(f"{prefix}sys/", include("system.urls")),
    path(f"{prefix}config/", include("config.urls")),
]

handler400 = custom_400_view
handler403 = custom_403_view
handler404 = custom_404_view
handler500 = custom_500_view
