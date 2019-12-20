# -*- coding: utf-8 -*-
#Logo : 3d 360 rotation by Dekin Dorcas from the Noun Project

import sys
from PyQt5 import uic, QtWidgets


 
#Création d'une métaclasse Ui_Mainwindow(je crois ?) associée au fichier xml (ca devient compliqué là mais c'est pas important)
Ui_MainWindow, QtBaseClass = uic.loadUiType("user_interface.ui")


#Définition de la class InterfaceGraphique qui hérite des classes "QtWidgets.QMainWindow"
# et "Ui_MainWindow"
class InterfaceGraphique(QtWidgets.QMainWindow, Ui_MainWindow):

    from MethodesClasseIG import ajouter_points, choix_fichier, afficher, afficher_graph, retirer_points, capture
    #from MethodeUpdateGraph import update_graph
    #Defiition du constructeur de la classe
    def __init__(self):
        #Initialisation de la classe parent QMainWindow
        QtWidgets.QMainWindow.__init__(self)
        #Utilisation de la méthode setupUi hérité de la classe Ui_Mainwindow
        self.setupUi(self)
        #Définition d'un attribut nb_points
        self.nb_points=0
        #Définition d'un attribut matrix
        self.matrix=0;
        
        self.afficher_graph()
        
        self.select_file.clicked.connect(self.choix_fichier)
        self.launch.clicked.connect(self.afficher)
        self.add_point.clicked.connect(self.ajouter_points)
        self.remove_point.clicked.connect(self.retirer_points)
        #self.update_graph.clicked.connect(self.afficher_graph)
        self.screenshot.clicked.connect(self.capture)
        
        #Si un paramètre est changé on met le graphique à jour
        self.spinBox_black_point.valueChanged.connect(self.afficher_graph)
        self.spinBox_white_point.valueChanged.connect(self.afficher_graph)
        self.add_point.clicked.connect(self.afficher_graph)
        self.remove_point.clicked.connect(self.afficher_graph)
        self.point1spinBox.valueChanged.connect(self.afficher_graph)
        self.point2spinBox.valueChanged.connect(self.afficher_graph)
        self.point3spinBox.valueChanged.connect(self.afficher_graph)
        self.point1Slider.valueChanged.connect(self.afficher_graph)
        self.point2Slider.valueChanged.connect(self.afficher_graph)
        self.point3Slider.valueChanged.connect(self.afficher_graph) 
        
        
        
   
  

 
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = InterfaceGraphique()
    window.show()
    sys.exit(app.exec_())
    
