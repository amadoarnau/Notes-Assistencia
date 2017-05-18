# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.db.models.signals import post_save
from django.core.signals import request_finished
from django.dispatch import receiver

from django.db import models

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

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
    return redirect('/assistencia')


    """Usuari_list = Usuari.objects.order_by('username')[:5]
    template = loader.get_template('admincenter/index.html')
    context = {
        'Usuari_list': Usuari_list,
    }
    return HttpResponse(template.render(context, request))"""

def vote(request, question_id):
    question = get_object_or_404(Question)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def nomprofessors(request):
    username = request.session['username']
    Usuari_list = Usuari.objects.order_by('username')[:5]
    llista_de_professors = Professor.objects.order_by('nom')
    template = loader.get_template('admincenter/nomprofessor.html')
    context = {
        'username': username,
        'llista_de_professors': llista_de_professors,
    }
    return HttpResponse(template.render(context, request))

def quies(request):
    if request.session.has_key('username'):
        username = request.session['username']
        Usuari = User.objects.filter(username=username).get()
        Usuari_list = User.objects.filter(username=username)
        perfil = Perfil.objects.filter(usuario_id=Usuari.id)

        con = ldap.initialize('ldap://127.0.0.1:389')
        #con = ldap.initialize('ldap://10.27.100.151:389')
        con.simple_bind_s("cn=admin,dc=ester,dc=cat", "P@ssw0rd")
        ldap_base = "dc=ester,dc=cat"
        query = "(uid="+username+")"
        result = con.search_s(ldap_base, ldap.SCOPE_SUBTREE, query)
        perfilusuari = Perfil.objects.filter(usuario_id=Usuari.id).get()

        #print(result)
        #print(result.seeAlso)
        #print(result['seeAlso'])

        for l in result:
            print(l[0])
            s = l[0]
            print("ou=Professors,ou=Users,dc=ester,dc=cat" in s)


            if "ou=Professors,ou=Users,dc=ester,dc=cat" in s:
                if perfilusuari.nomprofeshorari != "":
                    return redirect('/assistencia')
                else:
                    return redirect('/nomprofessors')
            else:
                return redirect('/notes')
                




            """if s.find("ou=Professors,ou=Users,dc=ester,dc=cat") == -1:
                print("Profe!")
            else:
                print("Nom profe.")"""
            

        """term = request.GET.get('term') # term => text sent from the page
        user_list = []uidNumber
        user_list = LDAPBackend().search(term) # search does not exist. I need to populate this array with all users that match the captured term.
        print(json.dumps(user_list))
        
       """


        if perfil:
            perfilusuari = Perfil.objects.filter(usuario_id=Usuari.id).get()
            print(perfilusuari.nomprofeshorari)
            #if perfilusuari.tipus == "profe": #temp
            if perfilusuari.tipus == "": #temp
                print("profe si")
                if perfilusuari.nomprofeshorari != "":
                    return redirect('/assistencia')
                else:
                    return redirect('/nomprofessors')
            elif perfilusuari.tipus == "notespares":
                return redirect('/notes')
            elif perfilusuari.tipus == "notesalumnes":
                return redirect('/notes')
            else:
                return redirect('/assistencia')

            
        else:
            
            Usuari_list = User.objects.filter(username=username)
            

            #Perfil.objects.create(usuario_id=Usuari.id, nomprofeshorari="", tipus="profe")

       
        return redirect('/assistencia')
    else:
        return redirect('/')

def assistencia(request):
    if request.session.has_key('username'):
        username = request.session['username']
        template = loader.get_template('admincenter/inici.html')
        context = {
            'username': username,
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
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def classes_llista(request):
    if request.session.has_key('username'):
        username = request.session['username']
        modul = Modul.objects.filter(professor_id=1)
        classes = Classe.objects.order_by('id')
        template = loader.get_template('admincenter/classes_llista.html')
        context = {
            'username': username,
            'classes': classes,
            'modul': modul,
        }
        print(modul)
        return HttpResponse(template.render(context, request))
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
                #print(lliconom)

                if not lliconom:
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
                        print(t.id_llico)
                        array.extend([t.id_classe])
                        num = num +1



            except:
                template = loader.get_template('admincenter/llicoassignar.php')
                context = {
                    'username': username,
                    'title': "Passar llista en el teu horari",
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
            'classes': array,
        }
        return HttpResponse(template.render(context, request))
        
    else:
        return redirect('/')

def passar_llista_classe(request, id_classe_passar_llista):
    if request.session.has_key('username'):

        Usuari = User.objects.filter(username=username).get()
        nomclasse = Classe.objects.filter(id=id_classe_passar_llista).get()
        alunesclasse = Alumne.objects.filter(classe_id=id_classe_passar_llista)

        username = request.session['username']
        template = loader.get_template('admincenter/alumnesclasse.html')
        context = {
            'username': username,
            'alunesclasse': alunesclasse,
            'nomclasse': nomclasse,
        }

        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def llicoclasse(request):

    username = request.session['username']
    Usuari = User.objects.filter(username=username).get()

    Llico_classe.objects.create(id_llico=request.GET['id_llico'], id_classe=request.GET['id_classe'], room="prova")

    return redirect('/assistencia')

def guardarassistencia(request):

    h = time.strftime("%H:%M:%S")
    data = time.strftime("%d/%m/%y")



    username = request.session['username']
    Usuari = User.objects.filter(username=username).get()
    #print(hora)

    Assistencia.objects.create(professor=username, id_alumne=request.GET['id_alumne'], llico=request.GET['nomllico'], valor=request.GET['assistencia'], dia=data, hora=h)

    return redirect('/assistencia')


def passar_llista(request):
    if request.session.has_key('username'):

        arrayalumnes = []
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
        llicoprofesors = Llico.objects.filter(lesson_teacher=perfilusuari.nomprofeshorari, assigned_starttime__lte=hm, assigned_endtime__gte=hm, assigned_day=diasetmana()).get()
        assig = Assignatura.objects.filter(id_xml=llicoprofesors.lesson_subject).get()
        try:
            #print("llicoprofesors.lesson_subject")
            #print(hm)
            #print(llicoprofesors.id_xml)
            classes = Classe.objects.order_by('id')
            lliconom = Llico_classe.objects.filter(id_llico=llicoprofesors.id_xml).get()

            classenom = lliconom.id_classe[3:len(lliconom.id_classe)]
            alunesclasse = Alumne.objects.filter(nom=classenom)





            con = ldap.initialize('ldap://127.0.0.1:389')
            #con = ldap.initialize('ldap://10.27.100.151:389')
            con.simple_bind_s("cn=admin,dc=ester,dc=cat", "P@ssw0rd")
            ldap_base = "dc=ester,dc=cat"
            query = "(cn="+classenom+")"
            result = con.search_s(ldap_base, ldap.SCOPE_SUBTREE, query)
            #print(result)

            for r in result:
                #print(r[1]["member"])
                print("\n\n\n\n\n\n\n")

                uid = r[1]["member"]
                #print(uid)
                for o in uid:
                    #print(o)
                    #o = o[4:15]
                    o = o[4:14]
                    #print(o)
                    con = ldap.initialize('ldap://127.0.0.1:389')
                    #con = ldap.initialize('ldap://10.27.100.151:389')
                    con.simple_bind_s("cn=admin,dc=ester,dc=cat", "P@ssw0rd")
                    ldap_base = "dc=ester,dc=cat"
                    query = "(uidNumber="+o+")"
                    resultnom = con.search_s(ldap_base, ldap.SCOPE_SUBTREE, query)
                    #print(resultnom)
                    for q in resultnom:
                        #print(q[1]["cn"])
                        q = q[1]["cn"]
                        #print(q[0])
                        q = q[0]

                        arrayalumnes.extend([[q, o]])
                




            #print(lliconom.id_llico)
            #print(lliconom.id_classe[3:len(lliconom.id_classe)])
            #print(lliconom.room)
            #print(assig.nom)
        except:
            template = loader.get_template('admincenter/llicoassignar.php')
            context = {
                'username': username,
                'title': "Passar llista en el teu horari",
                'classes': classes,
                'nomclasse': "Error / Hora d'esbarjo",
                'llico': llicoprofesors.id_xml,
            }
            return HttpResponse(template.render(context, request))

        print(arrayalumnes)
        template = loader.get_template('admincenter/passarllista.html')
        context = {
            'username': username,
            'title': "Passar llista en el teu horari",
            'alunesclasse': arrayalumnes,
            'nomclasse': assig.nom,
            'llico': llicoprofesors.id_xml,
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