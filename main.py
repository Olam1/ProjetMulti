# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 15:55:37 2019

@author: malot
"""

import sys
from PyQt5 import QtCore, uic, QtWidgets,QtGui
import visualisation_ok as visu
import WindowStandby
import LirePoints

import matplotlib
matplotlib.use('QT5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


qtCreatorFile = "user_interface.ui" # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    # On initialise une variable globale qui contiendra notre 
    # future matrice d'images
    matrix = 0
    nb_points = 0
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.select_file.clicked.connect(self.choix_fichier)
        self.launch.clicked.connect(self.afficher)
        self.add_point.clicked.connect(self.ajouter_point)
        self.update_graph.clicked.connect(self.voir_graph)
    
    
    def ajouter_point(self):
        MyApp.nb_points+=1
        if MyApp.nb_points == 1:
            self.point1Slider.setEnabled(True)
            self.point1spinBox.setEnabled(True)
        elif MyApp.nb_points == 2:
            self.point2Slider.setEnabled(True)
            self.point2spinBox.setEnabled(True)
        else:
            self.point3Slider.setEnabled(True)
            self.point3spinBox.setEnabled(True)
        print(MyApp.nb_points)
        return MyApp.nb_points
 
    
    #Reçoit un dossier contenant les TIF et renvoie une 
    def choix_fichier(self):
        print('choix_fichier')
        # L'utilisateur choisi le dossier dans lequel se trouve les fichiers
        path = QtWidgets.QFileDialog.getExistingDirectory(
                self,
                "Open a folder",
                options = QtWidgets.QFileDialog.ShowDirsOnly
                )
        self.warning_text_select_file.clear()
        if path:
            try:
                MyApp.matrix = visu.file_choice(path)
            except IndexError:
                self.warning_text_select_file.setText("/!\ Please select another folder")
                return 1
            return MyApp.matrix
    
    
    def afficher(self):
        self.warning_text_launch.clear()
        wp, bp, p1, p2, p3 =LirePoints.Do(self,MyApp)
        visu.greyscale_graph(wp, bp, p1, p2, p3, MyApp.nb_points)
        #On charge le gif contenant l'icône de chargement
        Loader = QtGui.QMovie("loader.gif")
        #On met la fenêtre principale en pause
        WindowStandby.PauseWindow(self, Loader)
        # On teste si l'utilisateur a choisi un stack de fichiers
        #Si ce n'est pas le cas on affiche un message d'erreur
        try:
            visu.visualisation(wp, bp, MyApp.matrix, p1, p2, p3, MyApp.nb_points)
        except AttributeError:
            self.warning_text_launch.setText("/!\ Please select files")
            WindowStandby.RestartWindow(self, Loader)
            return 1
        #On réactive la fenêtre principale
        WindowStandby.RestartWindow(self, Loader)
        return 0
      
        
    
    def voir_graph(self):
        wp, bp, p1, p2, p3 =LirePoints.Do(self,MyApp)
        fig = visu.greyscale_graph(wp, bp, p1, p2, p3, MyApp.nb_points)
        self.plotWidget = FigureCanvas(fig)
        lay = QtWidgets.QVBoxLayout(self.content_plot)  
        lay.setContentsMargins(0, 0, 0, 0)      
        lay.addWidget(self.plotWidget)
        return 0


  

 
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
    
