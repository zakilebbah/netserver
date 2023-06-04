from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.functions import func
from app import app
from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from app.models import Parametre, Article, Piece, Tiers, FamTiers
from app import db
import json
from app.models import self_init
import datetime
import dateutil.parser
import sqlalchemy as sa
from sqlalchemy.orm import create_session
from sqlalchemy import create_engine
from app import models as app_models

"""
api functions
"""

def local_get_solde_tiers(obj0):
    # obj0['codefamille']])))[int(obj0['LBrowArticles']):int(obj0['UBrowArticles'
    tierss = []
    lb0 = int(obj0['LBrowTiers'])
    ub0 = int(obj0['UBrowTiers'])
    try:
        if ('PREM_CODE_TIERS' not in obj0):
            obj0['PREM_CODE_TIERS'] = ''
        data1 = {'CODE_FAM':obj0['CODE_FAM'], 'PREM_CODE_TIERS':obj0['PREM_CODE_TIERS']}
        # tierss = app_models.query_result_serial("select T.*, s.SOLDE, s.POINTS_GAGNES from SPTIERS(:CODE_FAM) s left join tiers T on (s.CODE_TIERS = T.CODE_TIERS)", data1, [])
        sql0 = "select T.*, (select sum(coalesce(p.montant, 0)*COALESCE(p.annulee, 1)*(coalesce(p.COEFF, 0) + coalesce(p.COEFF_TR, 0))) from piece p where (p.code_tiers = T.CODE_TIERS)) SOLDE_TOT from tiers T"
        if (obj0['PREM_CODE_TIERS'] != ''):
          sql0 = sql0 + " where (T.CODE_TIERS = :PREM_CODE_TIERS)"
        if (lb0 != -1):
            if ('firebird+fdb:' in app.config['SQLALCHEMY_DATABASE_URI']):
                sql0 = sql0 + ' rows ' + str(lb0+1) + ' to ' + str(ub0)
            else:
                sql0 = sql0 + ' offset ' + str(lb0) + ' limit ' + str(ub0-lb0)
        tierss = app_models.query_result_serial(sql0, data1, [])
        # articles = [dict(row) for row in results]
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return []
    return tierss


def all_sfamillesTiers(codes0):
    # print(" >>>>>>>>>>>>>>>0> "+ str(codes0), flush=True)
    familles0 = db.session.query(FamTiers).filter(FamTiers.code_fam_tiers_m.in_(codes0))
    codes1 = [fam0.code_fam_tiers for fam0 in familles0]
    # print(" >>>>>>>>>>>>>>>1> "+ str(codes1), flush=True)
    codes2 = []
    news0 = []
    if codes1 != []:
        codes2 = all_sfamillesTiers(codes1)
        news0 = codes0 + codes2
    else:
        news0 = codes0 + codes1
    print(" >>>>>>>>>>>>>>>S_FAMILIES> "+ str(news0), flush=True)
    return  news0

def local_get_tierss():
    tierss = []
    try:
      tierss = db.session.query(Tiers).all()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return  ([e.serialize() for e in tierss])
    # tierss = db.session.query(Tiers).all()
    # return jsonify(tierss=[a.serialize for a in tierss])

def local_get_tiers_from_famille(code_fam_tiers0):
    tierss = []
    try:
      tierss = db.session.query(Tiers).filter(Tiers.code_fam_tiers.in_(all_sfamillesTiers([code_fam_tiers0])))
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return ([e.serialize() for e in tierss])

def local_get_tiers(code_tiers0):
    if (code_tiers0 == ''):
      tierss = []
      try:
        tierss = db.session.query(Tiers).all()
      except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
          app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
      return ([e.serialize() for e in tierss])
    else:
      tierss = []
      try:
        tierss = db.session.query(Tiers).filter_by(code_tiers=code_tiers0).one()
      except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
          app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
      return (tierss.serialize())

def local_get_tiers_interval(obj0):
    tierss = []
    try:
      tierss = db.session.query(Tiers)[int(obj0['LBrowTiers']):int(obj0['UBrowTiers'])]
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return ([e.serialize() for e in tierss])

def get_tiers_places(obj0):

    tierss = []
    listToSend = []
    # pieces = 
    try:
    #   tierss = db.session.query(Tiers).join(Piece, Piece.code_tiers==Tiers.code_tiers).filter(Piece.montantverse != Piece.montant)
        tierss = db.session.query(Tiers).filter(Tiers.code_fam_tiers == obj0['CODE_TIERS_PLACES'])
        for tierss0 in tierss:
            print(tierss0)
            piece = db.session.query(Piece.nopiece).filter(Piece.code_tiers == tierss0.code_tiers, Piece.montant != Piece.montantverse).order_by(Piece.datepiece.desc()).first()
            if (piece):
                listToSend.append({'TIERS': tierss0.serialize(), 'NOPIECE': piece['nopiece']})
            else:
                listToSend.append({'TIERS': tierss0.serialize(), 'NOPIECE': ''})
            print(tierss0)
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return (listToSend)
def nf2_get_one_tiers(obj0):
    tiers = Null
    try:
      tiers = db.session.query(Tiers).filter(Tiers.code_tiers == obj0['CODE_TIERS']).first()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return (tiers.serialize())

def local_makeANewTiers(obj0):
    addedtiers = Tiers()
    # obj0 = json.loads(obj0)
    self_init(Tiers, addedtiers, obj0)
    try:
      db.session.add(addedtiers)
      db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return (addedtiers.serialize())

def local_updateTiers(obj0):
    try:
      updatedtiers = db.session.query(Tiers).filter_by(code_tiers=obj0['code_tiers']).one()
      # obj0 = json.loads(obj0)
      self_init(Tiers, updatedtiers, obj0)
      db.session.add(updatedtiers)
      db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Updated an tiers with code_tiers %s' % obj0['code_tiers']

def local_deleteTiers(code_tiers0):
    try:
      tiersToDelete = db.session.query(Tiers).filter_by(code_tiers=code_tiers0).one()
      db.session.delete(tiersToDelete)
      db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Removed tiers with id %s' % code_tiers0


    # if 'date_creation' in obj0:
    #   addedtiers.date_creation = dateutil.parser.parse(obj0['date_creation'])


    # if 'date_creation' in obj0:
    #   updatedtiers.date_creation = dateutil.parser.parse(obj0['date_creation'])
