from app import app
from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from app.models import Item, Parametre, Article, Tiers, Famille, Cbanque, Piece
from app import db
import json
from app.models import self_init
import datetime
import dateutil.parser
from app import manage_item as m_item
import sqlalchemy as sa
import random
from sqlalchemy import func
from sqlalchemy import and_
import sqlalchemy
from sqlalchemy.sql.expression import cast

import math 

"""
api functions
"""

# articles1 = extendToImages(articles0)
def nf2_extendToItems(pieces0):
    list0 = []
    for e in pieces0:
        ee = {key.upper(): value for (key, value) in e.items() if (key.upper() != 'DETAIL2')}
        app.logger.info(">>>>>>>>>>>>>>>")
        app.logger.info(">>>>>>>>>>>>>>> E = " + str(e))
        pi0 = {'NOPIECE': e['NOPIECE'], 'ITEMS': [], 'VERSEMENTS': []}
        # add items
        nopiece = e['NOPIECE']
        items = []
        allItems = db.session.query(Item).filter(Item.nopiece==nopiece).all()
        items = [{key.upper(): value for (key, value) in e1.serialize().items() if (key.upper() != 'DETAIL2')} for e1 in allItems]
        app.logger.info(">>>>>>>>>>>>>>> II = " + str(items))
        pi0['ITEMS'] = items
        # add versements
        nopiece_o = e['NOPIECE']
        versements = []
        allVersements = db.session.query(Piece).filter(Piece.nopiece_o==nopiece_o).all()
        versements = [{key.upper(): value for (key, value) in e2.serialize().items() if (key.upper() != 'DETAIL2')} for e2 in allVersements]
        app.logger.info(">>>>>>>>>>>>>>> VV = " + str(versements))
        pi0['VERSEMENTS'] = versements

        list0.append(dict(ee, **pi0))
    return list0

def local_nf2_get_Pieces(obj0):
    try:
      allPieces = db.session.query(Piece)[int(obj0['LBrowPieces']):int(obj0['UBrowPieces'])]
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return []
    return nf2_extendToItems([e.serialize() for e in allPieces])
def local_nf2_get_only_piece(obj0):
    print(obj0)
    try:
        if (obj0['search_value'] == ''):
            allPieces = db.session.query(Piece).filter(Piece.datepiece >= obj0['date1'], Piece.datepiece <= obj0['date2'], Piece.code_type_piece == obj0['code_type_piece'])[int(obj0['LBrowPieces']):int(obj0['UBrowPieces'])]
        elif (obj0['search_column'] == 'NOPIECE' and obj0['search_value'] != ''):
            allPieces = db.session.query(Piece).filter(Piece.datepiece >= obj0['date1'], Piece.datepiece <= obj0['date2'], Piece.code_type_piece == obj0['code_type_piece'], func.lower(Piece.nopiece).like(func.lower(f"%{obj0['search_value']}%")))[int(obj0['LBrowPieces']):int(obj0['UBrowPieces'])]
        elif (obj0['search_column'] == 'REF_PIECE' and obj0['search_value'] != ''):
            allPieces = db.session.query(Piece).filter(Piece.datepiece >= obj0['date1'], Piece.datepiece <= obj0['date2'], Piece.code_type_piece == obj0['code_type_piece'], cast( Piece.ref_piece, sqlalchemy.String ).like(func.lower(f"%{obj0['search_value']}%")))[int(obj0['LBrowPieces']):int(obj0['UBrowPieces'])]
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return []
    return [e.serialize() for e in allPieces]
def local_nf2_get_only_piece_count(obj0):
    count = 0
    print(obj0)
    try:
        if (obj0['search_value'] == ''):
            count = db.session.query(Piece).filter(Piece.datepiece >= obj0['date1'], Piece.datepiece <= obj0['date2'], Piece.code_type_piece == obj0['code_type_piece']).count()
        elif (obj0['search_column'] == 'NOPIECE' and obj0['search_value'] != ''):
            count = db.session.query(Piece).filter(Piece.datepiece >= obj0['date1'], Piece.datepiece <= obj0['date2'], Piece.code_type_piece == obj0['code_type_piece'], func.lower(Piece.nopiece).like(func.lower(f"%{obj0['search_value']}%"))).count()
        elif (obj0['search_column'] == 'REF_PIECE' and obj0['search_value'] != ''):
            count = db.session.query(Piece).filter(Piece.datepiece >= obj0['date1'], Piece.datepiece <= obj0['date2'], Piece.code_type_piece == obj0['code_type_piece'], cast( Piece.ref_piece, sqlalchemy.String ).like(func.lower(f"%{obj0['search_value']}%"))).count()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return []
    return {'count': count}
def local_nf2_get_one_piece(obj0):
    try:
      allPieces = db.session.query(Piece).filter(Piece.nopiece == obj0['NOPIECE']).order_by(Piece.datepiece.desc()).first()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return []
    return nf2_extendToItems([e.serialize() for e in [allPieces]])

def local_nf2_get_piece_versements(obj0):
    allPieces = []
    try:
      allPieces = db.session.query(Piece).filter(Piece.nopiece_o == obj0['NOPIECE_O']).order_by(Piece.datepiece.desc()).all()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return []
    return [e.serialize() for e in allPieces]

def local_get_Piece(obj0):
    allPieces = []
    if (obj0 == ''):
        allPieces = db.session.query(Piece).all()
        return ([e.serialize() for e in allPieces])
    else:
        allPieces = db.session.query(Piece).filter_by(nopiece=obj0).one()
        return (allPieces.serialize())

def local_makeANewPiece(obj0):
    # app.logger.info("################# local_makeANewPiece " + str(obj0))
    app.logger.info("################# new PIECE")
    code_site = db.engine.execute("select valeur from public.parametre where param = 'CODE_DU_SITE';").fetchone()
    obj0['NOPIECE'] = db.engine.execute(f"select '{code_site[0]}' || nextval('nextpiece');").fetchone()[0]
    nopiece = obj0['NOPIECE']
    addedPiece = Piece()
    # obj0 = json.loads(obj0)
    self_init(Piece, addedPiece, obj0)
    try:
        db.session.add(addedPiece)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return []
    pi0 = [{'NOPIECE': addedPiece.nopiece, 'REF_PIECE': addedPiece.ref_piece}]
    
    if ('ITEMS' in obj0):
        app.logger.info("################# new ITEM")
        for item0 in obj0['ITEMS']:
            item0["NOPIECE"] = nopiece
            it0 = m_item.local_makeANewItem(item0)
            if 'NOITEM' in item0:
                pi0.append({'NOITEM': item0['NOITEM']})
            else:
                pi0.append({'NOITEM': ''})
        return pi0
    else:
        return pi0

def local_makeANewPieces(pieces0):
    commitedPieces0 = []
    for piece0 in pieces0:
        p0 = local_makeANewPiece(piece0)
        if commitedPieces0 == []:
            commitedPieces0 = p0
        else:
            app.logger.info("################# append to commitedPieces0 ")
            app.logger.info("################# commitedPieces0 " + str(commitedPieces0))
            app.logger.info("################# p0 " + str(p0))
            commitedPieces0 = commitedPieces0 + p0
    # app.logger.info("################# local_makeANewPieces return " + str(commitedPieces0))
    return (commitedPieces0)


def local_nf2_makeANewPiece(obj0):
    print(obj0)
    # app.logger.info("################# local_makeANewPiece " + str(obj0))
    app.logger.info("################# new PIECE")
    addedPiece = Piece()
    # if (obj0['NOPIECE'] == '') :
    #     code_site = db.engine.execute("select valeur from public.parametre where param = 'CODE_DU_SITE';").fetchone()
    #     obj0['NOPIECE'] =  obj0['CODE_SITE'] + db.engine.execute(f"select '{code_site[0]}' || nextval('nextpiece');").fetchone()[0]
    #     addedPiece = Piece()
    # else :
    PieceExists = db.session.query(db.session.query(Piece).filter_by(nopiece=obj0['NOPIECE']).exists()).scalar()
    if (PieceExists):
        db.session.query(Piece).filter(Piece.nopiece_o == obj0['NOPIECE']).delete()
        db.session.query(Item).filter(Item.nopiece == obj0['NOPIECE']).delete()
        db.session.query(Piece).filter(Piece.nopiece == obj0['NOPIECE']).delete()
        
    # if (obj0['REF_PIECE'] < 0):
    #    obj0['REF_PIECE'] = db.session.connection().execute(f"select max(ref_piece)+1 from piece where code_type_piece = '{obj0['CODE_TYPE_PIECE']}' ;").fetchone()[0]
    nopiece = obj0['NOPIECE']
    # obj0 = json.loads(obj0)
    self_init(Piece, addedPiece, obj0)   
    app.logger.info(">>>>>>>>>>>>>>>>>>>>> addedPiece addedPiece addedPiece addedPiece addedPiece addedPiece addedPiece addedPiece" + str(addedPiece))     
    try:
        db.session.add(addedPiece)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return []
    pi0 = [{'NOPIECE': addedPiece.nopiece, 'REF_PIECE': addedPiece.ref_piece}]
    if ('VERSEMENTS' in obj0):
        for vers in obj0['VERSEMENTS']:
            vers['NOPIECE_O'] = obj0['NOPIECE']
            res = local_nf2_makeANewVersements(vers)
            pi0.append({'NOPIECE': res['NOPIECE'], 'NOPIECE_O': res['NOPIECE_O']})
    if ('ITEMS' in obj0):
        for item0 in obj0['ITEMS']:
            item0["NOPIECE"] = nopiece
            it0 = m_item.local_nf2_makeANewItem(item0)
            if 'NOITEM' in item0:
                pi0.append({'NOITEM': item0['NOITEM']})
            else:
                pi0.append({'NOITEM': ''})
        return pi0
    else:
        return pi0

def local_nf2_makeANewVersements(obj0): 
    addedPiece = Piece()
    # if (obj0['NOPIECE'] == '') :
    #     code_site = db.engine.execute("select valeur from public.parametre where param = 'CODE_DU_SITE';").fetchone()
    #     obj0['NOPIECE'] =  obj0['CODE_SITE'] + db.engine.execute(f"select '{code_site[0]}' || nextval('nextpiece');").fetchone()[0]
    # if (obj0['REF_PIECE'] < 0):
    #    obj0['REF_PIECE'] = db.session.connection().execute(f"select max(ref_piece)+1 from piece where code_type_piece = '{obj0['CODE_TYPE_PIECE']}' ;").fetchone()[0]
    self_init(Piece, addedPiece, obj0)        
    try:
        db.session.add(addedPiece)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
        return []
    return addedPiece.serialize()
def local_nf2_makeANewPieces(pieces0):
    commitedPieces0 = []
    for piece0 in pieces0:
        p0 = local_nf2_makeANewPiece(piece0)
        if commitedPieces0 == []:
            commitedPieces0 = p0
        else:
            app.logger.info("################# append to commitedPieces0 ")
            app.logger.info("################# commitedPieces0 " + str(commitedPieces0))
            app.logger.info("################# p0 " + str(p0))
            commitedPieces0 = commitedPieces0 + p0
    # app.logger.info("################# local_makeANewPieces return " + str(commitedPieces0))
    return (commitedPieces0)
def local_makeNewPicesrandom(obj0):
    i = 0
    j = 0
    if obj0:
        pieceNumber = obj0["NUMBER"]
    else:
        pieceNumber = 3000
    tiersCount = db.session.query(Tiers.code_tiers).count()
    addedPiece = Piece()
    CODE_SITE = db.engine.execute("select valeur from public.parametre where param = 'CODE_DU_SITE';").fetchone()
    print(CODE_SITE)
    for i in range(pieceNumber):
        app.logger.info("#################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ PIECE NUMBER NUMBER NUMBER NUMBER NUMBER  " + str(i))
        app.logger.info("#################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ addedPiece.nopiece addedPiece.nopiece addedPiece.nopiece addedPiece.nopiece addedPiece.nopiece " + str(CODE_SITE))
        itemNumber = random.randint(1, 5)
        addedPiece = Piece()
        addedPiece.nopiece = db.engine.execute(f"select '{CODE_SITE[0]}' || nextval('nextpiece');").fetchone()[0]
        addedPiece.code_type_piece = "PC_VE_B"
        addedPiece.ref_piece = db.session.connection().execute("select max(ref_piece)+1 from piece where code_type_piece = 'PC_VE_B' ;").fetchone()[0]
        # addedPiece.ref_piece = db.session.query(func.max(Piece.ref_piece)).filter_by(code_type_piece = 'PC_VE_B')
        addedPiece.code_site = db.engine.execute("select valeur from public.parametre where param = 'CODE_DU_SITE';").fetchone()[0]
        addedPiece.code_tiers = db.session.query(Tiers).order_by(func.random()).limit(1).first().code_tiers
        addedPiece.datepiece = datetime.datetime.now()
        addedPiece.coeff = -1
        addedPiece.coeff_tr = 0
        addedPiece.montantht = 0
        addedPiece.montant = addedPiece.montantht
        addedPiece.montantttc = addedPiece.montantht
        failed = False
        try:
            db.session.add(addedPiece)
            db.session.commit()
        except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
            failed = True
        if not failed:
            j = 0
            montant = 0
            while j < itemNumber:
                addedItem = m_item.local_makeNewItemRandom(addedPiece)
                montant = montant + addedItem.prixht
                j = j + 1
            newAddedPiece = db.session.query(Piece).filter_by(nopiece = addedPiece.nopiece).update(dict(montantht = montant, montant=montant, montantttc=montant))
            db.session.commit()
        app.logger.info("#################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ PIECE NOPIECE " + str(addedPiece.nopiece))
        addedPiece = None
        i = i + 1
    return "Success" + str(i)

def local_updatePiece(obj0):
    try:
        updatedPiece = db.session.query(Piece).filter_by(status_cart=obj0['status_cart']).one()
        # obj0 = json.loads(obj0)
        self_init(Piece, updatedPiece, obj0)
        db.session.add(updatedPiece)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Updated an Piece with nopiece %s' % obj0['nopiece']

def local_deletePiece(obj0):
    try:
        PieceToDelete = db.session.query(Piece).filter_by(nopiece=obj0).one()
        db.session.delete(PieceToDelete)
        db.session.commit()
    except (sa.exc.SQLAlchemyError, sa.exc.DBAPIError) as e:
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> Encountered SQLAlchemyError!" + str(e))
    return 'Removed Piece with nopiece %s' % obj0



def countPanierPiece(obj0):
    numOfPiece = db.session.query(Piece).filter(Piece.emailnet==obj0["email"], Piece.code_type_piece=="PC_VE_PAN", Piece.status_cart!="an").count()
    return {"number": math.ceil(numOfPiece/10)}
def local_get_Pieces_cart(obj0):
    app.logger.info(">>>>>>>>>>>>>>>>>>>>> PIECE EMAIL" + str(obj0))
    # allPieces = db.session.query(Piece).all()
    if ('emailnet' in obj0):
        piece = db.session.query(Piece).filter(Piece.emailnet==obj0["emailnet"], Piece.code_type_piece=="PC_VE_PAN", Piece.status_cart!="an").order_by(Piece.datepiece.desc()).limit(10).offset((obj0["page"]-1)*10).all()
    else :
        piece = []
    
    return [e.serialize() for e in piece]

def local_cancel_Pieces_cart(obj0):
    if ('nopiece_cancel' in obj0):
        piece = db.session.query(Piece).filter_by(nopiece=obj0["nopiece_cancel"]).one()
        piece.status_cart = obj0["status_cart_cancel"]
        piece.chaine20 = obj0["status_cart_etat"]
        piece.annulee = 0
        db.session.commit()
        return piece.serialize()
    else:
        return ''

def local_update_montant_Pieces_cart(obj0):
    if ('nopiece_item_delete' in obj0):
        piece = db.session.query(Piece).filter_by(nopiece=obj0["nopiece_item_delete"]).one()
        # piece.status_cart = obj0["status_cart_cancel"]
        piece.montant = obj0["montant"]
        piece.montantttc = obj0["montant"]
        piece.montantht = obj0["montant"]
        db.session.commit()
        return piece.serialize()
    else:
        return ''

def get_piece_Vitrine(obj0):
    pieces0 = db.session.query(Piece.refdoc, Piece.date001).filter_by(code_type_piece='PC_VE_VITRINE').all()
    refdocs = []
    for refdoc in pieces0:
        refdocs.append((str(refdoc[0]),refdoc[1]))
    return refdocs

def get_item_vitrine(obj0):
    items = []
    count = 0
    if obj0["TYPE"] == "all":
        pieces0 = get_piece_Vitrine(obj0)
        count = 0
        obk = {}
        # app.logger.info(">>>>>>>>>>>>>>>>>>>>> items0 items0 items0" + str(pieces0))
        for item in pieces0:
            items.append({"title": item[0],"products": [], "date": item[1]})
            items0 = db.session.query(Item.ref_art).join(Piece, Piece.nopiece==Item.nopiece).join(Article, Article.ref_art == Item.ref_art).filter(Piece.refdoc==item[0]).order_by(Piece.nopiece).limit(6)
            for item1 in items0:
                items[count]["products"].append(item1[0])
            count += 1
        return items
    elif obj0["TYPE"] == "specific":
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> gggg ggggggg g")
        # items.append({obj0["REFDOC"]: []})
        item = db.session.query(Piece.refdoc, Piece.date001).filter(Piece.code_type_piece=='PC_VE_VITRINE', Piece.refdoc==obj0["REFDOC"]).one()
        # app.logger.info(">>>>>>>>>>>>>>>>>>>>> items0 items0 items0" + str(item))
        piece={"title": item[0],"products": [], "date": item[1]}
        items0 = db.session.query(Item.ref_art).join(Piece, Piece.nopiece==Item.nopiece).join(Article, Article.ref_art == Item.ref_art).filter(Piece.refdoc==obj0["REFDOC"]).order_by(Piece.nopiece).all()
        for item1 in items0:
            piece["products"].append(item1[0])
        # app.logger.info(">>>>>>>>>>>>>>>>>>>>> items0 items0 items0" + str(items0))
        app.logger.info(">>>>>>>>>>>>>>>>>>>>> items items items" + str(items))
        return piece

def getOnePiece(nopiece):
    piece = db.session.query(Piece).filter(Piece.nopiece==nopiece).all()
    app.logger.info(">>>>>>>>>>>>>>>>>>>>> getOnePiece getOnePiece getOnePiece" + str(nopiece))
    # piece = piece.serialize()
    return  ([e.serialize() for e in piece])

def local_update_deliveryCode_Pieces_cart(obj0):
    if ('nopiece_deliveryCode' in obj0):
        piece = db.session.query(Piece).filter_by(nopiece=obj0["nopiece_deliveryCode"]).one()
        piece.chaine08 = obj0["code"]
        db.session.commit()
        return piece.serialize()
    else:
        return ''