
# Introduction

> Ce projet permet d'afficher l'heure et les statistiques d'une chaîne YouTube sur une matrix de LED 8*32 (à acheter [ici](https://www.amazon.fr/gp/product/B072XLD57Q/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1 "Lien vers la page Amazon du produit")) et un RaspBerry Pi avec connexion internet.
<br/> Quelques animations sont incluses.

# Installation


> Je me suis basé sur la doc de la [librairie](https://luma-led-matrix.readthedocs.io/en/latest/install.html "Lien vers la documentation") de la matrix  
> Vous pouvez aussi regarder la vidéo YouTube que j'ai fait sur le sujet.

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

> *Remarque : maintenant, au démmarage du RaspBerry, votre afficheur devrait s'éclairer en rouge.*

## Installation de la librairie ##

> Commencez par effectuer les commandes suivantes, certaines ne sont pas nécessaire car elles sont déjà installées par défaut sur le RaspBerry :  
> `sudo usermod -a -G spi,gpio pi`  
> Puis : `sudo apt-get install build-essential python-dev python-pip libfreetype6-dev libjpeg-dev`
> Pour finir : `sudo -H pip install --upgrade luma.led_matrix`

# Premier test ! 

> Avant de lancer le programme, nous allons exécuter un programme de test fournis dans le GitHub de la librairie  
> Commencez par lancer la commande suivante pour télécharger le repository GitHub de la librairie :  
> `cd Desktop && git clone https://github.com/rm-hull/luma.led_matrix.git`  
> (Je l'ai placé sur le bureau avec `cd Desktop` mais vous pouvez le mettre où vous voulez).  
> Ouvrez ensuite le dossier, puis faites "outil", ouvrir le dossier actuel dans un terminal :

![](https://image.ibb.co/mgBNic/outil.png)

> Tapez ensuiste la commande `python examples/matrix_demo.py`  
> Sur votre afficheur vous devriez avoir le résultat suivant :  

[![Alt text](https://img.youtube.com/vi/4s9mpKIC8Eo/0.jpg)](https://www.youtube.com/watch?v=4s9mpKIC8Eo)

# Configuration/Lancement du programme

> Si le programme de test fonctionne, vous pouvez télécharger le fichier python situé dans ce repo GitHub et le mettre sur le bureau du RaspBerry.  
> Editez le avec Geany ou Thonny sur votre RaspBerry, vous obtiendrez ceci :  

![](https://image.ibb.co/c3MBRx/codeconf.png)

> Vous pouvez maintenant modifier le programme à votre aise pour que cela fonctionne pour vous, les paramètres sont bien détaillés dans le code et dans la vidéo, je ne vois donc pas d'utilité à tout expliquer dans ce README.  
> **Enfin pour lancer le programme, il vous suffit de lancer la commande suivante dans un terminal : `cd Desktop && python connectedclock.py`**

# BONUS #

> En ajoutant la ligne suivante dans le fichier `/etc/rc.local` de votre RaspBerry vous pouvez lancer le programme au démarrage de celui ci.
> Pour éditer ce fichier, utilisez la commande `sudo nano /etc/rc.local` ou `sudo vim /etc/rc.local`.  
>  Il ressemble à ça :  

![](https://image.ibb.co/gWL2zH/rclocal.png)

> Il vous suffit de rajouter la ligne `python /home/pi/Desktop/connectedclock.py &` entre `fi` et `exit 0` **NE TOUCHEZ A RIEN D'AUTRE, SINON VOUS DEVREZ PEUT ETRE REINSTALLER RASPBIAN (si vous supprimez `exit 0` par exemple)**

# FIN #

> On se retrouve à la fin du tuto, j'espère que ce projet vous aura plus et vous aura donné des idées avec les autres projet que j'ai déjà fait (Domotique, SARAH...) **BON BRICOLAGE !**


# VERSIONS #

- Version 1.0 : Horloge + Compteur de vues et d'abonnés YouTube
- *(Prochaine) Version 1.5 : Rajout de la domotique et de SARAH (Rassemblement des 3 projets)*
- *(Prochaine) Version 2.0 : Rajout d'une fonctionnalité réveil configurable à partir d'une application android ou une interface web (pour les appareils Apple)*

# FONCTIONNALITES #

- Version 1.0 :
	
	- Compteur d'abonnés et de vues YouTube
	- Horloge
	- Animations (Changement de minutes, heures...)
	- Diminution et augmentation de la luminosité grâce à une plage horaire définie
