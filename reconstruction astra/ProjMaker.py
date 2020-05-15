# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 17:29:32 2020

@author: malot
"""

from __future__ import division
 
import numpy as np
from os import mkdir
from os.path import join, isdir
from imageio import get_writer
 
# Il est nécéssaire d'avoir une carte graphique NVidia supportant CUDA 
# pour faire tourner ce programme.
import astra
 
# On crée des variables qui correspondent aux dimensions souhaitées
distance_source_origin = 300  # [mm]
distance_origin_detector = 100  # [mm]
detector_pixel_size = 0.08117512  # [mm]
detector_rows = 1000  # Hauteur du détecteur [pixels]
detector_cols = 1000  # Largeur du détecteur [pixels]
num_of_projections = 360
angles = np.linspace(0, 2 * np.pi, num=num_of_projections, endpoint=False)
output_dir = 'dataset'
 
# On crée un objet virtuel appelé "phantom"
# Cet objet est un pavé avec un trou carré sur l'une des faces latéral
vol_geom = astra.creators.create_vol_geom(detector_cols, detector_cols,
                                          detector_rows)
phantom = np.zeros((detector_rows, detector_cols, detector_cols))
hb = 110  # Height of beam [pixels].
wb = 40   # Width of beam [pixels].
hc = 100  # Height of cavity in beam [pixels].
wc = 30   # Width of cavity in beam [pixels].
phantom[detector_rows // 2 - hb // 2 : detector_rows // 2 + hb // 2,
        detector_cols // 2 - wb // 2 : detector_cols // 2 + wb // 2,
        detector_cols // 2 - wb // 2 : detector_cols // 2 + wb // 2] = 1
phantom[detector_rows // 2 - hc // 2 : detector_rows // 2 + hc // 2,
        detector_cols // 2 - wc // 2 : detector_cols // 2 + wc // 2,
        detector_cols // 2 - wc // 2 : detector_cols // 2 + wc // 2] = 0
phantom[detector_rows // 2 - 5 :       detector_rows // 2 + 5,
        detector_cols // 2 + wc // 2 : detector_cols // 2 + wb // 2,
        detector_cols // 2 - 5 :       detector_cols // 2 + 5] = 0
phantom_id = astra.data3d.create('-vol', vol_geom, data=phantom)
 
# On crée des projections avec des angles croissants 
# Les projections sont telles que l'objet est tourné dans le sens des aiguilles d'une montre 
# La tranche zéro se trouve en haut de l'objet. 
proj_geom = astra.create_proj_geom('cone', 1, 1, detector_rows, detector_cols, angles,
                         (distance_source_origin + distance_origin_detector) / detector_pixel_size, 0)

projections_id, projections = astra.creators.create_sino3d_gpu(phantom_id, proj_geom, vol_geom)
projections /= np.max(projections)
 
# On applique un bruit de Poisson
projections = np.random.poisson(projections * 10000) / 10000
projections[projections > 1.1] = 1.1
projections /= 1.1
 
# On enregistre les projections dans un dossier "dataset" créé dans le répertoire de travail
if not isdir(output_dir):
    mkdir(output_dir)
projections = np.round(projections * 65535).astype(np.uint16)
for i in range(num_of_projections):
    projection = projections[:, i, :]
    with get_writer(join(output_dir, 'proj%04d.tif' %i)) as writer:
        writer.append_data(projection, {'compress': 9})
 
# Nettoyage
astra.data3d.delete(projections_id)
astra.data3d.delete(phantom_id)



