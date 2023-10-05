#! /usr/bin/python
# -*- coding:utf-8 -*-
import os
import shutil

from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                        template_folder='templates')

upload_folder = os.getcwd() + '/static/images/'

@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()
#     sql = '''DROP TABLE IF EXISTS est_de_type;'''
#     mycursor.execute(sql)
#     sql = '''DROP TABLE IF EXISTS ligne_panier;'''
#     mycursor.execute(sql)
#     sql = '''DROP TABLE IF EXISTS ligne_commande;'''
#     mycursor.execute(sql)
#     sql = '''DROP TABLE IF EXISTS commande;'''
#     mycursor.execute(sql)
#     sql = '''DROP TABLE IF EXISTS etat;'''
#     mycursor.execute(sql)
#     sql = '''DROP TABLE IF EXISTS type_velo;'''
#     mycursor.execute(sql)
#     sql = '''DROP TABLE IF EXISTS velo;'''
#     mycursor.execute(sql)
#     sql = '''DROP TABLE IF EXISTS couleur;'''
#     mycursor.execute(sql)
#     sql = '''DROP TABLE IF EXISTS taille;'''
#     mycursor.execute(sql)
#     sql = '''DROP TABLE IF EXISTS modele_velo;'''
#     mycursor.execute(sql)
#     sql = '''DROP TABLE IF EXISTS fournisseur;'''
#     mycursor.execute(sql)
#     sql = '''DROP TABLE IF EXISTS adresse;'''
#     mycursor.execute(sql)
#     sql = '''DROP TABLE IF EXISTS utilisateur;'''
#     mycursor.execute(sql)
#
#
#
#     sql = ''' CREATE TABLE utilisateur(
#        id_utilisateur INT AUTO_INCREMENT,
#        login VARCHAR(255),
#        email VARCHAR(255),
#        nom VARCHAR(255),
#        password VARCHAR(255),
#        role VARCHAR(50),
#        PRIMARY KEY(id_utilisateur),
#        UNIQUE(login),
#        UNIQUE(email)
#     );'''
#     mycursor.execute(sql)
#     sql = '''CREATE TABLE adresse(
#    id_adresse INT AUTO_INCREMENT,
#    nom VARCHAR(255),
#    rue VARCHAR(255),
#    code_postal INT NOT NULL,
#    ville VARCHAR(255),
#    id_utilisateur INT,
#    PRIMARY KEY(id_adresse),
#    FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
# );'''
#     mycursor.execute(sql)
#
#     sql = ''' CREATE TABLE etat(
#        id_etat INT AUTO_INCREMENT,
#        libelle VARCHAR(255),
#        PRIMARY KEY(id_etat)
#     );'''
#     mycursor.execute(sql)
#
#     sql = ''' CREATE TABLE type_velo(
#        id_type_velo INT AUTO_INCREMENT,
#        libelle VARCHAR(255),
#        PRIMARY KEY(id_type_velo)
#     );'''
#     mycursor.execute(sql)
#
#
#     sql = ''' CREATE TABLE taille(
#        id_taille INT AUTO_INCREMENT,
#        libelle VARCHAR(255),
#        PRIMARY KEY(id_taille)
#     );'''
#     mycursor.execute(sql)
#
#     sql = ''' CREATE TABLE couleur(
#        id_couleur INT AUTO_INCREMENT,
#        nom_couleur VARCHAR(255),
#        PRIMARY KEY(id_couleur)
#     );'''
#     mycursor.execute(sql)
#
#
#     sql = ''' CREATE TABLE fournisseur(
#        id_fournisseur INT AUTO_INCREMENT,
#        libelle_fournisseur VARCHAR(255),
#        PRIMARY KEY(id_fournisseur)
#     );'''
#     mycursor.execute(sql)
#
#
#     sql = ''' CREATE TABLE commande(
#        id_commande INT AUTO_INCREMENT,
#        date_achat DATE,
#        id_utilisateur INT NOT NULL,
#        id_etat INT NOT NULL,
#        PRIMARY KEY(id_commande),
#        FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
#        FOREIGN KEY(id_etat) REFERENCES etat(id_etat)
#     );'''
#     mycursor.execute(sql)
#
#     sql = ''' CREATE TABLE modele_velo(
#        id_modele INT AUTO_INCREMENT,
#        nom_modele VARCHAR(255),
#        image VARCHAR(255),
#        description VARCHAR(2000),
#        prix DECIMAL(15,2),
#        id_fournisseur INT NOT NULL,
#        PRIMARY KEY(id_modele),
#        FOREIGN KEY(id_fournisseur) REFERENCES fournisseur(id_fournisseur)
#     );'''
#     mycursor.execute(sql)
#
#     sql = ''' CREATE TABLE velo(
#        id_velo INT AUTO_INCREMENT,
#        poids DECIMAL(15,2),
#        id_couleur INT NOT NULL,
#        id_modele INT NOT NULL,
#        id_taille INT NOT NULL,
#        image VARCHAR(255),
#        stock INT,
#        PRIMARY KEY(id_velo),
#        FOREIGN KEY(id_couleur) REFERENCES couleur(id_couleur),
#        FOREIGN KEY(id_modele) REFERENCES modele_velo(id_modele),
#        FOREIGN KEY(id_taille) REFERENCES taille(id_taille)
#     );'''
#     mycursor.execute(sql)
#
#     sql = ''' CREATE TABLE ligne_commande(
#        id_commande INT,
#        id_velo INT,
#        quantite INT,
#        prix DECIMAL(15,2),
#        PRIMARY KEY(id_commande, id_velo),
#        FOREIGN KEY(id_commande) REFERENCES commande(id_commande),
#        FOREIGN KEY(id_velo) REFERENCES velo(id_velo)
#     );'''
#     mycursor.execute(sql)
#
#     sql = ''' CREATE TABLE ligne_panier(
#        id_utilisateur INT,
#        id_velo INT,
#        quantite INT,
#        date_ajout DATE,
#        PRIMARY KEY(id_utilisateur, id_velo),
#        FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
#        FOREIGN KEY(id_velo) REFERENCES velo(id_velo)
#     );'''
#     mycursor.execute(sql)
#
#     sql = ''' CREATE TABLE est_de_type(
#         id_modele INT,
#        id_type_velo INT,
#        PRIMARY KEY(id_type_velo, id_modele),
#        FOREIGN KEY(id_type_velo) REFERENCES type_velo(id_type_velo),
#        FOREIGN KEY(id_modele) REFERENCES modele_velo(id_modele)
#     );'''
#     mycursor.execute(sql)
#
#     sql = '''INSERT INTO etat(libelle) VALUES ('en attente'), ('expédié'), ('validé'), ('confirmé');'''
#     mycursor.execute(sql)
#     sql = '''INSERT INTO fournisseur(libelle_fournisseur) VALUES('Decathlon'),('Revolution Bike'),('levelomad'),('Big Bike'),('Culture Velo');'''
#     mycursor.execute(sql)
#     sql = '''INSERT INTO type_velo(libelle) VALUES ('VTT'),('Vélo électrique'),('VTC'),('Vélo de ville'),('Vélo de route'),('Vélo enfant');'''
#     mycursor.execute(sql)
#     sql = '''INSERT INTO taille(libelle) VALUES('12-13 mois'),('3-5 ans'),('XS'), ('S'), ('M'), ('L'), ('XL'),('Taille unique');'''
#     mycursor.execute(sql)
#     sql = '''INSERT INTO couleur(nom_couleur) VALUES('Noir'),('Blanc'),('Rouge'),('Bleu'),('Vert'),('Jaune'),('Orange'),('Rose'),('Gris'),('Marron'),('Violet');'''
#     mycursor.execute(sql)
#
#     sql = '''INSERT INTO modele_velo VALUES (NULL,'VÉLO VTT ÉLECTRIQUE E-ST 100 ','velo-vtt-electrique-e-st-100-bleu-275.png','Ce VTT électrique (VTTAE) est conçu pour les randonnées tout terrain, avec un dénivelé modéré (parcours vallonnés). C est un vélo parfaitement adapté pour découvrir ou redécouvrir la pratique et vivre ses premières sensations en VTT.',1099,1),
#                             (NULL,'VÉLO VTT RANDONNÉE EXPLORE 500 ','velo-vtt-randonnee-explore-500-noir-29.png','Ce VTT 29" est conçu pour vos randonnées VTT, toute l année, de 2h à 3h.Confort et réactivité face aux aléas du terrain: les roues 29" (27,5" en S), le mono plateau et les freins à disque hydrauliques du VTT EXPL 500 vont changer vos randonnées VTT !',499,1),
#                             (NULL,'VÉLO VTT ST 100 ','velo-vtt-st-100-jaune-275.png','Ce VTT 27,5" est conçu pour vos 1ères randonnées VTT, par temps sec, jusqu à 1h30. Efficacité ? Robustesse ? Les 2 s il vous plaît ! Franchissez sans peine et sans casse vos premiers obstacles : cadre aluminium léger et roues en 27,5 montées sur jantes double parois.',250,1),
#                             (NULL,'VELO 14 POUCES 3-5 ANS 500 ','velo-14-pouces-3-5-ans-500-ocean.png','1,2,3 pédalez! Nous avons conçu ce vélo 14" pour que les enfants de 3 à 5 ans, mesurant 90cm à 105cm, apprennent à pédaler et à rouler comme les grands. Avec un enjambement bas, ce vélo avec stabilisateurs permet à votre enfant d apprendre à rouler à son rythme. Il est équipé d un carter de chaine et de garde boues pour éviter frottement et salissure',100,1),
#                             (NULL,'Draisienne enfant – Draisienne G-Bike','draisienne-enfant-draisienne-g-bike-vert.png','Cette draisienne accompagnera votre enfant dès 2 ans dans l’apprentissage de la mobilité et du vélo en évitant les petites roues !',83.932,1),
#                             (NULL,'BUNZI, Porteur et première draisienne 2en1','bunzi-porteur-et-premiere-draisienne-2en1.png','Tricycle et draisienne évolutifs 2en1, conçu pour apprendre à l’enfant à développer son sens de l équilibre. Passez en quelques secondes du mode 3 roues en mode 2 roues et sans utiliser d outils.',54.99,1),
#                             (NULL,'VTT All Mountain AM 100 ','vtt-all-mountain-am-100-s.png','Ce VTT tout suspendu a été conçu pour la pratique du All Mountain. Il est particulièrement adapté pour piloter vite tout en prenant un max de fun ! Parfait pour se dépasser sur les singles techniques et cassants ! Sa géométrie adaptée et ses roues en 29 favorisent la vitesse et la stabilité, votre flow na plus qu à sexprimer;)',1799,1),
#                             (NULL,'Vélo de Ville Pliant à Assistance Électrique 24 - Legend Siena 13Ah','velo-de-ville-pliant-a-assistance-electrique-24-legend-siena-13ah-noir.png','Vélo électrique pliant de ville. Le Smart eBike Siena est un vélo pliant électrique confortable, idéal pour les déplacements urbains grâce à ses pneus de 24 pouces.',1804.05,1),
#                             (NULL,'Bottecchia 115 Altus Disque 16S 27,5 2022','9.png','Nous avons conçu ce vélo pour vous permettre de progresser facilement. Sa polyvalence et ses 2X8 vitesses vous permettront d explorer toutes les routes. Progressez avec un vélo polyvalent! Sa géométrie confort, son cadre en aluminium, sa fourche carbone et ses freins à disque vous permettront de vous frotter à tous les types de parcours',590,2),
#                             (NULL,'VELO DE VILLE ELOPS 520','velo-de-ville-elops-520-cadre-bas-vert.png','Notre équipe de concepteurs⸱trices a conçu ce vélo confortable pour réaliser vos trajets urbains occasionnels, équipé pour le transport en toute sécurité.',349,1),
#                             (NULL,'Le Sport +','velo-vtt-electrique-e-st-500-noir-275-moteur-central.jpg','Doté d un moteur central à capteurs de couple, garantissant autonomie et légèreté, le Sport + reprend ce qui a fait le succès du modèle Sport, et le rend encore meilleur. + Fluide + Élégant + Polyvalent + MAD.',2490,3),
#                             (NULL,'Scott Genius LT 720 Plus 2017','scott_2017_geniuslt720plus__crop_1000x604.jpg','Ce VTT est conçu pour les randonnées tout terrain.C est un vélo parfaitement adapté pour découvrir ou redécouvrir la pratique et vivre ses premières sensations en VTT.',3499,4),
#                             (NULL,'Zesty XM 327','2016-Zesty-XM-327-6420.jpg','Ce VTT est conçu pour les randonnées tout terrain.C est un vélo parfaitement adapté pour découvrir ou redécouvrir la pratique et vivre ses premières sensations en VTT.',2499,5),
#                             (NULL,'VÉLO VTT ST 120 NOIR','velo-vtt-st-120-noir-bleu-275.png','Ce VTT est conçu pour vos 1ères randonnées VTT, par temps sec, jusqu à 1h30.Un VTT performant et facile ! Aux commandes du VTT ST 120, vous vous sentez précis et léger grâce au mono plateau (1x9 vitesses) et à ses freins à disque mécaniques. Adaptez votre vitesse facilement.',360,1),
#                             (NULL,'VELO VILLE RAPIDE ELOPS SPEED 900','velo-ville-rapide-elops-speed-900-gris.png','Vitesse et agilité marquent l’identité de notre vélo Elops Speed 900. Derrière ce look sobre se cache un caractère vif pour se jouer de la ville avec style. Notre envie ? Vous proposer un vélo rapide, nerveux, offrant une dimension sportive à vos trajets urbains sans omettre la sécurité grâce à des équipements de qualité.',439,1);'''
#
#     mycursor.execute(sql)
#
#
#
#
#     sql = '''INSERT INTO velo VALUES
#                             (NULL,13,4,1,3,'velo-vtt-electrique-e-st-100-bleu-275.png',5),
#                             (NULL,14,1,2,4,'velo-vtt-randonnee-explore-500-noir-29.png',5),
#                             (NULL,15,6,3,3,'velo-vtt-st-100-jaune-275.png',12),(NULL,16,6,3,4,'velo-vtt-st-100-jaune-275.png',14),(NULL,17,6,3,5,'velo-vtt-st-100-jaune-275.png',12),
#                             (NULL,9,4,4,2,'velo-14-pouces-3-5-ans-500-ocean.png',15),
#                             (NULL,2,5,5,1,'draisienne-enfant-draisienne-g-bike-vert.png',15),
#                             (NULL,3,5,6,1,'bunzi-porteur-et-premiere-draisienne-2en1.png',20),
#                             (NULL,15,4,7,4,'vtt-all-mountain-am-100-s.png',48),
#                             (NULL,21,1,8,4,'velo-de-ville-pliant-a-assistance-electrique-24-legend-siena-13ah-noir.png',45),(NULL,21,1,8,5,'velo-de-ville-pliant-a-assistance-electrique-24-legend-siena-13ah-noir.png',10),(NULL,21,1,8,6,'velo-de-ville-pliant-a-assistance-electrique-24-legend-siena-13ah-noir.png',2),(NULL,21,2,8,4,'velo-de-ville-pliant-a-assistance-electrique-24-legend-siena-13ah-blanc.png',14),(NULL,21,3,8,4,'velo-de-ville-pliant-a-assistance-electrique-24-legend-siena-13ah-rouge.png',50),
#                             (NULL,15,3,9,5,'9.png',55),
#                             (NULL,15,5,10,5,'velo-de-ville-elops-520-cadre-bas-vert.png',12),
#                             (NULL,19,1,11,7,'velo-vtt-electrique-e-st-500-noir-275-moteur-central.jpg',0),
#                             (NULL,14,9,12,6,'scott_2017_geniuslt720plus__crop_1000x604.jpg',22),
#                             (NULL,14,4,13,6,'2016-Zesty-XM-327-6420.jpg',20),
#                             (NULL,15,1,14,6,'velo-vtt-st-120-noir-bleu-275.png',1),
#                             (NULL,11,9,15,5,'velo-ville-rapide-elops-speed-900-gris.png',5);'''
#     mycursor.execute(sql)
#
#     sql = '''INSERT INTO est_de_type VALUES(1,1),(1,2),
#                                   (2,1),
#                                   (3,1),
#                                   (4,6),
#                                   (5,6),
#                                   (6,6),
#                                   (7,1),
#                                   (8,4),(8,2),
#                                   (9,1),
#                                   (10,4),
#                                   (11,1),(11,2),
#                                   (12,1),
#                                   (13,1),
#                                   (14,3),
#                                   (15,4);'''
#     mycursor.execute(sql)
#
#     sql = '''INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom) VALUES
#     (1,'admin','admin@admin.fr',
#         'sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf',
#         'ROLE_admin','admin'),
#     (2,'client','client@client.fr',
#         'sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d',
#         'ROLE_client','client'),
#     (3,'client2','client2@client2.fr',
#         'sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422',
#         'ROLE_client','client2');'''
#     mycursor.execute(sql)

    mycursor = get_db().cursor()
    fichier = open("sae_sql.sql", "r" , encoding="utf-8")
    texte= fichier.read().replace("\n","").split(';')
    for i in texte[:-1]:
        mycursor.execute(i)
    fichier.close()
    shutil.rmtree(os.path.join('static/', 'images'))
    shutil.copytree(os.path.join('static/', 'backup'), os.path.join('static/', 'images'))
    get_db().commit()
    return redirect('/')
