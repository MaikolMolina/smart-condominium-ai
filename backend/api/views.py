from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from .models import User, UnidadHabitacional, Rol, Privilegio, RolPrivilegio, Cuota
from .serializers import (UserSerializer, LoginSerializer, 
                         UnidadHabitacionalSerializer, RolSerializer, 
                         PrivilegioSerializer, RolPrivilegioSerializer, CuotaSerializer)

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

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

class RolPrivilegioViewSet(viewsets.ModelViewSet):
    queryset = RolPrivilegio.objects.all()
    serializer_class = RolPrivilegioSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def privilegios(self, request, pk=None):
        rol = self.get_object()
        privilegios = rol.privilegios.all()
        serializer = PrivilegioSerializer(privilegios, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def asignar_privilegio(self, request, pk=None):
        rol = self.get_object()
        privilegio_id = request.data.get('privilegio_id')
        
        if not privilegio_id:
            return Response({'error': 'privilegio_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            privilegio = Privilegio.objects.get(id=privilegio_id)
        except Privilegio.DoesNotExist:
            return Response({'error': 'Privilegio no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        # Verificar si ya existe la relación
        if RolPrivilegio.objects.filter(rol=rol, privilegio=privilegio).exists():
            return Response({'error': 'Este privilegio ya está asignado al rol'}, status=status.HTTP_400_BAD_REQUEST)
        
        rol_privilegio = RolPrivilegio.objects.create(rol=rol, privilegio=privilegio)
        serializer = RolPrivilegioSerializer(rol_privilegio)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def remover_privilegio(self, request, pk=None, privilegio_pk=None):
        rol = self.get_object()
        
        try:
            privilegio = Privilegio.objects.get(id=privilegio_pk)
        except Privilegio.DoesNotExist:
            return Response({'error': 'Privilegio no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            rol_privilegio = RolPrivilegio.objects.get(rol=rol, privilegio=privilegio)
            rol_privilegio.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except RolPrivilegio.DoesNotExist:
            return Response({'error': 'Este privilegio no está asignado al rol'}, status=status.HTTP_404_NOT_FOUND)

class CuotaViewSet(viewsets.ModelViewSet):
    queryset = Cuota.objects.all()
    serializer_class = CuotaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Cuota.objects.all()
        # Filtros opcionales por query params
        unidad_id = self.request.query_params.get('unidad_id', None)
        if unidad_id is not None:
            queryset = queryset.filter(unidad_habitacional_id=unidad_id)
        return queryset