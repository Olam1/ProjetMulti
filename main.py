# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 15:55:37 2019

@author: malot
"""

import sys
from PyQt5 import QtCore, uic, QtWidgets,QtGui
import visualisation_ok as visu


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
        self.select_file.clicked.connect(self.FonctionsQt.choix_fichier)
        self.launch.clicked.connect(self.FonctionsQt.afficher)
        self.add_point.clicked.connect(self.FonctionsQt.ajouter_point)
        

  

 
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
    
