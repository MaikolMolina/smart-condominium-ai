# backend/api/urls.py
from rest_framework.routers import DefaultRouter
from .views import (
    AuthViewSet,
    UserViewSet,
    UnidadHabitacionalViewSet,
    RolViewSet,
    PrivilegioViewSet,
    RolPrivilegioViewSet,
    CuotaViewSet,
)

router = DefaultRouter()
router.register(
    r"auth", AuthViewSet, basename="auth"
)  # /api/auth/login, /api/auth/logout
router.register(r"users", UserViewSet, basename="users")  # /api/users/, /api/users/me/
router.register(r"unidades", UnidadHabitacionalViewSet, basename="unidades")
router.register(r"roles", RolViewSet, basename="roles")
router.register(r"privileges", PrivilegioViewSet, basename="privileges")
router.register(r"rol-privilegios", RolPrivilegioViewSet, basename="rol-privilegios")
router.register(r"cuotas", CuotaViewSet, basename="cuotas")

urlpatterns = router.urls
