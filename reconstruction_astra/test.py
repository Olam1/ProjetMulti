# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 13:53:58 2020

@author: malot
"""

import sys
from PyQt5 import uic, QtWidgets
import os

cwd = os.getcwd()
print(cwd)
Ui_MainWindow, QtBaseClass = uic.loadUiType("user_interface_test.ui")


class InterfaceGraphique(QtWidgets.QMainWindow, Ui_MainWindow):
    from Methodes import choix_fichier
    def __init__(self):
        #Initialisation de la classe parent QMainWindow
        QtWidgets.QMainWindow.__init__(self)
        #Utilisation de la méthode setupUi hérité de la classe Ui_Mainwindow
        self.setupUi(self)
        #Appel à la fonction "choix_fichier"
        self.selectFile.clicked.connect(self.choix_fichier)
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = InterfaceGraphique()
    window.show()
    sys.exit(app.exec_())

