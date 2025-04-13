from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
import json

class UsuarioManager(BaseUserManager):
    def create_user(self,email,username,nombres,apellidos,password=None):
        
        if not email:
            raise ValueError("El usuario debe tener un correo electronico")
        usuario = self.model(
            username = username,
            email = self.normalize_email(email), 
            nombres = nombres, 
            apellidos = apellidos
        )
        usuario.set_password(password)
        usuario.save()
        return usuario
    
    def create_superuser(self,email,username,nombres,apellidos,password):
        usuario = self.create_user(
            email,
            username = username,
            nombres = nombres, 
            apellidos = apellidos,
            password = password,
        )
        usuario.usuario_administrador = True
        usuario.save()
        return usuario
    

class Usuario(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(("Identificacion"), unique=True, max_length=100, default="")
    nombres = models.CharField(max_length=50, blank=False)
    apellidos = models.CharField(max_length=50, blank=False, default="")
    email = models.EmailField(unique=True)
    celular = models.CharField(max_length=15, blank=False, unique=True)
    genero = models.CharField(max_length=10, choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Otro', 'Otro')])
    cargo = models.CharField(max_length=50, choices=[('Administrativo', 'Administrativo'), ('Contador', 'Contador'), ('Recursos humanos', 'Recursos humanos')], default='')
    imagen = models.ImageField(("Imagen de perfil"), upload_to='perfil/', height_field=None, width_field=None, max_length=200, blank=True, null=True)
    usuario_activo = models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default=False)
    objects = UsuarioManager()
    pais = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    
    

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nombres', 'apellidos', 'email',]

    def __str__(self):
        return f"{self.nombres},{self.apellidos}"

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self,app_label):
        return True
    
    @property
    def is_staff(self):
        return self.usuario_administrador
    
class Empleado(models.Model):
    #Activo
    activo = models.BooleanField(default=True)

    # Datos Fiscales
    foto = models.ImageField(upload_to='fotos_empleados/', blank=True, null=True)
    contrato = models.FileField(upload_to='contratos_empleados/', blank=True, null=True)
    numero_interno = models.CharField(max_length=20, blank=False)
    nombres = models.CharField(max_length=100, blank=False)
    apellidos = models.CharField(max_length=100, blank=False)
    fecha_nacimiento = models.DateField(blank=False)
    documento_identidad = models.IntegerField(null=True, blank=False)
    domicilio = models.CharField(max_length=255, blank=False)
    correo = models.EmailField(blank=False)
    telefono = models.IntegerField(null=True, blank=False)
    EPS = models.CharField(max_length=100, blank=False)
    estado_civil = models.CharField(max_length=20, blank=False)
    dependientes_economicos = models.PositiveIntegerField(default=0)
    cargo = models.CharField(max_length=100, blank=False)
    tipo_contrato = models.CharField(max_length=100, blank=False, choices=(
        ('Contrato a Término Fijo', 'Contrato a Término Fijo'),
        ('Contrato a término indefinido', 'Contrato a término indefinido'),
        ('Contrato de Obra o labor', 'Contrato de Obra o labor'),
        ('Contrato civil por prestación de servicios', 'Contrato civil por prestación de servicios'),
        ('Contrato de aprendizaje', 'Contrato de aprendizaje'),
        ('Contrato ocasional, accidental o transitorio de trabajo', 'Contrato ocasional, accidental o transitorio de trabajo'),
    ))
    talla_ropa = models.CharField(max_length=10, blank=False)
    talla_calzado = models.IntegerField(null=True, blank=False)

    # Datos Académicos
    formacion_reglada = models.CharField(max_length=255)
    formacion_complementaria = models.CharField(max_length=255)
    institucion_graduacion = models.CharField(max_length=255)
    experiencias_previas = models.TextField(blank=True)

    # Contacto de emergencia
    relacion_empleado = models.CharField(max_length=100)
    contacto_nombres = models.CharField(max_length=100)
    contacto_apellidos = models.CharField(max_length=100)
    contacto_fecha_nacimiento = models.DateField()
    contacto_carnet_identidad = models.IntegerField(blank=False)
    contacto_domicilio = models.CharField(max_length=255)
    contacto_telefono = models.IntegerField(blank=False)
    contacto_correo = models.EmailField()

    # Datos Bancarios
    banco = models.CharField(max_length=100)
    tipo_cuenta = models.CharField(max_length=20, choices=(('Ahorros', 'Ahorros'), ('Corriente', 'Corriente')))
    numero_cuenta = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    
class Asistencia(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    hora_entrada = models.TimeField(null=True, blank=True)
    hora_salida = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"Asistencia de {self.empleado.nombres} {self.empleado.apellidos} - {self.fecha}"

class Vacacion(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    aprobada = models.BooleanField(default=False)

    def __str__(self):
        return f"Vacaciones de {self.empleado.nombres} {self.empleado.apellidos}"

class Entrevista(models.Model):
    nombre_candidato = models.CharField(max_length=100)
    correo_candidato = models.EmailField()
    fecha_programada = models.DateTimeField()
    cargo_aplicado = models.CharField(max_length=100)

    def __str__(self):
        return f"Entrevista con {self.nombre_candidato} para {self.cargo_aplicado}"

class Permiso(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    motivo = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    aprobado = models.BooleanField(default=False)

    def __str__(self):
        return f"Permiso de {self.empleado.nombres} {self.empleado.apellidos}"

