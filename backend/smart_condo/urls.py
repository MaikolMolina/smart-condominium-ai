from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    AuthViewSet,
    UserViewSet,
    UnidadHabitacionalViewSet,
    RolViewSet,
    PrivilegioViewSet,
    RolPrivilegioViewSet,
    CuotaViewSet,
    InvitadoViewSet,
)

router = DefaultRouter()
router.register(r"auth", AuthViewSet, basename="auth")
router.register(r"users", UserViewSet)
router.register(r"unidades", UnidadHabitacionalViewSet)
router.register(r"roles", RolViewSet)
router.register(r"privilegios", PrivilegioViewSet)
router.register(r"rol-privilegios", RolPrivilegioViewSet, basename="rolprivilegio")
router.register(r"cuotas", CuotaViewSet)
router.register(r"invitados", InvitadoViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/", include("bitacora.urls")),
    path("api/", include("areas.urls")),
]
