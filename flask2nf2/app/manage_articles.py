from app import app
from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from app.models import Parametre, Article, Famille
from app import db
import json
from app.models import self_init
import datetime
import dateutil.parser
import glob
import ntpath
import random
import urllib.parse
import sqlalchemy as sa
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy.orm import create_session
from sqlalchemy import create_engine
from app import models as app_models
from sqlalchemy.sql.expression import case, null
import copy

import os
"""
api functions
"""

# articles1 = extendToImages(articles0)
def extendToImages(articles0):
    list0 = []
    imagesPath = app.config['PRODUCTS_IMAGES']
    defaultImagePath = app.config['DEFAULT_IMAGE']
    directory = os.fsencode(imagesPath)
    for e in articles0:
        pi0 = {'REF_ART': e['REF_ART'], 'IMAGES': []}
        numOfsons = null
        # app.logger.info(">>>>>>>>>>>>>>> numOfsons " + str(numOfsons))
        # numOfsons = db.session.query(Article.ref_art).filter_by(boutiq_visible=1,master_ref_art=e['REF_ART']).one_or_none()
        # app.logger.info(">>>>>>>>>>>>>>> numOfsons " + str(numOfsons))
        # if (numOfsons is not null):
        #     pi0['PARENT'] = 1
        # else:
        #     pi0['PARENT'] = 0
        if ('MASTER_REF_ART' in e and e["MASTER_REF_ART"] is not null):
            refArt = e['MASTER_REF_ART']
        else:
            refArt = e['REF_ART']
        images = []
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename == refArt:
                for file1 in os.listdir(os.fsencode(f'{imagesPath}/{filename}')):
                    imageName = os.fsdecode(file1)
                    images.append(imageName)
        if len(images) == 0:
            # path, defaultName = ntpath.split(defaultImagePath)
            defaultName = os.path.basename(os.path.normpath(defaultImagePath))
            images.append(defaultName)
        pi0['IMAGES'] = images

        list0.append(dict(e, **pi0))
        # app.logger.info(">>>>>>>>>>>>>>> list0 list0 list0 \n" + str(list0))
    return list0

def randomExtendToImages(articles0):
    numberList = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11']
    list0 = []
    for e in articles0:
        dossier0 = random.choice(numberList)
        pi0 = {'REF_ART': urllib.parse.quote(e['REF_ART']), 'DOSSIER': urllib.parse.quote(dossier0), 'IMAGES': []}
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
    return  list0



def extend1ToImages(e):
    imagesPath = app.config['PRODUCTS_IMAGES']
    defaultImagePath = app.config['DEFAULT_IMAGE']
    directory = os.fsencode(imagesPath)
    pi0 = {'REF_ART': urllib.parse.quote(e['REF_ART']), 'IMAGES': []}
    refArt = e['REF_ART']
    images = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename == refArt:
            for file1 in os.listdir(os.fsencode(f'{imagesPath}/{filename}')):
                imageName = os.fsdecode(file1)
                images.append(imageName)
    if len(images) == 0:
        path, defaultName = ntpath.split(defaultImagePath)
        images.append(defaultName)
    pi0['IMAGES'] = images
    e0 = dict(e, **pi0)
    return e0


def extend1ToImagesRandom(e):
    numberList = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11']
    list0 = []
    dossier0 = random.choice(numberList)
    pi0 = {'REF_ART': urllib.parse.quote(e['REF_ART']), 'DOSSIER': urllib.parse.quote(dossier0), 'IMAGES': []}
    path0 = app.config['UPLOAD_FOLDER'] + '/' + dossier0
    # app.logger.info(">>>>>>>>>>>>>>> path " + path0)
    list1 = glob.glob(path0 + "/*.*")
    images0 = []
    for file0 in list1:
        # app.logger.info(">>>>>>>>>>>>>>> filename " + file0)
        images0.append(urllib.parse.quote(ntpath.basename(file0)))
        # app.logger.info(">>>>>>>>>>>>>>> filename " + file0)
    pi0['IMAGES'] = images0
    e0 = dict(e, **pi0)
    return  e0



def all_sfamilles(codes0):
    # print(" >>>>>>>>>>>>>>>0> "+ str(codes0), flush=True)
    familles0 = db.session.query(Famille).filter(Famille.codefamille_m.in_(codes0))
    codes1 = [fam0.codefamille for fam0 in familles0]
    # print(" >>>>>>>>>>>>>>>1> "+ str(codes1), flush=True)
    codes2 = []
    news0 = []
    if codes1 != []:
        codes2 = all_sfamilles(codes1)
        news0 = codes0 + codes2
    else:
        news0 = codes0 + codes1
    print(" >>>>>>>>>>>>>>>S_FAMILIES> "+ str(news0), flush=True)
    return  news0



def local_get_articles(nbrows0):
    articles = []
    articlesCount = 0
    try:
        if nbrows0==0:
          articles = db.session.query(Article).all()
          app.logger.info("\n>>>>>>>>>>>>>>>>>>>>> Articles Articles Articles\n" + str(articles))
        else:
          articlesCount = db.session.query(Article.ref_art).count()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        if nbrows0==1:
            return 0
        else:
            return []
    if nbrows0==1:
        return articlesCount
    else:
        return extendToImages([e.serialize() for e in articles])
    # articles = db.session.query(Article).all()
    # return jsonify(articles=[a.serialize for a in articles])

def local_get_articles_images():
    numberList = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11']
    articles = db.session.query(Article).all()
    list0 = []
    for e in articles:
        dossier0 = random.choice(numberList)
        pi0 = {'ref_art': urllib.parse.quote(e.ref_art), 'dossier': urllib.parse.quote(dossier0), 'images': []}
        path0 = app.config['UPLOAD_FOLDER'] + '/' + dossier0
        # app.logger.info(">>>>>>>>>>>>>>> path " + path0)
        list1 = glob.glob(path0 + "/*.*")
        images0 = []
        for file0 in list1:
            # app.logger.info(">>>>>>>>>>>>>>> filename " + file0)
            images0.append(urllib.parse.quote(ntpath.basename(file0)))
            # app.logger.info(">>>>>>>>>>>>>>> filename " + file0)
        pi0['images'] = images0
        list0.append(pi0)
    return  list0

def local_get_articles_search_refArt(obj0):
    articles = []
    articlesCount = 0
    if ('REF_ART' in obj0):
        articles = db.session.query(Article).filter(func.lower(Article.ref_art).like(func.lower(obj0['REF_ART'])), Article.boutiq_visible==1).order_by(Article.ref_art.asc()).limit(50)
    return [e.serialize() for e in articles]
def local_get_articles_search_design(obj0, nbrows0):
    articles = []
    articlesCount = 0
    try:
        if ('LBrowArticles' in obj0):
            if nbrows0==1:
                articlesCount = db.session.query(Article.ref_art).filter(func.lower(Article.designation).like(func.lower('%'+obj0['PREM_DESIGNATION'])))[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])].count()
            else:
                if obj0['sort_type'] == "NOUV_ARTICLE" :
                    articles = db.session.query(Article).filter(func.lower(Article.designation).like(func.lower(obj0['PREM_DESIGNATION'])), Article.boutiq_visible==1).order_by(Article.date_creation.desc())[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])]
                elif obj0['sort_type'] == "PRIX_CROISSANT" :
                    articles = db.session.query(Article).filter(func.lower(Article.designation).like(func.lower(obj0['PREM_DESIGNATION'])), Article.boutiq_visible==1).order_by(Article.prixventettc.asc())[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])]
                elif obj0['sort_type'] == "PRIX_DECROISSANT" :
                    articles = db.session.query(Article).filter(func.lower(Article.designation).like(func.lower(obj0['PREM_DESIGNATION'])), Article.boutiq_visible==1).order_by(Article.prixventettc.desc())[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])]
                elif obj0['sort_type'] == "ORDRE_ALPHABETIQUE" :
                    articles = db.session.query(Article).filter(func.lower(Article.designation).like(func.lower(obj0['PREM_DESIGNATION'])), Article.boutiq_visible==1).order_by(Article.designation)[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])]
                else:
                    articles = db.session.query(Article).filter(func.lower(Article.designation).like(func.lower(obj0['PREM_DESIGNATION'])), Article.boutiq_visible==1)[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])]
        else:
            if nbrows0==1:
                articlesCount = db.session.query(Article.ref_art).filter(func.lower(Article.designation).like(func.lower(obj0['PREM_DESIGNATION'])), Article.boutiq_visible==1).count()
            else:
                articles = db.session.query(Article).filter(func.lower(Article.designation).like(func.lower(obj0['PREM_DESIGNATION'])))
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        if nbrows0==1:
            return 0
        else:
            return []
    if nbrows0==1:
        return  articlesCount
    else:
        return  extendToImages([e.serialize() for e in articles])



    # families: (2) ["NIVEA", "BIOBAIL"]
    # availability: (3) ["Active", "Upcoming", "Missed"]
    # money: {min: 19863, max: 100000}
# http://www.leeladharan.com/sqlalchemy-query-with-or-and-like-common-filters
def local_get_articles_search_mult(obj0, nbrows0):
    articles = []
    articlesCount0 = 0
    try:
        if ('LBrowArticles' in obj0):
            if nbrows0==0:
                if obj0['sort_type'] == "NOUV_ARTICLE" :
                    articles = db.session.query(Article).filter(Article.codefamille.in_(all_sfamilles(obj0['LIST_REF_FAMILLES'])), Article.prixventettc >= obj0['money']['min'], Article.prixventettc <= obj0['money']['max']).order_by(Article.date_creation.desc())[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])]
                elif obj0['sort_type'] == "PRIX_CROISSANT" :
                    articles = db.session.query(Article).filter(Article.codefamille.in_(all_sfamilles(obj0['LIST_REF_FAMILLES'])), Article.prixventettc >= obj0['money']['min'], Article.prixventettc <= obj0['money']['max']).order_by(Article.prixventettc.asc())[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])]
                elif obj0['sort_type'] == "PRIX_DECROISSANT" :
                    articles = db.session.query(Article).filter(Article.codefamille.in_(all_sfamilles(obj0['LIST_REF_FAMILLES'])), Article.prixventettc >= obj0['money']['min'], Article.prixventettc <= obj0['money']['max']).order_by(Article.prixventettc.desc())[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])]
                elif obj0['sort_type'] == "ORDRE_ALPHABETIQUE" :
                    articles = db.session.query(Article).filter(Article.codefamille.in_(all_sfamilles(obj0['LIST_REF_FAMILLES'])), Article.prixventettc >= obj0['money']['min'], Article.prixventettc <= obj0['money']['max']).order_by(Article.designation)[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])]
                else:
                    articles = db.session.query(Article).filter(Article.codefamille.in_(all_sfamilles(obj0['LIST_REF_FAMILLES'])), Article.prixventettc >= obj0['money']['min'], Article.prixventettc <= obj0['money']['max'])[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])]
            else:
                articlesCount0 = db.session.query(Article.ref_art).filter(Article.codefamille.in_(all_sfamilles(obj0['LIST_REF_FAMILLES'])), Article.prixventettc >= obj0['money']['min'], Article.prixventettc <= obj0['money']['max'])[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])].count()
        else:
            if nbrows0==0:
                articles = db.session.query(Article).filter(Article.codefamille.in_(all_sfamilles(obj0['LIST_REF_FAMILLES'])), Article.prixventettc >= obj0['money']['min'], Article.prixventettc <= obj0['money']['max'])
            else:
                if 'money' in obj0:
                    articlesCount0 = db.session.query(Article.ref_art).filter(Article.codefamille.in_(all_sfamilles(obj0['LIST_REF_FAMILLES'])), Article.prixventettc >= obj0['money']['min'], Article.prixventettc <= obj0['money']['max'], Article.boutiq_visible==1).count()
                else:
                    articlesCount0 = db.session.query(Article.ref_art).filter(Article.codefamille.in_(all_sfamilles(obj0['LIST_REF_FAMILLES'])), Article.boutiq_visible==1).count()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        if nbrows0==0:
            return []
        else:
            return 0
    if nbrows0==0:
        return extendToImages([e.serialize() for e in articles])
    else:
        return articlesCount0


def local_get_article_from_famille(codefamille0):
    articles = 0
    try:
        articles = db.session.query(Article).filter(Article.codefamille.in_(all_sfamilles(codefamille0))).filter_by(boutiq_visible=1).count()
        # articles = db.session.query(Article).filter_by(boutiq_visible=1).all()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return []
    app.logger.info(">>>>>>>>>>>>>>>>>>>>> ERROR ERROR ERROR ERROR")
    return articles

def local_get_article_from_famille_nf2(codefamille0):
    articles = []
    try:
        articles = db.session.query(Article).filter(Article.codefamille.in_(all_sfamilles([codefamille0]))).all()
        # articles = db.session.query(Article).filter_by(boutiq_visible=1).all()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return []
    app.logger.info(">>>>>>>>>>>>>>>>>>>>> ERROR ERROR ERROR ERROR")
    return [e.serialize() for e in articles]
def get_articales_from_famille(codefamille0):
    articles = []
    try:
        articles = db.session.query(Article).filter_by(codefamille = codefamille0).order_by(Article.designation).all()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return []
    app.logger.info(">>>>>>>>>>>>>>>>>>>>> ERROR ERROR ERROR ERROR")
    return extendToImages([e.serialize() for e in articles])

def local_get_article(obj0):
    articles = []
    if (obj0 == ''):
        try:
            articles = db.session.query(Article).all()
        except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
            app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
            return []
        return extendToImages([e.serialize() for e in articles])
    else:
        
        articles = db.session.query(Article).filter_by(ref_art=obj0).one()
        return extend1ToImages(articles.serialize())


# https://kite.com/python/docs/sqlalchemy.orm.session.Session.execute
# How to: Get the first two rows from a query after skipping a row
# q = session.query(User).offset(1).limit(2)
# q = session.query(User)[1:3]
#*************[debut1:fin1]
#*************[fin1-1:fin2] ...
def local_get_article_interval(obj0, nbrows0):
    articles = []
    articlesCount0 = 0
    try:
        if nbrows0==0:
            articles = db.session.query(Article)[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])]
        else:
            articlesCount0 = db.session.query(Article.ref_art)[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])].count()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        if nbrows0==0:
            return []
        else:
            return 0
    if nbrows0==0:
      return extendToImages([e.serialize() for e in articles])
    else:
        return articlesCount0

def local_get_article_famille_interval(obj0, nbrows0):
    articles = []
    articlesCount0 = 0
    try:
        if nbrows0==0:
            if obj0['sort_type'] == "NOUV_ARTICLE" :
                articles = db.session.query(Article).filter(Article.codefamille.in_(all_sfamilles([obj0['codefamille']]))).order_by(Article.date_creation.desc())[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])]
            elif obj0['sort_type'] == "PRIX_CROISSANT" :
                articles = db.session.query(Article).filter(Article.codefamille.in_(all_sfamilles([obj0['codefamille']]))).order_by(Article.prixventettc.asc())[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])]
            elif obj0['sort_type'] == "PRIX_DECROISSANT" :
                articles = db.session.query(Article).filter(Article.codefamille.in_(all_sfamilles([obj0['codefamille']]))).order_by(Article.prixventettc.desc())[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])]
            elif obj0['sort_type'] == "ORDRE_ALPHABETIQUE" :
                articles = db.session.query(Article).filter(Article.codefamille.in_(all_sfamilles([obj0['codefamille']]))).order_by(Article.designation)[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])]
            else:
                articles = db.session.query(Article).filter(Article.codefamille.in_(all_sfamilles([obj0['codefamille']]))).order_by(Article.date_creation.desc())[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])]

        else:
            articlesCount0 = db.session.query(Article.ref_art).filter(Article.codefamille.in_(all_sfamilles([obj0['codefamille']])), Article.boutiq_visible == 1)[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])].count()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        if nbrows0==0:
            return []
        else:
            return 0
    if nbrows0==0:
        return extendToImages([e.serialize() for e in articles])
    else:
        return articlesCount0


def local_nf2_get_article_famille_interval(obj0):
    articles = []
    articlesCount0 = 0
    try:
            if (obj0['LBrowArticles'] == -1 and obj0['UBrowArticles'] == -1):
                if (obj0['count'] == 1):
                    articles = db.session.query(Article).filter(Article.codefamille.in_(all_sfamilles([obj0['codefamille']]))).order_by(Article.date_creation.desc()).count()
                else:
                    articles = db.session.query(Article).filter(Article.codefamille.in_(all_sfamilles([obj0['codefamille']]))).order_by(Article.date_creation.desc()).all()
            elif (obj0['codefamille'] != '' and obj0['search_value'] == '') :
                if (obj0['count'] == 1):
                    articlesCount0 = db.session.query(Article).filter(Article.codefamille.in_(all_sfamilles([obj0['codefamille']]))).count()
                else:
                    articles = db.session.query(Article).filter(Article.codefamille.in_(all_sfamilles([obj0['codefamille']]))).order_by(Article.date_creation.desc())[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])]
            elif (obj0['codefamille'] != '' and obj0['search_value'] != '' and obj0['search_column'] == 'DESIGNATION'):
                if (obj0['count'] == 1):
                    articlesCount0 = rticles = db.session.query(Article).filter(Article.codefamille.in_(all_sfamilles([obj0['codefamille']])), func.upper(Article.designation).like(func.upper(f"%{obj0['search_value']}%"))).count()
                else:
                    articles = db.session.query(Article).filter(Article.codefamille.in_(all_sfamilles([obj0['codefamille']])), func.upper(Article.designation).like(func.upper(f"%{obj0['search_value']}%"))).order_by(Article.date_creation.desc())[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])]
            elif (obj0['codefamille'] != '' and obj0['search_value'] != '' and obj0['search_column'] == 'REF_ART'):
                if (obj0['count'] == 1):
                    articlesCount0 = rticles = db.session.query(Article).filter(Article.codefamille.in_(all_sfamilles([obj0['codefamille']])), func.upper(Article.ref_art).like(func.upper(f"%{obj0['search_value']}%"))).count()
                else:
                    articles = db.session.query(Article).filter(Article.codefamille.in_(all_sfamilles([obj0['codefamille']])), func.upper(Article.ref_art).like(func.upper(f"%{obj0['search_value']}%"))).order_by(Article.date_creation.desc())[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])]
            else:
                articles = db.session.query(Article).filter(Article.codefamille.in_(all_sfamilles([obj0['codefamille']]))).order_by(Article.date_creation.desc())[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'])]
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        if obj0['count'] == 0:
            return []
        else:
            return 0
    if (obj0['count'] == 0):
        return [e.serialize() for e in articles]
    else:
        return articlesCount0
def local_makeANewArticle(obj0):
    addedarticle = Article()
    # obj0 = json.loads(obj0)
    self_init(Article, addedarticle, obj0)
    try:
        db.session.add(addedarticle)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return extend1ToImages(addedarticle.serialize())

def local_updateArticle(obj0):
    try:
        updatedArticle = db.session.query(Article).filter_by(ref_art=obj0['ref_art']).one()
        # obj0 = json.loads(obj0)
        self_init(Article, updatedArticle, obj0)
        db.session.add(updatedArticle)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Updated an Article with ref_art %s' % obj0['ref_art']


def local_deleteArticle(ref_art0):
    try:
        articleToDelete = db.session.query(Article).filter_by(ref_art=ref_art0).one()
        db.session.delete(articleToDelete)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Removed Article with id %s' % ref_art0


    # if 'datedebpromo' in obj0:
    #   addedarticle.datedebpromo = dateutil.parser.parse(obj0['datedebpromo'])
    # if 'datefinpromo' in obj0:
    #   addedarticle.datefinpromo = dateutil.parser.parse(obj0['datefinpromo'])
    # if 'dateperemp' in obj0:
    #   addedarticle.dateperemp = dateutil.parser.parse(obj0['dateperemp'])
    # if 'date_creation' in obj0:
    #   addedarticle.date_creation = dateutil.parser.parse(obj0['date_creation'])

    # if 'datedebpromo' in obj0:
    #   updatedArticle.datedebpromo = dateutil.parser.parse(obj0['datedebpromo'])
    # if 'datefinpromo' in obj0:
    #   updatedArticle.datefinpromo = dateutil.parser.parse(obj0['datefinpromo'])
    # if 'dateperemp' in obj0:
    #   updatedArticle.dateperemp = dateutil.parser.parse(obj0['dateperemp'])
    # if 'date_creation' in obj0:
    #   updatedArticle.date_creation = dateutil.parser.parse(obj0['date_creation'])
# #######################################################Zakaria#################################
def extend1ToImagesList(articles):
    imagesPath = app.config['PRODUCTS_IMAGES']
    defaultImagePath = app.config['DEFAULT_IMAGE']
    directory = os.fsencode(imagesPath)
    e1 = []
    for e in articles :
        e = e.serialize()
        pi0 = {'REF_ART': urllib.parse.quote(e['REF_ART']), 'IMAGES': []}
        refArt = e['REF_ART']
        images = []
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename == refArt:
                for file1 in os.listdir(os.fsencode(f'{imagesPath}/{filename}')):
                    imageName = os.fsdecode(file1)
                    images.append(imageName)
        if len(images) == 0:
            path, defaultName = ntpath.split(defaultImagePath)
            images.append(defaultName)
        pi0['IMAGES'] = images
        e0 = dict(e, **pi0)
        e1.append(e0)
    return e1

def local_get_article_list(obj0):
    articles = []
    if (obj0 == []):
        try:
            articles = db.session.query(Article).all()
        except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
            app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
            return []
        return extendToImages([e.serialize() for e in articles])
    else:
        ordering = case(
            {ref_art: index for index, ref_art in enumerate(obj0)},
            value=Article.ref_art
         )
        articles = db.session.query(Article).filter(Article.ref_art.in_(obj0)).order_by(ordering).all()
        return extend1ToImagesList(articles)

def local_nf2_get_article_list(obj0):
    articles = []
    try:
        articles = db.session.query(Article).filter(Article.ref_art.in_(obj0)).all()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return [e.serialize() for e in articles]

def local_get_no_stock(obj0, with_stock):
    # app.logger.info(">>>>>>>>>>>>>>>>>>>>> QTE QTE QTE QTE QTE" + str(obj0))
    lb0 = int(obj0['LBrowArticles'])
    ub0 = int(obj0['UBrowArticles'])
    articles = []
    try:
        if ('PREM_REF_ART' not in obj0):
            obj0['PREM_REF_ART'] = '%'
        if ('PREM_DESIGNATION' not in obj0):
            obj0['PREM_DESIGNATION'] = '%'
        if ('CODE_DEPOT' not in obj0):
            obj0['CODE_DEPOT'] = '%'
        if ('CODE_FAM' not in obj0):
            obj0['CODE_FAM'] = 'TOUS'
        if ('sort_type' not in obj0):
            obj0['sort_type'] = '%'
        if ('ITEM_QTE' not in obj0):
            obj0['ITEM_QTE'] = '10'
        if ('ITEM_QTEPARCOLIS' not in obj0):
            obj0['ITEM_QTEPARCOLIS'] = '10'
        if ('EMAILNET' not in obj0):
            obj0['EMAILNET'] = ''
        #
        if ('MASTER_REF_ART' not in obj0):
            obj0['MASTER_REF_ART'] = ''
        if ('CODE_TYPE_TARIF' not in obj0):
            obj0['CODE_TYPE_TARIF'] = ''
        if ('FAMILLES_CONCAT' not in obj0):
            obj0['FAMILLES_CONCAT'] = ''
        if ('VISIBLE' not in obj0):
            obj0['VISIBLE'] = 1
        if ('ARTICLES_CONCAT' not in obj0):
            obj0['ARTICLES_CONCAT'] = ''
        if ('WITH_STOCK' not in obj0):
            obj0['WITH_STOCK'] = '1'

        data1 = {'PREM_REF_ART':obj0['PREM_REF_ART'], 'CODE_FAM':obj0['CODE_FAM'], 'CODE_DEPOT':obj0['CODE_DEPOT'], 'PREM_DESIGNATION':obj0['PREM_DESIGNATION'],
            'ITEM_QTE': obj0['ITEM_QTE'], 'ITEM_QTEPARCOLIS': obj0['ITEM_QTEPARCOLIS'], 'EMAILNET': obj0['EMAILNET'], 'MASTER_REF_ART': obj0['MASTER_REF_ART'],
            'CODE_TYPE_TARIF': obj0['CODE_TYPE_TARIF'], 'FAMILLES_CONCAT': obj0['FAMILLES_CONCAT'], 'ARTICLES_CONCAT': obj0['ARTICLES_CONCAT'],
            'WITH_STOCK': obj0['WITH_STOCK']}

        condition0 =  " where (Upper(A.REF_ART) like Upper(:PREM_REF_ART)) and (Upper(A.DESIGNATION) like Upper(:PREM_DESIGNATION)) "
        condition0 += " and ((COALESCE(:FAMILLES_CONCAT, '')='') or (position('^'||A.CODEFAMILLE||'^' in :FAMILLES_CONCAT)>0)) "
        condition0 += " and ((COALESCE(:ARTICLES_CONCAT, '')='') or (position('^'||A.REF_ART||'^' in :ARTICLES_CONCAT)>0)) "
        if (obj0['MASTER_REF_ART'] == '%'):
            pass
        elif (obj0['MASTER_REF_ART'] == ''):
            condition0 += " and (COALESCE(A.MASTER_REF_ART, '') = '') "
        else :
            condition0 += " and (Upper(A.MASTER_REF_ART) = Upper(:MASTER_REF_ART)) "

        if ('money' in obj0):
            condition0 += " and (A.prixventettc >= {min_money}) and (A.prixventettc <= {max_money}) ".format(min_money=obj0['money']['min'],max_money=obj0['money']['max'])
        if (obj0['VISIBLE'] == 1):
            condition0 += " and (A.BOUTIQ_VISIBLE = 1)"

        orderby0 = "ORDER BY A.DATE_CREATION DESC"
        if obj0['sort_type'] == "NOUV_ARTICLE" :
            orderby0 = "ORDER BY A.DATE_CREATION DESC"
        elif obj0['sort_type'] == "PRIX_CROISSANT" :
            orderby0 = "ORDER BY PRIXVENTETTC ASC"
        elif obj0['sort_type'] == "PRIX_DECROISSANT" :
            orderby0 = "ORDER BY PRIXVENTETTC DESC"
        elif obj0['sort_type'] == "ORDRE_ALPHABETIQUE" :
            orderby0 = "ORDER BY A.DESIGNATION ASC"
        else: 
            orderby0 = ""

        rows0 = ''
        if (lb0 != -1):
            if ('firebird+fdb:' in app.config['SQLALCHEMY_DATABASE_URI']):
                rows0 = ' rows ' + str(lb0+1) + ' to ' + str(ub0)
            else:
                rows0 = ' offset ' + str(lb0) + ' limit ' + str(ub0-lb0)

        datecurr0 = ''
        if ('firebird+fdb:' in app.config['SQLALCHEMY_DATABASE_URI']):
            datecurr0 = 'select current_timestamp from rdb$database'
        else:
            datecurr0 = 'SELECT CURRENT_DATE'

        sql_champs0 = ''
        sql_table0 = ''
        if with_stock:
            sql_champs0 = ', s.QTE QTE_TOT,'
            if ('firebird+fdb:' in app.config['SQLALCHEMY_DATABASE_URI']): 
                sql_table0 = 'spart(:CODE_FAM, :CODE_DEPOT, :PREM_REF_ART, :PREM_DESIGNATION) s left join article A on (s.REF_ART = A.REF_ART)'
            else:
                sql_table0 = 'stockart s left join article A on (s.REF_ART = A.REF_ART)'
        else:
            sql_champs0 = ', 0 QTE_TOT,'
            sql_table0 = 'article A'


        if ('firebird+fdb:' in app.config['SQLALCHEMY_DATABASE_URI']): 
            sql_champs0 += ' (select count(1) from article AA where (AA.boutiq_visible=1) and (AA.master_ref_art=A.REF_ART) rows 1 to 1) EXISTS_CHILDREN,'
        else:
            sql_champs0 += ' (select count(1) from article AA where (AA.boutiq_visible=1) and (AA.master_ref_art=A.REF_ART) LIMIT 1) EXISTS_CHILDREN,'

        # sql_champs0 += ' 0 EXISTS_CHILDREN,'

        #          when (A.DATEDEBPROMO <= ({DATE_CURR})) and (A.DATEFINPROMO >= ({DATE_CURR})) and (A.ACTIVEPROMO = 1) then A.PRIXHTPROMO
        #          when (A.DATEDEBPROMO <= ({DATE_CURR})) and (A.DATEFINPROMO >= ({DATE_CURR})) and (A.ACTIVEPROMO = 1) then A.PRIXTTCPROMO
        sql_gener = """
            select A.REF_ART, A.MASTER_REF_ART, A.DATE_CREATION, A.DESIGNATION, A.CODEFAMILLE, A.DETAIL, A.HTMLDETAIL,A.ACTIVEPROMO, A.DATEDEBPROMO, A.DATEFINPROMO, A.PRIXTTCPROMO {SQL_CHAMPS}
                case
                  when COALESCE(AR.PRIXHT, 0) <> 0 then AR.PRIXHT
                  when A.TARIF_P_QTE = 1 then  COALESCE(ta.PRIXHT, A.PRIXVENTEHT)
                  when A.TARIF_P_QTE = 2 then COALESCE(ta2.PRIXHT, A.PRIXVENTEHT) 
                else  A.PRIXVENTEHT 
                end PRIXVENTEHT, 
                case
                  when COALESCE(AR.PRIXHT, 0) <> 0 then AR.PRIXHT*(1 + A.TAUX_TVA/100) 
                  when A.TARIF_P_QTE = 1 then  COALESCE(ta.PRIXHT*(1 + A.TAUX_TVA/100), A.PRIXVENTETTC)
                  when A.TARIF_P_QTE = 2 then COALESCE(ta2.PRIXHT*(1 + A.TAUX_TVA/100), A.PRIXVENTETTC) 
                else  A.PRIXVENTETTC 
                end PRIXVENTETTC
            from {SQL_TABLE} 
            	left join TARIF AR on ((AR.REF_ART = A.REF_ART) and (AR.code_type_tarif = 
                  (select TI.code_type_tarif from TIERS TI where TI.email=:EMAILNET)))
                left join TARIF ta on ((A.TARIF_P_QTE = 1) and (ta.REF_ART=A.ref_art) and (:ITEM_QTEPARCOLIS >= ta.QTEMIN) and (:ITEM_QTEPARCOLIS <= ta.QTEMAX)) 
                left join TARIF ta2 on ((A.TARIF_P_QTE = 2) and (ta2.REF_ART=A.ref_art) and (:ITEM_QTE >= ta2.QTEMIN) and (:ITEM_QTE <= ta2.QTEMAX)) 
            {CONDITION} {ORDERBY} {ROWS}
            """.format(CONDITION=condition0, ORDERBY=orderby0, DATE_CURR=datecurr0, ROWS=rows0, SQL_CHAMPS=sql_champs0, SQL_TABLE=sql_table0)

        # numOfsons = db.session.query(Article.ref_art).filter_by(boutiq_visible=1,master_ref_art=e['REF_ART']).one_or_none()

        # app.logger.info("<<<<<<<<<<<<<<<<<<<<<<<<<< " + sql_gener)
        articles = app_models.query_result_serial(sql_gener, data1, ["photo"])
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        return []
    return extendToImages(articles)

def local_get_no_stock_familles(obj0, with_stock):
    list0 = []
    fams0 = ''
    for ref_famille0 in obj0['LIST_REF_FAMILLES']:
        # fams0 = fams0 + ' ' + ref_famille0
        for ref_famille1 in all_sfamilles([ref_famille0]):
            fams0 = fams0 + '^' + ref_famille1 + '^'
    arg0 = {'FAMILLES_CONCAT': fams0}
    arg0 = dict(arg0, **obj0)
    articles0 = local_get_no_stock(arg0, with_stock)
    list0 = articles0
    return list0

def local_get_no_stock_articles(obj0, with_stock):
    list0 = []
    # app.logger.info(">>>>>>>>>>>>>>> local_get_stock_articles arguments: " + str(obj0))
    # for ref_art0 in obj0['LIST_REF_ARTICLES']:
    #     arg0 = {'PREM_REF_ART': ref_art0, 'LBrowArticles':0, 'UBrowArticles':1}
    #     arg0 = dict(arg0, **obj0)
    #     articles0 = local_get_no_stock(arg0)
    #     app.logger.info(">>>>>>>>>>>>>>> article stock " + str(articles0))
    #     list0 = list0 + articles0
    arts0 = ''
    for ref_art0 in obj0['LIST_REF_ARTICLES']:
        arts0 = arts0 + '^' + ref_art0 + '^'
        print(arts0)
    arg0 = {'ARTICLES_CONCAT': arts0}
    arg0 = dict(arg0, **obj0)
    articles0 = local_get_no_stock(arg0, with_stock)
    list0 = articles0
    return list0
