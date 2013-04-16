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

TIPO_SELECCION = (
    ('0','ALEATORIA'),
    ('1','DIRIGIDA'),
)

ESTADO_ANTIDOPING = (
    ('0','POSITIVO'),
    ('1','NEGATIVO'),
)

SEMESTRE = (
    ('1-3', '1° - 3°'),
    ('4-6', '4° - 6°'),
    ('7-8', '7° - 8°'),
    ('9', '9°'),
)

CONSUMIDO = (
    ('Escuela', 'Escuela'),
    ('Trabajo', 'Trabajo'),
    ('Fiesta', 'Fiesta'),
    ('Otros', 'Otros'),
)

FRECUENCIA = (
    ('1 dia', '1 dia'),
    ('4 dias', '4 dias'),
    ('1 semana', '1 semana'),
    ('1 mes', '1 mes'),
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
    ('lunes', 'Lunes'),
    ('martes', 'Martes'),
    ('miercoles', 'Miércoles'),
    ('jueves', 'Jueves'),
    ('viernes', 'Viernes'),
    ('sabado', 'Sábado'),
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
  nombre = forms.CharField(error_messages=my_default_errors,label="Nombre")
  tamano_muestra = forms.DecimalField(label="Tamaño de la muestra (máximo)")
  notas = forms.CharField(widget=forms.Textarea, error_messages=my_default_errors, label="Notas", required=False)
  seleccion_alumnos = forms.CharField(widget=forms.Textarea, required=False, label="Selección de alumnos")
  seleccion_grupos = forms.CharField(widget=forms.Textarea, required=False, label="Selección de grupos")
  dia = forms.ChoiceField(error_messages=my_default_errors,choices=DIA_SEMANA, label="Día")
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
      'tamano_muestra',
      'dia',
      'seleccion_alumnos',
	    css_class='span3'
      ),
	Div(
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

# Esta forma se encarga de evaluar el resultado estudiante para cada antidoping.

class EvaluaEstudiante(ModelForm):
  notificacion = forms.BooleanField(required=False)
  estado = forms.ChoiceField(error_messages=my_default_errors,choices=ESTADO_ANTIDOPING)
  tipo_seleccion = forms.ChoiceField(error_messages=my_default_errors,choices=TIPO_SELECCION)
  notas = forms.CharField(widget=forms.Textarea, error_messages=my_default_errors, label="Notas", required=False)

  class Meta:
    model = EstudianteMuestra
    exclude = ('folio','antidoping','inscrito','respuestas')
        
  def __init__(self, *args, **kwargs):
      self.helper = FormHelper()
      self.helper.form_id = 'id-EvaluaEstudiante'
      self.helper.form_class = 'blueForms'
      self.helper.form_method = 'POST'
      self.helper.form_action = ''
      self.helper.layout = Layout(
  Div(
  Div(
      'notificacion',
      'tipo_seleccion',
      'estado',
      'notas',

      css_class='span3'),css_class='row-fluid'),
  ButtonHolder(
      Submit('submit', 'Crear', css_class='btn-success')
  ))
      super(EvaluaEstudiante, self).__init__(*args, **kwargs)

class AplicacionEncuesta(ModelForm):
  folio = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), error_messages=my_default_errors, label="Folio", required=False)
  nombres = forms.CharField(error_messages=my_default_errors,label="Nombres",required=True)
  apellidos = forms.CharField(error_messages=my_default_errors,label="Apellidos",required=True)
  matricula = forms.DecimalField(required = True,label="Matricula")
  correo = forms.EmailField(error_messages=my_default_errors,label="Correo",required=True)
  semestre = forms.ChoiceField(widget=forms.RadioSelect(), choices=SEMESTRE, required = True, label="Semestre")
  #consumido = forms.ChoiceField(widget=forms.CheckboxSelectMultiple(), choices=CONSUMIDO, required = False, label="Consumido")
  opinion = forms.CharField(widget=forms.Textarea(), required = False,label="Opinion")
  frecuencia = forms.ChoiceField(error_messages=my_default_errors, choices=FRECUENCIA, required = True, label="Frecuencia")
  
  class Meta:
    model = EstudianteMuestra
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
	    Submit('submit', 'Enviar respuestas', css_class='btn-success')
	))
      super(AplicacionEncuesta, self).__init__(*args, **kwargs)

class EncuestaContestada(ModelForm):
  folio = forms.CharField(error_messages=my_default_errors, label="Folio", required=False)
  nombres = forms.CharField(error_messages=my_default_errors,label="Nombres",required=True)
  apellidos = forms.CharField(error_messages=my_default_errors,label="Apellidos",required=True)
  matricula = forms.DecimalField(required = True,label="Matricula")
  correo = forms.EmailField(error_messages=my_default_errors,label="Correo",required=True)
  semestre = forms.CharField(error_messages=my_default_errors,label="Semestre",required=True)
  #consumido = forms.ChoiceField(widget=forms.CheckboxSelectMultiple(), choices=CONSUMIDO, required = False, label="Consumido")
  opinion = forms.CharField(widget=forms.Textarea(), required = False,label="Opinion")
  frecuencia = forms.CharField(error_messages=my_default_errors,label="Frecuencia",required=True)
  notas = forms.CharField(widget=forms.Textarea(), required = False,label="Notas")
  
  class Meta:
    model = EstudianteMuestra
    exclude = ('id', 'folio', 'respuestas')
        
  def __init__(self, *args, **kwargs):
      self.helper = FormHelper()
      self.helper.form_id = 'id-EncuestaContestada'
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
	    'notas',
	    css_class='span3'),css_class='row-fluid'),
	ButtonHolder(
	    Submit('submit', 'Subir notas', css_class='btn-success')
	))
      super(EncuestaContestada, self).__init__(*args, **kwargs)
