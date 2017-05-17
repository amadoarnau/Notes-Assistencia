# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Usuari, Modul, UF, Nota, Classe, Alumne, Professor, Horari, Perfil

admin.site.register(Usuari)
admin.site.register(Modul)
admin.site.register(UF)
admin.site.register(Nota)
admin.site.register(Classe)
admin.site.register(Alumne)
admin.site.register(Professor)
admin.site.register(Perfil)
admin.site.register(Horari)