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
    ('0','Activo'),
    ('1','Inactivo'),
)

TIPO_SELECCION = (
    ('0','Aleatoria'),
    ('1','Dirigida'),
)

TIPO_DROGA = (
    ('0', 'Marihuana'),
    ('1', 'Cocaína'),
    ('2', 'Metanfetaminas | Anfetaminas'),
    ('3', 'Alucinógenos'),
    ('4', 'Opiáceos'),
    ('5', 'Otro'),
)

ESTADO_ANTIDOPING = (
    ('0','Iniciado'),
    ('1','1era. Notificación recibida'),
    ('2','2da. Notificación recibida'),
    ('3','Encuesta realizada'),
    ('4','Prueba realizada'),
    ('5','Cerrado'),
)

SI_NO = (
    ('0','Sí'),
    ('1','No'),
)

ALCOHOL_FRECUENCIA = (
    ('0','No consumo'),
    ('1','Una vez a la semana o menos'),
    ('2','Dos veces a la semana'),
    ('3','Más de dos veces por semana'),
)

TABACO_FRECUENCIA = (
    ('0','No consumo'),
    ('1','Menos de 5 cigarros al día'),
    ('2','De 5 a 10 cigarros al día'),
    ('3','De 10 cigarrillos a una cajetilla al día'),
    ('4','Más de una cajetilla al día'),
)

SI_NO_2 = (
    ('0','Sí'),
    ('1','No (Pasa a la pregunta 8)'),
)

QUIEN_OFRECIDO = (
    ('0','Un compañero de la escuela'),
    ('1','Un amigo'),
    ('2','Un vecino'),
    ('3','Un conocido'),
    ('4','Un familiar'),
    ('5','Otro'),
)

DONDE_OFRECIDO = (
    ('0','En un antro, bar, concierto o fiesta'),
    ('1','En un viaje al extranjero'),
    ('2','En casa de algún amigo o compañero'),
    ('3','En la escuela'),
    ('4','En la calle'),
    ('5','Otro'),
)

QUE_OFRECIDO_CONSUMIDO = (
    ('0','Marihuana'),
    ('1','Cocaína'),
    ('2','Anfetaminas, Metanfetaminas'),
    ('3','Alucinógenos'),
    ('4','Opiáceos'),
    ('5','Otro'),
)

SI_NO_3 = (
    ('0','Sí'),
    ('1','No (Pasa a la pregunta 13)'),
)

ULTIMO_CONSUMIDO = (
    ('0','En los últimos 30 días'),
    ('1','Hace más de un mes y menos de cinco meses'),
    ('2','Hace más de seis meses'),
)

QUIEN_OFRECIDO = (
    ('0','Un compañero de la escuela'),
    ('1','Un amigo'),
    ('2','Un vecino'),
    ('3','Un conocido'),
    ('4','Un familiar'),
    ('5','Otro'),
)

LUGAR_CONSUMIDO = (
    ('0','En un antro, bar, concierto o fiesta'),
    ('1','En un viaje al extranjero'),
    ('2','En casa de algún amigo o compañero'),
    ('3','En la escuela'),
    ('4','En la calle'),
    ('5','Otro'),
)

COLOR = (
    ('0','Gris'),
    ('1','Verde'),
    ('2','Amarillo'),
    ('3','Naranja'),
    ('4','Negro'),
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

RESULTADO_ANTIDOPING = (
    ('0', 'Negativo'),
    ('1', 'Positivo'),
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
  tipo_droga = forms.MultipleChoiceField(required = False, widget=forms.CheckboxSelectMultiple, choices=TIPO_DROGA)
  estado = forms.ChoiceField(required = False, error_messages=my_default_errors,choices=ESTADO_ANTIDOPING)
  tipo_seleccion = forms.ChoiceField(required = False, error_messages=my_default_errors,choices=TIPO_SELECCION)
  resultado = forms.ChoiceField(required = False, error_messages=my_default_errors,choices=RESULTADO_ANTIDOPING)
  notas = forms.CharField(required = False, widget=forms.Textarea, error_messages=my_default_errors, label="Notas")

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
      'tipo_droga',
      'tipo_seleccion',
      'estado',
      'resultado',
      'notas',

      css_class='span3'),css_class='row-fluid'),
  ButtonHolder(
      Submit('submit', 'Guardar', css_class='btn-success')
  ))
      super(EvaluaEstudiante, self).__init__(*args, **kwargs)

class AplicacionEncuesta(ModelForm):
  folio = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), error_messages=my_default_errors, label="Folio", required=False)
  medicamento_consumido = forms.ChoiceField(widget=forms.RadioSelect(), choices=SI_NO, label="1. ¿Actualmente consumes algún medicamento?",required=False)
  medicamento_consumido_paraque = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':40}), label="Si respondiste 'Sí', ¿cuál y para qué?", required = False)
  alcohol_frecuencia = forms.ChoiceField(widget=forms.RadioSelect(), choices=ALCOHOL_FRECUENCIA, label="2. ¿Con qué frecuencia consumes bebidas alcohólicas?",required=False)
  tabaco_frecuencia = forms.ChoiceField(widget=forms.RadioSelect(), choices=TABACO_FRECUENCIA, label="3. ¿Con qué frecuencia consumes cigarros de tabaco?",required=False)
  droga_ofrecido = forms.ChoiceField(widget=forms.RadioSelect(), choices=SI_NO_2, label="4. ¿Ten han ofrecido alguna vez alguna droga ilegal?",required=False)
  quien_ofrecido = forms.ChoiceField(widget=forms.RadioSelect(), choices=QUIEN_OFRECIDO, label="5. ¿Quién te ha ofrecido?",required=False)
  quien_ofrecido_otro = forms.CharField(widget=forms.TextInput(), label="Si responsite 'Otro' especifica quién", required=False)
  donde_ofrecido = forms.ChoiceField(widget=forms.RadioSelect(), choices=DONDE_OFRECIDO, label="6. ¿En dónde te han ofrecido?",required=False)
  donde_ofrecido_otro = forms.CharField(widget=forms.TextInput(), label="Si responsite 'Otro' especifica dónde", required=False)  
  que_ofrecido = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=QUE_OFRECIDO_CONSUMIDO, label="7. ¿Qué te ofrecieron? (Puedes seleccionar más de una opción)", required = False)
  que_ofrecido_otro = forms.CharField(widget=forms.TextInput(), label="Si responsite 'Otro' especifica qué", required=False)
  haz_consumido = forms.ChoiceField(widget=forms.RadioSelect(), choices=SI_NO_3, label="8. ¿Has consumido alguna vez alguna droga ilegal?",required=False)
  edad_consumido = forms.CharField(widget=forms.TextInput(), label="9. ¿A qué edad consumiste por primera vez?", required=False)
  que_consumido = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=QUE_OFRECIDO_CONSUMIDO, label="10. ¿Qué consumiste? (Puedes seleccionar más de una opción)", required = False)
  que_consumido_otro = forms.CharField(widget=forms.TextInput(), label="Si responsite 'Otro' especifica qué", required=False)
  ultimo_consumido = forms.ChoiceField(widget=forms.RadioSelect(), choices=ULTIMO_CONSUMIDO, label="11. ¿Cuándo fue tu último consumo? (Recuerda que adicionalmente a este cuestionario se te aplicará una prueba de dopaje)", required=False)
  que_consumido2 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=QUE_OFRECIDO_CONSUMIDO, label="12. ¿Qué consumiste? (Puedes seleccionar más de una opción)", required = False)
  que_consumido2_otro = forms.CharField(widget=forms.TextInput(), label="Si responsite 'Otro' especifica qué", required=False)
  conoces_consumidor = forms.ChoiceField(widget=forms.RadioSelect(), choices=SI_NO, label="13. ¿Conoces a alguien que consuma drogas ilegales?", required=False)
  de_donde = forms.ChoiceField(widget=forms.RadioSelect(), choices=QUIEN_OFRECIDO, label="14. Si respondiste afirmativamente a la pregunta anterior, indica de donde:", required=False)  
  de_donde_otro = forms.CharField(widget=forms.TextInput(), label="Si responsite 'Otro' especifica quién", required=False)
  lugar_consumo = forms.ChoiceField(widget=forms.RadioSelect(), choices=SI_NO, label="15. ¿Has estado en algún lugar donde a tu alrededor se consuman drogas ilegales?", required=False)
  lugar_consumo_donde = forms.ChoiceField(widget=forms.RadioSelect(), choices=LUGAR_CONSUMIDO, label="16. Si respondiste afirmativamente a la pregunta anterior, indica de donde:", required=False)  
  relaciones = forms.ChoiceField(widget=forms.RadioSelect(), choices=SI_NO, label="17. ¿Has tenido relaciones sexuales en los últimos 30 días?", required=False)
  class Meta:
    model = EstudianteMuestra
    exclude = ('resultado', 'antidoping', 'inscrito', 'tipo_seleccion', 'tipo_droga', 'estado','respuestas', 'notas')
        
  def __init__(self, *args, **kwargs):
      self.helper = FormHelper()
      self.helper.form_id = 'id-AplicacionEncuesta'
      self.helper.form_class = 'blueForms'
      self.helper.form_method = 'POST'
      self.helper.layout = Layout(
	Div(
	Div('folio',),
	Div('medicamento_consumido',
	    'medicamento_consumido_paraque',
	    'alcohol_frecuencia',
	    'tabaco_frecuencia',
	    'droga_ofrecido',
	    'quien_ofrecido',
	    'quien_ofrecido_otro',
	    'donde_ofrecido',
	    'donde_ofrecido_otro',
	    'que_ofrecido',
	    'que_ofrecido_otro',
	    'haz_consumido',
	    'edad_consumido',
	    css_class='span5'),
	Div('que_consumido',
	    'que_consumido_otro',
	    'ultimo_consumido',
	    'que_consumido2',
	    'que_consumido2_otro',
	    'conoces_consumidor',
	    'de_donde',
	    'de_donde_otro',
	    'lugar_consumo',
	    'lugar_consumo_donde',
	    'relaciones',
	    css_class='span5'),css_class='row-fluid'),
	ButtonHolder(
	    Submit('submit', 'Enviar respuestas', css_class='btn-success')
	))
      super(AplicacionEncuesta, self).__init__(*args, **kwargs)

class EncuestaContestada(ModelForm):
  folio = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), error_messages=my_default_errors, label="Folio", required=False)
  medicamento_consumido = forms.ChoiceField(widget=forms.RadioSelect(), choices=SI_NO, label="1. ¿Actualmente consumes algún medicamento?",required=False)
  medicamento_consumido_paraque = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':40}), label="Si respondiste 'Sí', ¿cuál y para qué?", required = False)
  alcohol_frecuencia = forms.ChoiceField(widget=forms.RadioSelect(), choices=ALCOHOL_FRECUENCIA, label="2. ¿Con qué frecuencia consumes bebidas alcohólicas?",required=False)
  tabaco_frecuencia = forms.ChoiceField(widget=forms.RadioSelect(), choices=TABACO_FRECUENCIA, label="3. ¿Con qué frecuencia consumes cigarros de tabaco?",required=False)
  droga_ofrecido = forms.ChoiceField(widget=forms.RadioSelect(), choices=SI_NO_2, label="4. ¿Ten han ofrecido alguna vez alguna droga ilegal?",required=False)
  quien_ofrecido = forms.ChoiceField(widget=forms.RadioSelect(), choices=QUIEN_OFRECIDO, label="5. ¿Quién te ha ofrecido?",required=False)
  quien_ofrecido_otro = forms.CharField(widget=forms.TextInput(), label="Si responsite 'Otro' especifica quién", required=False)
  donde_ofrecido = forms.ChoiceField(widget=forms.RadioSelect(), choices=DONDE_OFRECIDO, label="6. ¿En dónde te han ofrecido?",required=False)
  donde_ofrecido_otro = forms.CharField(widget=forms.TextInput(), label="Si responsite 'Otro' especifica dónde", required=False)  
  que_ofrecido = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=QUE_OFRECIDO_CONSUMIDO, label="7. ¿Qué te ofrecieron? (Puedes seleccionar más de una opción)", required = False)
  que_ofrecido_otro = forms.CharField(widget=forms.TextInput(), label="Si responsite 'Otro' especifica qué", required=False)
  haz_consumido = forms.ChoiceField(widget=forms.RadioSelect(), choices=SI_NO_3, label="8. ¿Has consumido alguna vez alguna droga ilegal?",required=False)
  edad_consumido = forms.CharField(widget=forms.TextInput(), label="9. ¿A qué edad consumiste por primera vez?", required=False)
  que_consumido = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=QUE_OFRECIDO_CONSUMIDO, label="10. ¿Qué consumiste? (Puedes seleccionar más de una opción)", required = False)
  que_consumido_otro = forms.CharField(widget=forms.TextInput(), label="Si responsite 'Otro' especifica qué", required=False)
  ultimo_consumido = forms.ChoiceField(widget=forms.RadioSelect(), choices=ULTIMO_CONSUMIDO, label="11. ¿Cuándo fue tu último consumo? (Recuerda que adicionalmente a este cuestionario se te aplicará una prueba de dopaje)", required=False)
  que_consumido2 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=QUE_OFRECIDO_CONSUMIDO, label="12. ¿Qué consumiste? (Puedes seleccionar más de una opción)", required = False)
  que_consumido2_otro = forms.CharField(widget=forms.TextInput(), label="Si responsite 'Otro' especifica qué", required=False)
  conoces_consumidor = forms.ChoiceField(widget=forms.RadioSelect(), choices=SI_NO, label="13. ¿Conoces a alguien que consuma drogas ilegales?", required=False)
  de_donde = forms.ChoiceField(widget=forms.RadioSelect(), choices=QUIEN_OFRECIDO, label="14. Si respondiste afirmativamente a la pregunta anterior, indica de donde:", required=False)  
  de_donde_otro = forms.CharField(widget=forms.TextInput(), label="Si responsite 'Otro' especifica quién", required=False)
  lugar_consumo = forms.ChoiceField(widget=forms.RadioSelect(), choices=SI_NO, label="15. ¿Has estado en algún lugar donde a tu alrededor se consuman drogas ilegales?", required=False)
  lugar_consumo_donde = forms.ChoiceField(widget=forms.RadioSelect(), choices=LUGAR_CONSUMIDO, label="16. Si respondiste afirmativamente a la pregunta anterior, indica de donde:", required=False)  
  relaciones = forms.ChoiceField(widget=forms.RadioSelect(), choices=SI_NO, label="17. ¿Has tenido relaciones sexuales en los últimos 30 días?", required=False)
  notas = forms.CharField(widget=forms.Textarea(), required = False,label="Notas")  
  class Meta:
    model = EstudianteMuestra
    exclude = ('resultado', 'antidoping', 'inscrito', 'tipo_seleccion', 'tipo_droga', 'estado','respuestas')
        
  def __init__(self, *args, **kwargs):
      self.helper = FormHelper()
      self.helper.form_id = 'id-EncuestaContestada'
      self.helper.form_class = 'blueForms'
      self.helper.form_method = 'POST'
      self.helper.layout = Layout(
	Div(
	Div('folio',),
	Div('medicamento_consumido',
	    'medicamento_consumido_paraque',
	    'alcohol_frecuencia',
	    'tabaco_frecuencia',
	    'droga_ofrecido',
	    'quien_ofrecido',
	    'quien_ofrecido_otro',
	    'donde_ofrecido',
	    'donde_ofrecido_otro',
	    'que_ofrecido',
	    'que_ofrecido_otro',
	    'haz_consumido',
	    'edad_consumido',
	    css_class='span5'),
	Div('que_consumido',
	    'que_consumido_otro',
	    'ultimo_consumido',
	    'que_consumido2',
	    'que_consumido2_otro',
	    'conoces_consumidor',
	    'de_donde',
	    'de_donde_otro',
	    'lugar_consumo',
	    'lugar_consumo_donde',
	    'relaciones',
	    'notas',
	    css_class='span5'),css_class='row-fluid'),
	ButtonHolder(
	    Submit('submit', 'Subir notas', css_class='btn-success')
	))
      super(EncuestaContestada, self).__init__(*args, **kwargs)

class UploadFileForm(forms.Form):
  file  = forms.FileField(label="CSV")

  def __init__(self, *args, **kwargs):
      self.helper = FormHelper()
      self.helper.form_id = 'id-UploadFileForm'
      self.helper.form_class = 'blueForms'
      self.helper.form_method = 'POST'
      self.helper.layout = Layout(
  Div(
  Div('file',
      css_class='span3'),css_class='row-fluid'),
  Div(
  ButtonHolder(
      Submit('submit', 'Subir', css_class='btn-success'), css_class='row-fluid')
  ))
      super(UploadFileForm, self).__init__(*args, **kwargs)
