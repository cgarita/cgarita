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
# Import the email modules we'll need
from email.mime.text import MIMEText

TO = 'christian.garita.hidalgo@una.cr'
SUBJECT = "Magnitudes Log"
 
FROM = "cgarita@una.cr"
os.system('tail /var/log/messages >  /opt/ProgramaEQ/tail.txt ')
# read a text file as a list of lines
# find the last line, change to a file you have

#lineList = fileHandle.readlines()
#fileHandle.close()
# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
fp = open('/opt/ProgramaEQ/tail.txt',"r")
# Create a text/plain message
msg = MIMEText(fp.read())
#BODY= lineList
#print "The last line is:"
#print lineList[len(lineList)-1]
# or simply
#BODY= lineList[-1]
#BODY= "Prueba"
#print BODY
msg['Subject'] = 'The contents of'
msg['From'] = FROM
msg['To'] = TO


try:
	# Send the message via our own SMTP server, but don't include the
# envelope header.
	s = smtplib.SMTP('samara.una.ac.cr')
	s.sendmail(FROM, [TO], msg.as_string())
	print "EXITO"
	s.quit()	
except Exception, e:
	print "Error: unable to send email" + TO

#FIN envio Correo
#Envio de mensaje de texto
