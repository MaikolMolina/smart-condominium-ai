from rest_framework import permissions

class TienePrivilegio(permissions.BasePermission):
    """
    Permiso personalizado para verificar si el usuario tiene un privilegio específico.
    """
    
    def has_permission(self, request, view):
        # Superusuarios tienen todos los permisos
        if request.user.is_superuser:
            return True
            
        # Obtener el privilegio requerido de la vista
        privilegio_requerido = getattr(view, 'privilegio_requerido', None)
        
        if not privilegio_requerido:
            return False
            
        # Verificar si el usuario tiene el privilegio a través de sus roles
        return request.user.roles.filter(privilegios__codigo=privilegio_requerido).exists()