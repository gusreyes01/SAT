# Create your views here.
# -*- coding: utf-8 -*
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
    if request.method == 'POST':
      forma = AltaEstudiante(request.POST, instance=estudiante)
      forma.helper.form_action = reverse('perfil_estudiante', args=[id])
      if forma.is_valid():
        forma.save()
        return redirect('/estudiante/')  
    else:
      forma = AltaEstudiante(instance=estudiante)
    return render_to_response('home/perfil_estudiante.html', {'forma': forma}, context_instance=RequestContext(request))    
   
@login_required
def estudiante(request):
    estudiantes = Estudiante.objects.all()[:1000]  
    return render_to_response('home/estudiante.html',{'estudiantes': estudiantes}, context_instance=RequestContext(request))    
    
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
    return render_to_response('home/alta_estudiante.html', { 'forma': forma} , context_instance=RequestContext(request))    
    
@login_required
def muestra(request):
    antidopings = Antidoping.objects.all()  
    return render_to_response('home/muestra.html',{'antidopings': antidopings}, context_instance=RequestContext(request))


@login_required
def eliminar_muestra(request,id):
   #+some code to check if New belongs to logged in user
   a = Antidoping.objects.get(pk=id).delete()    
   return redirect('/muestra/')

@login_required
def perfil_muestra(request,id):
   antidoping = Antidoping.objects.get(pk=id)
   #Select
   itemset_queryset = EstudianteMuestra.objects.filter(antidoping_id=1).values_list('inscrito_id', flat=True)
   alumnos = Estudiante.objects.filter(matricula__in=itemset_queryset)
   return render_to_response('home/perfil_muestra.html',{'alumnos': alumnos,'antidoping': antidoping}, context_instance=RequestContext(request))    

@login_required
def seleccion_muestra(request):
    if request.method == 'POST':
      # La forma ligada a los datos enviados en el POST
      forma = CrearAntidoping(request.POST)      

      # Todas las reglas de validacion aprobadas
      if forma.is_valid():

        nuevo_antidoping = forma.save(commit=False)
        nuevo_antidoping.antidoping_inicio = timezone.now()

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
        print "hora de inicio.." ,nuevo_antidoping.antidoping_inicio
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
          print "er:", elementos_restantes
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
          # cantidad_total_muestra = cantidad_total_muestra + cantidad_tmp
          elementos_restantes = elementos_restantes - cantidad_tmp

        cantidad_alumnos_aleatorios = len(muestra_aleatorios)
        cantidad_total_muestra = cantidad_alumnos_aleatorios + cantidad_alumnos_seleccionados

        

        return render_to_response('home/verificar_muestra.html',
          {
          'muestra': muestra_aleatorios, 
          'muestra_seleccionados': muestra_seleccionados, 
          'cantidad_total_muestra': cantidad_total_muestra,
          # 'cantidad_total_aleatorios': cantidad_alumnos_aleatorios,
          'cantidad_total_seleccionados': cantidad_alumnos_seleccionados,
          'dia': dia, 
          'inicio': inicio, 
          'fin': fin, 
          'verificar': True
          }, context_instance=RequestContext(request))

  
    else:
        forma = CrearAntidoping() # An unbound form
        #forma2 = SeleccionMuestra() # An unbound form
    return render_to_response('home/seleccion_muestra.html', {'forma': forma} , context_instance=RequestContext(request))

@login_required
def alta_muestra(request):
  if request.method == 'POST':
    print request.POST.getlist('eliminar-de-muestra')
    muestra = Inscrito.objects.filter(pk__in=map(int, request.POST.getlist('eliminar-de-muestra')))
    for m in muestra:
      print m.estudiante.matricula, m.estudiante.nombre
    return redirect('/success')  # Redirect after POST
  else:
    # return render_to_response('home/home.html', context_instance=RequestContext(request))
    return home(request)

@login_required
def success(request):
    return render_to_response('home/success_muestra.html', context_instance=RequestContext(request))    
