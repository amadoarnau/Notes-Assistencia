
import requests
import json
 
arraytot = []
array = {}
token = "8e645c89dca53418046b53a4124d1df5"
url = "http://etldap.duhowpi.net/webservice/rest/server.php?wstoken=" + token + ""
# afegir aixo si vols resposta json
url=url+"&moodlewsrestformat=json"
url=url+"&wsfunction=core_user_get_users_by_field"
 
# dades minimes per crear un curs
data = {
  #'wsfunction': 'core_user_get_users_by_field',
  "field" : 'idnumber',
  "values[0]" : '17179975059'
 
} 

#sprint(data)
 
r = requests.post(url, params=data, verify=False)
r= r.json()

url = "http://etldap.duhowpi.net/webservice/rest/server.php?wstoken=" + token + ""
# afegir aixo si vols resposta json
url=url+"&moodlewsrestformat=json"
url=url+"&wsfunction=core_enrol_get_users_courses"

data = {
  "userid" : r[0]['id']
} 
 
rs = requests.post(url, params=data, verify=False)
rs= rs.json()


#print(rs.json())

for l in rs:
  #print(l['id'])
  print("-----------------"+l['fullname']+"-----------------")

  url = "http://etldap.duhowpi.net/webservice/rest/server.php?wstoken=" + token + ""
  # afegir aixo si vols resposta json
  url=url+"&moodlewsrestformat=json"
  url=url+"&wsfunction=core_course_get_contents"

  data = {
    "courseid" : l['id']
  } 
   
  nomcurs = requests.post(url, params=data, verify=False)
  nomcurs= nomcurs.json()

  #print(nomcurs)

  for o in nomcurs:
    #print('\n\n\n')
    #print(o['modules'])
    modules = o['modules']
    for t in modules:
      #print('\n\n\n')
      #print(t['name'])
      array[t['id']] = t['name']




  url = "http://etldap.duhowpi.net/webservice/rest/server.php?wstoken=" + token + ""
  # afegir aixo si vols resposta json
  url=url+"&moodlewsrestformat=json"
  url=url+"&wsfunction=gradereport_user_get_grade_items"

  data = {
    "userid" : r[0]['id'],
    "courseid" : l['id']
    } 
       
  notes = requests.post(url, params=data, verify=False)
  notes= notes.json()
  notesss = notes['usergrades']

  for n in notesss:
    #print(n['gradeitems'])
    gradeitems = n['gradeitems']
    for note in gradeitems:

      if note['id'] in array:
        print(array[note['id']]+ " , " +note['percentageformatted'])
        arraytot.extend([[l['fullname'], array[note['id']], note['percentageformatted']]])
      else:
        print("Total --- " +note['percentageformatted'])
        arraytot.extend([[l['fullname'], "Total", note['percentageformatted']]])
  arraytot.extend([["----", "----", "----"]])


print(arraytot)


        
