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

DIA_SEMANA = (
    ('0', 'Lunes'),
    ('1', 'Martes'),
    ('2', 'Miércoles'),
    ('3', 'Jueves'),
    ('4', 'Viernes'),
    ('5', 'Sábado'),
  )

HORARIO = (
    ('7', '7:00'),
    ('7+', '7:30'),
    ('8', '8:00'),
    ('8+', '8:30'),
    ('9', '9:00'),
    ('9+', '9:30'),
    ('10', '10:00'),
    ('10+', '10:30'),
    ('11', '11:00'),
    ('11+', '11:30'),
    ('12', '12:00'),
    ('12+', '12:30'),
    ('13', '13:00'),
    ('13+', '13:30'),
    ('14', '14:00'),
    ('14+', '14:30'),
    ('15', '15:00'),
    ('15+', '15:30'),
    ('16', '16:00'),
    ('16+', '16:30'),
    ('17', '17:00'),
    ('17+', '17:30'),
    ('18', '18:00'),
    ('18+', '18:30'),
    ('19', '19:00'),
    ('19+', '19:30'),
    ('20', '20:00'),
    ('20+', '20:30'),
    ('21', '21:00'),
    ('21+', '21:30'),
    ('22', '22:00'),
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
  nombre = forms.CharField(error_messages=my_default_errors,label="Crear Prueba")
  tamano_muestra = forms.DecimalField(label="Cuantos Alumnos")
  notas = forms.CharField(error_messages=my_default_errors,label="Notas")
  seleccion_alumnos = forms.CharField(widget=forms.Textarea, required=False)
  seleccion_grupos = forms.CharField(widget=forms.Textarea, required=False)
  dia = forms.ChoiceField(error_messages=my_default_errors,choices=DIA_SEMANA)
  inicio = forms.ChoiceField(error_messages=my_default_errors,choices=HORARIO)
  fin = forms.ChoiceField(error_messages=my_default_errors,choices=HORARIO)
  
  class Meta:
    model = Antidoping
    exclude = ('muestra_inicio', 'antidoping_inicio', 'antidoping_fin', 'muestra_fin', 'estudianteMuestra', 'estado_antidoping')
        
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
	    css_class='span3'
      ),
	Div(
	    'tamano_muestra',
      'dia',
      'inicio',
      'fin',
	    css_class='span3'
      ),
	Div(
	    'notas',
	    'seleccion_grupos',
	    css_class='span3'),css_class='row-fluid'),
	ButtonHolder(
	    Submit('submit', 'Crear', css_class='btn-success')
	))
      super(CrearAntidoping, self).__init__(*args, **kwargs)

#class EstudiantesMuestra(ModelForm):
  