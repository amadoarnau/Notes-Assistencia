# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models.signals import post_save
from django.core.signals import request_finished
from django.dispatch import receiver
from django.db import models
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Permission

from .models import Assistencia, Llico_classe, Fitxatge, Perfil, Horari, Alumne, Nota, UF, Modul, Assignatura, Llico, Professor, Department, Classe, Room, Usuari
import ldap
from django_auth_ldap.backend import LDAPBackend
import time


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        

        Perfil.objects.create(usuario=instance)

def save_user_profile(sender, instance, **kwargs):
    if not instance.is_superuser:  # add this, so I can login into django-admin
        instance.profile.save()

def index(request):
    Usuari_list = Usuari.objects.order_by('username')[:5]
    template = loader.get_template('admincenter/index.html')
    context = {
        'Usuari_list': Usuari_list,
        'title':"Login"
    }
    return HttpResponse(template.render(context, request))

def faltes(request):

    faltesprova = []
    username = request.session['username']
    query = "(uid="+username+")"
    result = conect(query)

    results = result[0]
    uid = results[0]

    textseparat = uid.split(",")
    text1 = textseparat[0]
    uidNumberusuari = text1.split("=")
    uidNumberusuari = uidNumberusuari[1]

    print(uidNumberusuari)

   
    #faltes = Assistencia.objects.filter(id_alumne=uidNumberusuari, valor__gte=2)
    faltes = Assistencia.objects.filter(id_alumne=uidNumberusuari, valor=3)

    #print(len(faltes))

    for x in faltes:

        llico = x.llico
        nommodul = Llico.objects.filter(id_xml= llico)
        for r in nommodul:
            print(r.lesson_subject)
            print("\n\n\n\n")
            modul = r.lesson_subject
            modul = modul[3:len(modul)]

        #nommodul = nommodul.lesson_subject

        llico = llico[0:3]

        if llico == "LS_":
            faltesprova.extend([[modul, x.dia, x.hora]])
        else:
            faltesprova.extend([["Guardia", x.dia, x.hora]])

        

    Usuari_list = Usuari.objects.order_by('username')[:5]
    template = loader.get_template('admincenter/faltesalumne.html')
    context = {
        'Usuari_list': Usuari_list,
        'username': username,
        'title':"Faltes de l'alumne",
        'faltes':faltes,
        'faltesprova':faltesprova
    }
    return HttpResponse(template.render(context, request))

def notes(request):
    
    import requests
    import json

    username = request.session['username']
    query = "(uid="+username+")"
    result = conect(query)

    results = result[0]
    uid = results[0]

    textseparat = uid.split(",")
    text1 = textseparat[0]
    uidNumberusuari = text1.split("=")
    uidNumberusuari = uidNumberusuari[1]
    #print(uidNumberusuari)

    """for x in results:
        print("\n\n\n")
        print(results[0])"""

    arraytot = []
    array = {}

    data = {
      "field" : 'idnumber',
      "values[0]" : uidNumberusuari
     
    } 
    retorn = conectmoodle("core_user_get_users_by_field", data)
    
    data = {
      "userid" : retorn[0]['id']
     
    } 
    rs = conectmoodle("core_enrol_get_users_courses", data)

    for l in rs:
      #print(l['id'])
      arraytot.extend([[l['fullname'], " ", " "]])
      #print("-----------------"+l['fullname']+"-----------------")

      data = {
        "courseid" : l['id']
      } 
             
      nomcurs= conectmoodle("core_course_get_contents", data)

      for o in nomcurs:
        modules = o['modules']
        for t in modules:
          array[t['id']] = t['name']


      data = {
        "userid" : retorn[0]['id'],
        "courseid" : l['id']
        } 
           
      notes= conectmoodle("gradereport_user_get_grade_items", data)
      notesss = notes['usergrades']

      for n in notesss:
        gradeitems = n['gradeitems']
        for note in gradeitems:

          if note['id'] in array:
            notesalumne = note['percentageformatted']
            notesalumne = notesalumne[0:len(notesalumne)-1]
            arraytot.extend([["", array[note['id']], notesalumne]])
          else:
            notesalumne = note['percentageformatted']
            notesalumne = notesalumne[0:len(notesalumne)-1]
            #arraytot.extend([["", "Total", notesalumne]])
      arraytot.extend([[" ", " ", " "]])


    
    template = loader.get_template('admincenter/notesalumne.html')
    context = {
        'username': username,
        'title':"Notes del alumne",
        'uidNumnber':"17179975059",
        'notes':arraytot
    }
    return HttpResponse(template.render(context, request))

def nom_horari_save(request):

    username = request.session['username']
    Usuari = User.objects.filter(username=username).get()
    """Perfils = get_object_or_404(Perfil, usuario_id=Usuari.id)
    selected_choice = Perfils.choice_set.get(usuario_id=Usuari.id)
    selected_choice.nomprofeshorari = "asdads"
    selected_choice.save()"""

    patient_edit = Perfil.objects.get(usuario_id=Usuari.id) # object to update
    patient_edit.nomprofeshorari = request.GET['nom_id'] # update name
    patient_edit.save() # save object
    return redirect('/professors')


    """Usuari_list = Usuari.objects.order_by('username')[:5]
    template = loader.get_template('admincenter/index.html')
    context = {
        'Usuari_list': Usuari_list,
    }
    return HttpResponse(template.render(context, request))"""



def nomprofessors(request):
    username = request.session['username']
    Usuari_list = Usuari.objects.order_by('username')[:5]
    llista_de_professors = Professor.objects.order_by('nom')
    template = loader.get_template('admincenter/nomprofessor.html')
    context = {
        'username': username,
        'llista_de_professors': llista_de_professors,
        'title': "Passar llista en el teu horari",
    }
    return HttpResponse(template.render(context, request))

def quies(request):
    if request.session.has_key('username'):
        username = request.session['username']
        Usuari = User.objects.filter(username=username).get()
        Usuari_list = User.objects.filter(username=username)
        perfil = Perfil.objects.filter(usuario_id=Usuari.id)

        query = "(uid="+username+")"
        result = conect(query)
        perfilusuari = Perfil.objects.filter(usuario_id=Usuari.id).get()

        for l in result:
            print(l[0])
            s = l[0]
            print("ou=Professors,ou=Users,dc=ester,dc=cat" in s)


            if "ou=Professors,ou=Users,dc=ester,dc=cat" in s:
                if perfilusuari.nomprofeshorari != "":
                    return redirect('/professors')
                else:
                    return redirect('/nomprofessors')
            else:
                return redirect('/alumne')
                

        if perfil:
            perfilusuari = Perfil.objects.filter(usuario_id=Usuari.id).get()
            print(perfilusuari.nomprofeshorari)
            #if perfilusuari.tipus == "profe": #temp
            if perfilusuari.tipus == "": #temp
                print("profe si")
                if perfilusuari.nomprofeshorari != "":
                    return redirect('/professors')
                else:
                    return redirect('/nomprofessors')
            elif perfilusuari.tipus == "notespares":
                return redirect('/notes')
            elif perfilusuari.tipus == "notesalumnes":
                return redirect('/notes')
            else:
                return redirect('/professors')

            
        else:
            
            Usuari_list = User.objects.filter(username=username)
            
       
        return redirect('/professors')
    else:
        return redirect('/')

def professors(request):
    if request.session.has_key('username'):
        username = request.session['username']
        template = loader.get_template('admincenter/inici.html')
        context = {
            'username': username,
            'title': "Menu gestio professors",
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def alumne(request):
    if request.session.has_key('username'):
        username = request.session['username']
        template = loader.get_template('admincenter/menualumne.html')
        context = {
            'username': username,
            'title': "Passar llista en el teu horari",
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def professors_llista(request):
    if request.session.has_key('username'):
        professor = Professor.objects.order_by('id')
        username = request.session['username']
        template = loader.get_template('admincenter/professors_llista.html')
        context = {
            'username': username,
            'professor': professor,
            'title': "Passar llista en el teu horari",
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def professors_llista_assistencia(request):
    if request.session.has_key('username'):
        username = request.session['username']
        template = loader.get_template('admincenter/inici.html')
        context = {
            'username': username,
            'title': "Passar llista en el teu horari",
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def alumnes_llista_assistencia(request):
    if request.session.has_key('username'):
        username = request.session['username']
        template = loader.get_template('admincenter/alumnes_llista_assistencia.html')
        context = {
            'username': username,
            'title': "Passar llista en el teu horari",
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def classes_llista_guardia(request):
    if request.session.has_key('username'):
        username = request.session['username']
        modul = Modul.objects.filter(professor_id=1)
        classes = Classe.objects.order_by('id')
        template = loader.get_template('admincenter/classes_llista_guardia.html')

        arrayalumnes = []
        

        for n in classes:
            #print(n)
            n = str(n)
            #print(len(n))
            n = n[3:len(n)]
            arrayalumnes.extend([n])

        context = {
            'username': username,
            'classes': arrayalumnes,
            'modul': modul,
            'title': "Llista de totes les classes del centre",
        }
        print(arrayalumnes)
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def classes_llista(request):
    if request.session.has_key('username'):
        username = request.session['username']
        Usuari = User.objects.filter(username=username).get()
        perfilusuari = Perfil.objects.filter(usuario_id=Usuari.id).get()
        llicoprofesors = Llico.objects.filter(lesson_teacher=perfilusuari.nomprofeshorari)

        array = []
        num = 0
        for i in llicoprofesors:
            #print(i)
            try:
                classes = Classe.objects.order_by('id')
                lliconom = Llico_classe.objects.filter(id_llico=i)
                #lliconom = Llico_classe.objects.all().distinct('id_classe')
                #lliconom = Llico_classe.objects.filter(id_llico=i).values_list('id_classe').distinct()
                
                for b in lliconom:
                    #print("\n\n")
                    #print(b.id_classe)
                    text = b.id_classe[3:len(b.id_classe)]
                    if not text in array:
                        array.extend([text])

                #rint(array)

                """if not lliconom:
                    template = loader.get_template('admincenter/llicoassignar.php')
                    context = {
                        'username': username,
                        'title': "Passar llista en el teu horari",
                        'classes': classes,
                        'nomclasse': "Error / Hora d'esbarjo",
                        'llico': i,
                    }
                    return HttpResponse(template.render(context, request))
                else:
                    for t in lliconom:
                        print(t.id_classe)
                        print(t.id_llico[3:len(t.id_llico)])
                        nomllico = t.id_llico[3:len(t.id_llico)]
                        array.extend([[t.id_classe, nomllico]])
                        num = num +1
"""


            except:
                arrayclasses = []
                for b in classes:
                    #print(b.id_xml)
                    text = b.id_xml
                    text = text[3:len(text)]
                    print(text)
                    arrayclasses.extend([[text]])
                template = loader.get_template('admincenter/llicoassignar.html')
                context = {
                    'username': username,
                    'title': "Assignar un classe a un horari",
                    'classes': classes,
                    'nomclasse': "Error / Hora d'esbarjo",
                    'llico': i,
                }
                return HttpResponse(template.render(context, request))
                #classes = Classe.objects.order_by('id')
                #lliconom = Llico_classe.objects.filter(id_llico=i).values('id_classe').distinct('id_classe')
                
                #print("\n\n")
                #print(lliconom)
        

        #print(array[0])
        print(array)
        template = loader.get_template('admincenter/classes_llista_assistencia.html')
        context = {
            'username': username,
            'classes': array,
            'title': "Llista de les teves classes",
        }
        return HttpResponse(template.render(context, request))


        """classes = Classe.objects.order_by('id')
        template = loader.get_template('admincenter/classes_llista_assistencia.html')
        context = {
            'username': username,
            'classes': classes,
        }
        print(classes)
        return HttpResponse(template.render(context, request))"""
    else:
        return redirect('/')

def llista_alumnes(request, nom_classe):
    if request.session.has_key('username'):
        username = request.session['username']
        arrayalumnes = []
        
        query = "(cn="+nom_classe+")"
        result = conect(query)

        for r in result:
            #print(r[1]["member"])
            #print("\n\n\n\n\n\n\n")

            uid = r[1]["member"]
            #print(uid[0])

            for o in uid:
                #print(o)
                #o = o[4:15]
                textseparat = o.split(",")
                text1 = textseparat[0]
                uidNumberusuari = text1.split("=")
                uidNumberusuari = uidNumberusuari[1]
                print(uidNumberusuari)
                
                query = "(uidNumber="+uidNumberusuari+")"
                resultnom = conect(query)
                print(query)
                print(resultnom)
                faltes = Assistencia.objects.filter(id_alumne=uidNumberusuari).count()

                if not resultnom:
                    arrayalumnes.extend([[uidNumberusuari, uidNumberusuari, faltes]])
                else:
                    for q in resultnom:
                        #print(q[1]["cn"])
                        q = q[1]["cn"]
                        #print(q[0])
                        q = q[0]
                        print(q)

                        arrayalumnes.extend([[q, uidNumberusuari, faltes]])



        """except:
            template = loader.get_template('admincenter/llicoassignar.php')
            context = {
                'username': username,
                'title': "Passar llista en el teu horari",
                'classes': classes,
                'nomclasse': "Error / Hora d'esbarjo",
                'llico': id_classe_passar_llista,
            }
            return HttpResponse(template.render(context, request))"""

        print(arrayalumnes)
        template = loader.get_template('admincenter/alumnes_llista_assistencia.html')
        context = {
            'username': username,
            'title': "Passar llista en el teu horari",
            'alunesclasse': arrayalumnes,
        }
        return HttpResponse(template.render(context, request))




        """username = request.session['username']
        modul = Modul.objects.filter(professor_id=1)
        classes = Classe.objects.order_by('id')
        template = loader.get_template('admincenter/classes_llista.html')
        context = {
            'username': username,
            'classes': classes,
            'modul': modul,
        }
        print(modul)
        return HttpResponse(template.render(context, request))"""
    else:
        return redirect('/')

def llista_teves_classes(request):
    if request.session.has_key('username'):

        classesdia = []

        hora = time.strftime("%I:%M:%S")
        hm = float(time.strftime("%H%M"))
        data = time.strftime("%d/%m/%y")

        hm = int(float(hm))
        hm = int(float(hm))
        #print(hm)
        #print(s)

        #print(diasetmana())

        username = request.session['username']
        Usuari = User.objects.filter(username=username).get()
        perfilusuari = Perfil.objects.filter(usuario_id=Usuari.id).get()
        llicoprofesors = Llico.objects.filter(lesson_teacher=perfilusuari.nomprofeshorari, assigned_day=diasetmana())
        #classesdia = llicoprofesors
        
        array = []
        num = 0
        for i in llicoprofesors:
            #print(i)
            try:
                classes = Classe.objects.order_by('id')
                lliconom = Llico_classe.objects.filter(id_llico=i)
                
                print("\n\n")
                print(i.lesson_subject)

                if not lliconom:
                    arrayclasses = []
                for b in classes:
                    #print(b.id_xml)
                    text = b.id_xml
                    text = text[3:len(text)]
                    print(text)
                    arrayclasses.extend([[text]])
                template = loader.get_template('admincenter/llicoassignar.html')
                    context = {
                        'username': username,
                        'title': "Assignar un classe a un horari",
                        'classes': classes,
                        'nomclasse': "Error / Hora d'esbarjo",
                        'llico': i,
                    }
                    return HttpResponse(template.render(context, request))
                else:
                    for t in lliconom:
                        print(t.id_classe)
                        print(t.id_classe)
                        print(t.id_llico[3:len(t.id_llico)])
                        nomllico = t.id_llico[3:len(t.id_llico)]

                        nomclasses = t.id_classe[3:len(t.id_classe)]
                        subject = i.lesson_subject[3:len(i.lesson_subject)]

                        array.extend([[nomclasses, nomllico, subject]])
                        num = num +1



            except:
                arrayclasses = []
                for b in classes:
                    #print(b.id_xml)
                    text = b.id_xml
                    text = text[3:len(text)]
                    print(text)
                    arrayclasses.extend([[text]])
                template = loader.get_template('admincenter/llicoassignar.html')
                context = {
                    'username': username,
                    'title': "Assignar un classe a un horari",
                    'classes': classes,
                    'nomclasse': "Error / Hora d'esbarjo",
                    'llico': i,
                }
                return HttpResponse(template.render(context, request))
        

        print(array[0])
        print(array)
        template = loader.get_template('admincenter/classes_llista.html')
        context = {
            'username': username,
            'title': "Llista de les classes del teu horari d'avui",
            'classes': array,
        }
        return HttpResponse(template.render(context, request))
        
    else:
        return redirect('/')

def passar_llista_classe(request, id_classe_passar_llista):
    if request.session.has_key('username'):
        arrayalumnes = []

        username = request.session['username']
        id_classe_passar_llista = "LS_"+id_classe_passar_llista
        print(id_classe_passar_llista)

        llicoprofesors = Llico.objects.filter(id_xml=id_classe_passar_llista)
        for p in llicoprofesors:
            print(p.lesson_subject)
        assig = Assignatura.objects.filter(id_xml=p.lesson_subject).get()

        #try:
        classenom = Llico_classe.objects.filter(id_llico=id_classe_passar_llista).get()
        print(classenom.id_classe)
        classenom = classenom.id_classe[3:len(classenom.id_classe)]
        print(classenom)
        classes = Classe.objects.order_by('id')
        query = "(cn="+classenom+")"
        result = conect(query)
        #print(result)

        for r in result:
            #print(r[1]["member"])
            print("\n\n\n\n\n\n\n")

            uid = r[1]["member"]
            #print(uid)
            for o in uid:
                #print(o)
                #o = o[4:15]
                textseparat = o.split(",")
                text1 = textseparat[0]
                uidNumberusuari = text1.split("=")
                uidNumberusuari = uidNumberusuari[1]
                print(uidNumberusuari)
                
                query = "(uidNumber="+uidNumberusuari+")"
                resultnom = conect(query)
                
                print(query)
                print(resultnom)
                if not resultnom:
                    arrayalumnes.extend([[uidNumberusuari, uidNumberusuari]])
                else:
                    for q in resultnom:
                        #print(q[1]["cn"])
                        q = q[1]["cn"]
                        #print(q[0])
                        q = q[0]
                        print(q)

                        arrayalumnes.extend([[q,uidNumberusuari]])
        """except:
            template = loader.get_template('admincenter/llicoassignar.php')
            context = {
                'username': username,
                'title': "Passar llista en el teu horari",
                'classes': classes,
                'nomclasse': "Error / Hora d'esbarjo",
                'llico': id_classe_passar_llista,
            }
            return HttpResponse(template.render(context, request))"""

        print(arrayalumnes)
        template = loader.get_template('admincenter/passarllista.html')
        context = {
            'username': username,
            'title': "Passar llista en el teu horari",
            'alunesclasse': arrayalumnes,
            'nomclasse': assig.nom,
            'llico': id_classe_passar_llista,
            'text': "Nom",
        }
        return HttpResponse(template.render(context, request))

        """
        Usuari = User.objects.filter(username=username).get()
        nomclasse = Classe.objects.filter(id=id_classe_passar_llista).get()
        alunesclasse = Alumne.objects.filter(classe_id=id_classe_passar_llista)"""



        """username = request.session['username']
        template = loader.get_template('admincenter/alumnesclasse.html')
        context = {
            'username': username,
            'alunesclasse': alunesclasse,
            'nomclasse': nomclasse,
        }"""
        """template = loader.get_template('admincenter/passarllista.html')
        context = {
            'username': username,
            'title': "Passar llista",
            'alunesclasse': arrayalumnes,
            'nomclasse': assig.nom,
            'llico': llicoprofesors.id_xml,
        }"""

        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def passar_llista_classe_guardias(request, nom_classe):
    print(nom_classe)

def passar_llista_classe_guardia(request, nom_classe):
    if request.session.has_key('username'):
        arrayalumnes = []

        username = request.session['username']
        """id_classe_passar_llista = "LS_"+passar_llista_classe_guardia    
        print(id_classe_passar_llista)

        llicoprofesors = Llico.objects.filter(id_xml=id_classe_passar_llista)
        for p in llicoprofesors:
            print(p.lesson_subject)
        assig = Assignatura.objects.filter(id_xml=p.lesson_subject).get()

        #try:
        classenom = Llico_classe.objects.filter(id_llico=id_classe_passar_llista).get()
        print(classenom.id_classe)
        classenom = classenom.id_classe[3:len(classenom.id_classe)]"""
        classenom = nom_classe
        print(classenom)
        classes = Classe.objects.order_by('id')
        
        query = "(cn="+classenom+")"
        result = conect(query)
        print(result)

        for r in result:
            #print(r[1]["member"])
            print("\n\n\n\n\n\n\n")

            uid = r[1]["member"]
            #print(uid)
            for o in uid:
                #print(o)
                #o = o[4:15]
                textseparat = o.split(",")
                text1 = textseparat[0]
                uidNumberusuari = text1.split("=")
                uidNumberusuari = uidNumberusuari[1]
                print(uidNumberusuari)
                
                query = "(uidNumber="+uidNumberusuari+")"
                resultnom = conect(query)
                
                print(query)
                print(resultnom)
                if not resultnom:
                    d = time.strftime("%y-%m-%d")
                    fitxa = Fitxatge.objects.filter(id_ldap=uidNumberusuari, dia_hora__contains = d)

                    if fitxa:
                        #print(fitxa)
                        arrayalumnes.extend([[q, uidNumberusuari, "Si"]])
                    else:
                        #print("no")
                        arrayalumnes.extend([[uidNumberusuari, uidNumberusuari, ""]])
                        #arrayalumnes.extend([[uidNumberusuari, uidNumberusuari]])
                else:
                    for q in resultnom:
                        #print(q[1]["cn"])
                        q = q[1]["cn"]
                        #print(q[0])
                        q = q[0]
                        print(q)

                        #arrayalumnes.extend([[q, uidNumberusuari]])
                        d = time.strftime("%y-%m-%d")

                        fitxa = Fitxatge.objects.filter(id_ldap=uidNumberusuari, dia_hora__contains = d)

                        if fitxa:
                            print(fitxa)
                            arrayalumnes.extend([[q, uidNumberusuari, "Si"]])
                        else:
                            arrayalumnes.extend([[q, uidNumberusuari, ""]])
                        #print(resultnom)

                

                
        """except:
            template = loader.get_template('admincenter/llicoassignar.php')
            context = {
                'username': username,
                'title': "Passar llista en el teu horari",
                'classes': classes,
                'nomclasse': "Error / Hora d'esbarjo",
                'llico': id_classe_passar_llista,
            }
            return HttpResponse(template.render(context, request))"""

        print(arrayalumnes)
        template = loader.get_template('admincenter/passarllista.html')
        context = {
            'username': username,
            'title': "Passar llista en el teu horari",
            'alunesclasse': arrayalumnes,
            #'nomclasse': assig.nom,
            'llico': nom_classe,
            'text': "Nom",
        }
        return HttpResponse(template.render(context, request))


        #return HttpResponse(template.render(context, request))
    else:
        return redirect('/')


def llicoclasse(request):

    username = request.session['username']
    Usuari = User.objects.filter(username=username).get()

    Llico_classe.objects.create(id_llico=request.GET['id_llico'], id_classe=request.GET['id_classe'], room="prova")

    return redirect('/professors')

def guardarassistencia(request):

    h = time.strftime("%H:%M:%S")
    data = time.strftime("%d/%m/%y")



    username = request.session['username']
    Usuari = User.objects.filter(username=username).get()
    #print(hora)

    Assistencia.objects.create(professor=username, id_alumne=request.GET['id_alumne'], llico=request.GET['nomllico'], valor=request.GET['assistencia'], dia=data, hora=h)

    return redirect('/professors')


def passar_llista(request):
    if request.session.has_key('username'):

        arrayalumnes = []
        hora = time.strftime("%I:%M:%S")
        hm = float(time.strftime("%H%M"))
        data = time.strftime("%d/%m/%y")

        hm = int(float(hm))
        #hm = 1630


        username = request.session['username']
        Usuari = User.objects.filter(username=username).get()
        perfilusuari = Perfil.objects.filter(usuario_id=Usuari.id).get()

      
        llicoprofesors = None
        print(filtre(perfilusuari, hm))
       
        if filtre(perfilusuari, hm):
            llicoprofesors = Llico.objects.filter(lesson_teacher=perfilusuari.nomprofeshorari, assigned_starttime__lte=hm, assigned_endtime__gte=hm, assigned_day=diasetmana()).get()
        else:
            template = loader.get_template('admincenter/passarllista.html')
            context = {
                'username': username,
                'title': "No tens classe",
                'nomclasse': "No tens classe",
                'text': "No tens classe",
            }
            return HttpResponse(template.render(context, request))
            print(llicoprofesors)
        print("\n\n\n\n\n\n\n\n\n")

        assig = Assignatura.objects.filter(id_xml=llicoprofesors.lesson_subject).get()
        try:
            classes = Classe.objects.order_by('id')
            lliconom = Llico_classe.objects.filter(id_llico=llicoprofesors.id_xml).get()

            classenom = lliconom.id_classe[3:len(lliconom.id_classe)]
            alunesclasse = Alumne.objects.filter(nom=classenom)

            
            query = "(cn="+classenom+")"
            result = conect(query)

            for r in result:
                #print(r[1]["member"])
                #print("\n\n\n\n\n\n\n")

                uid = r[1]["member"]
                #print(uid)
                for o in uid:
                    #print(o)
                    #o = o[4:15]
                    textseparat = o.split(",")
                    text1 = textseparat[0]
                    uidNumberusuari = text1.split("=")
                    uidNumberusuari = uidNumberusuari[1]
                    #print(uidNumberusuari)
                    
                    query = "(uidNumber="+uidNumberusuari+")"
                    resultnom = conect(query)

                    #print(query)
                    #print(resultnom)
                    if not resultnom:

                        #arrayalumnes.extend([[uidNumberusuari, uidNumberusuari, "si temp"]])

                        d = time.strftime("%y-%m-%d")
                        fitxa = Fitxatge.objects.filter(id_ldap=uidNumberusuari, dia_hora__contains = d)

                        if fitxa:
                            #print(fitxa)
                            arrayalumnes.extend([[q, uidNumberusuari, "Si"]])
                        else:
                            #print("no")
                            arrayalumnes.extend([[uidNumberusuari, uidNumberusuari, ""]])

                    else:
                        for q in resultnom:
                            #print(q[1]["cn"])
                            q = q[1]["cn"]
                            #print(q[0])
                            q = q[0]
                            #print(q)
                            #print(uidNumberusuari)

                            d = time.strftime("%y-%m-%d")

                            fitxa = Fitxatge.objects.filter(id_ldap=uidNumberusuari, dia_hora__contains = d)

                            if fitxa:
                                print(fitxa)
                                arrayalumnes.extend([[q, uidNumberusuari, "Si"]])
                            else:
                                arrayalumnes.extend([[q, uidNumberusuari, ""]])

                




            #print(lliconom.id_llico)
            #print(lliconom.id_classe[3:len(lliconom.id_classe)])
            #print(lliconom.room)
            #print(assig.nom)
            
        except:
            arrayclasses = []
            for b in classes:
                #print(b.id_xml)
                text = b.id_xml
                text = text[3:len(text)]
                print(text)
                arrayclasses.extend([[text]])
            template = loader.get_template('admincenter/llicoassignar.html')
            context = {
                'username': username,
                'title': "Passar llista en el teu horari",
                'classes': arrayclasses,
                'nomclasse': "Error / Hora d'esbarjo",
                'llico': llicoprofesors.id_xml,
            }
            return HttpResponse(template.render(context, request))

        #print("\n\n\n")
        #print(arrayalumnes)
        template = loader.get_template('admincenter/passarllista.html')
        context = {
            'username': username,
            'title': "Passar llista en el teu horari",
            'alunesclasse': arrayalumnes,
            'nomclasse': assig.nom,
            'llico': llicoprofesors.id_xml,
            'text': "Nom",
        }
        return HttpResponse(template.render(context, request))
        
    else:
        return redirect('/')
    
def logout(request):
   try:
      del request.session['username']
   except:
      pass
   return redirect('/')

def check(request): 
    #print(request.GET['password'])

    #try:
        user = authenticate(username=request.GET['username'], password=request.GET['password'])
        if user is not None:
            request.session['username'] = request.GET['username']
            return redirect('/quies',request)

        # A backend authenticated the credentials
        else:
            #return HttpResponse("No")
            return redirect('/')
    #except NameError:
     #   return HttpResponse("Error")
def diasetmana(): 
    import datetime
    x = datetime.datetime.now()
    dicdias = {'MONDAY':'1','TUESDAY':'2','WEDNESDAY':'3','THURSDAY':'4','FRIDAY':'5','SATURDAY':'6','SUNDAY':'7'}
    anho = x.year
    mes =  x.month
    dia= x.day
         
    fecha = datetime.date(anho, mes, dia)
    return dicdias[fecha.strftime('%A').upper()] 

def conect(query):
    #con = ldap.initialize('ldap://etldap.duhowpi.net:389')
    #con = ldap.initialize('ldap://127.0.0.1:389')
    con = ldap.initialize('ldap://10.27.100.151:389')
    con.simple_bind_s("cn=admin,dc=ester,dc=cat", "P@ssw0rd")
    ldap_base = "dc=ester,dc=cat"
    result = con.search_s(ldap_base, ldap.SCOPE_SUBTREE, query)

    #print(result)
    return result

def conectmoodle(frase, data):
    import requests
    import json

    token = "8e645c89dca53418046b53a4124d1df5"
    url = "http://etldap.duhowpi.net/webservice/rest/server.php?wstoken=" + token + ""
    url=url+"&moodlewsrestformat=json"
    url=url+"&wsfunction=" + frase + ""
     
    result = requests.post(url, params=data, verify=False)
    result= result.json()

    return result

def filtre(perfilusuari, hm):
    try:
        llicoprofesors = Llico.objects.filter(lesson_teacher=perfilusuari.nomprofeshorari, assigned_starttime__lte=hm, assigned_endtime__gte=hm, assigned_day=diasetmana()).get()
        return True
    except:
        return False