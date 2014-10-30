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

subprocess.call('/opt/ProgramaEQ/leereqmapa.py')


