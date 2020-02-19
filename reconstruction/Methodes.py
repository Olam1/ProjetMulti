# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 12:37:16 2020

@author: malot
"""

import os
import tomopy
import pylab
import glob
import numpy as np
from PyQt5 import QtWidgets

#Ouvre toutes les ficheirs d'un dossier et genère un volume constitué de l'empilement de toutes les slices 2D
def MatrixGeneration(filePath):   
    filenames = [img for img in glob.glob(filePath)]
    print("\n\nHello\n\n")
    filenames.sort()

    temp = pylab.imread(filenames[0])
    d, w = temp.shape
    h = len(filenames)
    matrix = np.zeros((d, w, h), dtype=np.uint16)
    k=0
    for img in filenames: #On suppose que tous les fichiers sont des tif    
        im=pylab.imread(img)
        matrix[:,:,k] = im
        k+=1
    result = [matrix, w, d, h]
    rec = tomopy.recon(matrix, tomopy.angles(720,0.,360.), algorithm='art')
    pylab.imshow(rec[64], cmap='gray')
    pylab.show()
    return result

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
            self.matrix, w, d, h = MatrixGeneration(path+'/*.tif')
        except IndexError:
            return tomopy.project(tomopy.shepp3d(), tomopy.angles(180))
        return self.matrix

#def main():
#    obj = tomopy.shepp3d()
#    ang = tomopy.angles(180)
#    sim = tomopy.project(obj, ang)
#    rec = tomopy.recon(sim, ang, algorithm='art')
#    pylab.imshow(rec[64], cmap='gray')
#    pylab.show()