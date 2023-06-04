from app import app
from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from app.models import Tarif
from app import db
import json
from app.models import self_init
import datetime
import dateutil.parser
import sqlalchemy as sa

"""
api functions
"""

def local_get_Tarifs():
    allTarifs = []
    try:
        allTarifs = db.session.query(Tarif).all()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return  ([e.serialize() for e in allTarifs])

def local_get_Tarif(obj0):
    if (obj0 == ''):
        allTarifs = []
        try:
            allTarifs = db.session.query(Tarif).all()
        except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
            app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return ([e.serialize() for e in allTarifs])
    else:
        allTarifs = []
        try:
            allTarifs = db.session.query(Tarif).filter_by(code_tarif=obj0).one()
        except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
            app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return (allTarifs.serialize())

def local_makeANewTarif(obj0):
    addedTarif = Tarif()
    # obj0 = json.loads(obj0)
    self_init(Tarif, addedTarif, obj0)
    try:
        db.session.add(addedTarif)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return (addedTarif.serialize())

def local_updateTarif(obj0):
    try:
        updatedTarif = db.session.query(Tarif).filter_by(code_tarif=obj0['code_tarif']).one()
        # obj0 = json.loads(obj0)
        self_init(Tarif, updatedTarif, obj0)
        db.session.add(updatedTarif)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Updated an Tarif with code_tarif %s' % obj0['noTacode_tarifrif']

def local_deleteTarif(obj0):
    try:
        TarifToDelete = db.session.query(Tarif).filter_by(code_tarif=obj0).one()
        db.session.delete(TarifToDelete)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Removed Tarif with code_tarif %s' % obj0

