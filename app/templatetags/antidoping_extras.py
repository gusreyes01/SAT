# -*- coding: utf-8 -*
from django import template
from app.models import *
import datetime

register = template.Library()

def horario(inscrito, dia):
    if dia == "lunes":
        return inscrito.grupo.horario_1
    elif dia == "martes":
        return inscrito.grupo.horario_2
    elif dia == "miercoles":
        return inscrito.grupo.horario_3
    elif dia == "jueves":
        return inscrito.grupo.horario_4
    elif dia == "viernes":
        return inscrito.grupo.horario_5
    elif dia == "sabado":
        return inscrito.grupo.horario_6 

def estado(estado_en_numero):
    # print estado_en_numero
    # print estado_en_numero == 0
    if estado_en_numero == 0:
        return 'Iniciado'
    elif estado_en_numero == 1:
        return '1era. Noticificación recibida'
    elif estado_en_numero == 2:
        return '2da. Noticificación recibida'
    elif estado_en_numero == 3:
        return 'Encuesta realizada'
    elif estado_en_numero == 4:
        return 'Prueba realizada'
    elif estado_en_numero == 5:
        return 'Cerrado'

def color(color_en_numero):
    if color_en_numero == 1:
        return '#8CBF26'  #VERDE
    elif color_en_numero == 2:
        return '#E8BE1B'  #AMARILLO
    elif color_en_numero == 3:
        return '#F09609'  #NARANJA
    elif color_en_numero == 4:
        return '#E51400'  #ROJO
    elif color_en_numero == 5:
        return '#000000'  #NEGRO
    else:
        return '#989898'

def color_texto(color_en_numero):
    if color_en_numero == 1:
        return 'Verde'  #VERDE
    elif color_en_numero == 2:
        return 'Amarillo'  #AMARILLO
    elif color_en_numero == 3:
        return 'Naranja'  #NARANJA
    elif color_en_numero == 4:
        return 'Rojo'  #ROJO
    elif color_en_numero == 5:
        return 'Negro'  #NEGRO
    else:
        return 'No encontrado'

def resultado(resultado_en_numero):
    if resultado_en_numero == 0:
        return 'Negativo' 
    elif resultado_en_numero == 1:
        return 'Positivo'
    else:
        return 'Pendiente'  

def contar_objetos(antidoping, estado):
    cantidad = 0
    if antidoping:
        cantidad = EstudianteMuestra.objects.filter(antidoping_id = antidoping.id).filter(estado = estado).count()
        return cantidad

def positivos(antidoping):
    cantidad = 0
    if antidoping:
        cantidad = EstudianteMuestra.objects.filter(antidoping_id = antidoping.id, resultado=1).count()
        return cantidad

def negativos(antidoping):
    cantidad = 0
    if antidoping:
        cantidad = EstudianteMuestra.objects.filter(antidoping_id = antidoping.id, resultado=0).count()
        return cantidad

def contar_total(objeto):
    cantidad = 0
    if objeto:
        cantidad = EstudianteMuestra.objects.filter(antidoping_id = objeto.id).count()
        return cantidad

register.filter('estado', estado)
register.filter('horario', horario)
register.filter('color', color)
register.filter('color_texto', color_texto)
register.filter('resultado', resultado)
register.filter('contar_objetos', contar_objetos)
register.filter('contar_total', contar_total)
register.filter('positivos', positivos)
register.filter('negativos', negativos)