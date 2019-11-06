# BeeDetection

## Objectifs 

A partir d'une vidéo déja réalisée ou en streaming de la zone d'entrée de la ruche :
- compter les entrées/sorties d'abeilles,
- compter les varroa sur les abeilles en vol pour en déduire un % d'infestation sans perturber la colonie,

![Alt text](https://agripensar.files.wordpress.com/2012/07/6a00d83455b58069e20105361a6de7970c-500wi.jpg)

- détecter, caractériser et quantifier le pollen.

![Alt text](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSNFnr8p8BPzZkSS-ff4QY-BbNaoRdQovqRTNWSwbAVOT2Cj0R-Ig)
	
## Fonctions principales

En Python 3 openCV
	
- la détection des abeilles en vol *- ok*

selection du ROI (Region Of Interest) :

<img src="images/1-ROI.png" width="500"/>

Aprés 1ere binarisation :

<img src="images/2.png" width="500"/>

Aprés suppression du bruit de fond (gaussian, dilate) et soustraction de l'image précédente pour garder que ce qui est en mouvement :

<img src="images/3.png" width="500"/>

Détection des contours :

<img src="images/detect.png" width="500"/>

- le tracking 

Reprise du code sur : <https://github.com/srianant/kalman_filter_multi_object_tracking>

<img src="images/tracking.png" width="500"/>

<img src="images/tracking2.png" width="500"/>

- l'identification


- détection varroa

- détection pollen

Apprentissage par reseau de neurones à convolution avec TensorFlow/keras.
Premier dataset : <https://github.com/piperod/PollenDataset>
Dataset perso a refaire sur fond blanc au printemps :<https://github.com/Rastafouille/PollenDataSet> 

Caractéristique du réseau et dataset :
<img src="images/TF_summary.png" width="500"/>

<img src="images/TF_bee_result.png" width="500"/>

<img src="images/TF_graph_result.png" width="500"/>


- classification pollen



## Installation dépendances pour Ubuntu 18.04

`sudo apt-get update`

`sudo apt-get upgrade`

`sudo apt install python3`

`sudo apt-get install build-essential cmake unzip pkg-config libjpeg-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libatlas-base-dev gfortran`

`sudo apt-get install python3-dev`

`wget https://bootstrap.pypa.io/get-pip.py`

`sudo python3 get-pip.py`

`sudo pip install spyder opencv-python opencv-contrib-python`

`python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose`

tensorflow

