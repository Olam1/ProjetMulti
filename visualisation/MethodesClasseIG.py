# -*- coding: utf-8 -*-
import os
from PyQt5 import QtWidgets, QtGui
import visualisation_ok as visu
#import WindowStandby
import LirePoints
import WindowStandby as WS
import time
from matplotlib.backends.backend_qt5agg import FigureCanvas 
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


#Fichier contenant les méthodes de la classe InterfaceGraphique 
OFFSET = 1000


#Rend les boutons des points 1,2 et 3 cliquables
def ajouter_points(self):
    self.nb_points+=1
    if self.nb_points == 1:
        self.point1Slider.setEnabled(True)
        self.point1spinBox.setEnabled(True)
        self.point1spinBox.setMinimum(self.point0spinBox.value())
        self.point1spinBox.setValue(self.point0spinBox.value() + OFFSET)
        self.point0spinBox.setMaximum(self.point1spinBox.value())
    elif self.nb_points == 2:
        self.point2Slider.setEnabled(True)
        self.point2spinBox.setEnabled(True)
        self.point2spinBox.setMinimum(self.point1spinBox.value())
        self.point2spinBox.setValue(self.point1spinBox.value() + OFFSET)
        self.point1spinBox.setMaximum(self.point2spinBox.value())
    else:
        self.point3Slider.setEnabled(True)
        self.point3spinBox.setEnabled(True)
        self.point3spinBox.setMinimum(self.point2spinBox.value())
        self.point3spinBox.setValue(self.point2spinBox.value() + OFFSET)
        self.point2spinBox.setMaximum(self.point3spinBox.value())
    return self.nb_points


#Rend les boutons des points 1,2 et 3 non cliquables  
def retirer_points(self):
    if self.nb_points == 1:
        self.point1Slider.setEnabled(False)
        self.point1spinBox.setEnabled(False)
    elif self.nb_points == 2:
        self.point2Slider.setEnabled(False)
        self.point2spinBox.setEnabled(False)
    else:
        self.nb_points = 3
        self.point3Slider.setEnabled(False)
        self.point3spinBox.setEnabled(False)
    self.nb_points-=1
    return self.nb_points
 
    
#Reçoit un dossier contenant les TIF et renvoie une matrice
def choix_fichier(self):
    gestion_message(self, 100)
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
        Loader = QtGui.QMovie("loader.gif")
        WS.PauseWindow(self, Loader)
        time.sleep(0.2)
        try:
            self.matrix, w, d, h = visu.MatrixGeneration(path+'/*.tif')
        except IndexError:
            gestion_message(self, 111)
            return 1
        except ValueError:
            gestion_message(self, 113)
            return 1
        gestion_message(self, 115, str(w),str(d),str(h))
        WS.RestartWindow(self, Loader)
        return self.matrix


#Ouvre la fenêtre conteant la visualisation en 3D de l'objet
def afficher(self):
    #On efface tous les widgets présents dans le layout 'object_layout'
    for i in reversed(range(self.object_layout.count())): 
        self.object_layout.itemAt(i).widget().deleteLater()
    
    #On crée le widget qui contient la fenetre interactive et on l'ajoute au layout    
    self.vtkWidget = QVTKRenderWindowInteractor(self.object_plot)
    self.object_layout.addWidget(self.vtkWidget)

    self.renderer = vtk.vtkRenderer()
    self.renderer.GlobalWarningDisplayOff() #On cache la fenêtre d'erreur Vtk
    self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
    self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
    
    #On récupère les données des points du graph
    p0, p5, p1, p2, p3 =LirePoints.Do(self)
    #On teste si l'utilisateur a choisi un stack de fichiers
    #Si ce n'est pas le cas on affiche un message d'erreur
    try:
        volume = visu.visualisation(self.matrix, p0, p1, p2, p3, p5, self.nb_points)
    except AttributeError:
        gestion_message(self, 112)
        return 1
    
    self.renderer.AddVolume(volume)
    self.renderer.ResetCamera()
    self.renderer.SetBackground(1,1,1)
    self.object_plot.setLayout(self.object_layout)
    
    self.show()
    self.iren.Initialize()
    self.iren.Start()
    return 0
  
    
#Afficher la graph contenant la courbe d'opacité des différents niveaux de gris
def afficher_graph(self):
    p0, p5, p1, p2, p3 = LirePoints.Do(self)
    
    #On efface tous les widgets présents dans le layout 'graph_layout'
    for i in reversed(range(self.graph_layout.count())): 
        self.graph_layout.itemAt(i).widget().deleteLater()
    #On lit les points à afficher et on cree le graph à partir de ces points
    #p0, p5, p1, p2, p3 = LirePoints.Do(self)
    fig = visu.creer_graph(p0, p1, p2, p3, p5,self.nb_points)
    #FigureCanvas permet de transformer le graph matplotliq en graph Qt
    self.plotWidget = FigureCanvas(fig)
    #On ajoute le widget contenant le graph dans le layout  
    self.graph_layout.addWidget(self.plotWidget)
    
    #ActualiserMinMax(self)
    return 0


#Permet d'afficher des massages d'erreur dans la barre de statut
def gestion_message(self, codeErreur = 100, w=0, d=0, h=0):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(2)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.setWindowTitle("Warning")
    self.statusbar.clearMessage()
    if codeErreur == 100:
        self.statusbar.clearMessage()
    elif codeErreur == 111:
        msg.setText("Please select another folder")
        msg.exec()
    elif codeErreur == 112:
        msg.setText("Please select files")
        msg.exec()
    elif codeErreur == 113:
        msg.setText("Image with an unexpected size")
        msg.exec()
    elif codeErreur == 114:
        self.statusbar.showMessage("Screenshot done", 5000)
    elif codeErreur == 115:
        self.statusbar.showMessage("width : "+w+" | depth : "+d+" | height : "+h)
    else:
        self.statusbar.showMessage("Unknown error")
    return 0


def capture(self):
    file = QtWidgets.QFileDialog.getSaveFileName(self,
                                                 'Save Image As', os.sep.join((os.path.expanduser('~'), 'Desktop')), #Permet d'afficher le bureau à l'ouverture de la fenêtre
                                                 "PNG (*.png);; BMP (*.bmp);;TIFF (*.tiff *.tif);; JPEG (*.jpg *.jpeg)")
    self.object_plot.grab().save(file[0]);
    gestion_message(self, 114)
    return 0
    
def ActualiserMinMax(self):
    p0, p5, p1, p2, p3 =LirePoints.Do(self)
    self.point1spinBox.setMinimum(p0["value"])
    self.point2spinBox.setMinimum(p1["value"])
    self.point3spinBox.setMinimum(p2["value"])
    self.point3spinBox.setMaximum(p5["value"])
    self.point2spinBox.setMaximum(p3["value"])   
    self.point1spinBox.setMaximum(p2["value"])       
    return 0    
    
    
    
