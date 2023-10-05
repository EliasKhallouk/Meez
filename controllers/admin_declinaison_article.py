#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, flash
import os
import random
from werkzeug.utils import secure_filename
from connexion_db import get_db

admin_declinaison_article = Blueprint('admin_declinaison_article', __name__,
                         template_folder='templates')

UPLOAD_FOLDER = os.getcwd() + '/static/images/'
BACKUP_FOLDER = os.getcwd() + '/static/backup/'

@admin_declinaison_article.route('/admin/declinaison_article/add')
def add_declinaison_article():
    id_article=request.args.get('id_article')
    mycursor = get_db().cursor()
    sql = ''' SELECT modele_velo.id_modele AS id_article,
        modele_velo.image AS image
        , modele_velo.nom_modele AS nom
        , modele_velo.prix AS prix
        , modele_velo.description AS description
        , tv.id_type_velo AS type_article_id
        FROM modele_velo
        INNER JOIN est_de_type edt on modele_velo.id_modele = edt.id_modele
        INNER JOIN type_velo tv on edt.id_type_velo = tv.id_type_velo
        WHERE modele_velo.id_modele = %s '''
    mycursor.execute(sql, id_article)
    article= mycursor.fetchone()
    sql ='''SELECT id_couleur, nom_couleur as libelle FROM couleur'''
    mycursor.execute(sql)
    couleurs= mycursor.fetchall()
    sql ='''SELECT id_taille , libelle FROM taille'''
    mycursor.execute(sql)
    tailles= mycursor.fetchall()
    return render_template('admin/article/add_declinaison_article.html'
                           , article=article
                           , couleurs=couleurs
                           , tailles=tailles
                           )


@admin_declinaison_article.route('/admin/declinaison_article/add', methods=['POST'])
def valid_add_declinaison_article():
    mycursor = get_db().cursor()

    id_article = request.form.get('id_article')
    stock = request.form.get('stock')
    taille = request.form.get('taille')
    couleur = request.form.get('couleur')
    image = request.files.get('image','')

    sql ='''SELECT * FROM velo WHERE id_taille=%s and id_couleur=%s'''
    mycursor.execute(sql, (taille,couleur))
    velo= mycursor.fetchone()
    if velo is None:
        image_nom=''
        if image != '' and image.filename!='':
            image_nom = str(random.randint(1,445451548515258))+secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, image_nom))

        sql ='''INSERT INTO velo (id_couleur, id_taille, id_modele, image, stock) VALUES (%s,%s,%s,%s,%s)'''
        mycursor.execute(sql, (couleur,taille,id_article,image_nom,stock))
        get_db().commit()
    else:
        flash('Cette déclinaison existe déjà')
    return redirect('/admin/article/edit?id_article=' + id_article)


@admin_declinaison_article.route('/admin/declinaison_article/edit', methods=['GET'])
def edit_declinaison_article():
    id_declinaison_article = request.args.get('id_declinaison_article')
    mycursor = get_db().cursor()
    sql = ''' SELECT velo.id_velo as id_declinaison_article , velo.image as image_article , velo.stock , velo.id_couleur as couleur_id, velo.id_taille as taille_id , velo.id_modele as article_id FROM velo WHERE velo.id_velo = %s '''
    mycursor.execute(sql, (id_declinaison_article))
    declinaison_article= mycursor.fetchone()
    sql ='''SELECT id_couleur , nom_couleur as libelle FROM couleur'''
    mycursor.execute(sql)
    couleurs=mycursor.fetchall()
    sql ='''SELECT id_taille , libelle FROM taille'''
    mycursor.execute(sql)
    tailles= mycursor.fetchall()
    return render_template('admin/article/edit_declinaison_article.html'
                           , tailles=tailles
                           , couleurs=couleurs
                           , declinaison_article=declinaison_article
                           )


@admin_declinaison_article.route('/admin/declinaison_article/edit', methods=['POST'])
def valid_edit_declinaison_article():
    id_declinaison_article = request.form.get('id_declinaison_article','')
    id_article = request.form.get('id_article','')
    stock = request.form.get('stock','')
    taille_id = request.form.get('id_taille','')
    couleur_id = request.form.get('id_couleur','')
    image = request.files.get('image','')
    mycursor = get_db().cursor()
    if image.filename != '':
        sql = '''SELECT * FROM velo WHERE id_velo = %s'''
        mycursor.execute(sql, id_declinaison_article)
        article = mycursor.fetchone()
        sql = '''SELECT velo.image FROM velo WHERE velo.image = %s and velo.id_velo !=%s'''
        mycursor.execute(sql, (article["image"], id_declinaison_article))
        velo = mycursor.fetchone()
        sql = '''SELECT mv.image FROM modele_velo mv WHERE mv.image = %s'''
        mycursor.execute(sql, article["image"])
        modele = mycursor.fetchone()
        print(image.filename)
        print(velo)
        print('------------------')
        print(modele)
        if velo is None and modele is None:
            if article['image'] != '':
                os.remove(os.path.join(UPLOAD_FOLDER, article['image']))

        image.filename = str(random.randint(1,100000000))+secure_filename(image.filename)
        image.save(os.path.join(UPLOAD_FOLDER, image.filename))
        sql = '''UPDATE velo SET stock = %s, id_couleur = %s, id_taille = %s , image = %s WHERE id_velo = %s '''
        mycursor.execute(sql, (stock, couleur_id, taille_id, image.filename, id_declinaison_article))
    else:
        sql = '''UPDATE velo SET stock = %s, id_couleur = %s, id_taille = %s WHERE id_velo = %s '''
        mycursor.execute(sql, (stock, couleur_id, taille_id, id_declinaison_article))
    get_db().commit()


    message = u'declinaison_article modifié , id:' + str(id_declinaison_article) + '- stock :' + str(stock) + ' - taille_id:' + str(taille_id) + ' - couleur_id:' + str(couleur_id) + ' - image:' + str(image.filename)
    flash(message, 'alert-success')
    return redirect('/admin/article/edit?id_article=' + str(id_article))


@admin_declinaison_article.route('/admin/declinaison_article/delete', methods=['GET'])
def admin_delete_declinaison_article():
    id_declinaison_article = request.args.get('id_declinaison_article','')
    id_article = request.args.get('id_article','')
    mycursor = get_db().cursor()
    sql = '''SELECT * FROM ligne_panier WHERE id_velo=%s '''
    mycursor.execute(sql, id_declinaison_article)
    ligne_panier = mycursor.fetchone()
    sql = '''SELECT * FROM ligne_commande WHERE id_velo = %s'''
    mycursor.execute(sql, id_declinaison_article)
    ligne_commande = mycursor.fetchone()
    if ligne_panier is None and ligne_commande is None:
        sql = '''SELECT * FROM velo WHERE id_velo = %s'''
        mycursor.execute(sql, id_declinaison_article)
        article = mycursor.fetchone()
        image = article['image']
        sql = '''DELETE FROM velo WHERE id_velo = %s'''
        mycursor.execute(sql, id_declinaison_article)
        get_db().commit()
        sql = '''SELECT velo.image FROM velo INNER JOIN modele_velo mv ON mv.id_modele = velo.id_modele WHERE velo.image = %s and mv.image =%s and velo.id_velo !=%s'''

        if image != '':
            sql='''SELECT velo.image FROM velo WHERE velo.image = %s and velo.id_velo !=%s'''
            mycursor.execute(sql, (image,id_declinaison_article))
            velo = mycursor.fetchone()
            sql='''SELECT mv.image FROM modele_velo mv WHERE mv.image = %s'''
            mycursor.execute(sql, (image))
            modele = mycursor.fetchone()
            if velo is None and modele is None:
                os.remove(os.path.join(UPLOAD_FOLDER, image))
        get_db().commit()
        flash(u'declinaison supprimée, id_declinaison_article : ' + str(id_declinaison_article),  'alert-success')
    else:
        flash(u'Impossible de supprimer cette déclinaison, elle est utilisée dans un panier ou une commande',  'alert-danger')

    return redirect('/admin/article/edit?id_article=' + str(id_article))