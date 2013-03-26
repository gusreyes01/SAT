# Create your views here.
# -*- coding: utf-8 -*
from app.forms import *
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
def estudiante(request):
    estudiantes = Estudiante.objects.all()  
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
   #+some code to check if New belongs to logged in user
   antidoping = Antidoping.objects.get(pk=id)
   
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
	  seleccion_alumnos = forma.cleaned_data['seleccion_alumnos']
	  seleccion_grupos = forma.cleaned_data['seleccion_grupos']
	  forma.save()
	  id_reciente = Antidoping.objects.latest('id')
	  return redirect('/success')  # Redirect after POST
    else:
        forma = CrearAntidoping() # An unbound form
        #forma2 = SeleccionMuestra() # An unbound form
    return render_to_response('home/seleccion_muestra.html', { 'forma': forma} , context_instance=RequestContext(request))