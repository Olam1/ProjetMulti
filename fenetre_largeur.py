# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 15:55:37 2019

@author: malot
"""

import sys
from PyQt5 import QtCore, uic, QtWidgets
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
        self.select_file.clicked.connect(self.choix_fichier)
        self.launch.clicked.connect(self.afficher)
        self.add_point.clicked.connect(self.ajouter_point)
    
    def ajouter_point(self):
        MyApp.nb_points+= 1
        self.point1Slider.setEnabled(True)
        self.point1spinBox.setEnabled(True)
        print(MyApp.nb_points)
        return MyApp.nb_points
    
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
        width=self.spinBox_width.value()
        height=self.spinBox_height.value()
        wp=self.spinBox_white_point.value()
        bp=self.spinBox_black_point.value()
        if MyApp.nb_points == 1:
            p1 = {}
            p1["value"]=self.point1spinBox.value()
            p1["opacity"]=self.point1Slider.value()
            try:
                visu.visualisation(wp, bp, MyApp.matrix, p1)
            except AttributeError:
                self.warning_text_launch.setText("/!\ Please select files")
                return 1
        else:
            # On teste si l'utilisateur a choisi un stack de fichiers
            #Si ce n'est pas le cas on affiche un message d'erreur
            try:
                visu.visualisation(wp, bp, MyApp.matrix)
            except AttributeError:
                self.warning_text_launch.setText("/!\ Please select files")
                return 1
            return (width, height)
 
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
    