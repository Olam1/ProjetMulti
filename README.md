## <a href="http://www.insa-toulouse.fr/" ><img src="http://www.math.univ-toulouse.fr/~besse/Wikistat/Images/Logo_INSAvilletoulouse-RVB.png" style="float:left; max-width: 80px; display: inline" alt="INSA"/></a> |  [*Génie Physique*](http://geniephysique.insa-toulouse.fr/fr/index.html) <span style='color:blue'>|</span> [*ProjetMulti*](https://github.com/Olam1/ProjetMulti)

# Mise en place d'un système de tomographie X
 Le programme permet de visualiser un dossier de fichiers .tif en 3D et de les traiter
 rapidement. Les programmes de reconstructions ne permettent pas encore d'obtenir un résultat probant.
 
## Exécuter le programme
 Il est nécessaire de télécharger l'ensemble des fichiers de la branche *master*
 et d'éxécuter le fichier nommé *main.py* pour la visualisation ou *test.py* pour la reconstruction.
 
## Utilisation du logiciel de visualisation
 - L'utilisateur commence par sélectionner ses fichiers à l'aide du bouton 'Select Folder'
 - Il peut ensuite définir le point blanc et le point noir des son image dans le menu 'opacity'
 - Le point noir correspond au pixels les plus noirs (valeur = 65536) qui ont une opacité de 
 100% par défaut
 - Le point blanc correspond au pixels les plus blancs (valeur = 0) qui ont une opacité de 
 0% par défaut
 - L'utilisateur peut ajouter des points pour filtrer plus précisément les valeurs de pixels 
  qu'il souhaite observer. Pour cela il lui suffit de cliquer sur 'Add Point' et de régler ensuite
  la valeur des pixels à sélectionner et l'opacité qu'il souhaite leur appliquer
 - Enfin, l'appuie sur 'Visualisation' ouvre une fenêtre contenant l'objet 3D, qu'il est possible de 
  tourner, zoomer ou déplacer.
 
## Utilistion du programme reconstruction_tomopy
 - Lancer test.py avec python
 - Choisir un dossier contenant les projetctions au format .tif en cliquant sur *Select*
 - La reconstruction se lance et une coupe apparait dans une fenêtre indépendante

## Utilistion du programme reconstruction_astra
- Installer la librairie astra avec conda : `conda install -c astra-toolbox/label/dev astra-toolbox`
- Lancer *ProjMaker.py*. Ce fichier permet de simuler une tomographie d'un objet en contrôlant les paramètres.
- Lancer test.py dans un terminal externe (dans spyder : Exécution -> Configuration par fichier... -> Exécuter dans un terminal   système externe)
- Cliquer sur *Select File* et choisir le dossier *dataset* qui s'est créé.
  - **Remarque :** Dans la liste déroulante on peut choisir de réduire la taille des images pour simplifier les calculs. Dans un premier temps, choisir : *0.2*
- Attendre la fin du chargement. Si tout s'est bien déroulé une pop-up s'ouvre indiquant : *La reconstruction a bien été effectué*
- Les images reconstruites se trouvent dans le dossier *recon*

## Pré-requis
 - PyQt5
 - Pylab
 - [Glob](https://docs.python.org/fr/3.6/library/glob.html)
 - [Vtk](https://github.com/Kitware/VTK)
 - [Tomopy](https://github.com/tomopy/tomopy)
 - astra-toolbox
 
