
# Introduction

> Ce projet permet d'afficher l'heure et les statistiques d'une chaîne YouTube sur une matrix de LED 8*32 (à acheter ici : https://www.amazon.fr/gp/product/B072XLD57Q/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1) et un RaspBerry Pi avec connexion internet.
<br/> Quelques animations sont incluses.

# Installation
Je me suis basé sur la doc de la <a href=https://luma-led-matrix.readthedocs.io/en/latest/install.html>librairie</a> de la matrix

## Branchements
> Pour commencer, il faut brancher la matrix au RaspBerry selon ce tableau : 
<br/>
<img src="https://image.ibb.co/jTQUTc/array.png" alt="array" border="0">
<br/>
Pour vous repérer sur les pins du RaspBerry :
<br/>
<img src="https://image.ibb.co/epF2gx/gpio.png" alt="gpio" border="0">
<br/>

## Activation du SPI

> Pour activer le SPI sur le RaspBerry (nécessaire pour faire fonctionner la matrix), rentrez la commande suivante dans le terminal :
<br/><code>sudo raspi-config</code>
<br/> Descendez ensuite jusqu'au numéro 5 (Avec la flèche bas du clavier)
<br/><img src="https://image.ibb.co/iE2ZTc/raspiconfig1.png" alt="raspiconfig1" border="0">
<br/> Faites "Entrée"
<br/> Descendez jusqu'a "P4 SPI" puis enter
<br/>


