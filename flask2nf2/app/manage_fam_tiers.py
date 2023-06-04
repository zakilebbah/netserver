from app import app
from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from app.models import Parametre, Article, Tiers, Famille, FamTiers
from app import db
import json
from app.models import self_init
import datetime
import dateutil.parser
import sqlalchemy as sa

"""
api functions
"""

def local_get_FamTierss():
    allFamTierss = []
    try:
        allFamTierss = db.session.query(FamTiers).all()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return  ([e.serialize() for e in allFamTierss])

def local_get_FamTiers(obj0):
    if (obj0 == ''):
        allFamTierss = []
        try:
            allFamTierss = db.session.query(FamTiers).all()
        except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
            app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return ([e.serialize() for e in allFamTierss])
    else:
        allFamTierss = []
        try:
            allFamTierss = db.session.query(FamTiers).filter_by(code_fam_tiers=obj0).one()
        except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
            app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return (allFamTierss.serialize())
        
def local_makeANewFamTiers(obj0):
    addedFamTiers = FamTiers()
    # obj0 = json.loads(obj0)
    self_init(FamTiers, addedFamTiers, obj0)
    try:
        db.session.add(addedFamTiers)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return (addedFamTiers.serialize())

def local_updateFamTiers(obj0):
    try:
        updatedFamTiers = db.session.query(FamTiers).filter_by(code_fam_tiers=obj0['code_fam_tiers']).one()
        # obj0 = json.loads(obj0)
        self_init(FamTiers, updatedFamTiers, obj0)
        db.session.add(updatedFamTiers)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Updated an FamTiers with code_fam_tiers %s' % obj0['code_fam_tiers']

def local_deleteFamTiers(obj0):
    try:
        FamTiersToDelete = db.session.query(FamTiers).filter_by(code_fam_tiers=obj0).one()
        db.session.delete(FamTiersToDelete)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Removed FamTiers with code_fam_tiers %s' % obj0

