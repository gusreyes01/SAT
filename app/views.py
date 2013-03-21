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
def seleccion_muestra(request):
    if request.method == 'POST':
      # La forma ligada a los datos enviados en el POST
      forma = CrearAntidoping(request.POST)      
      forma2 = SeleccionMuestra(request.POST)     
      # Todas las reglas de validacion aprobadas
      if forma.is_valid():
	  forma.save()
	  return redirect('/home/') # Redirect after POST
    else:
        forma = CrearAntidoping() # An unbound form
        forma2 = SeleccionMuestra() # An unbound form
    return render_to_response('mhome/seleccion_muestra.html', { 'forma': forma,'forma2': forma2} , context_instance=RequestContext(request))