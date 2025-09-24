from django.db import models
from django.contrib.auth.models import AbstractUser

class UnidadHabitacional(models.Model):
    numero = models.CharField(max_length=10)
    piso = models.CharField(max_length=10, blank=True, null=True)
    torre = models.CharField(max_length=10, blank=True, null=True)
    metraje = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.torre or ''} - {self.piso or ''} - {self.numero}"
    
class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class User(AbstractUser):
    TIPO_USUARIO = [
        ('admin', 'Administrador'),
        ('residente', 'Residente'),
        ('inquilino', 'Inquilino'),
        ('mantenimiento', 'Personal de Mantenimiento'),
        ('seguridad', 'Personal de Seguridad'),
    ]
    
    ci = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios')
    unidad_habitacional = models.ForeignKey(UnidadHabitacional, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.ci}"


class Privilegio(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    codigo = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class RolPrivilegio(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    privilegio = models.ForeignKey(Privilegio, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('rol', 'privilegio')

    def __str__(self):
        return f"{self.rol.nombre} - {self.privilegio.nombre}"
    
class Cuota(models.Model):
    TIPO_CHOICES = [
        ('ordinaria', 'Ordinaria'),
        ('extraordinaria', 'Extraordinaria'),
        ('multa', 'Multa'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
        ('vencida', 'Vencida'),
    ]

    unidad_habitacional = models.ForeignKey(UnidadHabitacional, on_delete=models.CASCADE, related_name='cuotas')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='ordinaria')
    descripcion = models.TextField(blank=True, null=True)
    fecha_emision = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cuota {self.tipo} - {self.unidad_habitacional} - {self.monto}"

    class Meta:
        ordering = ['-fecha_emision']

class Invitado(models.Model):
    TIPO_EVENTO_CHOICES = [
        ('cumpleanos', 'Cumpleaños'),
        ('reunion', 'Reunión'),
        ('fiesta', 'Fiesta'),
        ('otro', 'Otro'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]

    residente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitados')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    ci = models.CharField(max_length=20, verbose_name='Cédula de Identidad')
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    tipo_evento = models.CharField(max_length=20, choices=TIPO_EVENTO_CHOICES, default='reunion')
    descripcion_evento = models.TextField(blank=True, null=True)
    fecha_evento = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    numero_invitados = models.PositiveIntegerField(default=1)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    observaciones = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.fecha_evento}"

    class Meta:
        ordering = ['-creado_en']
        verbose_name = 'Invitado'
        verbose_name_plural = 'Invitados'