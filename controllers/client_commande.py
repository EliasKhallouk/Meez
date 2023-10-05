#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''SELECT ligne_panier.quantite as quantite, modele_velo.prix as prix, modele_velo.nom_modele as nom , couleur.nom_couleur as couleur , taille.libelle as taille , velo.stock as stock , velo.id_velo as id_velo 
                FROM ligne_panier
                INNER JOIN velo ON velo.id_velo = ligne_panier.id_velo
                INNER JOIN modele_velo ON velo.id_modele = modele_velo.id_modele
                INNER JOIN couleur ON velo.id_couleur = couleur.id_couleur
                INNER JOIN taille ON velo.id_taille = taille.id_taille
                WHERE ligne_panier.id_utilisateur = %s;
                '''
    mycursor.execute(sql, (id_client))
    articles_panier = mycursor.fetchall()

    if len(articles_panier) >= 1:
        sql = ''' SELECT SUM(ligne_panier.quantite * modele_velo.prix) AS prix_total FROM ligne_panier 
                    INNER JOIN velo ON velo.id_velo = ligne_panier.id_velo
                    INNER JOIN modele_velo ON velo.id_modele = modele_velo.id_modele
                    '''
        mycursor.execute(sql)
        prix_total = mycursor.fetchone()['prix_total']

    else:
        prix_total = None

    # etape 2 : selection des adresses
    sql = '''select adresse.id_adresse,commande.date_achat,adresse.code_postal,adresse.rue,adresse.ville from adresse LEFT JOIN commande ON adresse.id_adresse=commande.id_adresse_livraison where adresse.id_utilisateur=%s ORDER BY date_achat DESC;'''
    mycursor.execute(sql, id_client)
    adresses = mycursor.fetchall()

    return render_template('client/boutique/panier_validation_adresses.html'
                           , adresses=adresses
                           , articles_panier=articles_panier
                           , prix_total=prix_total
                           , validation=1
                           )

@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    adresse_livraison = request.form.get('id_adresse_livraison')
    adresse_identique = request.form.get('adresse_identique')
    adresse_facturation = request.form.get('id_adresse_facturation')

    if adresse_identique == 'adresse_identique':
        adresse_facturation=adresse_livraison

    if adresse_facturation == adresse_livraison:
        flash(u'adresse de facturation identique que adresse de livraison','alert-info')

    sql = '''SELECT * FROM ligne_panier WHERE id_utilisateur=%s;'''
    mycursor.execute(sql, (id_client))
    items_ligne_panier = mycursor.fetchall()

    sql = '''SELECT NOW();'''
    mycursor.execute(sql)
    date_heur = mycursor.fetchone()
    dt_string=str(date_heur.get('NOW()'))
    a = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")

    if items_ligne_panier is None or len(items_ligne_panier) < 1:
        flash(u'Pas d\'articles dans le ligne_panier', 'alert-warning')
        return redirect(url_for('client_index'))

    #https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    sql_insert = '''INSERT INTO commande VALUES (null, %s,%s,%s, %s, 1);'''
    mycursor.execute(sql_insert, (a,adresse_livraison,adresse_facturation,id_client))
    insert_commande = mycursor.fetchall()
    sql_last_insert = '''SELECT LAST_INSERT_ID() FROM commande;'''
    mycursor.execute(sql_last_insert)
    select_nb_commande = mycursor.fetchall()
    id_commande=select_nb_commande[0].get('LAST_INSERT_ID()')


    sql_select_velo = '''SELECT id_modele FROM velo WHERE id_velo=%s;'''

    sql_select_modele = '''SELECT prix FROM modele_velo WHERE id_modele=%s;'''

    sql_ajout = '''INSERT INTO ligne_commande VALUES (%s, %s, %s, %s);'''
    sql_suppr = '''DELETE FROM ligne_panier WHERE id_utilisateur=%s;'''
    # numéro de la dernière commande
    i=0
    for item in items_ligne_panier:
        id_velo = item['id_velo']
        quantite = item['quantite']



        mycursor.execute(sql_select_velo, (id_velo))
        modele = mycursor.fetchone()
        id_modele=modele.get('id_modele')

        mycursor.execute(sql_select_modele, (id_modele))
        prix_result = mycursor.fetchone()
        prix = prix_result.get('prix')

        mycursor.execute(sql_ajout, (id_commande, id_velo, quantite, prix))
        suppr_ligne_commande = mycursor.fetchall()

        mycursor.execute(sql_suppr, ( id_client))
        suppr_ligne_panier = mycursor.fetchall()
        i+=1


    get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/article/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql='''SELECT date_achat,COUNT(*) AS nbr_articles, SUM(prix) AS prix_total ,commande.id_etat AS etat_id, etat.libelle, commande.id_commande 
     FROM commande 
     INNER JOIN ligne_commande
     ON commande.id_commande=ligne_commande.id_commande 
     INNER JOIN etat 
     ON commande.id_etat=etat.id_etat
     WHERE id_utilisateur=%s 
     GROUP BY commande.id_commande 
     ORDER BY commande.id_etat ASC,date_achat DESC;'''
    mycursor.execute(sql, (id_client))
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande')
    if id_commande != None:

        sql='''SELECT nom_modele as nom, quantite, mv.prix, sum(mv.prix * ligne_commande.quantite) as prix_ligne
            from ligne_commande
            INNER JOIN commande c2 on c2.id_commande = ligne_commande.id_commande
            INNER JOIN velo v on ligne_commande.id_velo = v.id_velo
            INNER JOIn modele_velo mv on v.id_modele = mv.id_modele
            WHERE c2.id_commande=%s
            GROUP BY v.id_velo;
            '''
        mycursor.execute(sql, (id_commande))
        articles_commande = mycursor.fetchall()
        print(articles_commande)

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
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
            commande_adresses = adresse_livraison
            commande_adresses['adresse_identique'] = 'adresse_identique'

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )

