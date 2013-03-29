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
from django.utils import timezone

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
def success(request):
    return render_to_response('home/success.html', context_instance=RequestContext(request))    

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
      #forma2 = SeleccionMuestra(request.POST)     
      # Todas las reglas de validacion aprobadas
      if forma.is_valid():
        # pdb.set_trace()
        # El objeto no ha sido guardado en la forma.
        nuevo_antidoping = forma.save(commit=False)
        nuevo_antidoping.antidoping_inicio = timezone.now()

        seleccion_alumnos = forma.cleaned_data['seleccion_alumnos'].split(',')
        seleccion_grupos = forma.cleaned_data['seleccion_grupos'].split(',')
        
        # Datos necesarios para la muestra.
        tamano_muestra = int(forma.cleaned_data['tamano_muestra'])
        dia = forma.cleaned_data['dia']
        inicio = forma.cleaned_data['inicio']
        fin = forma.cleaned_data['fin']
        muestra_grupos = []
        delimitador = '|'

        print "dia..", dia
        print "antidoping id..",nuevo_antidoping.pk 
        print "hora de inicio.." ,nuevo_antidoping.antidoping_inicio
        print "dia de antidoping",dia
        print "hora inicio",inicio
        print "hora fin",fin
        print "Rango horas: ", obtener_horario_de_forma(inicio, fin)

        # Modificar si se necesita null.
        # def revisar_rango(horario_gpo, inicio, fin):
        #   horario_gpo = convierte_de_horario(horario_gpo)
        #   horario_atdp = obtener_horario_de_forma(inicio, fin)
        #   if horario_gpo['horario_inicio'] >= horario_atdp['horario_inicio'] and horario_gpo['horario_fin'] <= horario_atdp['horario_fin']
        print dia == '0'
        if dia == '0':
          grupos = Grupo.objects.exclude(horario_1='None')
          for gpo in grupos:
            horario_gpo = convierte_de_horario(gpo.horario_1, delimitador)
            horario_atdp = obtener_horario_de_forma(inicio, fin)
            if horario_gpo['hora_inicio'] >= horario_atdp['hora_inicio'] and horario_gpo['hora_fin'] <= horario_atdp['hora_fin']:
              print gpo.horario_1
              muestra_grupos = muestra_grupos + [gpo]

        elif dia == '1':
          grupos = Grupo.objects.exclude(horario_2='None')
        elif dia == '2':
          grupos = Grupo.objects.exclude(horario_3='None')
        elif dia == '3':
          grupos = Grupo.objects.exclude(horario_4='None')
        elif dia == '4':
          grupos = Grupo.objects.exclude(horario_5='None')
        elif dia == '5':
          grupos = Grupo.objects.exclude(horario_5='None')
  
        
        # filtrar_dia
        

        # Deshabilitar para que guarde.
        # forma.save()
        
        # Obtener los atributos que necesitamos.
        # antidoping_id = Antidoping.objects.latest('id')
        # seleccion_alumnos = forma.cleaned_data['seleccion_alumnos'].split(',')
        # seleccion_grupos = forma.cleaned_data['seleccion_grupos'].split(',')
        # tamano_muestra = int(tamano_muestra)

        return redirect('/success')  # Redirect after POST
    else:
        forma = CrearAntidoping() # An unbound form
        #forma2 = SeleccionMuestra() # An unbound form
    return render_to_response('home/seleccion_muestra.html', { 'forma': forma} , context_instance=RequestContext(request))