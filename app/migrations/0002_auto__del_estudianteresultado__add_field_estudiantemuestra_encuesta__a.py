# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'EstudianteResultado'
        db.delete_table('app_estudianteresultado')

        # Adding field 'EstudianteMuestra.encuesta'
        db.add_column('app_estudiantemuestra', 'encuesta',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)

        # Adding field 'EstudianteMuestra.notificacion'
        db.add_column('app_estudiantemuestra', 'notificacion',
                      self.gf('django.db.models.fields.IntegerField')(max_length=255, null=True),
                      keep_default=False)

        # Adding field 'EstudianteMuestra.estado'
        db.add_column('app_estudiantemuestra', 'estado',
                      self.gf('django.db.models.fields.IntegerField')(max_length=255, null=True),
                      keep_default=False)

        # Adding field 'EstudianteMuestra.notas'
        db.add_column('app_estudiantemuestra', 'notas',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'EstudianteResultado'
        db.create_table('app_estudianteresultado', (
            ('encuesta', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('notificacion', self.gf('django.db.models.fields.IntegerField')(max_length=255)),
            ('antidoping', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Antidoping'])),
            ('notas', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('estado', self.gf('django.db.models.fields.IntegerField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('estudiante', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Estudiante'])),
        ))
        db.send_create_signal('app', ['EstudianteResultado'])

        # Deleting field 'EstudianteMuestra.encuesta'
        db.delete_column('app_estudiantemuestra', 'encuesta')

        # Deleting field 'EstudianteMuestra.notificacion'
        db.delete_column('app_estudiantemuestra', 'notificacion')

        # Deleting field 'EstudianteMuestra.estado'
        db.delete_column('app_estudiantemuestra', 'estado')

        # Deleting field 'EstudianteMuestra.notas'
        db.delete_column('app_estudiantemuestra', 'notas')


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
            'encuesta': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'estado': ('django.db.models.fields.IntegerField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inscrito': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Inscrito']"}),
            'notas': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'notificacion': ('django.db.models.fields.IntegerField', [], {'max_length': '255', 'null': 'True'})
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