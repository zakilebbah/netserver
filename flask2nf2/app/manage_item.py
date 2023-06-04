from app import app
from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from app.models import Piece, Parametre, Article, Tarif, Tiers, Famille, Cbanque, Item
from app import manage_articles as m_article
from app import db
import json
from app.models import self_init
import datetime
import dateutil.parser
import datetime
import dateutil.parser
import sqlalchemy as sa
from sqlalchemy import and_
import dateutil.parser
import sqlalchemy as sa
from sqlalchemy import func
from datetime import date, datetime
import time
import dateutil.parser
import random

"""
api functions
"""


# def local_get_articles_best_solde(params0):
#     list0 = []
#     try:
#         if ('CODE_TYPE_TARIF' not in params0):
#             params0['CODE_TYPE_TARIF'] = ''
#         if (params0['CODE_TYPE_TARIF']=='%'):
#             params0['CODE_TYPE_TARIF'] = ''
#         # 'Yes' if fruit == 'Apple' else 'No'
#         items = []
#         if params0['CODE_TYPE_TARIF']=='':
#             items = db.session.query(Article, Article.prixventeht.label('TARIF_PRIXHT'), db.func.sum(Item.qte).label('item_tot')
#                 ).join(Article, Article.ref_art == Item.ref_art
#                 ).filter(and_(func.coalesce(Article.master_ref_art, '') == '', Article.boutiq_visible == 1, Item.coeff ==-1)
#                 ).group_by(Article, Article.prixventeht).order_by(func.sum(Item.qte).desc()
#                 ).limit(params0['NB']).all()
#         else: 
#             items = db.session.query(Article, Tarif.prixht.label('TARIF_PRIXHT'), db.func.sum(Item.qte).label('item_tot')
#                 ).join(Article, Article.ref_art == Item.ref_art
#                 ).join(Tarif, and_(Article.ref_art == Tarif.ref_art, Tarif.code_type_tarif == params0['CODE_TYPE_TARIF'])
#                 ).filter(and_(func.coalesce(Article.master_ref_art, '') == '', Article.boutiq_visible == 1, Item.coeff ==-1)
#                 ).group_by(Article, Tarif.prixht).order_by(func.sum(Item.qte).desc()
#                 ).limit(params0['NB']).all()
#         for e in items:
#             pi0 = {'QTE_TOT': e.item_tot, 'TARIF_PRIXHT': e.TARIF_PRIXHT, 'TARIF_PRIXTTC': (e.TARIF_PRIXHT*(1 + e.Article.taux_tva/100))}
#             list0.append(dict(e.Article.serialize(), **pi0))
#             app.logger.info(">>>>>>>>>>>>>>>>>>>>> local_get_articles_best_solde local_get_articles_best_solde" + str(list0))
#         return m_article.extendToImages(list0)
#     except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
#         app.logger.info(">>>>>>>>>>>>>>>>>>>>> local_get_articles_best_solde " + str(list0))
#     return list0
def local_get_articles_best_solde(params0):
    list0 = []
    try:
        if ('CODE_TYPE_TARIF' not in params0):
            params0['CODE_TYPE_TARIF'] = ''
        if (params0['CODE_TYPE_TARIF']=='%'):
            params0['CODE_TYPE_TARIF'] = ''
        # 'Yes' if fruit == 'Apple' else 'No'
        items = []
        subq1 = db.session.query(Item).order_by(Item.noitem.desc()).limit(1000).subquery()
        if params0['CODE_TYPE_TARIF']=='':
            items = db.session.query(Article, Article.prixventeht.label('TARIF_PRIXHT'), db.func.sum(subq1.c.qte).label('item_tot')
                ).join(Article, Article.ref_art == subq1.c.ref_art
                ).filter(and_(Article.boutiq_visible == 1, subq1.c.coeff ==-1)
                ).group_by(Article, Article.prixventeht).order_by(func.sum(subq1.c.qte).desc()
                ).limit(params0['NB']).all()
        else: 
            items = db.session.query(Article, Tarif.prixht.label('TARIF_PRIXHT'), db.func.sum(subq1.c.qte).label('item_tot')
                ).join(Article, Article.ref_art == subq1.c.ref_art
                ).join(Tarif, and_(Article.ref_art == Tarif.ref_art, Tarif.code_type_tarif == params0['CODE_TYPE_TARIF'])
                ).filter(and_(Article.boutiq_visible == 1, subq1.c.coeff ==-1)
                ).group_by(Article, Tarif.prixht).order_by(func.sum(subq1.c.qte).desc()
                ).limit(params0['NB']).all()
        for e in items:
            pi0 = {'QTE_TOT': e.item_tot, 'TARIF_PRIXHT': e.TARIF_PRIXHT, 'TARIF_PRIXTTC': (e.TARIF_PRIXHT*(1 + e.Article.taux_tva/100))}
            list0.append(dict(e.Article.serialize(), **pi0))
        return m_article.extendToImages(list0)
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return list0


def local_get_articles_last_solde(params0):
    list0 = []
    try:
        if ('CODE_TYPE_TARIF' not in params0):
            params0['CODE_TYPE_TARIF'] = ''
        if (params0['CODE_TYPE_TARIF']=='%'):
            params0['CODE_TYPE_TARIF'] = ''
        # 'Yes' if fruit == 'Apple' else 'No'
        items = []
        if params0['CODE_TYPE_TARIF']=='':
            items = db.session.query(Article, Item.noitem, Article.prixventeht.label('TARIF_PRIXHT'), db.func.max(Piece.datepiece).label('maxdatepiece')
                ).join(Article, Article.ref_art == Item.ref_art
                ).join(Piece, Piece.nopiece == Item.nopiece
                ).filter(and_(func.coalesce(Article.master_ref_art, '') == '', Article.boutiq_visible == 1, Item.coeff ==-1)
                ).group_by(Article, Item.noitem, Article.prixventeht).order_by(func.max(Piece.datepiece).desc()).limit(params0['NB']).all()
        else:
            items = db.session.query(Article, Item.noitem, Tarif.prixht.label('TARIF_PRIXHT'), db.func.max(Piece.datepiece).label('maxdatepiece')
                ).join(Article, Article.ref_art == Item.ref_art).join(Piece, Piece.nopiece == Item.nopiece
                ).join(Tarif, and_(Article.ref_art == Tarif.ref_art, Tarif.code_type_tarif == params0['CODE_TYPE_TARIF'])
                ).filter(and_(func.coalesce(Article.master_ref_art, '') == '', Article.boutiq_visible == 1, Item.coeff ==-1)
                ).group_by(Article, Item.noitem, Tarif.prixht).order_by(func.max(Piece.datepiece).desc()).limit(params0['NB']).all()
        for e in items:
            pi0 = {'DATE_MAX': e.maxdatepiece.isoformat(), 'TARIF_PRIXHT': e.TARIF_PRIXHT, 'TARIF_PRIXTTC': (e.TARIF_PRIXHT*(1 + e.Article.taux_tva/100))}
            list0.append(dict(e.Article.serialize(), **pi0))
        return m_article.extendToImages(list0)
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return list0

def local_get_articles_new_items(params0):
    list0 = []
    try:
        # items = db.session.query(Article, db.func.sum(Item.qte*(Item.coeff+Item.coeff_tr)).label('item_tot')).join(Article, Article.ref_art == Item.ref_art).
        #     group_by(Article).order_by(func.sum(Item.qte*(Item.coeff+Item.coeff_tr)).desc()).limit(5).all()
        if ('CODE_TYPE_TARIF' not in params0):
            params0['CODE_TYPE_TARIF'] = ''
        if (params0['CODE_TYPE_TARIF']=='%'):
            params0['CODE_TYPE_TARIF'] = ''
        # 'Yes' if fruit == 'Apple' else 'No'
        items = []
        if params0['CODE_TYPE_TARIF']=='':
            items = db.session.query(Article, Article.prixventeht.label('TARIF_PRIXHT')
            ).filter(and_(func.coalesce(Article.master_ref_art, '') == '', Article.boutiq_visible == 1)
            ).order_by(Article.date_creation.desc()).limit(params0['NB']).all()
        else:
            items = db.session.query(Article, Tarif.prixht.label('TARIF_PRIXHT')
            ).join(Tarif, and_(Article.ref_art == Tarif.ref_art, Tarif.code_type_tarif == params0['CODE_TYPE_TARIF'])
            ).filter(and_(func.coalesce(Article.master_ref_art, '') == '', Article.boutiq_visible == 1)
            ).order_by(Article.date_creation.desc()).limit(params0['NB']).all()
        for e in items:
            pi0 = {'TARIF_PRIXHT': e.TARIF_PRIXHT, 'TARIF_PRIXTTC': (e.TARIF_PRIXHT*(1 + e.Article.taux_tva/100))}
            list0.append(dict(e.Article.serialize(), **pi0))
        return m_article.extendToImages(list0)
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return list0



def local_get_Items():
    allItems = []
    try:
        allItems = db.session.query(Item).all()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return  ([e.serialize() for e in allItems])

def local_get_Item(obj0):
    if (obj0 == ''):
        allItems = []
        try:
            allItems = db.session.query(Item).all()
        except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
            app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return ([e.serialize() for e in allItems])
    else:
        allItems = []
        try:
            allItems = db.session.query(Item).filter_by(noitem=obj0).one()
        except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
            app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return (allItems.serialize())

def local_makeANewItem(obj0):
    addedItem = Item()
    # obj0 = json.loads(obj0)
    if (obj0['NOITEM'] == ''):
        code_site = db.engine.execute("select valeur from public.parametre where param = 'CODE_DU_SITE';").fetchone()
        obj0['NOITEM'] = db.engine.execute(f"select '{code_site[0]}' || nextval('nextitem');").fetchone()[0]
    
    self_init(Item, addedItem, obj0)
    try:
        db.session.add(addedItem)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return {}
    app.logger.info(">>>>>>>>>>>>>>>>>>>>> ITEM ADDED")
    return (addedItem.serialize())
def local_nf2_makeANewItem(obj0):
    addedItem = Item()
    # obj0 = json.loads(obj0)
    code_site = db.engine.execute("select valeur from public.parametre where param = 'CODE_DU_SITE';").fetchone()
    obj0['NOITEM'] = db.engine.execute(f"select '{code_site[0]}' || nextval('nextitem');").fetchone()[0]
   
    self_init(addedItem, addedItem, obj0)
    try:
        db.session.add(addedItem)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return {}
    app.logger.info(">>>>>>>>>>>>>>>>>>>>> ITEM ADDED")
    return (addedItem.serialize())
def local_makeNewItemRandom(obj0):
    articlesCount = db.session.query(Article.ref_art).count()
    addedItem = Item()
    CODE_SITE = db.engine.execute("select valeur from public.parametre where param = 'CODE_DU_SITE';").fetchone()[0]
    addedItem.noitem = db.engine.execute(f"select '{CODE_SITE[0]}' || nextval('nextitem');").fetchone()[0]
    addedItem.nopiece = obj0.nopiece
    # addedItem.ref_art = db.session.query(Article).offset(random.randint(1, articlesCount)).first().ref_art
    addedItem.ref_art = db.session.query(Article).order_by(func.random()).limit(1).first().ref_art
    addedItem.coeff = -1
    addedItem.coeff_tr = 0
    addedItem.qte = random.randint(1, 5)
    addedItem.qteparcolis = 1
    addedItem.prixht = round(random.uniform(200, 10000), 2)
    addedItem.prixttc = addedItem.prixht
    addedItem.datepiece = obj0.datepiece
    addedItem.annulee = 1
    try:
        db.session.add(addedItem)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return {}
    return addedItem
# {"calc_pump": 0, "coeff": -1, "coeff_tr": 0, "datepiece": "2020-06-01T11:30:39", "montant05": 239.0,"montant12": 12.0,"nbcolis": 20.0,"noitem": "14NIV396-11-1","nopiece": "14NIV396-11", "prixht": 239.0,"prixttc": 239.0,"qte": 240.0,"qteparcolis": 12.0,"ref_art": "80618-02000-30"}

def local_updateItem(obj0):
    try:
        updatedItem = db.session.query(Item).filter_by(noitem=obj0['noitem']).one()
        # obj0 = json.loads(obj0)
        self_init(Item, updatedItem, obj0)
        db.session.add(updatedItem)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Updated an Item with noitem %s' % obj0['noitem']

def local_deleteItem(obj0):
    try:
        ItemToDelete = db.session.query(Item).filter_by(noitem=obj0).one()
        db.session.delete(ItemToDelete)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Removed Item with noitem %s' % obj0


    # if 'datepiece' in obj0:
    #   addedItem.datepiece = dateutil.parser.parse(obj0['datepiece'])
    # if 'dateperemp' in obj0:
    #   addedItem.dateperemp = dateutil.parser.parse(obj0['dateperemp'])
    # if 'datefabric' in obj0:
    #   addedItem.datefabric = dateutil.parser.parse(obj0['datefabric'])
    # if 'datemisvente' in obj0:
    #   addedItem.datemisvente = dateutil.parser.parse(obj0['datemisvente'])
    # if 'date001' in obj0:
    #   addedItem.date001 = dateutil.parser.parse(obj0['date001'])
    # if 'date002' in obj0:
    #   addedItem.date002 = dateutil.parser.parse(obj0['date002'])


    # if 'datepiece' in obj0:
    #   updatedItem.datepiece = dateutil.parser.parse(obj0['datepiece'])
    # if 'dateperemp' in obj0:
    #   updatedItem.dateperemp = dateutil.parser.parse(obj0['dateperemp'])
    # if 'datefabric' in obj0:
    #   updatedItem.datefabric = dateutil.parser.parse(obj0['datefabric'])
    # if 'datemisvente' in obj0:
    #   updatedItem.datemisvente = dateutil.parser.parse(obj0['datemisvente'])
    # if 'date001' in obj0:
    #   updatedItem.date001 = dateutil.parser.parse(obj0['date001'])
    # if 'date002' in obj0:
    #   updatedItem.date002 = dateutil.parser.parse(obj0['date002'])
def local_get_Item_cart(obj0):
    pieces = []
    e0 = []
    for piece in obj0:
        allItems = db.session.query(Item).filter_by(nopiece=piece["NOPIECE"]).order_by(Item.datepiece).all()
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> db.session.query(Item)")
        piece["ITEMS"] = [e.serialize() for e in allItems]
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> [e.serialize() for e in allItems]")
    return [e for e in obj0]
def local_delete_artilce_cart(obj0):
    if ('ref_art_delete' in obj0):
        item = db.session.query(Item).filter(Item.nopiece==obj0["nopiece_item_delete"], Item.ref_art==obj0["ref_art_delete"]).delete()
        # piece.status_cart = obj0["status_cart_cancel"]
        db.session.commit()
        return item
    else:
        return ''

def local_nf2_get_piece_items(obj0):
    allItems = []
    try:
        allItems = db.session.query(Item).filter(Item.nopiece == obj0['NOPIECE']).all()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return  ([e.serialize() for e in allItems])
