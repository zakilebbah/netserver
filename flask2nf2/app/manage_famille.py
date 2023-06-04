import os
from app import app
from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from app.models import Parametre, Article, Tiers, Famille
from app import db
import json
from app.models import self_init
import datetime
import dateutil.parser
import pprint
import sqlalchemy as sa
import random
import urllib.parse
import ntpath
import glob
from sqlalchemy import func

"""
api functions
"""

def extendFamillesToImages(familles0):
    numberList = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11']
    list0 = []
    for e in familles0:
        dossier0 = random.choice(numberList)
        pi0 = {'CODEFAMILLE': urllib.parse.quote(e['CODEFAMILLE']), 'DOSSIER': urllib.parse.quote(dossier0), 'IMAGES': []}
        path0 = app.config['UPLOAD_FOLDER'] + '/' + dossier0
        # app.logger.info(">>>>>>>>>>>>>>> path " + path0)
        list1 = glob.glob(path0 + "/*.*")
        images0 = []
        for file0 in list1:
            # app.logger.info(">>>>>>>>>>>>>>> filename " + file0)
            images0.append(urllib.parse.quote(ntpath.basename(file0)))
            # app.logger.info(">>>>>>>>>>>>>>> filename " + file0)
        pi0['IMAGES'] = images0
        list0.append(dict(e, **pi0))
    return list0


def local_get_Familles():
    allFamilles = []
    try:
        allFamilles = db.session.query(Famille).all()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    # print(">>>>>>>>>>>>>>> local_get_Familles called", flush=True)
    return  ([e.serialize() for e in allFamilles])
def local_get_visible_Familles():
    allFamilles = []
    try:
        allFamilles = db.session.query(Famille).filter_by(boutiq_visible=1).order_by(Famille.intitule).all()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    # print(">>>>>>>>>>>>>>> local_get_Familles called", flush=True)
    return  ([e.serialize() for e in allFamilles])
def local_get_FamillesVisibles(code):
    allFamilles = db.session.query(Famille).filter_by(codefamille_m=code, boutiq_visible=1).order_by(Famille.intitule).all()
    # app.logger.info(">>>>>>>>>>>>>>>>>>>>> feeeeeeeeeeeeeeeeeeeeeeeeeeeee" + str([e.serialize() for e in allFamilles]))
    allFamillesVisibles = extendToImages([e.serialize() for e in allFamilles])
    return allFamillesVisibles

def local_get_Famille(obj0):
    if (obj0 == ''):
        allFamilles = []
        try:
            allFamilles = db.session.query(Famille).all()
        except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
            app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return ([e.serialize() for e in allFamilles])
    else:
        allFamilles = []
        try:
            allFamilles = db.session.query(Famille).filter_by(codefamille=obj0).one()
        except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
            app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return (allFamilles.serialize())
        
def extendToImages(articles0):
    list0 = []
    imagesPath = app.config['CATEGORIES_IMAGES']
    defaultImagePath = app.config['DEFAULT_IMAGE']
    directory = os.fsencode(imagesPath)
    for e in articles0:
        # app.logger.info(">>>>>>>>>>>>>>>>>>>>> *********************************************" + str(e))
        pi0 = {'CODEFAMILLE': urllib.parse.quote(e['CODEFAMILLE']), 'IMAGES': []}
        codeFamily = e['CODEFAMILLE']
        images = []
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            name, imageType = filename.split(".")
            if name == codeFamily:
                # for file1 in os.listdir(os.fsencode(f'{imagesPath}/{filename}')):
                #     imageName = os.fsdecode(file1)
                images.append(str(filename))
        if len(images) == 0:
            # continue
            path, defaultName = ntpath.split(defaultImagePath)
            images.append(defaultName)
        pi0['IMAGES'] = images
        print(pi0)
        list0.append(dict(e, **pi0))
    print(list0)
    return list0

def local_makeANewFamille(obj0):
    addedFamille = Famille()
    # obj0 = json.loads(obj0)
    self_init(Famille, addedFamille, obj0)
    try:
        db.session.add(addedFamille)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return (addedFamille.serialize())

def local_updateFamille(obj0):
    try:
        updatedFamille = db.session.query(Famille).filter_by(codefamille=obj0['codefamille']).one()
        # obj0 = json.loads(obj0)
        self_init(Famille, updatedFamille, obj0)
        db.session.add(updatedFamille)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Updated an Famille with codefamille %s' % obj0['codefamille']

def local_deleteFamille(obj0):
    try:
        FamilleToDelete = db.session.query(Famille).filter_by(codefamille=obj0).one()
        db.session.delete(FamilleToDelete)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Removed Famille with id %s' % obj0

def local_get_famille_search(obj0):
    familles = []
    if ('CODEFAMILLE' in obj0):
        familles = db.session.query(Famille).filter(func.lower(Famille.codefamille).like(func.lower(obj0['CODEFAMILLE'])), Famille.boutiq_visible==1).all()
    return [e.serialize() for e in familles]

def get_codesfamilles():
    familles = []
    familles0 = db.session.query(Famille.codefamille).filter_by(codefamille_m="TOUS", boutiq_visible=1).all()
    for f in familles0:
        familles.append(f[0])
    return familles

def getFamillePlaces(obj0):
    familles = []
    familles = db.session.query(Famille).filter_by(codefamille_m=obj0['FAMILLE_PLACES']).all()
    return [e.serialize() for e in familles]