from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_protect
import logging
from django.contrib.auth import logout
from django.http import JsonResponse
from django.utils.timezone import now


# Create your views here.
class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'  # Asegúrate de tener la ruta correcta al archivo HTML de inicio de sesión
    
def logout_view(request):
    logout(request)
    # Redirige a la página de inicio o a cualquier otra página después de cerrar sesión
    return redirect('login')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = authenticate(
                request, 
                username=form.cleaned_data['username'], 
                password=form.cleaned_data['password']
            )

            if usuario is not None:
                auth_login(request, usuario)
                messages.success(request, 'Inicio de sesión exitoso.')

                # Si existe un parámetro 'next' en la URL, redirige allí
                next_url = request.POST.get('next') or request.GET.get('next')
                return redirect(next_url or 'dashboard')
            else:
                messages.error(request, 'Credenciales incorrectas. Inténtalo de nuevo.')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

@login_required

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST, request.FILES)  # Agrega request.FILES aquí
        if form.is_valid():
            # Accede a la contraseña desde el formulario
            password = form.cleaned_data['contraseña']

            # Crea una instancia del usuario y establece la contraseña
            usuario = form.save(commit=False)
            usuario.password = make_password(password)
            usuario.save()

            return redirect('dashboard')  
    else:
        form = RegistroUsuarioForm()

    return render(request, 'registration/registro_usuario.html', {'form': form})

def dashboard(request):
    if request.user.is_authenticated:
        usuario = request.user

        total_empleados = Empleado.objects.count()
        asistencias_hoy = Asistencia.objects.filter(fecha=now().date()).count()
        vacaciones_pendientes = Vacacion.objects.filter(aprobada=False).count()
        entrevistas_programadas = Entrevista.objects.filter(fecha_programada__gte=now().date()).count()
        solicitudes_pendientes = Permiso.objects.filter(aprobado=False).count()

        context = {
            'usuario': usuario,
            'total_empleados': total_empleados,
            'asistencias_hoy': asistencias_hoy,
            'vacaciones_pendientes': vacaciones_pendientes,
            'entrevistas_programadas': entrevistas_programadas,
            'solicitudes_pendientes': solicitudes_pendientes,
        }

        return render(request, 'dashboard/dashboard.html', context)
    else:
        return redirect('index')


def error_permisos(request):
    return render(request, 'dashboard/error_permisos.html')

def registrar_empleado(request):
    if request.user.is_authenticated:
        if request.user.cargo == 'Recursos humanos' or request.user.usuario_administrador:
            usuario = request.user
            empleados = Empleado.objects.all()

            # Filtrar empleados según los parámetros de la consulta GET
            if request.method == 'GET':
                nombres = request.GET.get('nombres')
                apellidos = request.GET.get('apellidos')
                cargo = request.GET.get('cargo')
                documento_identidad = request.GET.get('documento_identidad')
                tipo_contrato = request.GET.get('tipo_contrato')
                numero_interno = request.GET.get('numero_interno')

                # Aplicar filtros según los campos ingresados
                if nombres:
                    empleados = empleados.filter(nombres__icontains=nombres)
                if apellidos:
                    empleados = empleados.filter(apellidos__icontains=apellidos)
                if cargo:
                    empleados = empleados.filter(cargo__icontains=cargo)
                if documento_identidad:
                    empleados = empleados.filter(documento_identidad=documento_identidad)
                if tipo_contrato:
                    empleados = empleados.filter(tipo_contrato__icontains=tipo_contrato)
                if numero_interno:
                    empleados = empleados.filter(numero_interno=numero_interno)
                    
            # Manejar la limpieza del filtro
            if request.method == 'GET' and 'limpiar' in request.GET:
                   empleados = Empleado.objects.all()  # Reiniciar el filtro

            return render(request, 'recursos_humanos/registro_empleados.html', {'usuario': usuario, 'empleados': empleados})     
        else:
            return error_permisos(request)
    else:
        return redirect('index')




def obtener_empleado(request, empleado_id):
    try:
        # Obtener el empleado por su ID
        empleado = Empleado.objects.get(pk=empleado_id)
        
        # Devolver los datos del empleado en formato JSON con el nombre 'empleado'
        return JsonResponse({
            'foto' : empleado.foto.url,
            'nombres': empleado.nombres,
            'apellidos': empleado.apellidos,
            'numero_interno': empleado.numero_interno,
            'fecha_nacimiento': empleado.fecha_nacimiento,
            'documento_identidad': empleado.documento_identidad,
            'domicilio': empleado.domicilio,
            'correo': empleado.correo,
            'telefono': empleado.telefono,
            'EPS': empleado.EPS,
            'estado_civil': empleado.estado_civil,
            'dependientes_economicos': empleado.dependientes_economicos,
            'cargo': empleado.cargo,
            'tipo_contrato': empleado.tipo_contrato,
            'talla_ropa': empleado.talla_ropa,
            'talla_calzado': empleado.talla_calzado,
            'formacion_reglada': empleado.formacion_reglada,
            'formacion_complementaria': empleado.formacion_complementaria,
            'institucion_graduacion': empleado.institucion_graduacion,
            'experiencias_previas': empleado.experiencias_previas,
            'relacion_empleado': empleado.relacion_empleado,
            'contacto_nombres': empleado.contacto_nombres,
            'contacto_apellidos': empleado.contacto_apellidos,
            'contacto_fecha_nacimiento': empleado.contacto_fecha_nacimiento,
            'contacto_carnet_identidad': empleado.contacto_carnet_identidad,
            'contacto_domicilio': empleado.contacto_domicilio,
            'contacto_telefono': empleado.contacto_telefono,
            'contacto_correo': empleado.contacto_correo,
            'banco': empleado.banco,
            'tipo_cuenta': empleado.tipo_cuenta,
            'numero_cuenta': empleado.numero_cuenta,
            # Agrega los demás campos del empleado aquí...
        })
    except Empleado.DoesNotExist:
        # Manejar el caso en que el empleado no exista
        return JsonResponse({'error': 'Empleado no encontrado'}, status=404)
    except Exception as e:
        # Manejar cualquier otro error que pueda ocurrir
        return JsonResponse({'error': str(e)}, status=500)

logger = logging.getLogger(__name__)

def crear_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado registrado correctamente.')
            return redirect('crear_empleado')
        else:
            logger.error("El formulario no es válido. Errores: %s", form.errors)
    else:
        form = EmpleadoForm()
    usuario = request.user
    return render(request, 'recursos_humanos/crear_empleado.html', {'form': form, 'usuario': usuario})

def user_information(request):
    # Obtener los datos del usuario (puedes reemplazar estos datos con los del usuario actual)
    usuarios = Usuario.objects.all()
    usuario = request.user

    return render(request, 'registration/user_information.html', {'usuario': usuario} )

@csrf_protect
def guardar_cambios_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_information')
    else:
        form = UsuarioForm(instance=request.user)
    return render(request, 'registration/user_information.html', {'form': form})

def empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'dashboard/empleados.html', {'empleados': empleados})

def registrar_asistencia(request):
    # Aquí podrías agregar la lógica de registro si es un formulario
    asistencias = Asistencia.objects.all()
    return render(request, 'dashboard/registrar_asistencia.html', {'asistencias': asistencias})

def solicitudes(request):
    permisos = Permiso.objects.all()
    return render(request, 'dashboard/solicitudes.html', {'permisos': permisos})

def calendario(request):
    entrevistas = Entrevista.objects.all()
    return render(request, 'dashboard/calendario.html', {'entrevistas': entrevistas})

def ejemplo(request):
    if request.user.is_authenticated:
        usuario = request.user

        total_empleados = Empleado.objects.count()
        asistencias_hoy = Asistencia.objects.filter(fecha=now().date()).count()
        vacaciones_pendientes = Vacacion.objects.filter(aprobada=False).count()
        entrevistas_programadas = Entrevista.objects.filter(fecha_programada__gte=now().date()).count()
        solicitudes_pendientes = Permiso.objects.filter(aprobado=False).count()

        context = {
            'usuario': usuario,
            'total_empleados': total_empleados,
            'asistencias_hoy': asistencias_hoy,
            'vacaciones_pendientes': vacaciones_pendientes,
            'entrevistas_programadas': entrevistas_programadas,
            'solicitudes_pendientes': solicitudes_pendientes,
        }

        return render(request, 'dashboard/ejemplo.html', context)
    else:
        return redirect('index')