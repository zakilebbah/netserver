from app import app
from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from app.models import LocalTypePiece
from app import db
import json
from app.models import self_init
import datetime
import dateutil.parser
import sqlalchemy as sa

"""
api functions
"""

def local_get_LocalTypePieces():
    allLocalTypePieces = []
    try:
        allLocalTypePieces = db.session.query(LocalTypePiece).all()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return  ([e.serialize() for e in allLocalTypePieces])

def local_get_LocalTypePiece(obj0):
    if (obj0 == ''):
        allLocalTypePieces = []
        try:
            allLocalTypePieces = db.session.query(LocalTypePiece).all()
        except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
            app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return ([e.serialize() for e in allLocalTypePieces])
    else:
        allLocalTypePieces = []
        try:
            allLocalTypePieces = db.session.query(LocalTypePiece).filter_by(code_type_piece=obj0).one()
        except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
            app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return (allLocalTypePieces.serialize())

def local_makeANewLocalTypePiece(obj0):
    addedLocalTypePiece = LocalTypePiece()
    # obj0 = json.loads(obj0)
    self_init(LocalTypePiece, addedLocalTypePiece, obj0)
    try:
        db.session.add(addedLocalTypePiece)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return (addedLocalTypePiece.serialize())

def local_updateLocalTypePiece(obj0):
    try:
        updatedLocalTypePiece = db.session.query(LocalTypePiece).filter_by(code_type_piece=obj0['code_type_piece']).one()
        # obj0 = json.loads(obj0)
        self_init(LocalTypePiece, updatedLocalTypePiece, obj0)
        db.session.add(updatedLocalTypePiece)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Updated an LocalTypePiece with code_type_piece %s' % obj0['code_type_piece']

def local_deleteLocalTypePiece(obj0):
    try:
        LocalTypePieceToDelete = db.session.query(LocalTypePiece).filter_by(code_type_piece=obj0).one()
        db.session.delete(LocalTypePieceToDelete)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Removed LocalTypePiece with code_type_piece %s' % obj0

