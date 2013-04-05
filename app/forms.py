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

SEMESTRE = (
    ('1', '1-3'),
    ('2', '4-6'),
    ('3', '7-8'),
    ('4', '9'),
)

CONSUMIDO = (
    ('1', 'Escuela'),
    ('2', 'Trabajo'),
    ('3', 'Fiesta'),
    ('4', 'Otros'),
)

FRECUENCIA = (
    ('1', '1 dia'),
    ('2', '4 dias'),
    ('3', '1 semana'),
    ('4', '1 mes'),
)

class AltaEstudiante(ModelForm):
  matricula = forms.DecimalField(required = True,label="Matricula")
  nombre = forms.CharField(error_messages=my_default_errors,label="Nombre",required=True)
  apellido = forms.CharField(error_messages=my_default_errors,label="Apellido",required=True)
  correo = forms.CharField(error_messages=my_default_errors,label="Correo",required=True)
  telefono = forms.CharField(required = False,label="Telefono")
  celular = forms.CharField(required = False,label="Celular")
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


class AplicacionEncuesta(ModelForm):
  if Encuesta.objects.all():
    fol_object = Encuesta.objects.all().order_by('id').reverse()[0]
    fol_all = fol_object.folio
    fol_sufix = fol_all[1:]
    fol_sufix_next = int(fol_sufix) + 1
    fol_next = 'e' + str(fol_sufix_next)
  else:
    fol_next = 'e1'
  
  folio = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), error_messages=my_default_errors, initial=fol_next, label="Folio", required=False)
  nombres = forms.CharField(error_messages=my_default_errors,label="Nombres",required=True)
  apellidos = forms.CharField(error_messages=my_default_errors,label="Apellidos",required=True)
  matricula = forms.DecimalField(required = True,label="Matricula")
  correo = forms.EmailField(error_messages=my_default_errors,label="Correo",required=True)
  semestre = forms.ChoiceField(widget=forms.RadioSelect(), choices=SEMESTRE, required = True, label="Semestre")
  #consumido = forms.ChoiceField(widget=forms.CheckboxSelectMultiple(), choices=CONSUMIDO, required = False, label="Consumido")
  opinion = forms.CharField(widget=forms.Textarea(), required = False,label="Opinion")
  frecuencia = forms.ChoiceField(error_messages=my_default_errors, choices=FRECUENCIA, required = True, label="Frecuencia")
  
  class Meta:
    model = Encuesta
    exclude = ('respuestas', 'notas')
        
  def __init__(self, *args, **kwargs):
      self.helper = FormHelper()
      self.helper.form_id = 'id-AplicacionEncuesta'
      self.helper.form_class = 'blueForms'
      self.helper.form_method = 'POST'
      self.helper.layout = Layout(
	Div(
	Div('folio',
	    'nombres',
	    'apellidos',
	    'matricula',
	    'correo',
	    'semestre',
	    css_class='span3'),
	Div(#'consumido',
	    'opinion',
	    'frecuencia',
	    css_class='span3'),css_class='row-fluid'),
	ButtonHolder(
	    Submit('submit', 'Crear', css_class='btn-success')
	))
      super(AplicacionEncuesta, self).__init__(*args, **kwargs)
