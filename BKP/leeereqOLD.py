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
#Funciones dpueblo
def Usage():
	print "dpueblo.py -h -a lat -o lon"
	sys.exit(0)
	
'''' subroutina para convertir la latitud geografica a latitud
 geocentrica utilizando f = 1/298.257'''
def dircos(lat,lon):
	rad = 0.017453292
	e2 = 0.993305615
	c = math.cos(rad*lat)
	s = math.sin(rad*lat)
	e4 = e2*e2
	fac = math.sqrt(e4+(1.0-e4)*c*c)
	slat = e2*s/fac
	clat = c/fac
	slon = math.sin(rad*lon)
	clon = math.cos(rad*lon)
	aa = clat*clon
	bb = clat*slon
	cc = slat
	return [aa,bb,cc,slat,clat,slon,clon]

def dlaz(elat,elon,slat,slon):
	rad = 0.017453292
	e2 = 0.993305615
	re = 6371.003
	[ea,eb,ec,eslat,eclat,eslon,eclon] = dircos(elat,elon)
	[sa,sb,sc,sslat,sclat,sslon,sclon] = dircos(slat,slon)
	cdel = ea*sa + eb*sb + ec*sc
	fac = (ea-sa)*(ea-sa) + (eb-sb)*(eb-sb) + (ec-sc)*(ec-sc)
	fac = math.sqrt(fac)/2.0
	dist = 2.0*math.asin(fac)
	saz = eclat*(sclat*math.sin(rad*(slon-elon)))
	caz = (sslat -cdel*eslat)
	fac = math.sqrt(saz*saz+caz*caz)
	if fac >= 0.0:
		saz = saz/fac
		caz = caz/fac
		az = math.atan2(saz,caz)
		sbz = -sclat*(eclat*math.sin(rad*(slon -elon)))
		cbz = (eslat -cdel*sslat)
		baz = math.atan2(sbz,cbz)
	else:
		az = 0.0
		caz = 1.0
		saz = 0.0
		baz = 180.0
	az = az/rad
	baz = baz/rad
	if az <= 0.0:
		az = az +360.0
	if baz <= 0.0:
		baz = baz +360.0
		
	return [dist*re, baz]


#INICIO
filelist = os.listdir('/autoeqs/') #$
filelist = filter(lambda x: not os.path.isdir(x), filelist)
newest = max(filelist)
newest = '/autoeqs/' + newest #$
f = open(newest, 'r')
lin = f.readline()
part = lin.split(',')
fecha = part[0]
hora = part[1]
lati = float(part[2])
longi = float(part[3])
depth = float(part[4])
if depth == 0:
	depth = 5
ML = float(part[5])
ML=round(ML,1)
MW = part[6]
if MW != ' - ':
	MW = float(MW)
	MW = round(MW,1)
origen = part[7]
region = part[8]
place = part[9]

###########$

#print 'Fecha GMT: '+fecha+ ' Hora GMT '+hora
#print 'Latitud: '+str(lati)+' Longitud: '+str(longi)
#print 'Profundidad: '+str(depth)+' Magnitud: '+str(ML)
#print 'MW: '+str(MW)

#Cambiar GMT a hora local

# FORMATO TIME p = '2011-04-05T00:41:54.000Z'
p = fecha + 'T' + hora +'.000Z'
utctime = dateutil.parser.parse(p)
localtime = utctime.astimezone(pytz.timezone('America/Costa_Rica'))
timedate = str(localtime)
fechalocal = timedate.split()
horazone = fechalocal[1]
horalocal = horazone.split('-')

#Obtener localizacion
try:
	fi = open('/opt/ProgramaEQ/pueblos.xy', 'r')
# Leyendo el archivo pueblos_gmt con codificación especial
	fo = open('/opt/ProgramaEQ/pueblos_gmt.txt', 'r')
except:
	print 'no existe el archivo pueblos.xy en este directorio'
	sys.exit(1)
	
''' el archivo contiene Nombre del pueblo, Distrito, Canton, Provincia '''

linea = fi.readline()
linea2 = fo.readline()
parte = linea.split(',')
parte2 = linea2.split(',')
pueblo = parte[0]
pueblo2 = parte2[0]
distrito = parte[1]
canton = parte[2]
provincia = parte[3]
distrito2 = parte2[1]
canton2 = parte2[2]
provincia2 = parte2[3]
lat= lati
lon= longi

#''' lat1 = string.atof(parte[5]) '''

lat1 = string.atof(parte[5])
lon1 = string.atof(parte[4])
[dist,baz] = dlaz(lat,lon,lat1,lon1)
while linea:
	parte = linea.split(',')
	parte2 = linea.split(',')
	if parte[0] != 'DESCONOCIDO':
		lat1 = string.atof(parte[5])
		lon1 = string.atof(parte[4])
		[dist1,baz1] = dlaz(lat,lon,lat1,lon1)
		if dist1 <= dist:
			dist = dist1
			baz = baz1
			pueblo = parte[0]
			distrito = parte[1]
			canton = parte[2]
			provincia = parte[3]
			pueblo2 = parte2[0]
			distrito2 = parte2[1]
			canton2 = parte2[2]
			provincia2 = parte2[3]
	linea = fi.readline()
	linea2 = fo.readline()

#print baz
# Obtener punto cardinal
if baz > 350 or baz <= 10:
    cardinal = 'Norte'
elif baz > 10 and baz <= 80:
    cardinal = 'Noreste'
elif baz > 80 and baz <= 100:
    cardinal = 'Este'
elif baz > 100 and baz <= 170:
    cardinal = 'Sureste'
elif baz > 170 and baz <= 190:
    cardinal = 'Sur'
elif baz > 190 and baz <= 260:
    cardinal = 'Suroeste'
elif baz > 260 and baz <= 280:
    cardinal = 'Oeste'
elif baz > 280 and baz <= 350:
    cardinal = 'Noroeste'

dist = int(dist)
if dist == 0:
	localizacion = 'En las cercanias  de '+ pueblo + ' de ' + canton + ' de ' + provincia
	localizacion2 = 'En las cercanias  de '+ pueblo2 
        localizacion3 = 'de ' + canton2 + ' de ' + provincia2
else: 
	localizacion = str(dist) + ' km al '+ cardinal +' de '+ pueblo + ' de ' + canton + ' de ' + provincia
	localizacion2 = str(dist) + ' km al '+ cardinal +' de '+ pueblo2 
	localizacion3 = 'de ' + canton2 + ' de ' + provincia2
emailb = 2
upd = 1
# Codigo para descartar que sea una actualizacion de un sismo +-10seg
try:
	t = open('/tmp/tmpeq', 'r+')
	li = t.readline()
	part = li.split(',')
	fch = part[0]
	hra = part[1]
	mg = part[2]
	#print mg + '+' + str (ML)
	tmphra = hra.split(':')
	nowhra = hora.split(':')
	t.close()
	if fch == fecha and hra == hora and float(mg) == ML: 
		print 'Sin novedad, se continua a la espera de un nuevo sismo'		
		sys.exit()
	elif fch == fecha and tmphra[0] == nowhra[0] and tmphra[1] == nowhra[1]:
 	  	restmpnow= int(tmphra[2]) - int(nowhra[2])
 	 	if restmpnow < 10 or mg != ML: 
			#try:
				#UPDATE si es el mismo sismo solo que relocalizado
				#Codigo para incluir en facebook como ACTUALIZACION
				if MW == ' - ':	#$Actualiza solo si es ML			
					print 'ACTUALIZANDO'					
					sismofb = 'FECHA: ' + fechalocal[0] + ' HORA: ' + horalocal[0] + ' MAG: '+ str(ML) + ' ml PROF: '+ str(depth) + 'km LAT: '+ str(lati) + ' LON: '+ str(longi) + ' LOC: '+ localizacion + ' // Localización preliminar, pendiente de  revisión'
					sismotw = 'ACTUALIZADO:' + fechalocal[0] + '/' + horalocal[0] + ' MAG:'+ str(ML) + ' ml PROF:'+ str(depth) + 'km / '+ localizacion
					sismoep = 'ACTUALIZADO:%20MAG:%20'+ str(ML) + 'ml%20FECHA:' + fechalocal[0] + '%20' + horalocal[0]
					db = MySQLdb.connect (host = "10.10.128.10",user = "root",passwd ="RootMysql",db = "autoeq")
				# prepare a cursor object using cursor() method
					cursor = db.cursor()			
				# Execute the SQL command
				#  INSERT a record into the database.
					try:			
						cursor.execute('UPDATE eqs SET magnitud="%f", profundidad="%f", localizacion="%s", latitud="%f", longitud="%f" WHERE fecha="%s" AND hora="%s"'%(ML, depth, localizacion, lati, longi, fch, hra))	
								
				#Guarda nuevo archivo
						db.commit()					
						print 'Este sismo fue relocalizado'
	 	  				os.system('rm /tmp/tmpeq')
 		   				tmp = open('/tmp/tmpeq', 'wb')
						tmp.write(fecha +','+ hora + ',' + str (ML))
						tmp.close()
						#Update on Twitter
						os.system('ttytter -status="'+ sismotw +'"')						
						##os.system('fbcmd ppost 106757629361504 ACTUALIZACION "'+ sismofb +'"')											
						db.close()
						sismo = fechalocal[0] + '/' + horalocal[0] + '/'+ str(ML) + '/'+ str(depth) + '/'+ str(lati) + '/'+ str(longi) + '/'+ localizacion 	
						# Creando archivo feeder de los sismos
						os.system("sed '15 d' /opt/feed/feed.txt > /opt/feed/feed2.txt")
						os.system("mv /opt/feed/feed2.txt /opt/feed/feed.txt")
						with open("/opt/feed/feed.txt", "r+") as f: s = f.read(); f.seek(0); f.write(sismo +"/U\n" + s)
						urllib2.urlopen("http://www.intraovsi.una.ac.cr/movilnotification/notification_sender.php?pushMessage="+ sismoep)
						upd = 2
					except:
					# Rollback in case there is any error
						print ML 
						print fch + ',' + hra				
						print fecha + ',' + hora
						print 'SQL Error'
						sys.exit()				
						db.rollback()
						db.close()
				else:
					print ' No se Actualizo' 
					upd = 2 #$ Indica que se el sismo fue un MW
except IOError:
	print 'Creando archivo /tmp/'
	tmp = open('/tmp/tmpeq','wb')
	tmp.write(fecha +','+ hora + ',' + str (ML))
	tmp.close()	
# Cambio 26/03/2012 Se habilita para todos los sismos mayores de 2.5 (antes solo mayores de 3) Solicitado por Ronnie
if ML >= 2.5 and dist < 100 and upd == 1:
	#Codigo para incluir en facebook
	if MW != ' - ':
		sismofb = 'SISMO: FECHA: ' + fechalocal[0] + ' HORA: ' + horalocal[0] + ' MAG: '+ str(MW) + ' mw PROF: '+ str(depth) + 'km LAT: '+ str(lati) + ' LON: '+ str(longi) + ' LOC: '+ localizacion + ' // Localización preliminar, pendiente de revisión'
		sismotw = 'PRE:' + fechalocal[0] + '/ ' + horalocal[0] + ' MAG:'+ str(MW) + 'mw PROF:'+ str(depth) + 'km / '+ localizacion + '.'
		sismoep = 'MAG:%20'+ str(MW) + '%20FECHA:' + fechalocal[0] + '%20' + horalocal[0]
	else:
		sismofb = 'SISMO: FECHA: ' + fechalocal[0] + ' HORA: ' + horalocal[0] + ' MAG: '+ str(ML) + ' ml PROF: '+ str(depth) + 'km LAT: '+ str(lati) + ' LON: '+ str(longi) + ' LOC: '+ localizacion + ' // Localización preliminar, pendiente de revisión'
		sismotw = 'PRE:' + fechalocal[0] + '/ ' + horalocal[0] + ' MAG:'+ str(ML) + ' ml PROF:'+ str(depth) + 'km / '+ localizacion + '.'
		sismoep = 'MAG:%20'+ str(ML) + '%20FECHA:' + fechalocal[0] + '%20' + horalocal[0]
	db = MySQLdb.connect (host = "10.10.128.10",user = "root",passwd ="RootMysql",db = "autoeq")
# prepare a cursor object using cursor() method
	cursor = db.cursor()
	try:
# Execute the SQL command
#  INSERT a record into the database.
		os.system('ttytter -status="'+ sismotw +'"')
		if MW == ' - ':
			print ' Aqui se inserta ML'		
			cursor.execute('INSERT INTO eqs(fecha, fechalocal, hora, horalocal, latitud, longitud, profundidad, magnitud, localizacion) VALUES ("%s","%s","%s","%s","%f","%f","%f","%f","%s")'%(fecha, fechalocal[0], hora, horalocal[0], lati, longi, depth, ML, localizacion))	
		else:
			print ' Aqui se inserta MW'
			cursor.execute('INSERT INTO eqs(fecha, fechalocal, hora, horalocal, latitud, longitud, profundidad, magnitud, mw, localizacion) VALUES ("%s","%s","%s","%s","%f","%f","%f","%f","%f","%s")'%(fecha, fechalocal[0], hora, horalocal[0], lati, longi, depth, ML, MW, localizacion))	
# Commit your changes in the database
		#Guarda archivo	
		print 'Se inserto correctamente'
		##os.system('fbcmd ppost 106757629361504 "'+ sismofb +'"')		
		tmp = open('/tmp/tmpeq','r+')
		tmp.write(fecha +','+ hora + ',' + str (ML))
		tmp.close()		
		db.commit()
		#print sismofb	
		
		sismo = fechalocal[0] + '/' + horalocal[0] + '/'+ str(ML) + '/'+ str(depth) + '/'+ str(lati) + '/'+ str(longi) + '/'+ localizacion 	
		# Creando archivo feeder de los sismos
		os.system("sed '15 d' /opt/feed/feed.txt > /opt/feed/feed2.txt")
                os.system("mv /opt/feed/feed2.txt /opt/feed/feed.txt")
                with open("/opt/feed/feed.txt", "r+") as f: s = f.read(); f.seek(0); f.write(sismo +"/A\n" + s)
		emailb = 1 
		urllib2.urlopen("http://www.intraovsi.una.ac.cr/movilnotification/notification_sender.php?pushMessage="+ sismoep)		
	except:
# Rollback in case there is any error
		db.rollback()
		tmp = open('/tmp/tmpeq','r+')
		tmp.write(fecha +','+ hora + ',' + str (ML))
		tmp.close()
		sys.exit()
# disconnect from server
	db.close()
#$Envia SMS si es mayor de 3.0 #24/06/2011
# Comprueba q el sismo no se haya enviado, si es = a 1 ya se envio si es = a 0 es nuevo
if emailb == 1 and ML >= 3:	
	if MW != ' - ':
		#Envio de mensaje de texto
		magnit= str(MW)+'mw'
		profund = str(depth)
		latit = str(lati)
		longit = str (longi)
		locali = localizacion.replace(" ", ";")
		horal = horalocal[0]
		fechal = fechalocal[0]		
		urllib2.urlopen("http://www.intraovsi.una.ac.cr/SMS/enviaGUARDIA.php?fecha=" + fechal + "&hora=" + horal +"&mag=" + magnit + "&prof=" + profund + "&latitud=" + latit + "&longitud=" + longit + "&local=" + locali)	
		print 'Se envia SMS con MW' +magnit
    	else:
		#Envio de mensaje de texto
		magnit= str(ML)+'ml'
		profund = str(depth)
		latit = str(lati)
		longit = str (longi)
		locali = localizacion.replace(" ", ";")
		horal = horalocal[0]
		fechal = fechalocal[0]
		urllib2.urlopen("http://www.intraovsi.una.ac.cr/SMS/enviaGUARDIA.php?fecha=" + fechal + "&hora=" + horal +"&mag=" + magnit + "&prof=" + profund + "&latitud=" + latit + "&longitud=" + longit + "&local=" + locali)	
		print 'Se envia SMS con ML' +magnit
print 'Fecha GMT: '+fecha+ ' Hora GMT '+hora
print 'Latitud: '+str(lati)+' Longitud: '+str(longi)
print 'Profundidad: '+str(depth)+' Magnitud: '+str(ML)+' MW'+str(MW)
print 'Localizacion: '+localizacion
print 'Fecha local: ' +fechalocal[0]+ ' Hora local ' + horalocal[0]
f.close()
#Fin archivo
