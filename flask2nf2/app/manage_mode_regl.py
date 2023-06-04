from app import app
from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from app.models import ModeRegl
from app import db
import json
from app.models import self_init
import datetime
import dateutil.parser
import sqlalchemy as sa

"""
api functions
"""

def local_get_ModeRegls():
    allModeRegls = []
    try:
      allModeRegls = db.session.query(ModeRegl).all()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return  ([e.serialize() for e in allModeRegls])

def local_get_ModeRegl(obj0):
    if (obj0 == ''):
      allModeRegls = []
      try:
        allModeRegls = db.session.query(ModeRegl).all()
      except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
          app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
      return ([e.serialize() for e in allModeRegls])
    else:
        allModeRegls = []
        try:
          allModeRegls = db.session.query(ModeRegl).filter_by(code_mode_regl=obj0).one()
        except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
            app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return (allModeRegls.serialize())

def local_makeANewModeRegl(obj0):
    addedModeRegl = ModeRegl()
    # obj0 = json.loads(obj0)
    self_init(ModeRegl, addedModeRegl, obj0)
    try:
      db.session.add(addedModeRegl)
      db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return (addedModeRegl.serialize())

def local_updateModeRegl(obj0):
    try:
      updatedModeRegl = db.session.query(ModeRegl).filter_by(code_mode_regl=obj0['code_mode_regl']).one()
      # obj0 = json.loads(obj0)
      self_init(ModeRegl, updatedModeRegl, obj0)
      db.session.add(updatedModeRegl)
      db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Updated an ModeRegl with code_mode_regl %s' % obj0['code_mode_regl']

def local_deleteModeRegl(obj0):
    try:
      ModeReglToDelete = db.session.query(ModeRegl).filter_by(code_mode_regl=obj0).one()
      db.session.delete(ModeReglToDelete)
      db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Removed ModeRegl with code_mode_regl %s' % obj0

