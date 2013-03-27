
# Implementar cuando la hora es unicamente 10 y una clase comienza a las 10+.
def convierte_de_horario(horario_salon, delimitador, debug=True):
	import sys
	try:	
		# El horario puede venir de la siguiente forma: hora (arg0) (delimitador) salon (arg1).
		argumentos = horario_salon.split(delimitador)
		salon = argumentos[1]
		# hora_inicio = int(argumentos[0].replace('+', '').replace('/', ''))
		if debug:
			print argumentos
			# print hora_inicio

		# El horario tec puede ser de la siguiente forma 10+/3.
		horario_tec = argumentos[0]

		if '+' in horario_tec:
			if debug:
				print '+ :)'
			inicia_en_minuto = 30				# Comienza a mitad de hora.
	 	else:
	 		inicia_en_minuto = 0

	 	if debug:
		 	print horario_tec
	 	horario_tec = horario_tec.replace('+', '')

	 	# Quiere decir que la duracion se maneja en media horas.
	 	if '/' in horario_tec:
	 		if debug:
				print '/ :)'
			tiempo = horario_tec.split('/')
			hora_inicio = int(tiempo[0])
			duracion = int(tiempo[1]) * 30			# Duracion en minutos.
		else:
			hora_inicio = horario_tec
			duracion = 60


		# Convierte en diccionario.
		return {'hora_inicio': hora_inicio, 'inicia_en_minuto': inicia_en_minuto, 'duracion': duracion, 'salon': salon}

	except:
		if debug:
			print sys.exc_info()[0]
		return None

