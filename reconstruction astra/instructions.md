# Instructions
- Installer la librairie astra avec conda : `conda install -c astra-toolbox/label/dev astra-toolbox`
- Lancer *ProjMaker.py*. Ce fichier permet de simuler une tomographie d'un objet en contrôlant les paramètres (plus simple pour le début qu'avec nos fichiers). Voir [ce tutoriel](https://tomroelandts.com/articles/astra-toolbox-tutorial-reconstruction-from-projection-images-part-1) pour plus de détails.
- Lancer test.py dans un terminal externe (dans spyder : Exécution -> Configuration par fichier... -> Exécuter dans un terminal système externe)
- Cliquer sur *Select File* et choisir le dossier *dataset* qui s'est créé.
  - **Remarque :** Dans la liste déroulante on peut choisir de réduire la taille des images pour simplifier les calculs. Dans un premier temps, choisir : *0.2*
- Attendre la fin du chargement. Si tout s'est bien déroulé une pop-up s'ouvre indiquant : *La reconstruction a bien été effectué*
- Les images reconstruites se trouvent dans le dossier *recon*
