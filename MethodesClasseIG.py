from PyQt5 import QtWidgets,QtGui
import visualisation_ok as visu
import WindowStandby
import LirePoints
from matplotlib.backends.backend_qt5agg import FigureCanvas 



#Fichier contenant les méthodes de la classe InterfaceGraphique 



def ajouter_points(self):
        self.nb_points+=1
        if self.nb_points == 1:
            self.point1Slider.setEnabled(True)
            self.point1spinBox.setEnabled(True)
        elif self.nb_points == 2:
            self.point2Slider.setEnabled(True)
            self.point2spinBox.setEnabled(True)
        else:
            self.point3Slider.setEnabled(True)
            self.point3spinBox.setEnabled(True)
        print(self.nb_points)
        return self.nb_points
 
    
#Reçoit un dossier contenant les TIF et renvoie une matrice
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
            self.matrix = visu.file_choice(path)
        except IndexError:
            self.warning_text_select_file.setText("/!\ Please select another folder")
            return 1
        return self.matrix

#Ouvre la fenêtre conteant la visualisation en 3D de l'objet
def afficher(self):
    self.warning_text_launch.clear()
    wp, bp, p1, p2, p3 =LirePoints.Do(self)
    visu.greyscale_graph(wp, bp, p1, p2, p3, self.nb_points)
    #On charge le gif contenant l'icône de chargement
    Loader = QtGui.QMovie("loader.gif")
    #On met la fenêtre principale en pause
    WindowStandby.PauseWindow(self, Loader)
    # On teste si l'utilisateur a choisi un stack de fichiers
    #Si ce n'est pas le cas on affiche un message d'erreur
    try:
        visu.visualisation(wp, bp, self.matrix, p1, p2, p3, self.nb_points)
    except AttributeError:
        self.warning_text_launch.setText("/!\ Please select files")
        WindowStandby.RestartWindow(self, Loader)
        return 1
    #On réactive la fenêtre principale
    WindowStandby.RestartWindow(self, Loader)
    return 0
  
    
#Afficher la graph contenant la courbe d'opacité des différents niveaux de gris
def afficher_graph(self):
    wp, bp, p1, p2, p3 =LirePoints.Do(self)
    fig = visu.creer_graph(wp, bp, p1, p2, p3, self.nb_points)
    self.plotWidget = FigureCanvas(fig)
    lay = QtWidgets.QVBoxLayout(self.content_plot)  
    lay.setContentsMargins(0, 0, 0, 0)      
    lay.addWidget(self.plotWidget)
    return 0


