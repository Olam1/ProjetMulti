# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 13:53:58 2020

@author: malot
"""

from __future__ import division
from PyQt5 import QtWidgets
#from PIL import Image
import os
import numpy as np
#import glob
#import pylab
import tomopy

from os import mkdir
from os.path import join, isdir
from imageio import imread, imwrite

from PIL import Image

import astra


def MatrixGeneration(self, filePath, factor): 
    # On crée des variables qui correspondent aux dimensions de la radio X
    # Le paramètre "factor" permet de s'ajuster avec le redimensionnement 
    # opéré sur le projections dans la fonction "downscaleIMG"
    distance_source_origin = 300  # [mm]
    distance_origin_detector = 100  # [mm]
    detector_pixel_size = 0.08117512  # [mm]
    detector_rows = int(1000 * factor)  # Hauteur du détecteur [pixels]
    detector_cols = int(1000 * factor)   # Largeur du détecteur [pixels]
    num_of_projections = 360
    #angles = tomopy.angles(num_of_projections,0.471,357.829)
    angles = np.linspace(0, 2 * np.pi, num=num_of_projections, endpoint=False)
    output_dir = 'recon'
    
    # On ouvre tous les ficheirs de projections et on les stocke dans la matrice "projections"
    projections = np.zeros((detector_rows, num_of_projections, detector_cols))      
    for i in range(num_of_projections):
        im = imread(join(filePath, 'proj%04d.tif' % i)).astype(float)
        im /= 65535
        #print(im.shape)
        im = downscaleIMG(im, factor)
        #print(im.shape)
        projections[:, i, :] = im
        self.progressBar.setValue(int((i/num_of_projections)*100)) # Bar de chargement des images
    print('Hello')
    
    # On donne ici la géométrie du détecteur
    # Plusieurs géométries sont possibles (http://www.astra-toolbox.com/docs/geom3d.html)
    # selon la réalité de la radio X
    proj_geom = astra.create_proj_geom('cone', 1, 1, detector_rows, detector_cols, angles,
                         (distance_source_origin + distance_origin_detector) /
                         detector_pixel_size, 0)
    print('0')
    
    #On crée les sinogrammes associés aux slices 
    projections_id = astra.data3d.create('-sino', proj_geom, projections)
    print('1')
    
    # On crée le volume dans lequel sera compris notre objet
    # Plusieurs géométries sont possibles (http://www.astra-toolbox.com/docs/data3d.html#)
    vol_geom = astra.creators.create_vol_geom(detector_cols, detector_cols,
                                              detector_rows)
    reconstruction_id = astra.data3d.create('-vol', vol_geom, data=0)
    print('2')
    
    # On définit l'algorithme de reconstruction (http://www.astra-toolbox.com/docs/algs)
    # Les images sont stockées dans la variable "reconstruction"
    alg_cfg = astra.astra_dict('FDK_CUDA') 
    print('3')
    #alg_cfg['ProjectorId'] = projector_id #Seulement pour les géométries 2D
    alg_cfg['ProjectionDataId'] = projections_id
    alg_cfg['ReconstructionDataId'] = reconstruction_id
    algorithm_id = astra.algorithm.create(alg_cfg)
    astra.algorithm.run(algorithm_id)
    reconstruction = astra.data3d.get(reconstruction_id)
    print('4')
    # On normalise les valeurs obtenues
    reconstruction[reconstruction < 0] = 0
    reconstruction /= np.max(reconstruction)
    reconstruction = np.round(reconstruction * 255).astype(np.uint8)
     
    # On enregistre les images dans le dossier "recon" créé dans le répertoire de travail
    if not isdir(output_dir):
        mkdir(output_dir)
    for i in range(detector_rows):
        im = reconstruction[i, :, :]
        im = np.flipud(im)
        imwrite(join(output_dir, 'reco%04d.png' % i), im)
    print('5')
    # Message de validation
    msg = QtWidgets.QMessageBox()
    msg.setIcon(1)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.setWindowTitle("Information")
    msg.setText("La reconstruction a bien été effectué")
    msg.exec()
    
    # Cleanup.
    astra.algorithm.delete(algorithm_id)
    astra.data3d.delete(reconstruction_id)
    astra.data3d.delete(projections_id)
    
    return 0

#Reçoit un dossier contenant les TIF et renvoie une matrice
def choix_fichier(self):
    factor = float(str(self.selectFactor.currentText()))
    # L'utilisateur choisi le dossier dans lequel se trouve les fichiers
    path = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Open a folder",
            os.sep.join((os.path.expanduser('~'), 'Desktop')), #Permet d'afficher le bureau à l'ouverture de la fenêtre
            options = QtWidgets.QFileDialog.ShowDirsOnly
            )
    #Gestion de l'exception dans le cas où l'utilisateur choisit un mauvais dossier
    #Dans ce cas on envoie des projections générées virtuellement par tomopy
    #Si aucun dossier n'est sélectionné path = 0 et il ne se passe rien
    if path:
        try:
            MatrixGeneration(self, path, factor)
        except IndexError:
            return tomopy.project(tomopy.shepp3d(), tomopy.angles(180))
    
# Cette fonction permet de redimensionner les images pour réduire les temps de calcul
# Le résultat final sera aussi moins bon
def downscaleIMG (im, factor):
    im = Image.fromarray(im)
    width, height = im.size
    new_width = int(factor * width)
    new_height = int(factor * height)
    new_im = np.array(im.resize((new_width, new_height), Image.ANTIALIAS))
    return new_im




