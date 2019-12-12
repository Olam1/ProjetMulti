

import sys
from PyQt5 import uic, QtWidgets

import matplotlib
matplotlib.use('QT5Agg')




 
#Création d'une métaclasse Ui_Mainwindow(je crois ?) associée au fichier xml (ca devient compliqué là mais c'est pas important)
Ui_MainWindow, QtBaseClass = uic.loadUiType("user_interface.ui")


#Définition de la class InterfaceGraphique qui hérite des classes "QtWidgets.QMainWindow"
# et "Ui_MainWindow"
class InterfaceGraphique(QtWidgets.QMainWindow, Ui_MainWindow):

    from MethodesClasseIG import ajouter_points, choix_fichier, afficher, voir_graph
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
        
        
        self.select_file.clicked.connect(self.choix_fichier)
        self.launch.clicked.connect(self.afficher)
        self.add_point.clicked.connect(self.ajouter_points)
        self.update_graph.clicked.connect(self.voir_graph)
    
    
   
  

 
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = InterfaceGraphique()
    window.show()
    sys.exit(app.exec_())
    
