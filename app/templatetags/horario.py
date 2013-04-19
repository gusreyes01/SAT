from django import template
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

register.filter('horario', horario)
