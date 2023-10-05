#! /usr/bin/python
# -*- coding:utf-8 -*-
import datetime
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article',None)
    id_modele = request.form.get('id_modele',None)
    quantite = request.form.get('quantite')
    id_couleur = request.form.get('radio-group',None)
    id_taille = request.form.get('id_taille',None)
    if id_article == None:
        sql= '''SELECT * FROM velo WHERE id_modele = %s'''
        mycursor.execute(sql,(id_modele))
        velos = mycursor.fetchall()
        print(velos,id_modele)
        if len(velos) == 0:
            flash('Ce produit n\'est plus disponible')
            return redirect('/client/article/show')
        elif len(velos) == 1 :
            print('1 seul velo')
            article= velos[0]
        elif len(velos) > 1 and id_couleur == None and id_taille == None:
            print('plusieurs velos')
            sql ='''SELECT DISTINCT c.nom_couleur, c.id_couleur, v.image FROM velo v INNER JOIN couleur c ON v.id_couleur = c.id_couleur WHERE v.id_modele = %s Group by c.id_couleur'''
            mycursor.execute(sql,id_modele)
            couleurs = mycursor.fetchall()
            sql ='''SELECT DISTINCT t.libelle, t.id_taille FROM velo v  INNER JOIN taille t ON v.id_taille = t.id_taille WHERE v.id_modele = %s'''
            mycursor.execute(sql,id_modele)
            tailles = mycursor.fetchall()
            sql = '''SELECT modele_velo.prix as prix, modele_velo.nom_modele as nom , couleur.nom_couleur as couleur , taille.libelle as taille , modele_velo.id_modele as id_modele
                FROM modele_velo
                INNER JOIN velo ON velo.id_modele = modele_velo.id_modele
                INNER JOIN couleur ON velo.id_couleur = couleur.id_couleur
                INNER JOIN taille ON velo.id_taille = taille.id_taille
                WHERE modele_velo.id_modele = %s;
                '''
            mycursor.execute(sql,id_modele)
            article = mycursor.fetchone()
            sql = '''SELECT id_couleur , id_taille  , stock FROM velo WHERE id_modele = %s GROUP BY id_couleur , id_taille'''
            mycursor.execute(sql,id_modele)
            stock = mycursor.fetchall()

            return render_template('client/boutique/declinaison_article.html', id_client=id_client,article=article, id_modele=id_modele, stock=stock, couleurs=couleurs, tailles=tailles)
        else:
            sql = '''SELECT * FROM velo v WHERE id_modele = %s AND id_couleur = %s AND id_taille = %s'''
            mycursor.execute(sql,(id_modele,id_couleur,id_taille))
            article = mycursor.fetchone()
    else:
        sql = '''SELECT * FROM velo WHERE id_velo = %s'''
        mycursor.execute(sql,(id_article))
        article = mycursor.fetchone()

    if article != None:
        sql = '''SELECT * FROM ligne_panier WHERE id_utilisateur = %s AND id_velo = %s'''
        mycursor.execute(sql,(id_client,article['id_velo']))
        article_panier = mycursor.fetchone()

        if quantite.isdecimal() and 0 < int(quantite) <= article['stock']:
            if article_panier != None:
                sql = '''UPDATE ligne_panier SET quantite = quantite + %s WHERE id_utilisateur = %s AND id_velo = %s'''
                mycursor.execute(sql,(quantite,id_client,article['id_velo']))
                sql = '''UPDATE velo SET stock = stock - %s WHERE id_velo = %s'''
                mycursor.execute(sql,(quantite,article['id_velo']))
            else:
                sql = '''INSERT INTO ligne_panier (id_utilisateur,id_velo,quantite) VALUES (%s,%s,%s)'''
                mycursor.execute(sql,(id_client,article['id_velo'],quantite))
                sql = '''UPDATE velo SET stock = stock - %s WHERE id_velo = %s'''
                mycursor.execute(sql,(quantite,article['id_velo']))
            get_db().commit()
        else:
            if quantite.isdecimal() == False or int(quantite) <= 0:
                flash('Quantité invalide', 'alert-danger')
            else:
                flash('Stock insuffisant', 'alert-danger')


    return redirect('/client/article/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article','')
    quantite = request.form.get('quantite',1)
    sql = '''SELECT * FROM velo WHERE id_velo = %s'''
    mycursor.execute(sql,(id_article))
    article = mycursor.fetchone()
    if article != None:
        sql = '''SELECT * FROM ligne_panier WHERE id_utilisateur = %s AND id_velo = %s'''
        mycursor.execute(sql,(id_client,article['id_velo']))
        article_panier = mycursor.fetchone()
        if article_panier != None:
            if article_panier['quantite'] > 1:
                sql = '''UPDATE ligne_panier SET quantite = quantite - %s WHERE id_utilisateur = %s AND id_velo = %s'''
                mycursor.execute(sql,(quantite,id_client,article['id_velo']))
                sql = '''UPDATE velo SET stock = stock + %s WHERE id_velo = %s'''
                mycursor.execute(sql,(quantite,article['id_velo']))
            else:
                sql = '''DELETE FROM ligne_panier WHERE id_utilisateur = %s AND id_velo = %s'''
                mycursor.execute(sql,(id_client,article['id_velo']))
                sql = '''UPDATE velo SET stock = stock + %s WHERE id_velo = %s'''
                mycursor.execute(sql,(quantite,article['id_velo']))
            get_db().commit()

    return redirect('/client/article/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = '''SELECT * FROM ligne_panier WHERE id_utilisateur = %s'''
    mycursor.execute(sql,(client_id))
    items_panier = mycursor.fetchall()
    for item in items_panier:
        sql = '''UPDATE velo SET stock = stock + %s WHERE id_velo = %s'''
        mycursor.execute(sql,(item['quantite'],item['id_velo']))
        sql2='''DELETE FROM ligne_panier WHERE id_utilisateur = %s AND id_velo = %s'''
        mycursor.execute(sql2,(client_id,item['id_velo']))
        get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')

    sql = '''SELECT * FROM ligne_panier WHERE id_utilisateur = %s AND id_velo = %s'''
    mycursor.execute(sql,(id_client,id_article))
    article_panier = mycursor.fetchone()
    if article_panier != None:
        sql = '''UPDATE velo SET stock = stock + %s WHERE id_velo = %s'''
        mycursor.execute(sql,(article_panier['quantite'],id_article))
        sql2='''DELETE FROM ligne_panier WHERE id_utilisateur = %s AND id_velo = %s'''
        mycursor.execute(sql2,(id_client,id_article))
        get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    if filter_word:
        session['filter_word'] = filter_word
    else:
        session.pop('filter_word', None)
    if filter_prix_min:
        session['filter_prix_min'] = filter_prix_min
    else:
        session.pop('filter_prix_min', None)
    if filter_prix_max:
        session['filter_prix_max'] = filter_prix_max
    else:
        session.pop('filter_prix_max', None)
    if filter_types:
        session['filter_types'] = filter_types
    else:
        session.pop('filter_types', None)

    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    if 'filter_word' in session:
        session.pop('filter_word', None)
    if 'filter_prix_min' in session:
        session.pop('filter_prix_min', None)
    if 'filter_prix_max' in session:
        session.pop('filter_prix_max', None)
    if 'filter_types' in session:
        session.pop('filter_types', None)
    return redirect('/client/article/show')
