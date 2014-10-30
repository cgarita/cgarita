#!/usr/bin/python
  # -*- coding: iso-8859-15 -*-
# Modulos importados
import os
import shutil
import string
import time
import MySQLdb
import getopt, sys, math
from os.path import exists, join, abspath
from os import pathsep
from string import split
from datetime import datetime
import pytz, dateutil.parser
import smtplib
import urllib2
import subprocess


TO = 'christian.garita.hidalgo@una.cr'
SUBJECT = "Magnitudes Log"
 
FROM = "cgarita@una.cr"
os.system('tail /var/log/messages >  /opt/ProgramaEQ/tail.txt ')
# read a text file as a list of lines
# find the last line, change to a file you have
fileHandle = open ( '/opt/ProgramaEQ/tail.txt',"r" )
lineList = fileHandle.readlines()
fileHandle.close()
#BODY= lineList
#print "The last line is:"
#print lineList[len(lineList)-1]
# or simply
BODY= lineList[-1]
#BODY= "Prueba"
print BODY
message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, BODY)

#print text
#BODY = string.join((
# 	"From: %s" % FROM,
#       	"To: %s" % TO,
#        "Subject: %s" % SUBJECT ,
#       	"",
#       	text
#      	), "\r\n")	
try:
	server = smtplib.SMTP("smtp.gmail.com")
	server.sendmail(FROM, TO, BODY)	
except Exception, e:
	print "Error: unable to send email" + TO
server.quit()
#FIN envio Correo
#Envio de mensaje de texto
