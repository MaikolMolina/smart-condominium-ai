# backend/smart_condo/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # Incluimos los routers de cada app
    path("api/", include("api.urls")),  # Auth, Users, Roles, etc. via router
    path("api/", include("bitacora.urls")),  # Bitácora via router
]
