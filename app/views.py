# -*- coding: utf-8 -*
# Create your views here.
import os
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
from random import sample, shuffle, randint
from app.cartas_notificacion import *

# For debugging.
import pdb

@login_required
def home(request):
    return render_to_response('home/home.html', context_instance=RequestContext(request))
    
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
        
def logout_view(request):
    logout(request)
    # Redirect to a success page.

@login_required
def perfil_estudiante(request,id):
    estudiante = Estudiante.objects.get(pk = id) 
    #itemset_queryset = EstudianteResultado.objects.filter(estudiante_id=id).values_list('antidoping_id', flat=True)
    resultados = EstudianteResultado.objects.filter(estudiante_id=id).select_related()
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
def estudiante(request):
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
    antidopings = Antidoping.objects.all()  
    return render_to_response('home/muestra/muestra.html',{'antidopings': antidopings}, context_instance=RequestContext(request))

@login_required
def success(request):
    return render_to_response('home/success.html', context_instance=RequestContext(request))    

@login_required
def eliminar_muestra(request,id):
   antidoping_borrar = Antidoping.objects.get(pk=int(id))   # Obtener el antidoping a borrar.
   antidoping_borrar.estudiantemuestra_set.all().delete()   # Borrar los alumnos de la muestra relacionados a él.
   antidoping_borrar.delete()                               # Borrar el antidoping.

   return redirect('/muestra/')

@login_required
def perfil_muestra(request,id):
   antidoping = Antidoping.objects.get(pk=id)
   #Select
   #itemset_queryset = EstudianteMuestra.objects.filter(antidoping=antidoping).values_list('inscrito_id', flat=True)
   #estudiantes_muestra = antidoping.estudiantemuestra_set.all()
   alumnos = map(lambda x: x.inscrito.estudiante, antidoping.estudiantemuestra_set.all())
   grupos = map(lambda x: x.inscrito.grupo, antidoping.estudiantemuestra_set.all())   
   grupos = list(set(grupos))
   #alumnos = Estudiante.objects.filter(matricula__in=itemset_queryset)   
   
   #alumnos_grupo = Inscrito.objects.filter(estudiante_id__in=itemset_queryset).values_list('grupo_id', flat=True)
   #grupos = Grupo.objects.filter(crn__in=alumnos_grupo).select_related()
   return render_to_response('home/muestra/perfil_muestra.html',{'alumnos': alumnos,'grupos': grupos,'antidoping': antidoping}, context_instance=RequestContext(request))    
   
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
        muestra_grupos = []
        muestra_aleatorios = []
        delimitador = '|'

        print "dia..", dia
        print "antidoping id..",nuevo_antidoping.pk 
        # print "hora de inicio.." ,nuevo_antidoping.antidoping_inicio
        print "dia de antidoping",dia
        print "hora inicio",inicio
        print "hora fin",fin
        print alumnos_seleccionados, grupos_seleccionados
        print "Rango horas: ", obtener_horario_de_forma(inicio, fin)

        # Modificar si se necesita null.
        if dia == 'lunes':
          grupos = Grupo.objects.exclude(horario_1='None')
          # Revisar que se encuentre los grupos dentro del horario deseado.
          for gpo in grupos:
            horario_gpo = convierte_de_horario(gpo.horario_1, delimitador)
            horario_atdp = obtener_horario_de_forma(inicio, fin)
            if horario_gpo['hora_inicio'] >= horario_atdp['hora_inicio'] and horario_gpo['hora_fin'] <= horario_atdp['hora_fin']:
              muestra_grupos = muestra_grupos + [gpo]       # Guardar el grupo en una lista.
     
        elif dia == 'martes':
          grupos = Grupo.objects.exclude(horario_2='None')
          # Revisar que se encuentre los grupos dentro del horario deseado.
          for gpo in grupos:
            horario_gpo = convierte_de_horario(gpo.horario_2, delimitador)
            horario_atdp = obtener_horario_de_forma(inicio, fin)
            if horario_gpo['hora_inicio'] >= horario_atdp['hora_inicio'] and horario_gpo['hora_fin'] <= horario_atdp['hora_fin']:
              muestra_grupos = muestra_grupos + [gpo]       # Guardar el grupo en una lista.

        elif dia == 'miercoles':
          grupos = Grupo.objects.exclude(horario_3='None')
          # Revisar que se encuentre los grupos dentro del horario deseado.
          for gpo in grupos:
            horario_gpo = convierte_de_horario(gpo.horario_3, delimitador)
            horario_atdp = obtener_horario_de_forma(inicio, fin)
            if horario_gpo['hora_inicio'] >= horario_atdp['hora_inicio'] and horario_gpo['hora_fin'] <= horario_atdp['hora_fin']:
              muestra_grupos = muestra_grupos + [gpo]       # Guardar el grupo en una lista.

        elif dia == 'jueves':
          grupos = Grupo.objects.exclude(horario_4='None')
          # Revisar que se encuentre los grupos dentro del horario deseado.
          for gpo in grupos:
            horario_gpo = convierte_de_horario(gpo.horario_4, delimitador)
            horario_atdp = obtener_horario_de_forma(inicio, fin)
            if horario_gpo['hora_inicio'] >= horario_atdp['hora_inicio'] and horario_gpo['hora_fin'] <= horario_atdp['hora_fin']:
              muestra_grupos = muestra_grupos + [gpo]       # Guardar el grupo en una lista.

        elif dia == 'viernes':
          grupos = Grupo.objects.exclude(horario_5='None')
          # Revisar que se encuentre los grupos dentro del horario deseado.
          for gpo in grupos:
            horario_gpo = convierte_de_horario(gpo.horario_5, delimitador)
            horario_atdp = obtener_horario_de_forma(inicio, fin)
            if horario_gpo['hora_inicio'] >= horario_atdp['hora_inicio'] and horario_gpo['hora_fin'] <= horario_atdp['hora_fin']:
              muestra_grupos = muestra_grupos + [gpo]       # Guardar el grupo en una lista.

        elif dia == 'sabado':
          grupos = Grupo.objects.exclude(horario_5='None')
          # Revisar que se encuentre los grupos dentro del horario deseado.
          for gpo in grupos:
            horario_gpo = convierte_de_horario(gpo.horario_5, delimitador)
            horario_atdp = obtener_horario_de_forma(inicio, fin)
            if horario_gpo['hora_inicio'] >= horario_atdp['hora_inicio'] and horario_gpo['hora_fin'] <= horario_atdp['hora_fin']:
              muestra_grupos = muestra_grupos + [gpo]       # Guardar el grupo en una lista.

       # Alumnos que pertenecen a los grupos senalados.
        for gpo_seleccionado in grupos_seleccionados:
          muestra_aleatorios = muestra_aleatorios + sample(Inscrito.objects.filter(grupo_id=gpo_seleccionado), randint(3,5))

        # Obtener alumnos que fueron senalados y que se pueden encontrar en los grupos.
        total_grupos = muestra_grupos + list(Grupo.objects.filter(pk__in=grupos_seleccionados))
        total_grupos = list(set(total_grupos))
        muestra_seleccionados = Inscrito.objects.filter(estudiante_id__in=alumnos_seleccionados, grupo__in=total_grupos)
      
        # Protegemos la identidad del alumno seleccionado agregando otros alumnos.
        for inscrito in muestra_seleccionados:
          muestra_aleatorios = muestra_aleatorios + sample(Inscrito.objects.filter(grupo=inscrito.grupo), randint(2,4))
          muestra_grupos = filter(lambda gpo: gpo != inscrito.grupo, muestra_grupos)  # Eliminar de la seleccion.

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
        nuevo_antidoping.muestra_inicio = inicio
        nuevo_antidoping.muestra_fin = fin
        nuevo_antidoping.antidoping_inicio = timezone.now()
        nuevo_antidoping.tamano_muestra = cantidad_total_muestra
        nuevo_antidoping.estado_antidoping = 0
        nuevo_antidoping.notas = forma.cleaned_data['notas']
        nuevo_antidoping.save()

        # Guardar las personas de la muestra.
        for inscrito in list(muestra_seleccionados) + list(muestra_aleatorios):
          tmp = EstudianteMuestra(inscrito=inscrito, antidoping=nuevo_antidoping)
          tmp.save() 


        return render_to_response('home/verificar_muestra.html',
          {
          'muestra': muestra_aleatorios, 
          'muestra_seleccionados': muestra_seleccionados, 
          'cantidad_total_muestra': cantidad_total_muestra,
          'cantidad_total_seleccionados': cantidad_alumnos_seleccionados,
          'dia': dia, 
          'inicio': inicio, 
          'fin': fin, 
          'verificar': True
          }, context_instance=RequestContext(request))

  
    else:
        forma = CrearAntidoping() # An unbound form
        #forma2 = SeleccionMuestra() # An unbound form
    return render_to_response('home/muestra/seleccion_muestra.html', { 'forma': forma} , context_instance=RequestContext(request))
    
@login_required
def alta_muestra(request):
  if request.method == 'POST':
    lista_a_borrar = map(int, request.POST.getlist('eliminar-de-muestra'))
    elementos_a_borrar = EstudianteMuestra.objects.filter(inscrito_id__in=lista_a_borrar)
    if len(elementos_a_borrar) > 0:
      antidoping_tmp = elementos_a_borrar[0].antidoping
      antidoping_tmp.tamano_muestra = elementos_a_borrar[0].antidoping.tamano_muestra - len(lista_a_borrar)
      antidoping_tmp.save()
      
    elementos_a_borrar.delete()



    # muestra = EstudianteMuestra.objects.all()
    # for m in muestra:
    #   print m.estudiante.matricula, m.estudiante.nombre

    return redirect('/success')  # Redirect after POST
  else:
    # return render_to_response('home/home.html', context_instance=RequestContext(request))
    return home(request)

@login_required
def success(request):
    return render_to_response('home/success_muestra.html', context_instance=RequestContext(request))

@login_required
def obtener_carta(request, params):
    
    params = "1-1"
    params_split = params.split("-")

    id_antidoping = int(params_split[0])
    notificacion = int(params_split[1])

    anti = Antidoping.objects.get(pk=id_antidoping)
    estudiante_muestra = EstudianteMuestra.objects.filter(antidoping=id_antidoping)

    lista = []
    
    for est in estudiante_muestra:

      # quitar comentario y identar esta lista.append
      # if est.notificacion = 0:
      
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
          hoja = primera_carta(alumno['materia'], alumno['salon'], alumno['horario'], alumno['nombres'], alumno['apellidos'], alumno['matricula'], alumno['tipo_de_seleccion'], fecha, fecha_completa, styles, imagen)
          plantilla += hoja
    elif notificacion== 2:
      for alumno in lista:
          hoja = segunda_carta(alumno['materia'], alumno['salon'], alumno['horario'], alumno['nombres'], alumno['apellidos'], alumno['matricula'], alumno['tipo_de_seleccion'], fecha, fecha_completa, styles, imagen)
          plantilla += hoja
    elif notificacion== 3:
      for alumno in lista:
          hoja = tercera_carta(alumno['materia'], alumno['salon'], alumno['horario'], alumno['nombres'], alumno['apellidos'], alumno['matricula'], alumno['tipo_de_seleccion'], fecha, fecha_completa, styles, imagen)
          plantilla += hoja
    
    # Vacia la plantilla en el documento    
    documento.build(plantilla)
    
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response

@login_required
def success(request):
    return render_to_response('home/success_muestra.html', context_instance=RequestContext(request))

login_required
def aplicacion_encuesta(request):
    if request.method == 'POST':
        forma = AplicacionEncuesta(request.POST)
        if forma.is_valid():            
            folio = forma.cleaned_data['folio']
            nombres = forma.cleaned_data['nombres']
            apellidos = forma.cleaned_data['apellidos']
            notas = "notas"
            matricula = forma.cleaned_data['matricula']
            correo = forma.cleaned_data['correo']
            semestre = forma.cleaned_data['semestre']
            opinion = forma.cleaned_data['opinion']
            frecuencia = forma.cleaned_data['frecuencia']
            respuestas = "{\"nombres\":\"%s\", \"apellidos\":\"%s\",\"matricula\":\"%s\",\"correo\":\"%s\",\"semestre\":\"%s\",\"opinion\":\"%s\",\"frecuencia\":%s}" % (nombres, apellidos, matricula, correo, semestre, opinion, frecuencia)
            e = Encuesta()
            e.folio = folio
            e.respuestas = respuestas
            e.notas = notas
            e.save()
        return redirect('/aplicacion_encuesta/')
    else:
        forma = AplicacionEncuesta()
    return render_to_response('encuestas/encuesta.html', { 'forma': forma}, context_instance=RequestContext(request))

@login_required
def encuesta(request):
    encuestas = Encuesta.objects.all()
    return render_to_response('encuestas/encuestas.html',{'encuestas': encuestas}, context_instance=RequestContext(request))

@login_required
def encuesta_estudiante(request,id):
    en_es = Encuesta.objects.get(pk = id)
    if request.method == 'POST':
        forma = AplicacionEncuesta(request.POST, instance=en_es)
        forma.helper.form_action = reverse('encuesta_estudiante', args=[id])
        if forma.is_valid():
            forma.save()
        return redirect('/encuesta_estudiante.html/')
    else:
        forma = AplicacionEncuesta(instance=en_es)
    return render_to_response('encuestas/encuesta_estudiante.html', {'forma': forma}, context_instance=RequestContext(request))

