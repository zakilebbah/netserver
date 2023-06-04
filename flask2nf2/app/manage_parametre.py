from app import app
from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from app.models import Parametre
from app import db
import json
from app.models import self_init
import datetime
import dateutil.parser
import sqlalchemy as sa

"""
api functions
"""

def local_get_parametres():
    allparametres = []
    try:
        allparametres = db.session.query(parametre).all()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return  ([e.serialize() for e in allparametres])

def local_get_parametre(obj0):
    if (obj0 == ''):
        allparametres = []
        try:
            allparametres = db.session.query(parametre).all()
        except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
            app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return ([e.serialize() for e in allparametres])
    else:
        allparametres = []
        try:
            allparametres = db.session.query(parametre).filter_by(param=obj0).one()
        except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
            app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return (allparametres.serialize())

def local_makeANewparametre(obj0):
    addedparametre = parametre()
    # obj0 = json.loads(obj0)
    self_init(parametre, addedparametre, obj0)
    try:
        db.session.add(addedparametre)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return (addedparametre.serialize())

def local_updateparametre(obj0):
    try:
        updatedparametre = db.session.query(parametre).filter_by(noparametre=obj0['param']).one()
        # obj0 = json.loads(obj0)
        self_init(parametre, updatedparametre, obj0)
        db.session.add(updatedparametre)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Updated an parametre with param %s' % obj0['param']

def local_deleteparametre(obj0):
    try:
        parametreToDelete = db.session.query(parametre).filter_by(param=obj0).one()
        db.session.delete(parametreToDelete)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Removed parametre with param %s' % obj0

