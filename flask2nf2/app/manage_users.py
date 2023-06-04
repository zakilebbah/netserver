from app import app
from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from app.models import User, Tiers
from app import db
import json
from app.models import self_init, self_insert
import datetime
import dateutil.parser
import sqlalchemy as sa

"""
api functions
"""

def local_get_Users():
    allUsers = []
    try:
        allUsers = db.session.query(User).all()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return  ([e.serialize() for e in allUsers])

def local_get_User(email0):
    allUsers = []
    try:
        allUsers = db.session.query(Tiers).filter_by(email=email0).one()
        # app.logger.info(">>>>>>>>>>>>>>>>>>>>> allUsers allUsers allUsers" + str(allUsers))
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return (allUsers.serialize())

def local_makeANewUser(obj0):
    addedUser = Tiers()
    # obj0 = json.loads(obj0)
    code_site = db.engine.execute("select valeur from public.parametre where param = 'CODE_DU_SITE';").fetchone()
    obj0['code_tiers'] = db.engine.execute(f"select '{code_site[0]}' || '$' || nextval('nexttiers');").fetchone()[0]
    if (obj0['raison_sociale'] == ''):
        obj0['raison_sociale'] = obj0['prenomnet'] + ' ' + obj0['usernamenet']

    # obj0['code_tiers'] = 
    self_init(Tiers, addedUser, obj0)
    addedUser.hash_password(obj0['passwordnet'])
    app.logger.info(">>>>>>>>>>>>>>>>>>>>> OBJ OBJ OBJ OBJ " + str(addedUser.serialize()))
    try:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Before idusernet remmove field!")
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> After idusernet remmove field!" + str(addedUser.serialize()))
        # delattr(addedUser, "idusernet")
        # app.logger.info(">>>>>>>>>>>>>>>>>>>>> After idusernet remmove field!" + str(addedUser.serialize()))
        # db.session.add(addedUser)
        # db.session.execute("insert into usernet (emailnet, passwordnet) values ('yyyy02@gmail.com', 'toto00')")
        # result = session.execute( "SELECT * FROM user WHERE id=:param",{"param":5})
        query0 = self_insert(Tiers, addedUser.serialize())
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> QUERY! " + query0)
        db.session.execute(query0, addedUser.serialize())
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return (addedUser.serialize())

def local_updateUser(obj0):
    try:
        updatedUser = db.session.query(Tiers).filter_by(email=obj0['EMAIL']).one()
        # obj0 = json.loads(obj0)
        self_init(Tiers, updatedUser, obj0)
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> PASSWORDNET PASSWORDNET!" + str(obj0['PASSWORDNET']))
        updatedUser.hash_password(obj0['PASSWORDNET'])
        db.session.add(updatedUser)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Updated an User with username %s' % obj0['EMAIL']

def local_deleteUser(obj0):
    try:
        UserToDelete = db.session.query(User).filter_by(emailnet=obj0).one()
        db.session.delete(UserToDelete)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Removed User with username %s' % obj0

# ####################################zakaria####################
def local_updateUser_password(email, password):
    try:
        updatedUser = db.session.query(Tiers).filter(Tiers.email==email).one()
        # obj0 = json.loads(obj0)
        # self_init(User, updatedUser, obj0)
        updatedUser.hash_password(password)
        db.session.add(updatedUser)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Updated an User with username %s' % email
