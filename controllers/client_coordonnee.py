#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_coordonnee = Blueprint('client_coordonnee', __name__,
                              template_folder='templates')


@client_coordonnee.route('/client/coordonnee/show')
def client_coordonnee_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''SELECT * FROM utilisateur WHERE id_utilisateur=%s;'''
    mycursor.execute(sql, id_client)
    utilisateur = mycursor.fetchone()

    sql = '''SELECT * FROM adresse WHERE id_utilisateur=%s;'''
    mycursor.execute(sql, id_client)
    adresse_bdd = mycursor.fetchall()

    adresses = adresse_bdd
    nb_adresses = len(adresses)

    return render_template('client/coordonnee/show_coordonnee.html'
                           , utilisateur=utilisateur
                           , adresses=adresses
                           , nb_adresses=nb_adresses
                           )


@client_coordonnee.route('/client/coordonnee/edit', methods=['GET'])
def client_coordonnee_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''SELECT * FROM utilisateur WHERE id_utilisateur=%s;'''
    mycursor.execute(sql, id_client)
    utilisateur = mycursor.fetchone()

    return render_template('client/coordonnee/edit_coordonnee.html'
                           , utilisateur=utilisateur
                           )


@client_coordonnee.route('/client/coordonnee/edit', methods=['POST'])
def client_coordonnee_edit_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom = request.form.get('nom')
    login = request.form.get('login')
    email = request.form.get('email')

    sql = '''SELECT * FROM utilisateur WHERE id_utilisateur=%s;'''
    mycursor.execute(sql, id_client)
    utilisateur = mycursor.fetchall()

    sql = '''SELECT email,login FROM utilisateur;'''
    mycursor.execute(sql)
    email_login_bdd = mycursor.fetchall()
    print(email_login_bdd)
    compteur=0
    for i in email_login_bdd:
        if i.get('email') == email or i.get('login') == login:
            compteur += 1

    if compteur > 1: 
        flash(u'votre cet Email ou ce Login existe déjà pour un autre utilisateur', 'alert-warning')
        return render_template('client/coordonnee/edit_coordonnee.html'
                               , utilisateur=utilisateur
                               )

    sql = '''UPDATE utilisateur SET login=%s, email=%s, nom=%s  WHERE id_utilisateur=%s'''
    mycursor.execute(sql, (login, email, nom, id_client))
    email = mycursor.fetchone()
    get_db().commit()
    return redirect('/client/coordonnee/show')


@client_coordonnee.route('/client/coordonnee/delete_adresse', methods=['POST'])
def client_coordonnee_delete_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse = request.form.get('id_adresse')
    sql = '''SELECT * FROM commande WHERE id_adresse_facturation=%s or id_adresse_livraison=%s;'''
    mycursor.execute(sql, (id_adresse, id_adresse))
    verif_adresse = mycursor.fetchone()
    if verif_adresse:
        flash(u'Vous ne pouvez pas supprimer cette adresse car elle est liée à une commande', 'alert-warning')
        return redirect('/client/coordonnee/show')
    sql = '''DELETE FROM adresse WHERE id_adresse=%s and id_utilisateur = %s;'''
    mycursor.execute(sql, (id_adresse, id_client))
    get_db().commit()
    return redirect('/client/coordonnee/show')


@client_coordonnee.route('/client/coordonnee/add_adresse')
def client_coordonnee_add_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''SELECT COUNT(*) FROM adresse WHERE id_utilisateur=%s;'''
    mycursor.execute(sql, id_client)
    nb_adresse = mycursor.fetchone()

    if nb_adresse.get("COUNT(*)") < 4:
        sql = '''SELECT * FROM utilisateur WHERE id_utilisateur=%s;'''
        mycursor.execute(sql, id_client)
        utilisateur = mycursor.fetchone()
    else:
        utilisateur= None



    return render_template('client/coordonnee/add_adresse.html'
                            ,utilisateur=utilisateur
                           )


@client_coordonnee.route('/client/coordonnee/add_adresse', methods=['POST'])
def client_coordonnee_add_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom = request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')

    sql = '''SELECT COUNT(*) FROM adresse WHERE id_utilisateur=%s;'''
    mycursor.execute(sql, id_client)
    nb_adresse = mycursor.fetchone()

    if nb_adresse.get("COUNT(*)") < 4:
        sql = '''INSERT INTO adresse VALUES (null, %s, %s, %s, %s, %s);'''
        mycursor.execute(sql, (nom, rue, code_postal, ville, id_client))
        email = mycursor.fetchone()
        get_db().commit()


    return redirect('/client/coordonnee/show')


@client_coordonnee.route('/client/coordonnee/edit_adresse')
def client_coordonnee_edit_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse = request.args.get('id_adresse')

    sql = '''SELECT * FROM utilisateur WHERE id_utilisateur=%s;'''
    mycursor.execute(sql, id_client)
    utilisateur = mycursor.fetchone()

    sql = '''SELECT * FROM adresse WHERE id_adresse=%s;'''
    mycursor.execute(sql, id_adresse)
    adresse = mycursor.fetchone()

    return render_template('/client/coordonnee/edit_adresse.html'
                            ,utilisateur=utilisateur
                            ,adresse=adresse
                           )


@client_coordonnee.route('/client/coordonnee/edit_adresse', methods=['POST'])
def client_coordonnee_edit_adresse_recoit():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom = request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')
    id_adresse = request.form.get('id_adresse')

    sql = '''UPDATE adresse  SET nom=%s, rue=%s, code_postal=%s, ville=%s, id_utilisateur=%s WHERE id_adresse=%s;'''
    mycursor.execute(sql, (nom, rue, code_postal, ville, id_client, id_adresse))
    email = mycursor.fetchall()
    get_db().commit()

    return redirect('/client/coordonnee/show')
