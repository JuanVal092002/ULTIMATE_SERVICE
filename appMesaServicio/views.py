from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from appMesaServicio.models import *
from random import *
from django.db import Error, transaction
from datetime import datetime

# para correo
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import threading
from smtplib import SMTPException
from django.http import JsonResponse


# para la constraseña
import random
import string


# importar el modelo Group - Roles
from django.contrib.auth.models import Group





# Graficos estadísticos
from django.db.models import Count
import matplotlib.pyplot as plt 
import os
from django.db.models.functions import ExtractMonth



# Create your views here.


def inicio(request):
    return render(request, "frmIniciarSesion.html")


def inicioAdministrador(request):
    if request.user.is_authenticated:
        datosSesion = {"user": request.user,
                       "rol": request.user.groups.get().name}
        return render(request, "administrador/inicio.html", datosSesion)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request, "frmIniciarSesion.html", {"mensaje": mensaje})


def inicioTecnico(request):
    if request.user.is_authenticated:
        datosSesion = {"user": request.user,
                       "rol": request.user.groups.get().name}
        return render(request, "tecnico/inicio.html", datosSesion)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request, "frmIniciarSesion.html", {"mensaje": mensaje})


def inicioEmpleado(request):
    if request.user.is_authenticated:
        datosSesion = {"user": request.user,
                       "rol": request.user.groups.get().name}
        return render(request, "empleado/inicio.html", datosSesion)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request, "frmIniciarSesion.html", {"mensaje": mensaje})


def login(request):
    username = request.POST["txtUser"]
    password = request.POST["txtPassword"]
    user = authenticate(username=username, password=password)
    if user is not None:
        # registrar la variable de sesión
        auth.login(request, user)
        if user.groups.filter(name='Administrador').exists():
            return redirect('/inicioAdministrador')
        elif user.groups.filter(name='Tecnico').exists():
            return redirect('/inicioTecnico')
        else:
            return redirect('/inicioEmpleado')
    else:
        mensaje = "Usuario o Contraseña Incorrectas"
        return render(request, "frmIniciarSesion.html", {"mensaje": mensaje})


def vistaSolicitud(request):
    if request.user.is_authenticated:
        # consultar las oficinas y ambientes registrados
        oficinaAmbientes = OficinaAmbiente.objects.all()
        datosSesion = {"user": request.user,
                       "rol": request.user.groups.get().name,
                       'oficinasAmbientes': oficinaAmbientes}
        return render(request, 'empleado/solicitud.html', datosSesion)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request, "frmIniciarSesion.html", {"mensaje": mensaje})


def registrarSolicitud(request):
    
    if request.user.is_authenticated:
        try:
            with transaction.atomic():
                user = request.user
                descripcion = request.POST['txtDescripcion']
                idOficinaAmbiente = int(request.POST['cbOficinaAmbiente'])
                oficinaAmbiente = OficinaAmbiente.objects.get(
                    pk=idOficinaAmbiente)
                solicitud = Solicitud(solUsuario=user, solDescripcion=descripcion,
                                      solOficinaAmbiente=oficinaAmbiente)
                solicitud.save()
                # obtener año para en el consecutivo agregar el año.
                fecha = datetime.now()
                year = fecha.year
                # obtener el número de solicitudes hechas por año actual
                consecutivoCaso = Solicitud.objects.filter(
                    fechaHoraCreacion__year=year).count()
                # ajustar el consecutivon con ceros a las izquierda
                consecutivoCaso = str(consecutivoCaso).rjust(5, '0')
                # crear el código del caso formato REQ-AÑOVIGENCIA-CONSECUTIVO
                codigoCaso = f"REQ-{year}-{consecutivoCaso}"
                # consultar el usuario tipo Administrador para asignarlo al caso
                userCaso = User.objects.filter(
                    groups__name__in=['Administrador']).first()
                # crear el caso
                caso = Caso(casSolicitud=solicitud,
                            casCodigo=codigoCaso, casUsuario=userCaso)
                caso.save()
                # enviar el correo al empleado
                asunto = 'Registro Solicitud - Mesa de Servicio - CTPI-CAUCA'
                mensajeCorreo = f'Cordial saludo, <b>{user.first_name} {user.last_name}</b>, nos permitimos \
                    informarle que su solicitud fue registrada en nuestro sistema con el número de caso \
                    <b>{codigoCaso}</b>. <br><br> Su caso será gestionado en el menor tiempo posible, \
                    según los acuerdos de solución establecidos para la Mesa de Servicios del CTPI-CAUCA.\
                    <br><br>Lo invitamos a ingresar a nuestro sistema en la siguiente url:\
                    http://mesadeservicioctpicauca.sena.edu.co.'
                # crear el hilo para el envío del correo
                thread = threading.Thread(
                    target=enviarCorreo, args=(asunto, mensajeCorreo, [user.email]))
                # ejecutar el hilo
                thread.start()
                mensaje = "Se ha registrado su solicitud de manera exitosa"
        except Error as error:
            transaction.rollback()
            mensaje = f"{error}"

        oficinaAmbientes = OficinaAmbiente.objects.all()
        retorno = {"mensaje": mensaje, "oficinasAmbientes": oficinaAmbientes}
        return render(request, "empleado/solicitud.html", retorno)
    else:
        mensaje = "Debe primero iniciar sesión"
        return render(request, "frmIniciarSesion.html", {"mensaje": mensaje})


def enviarCorreo(asunto=None, mensaje=None, destinatario=None, archivo=None):
    remitente = settings.EMAIL_HOST_USER
    template = get_template('enviarCorreo.html')
    contenido = template.render({
        'mensaje': mensaje,
    })
    try:
        correo = EmailMultiAlternatives(
            asunto, mensaje, remitente, destinatario)
        correo.attach_alternative(contenido, 'text/html')
        if archivo != None:
            correo.attach_file(archivo)
        correo.send(fail_silently=True)
    except SMTPException as error:
        print(error)


def listarCasos(request):
    
    if request.user.is_authenticated:
        try:
            mensaje = ""
            fecha = datetime.now()
            year = fecha.year
            listaCasos = Caso.objects.filter(
                casSolicitud__fechaHoraCreacion__year=year, casEstado='Solicitada')
            tecnicos = User.objects.filter(groups__name__in=['Tecnico'])
        except Error as error:
            mensaje = str(error)
        retorno = {"listaCasos": listaCasos,
                   "tecnicos": tecnicos, "mensaje": mensaje}
        return render(request, "administrador/listarCasos.html", retorno)
    else:
        mensaje = "Debe primero iniciar sesión"
        return render(request, "frmIniciarSesion.html", {"mensaje": mensaje})


def listarEmpleadosTecnicos(request):
    if request.user.is_authenticated:
        try:
            mensaje = ""
            # consulta para obtener todos los empleados con rol Tecnico
            tecnicos = User.objects.filter(groups__name__in=['Tecnico'])
        except Error as error:
            mensaje = str(error)
        retorno = {"tecnicos": tecnicos, 'mensaje': mensaje}
        return JsonResponse(retorno)
    else:
        mensaje = "Debe primero iniciar sesión"
        return render(request, "frmIniciarSesion.html", {"mensaje": mensaje})


def asignarTecnicoCaso(request):
    if request.user.is_authenticated:
        try:
            idTecnico = int(request.POST['cbTecnico'])
            userTecnico = User.objects.get(pk=idTecnico)
            idCaso = int(request.POST['idCaso'])
            caso = Caso.objects.get(pk=idCaso)
            caso.casUsuario = userTecnico
            caso.casEstado = "En Proceso"
            caso.save()
            # enviar correo al técnico
            asunto = 'Asignación Caso - Mesa de Servicio - CTPI-CAUCA'
            mensajeCorreo = f'Cordial saludo, <b>{userTecnico.first_name} {userTecnico.last_name}</b>, nos permitimos \
                    informarle que se le ha asignado un caso para dar solución. Código de Caso:  \
                    <b>{caso.casCodigo}</b>. <br><br> Se solicita se atienda de manera oportuna \
                    según los acuerdos de solución establecidos para la Mesa de Servicios del CTPI-CAUCA.\
                    <br><br>Lo invitamos a ingresar al sistema para gestionar sus casos asignados en la siguiente url:\
                    http://mesadeservicioctpicauca.sena.edu.co.'
            # crear el hilo para el envío del correo
            thread = threading.Thread(
                target=enviarCorreo, args=(asunto, mensajeCorreo, [userTecnico.email]))
            # ejecutar el hilo
            thread.start()
            mensaje = "Caso asignado"
        except Error as error:
            mensaje = str(error)
        return redirect('/listarCasosParaAsignar/')
    else:
        mensaje = "Debe primero iniciar sesión"
        return render(request, "frmIniciarSesion.html", {"mensaje": mensaje})


def listarCasosAsignadosTecnico(request):
    if request.user.is_authenticated:
        try:
            listaCasos = Caso.objects.filter(
                casEstado='En Proceso', casUsuario=request.user)
            listaTipoProcedimiento = TipoProcedimiento.objects.all().values()
            mensaje = "Listado de casos asignados"
        except Error as error:
            mensaje = str(error)

        retorno = {"mensaje": mensaje, "listaCasos": listaCasos,
                   "listaTipoSolucion": tipoSolucion,
                   "listaTipoProcedimiento": listaTipoProcedimiento
                   }
        return render(request, "tecnico/listarCasosAsignados.html", retorno)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request, "frmIniciarSesion.html", {"mensaje": mensaje})


def solucionarCaso(request):
    if request.user.is_authenticated:
        try:
            if transaction.atomic():
                procedimiento = request.POST['txtProcedimiento']
                tipoProc = int(request.POST['cbTipoProcedimiento'])
                tipoProcedimiento = TipoProcedimiento.objects.get(pk=tipoProc)
                tipoSolucion = request.POST['cbTipoSolucion']
                idCaso = int(request.POST['idCaso'])
                caso = Caso.objects.get(pk=idCaso)
                solucionCaso = SolucionCaso(solCaso=caso,
                                            solProcedimiento=procedimiento,
                                            solTipoSolucion=tipoSolucion)
                solucionCaso.save()
                # actualizar estado de caso dependiendo del tipo de la solución
                if (tipoSolucion == "Definitiva"):
                    caso.casEstado = "Finalizada"
                    caso.save()

                # crear el obejto solucion tipo procedimiento
                solucionCasoTipoProcedimiento = SolucionCasoTipoProcedimientos(
                    solSolucionCaso=solucionCaso,
                    solTipoProcedimiento=tipoProcedimiento
                )
                solucionCasoTipoProcedimiento.save()
                # enviar correo al empleado que realizó la solicitud
                solicitud = caso.casSolicitud
                userEmpleado = solicitud.solUsuario
                asunto = 'Solucion Caso - CTPI-CAUCA'
                mensajeCorreo = f'Cordial saludo, <b>{userEmpleado.first_name} {userEmpleado.last_name}</b>, nos permitimos \
                    informarle que se ha dado solución de tipo {tipoSolucion} al caso identificado con código:  \
                    <b>{caso.casCodigo}</b>. Lo invitamos a revisar el equipo y verificar la solución. \
                    <br><br>Para consultar en detalle la solución, ingresar al sistema para verificar las solicitudes \
                    reportadas en la siguiente url: http://mesadeservicioctpicauca.sena.edu.co.'
            # crear el hilo para el envío del correo
            thread = threading.Thread(
                target=enviarCorreo, args=(asunto, mensajeCorreo, [userEmpleado.email]))
            # ejecutar el hilo
            thread.start()
            mensaje = "Solución  Caso"
        except Error as error:
            transaction.rollback()
            mensaje = str(error)
        retorno = {"mensaje": mensaje}
        return redirect("/listarCasosAsignados/")
    else:
        mensaje = "Debe iniciar sesión"
        return render(request, "frmIniciarSesion.html", {"mensaje": mensaje})


def vistaGestionarUsuarios(request):
    if request.user.is_authenticated:
        usuarios = User.objects.all()
        retorno = {"usuarios": usuarios, "user": request.user,
                   "rol": request.user.groups.get().name}
        return render(request, "administrador/vistaGestionarUsuarios.html", retorno)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request, "frmIniciarSesion.html", {"mensaje": mensaje})


def vistaRegistrarUsuario(request):
    if request.user.is_authenticated:
        roles = Group.objects.all()
        retorno = {"roles": roles, "user": request.user, 'tipoUsuario': tipoUsuario,
                   "rol": request.user.groups.get().name}
        return render(request, "administrador/frmRegistrarUsuario.html", retorno)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request, "frmIniciarSesion.html", {"mensaje": mensaje})


def registrarUsuario(request):
    if request.user.is_authenticated:
        try:
            nombres = request.POST["txtNombres"]
            apellidos = request.POST["txtApellidos"]
            correo = request.POST["txtCorreo"]
            tipo = request.POST["cbTipo"]
            foto = request.FILES.get("fileFoto")
            idRol = int(request.POST["cbRol"])
            with transaction.atomic():
                # crear un objeto de tipo User
                user = User(username=correo, first_name=nombres,
                            last_name=apellidos, email=correo, userTipo=tipo, userFoto=foto)
                user.save()
                # obtener el Rol de acuerdo a id del rol
                rol = Group.objects.get(pk=idRol)
                # agregar el usuario a ese Rol
                user.groups.add(rol)
                # si rol es Administrador se habilita para que tenga acceso al sitio web del administrador
                if (rol.name == "Administrador"):
                    user.is_staff = True
                # guardamos el usuario con lo que tenemos
                user.save()
                # llamamos a la funcion generarPassword
                passwordGenerado = generarPassword()
                print(f"password {passwordGenerado}")
                # con el usuario creado llamamos a la función set_password que
                # encripta el password y lo agrega al campo password del user.
                user.set_password(passwordGenerado)
                # se actualiza el user
                user.save()
                mensaje = "Usuario Agregado Correctamente"
                retorno = {"mensaje": mensaje}
                # enviar correo al usuario
                asunto = 'Registro Sistema Mesa de Servicio CTPI-CAUCA'
                mensaje = f'Cordial saludo, <b>{user.first_name} {user.last_name}</b>, nos permitimos \
                    informarle que usted ha sido registrado en el Sistema de Mesa de Servicio \
                    del Centro de Teleinformática y Producción Industrial CTPI de la ciudad de Popayán, \
                    con el Rol: <b>{rol.name}</b>. \
                    <br>Nos permitimos enviarle las credenciales de Ingreso a nuestro sistema.<br>\
                    <br><b>Username: </b> {user.username}\
                    <br><b>Password: </b> {passwordGenerado}\
                    <br><br>Lo invitamos a utilizar el aplicativo, donde podrá usted \
                    realizar solicitudes a la mesa de servicio del Centro. Url del aplicativo: \
                    http://mesadeservicioctpi.sena.edu.co.'
                thread = threading.Thread(
                    target=enviarCorreo, args=(asunto, mensaje, [user.email]))
                thread.start()
                return redirect("/vistaGestionarUsuarios/", retorno)
        except Error as error:
            transaction.rollback()
            mensaje = f"{error}"
        retorno = {"mensaje": mensaje}
        return render(request, "administrador/frmRegistrarUsuario.html", retorno)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request, "frmIniciarSesion.html", {"mensaje": mensaje})


def generarPassword():
    """
    Genera un password de longitud de 10 que incluye letras mayusculas
    y minusculas,digitos y cararcteres especiales
    Returns:
        _str_: retorna un password
    """
    longitud = 10

    caracteres = string.ascii_lowercase + \
        string.ascii_uppercase + string.digits + string.punctuation
    password = ''

    for i in range(longitud):
        password += ''.join(random.choice(caracteres))
    return password


def recuperarClave(request):
    try:
        correo = request.POST['txtCorreo']
        user = User.objects.filter(email=correo).first()
        if (user):
            passwordGenerado = generarPassword()
            user.set_password(passwordGenerado)
            user.save()
            mensaje = "Contraseña Actualiza Correctamente y enviada al Correo Electrónico"
            retorno = {"mensaje": mensaje}
            # enviar correo al usuario
            asunto = 'Recuperación de Contraseña Sistema Mesa de Servicio CTPI-CAUCA'
            mensaje = f'Cordial saludo, <b>{user.first_name} {user.last_name}</b>, nos permitimos \
                    informarle que se ha generado nueva contraseña para ingreso al sistema. \
                    <br><b>Username: </b> {user.username}\
                    <br><b>Password: </b> {passwordGenerado}\
                    <br><br>Para comprobar ingresar al sistema haciendo uso de la nueva contraseña.'
            thread = threading.Thread(
                target=enviarCorreo, args=(asunto, mensaje, [user.email]))
            thread.start()
        else:
            mensaje = "No existe usuario con correo ingresado. Revisar"
            retorno = {"mensaje": mensaje}
    except Error as error:
        mensaje = str(error)

    return render(request, 'frmIniciarSesion.html', retorno)





def generarGraficaPorMes(request):
    try:
        solicitudes = Solicitud.objects.annotate(month=ExtractMonth('fechaHoraCreacion'))\
            .values('month')\
            .annotate(cantidad=Count('id'))\
            .values('month', 'cantidad')
        print(solicitudes)

        meses_numeros = []
        cantidades = []

        for s in solicitudes:
            meses_numeros.append(s['month'])
            cantidades.append(s['cantidad'])

        # Lista de nombres de meses
        nombres_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

        meses = [nombres_meses[numero - 1] for numero in meses_numeros]

        plt.figure(figsize=(10, 5))
        plt.title("Cantidad de Solicitudes por Mes")
        plt.xlabel("Mes")
        plt.ylabel("Cantidad")

        plt.bar(meses, cantidades)

        # Configurar el eje y para mostrar solo enteros únicos
        max_valor_y = max(cantidades)  # Obtener el máximo valor en el eje y
        plt.yticks(range(0, max_valor_y + 1))  # Establecer los ticks del eje y de 0 a max_valor_y

        rutaImagen = os.path.join(settings.MEDIA_ROOT, "graficaSolicitudesPorMeses.png")
        plt.savefig(rutaImagen)

        return render(request, "administrador/graficaSolPorMes.html")

    except Exception as error:
        mensaje = f"{error}"
        return render(request, "administrador/graficaSolPorMes.html", {"error": mensaje})
    



def generarGraficaPorOficina(request):
    try:
        # Obtener las solicitudes agrupadas por oficina
        solicitudes = Solicitud.objects.values('solOficinaAmbiente__ofiNombre')\
            .annotate(cantidad=Count('id'))
        
        print(solicitudes)

        oficinas = []
        cantidades = []

        for s in solicitudes:
            print(s)
            oficinas.append(s['solOficinaAmbiente__ofiNombre'])
            cantidades.append(s['cantidad'])

        # Generar una paleta de colores única para cada oficina
        #colores = plt.cm.get_cmap('tab20', len(oficinas))  # Usar una paleta de colores tab20

        plt.figure(figsize=(8, 8))
        plt.title("Cantidad de Solicitudes por Ambiente u Oficina")      

        # Graficar la gráfica de pastel con colores diferentes para cada oficina
        plt.pie(cantidades, labels=oficinas, autopct='%1.1f%%', startangle=140)

        rutaImagen = os.path.join(settings.MEDIA_ROOT ,"graficaOficinaAmbiente.png")
        #plt.tight_layout()
        plt.savefig(rutaImagen)
        plt.close()

        return render(request, "administrador/graficaSolPorOficina.html")

    except Exception as error:
        mensaje = f"{error}"
        return render(request, "administrador/graficaSolPorOficina.html", {"error": mensaje}) 





def generarPdfSolicitudes(request):
    from appMesaServicio.pdfSolicitudes import PdF
    solicitudes= Solicitud.objects.all()
    
    # creado en el archivo pdfSolicitudes.py
    doc= PdF()
    # Permite colocar el numero de paginas en el pdf
    doc.alias_nb_pages()
    # Permite agregar nuevas paginas
    doc.add_page()
    
    # se pasan las solicitudes como argumento
    doc.mostrarDatos(solicitudes)
    
    # generar el archivo Pdf en la carpeta media
    doc.output(f'media/solicitudes.pdf')
    
    return render(request, "administrador/mostrarPdf.html")
    


def salir(request):
    auth.logout(request)
    return render(request, "frmIniciarSesion.html",
                  {"mensaje": "Ha cerrado la sesión"})