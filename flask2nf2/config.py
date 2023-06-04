import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'firebird+fdb://sysdba:masterkey@localhost/C:/wamp64/www/wf1-backend/data/webdata.GDB'

    # SQLALCHEMY_DATABASE_URI = 'firebird+fdb://SYSDBA:masterkey@192.168.1.17/C:/OranSoft/NetFact2/Data/hamaza2019.FDB?charset=ISO8859_1'
    # SQLALCHEMY_DATABASE_URI = 'firebird+fdb://SYSDBA:masterkey@192.168.1.150/C:/OranSoft/NetFact2/Data/test.FDB?charset=ISO8859_1'
    # SQLALCHEMY_DATABASE_URI = 'firebird+fdb://SYSDBA:masterkey@192.168.1.15/D:/Programs/netfact2/webdata.GDB?charset=ISO8859_1'

    # POSTGRES = {
    # 'user': 'postgres',
    # 'pw': 'masterkey',
    # 'db': 'DatabaseFirst',
    # 'host': 'localhost',
    # 'port': '5432',
    # }

    # SQLALCHEMY_DATABASE_URI = 'firebird+fdb://SYSDBA:masterkey@localhost/E:/OranSoft/data/nf2test/BIG-BDD-Clients/NEW-ALFATRON-BiG-SupMohamedSTOCK-2020.FDB?charset=ISO8859_1'
    # D:/OranSoft/data/nf2test/os2007/OS2007.fdb?charset=ISO8859_1'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:masterkey2@localhost:5432/hamaza2021'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Hc8Kc6X3Fz40Rk2pzj@172.25.31.91:5432/os'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:masterkey@192.168.1.150:5432/os00'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:masterkey@localhost:5432/oth01'
    # UPLOAD_FOLDER = '/home/ya77ia/home/zakilbh/things/programming/web/flask-store/flask2nf2/app/articles-images'
    # UPLOAD_FOLDER = '/home/za4i/things/programming/web/flask-store/upload_images'
    # UPLOAD_FOLDER = 'E:/OranSoft/osgit/netserver/flask2nf2/app/articles-images'
    ERRORS_LOGGER = 'errors.log'
    IMAGES_FOLDER = "/home/za4i/things/programming/web/flask-store/images-hamaza2"
    # IMAGES_FOLDER = "/home/za4i/things/programming/web/flask-store/images-hamaza2"    
    # IMAGES_FOLDER = "E:/OranSoft/osgit/netserver/flask2nf2/app/images-client"
    PRODUCTS_IMAGES = f'{IMAGES_FOLDER}/articles'
    PRODUCTS_COVERS = f'{IMAGES_FOLDER}/covers'
    DEFAULT_IMAGE = f'{IMAGES_FOLDER}/default/gray.png'
    PROMO_IMAGES = f'{IMAGES_FOLDER}/promo'
    CATEGORIES_IMAGES = f'{IMAGES_FOLDER}/categories'
    LOGO_IMAGES = f'{IMAGES_FOLDER}/images/logo'
    LOGO_IMAGE_URL = "https://orientpalace-dz.com/images/logo/logo.jpeg"
    IMAGE_FORMAT = "jpeg"
    #FLASKFB.GDB'
    MAIL_SERVER = 'smtp.titan.email'
    MAIL_PORT = 465
    MAIL_USERNAME = 'showroom@orientpalace-dz.com'
    MAIL_PASSWORD = "Orientpalace2021"
    MAIL_RESEVER = 'zakilebbah@gmail.com'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    # CORS_HEADERS = 'Content-Type'
    YALIDINE_ID="24613501725898650391"
    YALIDINE_TOKEN="yCOgdF3Q84E5aLhsJ27OzHlgDKc8VXsktMAq0dPiYN1SKr46vbZfjI39SmwQAiUa"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = 1

    ENV = 'development'
    DEBUG = True
    TESTING = True

    # D:\OranSoft\gitoransoft\oranweb\flask2nf2\app\articles-images
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp'}

    SECRET_KEY = 'akliyi thagui, nchaallah, mayavgha rebbi'

    ENV = 'development'
    DEBUG = True
    TESTING = True
    MAX_CONTENT_LENGTH = 16*1024 * 1024
