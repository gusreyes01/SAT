# -*- coding: utf-8 -*
# Create your views here.
import os
from datetime import date
from io import BytesIO
from app.forms import *
from app.librerias.muestra import crear_muestra
from app.librerias.horario import convierte_de_horario, obtener_horario_de_forma
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.utils import timezone
from django.db import transaction
from random import sample, shuffle, randint
from app.cartas_notificacion import *
from django.utils import simplejson
from django.db.models import Max
from django.db.models import Sum, Count, Q
from django.http import HttpResponseRedirect
import datetime
import math
from django.db import transaction

# For debugging.
import pdb

# Variable para verificar el estado en el que se encuentra la importación del csv
estado_importacion = ""

# @login_required
# def home(request):
#     return render_to_response('home/home.html', context_instance=RequestContext(request))
    
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
          login(request, user)
          # Redirect to a success page.
        else:
          HttpResponse('')# Return a 'disabled account' error message
    else:
        # Return an 'invalid login' error message.
         HttpResponse('')
        
#   Vista para cerrar sesion
@login_required    
def logout_view(request):
    logout(request)
    response = redirect('/login/')
    return response
 

@login_required
def perfil_estudiante(request,id):
    #estudiante = Estudiante.objects.get(pk = id) 
    #itemset_queryset = EstudianteResultado.objects.filter(estudiante_id=id).values_list('antidoping_id', flat=True)
    #resultados = EstudianteResultado.objects.filter(estudiante_id=id).select_related()
    inscrito = Inscrito.objects.filter(estudiante=id)
    resultados = EstudianteMuestra.objects.filter(inscrito__in=inscrito)
    estudiante = Estudiante.objects.get(matricula=id)


    #antidopings = Antidoping.objects.filter(id__in=itemset_queryset)   
    return render_to_response('home/estudiante/perfil_estudiante.html',{'estudiante': estudiante,'resultados': resultados}, context_instance=RequestContext(request))    
        
@login_required
def edita_estudiante(request,id):
    estudiante = Estudiante.objects.get(pk = id)
    if request.method == 'POST':
      forma = AltaEstudiante(request.POST, instance=estudiante)
      forma.helper.form_action = reverse('perfil_estudiante', args=[id])
      if forma.is_valid():
        forma.save()
        return redirect('/estudiante/')  
    else:
      forma = AltaEstudiante(instance=estudiante)
    return render_to_response('home/estudiante/edita_estudiante.html', {'forma': forma}, context_instance=RequestContext(request))    

@login_required
def evaluar_estudiante(request,id):
    estudiante_muestra = EstudianteMuestra.objects.get(pk = id)
    if request.method == 'POST':
      forma = EvaluaEstudiante(request.POST, instance=estudiante_muestra)
      if forma.is_valid():
        estudiante_muestra = forma.save(commit=False)
        # estudiante_muestra.tipo_droga = forma.cleaned_data['tipo_droga']
        # estudiante_muestra.tipo_droga = ','.join(estudiante_muestra.tipo_droga)
        # if estudiante_muestra.estado > estudiante_muestra.antidoping.estado_antidoping:
        #   estudiante_muestra.antidoping.estado_antidoping = estudiante_muestra.estado 
        #   estudiante_muestra.antidoping.save()
        estudiante_muestra.save()
        return redirect('/perfil_muestra/' + str(estudiante_muestra.antidoping_id))  
    else:
      forma = EvaluaEstudiante(instance=estudiante_muestra)
    return render_to_response('home/estudiante/evaluar_estudiante.html', {'forma': forma}, context_instance=RequestContext(request))    
   
@login_required
def estudiante(request):
  if request.method=='POST':
      busqueda = request.POST.get('q1', '')
      if busqueda:
          results = Estudiante.objects.filter(matricula__contains=busqueda) # busqueda por matricula
          if len(results) < 1:
            results = Estudiante.objects.filter(correo__contains=busqueda) # busqueda por correo
          if len(results) < 1:
            results = Estudiante.objects.filter(nombre__contains=busqueda) # busqueda por nombre
          if len(results) < 1:
            results = Estudiante.objects.filter(apellido__contains=busqueda) # busqueda por apellido
          if len(results) < 1:
            tmp = EstudianteMuestra.objects.filter(folio__contains=busqueda) # busqueda por folio
            results = map(lambda estudiantemuestra: estudiantemuestra.inscrito.estudiante, tmp)

          data = {'results': results,}
      else:
        data = {'results': []}

      return render_to_response( 'home/estudiante/estudiante.html', data,context_instance = RequestContext( request ) )
  
  else:
    estudiantes = Estudiante.objects.all()[:100]  
    return render_to_response('home/estudiante/estudiante.html',{'estudiantes': estudiantes}, context_instance=RequestContext(request))    
    
@login_required
def alta_estudiante(request):
    if request.method == 'POST':
      # La forma ligada a los datos enviados en el POST
      forma = AltaEstudiante(request.POST)      
      #forma2 = SeleccionMuestra(request.POST)     
      # Todas las reglas de validacion aprobadas
      if forma.is_valid():
        forma.save()
        return redirect('/') # Redirect after POST
    else:
        forma = AltaEstudiante() # An unbound form
        #forma2 = SeleccionMuestra() # An unbound form
    return render_to_response('home/estudiante/alta_estudiante.html', { 'forma': forma} , context_instance=RequestContext(request))    
    
@login_required
def muestra(request):
   
    # Borrar antidopings mal inicializados.
    borrar_antidopings()

    antidopings = Antidoping.objects.exclude(estado_antidoping=None).order_by('-antidoping_inicio')
    for antidoping in antidopings:
      tmp = EstudianteMuestra.objects.filter(antidoping=antidoping.pk).aggregate(Max('estado'))
      antidoping.estado_antidoping = tmp['estado__max'] # Sacar el atributo y guardarlo.
      antidoping.save()
    return render_to_response('home/muestra/muestra.html',{'antidopings': antidopings}, context_instance=RequestContext(request))

@login_required
def success(request):
    return render_to_response('home/success.html', context_instance=RequestContext(request))    

def borrar_antidopings():
  antidoping_a_borrar = Antidoping.objects.filter(estado_antidoping=None)
  for borrar in antidoping_a_borrar:
    borrar_estudiante_muestra(borrar.pk)
  antidoping_a_borrar.delete()

def borrar_estudiante_muestra(id):
   antidoping_borrar = Antidoping.objects.get(pk=int(id))   # Obtener el antidoping a borrar.
   antidoping_borrar.estudiantemuestra_set.all().delete()   # Borrar los alumnos de la muestra relacionados a él.
   antidoping_borrar.delete()                               # Borrar el antidoping.

@login_required
def eliminar_muestra(request,id):
   borrar_estudiante_muestra(id)

   return redirect('/muestra/')

@login_required
def perfil_muestra(request,id):
   antidoping = Antidoping.objects.get(pk=id)
   alumnos = map(lambda x: x.inscrito.estudiante, antidoping.estudiantemuestra_set.all())
   grupos = map(lambda x: x.inscrito.grupo, antidoping.estudiantemuestra_set.all())   

   alumnos_matricula = map(lambda x: x.matricula, alumnos)
   estudiante_resultado = antidoping.estudiantemuestra_set.all()
   alumnos = zip(alumnos, estudiante_resultado)
   #muestra_seleccionados = Inscrito.objects.filter(estudiante_id__in=alumnos_seleccionados, grupo__in=total_grupos)

   grupos = list(set(grupos))

   return render_to_response('home/muestra/perfil_muestra.html',{'alumnos': alumnos,'estudiante_resultado':estudiante_resultado,'grupos': grupos,'antidoping': antidoping}, context_instance=RequestContext(request))    
   
@login_required
def seleccion_muestra(request):
    if request.method == 'POST':
      # La forma ligada a los datos enviados en el POST
      forma = CrearAntidoping(request.POST)      

      # Todas las reglas de validacion aprobadas
      if forma.is_valid():

        nuevo_antidoping = forma.save(commit=False)
        # nuevo_antidoping.antidoping_inicio = timezone.now()

        alumnos_seleccionados = forma.cleaned_data['seleccion_alumnos'].split(',')
        alumnos_seleccionados = filter (lambda item: item != '', alumnos_seleccionados)
        alumnos_seleccionados = map(int, alumnos_seleccionados)   # Convirtiendo lista de strings a int.

        grupos_seleccionados = forma.cleaned_data['seleccion_grupos'].split(',')
        grupos_seleccionados = filter (lambda item: item != '', grupos_seleccionados)
        grupos_seleccionados = map(int, grupos_seleccionados)     # Convirtiendo lista de strings a int.

        tamano_muestra = int(forma.cleaned_data['tamano_muestra'])
        dia = forma.cleaned_data['dia']
        inicio = forma.cleaned_data['inicio']
        fin = forma.cleaned_data['fin']
        muestra_seleccionados = []
        muestra_grupos = []
        muestra_aleatorios = []
        respuesta = {}
        meses = {
          '1': 1,
          '2': 1,
          '3': 1,
          '4': 1,
          '5': 1,
          '6': 2,
          '7': 2,
          '8': 3,
          '9': 3,
          '10': 3,
          '11': 3,
          '12': 3,
        }


        delimitador = '|'

        print "dia..", dia
        print "antidoping id..",nuevo_antidoping.pk 
        print "dia de antidoping",dia
        print "hora inicio",inicio
        print "hora fin",fin
        print alumnos_seleccionados, grupos_seleccionados
        print "Rango horas: ", obtener_horario_de_forma(inicio, fin)

        ## Obtener anio y semestre actual para filtar la muestra.
        time = timezone.now() # obtener la fecha actual
        anio = int(time.year)
        mes = str(time.month)
        semestre = meses[mes]
        try:
          # Verificar la cantidad de la muestra con los alumnos especificados.
          if len(alumnos_seleccionados) > tamano_muestra or tamano_muestra < 3:
            raise Exception("Cantidad de alumnos inconsistente")

          grupos_seleccionados_filtrados = Grupo.objects.filter(pk__in=grupos_seleccionados)

          # Modificar si se necesita null.
          if dia == 'lunes':
            semestre = Grupo.objects.filter(anio=anio, semestre=semestre)
            grupos = semestre.exclude(horario_1='None')
            # Revisar que se encuentre los grupos dentro del horario deseado.
            for gpo in grupos:
              horario_gpo = convierte_de_horario(gpo.horario_1, delimitador)
              horario_atdp = obtener_horario_de_forma(inicio, fin)
              if horario_gpo['hora_inicio'] >= horario_atdp['hora_inicio'] and horario_gpo['hora_fin'] <= horario_atdp['hora_fin']:
                muestra_grupos = muestra_grupos + [gpo]       # Guardar el grupo en una lista.
            grupos_seleccionados_filtrados = grupos_seleccionados_filtrados.exclude(horario_1='None')
       
          elif dia == 'martes':
            semestre = Grupo.objects.filter(anio=anio, semestre=semestre)
            grupos = semestre.exclude(horario_2='None')
            # Revisar que se encuentre los grupos dentro del horario deseado.
            for gpo in grupos:
              horario_gpo = convierte_de_horario(gpo.horario_2, delimitador)
              horario_atdp = obtener_horario_de_forma(inicio, fin)
              if horario_gpo['hora_inicio'] >= horario_atdp['hora_inicio'] and horario_gpo['hora_fin'] <= horario_atdp['hora_fin']:
                muestra_grupos = muestra_grupos + [gpo]       # Guardar el grupo en una lista.
            grupos_seleccionados_filtrados = grupos_seleccionados_filtrados.exclude(horario_2='None')

          elif dia == 'miercoles':
            semestre = Grupo.objects.filter(anio=anio, semestre=semestre)
            grupos = semestre.exclude(horario_3='None')
            # Revisar que se encuentre los grupos dentro del horario deseado.
            for gpo in grupos:
              horario_gpo = convierte_de_horario(gpo.horario_3, delimitador)
              horario_atdp = obtener_horario_de_forma(inicio, fin)
              if horario_gpo['hora_inicio'] >= horario_atdp['hora_inicio'] and horario_gpo['hora_fin'] <= horario_atdp['hora_fin']:
                muestra_grupos = muestra_grupos + [gpo]       # Guardar el grupo en una lista.
            grupos_seleccionados_filtrados = grupos_seleccionados_filtrados.exclude(horario_3='None')

          elif dia == 'jueves':
            semestre = Grupo.objects.filter(anio=anio, semestre=semestre)
            grupos = semestre.exclude(horario_4='None')
            # Revisar que se encuentre los grupos dentro del horario deseado.
            for gpo in grupos:
              horario_gpo = convierte_de_horario(gpo.horario_4, delimitador)
              horario_atdp = obtener_horario_de_forma(inicio, fin)
              if horario_gpo['hora_inicio'] >= horario_atdp['hora_inicio'] and horario_gpo['hora_fin'] <= horario_atdp['hora_fin']:
                muestra_grupos = muestra_grupos + [gpo]       # Guardar el grupo en una lista.
            grupos_seleccionados_filtrados = grupos_seleccionados_filtrados.exclude(horario_4='None')

          elif dia == 'viernes':
            semestre = Grupo.objects.filter(anio=anio, semestre=semestre)
            grupos = semestre.exclude(horario_5='None')
            # Revisar que se encuentre los grupos dentro del horario deseado.
            for gpo in grupos:
              horario_gpo = convierte_de_horario(gpo.horario_5, delimitador)
              horario_atdp = obtener_horario_de_forma(inicio, fin)
              if horario_gpo['hora_inicio'] >= horario_atdp['hora_inicio'] and horario_gpo['hora_fin'] <= horario_atdp['hora_fin']:
                muestra_grupos = muestra_grupos + [gpo]       # Guardar el grupo en una lista.
            grupos_seleccionados_filtrados = grupos_seleccionados_filtrados.exclude(horario_5='None')

          elif dia == 'sabado':
            semestre = Grupo.objects.filter(anio=anio, semestre=semestre)
            grupos = semestre.exclude(horario_6='None')
            # Revisar que se encuentre los grupos dentro del horario deseado.
            for gpo in grupos:
              horario_gpo = convierte_de_horario(gpo.horario_6, delimitador)
              horario_atdp = obtener_horario_de_forma(inicio, fin)
              if horario_gpo['hora_inicio'] >= horario_atdp['hora_inicio'] and horario_gpo['hora_fin'] <= horario_atdp['hora_fin']:
                muestra_grupos = muestra_grupos + [gpo]       # Guardar el grupo en una lista.
            grupos_seleccionados_filtrados = grupos_seleccionados_filtrados.exclude(horario_6='None')

          
          # obtener alumnos que fueron senalados y que se pueden encontrar en los grupos seleccionados.        
          total_grupos = muestra_grupos + list(grupos_seleccionados_filtrados)
          total_grupos = list(set(total_grupos))
          # for gpo in total_grupos:
          #   print gpo.crn

          for estudiante in alumnos_seleccionados:
            tmp = Inscrito.objects.filter(estudiante_id=estudiante, grupo__in=total_grupos)
            if tmp:
              muestra_seleccionados = muestra_seleccionados + [tmp[0]]        # Trick to merge querysets with the first student appearance n any of the groups.
              print tmp[0].grupo_id

          grupos_repetidos = []
          # Protegemos la identidad del alumno seleccionado agregando otros alumnos.
          for inscrito in muestra_seleccionados:
            muestra_aleatorios = muestra_aleatorios + sample(Inscrito.objects.filter(grupo=inscrito.grupo), randint(2,4))
            grupos_repetidos = grupos_repetidos + [inscrito.grupo_id]
            print inscrito.grupo
            # muestra_grupos = filter(lambda gpo: gpo != inscrito.grupo, muestra_grupos)  # Eliminar de la seleccion.
         
          grupos_seleccionados_filtrados = grupos_seleccionados_filtrados.exclude(crn__in=grupos_repetidos)

         # obtener alumnos que pertenecen a los grupos senalados.
          for gpo_seleccionado in grupos_seleccionados_filtrados:
            elegir_inscritos = Inscrito.objects.filter(grupo_id=gpo_seleccionado)
            muestra_aleatorios = muestra_aleatorios + sample(elegir_inscritos, randint(3,5))

          # Barajear a los grupos, para asegurar que el proceso sea aleatorio.
          shuffle(muestra_grupos)
          cantidad_alumnos_seleccionados = len(muestra_seleccionados)
          cantidad_alumnos_aleatorios = len(muestra_aleatorios)
          cantidad_total_muestra = cantidad_alumnos_aleatorios + cantidad_alumnos_seleccionados

          print cantidad_alumnos_aleatorios,cantidad_alumnos_seleccionados
          # Escoger alumnos aleatoriamente hasta que se cumpla el tamano de la muestra.
          elementos_restantes = tamano_muestra - cantidad_total_muestra

          for gpo in muestra_grupos:
            # print "er:", elementos_restantes
            if(elementos_restantes >= 3 and elementos_restantes <= 5):
              tmp = sample(Inscrito.objects.filter(grupo=gpo), elementos_restantes)
              cantidad_tmp = elementos_restantes
              muestra_aleatorios = muestra_aleatorios + tmp
            elif(elementos_restantes < 3):
              break
            else:
              tmp = sample(Inscrito.objects.filter(grupo=gpo), randint(3,5))
              cantidad_tmp = len(tmp)
              muestra_aleatorios = muestra_aleatorios + tmp

            elementos_restantes = elementos_restantes - cantidad_tmp

          cantidad_alumnos_aleatorios = len(muestra_aleatorios)
          cantidad_total_muestra = cantidad_alumnos_aleatorios + cantidad_alumnos_seleccionados

          # Guardar antidoping.
          nuevo_antidoping.nombre = forma.cleaned_data['nombre']
          nuevo_antidoping.dia = dia
          nuevo_antidoping.muestra_inicio = inicio
          nuevo_antidoping.muestra_fin = fin
          nuevo_antidoping.antidoping_inicio = timezone.now()
          nuevo_antidoping.tamano_muestra = cantidad_total_muestra
          nuevo_antidoping.estado_antidoping = 0
          nuevo_antidoping.notas = forma.cleaned_data['notas']
          nuevo_antidoping.save()

          # Guardar las personas de la muestra.
          for inscrito in list(muestra_seleccionados):
            tmp = EstudianteMuestra(inscrito=inscrito, antidoping=nuevo_antidoping, tipo_seleccion=1)
            tmp.save()

          for inscrito in list(muestra_aleatorios):
            tmp = EstudianteMuestra(inscrito=inscrito, antidoping=nuevo_antidoping, tipo_seleccion=0)
            tmp.save()

          respuesta = {
              # Se pueden eliminar parametros mandando el objeto antidoping,
              # borrar este comentario cuando se haga.
              'antidoping_id': nuevo_antidoping.pk,
              'muestra': muestra_aleatorios, 
              'muestra_seleccionados': muestra_seleccionados, 
              'cantidad_total_muestra': cantidad_total_muestra,
              'cantidad_total_seleccionados': cantidad_alumnos_seleccionados,
              'dia': dia, 
              'inicio': inicio, 
              'fin': fin, 
              'verificar': True,
              'error': False
            }

        except Exception as e:
          print '%s (%s)' % (e.message, type(e))
          respuesta = {
              'error': True
            }

        return render_to_response('home/verificar_muestra.html',
          respuesta, context_instance=RequestContext(request))

  
    else:
        forma = CrearAntidoping() # An unbound form
        #forma2 = SeleccionMuestra() # An unbound form
    return render_to_response('home/muestra/seleccion_muestra.html', { 'forma': forma} , context_instance=RequestContext(request))
    
@login_required
def alta_muestra(request):
  if request.method == 'POST':
    lista_a_borrar = map(int, request.POST.getlist('eliminar-de-muestra'))
    antidoping_id = int(request.POST.get('antidoping_id', ''))
    elementos_a_borrar = EstudianteMuestra.objects.filter(inscrito_id__in=lista_a_borrar, antidoping_id=antidoping_id)
    
    # Generar folios y guardar estado del alumno.
    muestra_antidoping = EstudianteMuestra.objects.filter(antidoping_id=antidoping_id)
    now = date.today()
    now = str(now).replace('-','')
    lista_de_numeros_aleatorios = range(0, 1000000)
    shuffle(lista_de_numeros_aleatorios)
    contador = 0
    for estudiantemuestra in muestra_antidoping:
      appendix = lista_de_numeros_aleatorios[contador]
      estudiantemuestra.folio = "e%s%d" %(now,appendix) # Falta verificar de que no existe un folio igual.
      estudiantemuestra.estado = 0
      estudiantemuestra.resultado = 0
      estudiantemuestra.save()
      contador = contador + 1     

    if len(elementos_a_borrar) > 0:
      antidoping_tmp = elementos_a_borrar[0].antidoping
      antidoping_tmp.save()
      
    elementos_a_borrar.delete()

    redireccion = '/'
    return redirect(redireccion)  # Redirect after POST
  else:
    # return render_to_response('home/home.html', context_instance=RequestContext(request))
    return home(request)

@login_required
def success(request):
    return render_to_response('home/success_muestra.html', context_instance=RequestContext(request))

@login_required
def obtener_carta(request, id_antidoping, notificacion):
    
    # params = "1-1"
    # params_split = params.split("-")

    notificacion = int(notificacion)
    id_antidoping = int(id_antidoping)
    # print notificacion
    # id_antidoping = int(params_split[0])
    # notificacion = int(params_split[1])

    anti = Antidoping.objects.get(pk=id_antidoping)
    estudiante_muestra = EstudianteMuestra.objects.filter(antidoping=id_antidoping)

    lista = []
    
    for est in estudiante_muestra:

      # quitar comentario y identar esta lista.append
      # if est.notificacion = 0:
      # Condiciones para generar una carta:
      # 1. estado = 0 iniciado | notificacion = 1
      # 2. estado = 1 primera notificacion recibida | notificacion = 2
      if est.estado == (notificacion - 1) and est.estado != 3: 
        dia = est.antidoping.dia
        if dia == "lunes":
          horario = est.inscrito.grupo.horario_1
        elif dia == "martes":
          horario = est.inscrito.grupo.horario_2
        elif dia == "miercoles":
          horario = est.inscrito.grupo.horario_3
        elif dia == "jueves":
          horario = est.inscrito.grupo.horario_4
        elif dia == "viernes":
          horario = est.inscrito.grupo.horario_5
        elif dia == "sabado":
          horario = est.inscrito.grupo.horario_6
        horario_split = horario.split("|")

        est_dic = {}
        est_dic['nombres'] = est.inscrito.estudiante.nombre
        est_dic['apellidos'] = est.inscrito.estudiante.apellido
        est_dic['matricula'] = est.inscrito.estudiante.matricula
        est_dic['horario'] = horario_split[0]
        est_dic['salon'] = horario_split[1]
        est_dic['materia'] = est.inscrito.grupo.clase.nombre
        est_dic['folio'] = est.folio
        est_dic['tipo_de_seleccion'] = 'seleccionado aleatoriamente'
        lista.append(est_dic)

    PWD = os.path.dirname(os.path.realpath(__file__))
    LOGO = os.path.join(PWD, "static/itesm.jpg")
    
    # Documento donde se vaciara la plantilla
    nombre_doc = "carta_notificacion_" + str(notificacion) + "_id_"+ str(id_antidoping) + ".pdf"
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + nombre_doc
    buffer = BytesIO()

    # Plantilla que se convertira en PDF
    plantilla=[]
    documento = SimpleDocTemplate(buffer,pagesize=letter,rightMargin=65,leftMargin=65,topMargin=20,bottomMargin=20)
    
    # Estilos del documento
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))

    # Imagen de la institución
    logo = LOGO
    imagen = Image(logo, 3.3*inch, 1.5*inch)
    imagen.hAlign = 'LEFT'
    
    fecha = obten_fecha()
    fecha_completa = obten_fecha_completa().upper()

    # Consulta cada elemento de la lista y lo convierte en una hoja que es enviada al documento verificando el numero de carta
    if notificacion== 1:
      for alumno in lista:
          hoja = primera_carta(alumno['materia'], alumno['salon'], alumno['horario'], alumno['nombres'], alumno['apellidos'], alumno['matricula'], alumno['folio'], alumno['tipo_de_seleccion'], fecha, fecha_completa, styles, imagen)
          plantilla += hoja
    elif notificacion== 2:
      for alumno in lista:
          hoja = segunda_carta(alumno['materia'], alumno['salon'], alumno['horario'], alumno['nombres'], alumno['apellidos'], alumno['matricula'], alumno['folio'], alumno['tipo_de_seleccion'], fecha, fecha_completa, styles, imagen)
          plantilla += hoja
    elif notificacion== 3:
      lista3 = []
      for est3 in estudiante_muestra:
        tn = {}
        tn['nombres'] = est3.inscrito.estudiante.nombre
        tn['apellidos'] = est3.inscrito.estudiante.apellido
        tn['matricula'] = est3.inscrito.estudiante.matricula
        lista3.append(tn)
      #genera el csv
      csv = tercera_carta_csv(lista3, styles, imagen)
      hoja = tercera_carta(lista3, styles, imagen)
      plantilla += hoja
    
    # Vacia la plantilla en el documento    
    documento.build(plantilla)
    
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    #return csv
    return response

@login_required
def success(request):
    return render_to_response('home/success_muestra.html', context_instance=RequestContext(request))

#Vista que da acceso al alumno a su encuesta correspondiente
@login_required
def autenticacion_encuesta(request):
    if request.method == 'POST':
        folio = request.POST['folio']
        if EstudianteMuestra.objects.filter(folio=folio).exists():
            campo = EstudianteMuestra.objects.get(folio = folio)
            if campo.respuestas:
                return render_to_response('encuestas/autenticacion.html', {'existe_respuesta': campo.respuestas}, context_instance=RequestContext(request))
            else:
                return redirect('/aplicacion_encuesta/'+folio)
        else:
            no_existe_folio = True
            return render_to_response('encuestas/autenticacion.html', {'no_existe_folio': no_existe_folio}, context_instance=RequestContext(request))
    else:
        return render_to_response('encuestas/autenticacion.html', context_instance=RequestContext(request))

#Vista de la forma de encuesta a llenar
@login_required
def aplicacion_encuesta(request,id):
    estudiante_muestra = EstudianteMuestra.objects.get(folio = id)
    estudiante = estudiante_muestra.inscrito.estudiante
    if request.method == 'POST':
      forma = AplicacionEncuesta(request.POST, instance=estudiante_muestra)
      forma.helper.form_action = reverse('aplicacion_encuesta', args=[id])
      if forma.is_valid():
        # nombres = forma.cleaned_data['nombres']
        # apellidos = forma.cleaned_data['apellidos']
        # matricula = forma.cleaned_data['matricula']
        medicamento_consumido = forma.cleaned_data['medicamento_consumido']
        medicamento_consumido_paraque = forma.cleaned_data['medicamento_consumido_paraque']
        alcohol_frecuencia = forma.cleaned_data['alcohol_frecuencia']
        tabaco_frecuencia = forma.cleaned_data['tabaco_frecuencia']
        droga_ofrecido = forma.cleaned_data['droga_ofrecido']
        quien_ofrecido = forma.cleaned_data['quien_ofrecido']
        quien_ofrecido_otro = forma.cleaned_data['quien_ofrecido_otro']
        donde_ofrecido = forma.cleaned_data['donde_ofrecido']
        donde_ofrecido_otro = forma.cleaned_data['donde_ofrecido_otro']
        que_ofrecido = forma.cleaned_data['que_ofrecido']
        que_ofrecido_otro = forma.cleaned_data['que_ofrecido_otro']
        haz_consumido = forma.cleaned_data['haz_consumido']
        edad_consumido = forma.cleaned_data['edad_consumido']
        que_consumido = forma.cleaned_data['que_consumido']
        que_consumido_otro = forma.cleaned_data['que_consumido_otro']
        ultimo_consumido = forma.cleaned_data['ultimo_consumido']
        que_consumido2 = forma.cleaned_data['que_consumido2']
        que_consumido2_otro = forma.cleaned_data['que_consumido2_otro']
        conoces_consumidor = forma.cleaned_data['conoces_consumidor']
        de_donde = forma.cleaned_data['de_donde']
        de_donde_otro = forma.cleaned_data['de_donde_otro']
        lugar_consumo = forma.cleaned_data['lugar_consumo']
        lugar_consumo_donde = forma.cleaned_data['lugar_consumo_donde']
        relaciones = forma.cleaned_data['relaciones']
        #print "Entre aqui"
        notas = "Escribir las notas aquí"
        respuestas = {"medicamento_consumido":"%s" % medicamento_consumido , "medicamento_consumido_paraque":"%s" % medicamento_consumido_paraque, "alcohol_frecuencia":"%s" % alcohol_frecuencia, "tabaco_frecuencia":"%s" % tabaco_frecuencia, "droga_ofrecido":"%s" % droga_ofrecido, "quien_ofrecido":"%s" % quien_ofrecido, "quien_ofrecido_otro":"%s" % quien_ofrecido_otro, "donde_ofrecido":"%s" % donde_ofrecido, "donde_ofrecido_otro":"%s" % donde_ofrecido_otro, "que_ofrecido":"%s" % que_ofrecido, "que_ofrecido_otro":"%s" % que_ofrecido_otro, "haz_consumido":"%s" % haz_consumido, "edad_consumido":"%s" % edad_consumido, "que_consumido":"%s" % que_consumido, "que_consumido_otro":"%s" % que_consumido_otro, "ultimo_consumido":"%s" % ultimo_consumido, "que_consumido2":"%s" % que_consumido2, "que_consumido2_otro":"%s" % que_consumido2_otro, "conoces_consumidor":"%s" % conoces_consumidor, "de_donde":"%s" % de_donde, "de_donde_otro":"%s" % de_donde_otro, "lugar_consumo":"%s" % lugar_consumo, "lugar_consumo_donde":"%s" % lugar_consumo_donde, "relaciones":"%s" % relaciones}
        respuestas = simplejson.dumps(respuestas)
        estudiante_muestra.respuestas = respuestas
        estudiante_muestra.notas = notas
        estudiante_muestra.estado = 3     # 3 que significa que ya se respondio la encuesta.
        estudiante_muestra.save()
        # return redirect('/encuesta_agradecimiento/')
        return render_to_response('encuestas/encuesta_agradecimiento.html', context_instance=RequestContext(request))
    else:
      forma = AplicacionEncuesta(instance=estudiante_muestra)
    return render_to_response('encuestas/encuesta.html', {'forma': forma, 'estudiante': estudiante}, context_instance=RequestContext(request))

#Vista de la pantalla despues de haber contestado la encuesta
# @login_required
# def encuesta_agradecimiento(request):
#   return render_to_response('encuestas/encuesta_agradecimiento.html', context_instance=RequestContext(request))

#Vista de todas las encuestas que han sido contestadas
@login_required
def encuestas_contestadas(request):
  encuestas = EstudianteMuestra.objects.exclude(respuestas__isnull=True).exclude(respuestas__exact='')
  return render_to_response('encuestas/encuestas_contestadas.html',{'encuestas': encuestas}, context_instance=RequestContext(request))

#Vista de la encuesta con las respuestas
@login_required
def revisar_encuesta(request,id):
    rev_enc = EstudianteMuestra.objects.get(pk = id)
    folio = rev_enc.folio 
    json = rev_enc.respuestas
    json = simplejson.loads(json)
    if request.method == 'POST':
        forma = EncuestaContestada(request.POST, instance=rev_enc)
        forma.helper.form_action = reverse('revisar_encuesta', args=[id])
        if forma.is_valid():
            medicamento_consumido = forma.cleaned_data['medicamento_consumido']
            medicamento_consumido_paraque = forma.cleaned_data['medicamento_consumido_paraque']
            alcohol_frecuencia = forma.cleaned_data['alcohol_frecuencia']
            tabaco_frecuencia = forma.cleaned_data['tabaco_frecuencia']
            droga_ofrecido = forma.cleaned_data['droga_ofrecido']
            quien_ofrecido = forma.cleaned_data['quien_ofrecido']
            quien_ofrecido_otro = forma.cleaned_data['quien_ofrecido_otro']
            donde_ofrecido = forma.cleaned_data['donde_ofrecido']
            donde_ofrecido_otro = forma.cleaned_data['donde_ofrecido_otro']
            que_ofrecido = forma.cleaned_data['que_ofrecido']
            que_ofrecido_otro = forma.cleaned_data['que_ofrecido_otro']
            haz_consumido = forma.cleaned_data['haz_consumido']
            edad_consumido = forma.cleaned_data['edad_consumido']
            que_consumido = forma.cleaned_data['que_consumido']
            que_consumido_otro = forma.cleaned_data['que_consumido_otro']
            ultimo_consumido = forma.cleaned_data['ultimo_consumido']
            que_consumido2 = forma.cleaned_data['que_consumido2']
            que_consumido2_otro = forma.cleaned_data['que_consumido2_otro']
            conoces_consumidor = forma.cleaned_data['conoces_consumidor']
            de_donde = forma.cleaned_data['de_donde']
            de_donde_otro = forma.cleaned_data['de_donde_otro']
            lugar_consumo = forma.cleaned_data['lugar_consumo']
            lugar_consumo_donde = forma.cleaned_data['lugar_consumo_donde']
            relaciones = forma.cleaned_data['relaciones']
            notas = forma.cleaned_data['notas']
            #print "Entre aqui"            
            respuestas = {"medicamento_consumido":"%s" % medicamento_consumido , "medicamento_consumido_paraque":"%s" % medicamento_consumido_paraque, "alcohol_frecuencia":"%s" % alcohol_frecuencia, "tabaco_frecuencia":"%s" % tabaco_frecuencia, "droga_ofrecido":"%s" % droga_ofrecido, "quien_ofrecido":"%s" % quien_ofrecido, "quien_ofrecido_otro":"%s" % quien_ofrecido_otro, "donde_ofrecido":"%s" % donde_ofrecido, "donde_ofrecido_otro":"%s" % donde_ofrecido_otro, "que_ofrecido":"%s" % que_ofrecido, "que_ofrecido_otro":"%s" % que_ofrecido_otro, "haz_consumido":"%s" % haz_consumido, "edad_consumido":"%s" % edad_consumido, "que_consumido":"%s" % que_consumido, "que_consumido_otro":"%s" % que_consumido_otro, "ultimo_consumido":"%s" % ultimo_consumido, "que_consumido2":"%s" % que_consumido2, "que_consumido2_otro":"%s" % que_consumido2_otro, "conoces_consumidor":"%s" % conoces_consumidor, "de_donde":"%s" % de_donde, "de_donde_otro":"%s" % de_donde_otro, "lugar_consumo":"%s" % lugar_consumo, "lugar_consumo_donde":"%s" % lugar_consumo_donde, "relaciones":"%s" % relaciones}
            respuestas = simplejson.dumps(respuestas)
            rev_enc.respuestas = respuestas
            rev_enc.notas = notas
            rev_enc.save()
        return redirect('/encuestas_contestadas/')
    else:
        forma = EncuestaContestada(instance=rev_enc)
        #folio
        forma.fields['folio'].initial = folio

        #respuesta de pregunta 1
        forma.fields['medicamento_consumido'].initial = json['medicamento_consumido']
        #respuesta de pregunta 1
        forma.fields['medicamento_consumido_paraque'].initial = json['medicamento_consumido_paraque']
        #respuesta de pregunta 2
        forma.fields['alcohol_frecuencia'].initial = json['alcohol_frecuencia']
        #respuesta de pregunta 3
        forma.fields['tabaco_frecuencia'].initial = json['tabaco_frecuencia']
        #respuesta de pregunta 4
        forma.fields['droga_ofrecido'].initial = json['droga_ofrecido']
        #respuesta de pregunta 5
        forma.fields['quien_ofrecido'].initial = json['quien_ofrecido']        
        #respuesta de pregunta 5
        forma.fields['quien_ofrecido_otro'].initial = json['quien_ofrecido_otro']
        #respuesta de pregunta 6
        forma.fields['donde_ofrecido'].initial = json['donde_ofrecido']
        #respuesta de pregunta 6
        forma.fields['donde_ofrecido_otro'].initial = json['donde_ofrecido_otro']
        #respuesta de pregunta 7
        forma.fields['que_ofrecido'].initial = json['que_ofrecido']
        #respuesta de pregunta 7
        forma.fields['que_ofrecido_otro'].initial = json['que_ofrecido_otro']
        #respuesta de pregunta 8
        forma.fields['haz_consumido'].initial = json['haz_consumido']
        #respuesta de pregunta 9
        forma.fields['edad_consumido'].initial = json['edad_consumido']
        #respuesta de pregunta 10
        forma.fields['que_consumido'].initial = json['que_consumido']        
        #respuesta de pregunta 10
        forma.fields['que_consumido_otro'].initial = json['que_consumido_otro']        
        #respuesta de pregunta 11
        forma.fields['ultimo_consumido'].initial = json['ultimo_consumido']
        #respuesta de pregunta 12
        forma.fields['que_consumido2'].initial = json['que_consumido2']
        #respuesta de pregunta 12
        forma.fields['que_consumido2_otro'].initial = json['que_consumido2_otro']
        #respuesta de pregunta 13
        forma.fields['conoces_consumidor'].initial = json['conoces_consumidor']        
        #respuesta de pregunta 14
        forma.fields['de_donde'].initial = json['de_donde']
        #respuesta de pregunta 14
        forma.fields['de_donde_otro'].initial = json['de_donde_otro']
        #respuesta de pregunta 15
        forma.fields['lugar_consumo'].initial = json['lugar_consumo']
        #respuesta de pregunta 16
        forma.fields['lugar_consumo_donde'].initial = json['lugar_consumo_donde']
        #respuesta de pregunta 17
        forma.fields['relaciones'].initial = json['relaciones']
    return render_to_response('encuestas/revisar_encuesta.html', {'forma': forma}, context_instance=RequestContext(request))

#   Vista para generar reportes en Highcharts
#   Se planea segmentar para generar diferentes clases de reportes.
@login_required
def reportes(request, anio=2013):
    general = EstudianteMuestra.objects.filter(resultado__isnull=False).values('resultado').annotate(Cantidad=Count('resultado'))
    color = Estudiante.objects.filter(color__isnull=False).values('color').annotate(Cantidad=Count('color'))

    total_alumnos_general = 0
    for x in general:
      total_alumnos_general += x['Cantidad']

    total_alumnos_color = 0
    for x in color:
      total_alumnos_color += x['Cantidad']

    return render_to_response('home/reportes/reportes.html', {'general': general,'total_alumnos_general': total_alumnos_general,'total_alumnos_color': total_alumnos_color, 'color': color}, context_instance=RequestContext(request))

@login_required
#@transaction.commit_manually
def subir_csv(request):
    if request.method == 'POST':
      forma = UploadFileForm(request.POST, request.FILES)
      if forma.is_valid():
        try:
          handle_uploaded_file(request.FILES['file'])
          #transaction.commit()
        except:
          pass
          #transaction.rollback()
        return HttpResponseRedirect('success/')
    else:
        forma = UploadFileForm()
    return render_to_response('home/upload_csv.html', {'forma': forma}, context_instance=RequestContext(request))

def consulta_master(request):
    if request.is_ajax():
        q1 = request.GET.get('q1', '')
        q2 = request.GET.get('q2', '')
        results = Avaluo.objects.all()
        if q1:
            results = results.filter(Q(FolioK__contains=q1) | Q(Referencia__contains=q1))
        if q2:
            results = results.filter((Q(Factura__contains=q2)))
        data = {'results': results}
        return render_to_response('home/consultas/results.html', data, context_instance=RequestContext(request))


@login_required
def subir_csv_back(request):
    if request.method == 'POST':
      forma = UploadFileForm(request.POST, request.FILES)
      if forma.is_valid():
        handle_uploaded_file(request.FILES['file'])
        return HttpResponseRedirect('success/')
    else:
        forma = UploadFileForm()
    return render_to_response('home/upload_csv.html', {'forma': forma}, context_instance=RequestContext(request))

@login_required
def subir_csv_success(request):
    return render_to_response('home/upload_csv_success.html', context_instance=RequestContext(request))

def handle_uploaded_file(f):
    inicial = datetime.datetime.now()

    #Lee el archivo linea por linea y lo almacena en la lista
    lista = []
    matriculas = []
    crns = []
    claves_mat = []

    contador_lectura = 0;
    for line in f:
      contador_lectura += 1
      estado_importacion = "Obteniendo linea " + str(contador_lectura) + " del archivo de CSV"
      print estado_importacion

      line = line.replace(",\n", "") # remove bad terminated line with extra comma
      line = line.replace("\n", "") # remove all the whitespace
      line = line.replace("'", "") # remove all the "
      line = line.replace('"', "") # remove all the '
      line = line.replace(', ', ",") # remove all the whitespace

      line = line.split(",")  
    
      fila = {}

      matricula = int(line[0].replace("A", ""))

      fila['matricula'] = matricula
      fila['nombre'] = line[1]
      fila['apellido'] = line[2]
      fila['correo'] = line[3]
      fila['telefono'] = line[4]
      fila['celular'] = line[5]
      fila['nombrePadre'] = line[6]
      fila['apellidoPadre'] = line[7]
      fila['correoPadre'] = line[8]
      fila['telefonoPadre'] = line[9]
      fila['celularPadre'] = line[10]
      fila['nombreMadre'] = line[11]
      fila['apellidoMadre'] = line[12]
      fila['correoMadre'] = line[13]
      fila['telefonoMadre'] = line[14]
      fila['celularMadre'] = line[15]
      fila['crn'] = line[16]
      fila['horario_1'] = line[17]
      fila['horario_2'] = line[18]
      fila['horario_3'] = line[19]
      fila['horario_4'] = line[20]
      fila['horario_5'] = line[21]
      fila['horario_6'] = line[22]
      fila['profesor'] = line[23]
      fila['clave_materia'] = line[24]
      fila['nombre_materia'] = line[25]
      lista.append(fila)

      matriculas.append(matricula)
      crns.append(line[16])
      claves_mat.append(line[24].replace("'", ""))
    
    # Obtiene los valores unicos almacenados en las listas de matriculas, crns y claves de materia
    matriculas = sorted(set(matriculas))
    crns = sorted(set(crns))
    claves_mat = sorted(set(claves_mat))

    estado_importacion = "Actualizando estatus en la institución de todos los estudiantes"
    print "\n\n\n"
    print estado_importacion

    # actualiza el estatus de todos los estudiantes a 0
    Estudiante.objects.all().update(estado_institucion='0')

    # Agrega o actualiza los estudiantes
    cont_estudiantes = 0
    print "\n\n\n"
    for matricula in matriculas:
      cont_estudiantes += 1
      estado_importacion = "Guardando información del estudiante " +  str(cont_estudiantes) + " de " + str(len(matriculas))
      print estado_importacion

      # Si el estudiante existe simplemente actualiza el estatus en la institución
      try:
        est = Estudiante.objects.get(matricula=matricula)
        est.estado_institucion = '1'
        est.save()
      
      #Si el estudiante no existe inserta los datos de su padre y madre, para posteriormente insertar al alumno
      except Estudiante.DoesNotExist:
        nuevoEst = buscaArreglo(matricula, 'matricula', lista)

        padreNuevo = Padre(nombre=nuevoEst['nombrePadre'], apellido=nuevoEst['apellidoPadre'], correo=nuevoEst['correoPadre'], telefono=nuevoEst['telefonoPadre'], celular=nuevoEst['celularPadre'])
        padreNuevo.save()
        madreNuevo = Padre(nombre=nuevoEst['nombreMadre'], apellido=nuevoEst['apellidoMadre'], correo=nuevoEst['correoMadre'], telefono=nuevoEst['telefonoMadre'], celular=nuevoEst['celularMadre'])
        madreNuevo.save()

        modeloEst = Estudiante (matricula=nuevoEst['matricula'], nombre=nuevoEst['nombre'], apellido=nuevoEst['apellido'], correo=nuevoEst['correo'], telefono=nuevoEst['telefono'], celular=nuevoEst['celular'], padre_id=padreNuevo.id, madre_id=madreNuevo.id, color='0', estado_institucion='1')
        modeloEst.save()

    # Agrega las materias que no estan dadas de alta en la base de datos
    cont_materias = 0
    print "\n\n\n"
    materia_claves_id = []
    for clave in claves_mat:
      cont_materias += 1
      estado_importacion = "Guardando información de la clase " +  str(cont_materias) + " de " + str(len(claves_mat))
      print estado_importacion

      # Si ya existe solo almacena el valor en la lista materia_claves_id
      try:
        clase = Clase.objects.get(clave_materia=clave)
        fil = {}
        fil['clave'] = clave
        fil['id'] = str(clase.id)
        materia_claves_id.append(fil)

      # Si no existe lo inserta, ademas de almacenar el valor en el arreglo
      except Clase.DoesNotExist:
        arrClase = buscaArreglo(clave, 'clave_materia', lista)
        claseNueva = Clase(clave_materia=arrClase['clave_materia'], nombre=arrClase['nombre_materia'])
        claseNueva.save()
        fil = {}
        fil['clave'] = clave
        fil['id'] = str(claseNueva.id)
        materia_claves_id.append(fil)

    # Obtiene el año y semestre actual
    anioActual = date.today().year
    semestre = date.today().month
    if semestre == 1 or semestre == 2 or semestre == 3 or semestre == 4 or semestre == 5:
      semestre = 1
    elif semestre == 6  or semestre == 7:
      semestre = 2
    else:
      semestre = 3

    # Para cada crn unico almacena la información de su grupo en la base de datos
    cont_grupo = 0
    print "\n\n\n"
    for crn in crns:
      cont_grupo += 1
      estado_importacion = "Guardando información del grupo " +  str(cont_grupo) + " de " + str(len(crns))
      print estado_importacion

      arrGrupos = buscaArreglo(crn, 'crn', lista)
      arrClave = buscaArreglo(arrGrupos['clave_materia'], 'clave', materia_claves_id)
      grupoNuevo = Grupo(crn=arrGrupos['crn'], clase_id=arrClave['id'], horario_1=arrGrupos['horario_1'], horario_2=arrGrupos['horario_2'], horario_3=arrGrupos['horario_3'], horario_4=arrGrupos['horario_4'], horario_5=arrGrupos['horario_5'], horario_6=arrGrupos['horario_6'], anio=anioActual ,semestre=semestre ,profesor=arrGrupos['profesor'])
      grupoNuevo.save()

    # Relaciona a los alumnos actuales con las materias que esta cursando
    inscritos = [Inscrito(estudiante_id=renglon['matricula'], grupo_id=renglon['crn']) for renglon in lista]
    Inscrito.objects.bulk_create(inscritos)

    final = datetime.datetime.now()
    diferencia = final - inicial
    estado_importacion = "Relacionando estudiantes con sus grupos actuales"
    print "\n\n\n"
    print estado_importacion
    print "La importación de datos tardo " + str(diferencia.seconds) + " segundo(s)"

def buscaArreglo(clave, campo, lista):
    for regresa in lista:
      if regresa[campo] == clave:
        return regresa
