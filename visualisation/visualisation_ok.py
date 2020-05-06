# -*- coding: utf-8 -*-
import pylab
import glob
import vtk
import numpy as np
import matplotlib.pyplot as plt


#Ouvre toutes les ficheirs d'un dossier et genère un volume constitué de l'empilement de toutes les slices 2D
def MatrixGeneration(filePath):   
    filenames = [img for img in glob.glob(filePath)]
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
    return result
        

#Fonction qui ouvre une fenêtre affichant un rendu 3D de l'objet 
def visualisation (matrix_full = np.array([[[0,0],[0,0]],[[0,0],[0,0]]]),
                   point_0 = {"value":0, "opacity":0.},
                   point_1 = {"value":0, "opacity":0.},
                   point_2 = {"value":0, "opacity":0.},
                   point_3 = {"value":0, "opacity":0.},
                   point_5 = {"value":65536, "opacity":1.},
                   nb_points = 0):
    #Création d'un objet VtkImage qui pourra être traité par la suite
    dataImporter = vtk.vtkImageImport()
    # La matrice est convertie en un string
    data_string = matrix_full.tostring()
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))
    # Changement du type de donnée
    dataImporter.SetDataScalarTypeToUnsignedShort()
    #On précise que ce sont des données en niveau de gris et pas couleurs
    dataImporter.SetNumberOfScalarComponents(1)
    
    # On explicite la manière dont les données sont stockées et les dimensions de la matrice
    w, d, h = matrix_full.shape
    dataImporter.SetDataExtent(0, h-1, 0, d-1, 0, w-1)
    dataImporter.SetWholeExtent(0, h-1, 0, d-1, 0, w-1) 
    # Création d'un object qui spécifie les paramètre de couleur
    colorFunc = vtk.vtkPiecewiseFunction()
    #On ajoute les deux points par défaut d'intensité aux deux extremes de niveaux de gris
    colorFunc.AddPoint(point_0.get("value"), point_0.get("opacity"));
    colorFunc.AddPoint(point_5.get("value"), point_5.get("opacity"));
    
    #Creation d'un objet qui gère l'opacité
    alphaChannelFunc = vtk.vtkPiecewiseFunction()
    
    #On défini les différents niveaux d'opacité selon les points entrés par l'utilisateur
    alphaChannelFunc.AddPoint(point_0.get("value"), point_0.get("opacity"));
    if nb_points == 0:
        pass
    elif nb_points == 1:
        alphaChannelFunc.AddPoint(point_1.get("value"), point_1.get("opacity"));
    elif nb_points == 2:
        alphaChannelFunc.AddPoint(point_1.get("value"), point_1.get("opacity"));
        alphaChannelFunc.AddPoint(point_2.get("value"), point_2.get("opacity"));
    else:
        alphaChannelFunc.AddPoint(point_1.get("value"), point_1.get("opacity"));
        alphaChannelFunc.AddPoint(point_2.get("value"), point_2.get("opacity"));
        alphaChannelFunc.AddPoint(point_3.get("value"), point_3.get("opacity"));
    alphaChannelFunc.AddPoint(point_5.get("value"), point_5.get("opacity"));
    
    #Creation d'un objet qui prend en charge les propriétés du volume, on lui passe les propriétes définies précedemment
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(colorFunc)
    volumeProperty.SetScalarOpacity(alphaChannelFunc)
    
    # Creation de l'objet volume
    volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
    #On fixe la distance entre deux images du volume
    volumeMapper.SetMaximumImageSampleDistance(0.01) 
    #On passe les données au volume crée
    volumeMapper.SetInputConnection(dataImporter.GetOutputPort())
    
    # Cration d'un autre objet volume qui combine le volume crée avant avec les propriétés de l'obet volumeProperty
    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)
    return volume


#Crée un graph matplotlib et le retourne à partir des points
def creer_graph(point_0 = {"value":0, "opacity":0.},
                point_1 = {"value":0, "opacity":0.},
                point_2 = {"value":0, "opacity":0.},
                point_3 = {"value":0, "opacity":0.},
                point_5 = {"value":65536, "opacity":1.},
                nb_points = 0):
    if nb_points == 0:
        X = [point_0.get("value"), point_5.get("value")]
        Y = [point_0.get("opacity"), point_5.get("opacity")]
    elif nb_points == 1:
        X = [point_0.get("value"), point_1.get("value"), point_5.get("value")]
        Y = [point_0.get("opacity"), point_1.get("opacity"), point_5.get("opacity")]
    elif nb_points == 2:
        X = [point_0.get("value"), point_1.get("value"), point_2.get("value"), point_5.get("value")]
        Y = [point_0.get("opacity"), point_1.get("opacity"), point_2.get("opacity"), point_5.get("opacity")]
    else:
        X = [point_0.get("value"), point_1.get("value"), point_2.get("value"), point_3.get("value"), point_5.get("value")]
        Y = [point_0.get("opacity"), point_1.get("opacity"), point_2.get("opacity"), point_3.get("opacity"), point_5.get("opacity")]
    #On efface les figure précédente pour ne pas saturer la mémoire
    plt.cla()
    plt.clf()
    plt.close()
    #On crée un objet fig qui contient notre graph et on le retourne
    fig, ax1 = plt.subplots()
    ax1.plot(X,Y,'bo-')
    ax1.set_xlim(-1000, 70000)
    ax1.set_ylim(-0.1, 1.1)
    return fig
    
    
    

