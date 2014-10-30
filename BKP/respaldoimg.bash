#!/bin/bash
_hoy=$(date +"%d_%m_%Y_%H:%M:%S")
#_inicio=$(date --date="-3 month" +"%d_%m_%Y")
cp /opt/WebMap/last_event.jpg /opt/bkp/WebMap/last_event$_hoy".jpg"
