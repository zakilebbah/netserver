from base64 import decode
from sqlalchemy.sql.functions import func
from app import app
from app import db
from app import auth
from app.models import self_init
from app import manage_articles as m_article
from app import manage_cbanque as m_cbanque
from app import manage_fam_tiers as m_fam_tiers
from app import manage_famille as m_famille
from app import manage_item as m_item
from app import manage_local_type_piece as m_local_type_piece
from app import manage_parametre as m_parametre
from app import manage_piece as m_piece
from app import manage_tarif as m_tarif
from app import manage_tiers as m_tiers
from app import manage_users as m_user
from app import manage_type_piece as m_type_piece
from app import manage_utilisateurs as m_utilisateurs
from app import manage_mode_regl as m_mode_regl
from app import manage_mode_liv as m_mode_liv
from app import manage_gps_positions as m_gps_positions
from app import manage_images as m_images
from flask import Flask, abort, request, flash, g, url_for, redirect, render_template, jsonify
import json
from flask_cors import CORS
from flask import jsonify
from flask import send_file
import sys
import logging
from app.models import Parametre, Article, Tiers, Famille, User, Piece
import importlib
import pprint
from flask_cors import CORS, cross_origin
import glob
import os
from logging.handlers import RotatingFileHandler
import logging.handlers as handlers
from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from flask_login import login_user
from flask import Blueprint
from werkzeug.utils import secure_filename
import weasyprint
import yagmail
import pdfkit 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from os import path
import pathlib
import time
import secrets
import string
import shutil  
from barcode import Code128
from barcode.writer import ImageWriter
import pdfkit
import base64
import requests
main = Blueprint('main', __name__)

# import cStringIO as StringIO

# from cloghandler import ConcurrentRotatingFileHandler
# handler = logging.FileHandler(app.config['ERRORS_LOGGER'])  # errors logged to this file
# handler.setLevel(logging.DEBUG)  # setLevel(logging.ERROR) : only log errors and above
# app.logger.addHandler(handler)

# CRITICAL 50
# ERROR 40
# WARNING 30
# INFO 20
# DEBUG 10
# NOTSET 0

LOG_LEVEL = 20
LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(message)s"
logging.basicConfig(
    handlers=[RotatingFileHandler(filename=app.config['ERRORS_LOGGER'], maxBytes=1024*1024, backupCount=10)],
    format=LOG_FORMAT, 
    level=LOG_LEVEL)
# logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
sq_log = logging.getLogger('sqlalchemy.engine')
# sq_log.setLevel(logging.CRITICAL)
# remove any preconfigured handlers there might be
for h in sq_log.handlers:
    sq_log.removeHandler(h)
    h.close()

# LOG_LEVEL = 20
# LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(message)s"
# logging.basicConfig(
#     filename=app.config['ERRORS_LOGGER'], 
#     format=LOG_FORMAT, 
#     level=LOG_LEVEL)
# logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)


# LOG_FORMAT = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
# logger = logging.getLogger('')
# logger.setLevel(LOG_LEVEL)
# handler = RotatingFileHandler(app.config['ERRORS_LOGGER'], maxBytes=10*1024, backupCount=10)
# handler.setFormatter(LOG_FORMAT)
# logger.addHandler(handler)
# logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)



# logging.getLogger('sqlalchemy.dialects').setLevel(LOG_LEVEL)
# logging.getLogger('sqlalchemy.pool').setLevel(LOG_LEVEL)
# logging.getLogger('sqlalchemy.orm').setLevel(LOG_LEVEL)
# logging.getLogger('sqlalchemy').propagate = True

# debug_handler = logging.FileHandler(app.config['ERRORS_LOGGER'])
# debug_handler.setLevel(logging.DEBUG)
# app.logger.addHandler(debug_handler)
# # get logger for SQLAlchemy
# sq_log = logging.getLogger('sqlalchemy.engine')
# sq_log.setLevel(logging.DEBUG)
# # remove any preconfigured handlers there might be
# for h in sq_log.handlers:
#     sq_log.removeHandler(h)
#     h.close()
# # Now, SQLAlchemy should not have any handlers at all. Let's add one
# # for the logfile
# sq_log.addHandler(debug_handler)

# handler_sql = logging.FileHandler(app.config['ERRORS_LOGGER'])
# handler_sql.setFormatter(logging.Formatter(LOG_FORMAT))
# sql_logger = logging.getLogger('sqlalchemy.engine')
# sql_logger.setLevel(LOG_LEVEL)
# sql_logger.addHandler(handler_sql)



# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@main.route('/index')
def index():
    app.logger.info('Logging to ' + app.config['ERRORS_LOGGER'])
    app.logger.info('Processing default request')
    return "Hello, World!"

# *********************************************
# *********************************************
# *********************************************
# ancien api-auth

# @main.route('/api-auth/login', methods=['POST'])
# def login():
#     json_data = request.json
#     user = Utilisateurs.query.join(Tiers, Utilisateurs.code_tiers==Tiers.code_tiers).filter(Tiers.email==json_data['email']).first()
#     if user and Bcrypt.check_password_hash(user.pass_field, json_data['password']):
#         session['logged_in'] = True
#         status = True
#     else:
#         status = False
#     return jsonify({'result': status})


# @main.route('/api-auth/logout')
# def logout():
#     session.pop('logged_in', None)
#     return jsonify({'result': 'success'})


# @main.route('/api-auth/status')
# def status():
#     if session.get('logged_in'):
#         if session['logged_in']:
#             return jsonify({'status': True})
#     else:
#         return jsonify({'status': False})


# *********************************************
# *********************************************
# *********************************************
# https://blog.miguelgrinberg.com/post/restful-authentication-with-flask

# @auth.verify_password
# def verify_password(username, password):
#     user = db.session.query(User).filter_by(usernamenet = username).first()
#     if not user or not user.verify_password(password):
#         return False
#     g.user = user
#     return True

# $ curl -u miguel:python -i -X GET http://127.0.0.1:5000/api/token
# $ curl -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTM4NTY2OTY1NSwiaWF0IjoxMzg1NjY5MDU1fQ.eyJpZCI6MX0.XbOEFJkhjHJ5uRINh2JA1BPzXjSohKYDRT472wGOvjc:unused -i -X GET http://127.0.0.1:5000/api/resource

@auth.verify_password
def verify_password(username_or_token, password):
    app.logger.info(">>>>>>>>>>>>>>> 1ST INPUT TOKEN : " + str(username_or_token))
    user = Tiers.verify_auth_token(username_or_token)
    if not user:
        app.logger.info(">>>>>>>>>>>>>>> NO TOKEN ")
        user = db.session.query(Tiers).filter_by(email=username_or_token).first()
        if not user:
            app.logger.info(">>>>>>>>>>>>>>> NO USER ")
            # return jsonify({'status': 'not exists'})
            return False
        elif not user.verify_password(password):
            app.logger.info(">>>>>>>>>>>>>>> NO USER ")
            # return jsonify({'status': 'pass-error'})
            return False
        else:
            app.logger.info(">>>>>>>>>>>>>>> USER ")
    else:
        app.logger.info(">>>>>>>>>>>>>>> TOKEN ")
    g.tiers = user
    return True


@main.route('/api-bab/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.emai})


@main.route('/api-bab/signup', methods=['POST'])
def new_user():
    req = request.get_json()
    obj0 = req
    app.logger.info(req)
    app.logger.info(obj0)
    username = request.json.get('usernamenet')
    password = request.json.get('passwordnet')
    email = request.json.get('email')
    if (username is None) or (password is None) or (email is None) or (username == "") or (password == "") or (email == ""):
        return jsonify({'status': 'error', 'error': 'arguments manquant'})    # missing arguments
    user0 = db.session.query(Tiers).filter(Tiers.email==email).first()        
    if user0 is not None:
        return jsonify({'status': 'exists', 'user': user0.serialize()}) 
    # is_valid = validate_email(str(email))  
    # if not is_valid :
    #     return jsonify({'status': 'email_Not_Exist'}) 
    # user = Utilisateurs(username=username)
    ret0 = m_user.local_makeANewUser(obj0)
    return jsonify({'status': 'new', 'user': ret0})    # missing arguments


@main.route('/api-bab/getuser', methods=['GET', 'POST'])
def get_user():
    if request.is_json:
        user0 = request.json.get('email')
        user = db.session.query(Tiers).filter_by(email=user0).first()
        if not user:
            return jsonify({'status': 'error', 'error': 'not exists'})    # missing arguments
            # abort(400)
        else:
            user0 = m_user.local_get_User(user0)
            user0['PASSWORDNET'] = ''
            return jsonify({'status': 'exists', 'user': user0})    # missing arguments
    else:
        return jsonify({'status': 'error', 'error': 'not json'})    # missing arguments
        # abort(400)

@main.route('/api-bab/token', methods=['GET', 'POST'])
@auth.login_required
def get_auth_token():
    app.logger.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> TOKEN TOKEN TOKEN")
    token = g.tiers.generate_auth_token(600)
    if (type(token) is bytes) :
        token = token.decode('ascii')
    
    app.logger.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> TOKEN TOKEN TOKEN" + str(token))
    return jsonify({'token': token , 'duration': 600})



@main.route('/api-bab/updateuser', methods=['GET', 'POST'])
def update_user():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        app.logger.info(req)
        user = db.session.query(Tiers).filter_by(email=obj0['EMAIL']).first()
        if not user:
            return jsonify({'status': 'error', 'error': 'not exists'})    # missing arguments
        else:
            m_user.local_updateUser(obj0)
            # SALAM
            ret0 = jsonify({'status': 'ok'})    # missing arguments
            return ret0
    else:
        abort(400)


# *********************************************
# *********************************************
# *********************************************


# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
@main.route('/api-nbrows', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_CountTable():
    # app.logger.info(">>>>>>>>>>>>>>> api-nbrows called")
    # app.logger.info(">>>>>>>>>>>>>>> api-nbrows request" + str(request))
    # app.logger.info(">>>>>>>>>>>>>>> api-nbrows is_json" + str(request.is_json))
    # app.logger.info(">>>>>>>>>>>>>>> api-nbrows json" + str(request.get_json()))
    if request.is_json:
        # app.logger.info(">>>>>>>>>>>>>>> api-nbrows is_json")
        req = request.get_json()
        obj0 = req
        # app.logger.info(">>>>>>>>>>>>>>> api-nbrows table "+str(obj0['table']))
        if ('table' in obj0):
            models0 = importlib.import_module('app.models')
            the_class0 = getattr(models0, obj0['table'])
            # app.logger.info(">>>>>>>>>>>>>>> api_CountTable, table " + str(obj0['table']))
            # app.logger.info(">>>>>>>>>>>>>>> api_CountTable, classe " + str(the_class0))
            ct0 = db.session.query(the_class0).count()
            # app.logger.info(">>>>>>>>>>>>>>> api_CountTable, count " + str(ct0))
            return {"nbrows": ct0}
        else:
            return {"nbrows": 0}
    else:
        return {"nbrows": 0}

@main.route('/api-article-search-design-nbrows', methods=['GET', 'PUT', 'DELETE', 'POST'])
def api_article_search_designNbRowsFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        app.logger.info(req)
        return {"nbrows": m_article.local_get_articles_search_design(obj0, 1)}
    else:
        return {"nbrows": m_article.local_get_articles(1)}

@main.route('/api-article-search-design', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_article_search_designFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        app.logger.info(req)
        return jsonify(m_article.local_get_articles_search_design(obj0, 0))
    else:
        return jsonify(m_article.local_get_articles(0))
@main.route('/api-article-search-ref_art', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_article_search_refArt():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        app.logger.info(req)
        return jsonify(m_article.local_get_articles_search_refArt(obj0))

@main.route('/api-sfamilles', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_article_all_sfamillesFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        app.logger.info(req)
        return jsonify(m_article.all_sfamilles([obj0['codefamille']]))
    else:
        return jsonify([])


@main.route('/api-article-search-mult', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_article_search_multFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        app.logger.info(req)
        return jsonify(m_article.local_get_articles_search_mult(obj0, 0))
    else:
        return jsonify(m_article.local_get_articles(0))

@main.route('/api-article-search-mult-nbrows', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_article_search_multNbRowsFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        app.logger.info(req)
        return {"nbrows": m_article.local_get_articles_search_mult(obj0, 1)}
    else:
        return {"nbrows": len(m_article.local_get_articles(0))}

@main.route('/api-articles-images', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_article_imagesFunction():
    return jsonify(m_article.local_get_articles_images())

#@main.route('/get_article_image/<string:ref_art>/<string:nom_image>', methods=['GET', 'POST'])
@main.route('/api-article-image', methods=['GET', 'POST'])
@cross_origin()
def get_article_image():
    dossier0 = request.args.get('dossier', None)
    image0 = request.args.get('image', None)
    app.logger.info(">>>>>>>>>>>>>>> base " + app.config['UPLOAD_FOLDER'])
    app.logger.info(">>>>>>>>>>>>>>> dossier0 " + dossier0)
    app.logger.info(">>>>>>>>>>>>>>> image " + image0)
    # file0 = os.path.join(app.config['UPLOAD_FOLDER'], '/', ref_art0, '/', nom_image0)
    file0 = app.config['UPLOAD_FOLDER'] + '/' + dossier0 + '/' + image0
    app.logger.info(">>>>>>>>>>>>>>> filename " + file0)
    return send_file(file0, mimetype='image/gif')


@main.route('/api-article-nbrows', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_articlenbrowsFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        app.logger.info(req)
        # obj0 = json.loads(req)
        # app.logger.info(obj0)
        if request.method == 'POST':
            if (('LBrowArticles' in obj0) and ('codefamille' in obj0)):
                # return m_a.local_get_articles()
                return {"nbrows": m_article.local_get_article_famille_interval(obj0, 1)}
            elif ('LBrowArticles' in obj0):
                # return m_a.local_get_articles()
                return {"nbrows": m_article.local_get_article_interval(obj0, 1)}
            elif ('codefamille' in obj0):
                # return m_a.local_get_articles()
                if obj0['codefamille'] == 'TOUS':
                    obj0['codefamille'] = m_famille.get_codesfamilles()
                else :
                    obj0['codefamille'] = [obj0['codefamille']]
                return {"nbrows": m_article.local_get_article_from_famille(obj0['codefamille'])}
            else:
                return {"nbrows": len(m_article.local_get_article(obj0['ref_art']))}
    else:
        return {"nbrows": m_article.local_get_articles(1)}


@main.route('/api-article', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_articleFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        app.logger.info(req)
        # obj0 = json.loads(req)
        # app.logger.info(obj0)
        if request.method == 'POST':
            if (('LBrowArticles' in obj0) and ('codefamille' in obj0)):
                # return m_a.local_get_articles()
                return jsonify(m_article.local_nf2_get_article_famille_interval(obj0, 0))
            elif ('LBrowArticles' in obj0):
                # return m_a.local_get_articles()
                return jsonify(m_article.local_get_article_interval(obj0, 0))
            elif ('codefamille' in obj0):
                # return m_a.local_get_articles()
                return json.dumps(m_article.local_get_article_from_famille(obj0['codefamille']))
                # return json.dumps(m_article.get_articales_from_famille(obj0['codefamille']))
            elif ('ref_arts' in obj0):
                return jsonify(m_article.local_get_article_list(obj0['ref_arts']))
            else:
                return jsonify(m_article.local_get_article(obj0['ref_art']))
        elif request.method == 'NEW':
            return jsonify(m_article.local_makeANewArticle(obj0))
        elif request.method == 'PUT':
            return m_article.local_updateArticle(obj0)
        elif request.method == 'DELETE':
            return m_article.local_deleteArticle(obj0['ref_art'])
    else:
        return jsonify(m_article.local_get_articles(0))
        # The request body wasn't JSON so return a 400 HTTP status code
        # return "Request was not JSON", 400


@main.route('/api-tiers', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_tiersFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        if request.method == 'POST':
            if ('LBrowTiers' in obj0):
                # return m_a.local_get_articles()
                return jsonify(m_tiers.local_get_tiers_interval(obj0))
            elif ('code_fam_tiers' in obj0):
              return jsonify(m_tiers.local_get_tiers_from_famille(obj0['code_fam_tiers']))
            else:
              return jsonify(m_tiers.local_get_tiers(obj0['code_tiers']))
        elif request.method == 'NEW':
            return jsonify(m_tiers.local_makeANewTiers(obj0))
        elif request.method == 'PUT':
            return m_tiers.local_updateTiers(obj0)
        elif request.method == 'DELETE':
            return m_tiers.local_deleteTiers(obj0['code_tiers'])
    else:
        return jsonify(m_tiers.local_get_tierss())


@main.route('/api-nf2-tiers', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_tiers_nf2Function():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        if request.method == 'POST':
            if ('CODE_TIERS_PLACES' in obj0):
               return jsonify(m_tiers.get_tiers_places(obj0))
            elif ('CODE_TIERS' in obj0):
                return jsonify(m_tiers.nf2_get_one_tiers(obj0))
            elif ('LBrowTiers' in obj0):
                # return m_a.local_get_articles()
                return jsonify(m_tiers.local_get_tiers_interval(obj0))
            elif ('code_fam_tiers' in obj0):
              return jsonify(m_tiers.local_get_tiers_from_famille(obj0['code_fam_tiers']))
            else:
              return jsonify(m_tiers.local_get_tiers(obj0['code_tiers']))
    else:
        return jsonify(m_tiers.local_get_tierss())

@main.route('/api-soldetiers', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_soldetiersFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        return jsonify(m_tiers.local_get_solde_tiers(obj0))
    else:
        return jsonify(m_tiers.local_get_tierss())
        # The request body wasn't JSON so return a 400 HTTP status code
        # return "Request was not JSON", 400

@main.route('/api-famille-search', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_famille_search():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        app.logger.info(req)
        return jsonify(m_famille.local_get_famille_search(obj0))

# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
@main.route('/api-famille', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_FamilleFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        if request.method == 'GET':
            if ('codefamille' in obj0):
              return jsonify(m_famille.local_get_Famille(obj0['codefamille']))
        elif request.method == 'POST':
            return jsonify(m_famille.local_makeANewFamille(obj0))
        elif request.method == 'PUT':
            return m_famille.local_updateFamille(obj0)
        elif request.method == 'DELETE':
            return m_famille.local_deleteFamille(obj0['codefamille'])
    else:
        return jsonify(m_famille.local_get_Familles())

@main.route('/api-nf2-famille', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_FamilleNf2Function():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        if request.method == 'POST':
            if ('FAMILLE_PLACES' in obj0):
                return jsonify(m_famille.getFamillePlaces(obj0))
            else:   
                return jsonify(m_famille.local_makeANewFamille(obj0))
    else:
        return jsonify(m_famille.local_get_Familles())

@main.route('/api-famille-all-visible', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_FamilleAllVisibleFunction():
    return jsonify(m_famille.local_get_visible_Familles())
        # if request.method == 'GET':
@main.route('/api-famille_visibles', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_FamilleVisiblesFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        return jsonify(m_famille.local_get_FamillesVisibles(obj0["CODEFAMILLE"]))

@main.route('/api-code-tiers', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_getCodeTier():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        code_tier = db.session.query(Tiers.code_tiers).filter(Tiers.email == obj0["EMAILNET"]).one()
        if (code_tier):
            return jsonify({"CODE_TIERS": code_tier[0]})
        else:
            return "error"

@main.route('/api-fam_tiers_categories', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_FamTiersCategoriesFunction():
    return jsonify({'particuliers': '001', 'revendeurs': '002', 'entreprises': '003'})

@main.route('/api-fam_tiers', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_FamTiersFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        if request.method == 'GET':
              return jsonify(m_fam_tiers.local_get_FamTiers(obj0['code_fam_tiers']))
        elif request.method == 'POST':
            return jsonify(m_fam_tiers.local_makeANewFamTiers(obj0))
        elif request.method == 'PUT':
            return m_fam_tiers.local_updateFamTiers(obj0)
        elif request.method == 'DELETE':
            return m_fam_tiers.local_deleteFamTiers(obj0['code_fam_tiers'])
    else:
        return jsonify(m_fam_tiers.local_get_FamTierss())
        # The request body wasn't JSON so return a 400 HTTP status code
        # return "Request was not JSON", 400

@main.route('/api-cbanque', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_CbanqueFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        if request.method == 'GET':
              return jsonify(m_cbanque.local_get_Cbanque(obj0['code_cbanque']))
        elif request.method == 'POST':
            return jsonify(m_cbanque.local_makeANewCbanque(obj0))
        elif request.method == 'PUT':
            return m_cbanque.local_updateCbanque(obj0)
        elif request.method == 'DELETE':
            return m_cbanque.local_deleteCbanque(obj0['code_cbanque'])
    else:
        return jsonify(m_cbanque.local_get_Cbanques())
        # The request body wasn't JSON so return a 400 HTTP status code
        # return "Request was not JSON", 400

@main.route('/api-mode_regl', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_ModeReglFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        if request.method == 'GET':
              return jsonify(m_mode_regl.local_get_ModeRegl(obj0['code_mode_regl']))
        elif request.method == 'POST':
            return jsonify(m_mode_regl.local_makeANewModeRegl(obj0))
        elif request.method == 'PUT':
            return m_mode_regl.local_updateModeRegl(obj0)
        elif request.method == 'DELETE':
            return m_mode_regl.local_deleteModeRegl(obj0['code_mode_regl'])
    else:
        return jsonify(m_mode_regl.local_get_ModeRegls())
        # The request body wasn't JSON so return a 400 HTTP status code
        # return "Request was not JSON", 400

@main.route('/api-mode_liv', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_ModeLivFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        if request.method == 'GET':
              return jsonify(m_mode_liv.local_get_ModeLiv(obj0['code_mode_liv']))
        elif request.method == 'POST':
            return jsonify(m_mode_liv.local_makeANewModeLiv(obj0))
        elif request.method == 'PUT':
            return m_mode_liv.local_updateModeLiv(obj0)
        elif request.method == 'DELETE':
            return m_mode_liv.local_deleteModeLiv(obj0['code_mode_liv'])
    else:
        return jsonify(m_mode_liv.local_get_ModeLivs())
        # The request body wasn't JSON so return a 400 HTTP status code
        # return "Request was not JSON", 400

@main.route('/api-nf2-pieces', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_nf2_PiecesFunction():
    app.logger.info(">>>>>>>>>>>>>>> api-pieces called")
    if request.is_json:
        req = request.get_json()
        obj0 = req
        # app.logger.info(">>>>>>>>>>>>>>> api-pieces table "+str(obj0))
        if request.method == 'POST':
            if ('PIECES' in obj0):
                return jsonify(m_piece.local_nf2_makeANewPieces(obj0['PIECES']))
            elif ('NOPIECE' in obj0) :
                return jsonify(m_piece.local_nf2_get_one_piece(obj0))
            elif ('NOPIECE_O' in obj0) :
                return jsonify(m_piece.local_nf2_get_piece_versements(obj0))
            elif ('LBrowPieces' in obj0 and 'count' in obj0 and  obj0['count'] == 0):
                return jsonify(m_piece.local_nf2_get_only_piece(obj0))
            elif ('LBrowPieces' in obj0 and 'count' in obj0 and  obj0['count'] == 1):
                return jsonify(m_piece.local_nf2_get_only_piece_count(obj0))
            else:
                return jsonify(m_piece.local_nf2_get_Pieces(obj0))
            # return jsonify(m_article.local_get_article_interval(obj0, 0))
        else:
            # The request body wasn't JSON so return a 400 HTTP status code
            return "Request was not JSON"
    else:
        return "Request was not JSON"




@main.route('/api-pieces', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_PiecesFunction():
    app.logger.info(">>>>>>>>>>>>>>> api-pieces called")
    if request.is_json:
        req = request.get_json()
        obj0 = req
        # app.logger.info(">>>>>>>>>>>>>>> api-pieces table "+str(obj0))
        if request.method == 'POST':
            ret0  = jsonify(m_piece.local_makeANewPieces(obj0))
            app.logger.info(">>>>>>>>>>>>>>> api-pieces ret "+str(ret0))
            return ret0
        else:
            # The request body wasn't JSON so return a 400 HTTP status code
            return "Request was not JSON"
    else:
        return "Request was not JSON"

@main.route('/api-piece', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_PieceFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        if request.method == 'GET':
              return jsonify(m_piece.local_get_Piece(obj0['nopiece']))
        elif request.method == 'POST':
            return m_piece.local_makeANewPiece(obj0)
        elif request.method == 'PUT':
            return m_piece.local_updatePiece(obj0)
        elif request.method == 'DELETE':
            return m_piece.local_deletePiece(obj0['nopiece'])
    else:
        # The request body wasn't JSON so return a 400 HTTP status code
        return "Request was not JSON", 400

@main.route('/api-item', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_ItemFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        if request.method == 'GET':
              return jsonify(m_item.local_get_Item(obj0['noitem']))
        elif request.method == 'POST':
            return jsonify(m_item.local_makeANewItem(obj0))
        elif request.method == 'PUT':
            return m_item.local_updateItem(obj0)
        elif request.method == 'DELETE':
            return m_item.local_deleteItem(obj0['noitem'])
    else:
        # The request body wasn't JSON so return a 400 HTTP status code
        return "Request was not JSON", 400

@main.route('/api-nf2-item', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_nf2_ItemFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        if request.method == 'POST':
            if ('NOPIECE' in obj0):
                return jsonify(m_item.local_nf2_get_piece_items(obj0))
            else :
                return jsonify(m_item.local_get_Items())
    else:
        # The request body wasn't JSON so return a 400 HTTP status code
        return "Request was not JSON", 400

@main.route('/api-item/best-solde', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_bestSoldeItemFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        return jsonify(m_item.local_get_articles_best_solde(obj0))
    else:
        # The request body wasn't JSON so return a 400 HTTP status code
        return "Request was not JSON", 400

@main.route('/api-item/last-solde', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_lastSoldeItemFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        return jsonify(m_item.local_get_articles_last_solde(obj0))
    else:
        # The request body wasn't JSON so return a 400 HTTP status code
        return "Request was not JSON", 400



@main.route('/api-item/new-articles', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_newArticleFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        return jsonify(m_item.local_get_articles_new_items(obj0))
    else:
        # The request body wasn't JSON so return a 400 HTTP status code
        return "Request was not JSON", 400



@main.route('/api-local_type_piece', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_LocalTypePieceFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        if request.method == 'GET':
              return jsonify(m_local_type_piece.local_get_LocalTypePiece(obj0['code_type_piece']))
        elif request.method == 'POST':
            return jsonify(m_local_type_piece.local_makeANewLocalTypePiece(obj0))
        elif request.method == 'PUT':
            return m_local_type_piece.local_updateLocalTypePiece(obj0)
        elif request.method == 'DELETE':
            return m_local_type_piece.local_deleteLocalTypePiece(obj0['code_type_piece'])
    else:
        return jsonify(m_local_type_piece.local_get_LocalTypePieces())
        # The request body wasn't JSON so return a 400 HTTP status code
        # return "Request was not JSON", 400

@main.route('/api-tarif', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_TarifFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        if request.method == 'GET':
              return jsonify(m_tarif.local_get_Tarif(obj0['code_tarif']))
        elif request.method == 'POST':
            return jsonify(m_tarif.local_makeANewTarif(obj0))
        elif request.method == 'PUT':
            return m_tarif.local_updateTarif(obj0)
        elif request.method == 'DELETE':
            return m_tarif.local_deleteTarif(obj0['code_tarif'])
    else:
        # The request body wasn't JSON so return a 400 HTTP status code
        return "Request was not JSON", 400

@main.route('/api-type_piece', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_TypePieceFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        if request.method == 'GET':
              return jsonify(m_type_piece.local_get_TypePiece(obj0['code_type_piece']))
        elif request.method == 'POST':
            return jsonify(m_type_piece.local_makeANewTypePiece(obj0))
        elif request.method == 'PUT':
            return m_type_piece.local_updateTypePiece(obj0)
        elif request.method == 'DELETE':
            return m_type_piece.local_deleteTypePiece(obj0['code_type_piece'])
    else:
        # The request body wasn't JSON so return a 400 HTTP status code
        return "Request was not JSON", 400


@main.route('/api-utilisateurs', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_UtilisateursFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        if request.method == 'GET':
              return jsonify(m_utilisateurs.local_get_Utilisateurs(obj0['username']))
        elif request.method == 'POST':
            return jsonify(m_utilisateurs.local_makeANewUtilisateurs(obj0))
        elif request.method == 'PUT':
            return m_utilisateurs.local_updateUtilisateurs(obj0)
        elif request.method == 'DELETE':
            return m_utilisateurs.local_deleteUtilisateurs(obj0['username'])
    else:
        # The request body wasn't JSON so return a 400 HTTP status code
        return "Request was not JSON", 400

@main.route('/api-parametre', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_ParametreFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        if request.method == 'GET':
              return jsonify(m_parametre.local_get_Parametre(obj0['param']))
        elif request.method == 'POST':
            return jsonify(m_parametre.local_makeANewParametre(obj0))
        elif request.method == 'PUT':
            return m_parametre.local_updateParametre(obj0)
        elif request.method == 'DELETE':
            return m_parametre.local_deleteParametre(obj0['param'])
    else:
        # The request body wasn't JSON so return a 400 HTTP status code
        return "Request was not JSON", 400

@main.route('/api-gps_positions', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_GpsPositionsFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        if request.method == 'GET':
              return jsonify(m_gps_positions.local_get_GpsPositions(obj0['gps_id']))
        elif request.method == 'POST':
            return jsonify(m_gps_positions.local_makeANewGpsPositions(obj0))
        elif request.method == 'PUT':
            return m_gps_positions.local_updateGpsPositions(obj0)
        elif request.method == 'DELETE':
            return m_gps_positions.local_deleteGpsPositions(obj0['gps_id'])
    else:
        # The request body wasn't JSON so return a 400 HTTP status code
        return "Request was not JSON", 400


######################################
######################################
######################################

#@main.route('/')
@main.route('/all-article', methods=['GET'])
def all_articlesFunction():
    if request.method == 'GET':
        return jsonify(m_article.local_get_articles(0))

@main.route("/getall")
def web_get_all():
    try:
        params=Parametre.query.all()
        return  jsonify([e.serialize() for e in params])
    except Exception as e:
	    return(str(e))

# landing page that will display all the books in our database
# This function will operate on the Read operation.
# @main.route('/')
# def web_showArticles():
#     try:
#       articles = db.session.query(Article).all()
#       # return  jsonify([e.serialize() for e in articles])
#       return render_template('web_articles.html', articles=articles)
#     except Exception as e:
# 	    return(str(e))

# This will let us Create a new book and save it in our database
@main.route('/Warticles/new/', methods=['GET', 'POST'])
def web_newArticle():
    if request.method == 'POST':
        newArticle = Article(ref_art=request.form['ref_art'],
                       designation=request.form['designation'],
                       codefamille=request.form['codefamille'])
        db.session.add(newArticle)
        db.session.commit()
        return redirect(url_for('web_showArticles'))
    else:
        return render_template('web_newArticle.html')


# This will let us Update our books and save it in our database
@main.route("/Warticles/<string:ref_art>/edit/", methods=['GET', 'POST'])
def web_editArticle(ref_art):
    editedArticle = db.session.query(Article).filter_by(ref_art=ref_art).one()
    if request.method == 'POST':
        if request.form['ref_art']:
            editedArticle.title = request.form['ref_art']
            return redirect(url_for('web_showArticles'))
    else:
        return render_template('web_editArticle.html', article=editedArticle)


# This will let us Delete our book
@main.route('/Warticles/<string:ref_art>/delete/', methods=['GET', 'POST'])
def web_deleteArticle(ref_art):
    articleToDelete = db.session.query(Article).filter_by(ref_art=ref_art).one()
    if request.method == 'POST':
        db.session.delete(articleToDelete)
        db.session.commit()
        return redirect(url_for('web_showArticles'))
    else:
        return render_template('web_deleteArticle.html', article=articleToDelete)


######################################
######################################zakaria
######################################
@main.route('/promo-images', methods=['GET', 'POST'])
def getPromoImages():
    promoImages = []
    promoPath = app.config['PROMO_IMAGES']
    directory = os.fsencode(promoPath)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith("webp") or filename.endswith("jpg") or filename.endswith("jpeg") or filename.endswith("JPEG") or filename.endswith("png") or filename.endswith("gif"): 
            promoImages.append(filename)
    return jsonify({"images": promoImages})
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
@app.route('/upload-images', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if request.form["type"] == "ARTICLE":
            name = request.form["dir"]
            # directory = secure_filename(directory)
            directory = name
            # directory = "articles/" + str(directory)
            if 'files[]' not in request.files:
                flash('No file part')
                return redirect(request.url)
            # dirName = request.json.get("NAME")
            files = request.files.getlist('files[]')
            directory.replace("%20", " ")
            path1 = os.path.join(app.config['PRODUCTS_IMAGES'], directory) 
            path0 = pathlib.Path(path1)
            # if path.exists(path1):
            #     shutil.rmtree(path1, ignore_errors=True)
            coverCount = 0
            for file in files:
                if file :
                    filename = file.filename.replace(" ", "")
                    path2 = path0
                    if path2.exists():
                        # shutil.rmtree(path2)
                        path3 = pathlib.Path(os.path.join(path1, filename))    
                        if path3.exists():
                            os.remove(path3)
                        file.save(os.path.join(path1, filename))
                    else: 
                        os.mkdir(path1)
                        file.save(os.path.join(path1, filename))
            m_images.transform_images_articles(path1, name)
            return jsonify("Image uploaded")
        elif request.form["type"] == "COVER":
            name = request.form["dir"]
            files = request.files.getlist('files[]')
            for file in files:
                filename = file.filename
                # filename = file.filename.replace("/", "\/")
                path0 = os.path.join(app.config['PRODUCTS_COVERS'], filename) 
                file.save(path0)
                m_images.transform_images_cover_articles(name, path0)
                return jsonify("Image uploaded")
        elif request.form["type"] == "PROMO":
            promoPath = app.config['PROMO_IMAGES']
            promoPath = pathlib.Path(promoPath)
            files = request.files.getlist('files[]')
            for file in files:
                if file:
                    filename = file.filename.replace(" ", "")
                    path0 = pathlib.Path(os.path.join(promoPath, filename))
                    # if path0.exists():
                    #     os.remove(path0) 
                    file.save(path0)
                    m_images.transform_images_promo(filename)
            return jsonify("Image uploaded")
        elif request.form["type"] == "CATEGORIE":
            promoPath = app.config['CATEGORIES_IMAGES']
            promoPath = pathlib.Path(promoPath)
            files = request.files.getlist('files[]')
            code_famille = str(request.form["dir"]) + '.' +app.config["IMAGE_FORMAT"]
            # code_famille = code_famille
            for file in files:
                if file :
                    filename = file.filename
                    path0 = pathlib.Path(os.path.join(promoPath, filename))
                    # if path0.exists():
                    #     os.remove(path0) 
                    file.save(path0)
                    m_images.transform_images_categories(filename, code_famille)
            return jsonify("Image uploaded")
        elif request.form["type"] == "LOGO":
            promoPath = app.config['LOGO_IMAGES']
            promoPath = pathlib.Path(promoPath)
            files = request.files.getlist('files[]')
            for file in files:
                if file :
                    filename = file.filename.replace(" ", "")
                    path0 = pathlib.Path(os.path.join(promoPath, "logo.jpeg"))
                    if path0.exists():
                        os.remove(path0) 
                    file.save(path0)
                    m_images.transform_images_promo(filename)
            return jsonify("Image uploaded")
    return jsonify("ERROR")
@app.route('/delete-all-images', methods=['GET', 'POST'])
def deleteAllImages():
    if request.method == 'POST':
        req = request.get_json()
        if req["type"] == "ARTICLE":
            refArt = req["ref_art"]
            directory = "articles/" + str(refArt)
            path0 = os.path.join(app.config['IMAGES_FOLDER'], directory)
            path1 = pathlib.Path(path0)
            path2 = os.path.join(app.config['PRODUCTS_COVERS'], str(refArt+ '.' + app.config['IMAGE_FORMAT']))
            path3 = pathlib.Path(path2)
            if path1.exists() and path3.exists():
                os.remove(path2)
                shutil.rmtree(path0, ignore_errors=True)
                return jsonify("deleted")
            else:
                return jsonify("not_exist")
        # elif request.form["type"] == "PROMO":
        elif req["type"] == "CATEGORIE":
            codefamille = req["codefamille"]
            path0 = os.path.join(app.config['CATEGORIES_IMAGES'], str(codefamille)+ '.' +app.config["IMAGE_FORMAT"])
            path1 = pathlib.Path(path0)
            if path1.exists():
                os.remove(path0)
                return jsonify("deleted")
            else:
                return jsonify("not_exist")
        elif req["type"] == "PROMO":
            imageName = req["IMAGE"]
            path0 = os.path.join(app.config['PROMO_IMAGES'], str(imageName))
            path1 = pathlib.Path(path0)
            if path1.exists():
                os.remove(path0)
                return jsonify("deleted")
            else:
                return jsonify("not_exist")

@app.route('/delete-images', methods=['GET', 'POST'])
def deleteImages():
    if request.method == 'POST':
        req = request.get_json()
        if req["TYPE"] == "ARTICLE":
            name = req["NAME"]
            refArt = req["DIR"]
            path0 = os.path.join(app.config['PRODUCTS_IMAGES'], refArt, name)
            path1 = pathlib.Path(path0)
            if path1.exists():
                os.remove(path0)
                return jsonify("deleted")
            else:
                return jsonify("not_exist")
        # elif request.form["type"] == "PROMO":
        elif req["TYPE"] == "COVER":
            name = req["NAME"]
            refArt = req["DIR"]
            path0 = os.path.join(app.config['PRODUCTS_COVERS'], name)
            path1 = pathlib.Path(path0)
            if path1.exists():
                os.remove(path0)
                return jsonify("deleted")
            else:
                return jsonify("not_exist")
        elif req["TYPE"] == "CATEGORIE":
            codefamille = req["NAME"]
            path0 = os.path.join(app.config['CATEGORIES_IMAGES'], str(codefamille))
            path1 = pathlib.Path(path0)
            if path1.exists():
                os.remove(path0)
                return jsonify("deleted")
            else:
                return jsonify("not_exist")
        elif req["TYPE"] == "PROMO":
            imageName = req["NAME"]
            path0 = os.path.join(app.config['PROMO_IMAGES'], str(imageName))
            path1 = pathlib.Path(path0)
            if path1.exists():
                os.remove(path0)
                return jsonify("deleted")
            else:
                return jsonify("not_exist")

@app.route('/display_images', methods=['GET', 'POST'])
def display_images():
    imageType = request.json.get("TYPE")
    filesList = []
    if imageType == "ARTICLE":
        directory = request.json.get("DIR")
        path0 = os.path.join(app.config['PRODUCTS_IMAGES'], directory) 
        if pathlib.Path(path0).exists():
            files = os.listdir(path0)
            for f in files:
                filesList.append(f)
    elif imageType == "COVER":
        directory = request.json.get("DIR")
        path1 = os.path.join(app.config['PRODUCTS_COVERS'], directory + '.' + app.config["IMAGE_FORMAT"]) 
        if pathlib.Path(path1).exists():
            filesList.append(directory + '.' + app.config["IMAGE_FORMAT"])
    elif imageType == "CATEGORIE":
        directory = request.json.get("DIR")
        path0 = os.path.join(app.config['CATEGORIES_IMAGES'], directory + '.' + app.config["IMAGE_FORMAT"]) 
        if pathlib.Path(path0).exists():
           filesList.append(directory + '.' + app.config["IMAGE_FORMAT"])
    if imageType == "PUB":
        path0 = os.path.join(app.config['PROMO_IMAGES']) 
        if pathlib.Path(path0).exists():
            files = os.listdir(path0)
            for f in files:
                filesList.append(f)
    return jsonify(filesList)
# @app.route('/get_promo_images', methods=['GET', 'POST'])
# def getPromoImages():
#     m_images.transform_images()
#     return jsonify("images transformed")


@app.route('/transform-images', methods=['GET', 'POST'])
def transform_file():
    m_images.transform_images()
    return jsonify("images transformed")

@app.route("/send-email", methods=['GET', 'POST'])
def sendMail():
    user = 'zakilebbah@gmail.com'
    app_password = 'zbox132001'
    to = 'zakilebbah@gmail.com'

    subject = 'Hello'
    content = ['Testing gmail with python']

    with yagmail.SMTP(user, app_password) as yag:
        yag.send(to, subject, content)
        return "Sent"
@app.route("/pdf", methods=['GET', 'POST'])
def sendPdf():
    pdf = weasyprint.HTML('http://www.google.com').write_pdf()
    open('google.pdf', 'wb').write(pdf)    
    return 'cool'
def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        # print(timeformat, end='\r')
        time.sleep(1)
        t -= 1

@app.route('/get-barcode', methods=['GET', 'POST'])
def get_barcode():
    folder = os.path.dirname(os.path.abspath(__file__))
    # imgSrc = url_for('static', filename="21d16000" + '.jpeg')
    with open(folder + "/static/" +"21d16000" + '.jpeg' , 'wb') as f:
        Code128('21d16000', writer=ImageWriter()).write(f)
    # file = open(filename, "w+b")
    html0 = render_template('mailToOwner.html', user="user",products= products, total=total, logo=logo, nopiece=nopiece, ref=ref, src=imgSrc)
    # pdf = StringIO()
    # pdf = pisa.CreatePDF(StringIO(html0), pdf)
    # pdf = pdf.getvalue()
    
@app.route('/get-cart', methods=['GET', 'POST'])
def get_cart():
    products = request.json.get("PRODUCTS")
    username = request.json.get("USER")
    total = request.json.get("TOTAL")
    logo = app.config['LOGO_IMAGE_URL']
    email = request.json.get("EMAIL")
    ref = request.json.get("REF_PIECE")
    nopiece = request.json.get("NOPIECE")
    piece = request.json.get("PIECE")
    imgSrc = os.path.dirname(os.path.abspath(__file__)) + '/static/' + nopiece + '.jpeg'
    with open(imgSrc, 'wb') as f:
        Code128(str(nopiece), writer=ImageWriter()).write(f)
    user = db.session.query(Tiers).filter(Tiers.email==email).one()
    user = user.serialize()
    html = render_template('mail.html', user=user,name=user["RAISON_SOCIALE"],products= products, total=total, logo=logo, code=nopiece, ref=ref, piece=piece)
    html0 = render_template('mailToOwner.html', user=user,products= products, total=total, logo=logo, nopiece=nopiece, ref=ref, src=imgSrc, piece=piece)
    file0 = open(os.path.dirname(os.path.abspath(__file__)) + '/static/' + "test.pdf", "w+b")
    config = pdfkit.configuration(wkhtmltopdf=bytes('/usr/bin/wkhtmltopdf', 'utf-8'))
    pdf = pdfkit.from_string(html0, False, configuration=config)
    server = smtplib.SMTP_SSL(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
    msg = MIMEMultipart('alternative')
    msg['From'] = app.config['MAIL_USERNAME']
    msg['To'] = email
    msg['Subject'] = "Panier"
    part2 = MIMEText(html, 'html')
    msg.attach(part2)
    # #################
    msg0 = MIMEMultipart('alternative')
    msg0['From'] = app.config['MAIL_USERNAME']
    msg0['To'] = email
    msg0['Subject'] = "Panier"
    part20 = MIMEText(html0, 'html')
    pdf0 = MIMEApplication(pdf, _subtype="pdf")
    pdf0.add_header('Content-Disposition','attachment',filename=str(nopiece) + '.pdf')
    # msg.attach('nopiece.jpeg','image/gif', open(imgSrc), 'inline', headers=[['Content-ID','<Myimage>'],])
    # pdf0.add_header('Content-Disposition','attachment','123.pdf')
    msg0.attach(pdf0)
    msg0.attach(part20)
    server.ehlo() # optional, called by login()è
    server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])  
    server.sendmail(app.config['MAIL_USERNAME'], email, msg.as_string())
    server.sendmail(app.config['MAIL_USERNAME'], app.config['MAIL_RESEVER'], msg0.as_string())
    server.close()
    os.remove(imgSrc)
    return jsonify(products)

@app.route('/email_panier_status', methods=['GET', 'POST'])
def send_email_panier_status():
    logo = app.config['LOGO_IMAGE_URL']
    products = request.json.get("PRODUCTS")
    total = request.json.get("TOTAL")
    email = request.json.get("EMAIL")
    message = request.json.get("MESSAGE")
    ref_piece = request.json.get("REF_PIECE")
    nopiece = request.json.get("NOPIECE")
    imgSrc = os.path.dirname(os.path.abspath(__file__)) + '/static/' + nopiece + '.jpeg'
    with open(imgSrc, 'wb') as f:
        Code128(str(nopiece), writer=ImageWriter()).write(f)
    piece = m_piece.getOnePiece(nopiece)
    if piece:
        piece = piece[0]
        html = render_template('status_mail.html', user=piece["EMAILNET"], products= products, total=total, logo=logo, message=message, ref_piece=piece["REF_PIECE"], piece=piece, src=None)
        html0 = render_template('status_mail.html', user=email, products= products, total=total, logo=logo, message=message, ref_piece=piece["REF_PIECE"], piece=piece, src=imgSrc)
        config = pdfkit.configuration(wkhtmltopdf=bytes('/usr/bin/wkhtmltopdf', 'utf-8'))
        pdf = pdfkit.from_string(html0, False, configuration=config)
        pdf0 = MIMEApplication(pdf, _subtype="pdf")
        pdf0.add_header('Content-Disposition','attachment',filename=str(nopiece) + '.pdf')
        server = smtplib.SMTP_SSL(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        msg = MIMEMultipart('alternative')
        msg['From'] = app.config['MAIL_USERNAME']
        msg['To'] = email
        msg['Subject'] = "Panier"
        part2 = MIMEText(html, 'html')
        #####################
        msg0 = MIMEMultipart('alternative')
        msg0['From'] = app.config['MAIL_USERNAME']
        msg0['To'] = email
        msg0['Subject'] = "Panier"
        part20 = MIMEText(html0, 'html')
        msg0.attach(part20)
        msg0.attach(pdf0)
        ######################
        msg.attach(part2)
        server.ehlo() # optional, called by login()è
        # server.login("ya77ia@gmail.com", "oran??31")  
        server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])  
        server.sendmail(app.config['MAIL_USERNAME'], email, msg.as_string())
        server.sendmail(app.config['MAIL_USERNAME'], app.config['MAIL_RESEVER'], msg0.as_string())
        server.close()
        os.remove(imgSrc)
        return "Mail envoyé"
    else :
        return "Mail non envoyé / Pièce commerciale inexistante !"

@main.route('/api-article-list', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_articleFunctionList():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        # obj0 = json.loads(req)
        # app.logger.info(obj0)
        if request.method == 'POST':
            if (('LBrowArticles' in obj0) and ('codefamille' in obj0)):
                # return m_a.local_get_articles()
                return jsonify(m_article.local_get_article_famille_interval(obj0, 0))
            elif ('LBrowArticles' in obj0):
                # return m_a.local_get_articles()
                return jsonify(m_article.local_get_article_interval(obj0, 0))
            elif ('codefamille' in obj0):
                # return m_a.local_get_articles()
                return jsonify(m_article.local_get_article_from_famille(obj0['codefamille']))
            elif ('ref_arts' in obj0):
                return jsonify(m_article.local_get_article_list(obj0))
                
        elif request.method == 'NEW':
            return jsonify(m_article.local_makeANewArticle(obj0))
        elif request.method == 'PUT':
            return m_article.local_updateArticle(obj0)
        elif request.method == 'DELETE':
            return m_article.local_deleteArticle(obj0['ref_art'])
    else:
        return jsonify(m_article.local_get_articles(0))
        # The request body wasn't JSON so return a 400 HTTP status code
        # return "Request was not JSON", 400

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if request.is_json:
        email0 = request.json.get('email')
        user = db.session.query(Tiers).filter_by(email=email0).first()
        if not user:
            return jsonify({'status': 'not_exists'})    
        else:
            # reload(sys)
            # sys.setdefaultencoding('UTF8')
            user = user.serialize()
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for i in range(12))
            user0 = m_user.local_updateUser_password(email0, password)
            email = user["EMAIL"]
            userName = user["RAISON_SOCIALE"]
            html = render_template('reset.html',password=password, name=userName)
            server = smtplib.SMTP_SSL(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
            msg = MIMEMultipart('alternative')
            msg['From'] = app.config['MAIL_USERNAME']
            msg['To'] = email
            msg['Subject'] = "Réinitialisation du mot de passe"
            part2 = MIMEText(html, 'html')
            msg.attach(part2)
            server.ehlo() # optional, called by login()è
            # server.login("ya77ia@gmail.com", "oran??31")  
            server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])  
            server.sendmail(app.config['MAIL_USERNAME'], email, msg.as_string())
            server.close()
            # addedUser.hash_password(obj0['passwordnet'])
            # user0['PASSWORDNET'] = password
            return jsonify({'status': 'done', "pass": password})
    else:
        return jsonify({'error': 'not json'})

@app.route('/user-exist', methods=['GET', 'POST'])
def is_user():
    if request.is_json:
        user0 = request.json.get('email')
        password = request.json.get('passwordnet')
        app.logger.info(">>>>>>>>>>>>>>> USER0 user-exist " + str(user0) + "////////" + str(password))
        user = User.verify_auth_token(user0)
        if not user:
            app.logger.info(">>>>>>>>>>>>>>> NO TOKEN user-exist")
            user = db.session.query(Tiers).filter_by(email=user0).first()
            if not user:
                app.logger.info(">>>>>>>>>>>>>>> NO USER user-exist")
                return jsonify({'status': 'not_exists'})
            elif not user.verify_password(password):
                app.logger.info(">>>>>>>>>>>>>>> NO USER user-exist")
                return jsonify({'status': 'pass-error'})
                # return False
            else:
                return jsonify({'status': 'exists'})
            
    else:
        return jsonify({'error': 'not json'})

@main.route('/api-get-pieces-cart', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_Get_PiecesFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        if ("emailnet" in request.json):
            app.logger.info(">>>>>>>>>>>>>>> m_piece.local_get_Pieces_cart " + str(obj0))
            allPieceNopiece = m_piece.local_get_Pieces_cart(obj0)
            app.logger.info(">>>>>>>>>>>>>>> m_item.local_get_Item_cart " + str(obj0))
            allItems = m_item.local_get_Item_cart(allPieceNopiece)
            app.logger.info(">>>>>>>>>>>>>>> end m_item.local_get_Item_cart " + str(obj0))
            return jsonify(allItems)
        elif ("piece_count" in request.json):
            pieceCount = m_piece.countPanierPiece(obj0)
            return jsonify(pieceCount)
        elif ("nopiece_cancel" in request.json):
            canceledPiece = m_piece.local_cancel_Pieces_cart(obj0)
            return jsonify(canceledPiece)
        elif ("ref_art_delete" in request.json):
            canceledPiece = m_item.local_delete_artilce_cart(obj0)
            if (canceledPiece):
                m_piece.local_update_montant_Pieces_cart(obj0)
            return jsonify(canceledPiece)
        elif ("nopiece_deliveryCode" in request.json):
            piece = m_piece.local_update_deliveryCode_Pieces_cart(obj0)
            return jsonify(piece)
    return jsonify("Error")

    

@app.route('/upload-files-seller', methods=['GET', 'POST'])
def upload_file_seller():
    if request.method == 'POST':
        if 'files[]' not in request.files and "MESSAGE" not in request.form:
            return jsonify("Error")
        # dirName = request.json.get("NAME")
        files = request.files.getlist('files[]')
        message = request.form["MESSAGE"]
        server = smtplib.SMTP_SSL(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        msg = MIMEMultipart('alternative')
        msg['From'] = app.config['MAIL_USERNAME']
        msg['To'] = app.config['MAIL_RESEVER']
        msg['Subject'] = "Info"
        msg.attach(MIMEText(message))
        if files:
            for file in files:
                filename = secure_filename(file.filename)
                file = file.read()
                fileToSend = MIMEApplication(file)
                fileToSend.add_header('Content-Disposition', 'attachment', filename= filename)
                msg.attach(fileToSend)
        app.logger.info(">>>>>>>>>>>>>>> FILES " + str(msg.items))
        server.ehlo() # optional, called by login()è
        # server.login("ya77ia@gmail.com", "oran??31")  
        server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])  
        server.sendmail(app.config['MAIL_USERNAME'], app.config['MAIL_RESEVER'], msg.as_string())
        server.close()
    return jsonify("Image uploaded")

@main.route('/api-piece-generate', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_PiecesFunctionRandom():
    pieceAnswer = "error"
    if request.method == 'POST':
        req = request.get_json()
        obj = req
        pieceAnswer = m_piece.local_makeNewPicesrandom(obj)
    else:
        obj = None
        pieceAnswer = m_piece.local_makeNewPicesrandom(obj)
    return pieceAnswer

@app.route('/api-max-prixventettc', methods=['GET', 'POST'])
def max_prixventettc():
    maxPrixventettc = db.session.query(func.max(Article.prixventettc)).scalar()
    return jsonify({"MAX_PRIXVENTETTC": maxPrixventettc})

@main.route('/api-modify-password', methods=['POST'])
def modify_pass():
    req = request.get_json()
    obj0 = req
    app.logger.info(req)
    app.logger.info(obj0)
    password = request.json.get('PASSWORDNET')
    email = request.json.get('EMAIL')
    user = db.session.query(Tiers).filter(Tiers.email==email).first()
    if (user):
        if (password is None) or (email is None) or (password == "") or (email == ""):
            return jsonify({'status': 'error', 'error': 'arguments manquant'})
        ret0 = m_user.local_updateUser(obj0)
        return jsonify({'status': 'new', 'user': ret0})
    else:
        return jsonify({'status': 'no user'})

    
# @main.route('/api-sms', methods=['GET'])
# def sendSms():
#     req = request.get_json()
#     obj0 = req
#     client = Client("AC15f0474d83b725bef66e8335149a53f2", "c8b03b63e3262d4b93ae4e34f6a51578")

#     # change the "from_" number to your Twilio number and the "to" number
#     # to the phone number you signed up for Twilio with, or upgrade your
#     # account to send SMS to any phone number
#     client.messages.create(to="0659627021", 
#                         from_="0699750034", 
#                         body="Hello from Python!")

@main.route('/api-stock', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_stockFunction():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        app.logger.info(req)
        # obj0 = json.loads(req)
        app.logger.info(obj0)
        with_stock = True
        if ('WITH_STOCK' in obj0):
            app.logger.info('WITH_STOCK IS INNNNNNNNNNNNNNNNN')
            if (obj0['WITH_STOCK'] == '0'):
                app.logger.info('WITH_STOCK FALSEEEEEEEEEEEEE')
                with_stock = False
            else:
                with_stock = True
        else:
          with_stock = False
        if ('LIST_REF_FAMILLES' in obj0):
            if obj0['LIST_REF_FAMILLES'] == ['TOUS']:
                obj0['LIST_REF_FAMILLES'] = m_famille.get_codesfamilles()
            return jsonify(m_article.local_get_no_stock_familles(obj0, with_stock))
        elif ('LIST_REF_ARTICLES' in obj0):
            return jsonify(m_article.local_get_no_stock_articles(obj0, with_stock))
        else:
            return jsonify(m_article.local_get_no_stock(obj0, with_stock))
    else:
        return jsonify(m_article.local_get_articles(0))

@main.route('/api-num-sons', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_numSons():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        refArt = obj0["REFART"]
        numOfsons = db.session.query(Article).filter_by(boutiq_visible=1,master_ref_art=refArt).count()
        return jsonify({"numSons": numOfsons})



# .filter(Famille.codefamille_m.in_(codes0))

@app.route('/adminPage_password', methods=['POST'])
def admin_password_request():
    if request.is_json:
        email = request.json.get('EMAIL')
        password = request.json.get('PASSWORD')
        if (email == app.config['MAIL_USERNAME'] and password == app.config['MAIL_PASSWORD']):
            return jsonify({'status': 1})
        else :
            return jsonify({'status': 0})
    else:
        return jsonify({'error': 'not json'})

    
@main.route('/api-piece-vitrine', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_getPieceVitrine():
    # if request.is_json:
    #     req = request.get_json()
    return jsonify(m_piece.get_piece_Vitrine(None))
        # return m_piece.get_piece_Vitrine(req)
@main.route('/api-item-vitrine', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_getItemVitrine():
    if request.is_json:
        req = request.get_json()
        response = m_piece.get_item_vitrine(req)
        return jsonify(response)
        # return m_piece.get_piece_Vitrine(req)

@main.route('/api-codefamille', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_codefamille():
    response = m_famille.get_codesfamilles()
    return jsonify(response)

@main.route('/api-yalidine-wilayas', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_yalidine_wilayas():
    id = app.config['YALIDINE_ID']
    token = app.config['YALIDINE_TOKEN']
    r = requests.get('https://api.yalidine.com/v1/wilayas/', headers= {"X-API-ID": id, "X-API-TOKEN": token})
    return jsonify(r.json())
@main.route('/api-yalidine-communs', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_yalidine_communs():
    if request.is_json: 
        id = app.config['YALIDINE_ID']
        token = app.config['YALIDINE_TOKEN']
        req = request.get_json()
        wilaya_id = req['WILAYA_ID']
        stop_desc = req['STOP_DESK']
        if (stop_desc) :
            params= {"wilaya_id": wilaya_id, "has_stop_desk": True}
        else :
            params= {"wilaya_id": wilaya_id}
        r = requests.get('https://api.yalidine.com/v1/communes/', 
        headers= {"X-API-ID": id, "X-API-TOKEN": token},
        params= params)
        return jsonify(r.json())

@main.route('/api-yalidine-fees', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_yalidine_fees():
    if request.is_json: 
        id = app.config['YALIDINE_ID']
        token = app.config['YALIDINE_TOKEN']
        req = request.get_json()
        wilaya_id = req['WILAYA_ID']
        r = requests.get('https://api.yalidine.com/v1/deliveryfees/', 
        headers= {"X-API-ID": id, "X-API-TOKEN": token},
        params= {"wilaya_id": wilaya_id})
        return jsonify(r.json())

@main.route('/api-yalidine-make-parcels', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_yalidine_make_parcels():
    if request.is_json: 
        id = app.config['YALIDINE_ID']
        token = app.config['YALIDINE_TOKEN']
        req = request.get_json()
        # wilaya_id = req['colis']
        r = requests.post('https://api.yalidine.com/v1/parcels/', 
        headers= {"X-API-ID": id, "X-API-TOKEN": token}, json=req)
        print(r)
        return jsonify(r.json())

@main.route('/api-yalidine-get-tracking', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_yalidine_get_tracking():
    if request.is_json: 
        id = app.config['YALIDINE_ID']
        token = app.config['YALIDINE_TOKEN']
        req = request.get_json()
        order_id = req['ORDER_ID']
        r = requests.post('https://api.yalidine.com/v1/parcels/', 
        headers= {"X-API-ID": id, "X-API-TOKEN": token}, params= {"order_id": order_id})
        print(r)
        return jsonify(r.json())
    
@main.route('/api-update-delivery-code', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_update_delivery_code():
    if request.is_json: 
        id = app.config['YALIDINE_ID']
        token = app.config['YALIDINE_TOKEN']
        req = request.get_json()
        order_id = req['ORDER_ID']
        r = requests.post('https://api.yalidine.com/v1/parcels/', 
        headers= {"X-API-ID": id, "X-API-TOKEN": token}, params= {"order_id": order_id})
        print(r)
        return jsonify(r.json())


@main.route('/api-nf2-article', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def api_articleNf2Function():
    if request.is_json:
        req = request.get_json()
        obj0 = req
        app.logger.info(req)
        # obj0 = json.loads(req)
        # app.logger.info(obj0)
        if request.method == 'POST':
            if (('LBrowArticles' in obj0) and ('codefamille' in obj0) and ('count' in obj0)):
                # return m_a.local_get_articles()
                return jsonify(m_article.local_nf2_get_article_famille_interval(obj0))
            elif ('LBrowArticles' in obj0):
                # return m_a.local_get_articles()
                return jsonify(m_article.local_get_article_interval(obj0, 0))
            elif ('codefamille' in obj0):
                # return m_a.local_get_articles()
                return jsonify(m_article.local_get_article_from_famille_nf2(obj0['codefamille']))
                # return json.dumps(m_article.get_articales_from_famille(obj0['codefamille']))
            elif ('ref_arts' in obj0):
                return jsonify(m_article.local_nf2_get_article_list(obj0['ref_arts']))
            else:
                return jsonify(m_article.local_get_article(obj0['ref_art']))
        elif request.method == 'NEW':
            return jsonify(m_article.local_makeANewArticle(obj0))
        elif request.method == 'PUT':
            return m_article.local_updateArticle(obj0)
        elif request.method == 'DELETE':
            return m_article.local_deleteArticle(obj0['ref_art'])
    else:
        return jsonify(m_article.local_get_articles(0))