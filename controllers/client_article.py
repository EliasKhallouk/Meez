#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                        template_folder='templates')

@client_article.route('/client/index')
@client_article.route('/client/article/show')              # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']
    #
#     sql = '''
#        SELECT mv.id_modele AS id_article,
    # mv.image AS image,
    # mv.nom_modele AS nom,
    # mv.prix AS prix,
    # SUM(velo.stock) AS stock
    # FROM modele_velo mv
    # INNER JOIN velo ON mv.id_modele = velo.id_modele
    # WHERE mv.id_modele IN (SELECT modele_velo.id_modele FROM modele_velo INNER JOIN est_de_type edt on modele_velo.id_modele = edt.id_modele WHERE edt.id_type_velo=2)
    # GROUP BY mv.id_modele
    # ORDER BY mv.id_modele;
#          '''
    # mycursor.execute(sql)
    # articles = mycursor.fetchall()
    filter_word = session.get('filter_word', None)
    filter_prix_min = session.get('filter_prix_min', None)
    filter_prix_max = session.get('filter_prix_max', None)
    filter_types = session.get('filter_types', None)
    param = []

    sql = '''SELECT mv.id_modele AS id_article,
            mv.image AS image,
            mv.nom_modele AS nom,
            mv.prix AS prix,
            SUM(velo.stock) AS stock
            FROM modele_velo mv
            INNER JOIN velo ON mv.id_modele = velo.id_modele
        '''
    if filter_word or filter_prix_min or filter_prix_max or filter_types:
        sql += " WHERE "
        if filter_word and filter_word != None:
            session['filter_word'] = filter_word
            sql += 'mv.nom_modele LIKE %s '
            param.append("%" + filter_word + "%")
        if filter_prix_min or filter_prix_max:
            if filter_prix_max != None:
                filter_prix_max.replace(',', '.')
            if filter_prix_min != None:
                filter_prix_min.replace(',', '.')
            try:
                if filter_prix_max != None:
                    float(filter_prix_max)
                if filter_prix_min != None:
                    float(filter_prix_min)



                if (filter_prix_min and float(filter_prix_min) < 0) or (filter_prix_max and float(filter_prix_max) < 0):
                    message = u"Le prix doit être positif"
                    flash(message, 'alert-warning')
                elif filter_prix_min != None and filter_prix_max == None:
                    if len(param) >= 1:
                        sql += 'and '
                    session['filter_prix_min'] = filter_prix_min
                    sql += "mv.prix >= %s "
                    param.append(float(filter_prix_min))

                elif filter_prix_min == None and filter_prix_max != None:
                    if len(param) >= 1:
                        sql += 'and '
                    session['filter_prix_max'] = filter_prix_max
                    sql += "mv.prix <= %s "
                    param.append(float(filter_prix_max))

                elif float(filter_prix_min) < float(filter_prix_max):
                    if len(param) >= 1:
                        sql += 'and'
                    session['filter_prix_min'] = filter_prix_min
                    session['filter_prix_max'] = filter_prix_max
                    sql += "(mv.prix >= %s and mv.prix <= %s) "
                    param.append(float(filter_prix_min))
                    param.append(float(filter_prix_max))
                else:
                    message = u'min <max'
                    flash(message, 'alert-warning')

            except ValueError:
                message = u"Le prix doit être un nombre"
                flash(message, 'alert-warning')

        if filter_types and filter_types != None:
            if len(param) >= 1:
                sql += 'and'
            sql += " mv.id_modele IN (SELECT modele_velo.id_modele FROM modele_velo INNER JOIN est_de_type edt on modele_velo.id_modele = edt.id_modele WHERE ( "
            message = u'Type de commerçant sélectionné '
            session['filter_types'] = [int(i) for i in filter_types]
            for case in filter_types:
                sql += " edt.id_type_velo=%s or"
                param.append(int(case))

            sql = sql[:-2] + " ))"

        if len(param) == 0:
            sql = sql[:-6]
    sql += " GROUP BY mv.id_modele ORDER BY mv.id_modele;"
    print(sql)
    mycursor.execute(sql, param)
    articles = mycursor.fetchall()

    sql = '''SELECT mv.id_modele AS id_article, COUNT(velo.id_velo) AS nb_declinaisons FROM modele_velo mv 
            INNER JOIN velo ON mv.id_modele = velo.id_modele
            GROUP BY mv.id_modele
            ORDER BY mv.id_modele;
            '''
    mycursor.execute(sql)
    nb_declinaisons = mycursor.fetchall()


    # utilisation du filtre



    sql3=''' prise en compte des commentaires et des notes dans le SQL    '''








    # pour le filtre
    sql='''SELECT type_velo.id_type_velo AS id_type_article, type_velo.libelle AS libelle
            FROM type_velo;
            '''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()

    # pour le panier
    sql = '''SELECT ligne_panier.quantite as quantite, modele_velo.prix as prix, modele_velo.nom_modele as nom , couleur.nom_couleur as couleur  , couleur.id_couleur , taille.libelle as taille , taille.id_taille ,velo.stock as stock , velo.id_velo as id_velo 
            FROM ligne_panier
            INNER JOIN velo ON velo.id_velo = ligne_panier.id_velo
            INNER JOIN modele_velo ON velo.id_modele = modele_velo.id_modele
            INNER JOIN couleur ON velo.id_couleur = couleur.id_couleur
            INNER JOIN taille ON velo.id_taille = taille.id_taille
            WHERE ligne_panier.id_utilisateur = %s;
            '''
    mycursor.execute(sql,(id_client))
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
    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           , prix_total=prix_total
                           , items_filtre=types_article,
                           session=session,nb_declinaisons=nb_declinaisons
                           )
