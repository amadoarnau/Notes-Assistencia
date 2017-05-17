# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User


class Usuari(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    dni = models.CharField(max_length=9)
    def __str__(self):
        return self.username

class Room(models.Model):
    id_xml = models.CharField(max_length=200)
    nom = models.CharField(max_length=200)
    def __str__(self):
        return self.id_xml

class Classe(models.Model):
    id_xml = models.CharField(max_length=200)
    nom = models.CharField(max_length=200)
    class_room = models.CharField(max_length=200)
    def __str__(self):
        return self.id_xml

class Department(models.Model):
    nom = models.CharField(max_length=200)
    def __str__(self):
        return self.nom

class Professor(models.Model):
    professor_id_xml = models.CharField(max_length=200)
    nom = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    departament_professor = models.CharField(max_length=200)
    def __str__(self):
        return self.nom

class Llico(models.Model):
    id_xml = models.CharField(max_length=200)
    periods = models.CharField(max_length=200)
    periods = models.CharField(max_length=200)
    lesson_subject = models.CharField(max_length=200)
    lesson_teacher = models.CharField(max_length=200)
    teacher_value = models.CharField(max_length=200)
    effectivebegindate = models.CharField(max_length=200)
    effectiveenddate = models.CharField(max_length=200)
    assigned_day = models.CharField(max_length=200)
    assigned_period = models.CharField(max_length=200)
    assigned_starttime = models.CharField(max_length=200)
    assigned_endtime = models.CharField(max_length=200)
    def __str__(self):
        return self.id_xml

class Assignatura(models.Model):
    id_xml = models.CharField(max_length=200)
    nom = models.CharField(max_length=200)
    forecolor = models.CharField(max_length=200)
    backcolor = models.CharField(max_length=200)
    def __str__(self):
        return self.id_xml

class Modul(models.Model):
    nom = models.CharField(max_length=200)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    def __str__(self):
        return self.nom

class UF(models.Model):
    modul = models.ForeignKey(Modul, on_delete=models.CASCADE)
    nom = models.CharField(max_length=200)
    def __str__(self):
        return self.nom

class Nota(models.Model):
    usuari = models.ForeignKey(Usuari, on_delete=models.CASCADE)
    modul = models.ForeignKey(Modul, on_delete=models.CASCADE)
    uf = models.ForeignKey(UF, on_delete=models.CASCADE)
    nota = models.CharField(max_length=200)
    def __str__(self):
        return self.nota

class Alumne(models.Model):
    nomalumne = models.CharField(max_length=200)
    cognom = models.CharField(max_length=200)
    id_grup = models.CharField(max_length=200)
    codi = models.CharField(max_length=200)
    nom = models.CharField(max_length=200)
    etapa = models.CharField(max_length=200)
    subetapa = models.CharField(max_length=200)
    nivell = models.CharField(max_length=200)
    regim = models.CharField(max_length=200)
    id_alumne = models.CharField(max_length=200)
    def __str__(self):
        return self.nom

class Horari(models.Model):
    id_xml = models.CharField(max_length=200)
    day = models.CharField(max_length=200)
    period = models.CharField(max_length=200)
    starttime = models.CharField(max_length=200)
    endtime = models.CharField(max_length=200)
    def __str__(self):
        return self.id_xml


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipus = models.CharField(max_length=200)
    nomprofeshorari = models.CharField(max_length=200)

class Fitxatge(models.Model):
    id_ldap = models.CharField(max_length=200)
    origenlector = models.CharField(max_length=200)
    dia_hora = models.CharField(max_length=200)
    id_tarjeta = models.CharField(max_length=200)
    def __str__(self):
        return self.id_tarjeta

class Assistencia(models.Model):
    id_alumne = models.CharField(max_length=200)
    dia = models.CharField(max_length=200)
    hora = models.CharField(max_length=200)
    llico = models.CharField(max_length=200) 
    def __str__(self):
        return self.llico

class Llico_classe(models.Model):
    id_llico = models.CharField(max_length=200)
    id_classe = models.CharField(max_length=200)
    room = models.CharField(max_length=200) 
    def __str__(self):
        return self.id_llico


#        return (self.usuari self.modul  self.uf)