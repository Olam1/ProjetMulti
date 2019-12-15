import os
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
    print ('width, depth, height : ',w,d,h)

    matrix = np.zeros((d, w, h), dtype=np.uint16)
    k=0
    for img in filenames: #On suppose que tous les fichiers sont des tif    
        im=pylab.imread(img)
        
        if im.shape != (d, w): #1d2w
            print('Image with an unexpected size')
            return 1
        
        matrix[:,:,k] = im
        k+=1
    return matrix
        
    

#Fonction qui ouvre une fenêtre affichant un rendu 3D de l'objet 

def visualisation (white_point = 30000,
                   black_point = 65536,
                   matrix_full = np.array([[[0,0],[0,0]],[[0,0],[0,0]]]),
                   point_1 = {"value":0, "opacity":0.},
                   point_2 = {"value":0, "opacity":0.},
                   point_3 = {"value":0, "opacity":0.},
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
    colorFunc.AddPoint(0, 0.0);
    colorFunc.AddPoint(65536, 1);
    
    #Creation d'un objet qui gère l'opacité
    alphaChannelFunc = vtk.vtkPiecewiseFunction()
    
    #On défini les différents niveaux d'opacité selon les points entrés par l'utilisateur
    alphaChannelFunc.AddPoint(white_point, 0.0);
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
    alphaChannelFunc.AddPoint(black_point, 1);
    
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
    
    # Creation de la fenetre de rendu
    renderer = vtk.vtkRenderer()
    renderWin = vtk.vtkRenderWindow()
    renderWin.AddRenderer(renderer)
    renderInteractor = vtk.vtkRenderWindowInteractor()
    renderInteractor.SetRenderWindow(renderWin)
    
    # On ajoute le volume au rendu
    renderer.AddVolume(volume)
    # On choisi la couleur de l'arrière plan, ici blanc
    renderer.SetBackground(1,1,1)
    #On choisi la taille de la fenetre 
    renderWin.SetSize(520, 603)
    renderWin.SetMultiSamples(4)
    
    # Fonction à appeller lorsque l'on souhaite quitter l'application
    def exitCheck(obj, event):
        if obj.GetEventPending() != 0:
            obj.SetAbortRender(1)
    
    # On utilise la fonction précédent quand la fenetre est fermée
    renderWin.AddObserver("AbortCheckEvent", exitCheck)
    
    renderInteractor.Initialize()
    # On initialise le rendu avant de lancer la fenetre
    renderInteractor.Start()
    return 0


def creer_graph(white_point = 30000,
                black_point = 65536,
                point_1 = {"value":0, "opacity":0.},
                point_2 = {"value":0, "opacity":0.},
                point_3 = {"value":0, "opacity":0.},
                nb_points = 0):
    if nb_points == 0:
        X = [white_point, black_point]
        Y = [0., 1.]
    elif nb_points == 1:
        X = [white_point, point_1.get("value"), black_point]
        Y = [0., point_1.get("opacity"), 1.]
    elif nb_points == 2:
        X = [white_point, point_1.get("value"), point_2.get("value"), black_point]
        Y = [0., point_1.get("opacity"), point_2.get("opacity"), 1.]
    else:
        X = [white_point, point_1.get("value"), point_2.get("value"), point_3.get("value"), black_point]
        Y = [0., point_1.get("opacity"), point_2.get("opacity"), point_3.get("opacity"), 1.]   
    fig, ax1 = plt.subplots()
    ax1.plot(X,Y,'bo-')
    ax1.set_xlim(-1000, 70000)
    return fig
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#visualisation()
