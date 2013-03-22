# -*- coding: utf-8 -*
from app.models import *
from django import forms
from django.forms import ModelForm 
from crispy_forms.helper import FormHelper,reverse
from crispy_forms.layout import *

my_default_errors = {
    'required': 'Se requiere este campo.',
    'invalid': 'Este campo es invalido.'
}

ESTADO_INSTITUCION = (
    ('0','ACTIVO'),
    ('1','INACTIVO'),
)

COLOR = (
    ('0','GRIS'),
    ('1','VERDE'),
    ('2','AMARILLO'),
    ('3','NARANJA'),
    ('4','NARANJA'),
    ('5','NEGRO'),
)

class AltaEstudiante(ModelForm):
  matricula = forms.DecimalField(required = True,label="Matricula")
  nombre = forms.CharField(error_messages=my_default_errors,label="Nombre",required=True)
  apellido = forms.CharField(error_messages=my_default_errors,label="Apellido",required=True)
  correo = forms.CharField(error_messages=my_default_errors,label="Correo",required=True)
  telefono = forms.DecimalField(required = False,label="Telefono")
  celular = forms.DecimalField(required = False,label="Celular")
  color = forms.ChoiceField(error_messages=my_default_errors,choices=ESTADO_INSTITUCION)
  estado_institucion = forms.ChoiceField(error_messages=my_default_errors,choices=COLOR)
  
  class Meta:
    model = Estudiante
    exclude = ('padre','madre')
        
  def __init__(self, *args, **kwargs):
      self.helper = FormHelper()
      self.helper.form_id = 'id-AltaEstudiante'
      self.helper.form_class = 'blueForms'
      self.helper.form_method = 'POST'
      self.helper.form_action = 'alta_estudiante'
      self.helper.layout = Layout(
	Div(
	Div(
	    'matricula',
	    'nombre',
	    'apellido',
	    'correo',
	    'telefono',
	    'celular',
	    css_class='span3'),
	Div('color',
	    'estado_institucion',
	    css_class='span3'),css_class='row-fluid'),
	ButtonHolder(
	    Submit('submit', 'Crear', css_class='btn-success')
	))
      super(AltaEstudiante, self).__init__(*args, **kwargs)
  
class CrearAntidoping(ModelForm):
  nombre = forms.CharField(error_messages=my_default_errors,label="Crear Prueba",required=False)
  tamano_muestra = forms.DecimalField(required = False,label="Cuantos Alumnos")
  notas = forms.CharField(error_messages=my_default_errors,label="Notas",required=False)
  seleccion_alumnos = forms.CharField(widget=forms.Textarea,required = False)
  seleccion_grupos = forms.CharField(widget=forms.Textarea,required = False)
  
  class Meta:
    model = Antidoping
    exclude = ('muestra_inicio','muestra_fin','estudianteMuestra','estado_antidoping')
        
  def __init__(self, *args, **kwargs):
      self.helper = FormHelper()
      self.helper.form_id = 'id-CrearAntidoping'
      self.helper.form_class = 'blueForms'
      self.helper.form_method = 'POST'
      self.helper.form_action = 'seleccion_muestra'
      self.helper.layout = Layout(
	Div(
	Div(
	    'nombre',
	    'seleccion_alumnos',
	    css_class='span3'),
	Div(
	    'tamano_muestra',
	    css_class='span3'),
	Div(
	    'notas',
	    'seleccion_grupos',
	    css_class='span3'),css_class='row-fluid'),
	ButtonHolder(
	    Submit('submit', 'Crear', css_class='btn-success')
	))
      super(CrearAntidoping, self).__init__(*args, **kwargs)

#class EstudiantesMuestra(ModelForm):
  