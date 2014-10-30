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
filelist = os.listdir('/autoeqs/')
filelist = filter(lambda x: not os.path.isdir(x), filelist)
newest = max(filelist)
newest = '/autoeqs/' + newest
f = file(newest, 'r')
# Day
f.seek(38)
day=f.read(2)
#Month
f.seek(41)
month=f.read(3)
#Year
f.seek(45)
year=f.read(4)
#Time
f.seek(50)
hora=f.read(8)
#Latitud
f.seek(63)
lati=float(f.read(6))
#Si latitud fue mayor de 9 grados########################################################
f.seek(70)
if f.read(3)=='lon':
	#Longitud
	f.seek(74)
	longi=float(f.read(6))
	#Depth ##########################Si profundidad es menor que 10#################
	f.seek(89)
	if f.read(1)== 'm':
		f.seek(87)
		depth=float(f.read(1))
		#Magnitud
		f.seek(121)
		ML=float(f.read(5)) #X
	else: ########################## Si profundidad es mayor que 10#####################
		f.seek(87)
		depth=float(f.read(3))
		#Magnitud
		f.seek(122)
		ML=float(f.read(5))
else:# latitud menor de 10 grados##########################################
	#Longitud
	f.seek(73)
	longi=float(f.read(6))
	#Depth ##########################Si profundidad es menor que 10#############
	f.seek(88)		
	if f.read(1)== 'm':
		f.seek(86)
		depth=float(f.read(1))
		# Origen
		#f.seek(105)
		#Magnitud
		f.seek(120)
		ML=float(f.read(5))
	else: 	#Depth ##########################Si profundidad es mayor que 10############
		f.seek(86)
		depth=float(f.read(3))
		#Magnitud
		f.seek(121)
		ML=float(f.read(5))

# Modificar Nombre Mes por Numeral
if month == 'Jan':
	month='01'
elif month == 'Feb':
	month='02'
elif month == 'Mar':
	month='03'
elif month == 'Apr':
	month='04'
elif month == 'May':
	month='05'
elif month == 'Jun':
	month='06'
elif month == 'Jul':
	month='07'
elif month == 'Aug':
	month='08'
elif month == 'Sep':
	month='09'
elif month == 'Oct':
	month='10'
elif month == 'Nov':
	month='11'
elif month == 'Dec':
	month='12'

fecha=year + '-' + month + '-' + day

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
if depth == 0:
	depth = 5
#lugar para pruebas
#prueba='Buenos dias'
#os.system('ttytter -status="ACTUALIZACION: '+ prueba +'"')
#Conexion a la BD
ML=round(ML,1)
emailb = 1

#sismofb = 'SISMO: FECHA: ' + fechalocal[0] + ' HORA: ' + horalocal[0] + ' MAG: '+ str(ML) + ' PROF: '+ str(depth) + 'km LAT: '+ str(lati) + ' LON: '+ str(longi) + ' LOC: '+ localizacion + ' // ESTA LOCALIZACION ES AUTOMATICA Y PRELIMINAR, PUEDE TENER ERRORES'
#print sismofb
# Codigo para descartar que sea una actualizacion de un sismo +-10seg
# Cambio 26/03/2012 Se habilita para todos los sismos mayores de 2.5 (antes solo mayores de 3) Solicitado por Ronnie
if ML >= 2.3 and dist < 56:
	#Codigo para incluir en facebook	
	sismofb = 'SISMO: FECHA: ' + fechalocal[0] + ' HORA: ' + horalocal[0] + ' MAG: '+ str(ML) + ' PROF: '+ str(depth) + 'km LAT: '+ str(lati) + ' LON: '+ str(longi) + ' LOC: '+ localizacion + ' // Localización preliminar, pendiente de revisión'
	sismotw = 'PRE:' + fechalocal[0] + '/ ' + horalocal[0] + ' MAG:'+ str(ML) + ' PROF:'+ str(depth) + 'km / '+ localizacion + '.'
	sismoep = 'MAG:%20'+ str(ML) + '%20FECHA:' + fechalocal[0] + '%20' + horalocal[0]
	#urllib2.urlopen("http://www.intraovsi.una.ac.cr/movilnotification/notification_sender.php?pushMessage="+ sismoep)
	#db = MySQLdb.connect (host = "10.0.50.36",user = "root",passwd ="RootMysql",db = "autoeq")
# prepare a cursor object using cursor() method
	#cursor = db.cursor()
	try:
# Execute the SQL command
#  INSERT a record into the database.
		#cursor.execute('INSERT INTO eqs(fecha, fechalocal, hora, horalocal, latitud, longitud, profundidad, magnitud, localizacion) VALUES ("%s","%s","%s","%s","%f","%f","%f","%f","%s")'%(fecha, fechalocal[0], hora, horalocal[0], lati, longi, depth, ML, localizacion))	
# Commit your changes in the database
		#Guarda archivo	
		print 'Se inserto correctamente'		
		#tmp = open('/tmp/tmpeq','r+')
		#tmp.write(fecha +','+ hora)
		#tmp.close()		
		#db.commit()
		#print sismofb	
		#os.system('fbcmd ppost OVSICORI-UNA "'+ sismofb +'"')
		sismo = fechalocal[0] + '/' + horalocal[0] + '/'+ str(ML) + '/'+ str(depth) + '/'+ str(lati) + '/'+ str(longi) + '/'+ localizacion 
		
		#os.system("sed '15 d' /opt/feed/feedtmp.txt > /opt/feed/feedtmp2.txt")
                #os.system("mv /opt/feed/feedtmp2.txt /opt/feed/feedtmp.txt")
		#with open("/opt/feed/feedtmp.txt", "r+") as f: s = f.read(); f.seek(0); f.write(sismo +"/A\n" + s)		
		#os.system('cp tempfile filename')		
		#feed=open('tempfile', 'w')
		#feed.write(sismo + "/A\n")
		#temporal=open('filename', 'r')
		#s = temporal.read()
		#os.rename('tempfile', 'filename')	
		#open('tempfile', 'w').write(sismo +'\n' + open('filename', 'r').read()) 
		#os.rename('tempfile', 'filename')		
		# Creando archivo feeder de los sismos
		#feed = open('/opt/feed/feed.txt','a+')
		#feed.write(sismo +"/A\n")
		#feed.close		
		#Twitter
		#os.system('ttytter -status="'+ sismotw +'"')		
		emailb = 1 
	except:
# Rollback in case there is any error
		#db.rollback()
		emailb = 1
		#tmp = open('/tmp/tmpeq','r+')
		#tmp.write(fecha +','+ hora)
		#tmp.close()
		print "error"
		sys.exit()
# disconnect from server
	#db.close()
#Envia Correo si es mayor de 4.0 #24/06/2011
# Comprueba q el sismo no se haya enviado, si es = a 1 ya se envio si es = a 0 es nuevo
if emailb == 1:#Desabilitado 19/09/2012 Se movio al servidor 10.10.128.175	
	if ML >= 4:
      		#Envio de mensaje de texto
		magnit= str(ML)
		profund = str(depth)
		latit = str(lati)
		longit = str (longi)
		locali = localizacion.replace(" ", ";")
		horal = horalocal[0]
		fechal = fechalocal[0]
		#urllib2.urlopen("http://www.guiaicai.una.ac.cr/~ovsicori/auto/enviaSMS.php?fecha=" + fechal + "&hora=" + horal +"&mag=" + magnit + "&prof=" + profund + "&latitud=" + latit +"&longitud=" + longit + "&local=" + locali)			
		print 'Mensaje enviado'
#sismo = fechalocal[0] + '/' + horalocal[0] + '/'+ str(ML) + '/'+ str(depth) + '/'+ str(lati) + '/'+ str(longi) + '/'+ localizacion 
#urllib2.urlopen("http://zurqui1.una.ac.cr/ovsicori/movilnotification/notification_sender.php?pushMessage="+ sismo)
print "Se envio el notification"		
print 'Fecha GMT: '+fecha+ ' Hora GMT '+hora
print 'Latitud: '+str(lati)+' Longitud: '+str(longi)
print 'Profundidad: '+str(depth)+' Magnitud: '+str(ML)
print 'Localizacion: '+localizacion
print 'Fecha local: ' +fechalocal[0]+ ' Hora local ' + horalocal[0]
f.close()
#Fin archivo


#Desde aqui se crea el archivo bulletin.asc (si no existe) con la información epicentral
#generada automáticamente. Así también se crea el archivo GMT para que introducir la 
#leyenda en el mapa.
#
#Verificando si el archivo bulletin.asc se encuentra vacio
num=os.stat("/opt/WebMap/bulletin.asc")[6]
if num == 0 :
#El archivo está vacio y se debe generar su header
	header="echo Date,TimeUTC,Latitude,Longitude,Magnitude,Depth > /opt/WebMap/bulletin.asc"
#Haciendo una llamada al sistema 
	os.system(header)
lati = round(lati,2)
longi = round(longi,2)
depth = round(depth,2)
ML = round(ML,1)
#Generando la linea para el archivo
event='echo '+fecha+','+hora+','+str(lati)+','+str(longi) +','+str(ML)+','+str(depth)+' >> /opt/WebMap/bulletin.asc'
#introduciendo la linea en el bulletin en la web con hora y fecha GMT
os.system(event)

#Generando la leyenda del boletin
f=open("/opt/GMT_OVSI/ovsi.legend","w")
f.write("H 10 1 Fecha: "+fechalocal[0]+",   Hora: "+horalocal[0]+",   Magnitud "+str(ML)+",   Profundidad: "+str(depth)+" km")
f.write("\n") 
#f.write("H 10 1 Ubicaci\\363n Geogr\\341fica"+"\n")

#f.write("END\n")
f.close()

#Header para el archivo temporal
header="echo Date,TimeUTC,Latitude,Longitude,Magnitude,Depth > /opt/GMT_OVSI/last_event.dat"
os.system(header)
#introduciendo la linea en el bulletin
os.system(event)
event='echo '+fechalocal[0]+','+horalocal[0]+','+str(lati)+','+str(longi) +','+str(ML)+','+str(depth)+' >> /opt/GMT_OVSI/last_event.dat'
#introduciendo la linea en el bulletin en la web con hora y fecha GMT
os.system(event)
#Ejecutando el script para actualizar el boletin
sGMT='sh /opt/GMT_OVSI/gmt_OVSICORI_localseismicity.gmt'
os.system(sGMT)
#Respaldo ultimo archivo
os.system('/opt/ProgramaEQ/respaldoimg.bash')
#THE END
