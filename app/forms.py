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

class CrearAntidoping(ModelForm):
  nombre = forms.CharField(error_messages=my_default_errors,label="Crear Prueba")
  tamano_muestra = forms.DecimalField(required = False,label="Cuantos Alumnos")
  
  class Meta:
    model = Antidoping
    exclude = ('inicio','fin','estado_antidoping','notas')
        
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
	    css_class='span3'),
	Div(
	    'tamano_muestra',
	    css_class='span3'),css_class='row-fluid'),)
      super(CrearAntidoping, self).__init__(*args, **kwargs)
      
class SeleccionMuestra(forms.Form):
  seleccion_alumnos = forms.CharField(widget=forms.Textarea,required = False)
  seleccion_grupos = forms.CharField(widget=forms.Textarea,required = False)

  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_id = 'id-SeleccionMuestra'
    self.helper.form_class = 'blueForms'
    self.helper.form_method = 'POST'
    self.helper.form_action = 'seleccion_muestra'
    self.helper.layout = Layout(
	Div(
	Div(
	    'seleccion_alumnos',
	    css_class='span3'),
	Div(
	    'seleccion_grupos',
	    css_class='span3'),css_class='row-fluid'),
	ButtonHolder(
	    Submit('submit', 'Crear', css_class='btn-success')
	))
    super(SeleccionMuestra, self).__init__(*args, **kwargs)

#class EstudiantesMuestra(ModelForm):
  