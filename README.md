
# Introduction

> Ce projet permet d'afficher l'heure et les statistiques d'une chaîne YouTube sur une matrix de LED 8*32 (à acheter [ici](https://www.amazon.fr/gp/product/B072XLD57Q/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1 "Lien vers la page Amazon du produit")) et un RaspBerry Pi avec connexion internet.
<br/> Quelques animations sont incluses.

# Installation


> Je me suis basé sur la doc de la [librairie](https://luma-led-matrix.readthedocs.io/en/latest/install.html "Lien vers la documentation") de la matrix

## Branchements


> Pour commencer, il faut brancher la matrix au RaspBerry selon ce tableau : 

<img src="https://image.ibb.co/jTQUTc/array.png" alt="array" border="0">



> Pour vous repérer sur les pins du RaspBerry :

<img src="https://image.ibb.co/epF2gx/gpio.png" alt="gpio" border="0">


## Activation du SPI



> Pour activer le SPI sur le RaspBerry (nécessaire pour faire fonctionner la matrix), rentrez la commande suivante dans le terminal :  
<code>sudo raspi-config</code>     
Descendez ensuite jusqu'au numéro 5 (Avec la flèche bas du clavier)
 
 
![](https://image.ibb.co/egPETc/raspiconfig1.png "")



> Faites "Entrée"  
Descendez jusqu'a "P4 SPI" puis enter

![](https://image.ibb.co/b8R01x/raspiconfig2.png "")



> Il vous demande ensuite si vous voulez activer le SPI, faites oui

![](https://image.ibb.co/mtNHzH/raspiconfig3.png "")

## Installation de la librairie ##

> Commencez par effectuer les commandes suivantes, certaines ne sont pas nécessaire car elles sont déjà installées par défaut sur le RaspBerry :
> `sudo usermod -a -G spi,gpio pi`  
> Puis : `sudo apt-get install build-essential python-dev python-pip libfreetype6-dev libjpeg-dev`
> Pour finir : `sudo -H pip install --upgrade luma.led_matrix`

## Premier test ! ##

> Avant de lancer le programme, nous allons exécuter un programme de test fournis dans le GitHub de la librairie  
> Commencez par lancer la commande suivante pour télécharger le repository GitHub de la librairie :
> `cd Desktop && git clone https://github.com/rm-hull/luma.led_matrix.git`  
> (Je l'ai placé sur le bureau avec `cd Desktop` mais vous pouvez le mettre où vous voulez).  
> Ouvrez ensuite le dossier, puis faites "outil", ouvrir le dossier actuel dans un terminal :

![](https://image.ibb.co/mgBNic/outil.png)
