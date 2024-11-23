from datetime import date
from django.db import models
from doctor.const import CIVIL_CHOICES, SEX_CHOICES
from django.contrib.auth.models import User
from doctor.utils import valida_cedula,phone_regex

      

class TipoSangre(models.Model):
  
    tipo = models.CharField(max_length=10, verbose_name="Tipo de Sangre", unique=True)
    descripcion = models.CharField(max_length=100, verbose_name="Descripcion")
    class Meta:
    
        verbose_name = "Tipo de Sangre"
        verbose_name_plural = "Tipos de Sangre"
        
    def __str__(self):
        return self.tipo 
    

class ActivePatientManager(models.Manager):
 
    def get_queryset(self):
         
        return super().get_queryset().filter(activo=True)
               


class Paciente(models.Model):
  
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    cedula = models.CharField(max_length=10, verbose_name="Cédula",validators=[valida_cedula])
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    
    telefono = models.CharField(max_length=20, verbose_name="Teléfono(s)",validators=[phone_regex])
    
    email = models.EmailField(verbose_name="Correo", null=True, blank=True,unique=True)
  
    sexo = models.CharField(max_length=1, choices=SEX_CHOICES, verbose_name="Sexo")
   
    estado_civil = models.CharField(max_length=10, choices=CIVIL_CHOICES, verbose_name="Estado Civil")
    
    direccion = models.CharField(max_length=255, verbose_name="Dirección Domiciliaria")
  
    latitud = models.DecimalField(max_digits=18, decimal_places=6, verbose_name="Latitud", null=True, blank=True)
  
    longitud = models.DecimalField(max_digits=18, decimal_places=6, verbose_name="Longitud", null=True, blank=True)
    
    tipo_sangre = models.ForeignKey(TipoSangre, on_delete=models.SET_NULL, null=True, verbose_name="Tipo de Sangre",related_name="tipos_sangre")
   
    foto = models.ImageField(upload_to='pacientes/', verbose_name="Foto", null=True, blank=True)
   
    alergias = models.CharField(max_length=100,verbose_name="Alergias", null=True, blank=True)
  
    enfermedades_cronicas = models.CharField(max_length=100,verbose_name="Enfermedades Crónicas", null=True, blank=True)
   
    medicacion_actual = models.CharField(max_length=100,verbose_name="Medicación Actual", null=True, blank=True)
  
    cirugias_previas = models.CharField(max_length=100,verbose_name="Cirugías Previas", null=True, blank=True)
    # Antecedentes médicos personales del paciente (enfermedades pasadas, hábitos, etc.)
    antecedentes_personales = models.TextField(verbose_name="Antecedentes Personales", null=True, blank=True)
    # Antecedentes médicos familiares del paciente (enfermedades hereditarias, condiciones genéticas)
    antecedentes_familiares = models.TextField(verbose_name="Antecedentes Familiares", null=True, blank=True)
    activo = models.BooleanField(default=True,verbose_name="Activo")
    
    objects = models.Manager()  # Manager predeterminado
    active_patient = ActivePatientManager()  # Manager Personalizado
   
    class Meta:
        # Define el orden predeterminado de los pacientes por nombre
        ordering = ['apellidos']
        indexes = [models.Index(fields=['apellidos'])]
        # Nombre en singular y plural del modelo en la interfaz de administración
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
    
    
    
    @property
    def nombre_completo(self):
        return f"{self.apellidos} {self.nombres}"
    
    
    def __str__(self):
        return self.nombres
    
    def get_image(self):
        if self.foto:
            return self.foto.url
        else:
            return '/static/img/usuario_anonimo.png'
     # Método estático para calcular la edad del paciente
    @staticmethod
    def calcular_edad(fecha_nacimiento):
        today = date.today()  # Obtener la fecha actual
        edad = today.year - fecha_nacimiento.year  # Calcular la diferencia de años
        # Ajustar la edad si el cumpleaños de este año no ha ocurrido aún
        if (today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
            edad -= 1  # Restar un año si el cumpleaños no ha pasado
        return edad  
    
    @staticmethod
    def cantidad_pacientes():
       return Paciente.objects.all().count()
       
"""
Modelo que representa las diferentes especialidades médicas.
Cada doctor puede tener una o varias especialidades.
"""
"realizado por: gabriel hasqui"
class Especialidad(models.Model):
    # Nombre de la especialidad médica (ej. Cardiología, Neurología, etc.)
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Especialidad")
    # Descripción de la especialidad (opcional)
    descripcion = models.TextField(verbose_name="Descripción de la Especialidad", null=True, blank=True)

    activo = models.BooleanField(default=True,verbose_name="Activo")
    
    def __str__(self):
        return self.nombre

    class Meta:
        # Nombre singular y plural del modelo en la interfaz administrativa
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"

# Modelo que representa a los doctores que trabajan en la clínica.
# Almacena información personal, profesional, y detalles importantes
# como su especialidad, curriculum y datos médicos adicionales.
"realizado por: gabriel hasqui"
class Doctor(models.Model):
    # Nombre del doctor
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    # Apellido del doctor
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    # Cédula de identidad única del doctor
    cedula = models.CharField(max_length=10, unique=True, verbose_name="Cédula")
    # Fecha de nacimiento del doctor
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    # Direccion del doctor
    direccion = models.CharField(max_length=100, unique=True, verbose_name="Direccion Trabajo")
    # Latitud de la ubicación del paciente (coordenada geográfica)
    latitud = models.DecimalField(max_digits=18, decimal_places=6, verbose_name="Latitud", null=True, blank=True)
    # Longitud de la ubicación del paciente (coordenada geográfica)
    longitud = models.DecimalField(max_digits=18, decimal_places=6, verbose_name="Longitud", null=True, blank=True)
    # Código único del doctor, utilizado para identificarlo internamente en la clínica
    codigoUnicoDoctor = models.CharField(max_length=20, unique=True, verbose_name="Código Único del Doctor")
    # Relación con el modelo Especialidad, permite asociar una o varias especialidades al doctor
    especialidad = models.ManyToManyField('Especialidad', verbose_name="Especialidades",related_name="especialidades")
    # Número de teléfono de contacto del doctor
    telefonos = models.CharField(max_length=20, verbose_name="Teléfonos")
    # Dirección de correo electrónico del doctor
    email = models.EmailField(verbose_name="Correo", null=True, blank=True)
    # Hora de inicio y fin de atención del doctor
    horario_atencion = models.TextField(verbose_name="Horario de Atencion")
    # tiempo de atencion en minutos
    duracion_cita = models.IntegerField(verbose_name="Tiempo de Atencion(minutos)",default=30)
    # Curriculum vitae del doctor en formato de archivo
    curriculum = models.FileField(upload_to='curriculums/', verbose_name="Curriculum Vitae", null=True, blank=True)
    # Firma digital del doctor (imagen o archivo)
    firmaDigital = models.ImageField(upload_to='firmas/', verbose_name="Firma Digital", null=True, blank=True)
    # Fotografía del doctor
    foto = models.ImageField(upload_to='doctores/', verbose_name="Foto", null=True, blank=True)
    # Imagen que se utilizará en las recetas firmadas por el doctor
    imagen_receta = models.ImageField(upload_to='recetas/', verbose_name="Imagen para Recetas", null=True, blank=True)
    activo = models.BooleanField(default=True,verbose_name="Activo")
    
    @property
    def nombre_completo(self):
        return f"{self.apellidos} {self.nombres}"
    
    def __str__(self):
        return f"nombre "


    class Meta:
        # Nombre singular y plural del modelo en la interfaz administrativa
        verbose_name = "Doctor"
        verbose_name_plural = "Doctores"
  
# Modelo que representa los diferentes cargos que pueden tener los empleados en la clínica.
# Cada cargo puede tener un nombre y una descripción.
"realizado por: gabriel hasqui"
class Cargo(models.Model):
    # Nombre del cargo (ej. Médico, Enfermero, Administrador, etc.)
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Cargo",unique=True)
    # Descripción del cargo (opcional)
    descripcion = models.TextField(verbose_name="Descripción del Cargo", null=True, blank=True)

    activo = models.BooleanField(default=True,verbose_name="Activo")
    
    def __str__(self):
        return self.nombre

    class Meta:
        # Nombre singular y plural del modelo en la interfaz administrativa
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

# Modelo que representa a los empleados que trabajan en la clínica.
# Incluye información personal, profesional y datos de contacto.
"realizado por: gabriel hasqui"
class Empleado(models.Model):
    # Nombre del empleado
    nombres = models.CharField(max_length=100, verbose_name="Nombre del Empleado")
    # Apellido del empleado
    apellidos = models.CharField(max_length=100, verbose_name="Apellido del Empleado")
    # Cédula de identidad única del empleado
    cedula = models.CharField(max_length=10, unique=True, verbose_name="Cédula")
    # Fecha de nacimiento del empleado
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    # Relación con el modelo Cargo, permite asociar un cargo específico al empleado
    cargo = models.ForeignKey('Cargo', on_delete=models.PROTECT, verbose_name="Cargo",related_name="cargos")
    # Sueldo del empleado
    
    sueldo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sueldo")
    # Dirección de residencia del empleado
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    # Latitud para la ubicación de la residencia del empleado
    latitud = models.FloatField(verbose_name="Latitud", null=True, blank=True)
    # Longitud para la ubicación de la residencia del empleado
    longitud = models.FloatField(verbose_name="Longitud", null=True, blank=True)
    # Fotografía del empleado
    foto = models.ImageField(upload_to='empleados/', verbose_name="Foto del Empleado", null=True, blank=True)
    activo = models.BooleanField(default=True,verbose_name="Activo")
    
    @property
    def nombre_completo(self):
        return f"{self.apellidos} {self.nombres}"

    def __str__(self):
        return f"{self.apellidos}"
    
    
    class Meta:
        # Ordena los empleados alfabéticamente por apellido y nombre
        # Nombre singular y plural del modelo en la interfaz administrativa
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

# Modelo que representa los diferentes tipos de medicamentos disponibles.
# Cada tipo de medicamento puede tener un nombre y una descripción.
"realizado por: gabriel hasqui"
class TipoMedicamento(models.Model):
    # Nombre del tipo de medicamento (ej. Analgésico, Antibiótico, etc.)
    nombre = models.CharField(max_length=100, verbose_name="Tipo de Medicamento",unique=True)
    # Descripción del tipo de medicamento (opcional)
    descripcion = models.TextField(verbose_name="Descripción", null=True, blank=True)
 
    activo = models.BooleanField(default=True,verbose_name="Activo")
    
    def __str__(self):
        return self.nombre

    class Meta:
        # Nombre singular y plural del modelo en la interfaz administrativa
        verbose_name = "Tipo de Medicamento"
        verbose_name_plural = "Tipos de Medicamentos"
        
"realizado por: gabriel hasqui"
class MarcaMedicamento(models.Model):
    # Nombre del tipo de medicamento (ej. Analgésico, Antibiótico, etc.)
    nombre = models.CharField(max_length=100, verbose_name="Marca de Medicamento",unique=True)
    # Descripción del tipo de medicamento (opcional)
    descripcion = models.TextField(verbose_name="Descripción", null=True, blank=True)
 
    activo = models.BooleanField(default=True,verbose_name="Activo")
    
    def __str__(self):
        return self.nombre

    class Meta:
        # Nombre singular y plural del modelo en la interfaz administrativa
        verbose_name = "Tipo de Medicamento"
        verbose_name_plural = "Tipos de Medicamentos"
        
class ActiveMedicationManager(models.Manager):
    # Método para obtener un queryset de pacientes activos
    def get_queryset(self):
        # Retorna un queryset que solo incluye los pacientes que están activos.   
        return super().get_queryset().filter(activo=True)
                       
# Modelo que representa los medicamentos que están disponibles en la clínica.
# Incluye información sobre el nombre, tipo, y detalles adicionales del medicamento.
"realizado por: gabriel hasqui"
class Medicamento(models.Model):
    # imagen del medicamento
    imagen = models.ImageField(upload_to='medicamentos/', verbose_name="Imagen", null=True, blank=True)
    # tipo de medicamento
    tipo = models.ForeignKey('TipoMedicamento', on_delete=models.PROTECT, verbose_name="Tipo de Medicamento",related_name="tipos_medicamentos")
    # marca del medicamento
    marca_medicamento = models.ForeignKey(MarcaMedicamento, on_delete=models.PROTECT,verbose_name="Marca",related_name="marca_medicamentos",null=True,blank=True)
    # Descripción del medicamento (opcional)
    nombre = models.CharField(max_length=100,verbose_name="Nombre del Medicamento",db_index=True,unique=True)
    # Descripción del medicamento (opcional)
    descripcion = models.TextField(verbose_name="Descripción del Medicamento", null=True, blank=True)
    # concentracion del medicamento
    concentracion = models.CharField(max_length=50, verbose_name="Concentración del Medicamento", null=True, blank=True)
    # Cantidad disponible del medicamento en inventario
    cantidad = models.PositiveIntegerField(verbose_name="Stock")
    # Precio del medicamento
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    # Campo que indica si el medicamento es genérico o comercial
    comercial = models.BooleanField(default=True,
        verbose_name="Comercial"
    )
    
    activo = models.BooleanField(default=True,verbose_name="Activo")
    
    objects = models.Manager()  # Manager predeterminado
    active_medication = ActiveMedicationManager()  # Manager Personalizado
    
    def __str__(self):
        return f"{self.nombre} - ({self.tipo})"
    
    class Meta:
        # Ordena los medicamentos alfabéticamente por nombre
        ordering = ['nombre']
        # Nombre singular y plural del modelo en la interfaz administrativa
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"

# Modelo que representa los diagnósticos médicos.
# Incluye un código único, descripción y un campo adicional para información relevante.
"realizado por: gabriel hasqui"
class Diagnostico(models.Model):
    # Código único del diagnóstico (ej. CIE-10, ICD-10, etc.)
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código del Diagnóstico")
    # Descripción detallada del diagnóstico
    descripcion = models.CharField(max_length=100, verbose_name="Descripción del Diagnóstico")
    # Campo adicional para información relevante sobre el diagnóstico (opcional)
    datos_adicionales = models.TextField(verbose_name="Datos Adicionales", null=True, blank=True)

    activo = models.BooleanField(default=True,verbose_name="Activo")
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    class Meta:
        # Nombre singular y plural del modelo en la interfaz administrativa
        verbose_name = "Diagnóstico"
        verbose_name_plural = "Diagnósticos"

# modelo que alamacena todos los aciones de ingreso, actualizacion, eliminacion d elos usarios que manipulan las opciones de la aplicacion
"realizado por: gabriel hasqui"
# class AuditUser(models.Model):
#     TIPOS_ACCIONES = (
#         ('A', 'A'),   # Adicion
#         ('M', 'M'),   # Modificacion
#         ('E', 'E')    # Eliminacion
#     )
#     usuario = models.ForeignKey(User, verbose_name='Usuario',on_delete=models.PROTECT)
#     tabla = models.CharField(max_length=100, verbose_name='Tabla')
#     registroid = models.IntegerField(verbose_name='Registro Id')
#     accion = models.CharField(choices=TIPOS_ACCIONES, max_length=10, verbose_name='Accion')
#     fecha = models.DateField(verbose_name='Fecha')
#     hora = models.TimeField(verbose_name='Hora')
#     estacion = models.CharField(max_length=100, verbose_name='Estacion')

#     def __str__(self):
#         return "{} - {} [{}]".format(self.usuario.username, self.tabla, self.accion)

#     class Meta:
#         verbose_name = 'Auditoria Usuario '
#         verbose_name_plural = 'Auditorias Usuarios'
#         ordering = ('-fecha', 'hora')
        