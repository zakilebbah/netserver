from app import app
from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from app.models import Parametre, Article, Tiers, Famille, Cbanque
from app import db
import json
from app.models import self_init
import datetime
import dateutil.parser
import sqlalchemy as sa

"""
api functions
"""

def local_get_Cbanques():
    allCbanques = db.session.query(Cbanque).all()
    return  [e.serialize() for e in allCbanques]

def local_get_Cbanque(obj0):
    if (obj0 == ''):
      allCbanques = []
      try:
        allCbanques = db.session.query(Cbanque).all()
      except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
          app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
      return ([e.serialize() for e in allCbanques])
    else:
        allCbanques = db.session.query(Cbanque).filter_by(code_cbanque=obj0).one()
        return (allCbanques.serialize())

def local_makeANewCbanque(obj0):
    addedCbanque = Cbanque()
    # obj0 = json.loads(obj0)
    self_init(Cbanque, addedCbanque, obj0)
    try:
      db.session.add(addedCbanque)
      db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return (addedCbanque.serialize())

def local_updateCbanque(obj0):
    try:
      updatedCbanque = db.session.query(Cbanque).filter_by(code_cbanque=obj0['code_cbanque']).one()
      # obj0 = json.loads(obj0)
      self_init(Cbanque, updatedCbanque, obj0)
      db.session.add(updatedCbanque)
      db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Updated an Cbanque with code_cbanque %s' % obj0['code_cbanque']

def local_deleteCbanque(obj0):
    try:
      CbanqueToDelete = db.session.query(Cbanque).filter_by(code_cbanque=obj0).one()
      db.session.delete(CbanqueToDelete)
      db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Removed Cbanque with code_cbanque %s' % obj0

