from app import app
from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from app.models import GpsPositions
from app import db
import json
from app.models import self_init
import datetime
import dateutil.parser
import datetime
import dateutil.parser
import sqlalchemy as sa

"""
api functions
"""

def local_get_GpsPositionss():
    try:
        allGpsPositionss = db.session.query(GpsPositions).all()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return  ([e.serialize() for e in allGpsPositionss])

def local_get_GpsPositions(obj0):
    if (obj0 == ''):
        try:
            allGpsPositionss = db.session.query(GpsPositions).all()
        except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
            app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return ([e.serialize() for e in allGpsPositionss])
    else:
        try:
            allGpsPositionss = db.session.query(GpsPositions).filter_by(gps_id=obj0).one()
        except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
            app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return (allGpsPositionss.serialize())

def local_makeANewGpsPositions(obj0):
    addedGpsPositions = GpsPositions()
    # obj0 = json.loads(obj0)
    self_init(GpsPositions, addedGpsPositions, obj0)
    try:
        db.session.add(addedGpsPositions)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return (addedGpsPositions.serialize())

# {"calc_pump": 0, "coeff": -1, "coeff_tr": 0, "datepiece": "2020-06-01T11:30:39", "montant05": 239.0,"montant12": 12.0,"nbcolis": 20.0,"noGpsPositions": "14NIV396-11-1","nopiece": "14NIV396-11", "prixht": 239.0,"prixttc": 239.0,"qte": 240.0,"qteparcolis": 12.0,"ref_art": "80618-02000-30"}

def local_updateGpsPositions(obj0):
    try:
        updatedGpsPositions = db.session.query(GpsPositions).filter_by(gps_id=obj0['gps_id']).one()
        # obj0 = json.loads(obj0)
        self_init(GpsPositions, updatedGpsPositions, obj0)
        db.session.add(updatedGpsPositions)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Updated an GpsPositions with gps_id %s' % obj0['gps_id']

def local_deleteGpsPositions(obj0):
    try:
        GpsPositionsToDelete = db.session.query(GpsPositions).filter_by(gps_id=obj0).one()
        db.session.delete(GpsPositionsToDelete)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Removed GpsPositions with gps_id %s' % obj0



    # if 'gps_date' in obj0:
    #   addedGpsPositions.gps_date = dateutil.parser.parse(obj0['gps_date'])
    
    # if 'gps_date' in obj0:
    #   updatedGpsPositions.gps_date = dateutil.parser.parse(obj0['gps_date'])
