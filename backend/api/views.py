from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from .models import (
    User,
    UnidadHabitacional,
    Rol,
    Privilegio,
    RolPrivilegio,
    Cuota,
    Invitado,
)
from .serializers import (
    UserSerializer,
    LoginSerializer,
    UnidadHabitacionalSerializer,
    RolSerializer,
    PrivilegioSerializer,
    RolPrivilegioSerializer,
    CuotaSerializer,
    InvitadoSerializer,
)
from .permissions import TienePrivilegio

from bitacora.utils import registrar_bitacora


class AuthViewSet(viewsets.ViewSet):
    """
    /api/auth/login/  -> POST {username, password} -> {access, refresh, user}
    /api/auth/logout/ -> POST {refresh|refresh_token} -> 205
    """

    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)

            # Bitácora: LOGIN exitoso
            try:
                registrar_bitacora(
                    request,
                    accion="LOGIN",  # usa choices del modelo
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

        # (opcional) podrías registrar intento fallido si amplías tus choices
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def logout(self, request):
        """
        Acepta {"refresh"} o {"refresh_token"} y siempre intenta registrar en bitácora,
        incluso si el cliente ya no tiene access (por eso AllowAny).
        """
        refresh_token = request.data.get("refresh") or request.data.get("refresh_token")
        user_obj = None

        if not refresh_token:
            # (opcional) registra fallo si amplías tus choices
            return Response(
                {"detail": "refresh token required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            rt = RefreshToken(refresh_token)

            # Intenta resolver el usuario del payload del refresh
            user_id = rt.get("user_id", None)
            if user_id:
                try:
                    user_obj = User.objects.get(pk=user_id)
                except User.DoesNotExist:
                    user_obj = None

            # Blacklist si está activado
            try:
                rt.blacklist()
            except Exception:
                pass

            # Bitácora: LOGOUT correcto
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
            # (opcional) registra fallo si amplías tus choices
            return Response(
                {"detail": "invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST
            )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, TienePrivilegio]

    def get_privilegio_requerido(self):
        if self.action == "list" or self.action == "retrieve":
            return "users.view"
        elif self.action == "create":
            return "users.create"
        elif self.action == "update" or self.action == "partial_update":
            return "users.edit"
        elif self.action == "destroy":
            return "users.delete"
        return None

    def get_permissions(self):
        # Asignar el privilegio requerido a la vista
        self.privilegio_requerido = self.get_privilegio_requerido()
        return super().get_permissions()


class UnidadHabitacionalViewSet(viewsets.ModelViewSet):
    queryset = UnidadHabitacional.objects.all()
    serializer_class = UnidadHabitacionalSerializer
    permission_classes = [IsAuthenticated, TienePrivilegio]

    def get_privilegio_requerido(self):
        if self.action == "list" or self.action == "retrieve":
            return "units.view"
        elif self.action == "create":
            return "units.create"
        elif self.action == "update" or self.action == "partial_update":
            return "units.edit"
        elif self.action == "destroy":
            return "units.delete"
        return None

    def get_permissions(self):
        self.privilegio_requerido = self.get_privilegio_requerido()
        return super().get_permissions()


class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated, TienePrivilegio]

    def get_privilegio_requerido(self):
        if self.action in ["list", "retrieve"]:
            return "roles.view"
        elif self.action == "create":
            return "roles.create"
        elif self.action in ["update", "partial_update"]:
            return "roles.edit"
        elif self.action == "destroy":
            return "roles.delete"
        return None

    def get_permissions(self):
        self.privilegio_requerido = self.get_privilegio_requerido()
        return super().get_permissions()


class PrivilegioViewSet(viewsets.ModelViewSet):
    queryset = Privilegio.objects.all()
    serializer_class = PrivilegioSerializer
    permission_classes = [IsAuthenticated, TienePrivilegio]

    def get_privilegio_requerido(self):
        if self.action == "list" or self.action == "retrieve":
            return "privileges.view"
        elif self.action == "create":
            return "privileges.create"
        elif self.action == "update" or self.action == "partial_update":
            return "privileges.edit"
        elif self.action == "destroy":
            return "privileges.delete"
        return None

    def get_permissions(self):
        self.privilegio_requerido = self.get_privilegio_requerido()
        return super().get_permissions()


class RolPrivilegioViewSet(viewsets.ModelViewSet):
    queryset = RolPrivilegio.objects.all()
    serializer_class = RolPrivilegioSerializer
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

        # Verificar si ya existe la relación
        if RolPrivilegio.objects.filter(rol=rol, privilegio=privilegio).exists():
            return Response(
                {"error": "Este privilegio ya está asignado al rol"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rol_privilegio = RolPrivilegio.objects.create(rol=rol, privilegio=privilegio)
        serializer = RolPrivilegioSerializer(rol_privilegio)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"])
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
    permission_classes = [IsAuthenticated, TienePrivilegio]

    def get_privilegio_requerido(self):
        if self.action == "list" or self.action == "retrieve":
            return "fees.view"
        elif self.action == "create":
            return "fees.create"
        elif self.action == "update" or self.action == "partial_update":
            return "fees.edit"
        elif self.action == "destroy":
            return "fees.delete"
        return None

    def get_permissions(self):
        self.privilegio_requerido = self.get_privilegio_requerido()
        return super().get_permissions()


class InvitadoViewSet(viewsets.ModelViewSet):
    queryset = Invitado.objects.all()
    serializer_class = InvitadoSerializer
    permission_classes = [IsAuthenticated, TienePrivilegio]

    def get_privilegio_requerido(self):
        if self.action == "list" or self.action == "retrieve":
            return "guests.view"
        elif self.action == "create":
            return "guests.create"
        elif self.action == "update" or self.action == "partial_update":
            return "guests.edit"
        elif self.action == "destroy":
            return "guests.delete"
        return None

    def get_permissions(self):
        self.privilegio_requerido = self.get_privilegio_requerido()
        return super().get_permissions()

    def get_queryset(self):
        queryset = Invitado.objects.all()

        # Si el usuario no es administrador, solo puede ver sus propios invitados
        if not self.request.user.is_superuser:
            queryset = queryset.filter(residente=self.request.user)

        # Filtros opcionales
        estado = self.request.query_params.get("estado", None)
        if estado is not None:
            queryset = queryset.filter(estado=estado)

        fecha_desde = self.request.query_params.get("fecha_desde", None)
        if fecha_desde is not None:
            queryset = queryset.filter(fecha_evento__gte=fecha_desde)

        fecha_hasta = self.request.query_params.get("fecha_hasta", None)
        if fecha_hasta is not None:
            queryset = queryset.filter(fecha_evento__lte=fecha_hasta)

        return queryset

    def perform_create(self, serializer):
        # Asignar automáticamente el residente actual al crear un invitado
        serializer.save(residente=self.request.user)

    @action(detail=True, methods=["post"])
    def aprobar(self, request, pk=None):
        if not request.user.is_superuser:
            return Response(
                {"error": "Solo los administradores pueden aprobar invitados"},
                status=status.HTTP_403_FORBIDDEN,
            )

        invitado = self.get_object()
        invitado.estado = "aprobado"
        invitado.save()

        serializer = self.get_serializer(invitado)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def rechazar(self, request, pk=None):
        if not request.user.is_superuser:
            return Response(
                {"error": "Solo los administradores pueden rechazar invitados"},
                status=status.HTTP_403_FORBIDDEN,
            )

        invitado = self.get_object()
        observaciones = request.data.get("observaciones", "")

        invitado.estado = "rechazado"
        invitado.observaciones = observaciones
        invitado.save()

        serializer = self.get_serializer(invitado)
        return Response(serializer.data)
