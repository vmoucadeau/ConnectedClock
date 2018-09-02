#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

import re
import time
import argparse
import requests
import json
import RPi.GPIO as GPIO
import sys,getopt



from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport					#LED Display Librairies
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
from luma.core import legacy
from datetime import datetime
#show_message(device, "Message voulu", fill="white", font=proportional(CP437_FONT)) (Ceci est une base pour un message quelconque)


									# ---------- CONFIGURATION ---------- #
'''
Infos :
Les accents et certains caractères spécieaux ne sont pas pris en compte ! :(
'''

				# ----- MATERIEL ----- #
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=-90)
			   # ----- API YOUTUBE ----- #
yt_activation = True #(Ou False) : Variable d'activation des informations YouTube
# Cela vous permet de désactiver les messages liés aux informations de votre chaine (si vous en avez pas, mettez False)

# Votre clef API YouTube ici :
yt_apikey = "AIzaSyAC_UVnLkTps5Cbtb47EvJT7EF40HEeSh4"
# Info : Pour récupérer votre clef API, RDV sur https://console.developers.google.com/apis

#L'id de votre chaine ici :
yt_channelid = "UC6PaoWMe1N30IR5fBzdj7Gw"
# Info : L'ID de votre chaine se trouve dans l'URL de celle ci.
# Ex : UC6PaoWMe1N30IR5fBzdj7Gw (GENERATION2GEEK)
# Ex : UC79hj8DOFEBaaCSrJr73Rbg (Chaine de Lucas Pecout)

# Nombre de répétitions du message YouTube, non nécessaire si yt_activation = False
yt_nbrerepet = 1

# Nombre de minutes avant l'exécution des messages YT
yt_minuteur = 5
yt_minactu = 0 # Minutes YouTube actuelles


		   # ----- MESSAGE INFOS DU JOUR ----- #
bvnmsg_activation = 1 # Permet de désactiver le message
# Pour modifier le messge, rdv à la ligne 238
bvnmsg_nbrerepet = 2 # Nombre de répétitions du message qui affiche les infos du jour
bvnmsg_minuteur = 0	 # Nombre de minutes avant l'exécution du message
bvnmsg_minactu = 0	 # Minutes actuelles

lumlowstart = 21 # Heure de début de la diminution de la luminositée de l'afficheur (21h par défaut)
lumlowstop = 8 	 # Heure de fin de la diminution de la luminositée de l'afficheur (8h par défaut)
lumoffstart = 22
lumoffstop = 7

gpiok = 17 # GPIO du servomoteur
statu=-1

lumislow = 0 # Ne pas toucher
device.contrast(16) # Ne pas toucher
started = 0 # Ne pas toucher

def youtubeinfos(yt_apikey, yt_channelid, yt_nbrerepet):
	try:
									   # ----- Requêtes vers l'API YT ----- #
		# Préparation de la requête stats
		requeststats = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + yt_channelid + "&key=" + yt_apikey
		# Préparation de la requête channel name
		requestchannelname = "https://www.googleapis.com/youtube/v3/channels?part=brandingSettings&id=" + yt_channelid + "&key=" + yt_apikey
		# Exécution de la requête stats
		resultstats = requests.get(requeststats)
		# Exécution de la requête pour récupérer le nom de la chaine
		resultchannelname = requests.get(requestchannelname)
		# Transformation en JSON du résultat de la requête pour récupérer les stats de la chaine
		jsonstats = resultstats.json()
		# Transformation en JSON du résultat de la requête pour récupérer le nom de la chaine
		jsonchannelname = resultchannelname.json()
		# Création des variables pour enregistrer les données récupérées
		subs = jsonstats['items'][0]['statistics']['subscriberCount'] # La variable "subs" contient votre nombre d'abonnés YT
		views = jsonstats['items'][0]['statistics']['viewCount'] # La variable "views" contient votre nombre de vues sur votre chaine YT
		channelname = jsonchannelname['items'][0]['brandingSettings']['channel']['title'] # La variable "channelname" contient le nom de votre chaine
	
										# ----- Diffusion des messages ----- #
		# Variable du message pour les subs (vous pouvez le modifier si vous le souhaitez) :
		msg = "Abonnes sur " + channelname + " : " + subs
		# Variable servant à la boucle while suivante
		message = 0
		# Boucle while permettant d'afficher plusieurs fois le message
		while message != yt_nbrerepet:
			show_message(device, msg, fill="white", font=proportional(CP437_FONT))
			message += 1
		message = 0 # Réinitialisation
		time.sleep(0.5) # Petite pause
		# Changement du message pour les vues
		msg = "Vues sur " + channelname + " : " + views
		# Même boucle
		while message != yt_nbrerepet:
			show_message(device, msg, fill="white", font=proportional(CP437_FONT)) 
			message += 1
		message = 0 # Réinitialisation
		time.sleep(0.5)
		upanim()
	except:
		show_message(device, "Aucune connexion internet ou probleme de configuration", fill="white", font=proportional(CP437_FONT))

def mintransition():
	hourstime = datetime.now().strftime('%H')
	mintime = datetime.now().strftime('%M')
	transitionhaut = 1
	transitionbas = 8
	affichagemin = viewport(device, width=device.width, height=100)
	affichagehours = viewport(device, width=device.width, height=100)
	with canvas(affichagemin) as draw:
		text(draw, (17, 1), mintime, fill="white", font=proportional(CP437_FONT))
	
	while transitionhaut != 8:
		with canvas(affichagehours) as draw:
			text(draw, (0, 1), hourstime, fill="white", font=proportional(CP437_FONT))
			text(draw, (15, 1), ":", fill="white", font=proportional(TINY_FONT))
		affichagemin.set_position((0, transitionhaut))
		affichagehours.set_position((0, 0))
		time.sleep(0.1)
		transitionhaut += 1
	while transitionbas != 1:
		with canvas(affichagehours) as draw:
			text(draw, (0, 1), hourstime, fill="white", font=proportional(CP437_FONT))
			text(draw, (15, 1), ":", fill="white", font=proportional(TINY_FONT))
		affichagemin.set_position((0, transitionbas))
		affichagehours.set_position((0, 0))
		time.sleep(0.1)
		transitionbas -= 1		
	
def hourstransition():
	hourstime = datetime.now().strftime('%H')
	mintime = datetime.now().strftime('%M')
	transitionhaut = 1
	transitionbas = 8
	affichage = viewport(device, width=device.width, height=100)
	with canvas(affichage) as draw:
		text(draw, (0, 1), hourstime, fill="white", font=proportional(CP437_FONT))
		text(draw, (15, 1), ":", fill="white", font=proportional(TINY_FONT))
		text(draw, (17, 1), mintime, fill="white", font=proportional(CP437_FONT))
	while transitionhaut != 8:
		affichage.set_position((0, transitionhaut))
		time.sleep(0.1)
		transitionhaut += 1
	while transitionbas != 1:	
		affichage.set_position((0, transitionbas))
		time.sleep(0.1)
		transitionbas -= 1

def upanim():
	hourstime = datetime.now().strftime('%H')
	mintime = datetime.now().strftime('%M')
	transitionbas = 8
	affichage = viewport(device, width=device.width, height=100)
	with canvas(affichage) as draw:
		text(draw, (0, 1), hourstime, fill="white", font=proportional(CP437_FONT))
		text(draw, (15, 1), ":", fill="white", font=proportional(TINY_FONT))
		text(draw, (17, 1), mintime, fill="white", font=proportional(CP437_FONT))
	affichage.set_position((0, 8))
	while transitionbas != 1:	
		affichage.set_position((0, transitionbas))
		time.sleep(0.1)
		transitionbas -= 1

def downanim():
	hourstime = datetime.now().strftime('%H')
	mintime = datetime.now().strftime('%M')
	transitionhaut = 1
	affichage = viewport(device, width=device.width, height=100)
	with canvas(affichage) as draw:
		text(draw, (0, 1), hourstime, fill="white", font=proportional(CP437_FONT))
		text(draw, (15, 1), ":", fill="white", font=proportional(TINY_FONT))
		text(draw, (17, 1), mintime, fill="white", font=proportional(CP437_FONT))
	affichage.set_position((0, 8))
	while transitionhaut != 8:
		affichage.set_position((0, transitionhaut))
		time.sleep(0.1)
		transitionhaut += 1

def lumfaible():
	downanim()
	show_message(device, "Diminution de la luminosite", fill="white", font=proportional(CP437_FONT)) 
	device.contrast(0)
	upanim()

def lumeleve():
	downanim()
	show_message(device, "Augmentation de la luminosite", fill="white", font=proportional(CP437_FONT))
	device.contrast(16)
	upanim()
	
def message(msg):
	downanim()
	show_message(device, msg, fill="white", font=proportional(CP437_FONT))
	upadnim()




def servo(angle, gpio):
	
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(gpio, GPIO.OUT)
	
	ajoutAngle = 5
	pwm=GPIO.PWM(17,100)
	pwm.start(5)

	angleChoisi = float(angle)/10 + ajoutAngle
	pwm.ChangeDutyCycle(angleChoisi)
	time.sleep(5)
	GPIO.cleanup()
		

while True:
	hours = datetime.now().strftime('%H') # Récup des heures
	hoursint = int(hours, 10)
	min = datetime.now().strftime('%M') # Récup des minutes
	day = datetime.now().strftime('%d')	# Récup du jour
	monthnbr = datetime.now().strftime('%m') # Récup du mois (le numéro)
	sec = datetime.now().strftime('%S') # Récup des secondes
	year = datetime.now().strftime('%Y') # Récup des années
	if monthnbr == "01":	 #-----|
		month = "Janvier"	 #	   |
	elif monthnbr == "02":	 #	   |
		month = "Fevrier"	 #	   |
	elif monthnbr == "03":	 #	   |
		month = "Mars"		 #	   |
	elif monthnbr == "04":	 #	   |
		month = "Avril"	     #	   |
	elif monthnbr == "05":	 #	   |
		month = "Mai"		 #	   |
	elif monthnbr == "06":	 #	   |
		month = "Juin"	     #	   |
	elif monthnbr == "07":	 #	   |---------------- Permet de déterminer le nom du mois actuel
		month = "Juillet"	 #     |
	elif monthnbr == "08":	 #     |
		month = "Aout"		 #	   |
	elif monthnbr == "09":	 #	   |
		month = "Septembre"	 #	   |
	elif monthnbr == "10":	 #	   | 
		month = "Octobre"	 #     |
	elif monthnbr == "11":	 #     |
		month = "Novembre"	 #     |
	elif monthnbr == "12":	 #	   |
		month = "Decembre"   #-----|
	
	if yt_activation:
		if sec == "15":
			if yt_minuteur == yt_minactu:
				yt_minactu = 0
				downanim()
				youtubeinfos(yt_apikey, yt_channelid, yt_nbrerepet)
			else:
				yt_minactu += 1
		
	if sec == "59":
		if min == "59":
			hourstransition()
		else:
			mintransition()	
	else:
		with canvas(device) as draw:
			text(draw, (0, 1), hours, fill="white", font=proportional(CP437_FONT))
			text(draw, (15, 1), ":", fill="white", font=proportional(TINY_FONT))
			text(draw, (17, 1), min, fill="white", font=proportional(CP437_FONT))
		
	if started == 0:
		started = 1
		upanim()
												  # ----- Luminosité ----- #				
	if hoursint >= lumlowstart or hoursint <= lumlowstop:
		if lumislow == 0:
			lumislow = 1
			downanim()
			lumfaible()			
	else:
		if lumislow == 1:
			lumislow = 0
			downanim()
			lumeleve()	 

	bvnmsg = day + " " + month + " " + year
	if bvnmsg_activation:
		if sec == "30":
			if bvnmsg_minuteur == bvnmsg_minactu:
				bvnmsg_minactu = 0
				downanim()
				show_message(device, bvnmsg, fill="white", font=proportional(CP437_FONT))
			else:
				bvnmsg_minactu += 1
				
	time.sleep(1)







	
