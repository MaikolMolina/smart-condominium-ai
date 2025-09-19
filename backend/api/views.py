# backend/api/views.py
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

# MODELOS (ajusta si tus nombres difieren)
from .models import (
    User,
    UnidadHabitacional,
    Rol,
    Privilegio,
    RolPrivilegio,
    Cuota,
)

# SERIALIZERS (ajusta si tus nombres/rutas difieren)
from .serializers import (
    UserSerializer,
    LoginSerializer,
    UnidadHabitacionalSerializer,
    RolSerializer,
    PrivilegioSerializer,
    RolPrivilegioSerializer,
    CuotaSerializer,
)

# Bitácora (logging explícito para auth)
from bitacora.utils import registrar_bitacora


class AuthViewSet(viewsets.ViewSet):
    """
    /api/auth/login/   -> POST {username, password} -> {access, refresh, user}
    /api/auth/logout/  -> POST {refresh | refresh_token} -> 205
    """

    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)

            # Bitácora: ACCESO
            try:
                registrar_bitacora(
                    request,
                    accion="ACCESO",
                    entidad="AUTH",
                    status=status.HTTP_200_OK,
                    user=user,
                    extra={"endpoint": "login"},
                )
            except Exception:
                pass

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def logout(self, request):
        """
        Acepta {"refresh": "..."} o {"refresh_token": "..."}.
        No requiere estar autenticado (AllowAny) para que SIEMPRE podamos registrar en bitácora,
        incluso si el frontend ya borró el access token.
        """
        refresh_token = request.data.get("refresh") or request.data.get("refresh_token")
        user_obj = None

        if not refresh_token:
            try:
                registrar_bitacora(
                    request,
                    accion="LOGOUT_FALLIDO",
                    entidad="AUTH",
                    status=status.HTTP_400_BAD_REQUEST,
                    extra={"endpoint": "logout", "error": "missing refresh token"},
                )
            except Exception:
                pass
            return Response(
                {"detail": "refresh token required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            rt = RefreshToken(refresh_token)

            # intenta resolver el usuario desde el payload del refresh
            user_id = rt.get("user_id", None)
            if user_id:
                try:
                    user_obj = User.objects.get(pk=user_id)
                except User.DoesNotExist:
                    user_obj = None

            # intenta poner en blacklist (si tienes token_blacklist instalado)
            try:
                rt.blacklist()
            except Exception:
                pass

            # registra LOGOUT correcto
            try:
                registrar_bitacora(
                    request,
                    accion="LOGOUT",
                    entidad="AUTH",
                    status=status.HTTP_205_RESET_CONTENT,
                    user=user_obj,
                    extra={"endpoint": "logout"},
                )
            except Exception:
                pass

            return Response(status=status.HTTP_205_RESET_CONTENT)

        except Exception as ex:
            # refresh inválido → igual registramos el intento
            try:
                registrar_bitacora(
                    request,
                    accion="LOGOUT_FALLIDO",
                    entidad="AUTH",
                    status=status.HTTP_400_BAD_REQUEST,
                    user=user_obj,
                    extra={"endpoint": "logout", "error": str(ex)},
                )
            except Exception:
                pass
            return Response(
                {"detail": "invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Bitácora: ACCESO_FALLIDO
        try:
            registrar_bitacora(
                request,
                accion="ACCESO_FALLIDO",
                entidad="AUTH",
                status=status.HTTP_400_BAD_REQUEST,
                extra={"endpoint": "login", "errors": serializer.errors},
            )
        except Exception:
            pass
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    /api/users/       (CRUD segun permisos)
    /api/users/me/    (perfil del usuario autenticado)
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="me",
    )
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UnidadHabitacionalViewSet(viewsets.ModelViewSet):
    queryset = UnidadHabitacional.objects.all()
    serializer_class = UnidadHabitacionalSerializer
    permission_classes = [IsAuthenticated]


class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated]


class PrivilegioViewSet(viewsets.ModelViewSet):
    queryset = Privilegio.objects.all()
    serializer_class = PrivilegioSerializer
    permission_classes = [IsAuthenticated]


class RolPrivilegioViewSet(viewsets.ModelViewSet):
    queryset = RolPrivilegio.objects.all()
    serializer_class = RolPrivilegioSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get"])
    def privilegios(self, request, pk=None):
        rol = self.get_object()
        privilegios = rol.privilegios.all()
        serializer = PrivilegioSerializer(privilegios, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def asignar_privilegio(self, request, pk=None):
        rol = self.get_object()
        privilegio_id = request.data.get("privilegio_id")

        if not privilegio_id:
            return Response(
                {"error": "privilegio_id es requerido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            privilegio = Privilegio.objects.get(id=privilegio_id)
        except Privilegio.DoesNotExist:
            return Response(
                {"error": "Privilegio no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        # Evitar duplicado
        if RolPrivilegio.objects.filter(rol=rol, privilegio=privilegio).exists():
            return Response(
                {"error": "Este privilegio ya está asignado al rol"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rol_privilegio = RolPrivilegio.objects.create(rol=rol, privilegio=privilegio)
        serializer = RolPrivilegioSerializer(rol_privilegio)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["delete"],
        url_path="remover_privilegio/(?P<privilegio_pk>[^/.]+)",
    )
    def remover_privilegio(self, request, pk=None, privilegio_pk=None):
        rol = self.get_object()
        try:
            privilegio = Privilegio.objects.get(id=privilegio_pk)
        except Privilegio.DoesNotExist:
            return Response(
                {"error": "Privilegio no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            rol_privilegio = RolPrivilegio.objects.get(rol=rol, privilegio=privilegio)
            rol_privilegio.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except RolPrivilegio.DoesNotExist:
            return Response(
                {"error": "Este privilegio no está asignado al rol"},
                status=status.HTTP_404_NOT_FOUND,
            )


class CuotaViewSet(viewsets.ModelViewSet):
    queryset = Cuota.objects.all()
    serializer_class = CuotaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        unidad_id = self.request.query_params.get("unidad_id")
        if unidad_id:
            qs = qs.filter(unidad_habitacional_id=unidad_id)
        return qs
