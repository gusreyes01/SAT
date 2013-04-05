# Create your views here.
# -*- coding: utf-8 -*
from app.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.models import Encuesta

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
    return render_to_response('home/alta_estudiante.html', { 'forma': forma}, context_instance=RequestContext(request))
    
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
            seleccion_alumnos = forma.cleaned_data['seleccion_alumnos']
            seleccion_grupos = forma.cleaned_data['seleccion_grupos']
            forma.save()
            id_reciente = Antidoping.objects.latest('id')
            return redirect('/success')  # Redirect after POST
        else:
            forma = CrearAntidoping() # An unbound form
            #forma2 = SeleccionMuestra() # An unbound form
        return render_to_response('home/seleccion_muestra.html', { 'forma': forma} , context_instance=RequestContext(request))


@login_required
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
