from app import app
from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from app.models import ModeLiv
from app import db
import json
from app.models import self_init
import datetime
import dateutil.parser
import sqlalchemy as sa

"""
api functions
"""

def local_get_ModeLivs():
    allModeLivs = []
    try:
      allModeLivs = db.session.query(ModeLiv).all()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return  ([e.serialize() for e in allModeLivs])

def local_get_ModeLiv(obj0):
    if (obj0 == ''):
      allModeLivs = []
      try:
        allModeLivs = db.session.query(ModeLiv).all()
      except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
          app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
      return ([e.serialize() for e in allModeLivs])
    else:
        allModeLivs = []
        try:
          allModeLivs = db.session.query(ModeLiv).filter_by(code_mode_liv=obj0).one()
        except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
            app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return (allModeLivs.serialize())

def local_makeANewModeLiv(obj0):
    addedModeLiv = ModeLiv()
    # obj0 = json.loads(obj0)
    self_init(ModeLiv, addedModeLiv, obj0)
    try:
      db.session.add(addedModeLiv)
      db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return (addedModeLiv.serialize())

def local_updateModeLiv(obj0):
    try:
      updatedModeLiv = db.session.query(ModeLiv).filter_by(code_mode_liv=obj0['code_mode_liv']).one()
      # obj0 = json.loads(obj0)
      self_init(ModeLiv, updatedModeLiv, obj0)
      db.session.add(updatedModeLiv)
      db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Updated an ModeLiv with code_mode_liv %s' % obj0['code_mode_liv']

def local_deleteModeLiv(obj0):
    try:
      ModeLivToDelete = db.session.query(ModeLiv).filter_by(code_mode_liv=obj0).one()
      db.session.delete(ModeLivToDelete)
      db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Removed ModeLiv with code_mode_liv %s' % obj0

