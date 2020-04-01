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

#Ouvre toutes les ficheirs d'un dossier et genère un volume constitué de l'empilement de toutes les slices 2D
def MatrixGeneration(self, filePath, factor):   
    distance_source_origin = 300  # [mm]
    distance_origin_detector = 100  # [mm]
    detector_pixel_size = 0.08117512  # [mm]
    detector_rows = int(1000 * factor)  # Vertical size of detector [pixels].
    detector_cols = int(1000 * factor)   # Horizontal size of detector [pixels].
    num_of_projections = 360
    #angles = tomopy.angles(num_of_projections,0.471,357.829)
    angles = np.linspace(0, 2 * np.pi, num=num_of_projections, endpoint=False)
    output_dir = 'recon'
    
    # Load projections.
    projections = np.zeros((detector_rows, num_of_projections, detector_cols))     
        
    for i in range(1, num_of_projections+1):
        im = imread(join(filePath, 'laser_hugo-malo_%04d.tif' % i)).astype(float)
        im /= 65535
        #print(im.shape)
        im = downscaleIMG(im, factor)
        #print(im.shape)
        projections[:, i-1, :] = im
        self.progressBar.setValue(int((i/num_of_projections)*100))
        #print('laser_hugo-malo_%04d.tif' % i)
    print('Hello')
    
    # Copy projection images into ASTRA Toolbox.
    proj_geom = astra.create_proj_geom('cone', 1, 1, detector_rows, detector_cols, angles,
                         (distance_source_origin + distance_origin_detector) /
                         detector_pixel_size, 0)
    print('0')
    projections_id = astra.data3d.create('-sino', proj_geom, projections)
    print('1')
    
    # Create reconstruction.
    vol_geom = astra.creators.create_vol_geom(detector_cols, detector_cols,
                                              detector_rows)
    print('2')
    reconstruction_id = astra.data3d.create('-vol', vol_geom, data=0)
    print('3')
    alg_cfg = astra.astra_dict('FDK_CUDA') #On définit l'algorithme http://www.astra-toolbox.com/docs/algs
    print('4')
    #alg_cfg['ProjectorId'] = projector_id #Seulement pour les géométries 2D
    alg_cfg['ProjectionDataId'] = projections_id
    alg_cfg['ReconstructionDataId'] = reconstruction_id
    algorithm_id = astra.algorithm.create(alg_cfg)
    astra.algorithm.run(algorithm_id)
    reconstruction = astra.data3d.get(reconstruction_id)
     
    # Limit and scale reconstruction.
    reconstruction[reconstruction < 0] = 0
    reconstruction /= np.max(reconstruction)
    reconstruction = np.round(reconstruction * 255).astype(np.uint8)
     
    # Save reconstruction.
    if not isdir(output_dir):
        mkdir(output_dir)
    for i in range(detector_rows):
        im = reconstruction[i, :, :]
        im = np.flipud(im)
        imwrite(join(output_dir, 'reco%04d.png' % i), im)
    
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
    #Si aucun dossier n'est sélectionné path = 0 et il ne se passe rien
    if path:
        try:
            MatrixGeneration(self, path, factor)
        except IndexError:
            return tomopy.project(tomopy.shepp3d(), tomopy.angles(180))
    

def downscaleIMG (im, factor):
    im = Image.fromarray(im)
    width, height = im.size
    new_width = int(factor * width)
    new_height = int(factor * height)
    new_im = np.array(im.resize((new_width, new_height), Image.ANTIALIAS))
    return new_im




