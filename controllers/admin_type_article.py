#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_type_article = Blueprint('admin_type_article', __name__,
                        template_folder='templates')

@admin_type_article.route('/admin/type-article/show')
def show_type_article():
    mycursor = get_db().cursor()
    sql = '''SELECT type_velo.*, count(id_modele) as nbr_articles FROM type_velo left join est_de_type edt on type_velo.id_type_velo = edt.id_type_velo group by type_velo.id_type_velo;'''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()
    return render_template('admin/type_article/show_type_article.html', types_article=types_article)

@admin_type_article.route('/admin/type-article/add', methods=['GET'])
def add_type_article():
    return render_template('admin/type_article/add_type_article.html')

@admin_type_article.route('/admin/type-article/add', methods=['POST'])
def valid_add_type_article():
    libelle = request.form.get('libelle', '')
    mycursor = get_db().cursor()
    sql='''SELECT * FROM type_velo WHERE libelle = %s'''
    mycursor.execute(sql, libelle)
    type_article = mycursor.fetchone()
    if type_article:
        flash(u'libellé déjà existant', 'alert-danger')
        return redirect('/admin/type-article/add')
    sql = '''INSERT INTO type_velo (libelle) VALUES (%s)'''
    mycursor.execute(sql, libelle)
    get_db().commit()
    message = u'type ajouté , libellé :'+libelle
    flash(message, 'alert-success')
    return redirect('/admin/type-article/show') #url_for('show_type_article')

@admin_type_article.route('/admin/type-article/delete', methods=['GET'])
def delete_type_article():
    id_type_article = request.args.get('id_type_article', '')
    mycursor = get_db().cursor()
    sql = '''SELECT count(edt.id_modele) as nbr_articles FROM type_velo left join est_de_type edt on type_velo.id_type_velo = edt.id_type_velo WHERE type_velo.id_type_velo = %s'''
    mycursor.execute(sql, id_type_article)
    type_article = mycursor.fetchone()
    if type_article['nbr_articles'] == 0:
        sql = '''DELETE FROM type_velo WHERE id_type_velo = %s'''
        mycursor.execute(sql, id_type_article)
        get_db().commit()
        flash(u'suppression type article , id : ' + id_type_article, 'alert-success')
    else:
        flash(u'le type article ne peut pas être supprimé car il est utilisé', 'alert-danger')
    return redirect('/admin/type-article/show')

@admin_type_article.route('/admin/type-article/edit', methods=['GET'])
def edit_type_article():
    id_type_article = request.args.get('id_type_article', '')
    mycursor = get_db().cursor()
    sql = '''Select * from type_velo where id_type_velo = %s'''
    mycursor.execute(sql, (id_type_article,))
    type_article = mycursor.fetchone()
    return render_template('admin/type_article/edit_type_article.html', type_article=type_article)

@admin_type_article.route('/admin/type-article/edit', methods=['POST'])
def valid_edit_type_article():
    libelle = request.form['libelle']
    id_type_article = request.form.get('id_type_article', '')
    tuple_update = (libelle, id_type_article)
    mycursor = get_db().cursor()

    sql='''SELECT * FROM type_velo WHERE libelle = %s'''
    mycursor.execute(sql, libelle)
    type_article = mycursor.fetchone()
    if type_article:
        flash(u'libellé déjà existant', 'alert-danger')
        return redirect('/admin/type-article/edit?id_type_article='+id_type_article)

    sql = '''UPDATE type_velo SET libelle = %s WHERE id_type_velo = %s'''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'type article modifié, id: ' + id_type_article + " libelle : " + libelle, 'alert-success')
    return redirect('/admin/type-article/show')







