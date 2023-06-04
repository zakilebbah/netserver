import os
from PIL import Image
import subprocess
import pathlib
from app import app
import os.path
from os import path
import shutil
from PIL import ImageFile
def transform_images_articles(urlFolder, refArt): 
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    covers = os.path.join(app.config['PRODUCTS_COVERS']) 
    articles = os.path.join(app.config['PRODUCTS_IMAGES']) 
    count = 0
    for file in os.listdir(urlFolder):
        count =+ 1
        filename = os.fsdecode(file)
        # if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".PNG") or filename.endswith(".jpeg") or filename.endswith(".JPEG") or filename.endswith(".webp") or filename.endswith(".JPG"):
        filename, imageType = filename.split(".")
        pathPng = f'{os.fsdecode(urlFolder)}/{filename}.{imageType}'
        pathWebp = os.path.join(urlFolder, str(filename + '.' +app.config["IMAGE_FORMAT"]))
        pathCover = os.path.join(covers, str(refArt + '.' +app.config["IMAGE_FORMAT"]))
        # f'{os.fsdecode(covers)}/{refArt}.{imageType}'
        path2 = pathlib.Path(pathPng)
        if path2.exists():
            im = Image.open(pathPng)
            width, height = im.size
            if ((width >= 1000 or height >= 1000)):
                os.remove(pathPng)
                im.thumbnail((1000, 1000), Image.ANTIALIAS)
                im0 = im.convert('RGB')
                im0.save(pathWebp, app.config["IMAGE_FORMAT"], optimize=True,quality=65)
                # subprocess.call(f'convert -resize 1000X1000 {pathPng} {pathWebp}.webp', shell=True)
                im0.close()
                # subprocess.call(f'rm -rf {pathPng}', shell=True)
            else:
                os.remove(pathPng)
                im0 = im.convert('RGB')
                im0.save(pathWebp, app.config["IMAGE_FORMAT"], optimize=True,quality=65)
                im0.close()
            im.close()
    # return True

def transform_images_cover_articles(refArt, path0): 
    pathCover = os.path.join(os.path.join(app.config['PRODUCTS_COVERS']), str(refArt + '.' +app.config["IMAGE_FORMAT"]))
    pathToDelete = pathlib.Path(pathCover)
    if pathToDelete.exists():
        os.remove(pathCover)
    imCover = Image.open(path0)
    imCover.thumbnail((200, 200), Image.ANTIALIAS)
    im0 = imCover.convert('RGB')
    im0.save(pathCover, app.config["IMAGE_FORMAT"], optimize=True,quality=65)
    imCover.close()
    im0.close()
    os.remove(path0)



def transform_images_promo(fileName): 
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    promoPath = os.path.join(app.config['PROMO_IMAGES']) 
    pathPng = os.path.join(promoPath, fileName)
    # if fileName.endswith(".jpg") or fileName.endswith(".png") or fileName.endswith(".PNG") or fileName.endswith(".jpeg") or fileName.endswith(".JPEG") or fileName.endswith(".webp") or fileName.endswith(".JPG"):
    name, imageType = fileName.split(".")
    pathPng = f'{os.fsdecode(promoPath)}/{name}.{imageType}'
    path0 = f'{os.fsdecode(promoPath)}/{name}.{app.config["IMAGE_FORMAT"]}'
    # pathWebp = pathlib.Path(f'{os.fsdecode(promoPath)}/{name}.webp')
    # if pathWebp.exists():
    #     os.remove(pathWebp)
    if pathlib.Path(pathPng).exists():
        im = Image.open(pathPng)
        os.remove(pathPng)
        width, height = im.size
        if width >= 1000 or height >= 1000:
            im.thumbnail((1000, 1000))
            im = im.convert('RGB')
            im.save(path0, optimize=True,quality=70)
        else:
            im = im.convert('RGB')
            im.save(path0, optimize=True,quality=70)
        im.close()
def transform_images_categories(fileName, code_famille): 
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    catPath = os.path.join(app.config['CATEGORIES_IMAGES']) 
    pathPng = os.path.join(catPath, fileName)
    # if fileName.endswith(".jpg") or fileName.endswith(".png") or fileName.endswith(".PNG") or fileName.endswith(".jpeg") or fileName.endswith(".JPEG") or fileName.endswith(".webp") or fileName.endswith(".JPG"):
    name, imageType = fileName.split(".")
    pathPng = f'{os.fsdecode(catPath)}/{name}.{imageType}'
    path0 = f'{os.fsdecode(catPath)}/{code_famille}'
    if pathlib.Path(pathPng).exists():
        im = Image.open(pathPng)
        os.remove(pathPng)
        width, height = im.size
        if width >= 200 or height >= 200:
            im.thumbnail((200, 200))
            im = im.convert('RGB')
            im.save(path0, optimize=True,quality=50)
        else:
            im = im.convert('RGB')
            im.save(path0, optimize=True,quality=50)
        im.close()

# def getPromoFiles():
#     promoPath = os.path.join(app.config['PROMO_IMAGES']) 
#     images = []
#     for filename in os.listdir(promoPath):
#         images.