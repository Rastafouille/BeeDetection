# BeeDetection

3 objectifs pour ce projet Python OpenCV !
A partir d'une vidéo déja réalisées ou en streaming de la zone d'entrée de la ruche :
- compter les entrées/sorties d'abeilles,
- compter les varroa sur les abeilles en vol pour en déduire un % d'infestation sans perturber la colonie

	 ![Alt text](data:image/jpeg;base64,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)

	- détecter, caractériser et quantifier le pollen

	 ![Alt text](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSNFnr8p8BPzZkSS-ff4QY-BbNaoRdQovqRTNWSwbAVOT2Cj0R-Ig)
	
Pour faire ca les fonctions principales sont :
	- la détection des abeilles en vol - ok
	- le tracking - en cours
	- l'identification
	- détection varroa
	- détection pollen
	- classification pollen

	