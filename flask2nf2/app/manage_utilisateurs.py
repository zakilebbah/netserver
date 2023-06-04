from app import app
from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from app.models import Utilisateurs
from app import db
import json
from app.models import self_init
import datetime
import dateutil.parser
import sqlalchemy as sa

"""
api functions
"""

def local_get_Utilisateurss():
    allUtilisateurss = []
    try:
        allUtilisateurss = db.session.query(Utilisateurs).all()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return  ([e.serialize() for e in allUtilisateurss])

def local_get_Utilisateurs(obj0):
    if (obj0 == ''):
        allUtilisateurss = []
        try:
            allUtilisateurss = db.session.query(Utilisateurs).all()
        except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
            app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return ([e.serialize() for e in allUtilisateurss])
    else:
        allUtilisateurss = []
        try:
            allUtilisateurss = db.session.query(Utilisateurs).filter_by(username=obj0).one()
        except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
            app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return (allUtilisateurss.serialize())

def local_makeANewUtilisateurs(obj0):
    addedUtilisateurs = Utilisateurs()
    # obj0 = json.loads(obj0)
    self_init(Utilisateurs, addedUtilisateurs, obj0)
    try:
        db.session.add(addedUtilisateurs)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return (addedUtilisateurs.serialize())

def local_updateUtilisateurs(obj0):
    try:
        updatedUtilisateurs = db.session.query(Utilisateurs).filter_by(username=obj0['username']).one()
        # obj0 = json.loads(obj0)
        self_init(Utilisateurs, updatedUtilisateurs, obj0)
        db.session.add(updatedUtilisateurs)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Updated an Utilisateurs with username %s' % obj0['username']

def local_deleteUtilisateurs(obj0):
    try:
        UtilisateursToDelete = db.session.query(Utilisateurs).filter_by(username=obj0).one()
        db.session.delete(UtilisateursToDelete)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Removed Utilisateurs with username %s' % obj0

