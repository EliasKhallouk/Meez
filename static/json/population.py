#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db
import simplejson as json
import json

admin_dataviz = Blueprint('admin_dataviz', __name__,
                          template_folder='templates')


code_depart_fr = []
code_depart_client = []
values = []
for i in range(0,96):
    values.append(1)
#print(values)
#print(len(values))
for i in range(1, 96):
    code_depart_fr.append(str(i))
code_depart_fr[19] = '2A'
code_depart_fr.insert(20, '2B')
#print(len(code_depart_fr))

mycursor = get_db().cursor()
sql = '''SELECT departement.nom AS "nom",COUNT(round((adresse.code_postal)/1000)) AS "values"       
FROM commande          
RIGHT JOIN adresse ON commande.id_adresse_livraison=adresse.id_adresse          
RIGHT OUTER JOIN departement ON departement.cp=round((adresse.code_postal)/1000,0) 
GROUP BY round((adresse.code_postal)/1000);

'''
#SELECT code_postal FROM commande INNER JOIN adresse; GROUP BY round((adresse.code_postal)/1000);

mycursor.execute(sql)
datas_show = mycursor.fetchall()
#datas_show=json.dump("'",'"')
print(datas_show)

datas_show=json.dumps(datas_show)



 #for i in range(len(datas_show)):
  #  for j in datas_show[i]:
  #      print(j)
   #     type(j)

#print(datas_show)
#datas_show[i]=str.replace(datas_show[i].get("nom"),"'",'"')
#print(datas_show)
#print(code_depart_client)


for i in range(len(code_depart_client)):
    for j in range(len(code_depart_fr)):
            if code_depart_client[i] == code_depart_fr[j]:
                values[j]+=1
#print(values)

# labels = [str(row['libelle']) for row in datas_show]
# values = [int(row['nbr_articles']) for row in datas_show]
labels = None
# sql = '''
#
#        '''
with open('/home/userdepinfo/COURS/SAE/s2.3-4-5/SAE04-master-1/static/json/population.json', 'w') as population:
    json.dump(datas_show, population)
print(datas_show)

