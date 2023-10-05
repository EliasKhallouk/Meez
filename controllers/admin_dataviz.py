#! /usr/bin/python
# -*- coding:utf-8 -*-
import os

from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db
import simplejson as json
import json

admin_dataviz = Blueprint('admin_dataviz', __name__,
                          template_folder='templates')


@admin_dataviz.route('/admin/dataviz/etat1')
def show_type_article_stock():
    mycursor = get_db().cursor()
    sql = '''SELECT departement.nom AS "nom",COUNT(round((adresse.code_postal)/1000)) AS "value"       
    FROM commande          
    RIGHT JOIN adresse ON commande.id_adresse_livraison=adresse.id_adresse          
    RIGHT OUTER JOIN departement ON departement.cp=round((adresse.code_postal)/1000,0) 
    GROUP BY round((adresse.code_postal)/1000);
    '''
    mycursor.execute(sql)
    datas_show = mycursor.fetchall()
    #print(datas_show)

    sql2='''SELECT COUNT(*) FROM commande; '''
    mycursor.execute(sql2)
    values = mycursor.fetchall()

    labels = None


    #print(os.getcwd())


    with open(os.getcwd()+'/static/json/population.json', 'w') as population:
        json.dump(datas_show, population)

    return render_template('admin/dataviz/dataviz_etat_1.html'
                           , datas_show=datas_show
                           , labels=labels
                           , values=values)
