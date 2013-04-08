# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Padre'
        db.create_table('app_padre', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('apellido', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('correo', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('telefono', self.gf('django.db.models.fields.IntegerField')(max_length=255, null=True)),
            ('celular', self.gf('django.db.models.fields.IntegerField')(max_length=255, null=True)),
        ))
        db.send_create_signal('app', ['Padre'])

        # Adding model 'Estudiante'
        db.create_table('app_estudiante', (
            ('matricula', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('apellido', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('correo', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('celular', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('padre', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Padre N/D', null=True, to=orm['app.Padre'])),
            ('madre', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Madre N/D', null=True, to=orm['app.Padre'])),
            ('color', self.gf('django.db.models.fields.IntegerField')(max_length=255, null=True)),
            ('estado_institucion', self.gf('django.db.models.fields.IntegerField')(max_length=255, null=True)),
        ))
        db.send_create_signal('app', ['Estudiante'])

        # Adding model 'Clase'
        db.create_table('app_clase', (
            ('id', self.gf('django.db.models.fields.AutoField')(max_length=255, primary_key=True)),
            ('clave_materia', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('app', ['Clase'])

        # Adding model 'Grupo'
        db.create_table('app_grupo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('crn', self.gf('django.db.models.fields.IntegerField')(max_length=255)),
            ('clase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Clase'])),
            ('horario_1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('horario_2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('horario_3', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('horario_4', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('horario_5', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('profesor', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('app', ['Grupo'])

        # Adding model 'Inscrito'
        db.create_table('app_inscrito', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('estudiante', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Estudiante'])),
            ('grupo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Grupo'])),
        ))
        db.send_create_signal('app', ['Inscrito'])

        # Adding model 'Antidoping'
        db.create_table('app_antidoping', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('dia', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('muestra_inicio', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('muestra_fin', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('antidoping_inicio', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('antidoping_fin', self.gf('django.db.models.fields.DateField')(max_length=255, null=True)),
            ('tamano_muestra', self.gf('django.db.models.fields.IntegerField')(max_length=255, null=True)),
            ('estado_antidoping', self.gf('django.db.models.fields.IntegerField')(max_length=255, null=True)),
            ('notas', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('app', ['Antidoping'])

        # Adding model 'EstudianteMuestra'
        db.create_table('app_estudiantemuestra', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('inscrito', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Inscrito'])),
            ('antidoping', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Antidoping'])),
        ))
        db.send_create_signal('app', ['EstudianteMuestra'])

        # Adding model 'EstudianteResultado'
        db.create_table('app_estudianteresultado', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('antidoping', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Antidoping'])),
            ('estudiante', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Estudiante'])),
            ('encuesta', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('notificacion', self.gf('django.db.models.fields.IntegerField')(max_length=255)),
            ('estado', self.gf('django.db.models.fields.IntegerField')(max_length=255)),
            ('notas', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('app', ['EstudianteResultado'])

        # Adding model 'Encuesta'
        db.create_table('app_encuesta', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('folio', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('respuestas', self.gf('django.db.models.fields.TextField')()),
            ('notas', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
        ))
        db.send_create_signal('app', ['Encuesta'])


    def backwards(self, orm):
        # Deleting model 'Padre'
        db.delete_table('app_padre')

        # Deleting model 'Estudiante'
        db.delete_table('app_estudiante')

        # Deleting model 'Clase'
        db.delete_table('app_clase')

        # Deleting model 'Grupo'
        db.delete_table('app_grupo')

        # Deleting model 'Inscrito'
        db.delete_table('app_inscrito')

        # Deleting model 'Antidoping'
        db.delete_table('app_antidoping')

        # Deleting model 'EstudianteMuestra'
        db.delete_table('app_estudiantemuestra')

        # Deleting model 'EstudianteResultado'
        db.delete_table('app_estudianteresultado')

        # Deleting model 'Encuesta'
        db.delete_table('app_encuesta')


    models = {
        'app.antidoping': {
            'Meta': {'object_name': 'Antidoping'},
            'antidoping_fin': ('django.db.models.fields.DateField', [], {'max_length': '255', 'null': 'True'}),
            'antidoping_inicio': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'dia': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'estado_antidoping': ('django.db.models.fields.IntegerField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'muestra_fin': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'muestra_inicio': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notas': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tamano_muestra': ('django.db.models.fields.IntegerField', [], {'max_length': '255', 'null': 'True'})
        },
        'app.clase': {
            'Meta': {'object_name': 'Clase'},
            'clave_materia': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'max_length': '255', 'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'app.encuesta': {
            'Meta': {'object_name': 'Encuesta'},
            'folio': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notas': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'respuestas': ('django.db.models.fields.TextField', [], {})
        },
        'app.estudiante': {
            'Meta': {'object_name': 'Estudiante'},
            'apellido': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'celular': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'color': ('django.db.models.fields.IntegerField', [], {'max_length': '255', 'null': 'True'}),
            'correo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'estado_institucion': ('django.db.models.fields.IntegerField', [], {'max_length': '255', 'null': 'True'}),
            'madre': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Madre N/D'", 'null': 'True', 'to': "orm['app.Padre']"}),
            'matricula': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'padre': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Padre N/D'", 'null': 'True', 'to': "orm['app.Padre']"}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        'app.estudiantemuestra': {
            'Meta': {'object_name': 'EstudianteMuestra'},
            'antidoping': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Antidoping']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inscrito': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Inscrito']"})
        },
        'app.estudianteresultado': {
            'Meta': {'object_name': 'EstudianteResultado'},
            'antidoping': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Antidoping']"}),
            'encuesta': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'estado': ('django.db.models.fields.IntegerField', [], {'max_length': '255'}),
            'estudiante': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Estudiante']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'notas': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notificacion': ('django.db.models.fields.IntegerField', [], {'max_length': '255'})
        },
        'app.grupo': {
            'Meta': {'object_name': 'Grupo'},
            'clase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Clase']"}),
            'crn': ('django.db.models.fields.IntegerField', [], {'max_length': '255'}),
            'horario_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'horario_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'horario_3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'horario_4': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'horario_5': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profesor': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'app.inscrito': {
            'Meta': {'object_name': 'Inscrito'},
            'estudiante': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Estudiante']"}),
            'grupo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Grupo']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        'app.padre': {
            'Meta': {'object_name': 'Padre'},
            'apellido': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'celular': ('django.db.models.fields.IntegerField', [], {'max_length': '255', 'null': 'True'}),
            'correo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'telefono': ('django.db.models.fields.IntegerField', [], {'max_length': '255', 'null': 'True'})
        }
    }

    complete_apps = ['app']