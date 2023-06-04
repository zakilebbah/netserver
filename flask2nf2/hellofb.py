import os
from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy  
import fdb
    
app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'firebird+fdb://sysdba:masterkey@localhost/C:/wamp64/www/wf1-backend/data/webdata.GDB'
# app.config['SECRET_KEY'] = "secret key"  

# app.config['SQLALCHEMY_DATABASE_URI'] = 'firebird+fdb://sysdba:masterkey@localhost:3050/C:/wamp64/www/wf1-backend/data/webdata.GDB'

# firebird+fdb://sysdba:masterkey@localhost:3050/
# localhost:c:\fdbb\school.fdb
# engine = create_engine('firebird+fdb://sysdba:masterkey@localhost:3050/c:/fdbb/school.fdb')

db = SQLAlchemy(app)  

class Parametre(db.Model):  
    __tablename__ = 'PARAMETRE'
    #id = db.Column('employee_id', db.Integer, primary_key = True)  
    param = db.Column('param', db.String(30), primary_key = True)  
    valeur = db.Column(db.String(40000))   

    def __init__(self, param, valeur):  
        self.param = param  
        self.valeur = valeur  

    def serialize(self):
        return {
            'param': self.param, 
            'valeur': self.valeur
        }


# class Famille(db.Model):  
#     __tablename__ = 'famille'
#     codefamille = db.Column(db.String(20), primary_key = True)  
#     codefamille_m = db. Column(db.String(40000), db.ForeignKey('famille.codefamille'),  nullable=True)   
#     #...




@app.route("/getall")
def get_all():
    try:
        params=Parametre.query.all()
        return  jsonify([e.serialize() for e in params])
    except Exception as e:
	    return(str(e))


    
if __name__ == '__main__':  
    db.create_all()  
    app.run(debug = True)  