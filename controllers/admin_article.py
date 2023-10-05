#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
from werkzeug.utils import secure_filename

#from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__,
                          template_folder='templates')
UPLOAD_FOLDER = os.getcwd() + '/static/images/'
BACKUP_FOLDER = os.getcwd() + '/static/backup/'
@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()
    sql = '''   SELECT modele_velo.id_modele AS id_article,
        modele_velo.image AS image
        , modele_velo.nom_modele AS nom
        , modele_velo.prix AS prix
        , IFNULL(SUM(velo.stock),0) AS stock
        , IFNULL(COUNT(velo.id_velo),0) AS nb_declinaisons
        FROM velo
        RIGHT JOIN modele_velo ON modele_velo.id_modele = velo.id_modele
        GROUP BY modele_velo.id_modele
        ORDER BY modele_velo.id_modele ASC;
    '''

    mycursor.execute(sql)
    articles = mycursor.fetchall()

    sql = ''' SELECT * , tv.libelle from est_de_type LEFT JOIN type_velo tv on est_de_type.id_type_velo = tv.id_type_velo'''
    mycursor.execute(sql)
    type_articles =  mycursor.fetchall()
    return render_template('admin/article/show_article.html', articles=articles , type_articles=type_articles)


@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():
    mycursor = get_db().cursor()

    sql= '''SELECT id_type_velo as id_type_article , libelle FROM type_velo'''
    mycursor.execute(sql)
    type_article = mycursor.fetchall()
    sql = '''SELECT * FROM fournisseur'''
    mycursor.execute(sql)
    fournisseurs = mycursor.fetchall()
    return render_template('admin/article/add_article.html'
                           ,types_article=type_article, fournisseurs=fournisseurs
                            )


@admin_article.route('/admin/article/add', methods=['POST'])
def valid_add_article():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_article_id = request.form.get('type_article_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    fournisseur_id = request.form.get('fournisseur_id', '')
    image = request.files.get('image', '')

    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join(UPLOAD_FOLDER, filename))
    else:
        filename=''

    sql = ''' INSERT INTO modele_velo (nom_modele, image, prix, description , id_fournisseur ) VALUES (%s, %s, %s, %s, %s)'''

    tuple_add = (nom, filename, prix, description, fournisseur_id)
    mycursor.execute(sql, tuple_add)
    get_db().commit()
    sql = " SELECT LAST_INSERT_ID() as id;"
    mycursor.execute(sql)
    id = mycursor.fetchone();
    print(id)
    type_id = request.form.getlist('type_article_id', None)
    for i in type_id:
        sql = "INSERT INTO est_de_type VALUES(%s,%s)"
        mycursor.execute(sql, (id['id'], i))
    get_db().commit()
    message = u'article ajouté , nom:' + nom + '- type_article:' + type_article_id + ' - prix:' + prix + ' - description:' + description + ' - image:' + str(
        image) + ' - fournisseur_id:' + fournisseur_id
    flash(message, 'alert-success')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/delete', methods=['GET'])
def delete_article():
    id_article=request.args.get('id_article')
    mycursor = get_db().cursor()
    sql = ''' SELECT COUNT(velo.id_velo) AS nb_declinaison FROM velo WHERE velo.id_modele = %s '''
    mycursor.execute(sql, id_article)
    nb_declinaison = mycursor.fetchone()
    if nb_declinaison['nb_declinaison'] > 0:
        message= u'il y a des declinaisons dans cet article : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
        # sql= '''DELETE FROM velo WHERE velo.id_modele = %s'''
        # mycursor.execute(sql, id_article)
        # get_db().commit()
    else:

        sql = '''SELECT * FROM modele_velo WHERE id_modele = %s'''
        mycursor.execute(sql, id_article)
        article = mycursor.fetchone() 
        image = article['image']
        
        sql = '''DELETE FROM est_de_type WHERE id_modele = %s'''
        mycursor.execute(sql, id_article)
        get_db().commit()

        sql = ''' DELETE FROM modele_velo WHERE id_modele = %s '''
        mycursor.execute(sql, id_article)
        get_db().commit()
        sql = '''SELECT velo.image FROM velo WHERE velo.image = %s'''
        mycursor.execute(sql, image)
        velo = mycursor.fetchone()
        sql = '''SELECT mv.image FROM modele_velo mv WHERE mv.image = %s and mv.id_modele !=%s'''
        mycursor.execute(sql, (image, id_article))
        modele = mycursor.fetchone()
        if velo is None and modele is None:
            if image != '':
                os.remove(os.path.join(UPLOAD_FOLDER, image))

        message = u'un article supprimé, id : ' + id_article
        flash(message, 'alert-success')

    return redirect('/admin/article/show')


@admin_article.route('/admin/article/edit', methods=['GET'])
def edit_article():
    id_article=request.args.get('id_article')
    mycursor = get_db().cursor()
    sql = '''
    SELECT modele_velo.id_modele AS id_article,
        modele_velo.image AS image
        , modele_velo.nom_modele AS nom
        , modele_velo.prix AS prix
        , modele_velo.description AS description
        FROM modele_velo
        LEFT JOIN est_de_type edt on modele_velo.id_modele = edt.id_modele
        WHERE modele_velo.id_modele = %s 
    '''
    mycursor.execute(sql, id_article)
    article = mycursor.fetchone()
    sql = '''
    SELECT id_type_velo as id_type_article , libelle  FROM type_velo'''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()

    sql = '''
    SELECT velo.id_velo as id_declinaison_article , velo.stock ,velo.image as image , velo.id_modele as article_id   , couleur.nom_couleur , taille.libelle as libelle_taille FROM velo
    INNER JOIN couleur ON couleur.id_couleur = velo.id_couleur
    INNER JOIN taille ON taille.id_taille = velo.id_taille
    WHERE velo.id_modele = %s'''
    mycursor.execute(sql, id_article)
    declinaisons_article = mycursor.fetchall()

    sql = ''' SELECT * FROM est_de_type WHERE id_modele =%s'''
    mycursor.execute(sql,id_article)
    types= mycursor.fetchall()


    return render_template('admin/article/edit_article.html'
                            ,article=article
                            ,types_article=types_article
                            ,declinaisons_article=declinaisons_article
                           ,types=types
                           )


@admin_article.route('/admin/article/edit', methods=['POST'])
def valid_edit_article():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    id_article = request.form.get('id_article')
    type_article_id = request.form.get('type_article_id', '')
    prix = request.form.get('prix', '')
    image = request.files.get('image', None)
    description = request.form.get('description')
    sql = ''' SELECT image from modele_velo WHERE id_modele=%s
       '''
    mycursor.execute(sql, id_article)
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image']
    if image:
        if image_nom != "" and image_nom is not None and os.path.exists(
                os.path.join(os.getcwd() + "/static/images/", image_nom)):
            sql = '''SELECT velo.image FROM velo WHERE velo.image = %s'''
            mycursor.execute(sql, image_nom)
            velo = mycursor.fetchone()
            sql = '''SELECT mv.image FROM modele_velo mv WHERE mv.image = %s and mv.id_modele !=%s '''
            mycursor.execute(sql, (image_nom, id_article))
            modele = mycursor.fetchone()
            if velo is None and modele is None:
                os.remove(os.path.join(UPLOAD_FOLDER, image_nom))
        filename = secure_filename(image.filename)
        if image:
            filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
            image.save(os.path.join(UPLOAD_FOLDER, filename))
            image_nom = filename

    sql = '''UPDATE modele_velo SET nom_modele = %s , image =%s , prix = %s , description =%s WHERE id_modele=%s '''
    mycursor.execute(sql, (nom, image_nom, prix, description, id_article))

    sql = '''DELETE FROM est_de_type WHERE id_modele = %s'''
    mycursor.execute(sql,id_article)
    type_id = request.form.getlist('type_article_id',None)
    for i in type_id:
        sql="INSERT INTO est_de_type VALUES(%s,%s)"
        mycursor.execute(sql,(id_article,i))




    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = u'article modifié , nom:' + nom + '- type_article :' + type_article_id + ' - prix:' + prix  + ' - image:' + image_nom + ' - description: ' + description
    flash(message, 'alert-success')
    return redirect('/admin/article/show')







@admin_article.route('/admin/article/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    article=[]
    commentaires = {}
    return render_template('admin/article/show_avis.html'
                           , article=article
                           , commentaires=commentaires
                           )


@admin_article.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)
    userId = request.form.get('idUser', None)

    return admin_avis(article_id)
