from sqlalchemy.sql.elements import Null
from app import app
from datetime import date, datetime
from app import db
from flask import jsonify
from sqlalchemy.inspection import inspect
import json
import pprint
from sqlalchemy import null
# import datetime
import dateutil.parser
import logging
import sys
import jwt
from passlib.apps import custom_app_context as pwd_context
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import time
# from sqlalchemy import Sequence
# from sqlalchemy.ext.declarative import declarative_base

def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's 
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return json.dumps(d)

# https://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
# https://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask
# https://wakatime.com/blog/32-flask-part-1-sqlalchemy-models-to-json
# https://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask
# https://www.it-swarm.dev/fr/python/convertir-un-objet-de-la-ligne-sqlalchemy-en-python-dict/968709091/
# https://stackoverflow.com/questions/3930713/python-serialize-a-dictionary-into-a-simple-html-output

    # for c in inspect(concept0).attrs.keys():
    # columns = self.__table__.columns.keys()
    # relationships = self.__mapper__.relationships.keys()
    # properties = dir(self)
    # {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}
    # Ship.__table__.columns will provide you with columns information
    # Ship.__table__.foreign_keys will list foreign keys
    # Ship.__table__.constraints
    # Ship.__table__.indexes are other properties you might find useful
    # return json.dumps(d)

    # def serialize(self, include={}, exclude=[], only=[]):
    #     serialized = {}
    #     for key in inspect(self).attrs.keys():
    #         to_be_serialized = True
    #         value = getattr(self, key)
    #         if key in exclude or (only and key not in only):
    #             to_be_serialized = False
    #         elif isinstance(value, BaseQuery):
    #             to_be_serialized = False
    #             if key in include:
    #                 to_be_serialized = True
    #                 nested_params = include.get(key, {})
    #                 value = [i.serialize(**nested_params) for i in value]
    #         if to_be_serialized:
    #             serialized[key] = value
    #     return serialized

    # return {c: getattr(self, c) for c in inspect(self).attrs.keys() if c.find('articles_')==-1}
    # fields0 = inspect(self).attrs.keys() 
    # return to_json(self, self.__class__)
    # return {
    #     'ref_art': self.ref_art, 
    #     'designation': self.designation,
    #     'codefamille': self.codefamille
    # }

# result = db.session.execute('SELECT * FROM article rows :lb to :ub', {"lb":1, "ub":2})
#all0 = query_result('SELECT * FROM article rows :lb to :ub', {"lb":1, "ub":10})
def query_result(sql0, jis0):
    result0 = db.session.execute(sql0, jis0)
    all0 = []
    for row in result0:
        d = dict()
        for c in result0._metadata.keys:
            if row[c] is not None:
                d[c] = row[c]
        all0.append(d)
    return [{key.upper(): value for key, value in d.items()} for d in all0]
    # return [{key: value for key, value in d.items()} for d in all0]

def query_result_serial(sql0, jis0, excludes0):
    result0 = db.session.execute(sql0, jis0)
    all0 = []
    excludes1 = [x.lower() for x in excludes0]
    for row in result0:
        d = dict()
        for c in result0._metadata.keys:
            if (c.lower() not in excludes1):
                if isinstance(row[c], (datetime, date)):
                    d[c] = row[c].isoformat()
                elif row[c] is not None:
                    d[c] = row[c]
        all0.append(d)
    return [{key.upper(): value for key, value in d.items()} for d in all0]

# obj0 = {'PREM_REF_ART':'', 'CODE_FAM':'TOUS', 'CODE_DEPOT':''}
# data1 = {'PREM_REF_ART':obj0['PREM_REF_ART'], 'CODE_FAM':obj0['CODE_FAM'], 'CODE_DEPOT':obj0['CODE_DEPOT'], 'GET_ITEM':'0', 'DATEMIN':'01/01/1950', 'DATEMAX':'01/01/2030'}
# a0 = query_result_serial("select A.*, s.FIN_DEPOT_QTE from spStock(:PREM_REF_ART, :CODE_FAM, :CODE_DEPOT, :GET_ITEM, :DATEMIN, :DATEMAX) s left join article A on (s.REF_ART = A.REF_ART)", data1, ["photo"])
# a1 = jsonify(a0)

def self_dict(concept0, obj0, withoutfields0=[]):
    d = dict()
    for c in concept0.__table__.columns:
        # app.logger.info(">>>>>>>>>>>>>>>>>>>>> GETATTR GETATTR GETATTR GETATTR " + str(c.name) + " " + str(obj0))
        v = getattr(obj0, c.name)
        # app.logger.info(">>>>>>>>>>>>>>>>>>>>> GETATTR GETATTR GETATTR GETATTR " + str(c.name) + " " + str(obj0))
        if isinstance(v, (datetime, date)):
            d[c.name] = v.isoformat()
        elif (v is not None) and (c.name.upper() not in withoutfields0):
            d[c.name] = v
    return d

# def self_init(concept0, self0, obj0):  
#     obj1 = obj0
#     for c in concept0.__table__.columns:
#         if (str(c.type)=="DATETIME") and (c.name in obj1):
#             setattr(self0, c.name, dateutil.parser.parse(obj1[c.name]))
#         elif (c.name in obj1):
#             setattr(self0, c.name, obj1[c.name])

# db.session.execute("insert into usernet (emailnet, passwordnet) values ('yyyy02@gmail.com', 'toto00')")
# result = session.execute( "SELECT * FROM user WHERE id=:param",{"param":5})
def self_insert(concept0, obj0):
    cols0 = ""
    binds0 = ""
    for attr, value in obj0.items():
        if cols0=="":
            cols0 = cols0 + "(" + attr
            binds0 = binds0 + "(:" + attr
        else:
            cols0 = cols0 + "," + attr
            binds0 = binds0 + ",:" + attr
    cols0 = cols0 + ")"
    binds0 = binds0 + ")"
    query0 = "insert into " + concept0.__tablename__ + " " + cols0 + " values " + binds0 
    return query0

    


def self_init(concept0, self0, obj0):
    obj1 = obj0
    # for key, value in obj1.items():
    #     setattr(self0, key, obj1[key])
    for c in concept0.__table__.columns:
        # app.logger.info("################# self_init, " + c.name + " " + str(c.type))
        obj_name = c.name
        if (c.name.upper() in obj1): 
            obj_name = c.name.upper()
            # app.logger.info("################### self_init found " + c.name + " " + str(c.type) + " / " + obj_name + " val = " + str(obj1[obj_name]))
        elif (c.name.lower() in obj1): 
            obj_name = c.name.lower()
            # app.logger.info("################### self_init  found " + c.name + " " + str(c.type) + " / " + obj_name + " val = " + str(obj1[obj_name]))
        if (str(c.type)=="DATETIME") and (obj_name in obj1):
            if (obj1[obj_name] is not None) and (obj1[obj_name] != ""):
                setattr(self0, c.name, dateutil.parser.parse(obj1[obj_name]))
        elif ("VARCHAR" in str(c.type)) and (obj_name in obj1):
            if (obj1[obj_name] is not None) and (obj1[obj_name] != ""):
                setattr(self0, c.name, obj1[obj_name])
        elif (obj_name in obj1):
            if obj1[obj_name] is not None:
                setattr(self0, c.name, obj1[obj_name])

def self_init_null(concept0, self0):  
    # obj1 = json.loads(obj0)
    for c in concept0.__table__.columns:
        self0[c] = null

def self_serialize(concept0, obj0, withoutfields0=[]):
    d = self_dict(concept0, obj0, withoutfields0)
    return {key.upper(): value for key, value in d.items()}

def self_items(concept0, obj0):
    d = self_dict(concept0, obj0)
    return pprint.papp.logger.info(d)

def self_html(concept0, obj0):
    d = self_dict(concept0, obj0)
    htmlLines = []
    for textLine in pprint.pformat(d).splitlines():
        htmlLines.append('<br/>%s' % textLine) # or something even nicer
    htmlText = '\n'.join(htmlLines)
    return htmlText




class Parametre(db.Model):  
    __tablename__ = 'PARAMETRE'
    param = db.Column('param', db.String(30), primary_key = True)  
    valeur = db.Column(db.String(40000))   
    def __repr__(self):
        return '<Param {}>'.format(self.param)
    def __init__(self):  
        self.param = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)
    # def __init__(self, code_tiers):  
    #     self.code_tiers = code_tiers  
    # def serialize(self):
    #     return {
    #         'param': self.param, 
    #         'valeur': self.valeur
    #     }

class Paramsparams(db.Model):
    __tablename__ = 'paramsparams'
    param = db.Column(db.String(30), nullable=True, primary_key=True)
    valeur = db.Column(db.String(20000), nullable=True)
    def __repr__(self):
        return '<Param {}>'.format(self.param)
    def __init__(self):  
        self.param = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class TypeTarif(db.Model):
    __tablename__ = 'type_tarif'
    code_type_tarif = db.Column(db.String(20), primary_key=True)
    intitule = db.Column(db.String(60), nullable=True)
    marge = db.Column(db.Float, nullable=True)
    def __repr__(self):
        return '<TypeTarif {}>'.format(self.code_type_tarif)
    def __init__(self):  
        self.code_type_tarif = '' 
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class FormJur(db.Model):
    __tablename__ = 'form_jur'
    code_form_jur = db.Column(db.String(20), primary_key = True)
    intitule = db.Column(db.String(60), nullable=True)
    def __repr__(self):
        return '<FormJur {}>'.format(self.code_form_jur)
    def __init__(self):  
        self.code_form_jur = ''
    def htmlize(self):
        return self_items(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class ModeLiv(db.Model):
    __tablename__ = 'mode_liv'
    code_mode_liv = db.Column(db.String(20), nullable=True, primary_key=True)
    intitule = db.Column(db.String(60), nullable=True)
    def __repr__(self):
        return '<ModeLiv {}>'.format(self.code_mode_liv)
    def __init__(self):  
        self.code_mode_liv = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class ModeRegl(db.Model):
    __tablename__ = 'mode_regl'
    code_mode_regl = db.Column(db.String(20), nullable=True, primary_key=True)
    intitule = db.Column(db.String(60), nullable=True)
    code_banque = db.Column(db.String(60), nullable=True)
    code_compte_enc = db.Column(db.String(60), nullable=True)
    code_compte_dec = db.Column(db.String(60), nullable=True)
    code_jrn_en = db.Column(db.String(60), nullable=True)
    code_jrn_dec = db.Column(db.String(60), nullable=True)
    def __repr__(self):
        return '<ModeRegl {}>'.format(self.code_mode_regl)
    def __init__(self):  
        self.code_mode_regl = ''
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class Unite(db.Model):
    __tablename__ = 'unite'
    code_unite = db.Column(db.String(20), primary_key=True)
    intitule = db.Column(db.String(30), nullable=True)
    categ = db.Column(db.String(5), nullable=True)
    facteur = db.Column(db.Float, nullable=True)
    code_unite_dest = db.Column(db.String(20), nullable=True)
    def __repr__(self):
        return '<Unite {}>'.format(self.code_unite)
    def __init__(self):  
        self.code_unite = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class Famille(db.Model):  
    __tablename__ = 'famille'
    codefamille = db.Column(db.String(20), primary_key = True)  
    codefamille_m = db.Column(db.String(20), db.ForeignKey('famille.codefamille'),  nullable=True)   
    codesfamilles_m = db.Column(db.String(100), nullable=True)
    intitule = db.Column(db.String(50), nullable=True)  
    boutiq_visible = db.Column(db.Integer, nullable=True)
    code_compte_ac = db.Column(db.String(12), nullable=True)
    code_compte_ve = db.Column(db.String(12), nullable=True)
    typesuivi = db.Column(db.Integer, nullable=True)
    taux_tva = db.Column(db.Float, nullable=True)
    codetaxe1 = db.Column(db.String(20), nullable=True)
    codetaxe2 = db.Column(db.String(20), nullable=True)
    codetaxe3 = db.Column(db.String(20), nullable=True)
    code_methode = db.Column(db.String(20), nullable=True)
    expr_points = db.Column(db.String(500), nullable=True)
    expression = db.Column(db.String(200), nullable=True)
    marge_benef = db.Column(db.Float, nullable=True)
    marge_reduc = db.Column(db.Float, nullable=True)
    familles_famille = db.relationship("Famille", foreign_keys="[Famille.codefamille_m]")
    def __repr__(self):
        return '<Famille {}>'.format(self.codefamille)
    def __init__(self):  
        self.codefamille = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class FamTiers(db.Model):
    __tablename__ = 'fam_tiers'
    code_fam_tiers = db.Column(db.String(20), primary_key = True)
    code_fam_tiers_m = db.Column(db.String(20), db.ForeignKey('fam_tiers.code_fam_tiers'),  nullable=True)
    categs = db.Column(db.String(200), nullable=True)
    intitule = db.Column(db.String(50), nullable=True)
    code_type_tarif = db.Column(db.String(20), db.ForeignKey('type_tarif.code_type_tarif'),  nullable=True)
    codesfamilles_m = db.Column(db.String(100), nullable=True)
    code_versement = db.Column(db.String(20), nullable=True)
    marge_benef = db.Column(db.Float, nullable=True)
    marge_reduc = db.Column(db.Float, nullable=True)
    familles_fam_tiers = db.relationship("FamTiers", foreign_keys="[FamTiers.code_fam_tiers_m]")
    familles_type_tarif = db.relationship("TypeTarif", foreign_keys="[FamTiers.code_type_tarif]")
    def __repr__(self):
        return '<FamTiers {}>'.format(self.code_fam_tiers)
    def __init__(self):  
        self.code_fam_tiers = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class Tiers(db.Model):
    __tablename__ = 'tiers' 
    code_tiers = db.Column(db.String(20), primary_key=True)
    code_fam_tiers = db.Column(db.String(20), db.ForeignKey('fam_tiers.code_fam_tiers'),  nullable=True)
    raison_sociale = db.Column(db.String(200), nullable=True)
    categs = db.Column(db.String(200), nullable=True)
    activite = db.Column(db.String(100), nullable=True)
    codefamille = db.Column(db.String(20), nullable=True)
    code_form_jur = db.Column(db.String(20), db.ForeignKey('form_jur.code_form_jur'),  nullable=True)
    cp = db.Column(db.String(60), nullable=True)
    ville = db.Column(db.String(30), nullable=True)
    pays = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    web = db.Column(db.String(200), nullable=True)
    tel = db.Column(db.String(100), nullable=True)
    fax = db.Column(db.String(100), nullable=True)
    noartimpos = db.Column(db.String(20), nullable=True)
    matfisc = db.Column(db.String(20), nullable=True)
    noreg = db.Column(db.String(20), nullable=True)
    code_compte_achat = db.Column(db.String(12), nullable=True)
    code_compte_vente = db.Column(db.String(12), nullable=True)
    soldemax = db.Column(db.Float, nullable=True)
    code_type_tarif = db.Column(db.String(20), db.ForeignKey('type_tarif.code_type_tarif'),  nullable=True)
    code_repres = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'))
    soldectrl = db.Column(db.Integer, nullable=True) 
    exonere_tva = db.Column(db.Integer, nullable=True) 
    divers = db.Column(db.String(500), nullable=True)
    code_fidelite = db.Column(db.String(35), nullable=True, unique=True)
    date_creation = db.Column(db.DateTime, nullable=True)
    nopiece = db.Column(db.String(35), nullable=True)
    nis = db.Column(db.String(35), nullable=True)
    gps_latitude = db.Column(db.Float, nullable=True)
    gps_longitude = db.Column(db.Float, nullable=True)
    gps_altitude = db.Column(db.Float, nullable=True)
    gps_accuracy = db.Column(db.Float, nullable=True)
    gps_altitude_accuracy = db.Column(db.Float, nullable=True)
    gps_heading = db.Column(db.Float, nullable=True)
    tierss_famTiers = db.relationship("FamTiers", foreign_keys="[Tiers.code_fam_tiers]")
    tierss_form_jur = db.relationship("FormJur", foreign_keys="[Tiers.code_form_jur]")
    tierss_type_tarif = db.relationship("TypeTarif", foreign_keys="[Tiers.code_type_tarif]")
    tierss_repres = db.relationship("Tiers", foreign_keys="[Tiers.code_repres]")
    def __init__(self):  
        self.code_tiers = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)
    # def __repr__(self):
    #     return '<Tiers {}>'.format(self.code_tiers)

class Utilisateurs(db.Model):
    # __tablename__ = 'users'
    # id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(32), index=True)
    # password_hash = db.Column(db.String(64))
    __tablename__ = 'utilisateurs'
    username = db.Column(db.String(20), primary_key=True)
    pass_field = db.Column('pass', db.String(20))
    code_tiers = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'),  nullable=True)
    host = db.Column(db.String(250), nullable=True)
    apikey = db.Column(db.String(100), nullable=True)
    #Foreign keys
    utilisateurs_tiers = db.relationship("Tiers", foreign_keys="[Utilisateurs.code_tiers]")
    def __init__(self):  
        self.username = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)


class User(UserMixin, db.Model):
    __tablename__ = 'usernet'
    # seq_reg_id = Sequence('seq_reg_id', metadata=db.Model.metadata)
    # id = db.Column(db.Integer, Sequence('user_seq', start=1001, increment=1), primary_key=True)
    emailnet = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    passwordnet = db.Column(db.String(120), nullable=False)
    idusernet = db.Column(db.Integer, nullable=False, autoincrement=True)
    code_tiers = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'),  nullable=True)
    usernamenet = db.Column(db.String(120), nullable=True)
    prenomnet = db.Column(db.String(120), nullable=True)
    raisonsociale = db.Column(db.String(120), nullable=True)
    hostnet = db.Column(db.String(250), nullable=True)
    apikey = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(400), nullable=True)
    activite = db.Column(db.String(100), nullable=True)
    cp = db.Column(db.String(50), nullable=True)
    ville = db.Column(db.String(100), nullable=True)
    pays = db.Column(db.String(100), nullable=True)
    web = db.Column(db.String(200), nullable=True)
    tel = db.Column(db.String(100), nullable=True)
    fax = db.Column(db.String(100), nullable=True)
    noartimpos = db.Column(db.String(100), nullable=True)
    matfisc = db.Column(db.String(100), nullable=True)
    noreg = db.Column(db.String(100), nullable=True)
    nis = db.Column(db.String(100), nullable=True)
    exonere_tva = db.Column(db.Integer, nullable=True)
    
    def get_id(self):
        return (self.emailnet)

    def hash_password(self, password):
        self.passwordnet = generate_password_hash(password, method='sha256')

    def verify_password(self, password):
        app.logger.info(">>>>>>>>>>>>>>>PASSWORD " + str(check_password_hash(self.passwordnet, password)))
        return check_password_hash(self.passwordnet, password)
        # return (self.passwordnet == password)

    # https://pyjwt.readthedocs.io/en/latest/
    def generate_auth_token(self, expires_in=600):
        return jwt.encode(
            {'email': self.emailnet, 'exp': time.time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            # app.logger.info(">>>>>>>>>>>>>>> DATA DATA DATA: " + data['email'])
            # app.logger.info(">>>>>>>>>>>>>>> INPUT TOKEN : " + str(token))
            data = jwt.decode(token, app.config['SECRET_KEY'],
                              algorithms=['HS256'])
            app.logger.info(">>>>>>>>>>>>>>> DATA DATA DATA : " + str(data))
        except:
            return
        app.logger.info(">>>>>>>>>>>>>>> TOKEN USER : " + data['email'])
        return  db.session.query(User).filter_by(emailnet=data['email']).first()
        # return User.query.get(data['username'])

    #Foreign keys
    users_tiers = db.relationship("Tiers", foreign_keys="[User.code_tiers]")
    def __init__(self):  
        self.usernamenet = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)


class Article(db.Model):
    __tablename__ = 'article'
    ref_art = db.Column(db.String(35), primary_key = True)  
    codefamille = db.Column(db.String(20), db.ForeignKey('famille.codefamille'))
    master_ref_art = db.Column(db.String(35), db.ForeignKey('article.ref_art'), nullable = True)  
    designation = db.Column(db.String(100), nullable = True) 
    code_barres = db.Column(db.String(60), unique = True, nullable = True)
    code_nap = db.Column(db.String(35), nullable = True) 
    photo = db.Column(db.LargeBinary, nullable = True)
    detail = db.Column(db.String(500), nullable = True)
    boutiq_visible = db.Column(db.Integer, nullable=True)
    code_depot = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'))
    code_fourn = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'))
    qtemin = db.Column(db.Float, nullable=True)
    qtemax = db.Column(db.Float, nullable=True)
    ctrlstock = db.Column(db.Integer, nullable=True)
    tarif_p_qte = db.Column(db.Integer, nullable=True)
    marge = db.Column(db.Float, nullable=True)
    prixachatht = db.Column(db.Float, nullable=True)
    prixventeht = db.Column(db.Float, nullable=True)
    prixventettc = db.Column(db.Float, nullable=True)
    prixachatttc = db.Column(db.Float, nullable=True)
    taux_tva = db.Column(db.Float, nullable=True)
    codetaxe1 = db.Column(db.String(20), nullable = True) 
    codetaxe2 = db.Column(db.String(20), nullable = True) 
    codetaxe3 = db.Column(db.String(20), nullable = True)
    code_compte_ac = db.Column(db.String(12), nullable = True)
    code_compte_ve = db.Column(db.String(12), nullable = True)
    code_unite_base = db.Column("code_unite_base", db.String, db.ForeignKey('unite.code_unite'))
    code_unite_ac = db.Column("code_unite_ac", db.String, db.ForeignKey('unite.code_unite'))
    code_unite_ve = db.Column("code_unite_ve", db.String, db.ForeignKey('unite.code_unite'))
    code_unite_pr = db.Column("code_unite_pr", db.String, db.ForeignKey('unite.code_unite'))
    code_unite_mp = db.Column("code_unite_mp", db.String, db.ForeignKey('unite.code_unite'))
    code_unite_volume = db.Column(db.String(20), nullable = True) 
    code_unite_poids = db.Column(db.String(20), nullable = True)
    poids_brut = db.Column(db.Float, nullable=True)
    poids_net = db.Column(db.Float, nullable=True)
    volume = db.Column(db.Float, nullable=True)
    code_barre = db.Column(db.String(35), nullable = True)
    code_fiscal = db.Column(db.String(35), nullable = True)
    type_nomenc = db.Column(db.String(5), nullable = True)
    en_sommeil = db.Column(db.Integer, nullable=True) 
    garantie_mois = db.Column(db.Integer, nullable=True) 
    delais = db.Column(db.Integer, nullable=True) 
    qte_format = db.Column(db.String(50), nullable = True)
    code_methode = db.Column(db.String(20), nullable = True)
    datedebpromo = db.Column(db.DateTime, nullable = True)
    datefinpromo = db.Column(db.DateTime, nullable = True)
    prixhtpromo = db.Column(db.Float, nullable=True)
    prixttcpromo = db.Column(db.Float, nullable=True)
    activepromo = db.Column(db.Integer, nullable=True) 
    expr_points = db.Column(db.String(500), nullable = True)
    dateperemp = db.Column(db.DateTime, nullable = True)
    date_creation = db.Column(db.DateTime, nullable = True)
    qtepcarton = db.Column(db.Float, nullable=True) 
    nopiece = db.Column(db.String(35), nullable = True)
    articles_famille = db.relationship("Famille", foreign_keys="[Article.codefamille]")
    articles_depot = db.relationship("Tiers", foreign_keys="[Article.code_depot]")
    articles_fournisseur = db.relationship("Tiers", foreign_keys="[Article.code_fourn]")
    articles_unite_base = db.relationship("Unite", foreign_keys="[Article.code_unite_base]")
    articles_unite_ac = db.relationship("Unite", foreign_keys="[Article.code_unite_ac]")
    articles_unite_ve = db.relationship("Unite", foreign_keys="[Article.code_unite_ve]")
    articles_unite_pr = db.relationship("Unite", foreign_keys="[Article.code_unite_pr]")
    articles_unite_mp = db.relationship("Unite", foreign_keys="[Article.code_unite_mp]")
    articles_master_ref_art = db.relationship("Article", foreign_keys="[Article.master_ref_art]")

    def __init__(self):  
        self.ref_art = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self, ['PHOTO'])
    # def __init__(self, ref_art, designation, codefamille):  
    #     self.ref_art = ref_art  
    #     self.designation = designation  
    #     self.codefamille = codefamille  
    # def __repr__(self):
    #     return self
    #     # return "{}({!r}".format(self.__class__.__name__, self.__dict__)


class Artcomp(db.Model):
    __tablename__ = 'artcomp'
    noartcomp = db.Column(db.String(35), nullable = True, primary_key = True)
    #TODO difference between code_m and code_composant
    code_m = db.Column("code_m", db.String, db.ForeignKey('article.ref_art'))
    code_composant = db.Column("code_composant", db.String, db.ForeignKey('article.ref_art'))
    qteunit = db.Column(db.Float, nullable=True)
    qteunit_min = db.Column(db.Float, nullable=True)
    qteunit_max = db.Column(db.Float, nullable=True)
    prc_prix = db.Column(db.Float, nullable=True)
    unit = db.Column(db.Float, nullable=True)
    #Foreign keys
    artcomps_article = db.relationship("Article", foreign_keys="[Artcomp.code_m]")
    artcomps_composant = db.relationship("Article", foreign_keys="[Artcomp.code_composant]")
    def __init__(self):  
        self.noartcomp = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class Auditoption(db.Model):
    __tablename__ = 'auditoption'
    table_name = db.Column(db.String(31), nullable = True, primary_key = True)
    def __init__(self):  
        self.table_name = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class Cbanque(db.Model):
    __tablename__ = 'cbanque'
    code_cbanque = db.Column(db.String(20), nullable = True, primary_key = True)
    nocompte = db.Column(db.String(30), nullable = True)
    libelle = db.Column(db.String(30), nullable = True)
    adresse = db.Column(db.String(100), nullable = True)
    cp = db.Column(db.String(5), nullable = True)
    ville = db.Column(db.String(30), nullable = True)
    pays = db.Column(db.String(30), nullable = True)
    tel = db.Column(db.String(100), nullable = True)
    fax = db.Column(db.String(100), nullable = True)
    code_compte = db.Column(db.String(12), nullable = True)
    code_jrn = db.Column(db.String(20), nullable = True)
    def __init__(self):  
        self.code_cbanque = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class ChampsModelepiece(db.Model):
    __tablename__ = 'champs_modelepiece'
    code_champs_modelepiece = db.Column(db.String(20), nullable = True, primary_key = True)
    code_modelepiece = db.Column(db.String(20), nullable = True)
    intitule = db.Column(db.String(20), nullable = True)
    type_champs = db.Column(db.Integer, nullable=True) 
    bande = db.Column(db.Integer, nullable=True) 
    dataset = db.Column(db.String(30), nullable = True)
    datafield = db.Column(db.String(30), nullable = True)
    pos_left = db.Column(db.Float, nullable=True)
    pos_top = db.Column(db.Float, nullable=True)
    width = db.Column(db.Float, nullable=True)
    height = db.Column(db.Float, nullable=True)
    justif = db.Column(db.String(1), nullable = True)
    fontname = db.Column(db.String(100), nullable = True)
    fontsize = db.Column(db.Integer, nullable=True) 
    fontcolor = db.Column(db.Integer, nullable=True) 
    fontstyle = db.Column(db.String(5), nullable = True)
    color = db.Column(db.Integer, nullable=True) 
    shape = db.Column(db.Integer, nullable=True) 
    brushcolor = db.Column(db.Integer, nullable=True) 
    data = db.Column(db.Integer, nullable=True) 
    pencolor = db.Column(db.Integer, nullable=True) 
    penwidth = db.Column(db.Integer, nullable=True) 
    transparent = db.Column(db.Integer, nullable=True) 
    def __init__(self):  
        self.code_champs_modelepiece = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class Contact(db.Model):
    __tablename__ = 'contact'
    nom = db.Column(db.String(100),primary_key=True)
    code_tiers = db.Column(db.ForeignKey('tiers.code_tiers'))
    fonction = db.Column(db.String(50), nullable = True)
    tel = db.Column(db.String(100), nullable = True)
    fax = db.Column(db.String(100), nullable = True)
    mobile = db.Column(db.String(100), nullable = True)
    email = db.Column(db.String(100), nullable = True)
    divers = db.Column(db.String(200), nullable = True)
    contacts_tiers = db.relationship("Tiers", foreign_keys="[Contact.code_tiers]")
    def __init__(self):  
        self.nom = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class DefChamps(db.Model):
    __tablename__ = 'def_champs'
    code_champs = db.Column(db.String(20), primary_key=True)
    nom_table = db.Column(db.String(30), nullable = True)
    nom_champs = db.Column(db.String(50), nullable = True)
    edit_format = db.Column(db.String(50), nullable = True)
    display_format = db.Column(db.String(50), nullable = True)
    def __init__(self):  
        self.code_champs = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class Entete(db.Model):
    __tablename__ = 'entete'
    noentete = db.Column(db.Integer, nullable=True, primary_key = True) 
    societe = db.Column(db.String(100), nullable = True)
    coordonnee = db.Column(db.String(900), nullable = True)
    image = db.Column(db.LargeBinary, nullable = True) 
    def __init__(self):  
        self.noentete = 0  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class EquivCbarres(db.Model):
    __tablename__ = 'equiv_cbarres'
    noequiv_cbarres = db.Column(db.String(35), primary_key = True)
    ref_art = db.Column(db.String(35), db.ForeignKey('article.ref_art'))
    code_barres = db.Column(db.String(60))
    cbarres_article = db.relationship("Article", foreign_keys="[EquivCbarres.ref_art]")
    def __init__(self):  
        self.noequiv_cbarres = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class Etat(db.Model):
    __tablename__ = 'etat'
    code_etat = db.Column(db.String(20), primary_key = True)
    intitule = db.Column(db.String(30), nullable=True)
    requette = db.Column(db.String(20000), nullable=True)
    coll_sizes = db.Column(db.String(500), nullable=True)
    orientation = db.Column(db.String(2), nullable=True)
    hauteur = db.Column(db.Float, nullable=True)
    largeur = db.Column(db.Float, nullable=True)
    pied = db.Column(db.String(500), nullable=True)
    def __init__(self):  
        self.code_etat = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class GpsPositions(db.Model):
    __tablename__ = 'gps_positions'
    gps_id = db.Column(db.String(100), primary_key = True)
    gps_date = db.Column(db.DateTime, nullable = True)
    gps_latitude = db.Column(db.Float, nullable=True)
    gps_longitude = db.Column(db.Float, nullable=True)
    gps_altitude = db.Column(db.Float, nullable=True)
    gps_accuracy = db.Column(db.Float, nullable=True)
    gps_altitude_accuracy = db.Column(db.Float, nullable=True)
    gps_heading = db.Column(db.Float, nullable=True)
    gps_speed = db.Column(db.Float, nullable=True)
    def __init__(self):  
        self.gps_id = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class Infochamps(db.Model):
    __tablename__ = 'infochamps'
    noinfochamps = db.Column(db.String(35), primary_key = True)
    ref_champs = db.Column(db.String(35), db.ForeignKey('article.ref_art'),  nullable=True)
    code_tiers = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'),  nullable=True)
    valeur = db.Column(db.String(60), nullable=True)
    code_fam_tiers = db.Column(db.String(20), db.ForeignKey('fam_tiers.code_fam_tiers'),  nullable=True)
    #Foreign keys
    infochamps_article = db.relationship("Article", foreign_keys="[Infochamps.ref_champs]")
    infochamps_tiers = db.relationship("Tiers", foreign_keys="[Infochamps.code_tiers]")
    infochamps_fam_tiers = db.relationship("FamTiers", foreign_keys="[Infochamps.code_fam_tiers]")
    def __init__(self):  
        self.noinfochamps = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class Infotiers(db.Model):
    __tablename__ = 'infotiers'
    noinfochamps = db.Column(db.String(35), primary_key = True)
    ref_champs = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'),  nullable=True)
    code_tiers = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'),  nullable=True)
    valeur = db.Column(db.String(100), nullable=True)
    code_fam_tiers = db.Column(db.String(20), db.ForeignKey('fam_tiers.code_fam_tiers'),  nullable=True)
    infotiers_champs_tiers = db.relationship("Tiers", foreign_keys="[Infotiers.ref_champs]")
    infotiers_tiers = db.relationship("Tiers", foreign_keys="[Infotiers.code_tiers]")
    infotiers_fam_tiers = db.relationship("FamTiers", foreign_keys="[Infotiers.code_fam_tiers]")
    def __init__(self):  
        self.noinfochamps = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class Piece(db.Model):
    __tablename__ = 'piece'
    __table_args__ = (db.UniqueConstraint('code_type_piece', 'ref_piece', 'code_site', 'nobis'),)
    nopiece = db.Column(db.String(35), nullable=True, primary_key=True)
    nopiece_o = db.Column(db.String(35), db.ForeignKey('piece.nopiece'))
    nopiece_t = db.Column(db.String(35), db.ForeignKey('piece.nopiece'))
    nopiece_e = db.Column(db.String(35), db.ForeignKey('piece.nopiece'))
    nopiece_d = db.Column(db.String(35), db.ForeignKey('piece.nopiece'))
    code_type_piece = db.Column(db.String(20))
    ref_piece = db.Column(db.Integer, nullable=True) 
    code_tiers = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'),  nullable=True)
    code_repres = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'),  nullable=True)
    code_depot = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'),  nullable=True)
    code_depot_tr = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'),  nullable=True)
    code_cbanque = db.Column(db.String(20), db.ForeignKey('cbanque.code_cbanque'),  nullable=True)
    code_cbanque_tr = db.Column(db.String(20), db.ForeignKey('cbanque.code_cbanque'),  nullable=True)
    code_superviseur = db.Column(db.String(20), nullable=True) #TODO check foreign key
    code_commercial = db.Column(db.String(20), nullable=True) #TODO check foreign key
    code_caissier = db.Column(db.String(20), nullable=True) #TODO check foreign key
    code_affaire = db.Column(db.String(20), nullable=True) #TODO check foreign key
    nom_contact = db.Column(db.String(100), nullable=True)
    lettrage = db.Column(db.String(20), nullable=True)
    refdoc = db.Column(db.String(255), nullable=True)
    datepiece = db.Column(db.DateTime, nullable=True)
    pied = db.Column(db.String(255), nullable=True)
    code_mode_regl = db.Column(db.String(20), db.ForeignKey('mode_regl.code_mode_regl'),  nullable=True)
    refpaye = db.Column(db.String(50), nullable=True)
    code_mode_liv = db.Column(db.String(20), db.ForeignKey('mode_liv.code_mode_liv'),  nullable=True)
    etat = db.Column(db.String(2), nullable=True)
    status_cart = db.Column(db.String(2), nullable=True)
    code_devise = db.Column(db.String(20), nullable=True)
    coeff = db.Column(db.Integer, nullable=True) 
    coeff_tr = db.Column(db.Integer, nullable=True) 
    montant = db.Column(db.Float, nullable=True)
    emailnet = db.Column(db.String(120), nullable=True)
    username = db.Column(db.String(30), nullable=True)
    poste = db.Column(db.String(20), nullable=True)
    livr_adresse = db.Column(db.String(200), nullable=True)
    livr_telephone = db.Column(db.String(100), nullable=True)
    livr_date = db.Column(db.DateTime, nullable=True)
    poids_net = db.Column(db.Float, nullable=True)
    poids_brut = db.Column(db.Float, nullable=True)
    volume = db.Column(db.Float, nullable=True)
    montantverse = db.Column(db.Float, nullable=True)
    montantht = db.Column(db.Float, nullable=True)
    montantttc = db.Column(db.Float, nullable=True)
    remise = db.Column(db.Float, nullable=True)
    tva = db.Column(db.Float, nullable=True)
    timbre = db.Column(db.Float, nullable=True)
    autretaxes = db.Column(db.Float, nullable=True)
    frais = db.Column(db.Float, nullable=True)
    especes = db.Column(db.Float, nullable=True)
    tauxdevise = db.Column(db.Float, nullable=True)
    iddevise = db.Column(db.String(10), nullable=True)
    chaine01 = db.Column(db.String(1000), nullable=True)
    chaine02 = db.Column(db.String(1000), nullable=True)
    chaine03 = db.Column(db.String(1000), nullable=True)
    montant01 = db.Column(db.Float, nullable=True)
    montant02 = db.Column(db.Float, nullable=True)
    montant03 = db.Column(db.Float, nullable=True)
    montant04 = db.Column(db.Float, nullable=True)
    montant05 = db.Column(db.Float, nullable=True)
    date001 = db.Column(db.DateTime, nullable=True)
    date002 = db.Column(db.DateTime, nullable=True)
    date003 = db.Column(db.DateTime, nullable=True)
    printed = db.Column(db.Integer, nullable=True) 
    code_site = db.Column(db.String(50), nullable=True)
    code_fidelite = db.Column(db.String(35), nullable=True)
    points_gagnes = db.Column(db.Float, nullable=True)
    chaine04 = db.Column(db.String(1000), nullable=True)
    chaine05 = db.Column(db.String(1000), nullable=True)
    chaine06 = db.Column(db.String(1000), nullable=True)
    chaine07 = db.Column(db.String(1000), nullable=True)
    chaine08 = db.Column(db.String(1000), nullable=True)
    chaine09 = db.Column(db.String(1000), nullable=True)
    chaine10 = db.Column(db.String(1000), nullable=True)
    montant06 = db.Column(db.Float, nullable=True)
    montant07 = db.Column(db.Float, nullable=True)
    montant08 = db.Column(db.Float, nullable=True)
    montant09 = db.Column(db.Float, nullable=True)
    montant10 = db.Column(db.Float, nullable=True)
    annulee = db.Column(db.Integer, nullable=True) 
    detail2 = db.Column(db.LargeBinary, nullable=True)
    montant11 = db.Column(db.Float, nullable=True)
    montant12 = db.Column(db.Float, nullable=True)
    montant13 = db.Column(db.Float, nullable=True)
    montant14 = db.Column(db.Float, nullable=True)
    montant15 = db.Column(db.Float, nullable=True)
    montant16 = db.Column(db.Float, nullable=True)
    montant17 = db.Column(db.Float, nullable=True)
    montant18 = db.Column(db.Float, nullable=True)
    montant19 = db.Column(db.Float, nullable=True)
    montant20 = db.Column(db.Float, nullable=True)
    montant21 = db.Column(db.Float, nullable=True)
    montant22 = db.Column(db.Float, nullable=True)
    montant23 = db.Column(db.Float, nullable=True)
    montant24 = db.Column(db.Float, nullable=True)
    montant25 = db.Column(db.Float, nullable=True)
    montant26 = db.Column(db.Float, nullable=True)
    montant27 = db.Column(db.Float, nullable=True)
    montant28 = db.Column(db.Float, nullable=True)
    montant29 = db.Column(db.Float, nullable=True)
    montant30 = db.Column(db.Float, nullable=True)
    verou = db.Column(db.Integer, nullable=True) 
    nobis =db.Column(db.Integer, nullable=True) 
    taux_tva1 = db.Column(db.Float, nullable=True)
    taux_tva2 = db.Column(db.Float, nullable=True)
    taux_tva3 = db.Column(db.Float, nullable=True)
    tva1 = db.Column(db.Float, nullable=True)
    tva2 = db.Column(db.Float, nullable=True)
    tva3 = db.Column(db.Float, nullable=True)
    #Foreign keys
    pieces_origin = db.relationship("Piece", foreign_keys="[Piece.nopiece_o]")
    pieces_transf = db.relationship("Piece", foreign_keys="[Piece.nopiece_t]")
    pieces_e = db.relationship("Piece", foreign_keys="[Piece.nopiece_e]")
    pieces_d = db.relationship("Piece", foreign_keys="[Piece.nopiece_d]")
    pieces_tiers = db.relationship("Tiers", foreign_keys="[Piece.code_tiers]")
    pieces_repres = db.relationship("Tiers", foreign_keys="[Piece.code_repres]")
    pieces_depot = db.relationship("Tiers", foreign_keys="[Piece.code_depot]")
    pieces_depot_tr = db.relationship("Tiers", foreign_keys="[Piece.code_depot_tr]")
    pieces_cbanque = db.relationship("Cbanque", foreign_keys="[Piece.code_cbanque]")
    pieces_cbanque_tr = db.relationship("Cbanque", foreign_keys="[Piece.code_cbanque_tr]")
    pieces_mode_regl = db.relationship("ModeRegl", foreign_keys="[Piece.code_mode_regl]")
    pieces_mode_liv = db.relationship("ModeLiv", foreign_keys="[Piece.code_mode_liv]")
    def __init__(self):  
        # self_init_null(self.__class__, self)
        self.nopiece = ''
        # self.type = sqlalchemy.sql.null()

    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

# class OldPiece(db.Model):
#     __tablename__ = 'OldPiece'
#     __table_args__ = (db.UniqueConstraint('code_type_piece', 'ref_piece', 'code_site', 'nobis'),)
#     nopiece = db.Column(db.String(35), nullable=True, primary_key=True)
#     nopiece_o = db.Column(db.String(35), db.ForeignKey('OldPiece.nopiece'))
#     nopiece_t = db.Column(db.String(35), db.ForeignKey('OldPiece.nopiece'))
#     nopiece_e = db.Column(db.String(35), db.ForeignKey('OldPiece.nopiece'))
#     nopiece_d = db.Column(db.String(35), db.ForeignKey('OldPiece.nopiece'))
#     code_type_piece = db.Column(db.String(20))
#     ref_piece = db.Column(db.Integer, nullable=True) 
#     code_tiers = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'),  nullable=True)
#     code_repres = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'),  nullable=True)
#     code_depot = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'),  nullable=True)
#     code_depot_tr = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'),  nullable=True)
#     code_cbanque = db.Column(db.String(20), db.ForeignKey('cbanque.code_cbanque'),  nullable=True)
#     code_cbanque_tr = db.Column(db.String(20), db.ForeignKey('cbanque.code_cbanque'),  nullable=True)
#     code_superviseur = db.Column(db.String(20), nullable=True) #TODO check foreign key
#     code_commercial = db.Column(db.String(20), nullable=True) #TODO check foreign key
#     code_caissier = db.Column(db.String(20), nullable=True) #TODO check foreign key
#     code_affaire = db.Column(db.String(20), nullable=True) #TODO check foreign key
#     nom_contact = db.Column(db.String(100), nullable=True)
#     lettrage = db.Column(db.String(20), nullable=True)
#     refdoc = db.Column(db.String(255), nullable=True)
#     datepiece = db.Column(db.DateTime, nullable=True)
#     pied = db.Column(db.String(255), nullable=True)
#     code_mode_regl = db.Column(db.String(20), db.ForeignKey('mode_regl.code_mode_regl'),  nullable=True)
#     refpaye = db.Column(db.String(50), nullable=True)
#     code_mode_liv = db.Column(db.String(20), db.ForeignKey('mode_liv.code_mode_liv'),  nullable=True)
#     etat = db.Column(db.String(2), nullable=True)
#     # status_cart = db.Column(db.String(2), nullable=True)
#     code_devise = db.Column(db.String(20), nullable=True)
#     coeff = db.Column(db.Integer, nullable=True) 
#     coeff_tr = db.Column(db.Integer, nullable=True) 
#     montant = db.Column(db.Float, nullable=True)
#     # emailnet = db.Column(db.String(120), nullable=True)
#     # username = db.Column(db.String(30), nullable=True)
#     poste = db.Column(db.String(20), nullable=True)
#     livr_adresse = db.Column(db.String(200), nullable=True)
#     livr_telephone = db.Column(db.String(100), nullable=True)
#     livr_date = db.Column(db.DateTime, nullable=True)
#     poids_net = db.Column(db.Float, nullable=True)
#     poids_brut = db.Column(db.Float, nullable=True)
#     volume = db.Column(db.Float, nullable=True)
#     montantverse = db.Column(db.Float, nullable=True)
#     montantht = db.Column(db.Float, nullable=True)
#     montantttc = db.Column(db.Float, nullable=True)
#     remise = db.Column(db.Float, nullable=True)
#     tva = db.Column(db.Float, nullable=True)
#     timbre = db.Column(db.Float, nullable=True)
#     autretaxes = db.Column(db.Float, nullable=True)
#     frais = db.Column(db.Float, nullable=True)
#     especes = db.Column(db.Float, nullable=True)
#     tauxdevise = db.Column(db.Float, nullable=True)
#     iddevise = db.Column(db.String(10), nullable=True)
#     chaine01 = db.Column(db.String(1000), nullable=True)
#     chaine02 = db.Column(db.String(1000), nullable=True)
#     chaine03 = db.Column(db.String(1000), nullable=True)
#     montant01 = db.Column(db.Float, nullable=True)
#     montant02 = db.Column(db.Float, nullable=True)
#     montant03 = db.Column(db.Float, nullable=True)
#     montant04 = db.Column(db.Float, nullable=True)
#     montant05 = db.Column(db.Float, nullable=True)
#     date001 = db.Column(db.DateTime, nullable=True)
#     date002 = db.Column(db.DateTime, nullable=True)
#     date003 = db.Column(db.DateTime, nullable=True)
#     printed = db.Column(db.Integer, nullable=True) 
#     code_site = db.Column(db.String(50), nullable=True)
#     code_fidelite = db.Column(db.String(35), nullable=True)
#     points_gagnes = db.Column(db.Float, nullable=True)
#     chaine04 = db.Column(db.String(1000), nullable=True)
#     chaine05 = db.Column(db.String(1000), nullable=True)
#     chaine06 = db.Column(db.String(1000), nullable=True)
#     chaine07 = db.Column(db.String(1000), nullable=True)
#     chaine08 = db.Column(db.String(1000), nullable=True)
#     chaine09 = db.Column(db.String(1000), nullable=True)
#     chaine10 = db.Column(db.String(1000), nullable=True)
#     montant06 = db.Column(db.Float, nullable=True)
#     montant07 = db.Column(db.Float, nullable=True)
#     montant08 = db.Column(db.Float, nullable=True)
#     montant09 = db.Column(db.Float, nullable=True)
#     montant10 = db.Column(db.Float, nullable=True)
#     annulee = db.Column(db.Integer, nullable=True) 
#     detail2 = db.Column(db.LargeBinary, nullable=True)
#     montant11 = db.Column(db.Float, nullable=True)
#     montant12 = db.Column(db.Float, nullable=True)
#     montant13 = db.Column(db.Float, nullable=True)
#     montant14 = db.Column(db.Float, nullable=True)
#     montant15 = db.Column(db.Float, nullable=True)
#     montant16 = db.Column(db.Float, nullable=True)
#     montant17 = db.Column(db.Float, nullable=True)
#     montant18 = db.Column(db.Float, nullable=True)
#     montant19 = db.Column(db.Float, nullable=True)
#     montant20 = db.Column(db.Float, nullable=True)
#     montant21 = db.Column(db.Float, nullable=True)
#     montant22 = db.Column(db.Float, nullable=True)
#     montant23 = db.Column(db.Float, nullable=True)
#     montant24 = db.Column(db.Float, nullable=True)
#     montant25 = db.Column(db.Float, nullable=True)
#     montant26 = db.Column(db.Float, nullable=True)
#     montant27 = db.Column(db.Float, nullable=True)
#     montant28 = db.Column(db.Float, nullable=True)
#     montant29 = db.Column(db.Float, nullable=True)
#     montant30 = db.Column(db.Float, nullable=True)
#     verou = db.Column(db.Integer, nullable=True) 
#     nobis =db.Column(db.Integer, nullable=True) 
#     taux_tva1 = db.Column(db.Float, nullable=True)
#     taux_tva2 = db.Column(db.Float, nullable=True)
#     taux_tva3 = db.Column(db.Float, nullable=True)
#     tva1 = db.Column(db.Float, nullable=True)
#     tva2 = db.Column(db.Float, nullable=True)
#     tva3 = db.Column(db.Float, nullable=True)
#     #Foreign keys
#     pieces_origin = db.relationship("OldPiece", foreign_keys="[OldPiece.nopiece_o]")
#     pieces_transf = db.relationship("OldPiece", foreign_keys="[OldPiece.nopiece_t]")
#     pieces_e = db.relationship("OldPiece", foreign_keys="[OldPiece.nopiece_e]")
#     pieces_d = db.relationship("OldPiece", foreign_keys="[OldPiece.nopiece_d]")
#     pieces_tiers = db.relationship("Tiers", foreign_keys="[OldPiece.code_tiers]")
#     pieces_repres = db.relationship("Tiers", foreign_keys="[OldPiece.code_repres]")
#     pieces_depot = db.relationship("Tiers", foreign_keys="[OldPiece.code_depot]")
#     pieces_depot_tr = db.relationship("Tiers", foreign_keys="[OldPiece.code_depot_tr]")
#     pieces_cbanque = db.relationship("Cbanque", foreign_keys="[OldPiece.code_cbanque]")
#     pieces_cbanque_tr = db.relationship("Cbanque", foreign_keys="[OldPiece.code_cbanque_tr]")
#     pieces_mode_regl = db.relationship("ModeRegl", foreign_keys="[OldPiece.code_mode_regl]")
#     pieces_mode_liv = db.relationship("ModeLiv", foreign_keys="[OldPiece.code_mode_liv]")
#     def __init__(self):  
#         # self_init_null(self.__class__, self)
#         self.nopiece = ''
#         # self.type = sqlalchemy.sql.null()

#     def htmlize(self):class OldPiece(db.Model):
#     __tablename__ = 'OldPiece'
#     __table_args__ = (db.UniqueConstraint('code_type_piece', 'ref_piece', 'code_site', 'nobis'),)
#     nopiece = db.Column(db.String(35), nullable=True, primary_key=True)
#     nopiece_o = db.Column(db.String(35), db.ForeignKey('OldPiece.nopiece'))
#     nopiece_t = db.Column(db.String(35), db.ForeignKey('OldPiece.nopiece'))
#     nopiece_e = db.Column(db.String(35), db.ForeignKey('OldPiece.nopiece'))
#     nopiece_d = db.Column(db.String(35), db.ForeignKey('OldPiece.nopiece'))
#     code_type_piece = db.Column(db.String(20))
#     ref_piece = db.Column(db.Integer, nullable=True) 
#     code_tiers = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'),  nullable=True)
#     code_repres = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'),  nullable=True)
#     code_depot = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'),  nullable=True)
#     code_depot_tr = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'),  nullable=True)
#     code_cbanque = db.Column(db.String(20), db.ForeignKey('cbanque.code_cbanque'),  nullable=True)
#     code_cbanque_tr = db.Column(db.String(20), db.ForeignKey('cbanque.code_cbanque'),  nullable=True)
#     code_superviseur = db.Column(db.String(20), nullable=True) #TODO check foreign key
#     code_commercial = db.Column(db.String(20), nullable=True) #TODO check foreign key
#     code_caissier = db.Column(db.String(20), nullable=True) #TODO check foreign key
#     code_affaire = db.Column(db.String(20), nullable=True) #TODO check foreign key
#     nom_contact = db.Column(db.String(100), nullable=True)
#     lettrage = db.Column(db.String(20), nullable=True)
#     refdoc = db.Column(db.String(255), nullable=True)
#     datepiece = db.Column(db.DateTime, nullable=True)
#     pied = db.Column(db.String(255), nullable=True)
#     code_mode_regl = db.Column(db.String(20), db.ForeignKey('mode_regl.code_mode_regl'),  nullable=True)
#     refpaye = db.Column(db.String(50), nullable=True)
#     code_mode_liv = db.Column(db.String(20), db.ForeignKey('mode_liv.code_mode_liv'),  nullable=True)
#     etat = db.Column(db.String(2), nullable=True)
#     # status_cart = db.Column(db.String(2), nullable=True)
#     code_devise = db.Column(db.String(20), nullable=True)
#     coeff = db.Column(db.Integer, nullable=True) 
#     coeff_tr = db.Column(db.Integer, nullable=True) 
#     montant = db.Column(db.Float, nullable=True)
#     # emailnet = db.Column(db.String(120), nullable=True)
#     # username = db.Column(db.String(30), nullable=True)
#     poste = db.Column(db.String(20), nullable=True)
#     livr_adresse = db.Column(db.String(200), nullable=True)
#     livr_telephone = db.Column(db.String(100), nullable=True)
#     livr_date = db.Column(db.DateTime, nullable=True)
#     poids_net = db.Column(db.Float, nullable=True)
#     poids_brut = db.Column(db.Float, nullable=True)
#     volume = db.Column(db.Float, nullable=True)
#     montantverse = db.Column(db.Float, nullable=True)
#     montantht = db.Column(db.Float, nullable=True)
#     montantttc = db.Column(db.Float, nullable=True)
#     remise = db.Column(db.Float, nullable=True)
#     tva = db.Column(db.Float, nullable=True)
#     timbre = db.Column(db.Float, nullable=True)
#     autretaxes = db.Column(db.Float, nullable=True)
#     frais = db.Column(db.Float, nullable=True)
#     especes = db.Column(db.Float, nullable=True)
#     tauxdevise = db.Column(db.Float, nullable=True)
#     iddevise = db.Column(db.String(10), nullable=True)
#     chaine01 = db.Column(db.String(1000), nullable=True)
#     chaine02 = db.Column(db.String(1000), nullable=True)
#     chaine03 = db.Column(db.String(1000), nullable=True)
#     montant01 = db.Column(db.Float, nullable=True)
#     montant02 = db.Column(db.Float, nullable=True)
#     montant03 = db.Column(db.Float, nullable=True)
#     montant04 = db.Column(db.Float, nullable=True)
#     montant05 = db.Column(db.Float, nullable=True)
#     date001 = db.Column(db.DateTime, nullable=True)
#     date002 = db.Column(db.DateTime, nullable=True)
#     date003 = db.Column(db.DateTime, nullable=True)
#     printed = db.Column(db.Integer, nullable=True) 
#     code_site = db.Column(db.String(50), nullable=True)
#     code_fidelite = db.Column(db.String(35), nullable=True)
#     points_gagnes = db.Column(db.Float, nullable=True)
#     chaine04 = db.Column(db.String(1000), nullable=True)
#     chaine05 = db.Column(db.String(1000), nullable=True)
#     chaine06 = db.Column(db.String(1000), nullable=True)
#     chaine07 = db.Column(db.String(1000), nullable=True)
#     chaine08 = db.Column(db.String(1000), nullable=True)
#     chaine09 = db.Column(db.String(1000), nullable=True)
#     chaine10 = db.Column(db.String(1000), nullable=True)
#     montant06 = db.Column(db.Float, nullable=True)
#     montant07 = db.Column(db.Float, nullable=True)
#     montant08 = db.Column(db.Float, nullable=True)
#     montant09 = db.Column(db.Float, nullable=True)
#     montant10 = db.Column(db.Float, nullable=True)
#     annulee = db.Column(db.Integer, nullable=True) 
#     detail2 = db.Column(db.LargeBinary, nullable=True)
#     montant11 = db.Column(db.Float, nullable=True)
#     montant12 = db.Column(db.Float, nullable=True)
#     montant13 = db.Column(db.Float, nullable=True)
#     montant14 = db.Column(db.Float, nullable=True)
#     montant15 = db.Column(db.Float, nullable=True)
#     montant16 = db.Column(db.Float, nullable=True)
#     montant17 = db.Column(db.Float, nullable=True)
#     montant18 = db.Column(db.Float, nullable=True)
#     montant19 = db.Column(db.Float, nullable=True)
#     montant20 = db.Column(db.Float, nullable=True)
#     montant21 = db.Column(db.Float, nullable=True)
#     montant22 = db.Column(db.Float, nullable=True)
#     montant23 = db.Column(db.Float, nullable=True)
#     montant24 = db.Column(db.Float, nullable=True)
#     montant25 = db.Column(db.Float, nullable=True)
#     montant26 = db.Column(db.Float, nullable=True)
#     montant27 = db.Column(db.Float, nullable=True)
#     montant28 = db.Column(db.Float, nullable=True)
#     montant29 = db.Column(db.Float, nullable=True)
#     montant30 = db.Column(db.Float, nullable=True)
#     verou = db.Column(db.Integer, nullable=True) 
#     nobis =db.Column(db.Integer, nullable=True) 
#     taux_tva1 = db.Column(db.Float, nullable=True)
#     taux_tva2 = db.Column(db.Float, nullable=True)
#     taux_tva3 = db.Column(db.Float, nullable=True)
#     tva1 = db.Column(db.Float, nullable=True)
#     tva2 = db.Column(db.Float, nullable=True)
#     tva3 = db.Column(db.Float, nullable=True)
#     #Foreign keys
#     pieces_origin = db.relationship("OldPiece", foreign_keys="[OldPiece.nopiece_o]")
#     pieces_transf = db.relationship("OldPiece", foreign_keys="[OldPiece.nopiece_t]")
#     pieces_e = db.relationship("OldPiece", foreign_keys="[OldPiece.nopiece_e]")
#     pieces_d = db.relationship("OldPiece", foreign_keys="[OldPiece.nopiece_d]")
#     pieces_tiers = db.relationship("Tiers", foreign_keys="[OldPiece.code_tiers]")
#     pieces_repres = db.relationship("Tiers", foreign_keys="[OldPiece.code_repres]")
#     pieces_depot = db.relationship("Tiers", foreign_keys="[OldPiece.code_depot]")
#     pieces_depot_tr = db.relationship("Tiers", foreign_keys="[OldPiece.code_depot_tr]")
#     pieces_cbanque = db.relationship("Cbanque", foreign_keys="[OldPiece.code_cbanque]")
#     pieces_cbanque_tr = db.relationship("Cbanque", foreign_keys="[OldPiece.code_cbanque_tr]")
#     pieces_mode_regl = db.relationship("ModeRegl", foreign_keys="[OldPiece.code_mode_regl]")
#     pieces_mode_liv = db.relationship("ModeLiv", foreign_keys="[OldPiece.code_mode_liv]")
#     def __init__(self):  
#         # self_init_null(self.__class__, self)
#         self.nopiece = ''
#         # self.type = sqlalchemy.sql.null()

#     def htmlize(self):
#         return self_html(self.__class__, self)
#     def itemize(self):
#         return self_items(self.__class__, self)
#     def serialize(self):
#         return self_serialize(self.__class__, self)
#         return self_html(self.__class__, self)
#     def itemize(self):
#         return self_items(self.__class__, self)
#     def serialize(self):
#         return self_serialize(self.__class__, self)

class Item(db.Model):
    __tablename__ = 'item'
    noitem = db.Column(db.String(35), primary_key = True)
    noitem_m = db.Column(db.String(35), db.ForeignKey('item.noitem'),  nullable=True)
    noitem_o = db.Column(db.String(35), db.ForeignKey('item.noitem'),  nullable=True)
    noitem_lien = db.Column(db.String(35), nullable=True)
    nopiece = db.Column(db.String(35), db.ForeignKey('piece.nopiece'),  nullable=True)
    ref_art = db.Column(db.String(35), db.ForeignKey('article.ref_art'),  nullable=True)
    cle_group = db.Column(db.String(200), nullable=True)
    coeff = db.Column(db.Integer, nullable=True) 
    coeff_tr = db.Column(db.Integer, nullable=True) 
    detail = db.Column(db.String(500), nullable=True)
    datepiece = db.Column(db.DateTime, nullable=True)
    code_tiers = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'),  nullable=True)
    code_depot = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'),  nullable=True)
    code_depot_tr = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'),  nullable=True)
    code_labo = db.Column(db.String(20), db.ForeignKey('tiers.code_tiers'),  nullable=True)
    qte = db.Column(db.Float, nullable=True)
    prixht = db.Column(db.Float, nullable=True)
    poids_net = db.Column(db.Float, nullable=True)
    poids_brut = db.Column(db.Float, nullable=True)
    volume = db.Column(db.Float, nullable=True)
    remise = db.Column(db.Float, nullable=True)
    rabais = db.Column(db.Float, nullable=True)
    prixbrut = db.Column(db.Float, nullable=True)
    prixstock = db.Column(db.Float, nullable=True)
    coutht = db.Column(db.Float, nullable=True)
    tva = db.Column(db.Float, nullable=True)
    qteunit = db.Column(db.Float, nullable=True)
    qteparcolis = db.Column(db.Float, nullable=True)
    nbcolis = db.Column(db.Float, nullable=True)
    code_unite = db.Column("code_unite", db.String, db.ForeignKey('unite.code_unite'))
    codelot = db.Column(db.String(20), nullable=True)
    dateperemp = db.Column(db.DateTime, nullable=True)
    datefabric = db.Column(db.DateTime, nullable=True)
    datemisvente = db.Column(db.DateTime, nullable=True)
    assujetctrl = db.Column(db.Integer, nullable=True) 
    refctrl = db.Column(db.Integer, nullable=True) 
    accepte = db.Column(db.Integer, nullable=True) 
    pump = db.Column(db.Float, nullable=True)
    ppa = db.Column(db.Float, nullable=True)
    shp = db.Column(db.Float, nullable=True)
    chaine01 = db.Column(db.String(1000), nullable=True)
    chaine02 = db.Column(db.String(1000), nullable=True)
    chaine03 = db.Column(db.String(1000), nullable=True)
    montant01 = db.Column(db.Float, nullable=True)
    montant02 = db.Column(db.Float, nullable=True)
    montant03 = db.Column(db.Float, nullable=True)
    montant04 = db.Column(db.Float, nullable=True)
    montant05 = db.Column(db.Float, nullable=True)
    date001 = db.Column(db.DateTime, nullable=True)
    date002= db.Column(db.DateTime, nullable=True)
    garantie_mois = db.Column(db.Integer, nullable=True) 
    calc_pump = db.Column(db.Integer, nullable=True) 
    chaine04 = db.Column(db.String(1000), nullable=True)
    chaine05 = db.Column(db.String(1000), nullable=True)
    chaine06 = db.Column(db.String(1000), nullable=True)
    chaine07 = db.Column(db.String(1000), nullable=True)
    chaine08 = db.Column(db.String(1000), nullable=True)
    chaine09 = db.Column(db.String(1000), nullable=True)
    chaine10 = db.Column(db.String(1000), nullable=True)
    montant06 = db.Column(db.Float, nullable=True)
    montant07 = db.Column(db.Float, nullable=True)
    montant08 = db.Column(db.Float, nullable=True)
    montant09 = db.Column(db.Float, nullable=True)
    montant10 = db.Column(db.Float, nullable=True)
    points_consom = db.Column(db.Float, nullable=True)
    detail2 = db.Column(db.LargeBinary, nullable=True)
    montant11 = db.Column(db.Float, nullable=True)
    montant12 = db.Column(db.Float, nullable=True)
    montant13 = db.Column(db.Float, nullable=True)
    montant14 = db.Column(db.Float, nullable=True)
    montant15 = db.Column(db.Float, nullable=True)
    montant16 = db.Column(db.Float, nullable=True)
    montant17 = db.Column(db.Float, nullable=True)
    montant18 = db.Column(db.Float, nullable=True)
    montant19 = db.Column(db.Float, nullable=True)
    montant20 = db.Column(db.Float, nullable=True)
    montant21 = db.Column(db.Float, nullable=True)
    montant22 = db.Column(db.Float, nullable=True)
    montant23 = db.Column(db.Float, nullable=True)
    montant24 = db.Column(db.Float, nullable=True)
    montant25 = db.Column(db.Float, nullable=True)
    montant26 = db.Column(db.Float, nullable=True)
    montant27 = db.Column(db.Float, nullable=True)
    montant28 = db.Column(db.Float, nullable=True)
    montant29 = db.Column(db.Float, nullable=True)
    montant30 = db.Column(db.Float, nullable=True)
    prixttc = db.Column(db.Float, nullable=True)
    items_master = db.relationship("Item", foreign_keys="[Item.noitem_m]")
    items_origin = db.relationship("Item", foreign_keys="[Item.noitem_o]")
    items_piece = db.relationship("Piece", foreign_keys="[Item.nopiece]")
    items_article = db.relationship("Article", foreign_keys="[Item.ref_art]")
    items_code_tiers = db.relationship("Tiers", foreign_keys="[Item.code_tiers]")
    items_code_depot = db.relationship("Tiers", foreign_keys="[Item.code_depot]")
    items_code_depot_tr = db.relationship("Tiers", foreign_keys="[Item.code_depot_tr]")
    items_code_labo = db.relationship("Tiers", foreign_keys="[Item.code_labo]")
    items_code_unite = db.relationship("Unite", foreign_keys="[Item.code_unite]")
    def __init__(self):  
        self.noitem = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class TypePiece(db.Model):
    __tablename__ = 'type_piece'
    code_type_piece = db.Column(db.String(20), primary_key=True)
    categ = db.Column(db.String(5), nullable=True)
    intitule = db.Column(db.String(60), nullable=True)
    coeff_piece = db.Column(db.Integer, nullable=True) 
    coeff_piece_tr = db.Column(db.Integer, nullable=True) 
    coeff_item = db.Column(db.Integer, nullable=True) 
    coeff_citem = db.Column(db.Integer, nullable=True) 
    coeff_item_tr = db.Column(db.Integer, nullable=True) 
    coeff_citem_tr = db.Column(db.Integer, nullable=True) 
    calc_pump = db.Column(db.Integer, nullable=True) 
    calc_marge = db.Column(db.Integer, nullable=True) 
    categ_tiers = db.Column(db.String(5), nullable=True)
    categ_depot = db.Column(db.String(5), nullable=True)
    categ_banque = db.Column(db.String(5), nullable=True)
    categ_repr = db.Column(db.String(5), nullable=True)
    code_modelepiece = db.Column(db.String(40), nullable=True)
    code_type_piece_vers = db.Column(db.String(20), nullable=True)
    code_type_piece_ech = db.Column(db.String(20), nullable=True)
    ed_form = db.Column(db.String(200), nullable=True)
    br_form = db.Column(db.String(200), nullable=True)
    allow_null_item = db.Column(db.Integer, nullable=True) 
    allow_user_filter = db.Column(db.Integer, nullable=True) 
    type_color = db.Column(db.Integer, nullable=True) 
    def __init__(self):  
        self.code_type_piece = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class LocalTypePiece(db.Model):
    __tablename__ = 'local_type_piece'
    code_type_piece = db.Column(db.String(20), nullable=True, primary_key=True)
    categ = db.Column(db.String(5), nullable=True)
    intitule = db.Column(db.String(60), nullable=True)
    coeff_piece = db.Column(db.Integer, nullable=True) 
    coeff_piece_tr = db.Column(db.Integer, nullable=True) 
    coeff_item = db.Column(db.Integer, nullable=True) 
    coeff_citem = db.Column(db.Integer, nullable=True) 
    coeff_item_tr = db.Column(db.Integer, nullable=True) 
    coeff_citem_tr = db.Column(db.Integer, nullable=True) 
    calc_pump = db.Column(db.Integer, nullable=True) 
    calc_marge = db.Column(db.Integer, nullable=True) 
    categ_tiers = db.Column(db.String(5), nullable=True)
    categ_depot = db.Column(db.String(5), nullable=True)
    categ_banque = db.Column(db.String(5), nullable=True)
    categ_repr = db.Column(db.String(5), nullable=True)
    code_modelepiece = db.Column(db.String(40), nullable=True)
    code_type_piece_vers = db.Column(db.String(20), nullable=True)
    code_type_piece_ech = db.Column(db.String(20), nullable=True)
    ed_form = db.Column(db.String(200), nullable=True)
    br_form = db.Column(db.String(200), nullable=True)
    allow_null_item = db.Column(db.Integer, nullable=True) 
    allow_user_filter = db.Column(db.Integer, nullable=True) 
    type_color = db.Column(db.Integer, nullable=True) 
    def __init__(self):  
        self.code_type_piece = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class Methode(db.Model):
    __tablename__ = 'methode'
    code_methode = db.Column(db.String(20), nullable=True, primary_key=True)
    intitule = db.Column(db.String(30), nullable=True)
    req_rech = db.Column(db.String(500), nullable=True)
    cle = db.Column(db.String(500), nullable=True)
    ordre = db.Column(db.String(500), nullable=True)
    autom = db.Column(db.Integer, nullable=True) 
    def __init__(self):  
        self.code_methode = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class ModelePiece(db.Model):
    __tablename__ = 'modele_piece'
    code_modelepiece = db.Column(db.String(20), nullable=True, primary_key=True)
    intitule = db.Column(db.String(20), nullable=True) 
    hauteur = db.Column(db.Float, nullable=True)
    largeur = db.Column(db.Float, nullable=True)
    haut_bande_pageheader = db.Column(db.Float, nullable=True)
    haut_bande_title = db.Column(db.Float, nullable=True)
    haut_bande_colheader = db.Column(db.Float, nullable=True)
    haut_bande_detail = db.Column(db.Float, nullable=True)
    haut_bande_detchild = db.Column(db.Float, nullable=True)
    haut_bande_subdetail = db.Column(db.Float, nullable=True)
    haut_bande_summary = db.Column(db.Float, nullable=True)
    haut_bande_pagefooter = db.Column(db.Float, nullable=True)
    def __init__(self):  
        self.code_modelepiece = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class Modif(db.Model):
    __tablename__ = 'modif'
    nomodif = db.Column(db.String(35), nullable=True, primary_key=True)
    nogroupe = db.Column(db.String(35), nullable=True) 
    datemodif = db.Column(db.DateTime) 
    username = db.Column(db.String(30), nullable=True) 
    poste = db.Column(db.String(30), nullable=True)
    table_modif = db.Column(db.String(50), nullable=True)
    cle = db.Column(db.String(30), nullable=True)
    champs = db.Column(db.String(50), nullable=True)
    val_old = db.Column(db.String(500), nullable=True)
    val_new = db.Column(db.String(500), nullable=True)
    divers = db.Column(db.String(200), nullable=True)
    etat = db.Column(db.String(2), nullable=True)
    def __init__(self):  
        self.nomodif = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class Nserie(db.Model):
    __tablename__ = 'nserie'
    noserie = db.Column(db.String(35), nullable=True, primary_key=True)
    noitem = db.Column(db.String(35), db.ForeignKey('item.noitem'),  nullable=True)
    numserie = db.Column(db.String(128), nullable=True)
    #Foreign keys
    nseries_item = db.relationship("Item", foreign_keys="[Nserie.noitem]")
    def __init__(self):  
        self.noserie = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class Objects(db.Model):
    __tablename__ = 'objects'
    objectname = db.Column(db.String(50), nullable=True, primary_key=True)
    objecttype = db.Column(db.String(1), nullable=True)
    objparent = db.Column(db.String(50), nullable=True)
    def __init__(self):  
        self.objectname = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class Parametat(db.Model):
    __tablename__ = 'parametat'
    code_parametat = db.Column(db.String(20), nullable=True, primary_key=True)
    code_etat = db.Column(db.String(20), db.ForeignKey('etat.code_etat'),  nullable=True)
    param_name = db.Column(db.String(30), nullable=True)
    param_intitule = db.Column(db.String(30), nullable=True)
    param_type = db.Column(db.Integer, nullable=True) 
    param_src = db.Column(db.String(900), nullable=True)
    param_src_fld = db.Column(db.String(30), nullable=True)
    param_src_displ = db.Column(db.String(30), nullable=True)
    param_affiche = db.Column(db.Integer, nullable=True) 
    param_default_value = db.Column(db.String(30), nullable=True)
    expression = db.Column(db.String(9000), nullable=True)
    aide = db.Column(db.String(2000), nullable=True)
    #Foreign keys
    paramsEtat_etat = db.relationship("Etat", foreign_keys="[Parametat.code_etat]")
    def __init__(self):  
        self.code_parametat = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class Permissions(db.Model):
    __tablename__ = 'permissions'
    code_permission = db.Column(db.Integer,  primary_key=True)
    object1 = db.Column(db.String(50), nullable=True)
    object2 = db.Column(db.String(50), nullable=True)
    relation = db.Column(db.String(1), nullable=True)
    paramobject2 = db.Column(db.String(50), nullable=True)
    subobject2 = db.Column(db.String(50), nullable=True)
    def __init__(self):  
        self.code_permission = 0 
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class Report(db.Model):
    __tablename__ = 'report'
    name = db.Column(db.String(40),  primary_key=True)
    template = db.Column(db.LargeBinary, nullable=True)
    tag = db.Column(db.Integer, nullable=True) 
    intitule = db.Column(db.String(200), nullable=True)
    idx_flds = db.Column(db.String(200), nullable=True)
    def __init__(self):  
        self.name = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class Rubrique(db.Model):
    __tablename__ = 'rubrique'
    code_rub = db.Column(db.String(20), primary_key=True)
    code_type_piece = db.Column(db.String(20), nullable=True)
    table_rub = db.Column(db.String(20))
    evenement = db.Column(db.String(20))
    symbol = db.Column(db.String(20), nullable=True)
    intitule = db.Column(db.String(60), nullable=True)
    expression = db.Column(db.String(2000), nullable=True)
    disp_format = db.Column(db.String(50), nullable=True)
    edit_format = db.Column(db.String(50), nullable=True)
    code_compte = db.Column(db.String(12), nullable=True)
    code_jrn = db.Column(db.String(12), nullable=True)
    imprimable = db.Column(db.Integer, nullable=True) 
    ordre = db.Column(db.Integer, nullable=True) 
    code_ch = db.Column(db.String(20), nullable=True)
    frame_name = db.Column(db.String(60), nullable=True)
    frame_line = db.Column(db.Integer, nullable=True) 
    frame_col = db.Column(db.Integer, nullable=True)
    frame_data_source = db.Column(db.String(60), nullable=True)
    frame_data_field = db.Column(db.String(60), nullable=True)
    frame_look_source = db.Column(db.String(200), nullable=True)
    frame_look_display = db.Column(db.String(60), nullable=True)
    frame_look_field = db.Column(db.String(60), nullable=True) 
    largeur = db.Column(db.Float, nullable=True)
    hauteur = db.Column(db.Float, nullable=True)
    oblig = db.Column(db.Float, nullable=True)
    def __init__(self):  
        self.code_rub = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class Stocks(db.Model):
    __tablename__ = 'stocks'
    __table_args__ = (db.UniqueConstraint('ref_art', 'code_lieu', 'code_type_lieu'),)
    ref_art = db.Column(db.String(35), primary_key=True)
    code_lieu = db.Column(db.String(20), nullable=True)
    code_type_lieu = db.Column(db.String(5), nullable=True)
    qte = db.Column(db.Float, nullable=True)
    def __init__(self):  
        self.ref_art = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class Tarif(db.Model):
    __tablename__ = 'tarif'
    code_tarif = db.Column(db.String(20), primary_key=True)
    code_type_tarif = db.Column(db.String(20), db.ForeignKey('type_tarif.code_type_tarif'),  nullable=True)
    ref_art = db.Column(db.String(35), db.ForeignKey('article.ref_art'))
    intitule = db.Column(db.String(60), nullable=True)
    marge = db.Column(db.Float, nullable=True)
    qtemin = db.Column(db.Float, nullable=True)
    qtemax = db.Column(db.Float, nullable=True)
    prixht = db.Column(db.Float, nullable=True)
    #Foreign keys
    tarifs_type_tarif = db.relationship("TypeTarif", foreign_keys="[Tarif.code_type_tarif]")
    tarifs_article = db.relationship("Article", foreign_keys="[Tarif.ref_art]")
    def __init__(self):  
        self.code_tarif = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class ValChamps(db.Model):
    __tablename__ = 'val_champs'
    __table_args__ = (db.UniqueConstraint('code_champs', 'code_row'),)
    code_champs = db.Column(db.String(20), primary_key=True) 
    code_row = db.Column(db.String(20))
    valeur = db.Column(db.String(100), nullable=True)
    def __init__(self):  
        self.code_champs = ''  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)

class Audit(db.Model):
    __tablename__ = 'audit'
    code_audit = db.Column(db.Integer,  primary_key=True)
    dateaudit = db.Column(db.DateTime, nullable=True)
    user_name = db.Column(db.String(31), nullable=True)
    poste = db.Column(db.String(31), nullable=True)
    table_name = db.Column(db.String(31), nullable=True)
    operation = db.Column(db.String(100), nullable=True)
    def __init__(self):  
        self.code_audit = 0  
    def htmlize(self):
        return self_html(self.__class__, self)
    def itemize(self):
        return self_items(self.__class__, self)
    def serialize(self):
        return self_serialize(self.__class__, self)
