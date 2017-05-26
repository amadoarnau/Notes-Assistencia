from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.index, name='home'),
    # ex: /check/guardarassistenci
    url(r'^guardarassistencia/$', views.guardarassistencia, name='guardarassistencia'),
    url(r'^llista_teves_classes/$', views.llista_teves_classes, name='llista_teves_classes'),
    url(r'^llicoclasse/$', views.llicoclasse, name='llicoclasse'),
    url(r'^nomprofessors/$', views.nomprofessors, name='nomprofessors'),
    url(r'^quies/$', views.quies, name='quies'),
    url(r'^passar_llista/$', views.passar_llista, name='passar_llista'),
    #url(r'^notes/$', views.notes, name='notes'),
    #url(r'^error/$', views.error, name='error'),
    url(r'^nom_horari_save/$', views.nom_horari_save, name='nom_horari_save'),
    url(r'^check/$', views.check, name='results'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^professors_llista/$', views.professors_llista, name='professors_llista'),
    url(r'^professors_llista_assistencia/$', views.professors_llista_assistencia, name='professors_llista_assistencia'),
    url(r'^alumnes_llista_assistencia/$', views.alumnes_llista_assistencia, name='alumnes_llista_assistencia'),
    url(r'^classes_llista/$', views.classes_llista, name='classes_llista'),
    url(r'^classes_llista_guardia/$', views.classes_llista_guardia, name='classes_llista_guardia'),
    url(r'^professors/$', views.professors, name='professors'),
    #url(r'^check/$', 'check', name='check'),
    # ex: /5/vote/
    url(r'^passar_llista/(?P<id_classe_passar_llista>[0-9]+)/$', views.passar_llista_classe, name='vote'),
    url(r'^passar_llista_classe/(?P<id_classe_passar_llista>\d+)/$', views.passar_llista_classe, name='vote'),
    url(r'^passar_llista_classe_guardia/(?P<nom_classe>\w+)/$', views.passar_llista_classe_guardia, name=''),
    url(r'^llista_alumnes/(?P<nom_classe>\w+)/$', views.llista_alumnes, name=''),
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^alumne/$', views.alumne, name='home'),
    url(r'^notes/$', views.notes, name='notes'),
    url(r'^faltes/$', views.faltes, name='faltes'),

]