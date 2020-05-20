# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 13:53:58 2020

@author: malot
"""

import sys
from PyQt5 import uic, QtWidgets
import os

#On force le path du fichier ui dans le répertoire courant
cwd = os.getcwd()
print(cwd)
full_path = os.path.realpath(__file__)
dirpath = os.path.dirname(full_path)
print(dirpath)
try:
    Ui_MainWindow, QtBaseClass = uic.loadUiType(cwd + r"\user_interface_test.ui")
except FileNotFoundError:
    Ui_MainWindow, QtBaseClass = uic.loadUiType(dirpath + r"\user_interface_test.ui")


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

