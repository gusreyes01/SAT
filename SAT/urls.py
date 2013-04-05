from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'app.views.home', name='home'),
    # url(r'^SAT/', include('SAT.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),

     # Url exitoso
     url(r'^success/$', 'app.views.success', name='success_muestra'),
     
     # Urls para el manejo de estudiantes.
     url(r'^estudiante/$', 'app.views.estudiante', name='estudiante'),
     url(r'^alta_estudiante/$', 'app.views.alta_estudiante', name='alta_estudiante'),
     url(r'^edita_estudiante/(\d+)/$', 'app.views.edita_estudiante', name='edita_estudiante'),
     url(r'^perfil_estudiante/(\d+)/$', 'app.views.perfil_estudiante', name='perfil_estudiante'),
      
     # Urls para el manejo de muestras.
     url(r'^muestra/$', 'app.views.muestra', name='muestra'),
     url(r'^seleccion_muestra/$', 'app.views.seleccion_muestra', name='seleccion_muestra'),
     url(r'^perfil_muestra/(\d+)/$', 'app.views.perfil_muestra', name='perfil_muestra'),
     url(r'^alta_muestra/$', 'app.views.alta_muestra', name='alta_muestra'),
     url(r'^eliminar_muestra/(\d+)/$', 'app.views.eliminar_muestra', name='eliminar_muestra'),
     
     # Url para crear cartas de notificacion
     url(r'^carta_notificacion/(\d+)/$', 'app.views.obtener_carta', name='obtener_carta'),
     
     # Urls para iniciar y cerrar sesion.
     url(r'^accounts/login/$',  login),
     url(r'^accounts/logout/$',  logout),
)

# Add the static files pattern to the url.
urlpatterns += staticfiles_urlpatterns()
