from PyQt5 import QtWidgets
from PIL import Image
import os
import numpy as np
import glob
import pylab
import tomopy

#Ouvre toutes les ficheirs d'un dossier et genère un volume constitué de l'empilement de toutes les slices 2D
def MatrixGeneration(filePath):   
    filenames = [img for img in glob.glob(filePath)]
    print("\n\nHello\n\n")
    filenames.sort()

    temp = pylab.imread(filenames[0])
    w,d = temp.shape
    h = len(filenames)
    matrix = np.zeros((w,d,h), dtype=np.uint16)
    k=0
    for img in filenames: #On suppose que tous les fichiers sont des tif    
        im=pylab.imread(img)
        matrix[:,:,k] = im
        k+=1 
    print("Je suis là")
    #matrix=np.rot90(matrix, axes=(0,1))     
    #result = [matrix, w, d, h]
    matrix = tomopy.minus_log(matrix)
    rec = tomopy.recon(matrix, tomopy.angles(103,0.,360.), algorithm='fbp')    
    compteur=0
    print(rec.shape)
    for i in range(len(rec)):
        #img = Image.fromarray(rec[i], mode='F')
        #img = img.convert("L")
        #img.save(str(i) + ".png", "PNG")
        compteur=compteur+1
    print(compteur)    
    pylab.imshow(rec[1], cmap='gray')
    pylab.show()
    print("\n\nJe suis ici\n\n")
    pylab.imshow(rec[250], cmap='gray')
    pylab.show()
    return 0

#Reçoit un dossier contenant les TIF et renvoie une matrice
def choix_fichier(self):
    # L'utilisateur choisi le dossier dans lequel se trouve les fichiers
    path = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Open a folder",
            os.sep.join((os.path.expanduser('~'), 'Desktop')), #Permet d'afficher le bureau à l'ouverture de la fenêtre
            options = QtWidgets.QFileDialog.ShowDirsOnly
            )
    #Gestion de l'exception dans le cas où l'utilisateur choisit un mauvais dossier
    #Si aucun dossier n'est sélectionné path = 0 et il ne se passe rien
    if path:
        try:
            MatrixGeneration(path+'/*.tif')
        except IndexError:
            return tomopy.project(tomopy.shepp3d(), tomopy.angles(180))
    

#def main():
#    obj = tomopy.shepp3d()  self.matrix, w, d, h = 
#    ang = tomopy.angles(180)
#    sim = tomopy.project(obj, ang)
#    rec = tomopy.recon(sim, ang, algorithm='art')
#    pylab.imshow(rec[64], cmap='gray')
#    pylab.show()
