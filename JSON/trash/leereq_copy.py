#!/usr/bin/python

import os
import sys
import json
import math
import urllib2
import pprint
import string
import time
import MySQLdb
import MySQLdb.cursors
from string import split
import pytz, dateutil.parser
import urllib2
import subprocess


verbose = False
limpiar_db = True
mysql_db = 'eqs'
# Para obtener los datos del URL web use este metodo.
# import json
# import urllib2
# req = urllib2.Request("http://www.ovsicori.una.ac.cr/sistemas/imagenes/json/eventos.json")
# opener = urllib2.build_opener()
#
# Para buscarlos locales se usa ete metodo.
#req = '/opt/ProgramaEQ/JSON/mounted_arkham/eventos_mundial.json'
req = '/opt/ProgramaEQ/JSON/mounted_arkham/eventos.json'
f = open(req, 'r')
j = json.load(f)

#pprint.pprint(j)

# Connectart a MySQL
try:
    db = MySQLdb.connect (host = "10.10.128.10",user = "root",
            passwd ="RootMysql",db = "autoeq")
            #cursorclass = MySQLdb.cursors.SSCursor)
except Exception,e:
    if verbose: print "Problems looking for MySQL db: %s" % e
    sys.exit(1)


fields = ['evid', 'orid', 'longitud', 'latitud', 'magnitud','profundidad',
    'localizacion', 'codigo_user', 'origen', 'fechalocal',
    'horalocal', 'magtype','sdobs','reviewed','nass','ndef','time']


def do_sql(db,action,fields=[],data=[],where=''):

    results = []

    if action is 'UPDATE':
        cmd = 'UPDATE %s SET ' % mysql_db
        values = dict(zip(fields, data))
        for v in values:
            cmd += " %s='%s'," % ( v,values[v] ) 

        cmd = cmd[:-1]

        cmd += where
    else:
        if fields:
            f_string = ','.join( fields )
            #if verbose: print "f: %s" % f_string
            k = '%s' % f_string
        else:
            k = ''

        if data:
            d_string = ','.join( [ '"%s"' % x for x in data] )
            #if verbose: print "d: %s" % d_string
            v = 'VALUES (%s)' % d_string
            k = "(%s)" % k
        else:
            v = ''

        if k and v:
            cmd = "%s %s %s %s %s" % (action,mysql_db,k,v,where)
        else:
            cmd = "%s %s FROM %s %s" % (action,k,mysql_db,where)

    if verbose: print "%s" % cmd

    cur = db.cursor()

    cur.execute( cmd )

    if action is 'SELECT':
        rows = cur.fetchall()
        for row in rows:
            results.append( dict(zip(fields, row)) )
        if verbose: print "Got %s results." % len(results)

    else:
        db.commit()


    cur.close()
    
    return results

def notificar(action,ev,localizacion):

    hora = '%s' % ev['horaLocal']
    dia = '%s' % ev['diaLocal']
    evtime = float(ev['time'])
    lat = float(ev['lat'])
    lon = float(ev['lon'])
    try:
        mag = float(ev['magnitude'])
    except:
        mag = 0
    try:
        depth = float(ev['depth'])
    except:
        depth = '-'


    if ( ( time.time() - evtime) > 18000): #18000secs mas de 5 hrs
        print "\tNO NOTIFICATION EV TOO OLD: %s" % evtime
        return

    if (mag != '-' and mag < 2):
        print "\tNO NOTIFICATION LOW MAGNITUDE: %s" % mag 
        return

    if (lat >= 6.5 and lat <= 13.0):
        pass
    else:
        print "\tNO NOTIFICATION TOO FAR LAT: %s" % lat 
        return

    if ( lon >= -88.5 and lon <= -81.0):
        pass
    else:
        print "\tNO NOTIFICATION TOO FAR LON: %s" % lon
        return


    # epicentro
    sismo = "%s/%s/%s/%s/%s/%s/%s" % (dia, hora,
        mag, depth, lat, lon, localizacion) 

    print "EPICENTRO: [%s]" % sismo
    # Creando archivo feeder de los sismos
    os.system("sed '15 d' /opt/feed/feed.txt > /opt/feed/feed2.txt")
    os.system("mv /opt/feed/feed2.txt /opt/feed/feed.txt")

    with open("/opt/feed/feed.txt", "r+") as f:
        s = f.read();
        f.seek(0);
        f.write(sismo +"/A\n" + s)

    url = "http://www.intraovsi.una.ac.cr/movilnotification/notification_sender.php?pushMessage="
    url += sismo
    urllib2.urlopen(url)

    # twitter
    twitter = "%s: %s/%s MAG: %s %s PROF:%skm / %s" % (action, dia, hora,
            mag,ev['magtype'], depth, localizacion)
    twitter = twitter[0:139]
    print "TWITER: [%s]" % twitter
    os.system('ttytter -status="'+ twitter +'"')


    # SMS
    if depth != '-' and mag != '-' and mag >= 3 and depth < 100:
        url = 'http://www.intraovsi.una.ac.cr/SMS/enviaGUARDIA.php?'
        url += "fecha=%s&hora=%s&mag=%s&prof=%s&latitud=%s&longitud=%s&local=%s" % \
            (dia,hora,mag,depth,lat,lon,localizacion)
        url = url.replace(' ',';')

        print "SMS: [%s]" % url
        urllib2.urlopen( url ) 
    else:
        print "SMS: Not sending to SMS"


def calcular_cardinal(baz): # Obtener punto cardinal
    if baz > 350 or baz <= 10:
        return 'Norte'
    elif baz > 10 and baz <= 80:
        return 'Noreste'
    elif baz > 80 and baz <= 100:
        return 'Este'
    elif baz > 100 and baz <= 170:
        return 'Sureste'
    elif baz > 170 and baz <= 190:
        return 'Sur'
    elif baz > 190 and baz <= 260:
        return 'Suroeste'
    elif baz > 260 and baz <= 280:
        return 'Oeste'
    elif baz > 280 and baz <= 350:
        return 'Noroeste'
    return ' -?- '


if limpiar_db:
    if verbose: print "Remover todos los eventos con evid=NULL"
    # Remover entradas erroneas en el db
    do_sql(db,'DELETE',where='WHERE evid=-1')


for ev in j.keys():

    event = j[ev]

    cardinal =  calcular_cardinal( event['acimut'] )
    localizacion = event['distancia'] + ' km al ' + \
            cardinal +' de '+ event['pueblo'] + ' de ' + \
            event['canton'] + ' de ' + event['provincia']

    data = [event['evid'], event['orid'], event['lon'], event['lat'], event['magnitude'],
            event['depth'],localizacion, event['auth'], 'unknown type', event['diaLocal'],
            event['horaLocal'], event['magtype'], event['sdobs'],event['review'],
            event['nass'], event['ndef'],event['time'] ]


    if verbose: print "\n\nEvento: %s" % event['evid']

    resultados = do_sql(db,'SELECT',fields,where='WHERE evid=%s' % event['evid'])

    try:
        total = len(resultados)
    except:
        total = 0

    if total == 1:
        # Verificar si tenemos un update.
        if resultados[0]['orid'] == event['orid']:
            if verbose: print "\tSame event already in db"
        else:
            print "\tUpdate to event %s" % event['evid']
            if verbose: print "\t\tORID new: %s" % event['orid']
            if verbose: print "\t\tORID old: %s" % resultados[0]['orid']
            do_sql(db,'UPDATE',fields,data,where='WHERE evid=%s' % event['evid'])
            notificar('UPDATE',event,localizacion)

        continue

    if total > 1:
        if verbose: print "\tMore than one in db:"
        for orid in resultados:
            if verbose: print "\t\tORID: %s" % orid['orid']
        # ALL OF THEM
        do_sql(db,'DELETE',where='WHERE evid=%s' % event['evid'])
             
    print "\tInsert ivent: %s" %  event['evid']
    do_sql(db,'INSERT INTO',fields,data)
    
    notificar('PRE',event,localizacion)


    emailb = 2
    upd = 1

# Verify DB
#if verbose: print "\nLimpiar el DB de evid=-1 "
#do_sql(db,'SELECT',fields,where='WHERE evid=-1')
#do_sql(db,'DELETE',where='WHERE magnitud > 1')

db.close()
