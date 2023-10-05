from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

import pymysql.cursors

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        #
        db = g._database = pymysql.connect(
            host="localhost",
            user="ekhallou",
            password="2305",
            database="BDD_zakburak",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
            #user="meez",
            #host="meez.mysql.pythonanywhere-services.com",
            #password="meezmeez",
            #database="meez$veloDeMeez",
        )
    return db