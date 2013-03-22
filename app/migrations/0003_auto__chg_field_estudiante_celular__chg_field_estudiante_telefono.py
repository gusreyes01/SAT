# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Estudiante.celular'
        db.alter_column('app_estudiante', 'celular', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Estudiante.telefono'
        db.alter_column('app_estudiante', 'telefono', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    def backwards(self, orm):

        # Changing field 'Estudiante.celular'
        db.alter_column('app_estudiante', 'celular', self.gf('django.db.models.fields.IntegerField')(max_length=255, null=True))

        # Changing field 'Estudiante.telefono'
        db.alter_column('app_estudiante', 'telefono', self.gf('django.db.models.fields.IntegerField')(max_length=255, null=True))

    models = {
        'app.antidoping': {
            'Meta': {'object_name': 'Antidoping'},
            'estado_antidoping': ('django.db.models.fields.IntegerField', [], {'max_length': '255', 'null': 'True'}),
            'estudianteMuestra': ('django.db.models.fields.IntegerField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'muestra_fin': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'max_length': '255'}),
            'muestra_inicio': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
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
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
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
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
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
            'cantidad_alumnos': ('django.db.models.fields.IntegerField', [], {'max_length': '255', 'null': 'True'}),
            'crn': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Clase']"}),
            'horario': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'profesor': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'salon': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'app.inscrito': {
            'Meta': {'object_name': 'Inscrito'},
            'estudiante': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Estudiante']"}),
            'grupo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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