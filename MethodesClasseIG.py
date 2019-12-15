from PyQt5 import QtWidgets,QtGui
import visualisation_ok as visu
import WindowStandby
import LirePoints
from matplotlib.backends.backend_qt5agg import FigureCanvas 
from PIL import ImageGrab
import win32gui



#Fichier contenant les méthodes de la classe InterfaceGraphique 


#Rend les boutons des points 1,2 et 3 cliquables
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
            options = QtWidgets.QFileDialog.ShowDirsOnly
            )
    #Gestion de l'exception dans le cas où l'utilisateur choisit un mauvais dossier
    #Si aucun dossier n'est sélectionné path = 0 et il ne se passe rien
    if path:
        try:
            self.matrix = visu.MatrixGeneration(path+'/*.tif')
        except IndexError:
            gestion_message(self, 111)
            return 1
        except ValueError:
            gestion_message(self, 113)
            return 1
        return self.matrix

#Ouvre la fenêtre conteant la visualisation en 3D de l'objet
def afficher(self):
    gestion_message(self, 100)
    #On récupère les données des points du graph
    wp, bp, p1, p2, p3 =LirePoints.Do(self)
    #On charge le gif contenant l'icône de chargement
    Loader = QtGui.QMovie("loader.gif")
    #On met la fenêtre principale en pause
    #WindowStandby.PauseWindow(self, Loader)
    #On teste si l'utilisateur a choisi un stack de fichiers
    #Si ce n'est pas le cas on affiche un message d'erreur
    try:
        visu.visualisation(wp, bp, self.matrix, p1, p2, p3, self.nb_points)
    except AttributeError:
        gestion_message(self, 112)
        #WindowStandby.RestartWindow(self, Loader)
        return 1
    #On réactive la fenêtre principale
    #WindowStandby.RestartWindow(self, Loader)
    return 0
  
    
#Afficher la graph contenant la courbe d'opacité des différents niveaux de gris
def afficher_graph(self):
    #On efface tous les widgets présents dans le layout 'lay'
    for i in reversed(range(self.lay.count())): 
        self.lay.itemAt(i).widget().deleteLater()
    #On lit les points à afficher et on cree le graph à partir de ces points
    wp, bp, p1, p2, p3 = LirePoints.Do(self)
    fig = visu.creer_graph(wp, bp, p1, p2, p3, self.nb_points)
    #FigureCanvas permet de transformer le graph matplotliq en graph Qt
    self.plotWidget = FigureCanvas(fig)
    #On ajoute le widget contenant le graph dans le layout  
    self.lay.addWidget(self.plotWidget)
    return 0


#Permet d'afficher des massages d'erreur dans la barre de statut
def gestion_message(self, codeErreur = 100):
    self.statusbar.clearMessage()
    if codeErreur == 100:
        self.statusbar.clearMessage()
    elif codeErreur == 111:
        self.statusbar.showMessage("Please select another folder")
    elif codeErreur == 112:
        self.statusbar.showMessage("Please select files")
    elif codeErreur == 113:
        self.statusbar.showMessage("Image with an unexpected size")
    elif codeErreur == 114:
        self.statusbar.showMessage("Screenshot done", 2000)
    elif codeErreur == 115:
        self.statusbar.showMessage("There is no visualisation to capture")
    else:
        self.statusbar.showMessage("Unknown error")
    
    
def capture(self):
    hwnd = win32gui.FindWindow(None,"Visualization Toolkit - Win32OpenGL #1")
    try:
        rect = win32gui.GetWindowRect(hwnd)
    except:
        gestion_message(self, 115)
        return 1
    left = rect[0]
    top = rect[1]
    right = rect[2]
    bottom = rect[3]
    win32gui.SetForegroundWindow(hwnd)
    img = ImageGrab.grab(bbox = (left, top, right, bottom))
    path = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Save your screenshot",
            options = QtWidgets.QFileDialog.ShowDirsOnly
            )
    #Gestion de l'exception dans le cas où l'utilisateur choisit un mauvais dossier
    #Si aucun dossier n'est sélectionné path = 0 et il ne se passe rien
    if path:
        img.save(path+"/visualisation.jpg", "JPEG")
        gestion_message(self, 114)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
