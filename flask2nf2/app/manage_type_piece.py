from app import app
from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from app.models import TypePiece
from app import db
import json
from app.models import self_init
import datetime
import dateutil.parser
import sqlalchemy as sa

"""
api functions
"""

def local_get_TypePieces():
    allTypePieces = db.session.query(TypePiece).all()
    return  ([e.serialize() for e in allTypePieces])

def local_get_TypePiece(obj0):
    allTypePieces = []
    if (obj0 == ''):
        allTypePieces = db.session.query(TypePiece).all()
        return ([e.serialize() for e in allTypePieces])
    else:
        allTypePieces = db.session.query(TypePiece).filter_by(code_type_piece=obj0).one()
        return (allTypePieces.serialize())

def local_makeANewTypePiece(obj0):
    addedTypePiece = TypePiece()
    # obj0 = json.loads(obj0)
    self_init(TypePiece, addedTypePiece, obj0)
    db.session.add(addedTypePiece)
    db.session.commit()
    return (addedTypePiece.serialize())

def local_updateTypePiece(obj0):
    updatedTypePiece = db.session.query(TypePiece).filter_by(code_type_piece=obj0['code_type_piece']).one()
    # obj0 = json.loads(obj0)
    self_init(TypePiece, updatedTypePiece, obj0)
    db.session.add(updatedTypePiece)
    db.session.commit()
    return 'Updated an TypePiece with code_type_piece %s' % obj0['code_type_piece']

def local_deleteTypePiece(obj0):
    TypePieceToDelete = db.session.query(TypePiece).filter_by(code_type_piece=obj0).one()
    db.session.delete(TypePieceToDelete)
    db.session.commit()
    return 'Removed TypePiece with code_type_piece %s' % obj0

