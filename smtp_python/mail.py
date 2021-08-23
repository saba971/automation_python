#!/usr/bin/python
import re
import os
import commands
import urllib
import smtplib
import subprocess
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#def prRed(skk):
	#return ("\033[91m {}\033[00m" .format(skk))
#TRED =  '\033[31m'
def FRnotificationemail():

        SERVER = "localhost"
#        TO = ['vijaya_ganesh.m@nokia.com','umapathy.gajendran@nokia.com','arun_kumar.deena_dayalan@nokia.com','kannan.govindaraju@nokia.com']
        #TO = ['umapathy.gajendran@nokia.com','arun_kumar.deena_dayalan@nokia.com','kannan.govindaraju@nokia.com']
	TO=['kannan.govindaraju@nokia.com','sabanayagam.thambaranathan@nokia.com']
	#TO=['sabanayagam.thambaranathan@nokia.com']
#       TO = ['umapathy.gajendran@nokia.com']
        #FROM = "umapathy.gajendran@nokia.com"
	FROM="kannan.govindaraju@nokia.com"
	#FROM="sabanayagam.thambaranathan@nokia.com"
        SUBJECT = "Gentle Reminder on Weekly Regression Slot Request Details"
	html ="""<html>
  		<head><font color="red">Gentle Reminder on Weekly Regression Slot Request Details</font></head>
	</html>"""
	#SUBJECT=prRed(SUBJECT)
	#SUBJECT = MIMEText(html, 'html')
        TEXT = "Hi"
        TEXT0 = "\n"
        TEXT1 = "Please check for RLAB Weekly Regression Slot Request Details.\n"
        TEXT2 = ""
        TEXT3 = ""
        TEXT4 = "Regards"
        TEXT5 = "RemoteLab"


        message = """\
From: %s
To: %s
Subject: %s

%s
%s
%s
%s
%s
%s
%s
        """ % (FROM, ", ".join(TO),SUBJECT, TEXT,TEXT0,TEXT1,TEXT2,TEXT3,TEXT4,TEXT5)
        server = smtplib.SMTP(SERVER)
        server.sendmail(FROM, TO, message)
        server.quit()
out1=FRnotificationemail()

