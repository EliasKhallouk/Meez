#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']
    sql = '''SELECT date_achat,COUNT(*) AS nbr_articles, SUM(prix) AS prix_total ,commande.id_etat AS etat_id, etat.libelle, commande.id_commande 
     FROM commande 
     INNER JOIN ligne_commande
     ON commande.id_commande=ligne_commande.id_commande 
     INNER JOIN etat 
     ON commande.id_etat=etat.id_etat
     GROUP BY commande.id_commande 
     ORDER BY commande.id_etat ASC,date_achat DESC;'''

    mycursor.execute(sql)
    commandes = mycursor.fetchall()
    print("articles_commande",commandes)

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    print(id_commande)
    if id_commande != None:
        sql = ''' SELECT nom_modele as nom, quantite, mv.prix, sum(mv.prix * ligne_commande.quantite) as prix_ligne
            from ligne_commande
            INNER JOIN commande c2 on c2.id_commande = ligne_commande.id_commande
            INNER JOIN velo v on ligne_commande.id_velo = v.id_velo
            INNER JOIn modele_velo mv on v.id_modele = mv.id_modele
            WHERE c2.id_commande=%s
            GROUP BY v.id_velo;
            '''
        mycursor.execute(sql, (id_commande))
        articles_commande = mycursor.fetchall()
        
        sql='''SELECT id_adresse_livraison, id_adresse_facturation FROM commande WHERE id_commande=%s'''
        mycursor.execute(sql,(id_commande))
        adresses = mycursor.fetchone()

        sql = '''SELECT nom AS nom_livraison, rue AS rue_livraison, code_postal AS code_postal_livraison,ville AS ville_livraison 
        FROM adresse 
        WHERE id_adresse=%s;'''
        mycursor.execute(sql,adresses['id_adresse_livraison'])
        adresse_livraison = mycursor.fetchone()

        if adresses['id_adresse_livraison'] != adresses['id_adresse_facturation']:

            sql=''' SELECT nom AS nom_facturation, rue AS rue_facturation, code_postal AS code_postal_facturation,
            ville AS ville_facturation 
            FROM adresse
            WHERE id_adresse=%s;'''
            mycursor.execute(sql, adresses['id_adresse_facturation'])

            adresse_facturation = mycursor.fetchone()
            adresse_livraison.update(adresse_facturation)
            commande_adresses = adresse_livraison
        else:
            print ("adresse identique")
            commande_adresses = adresse_livraison
            commande_adresses['adresse_identique']='adresse_identique'

    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id != None:
        sql = '''UPDATE commande SET id_etat=2 WHERE id_commande=%s;'''
        mycursor.execute(sql, commande_id)
        get_db().commit()
    return redirect('/admin/commande/show')
