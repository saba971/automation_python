#!/usr/bin/python
import cgi, cgitb ,sys
import commands
import os
import re
import ctypes
from decimal import Decimal
#import pymysql
#pymysql.install_as_MySQLdb()
import MySQLdb
import urllib
import math
import datetime
from datetime import date, timedelta
lst1=[]
lst2=[]
lst3=[]
lst4=[]
lst5=[]
lst6=[]
#mysql db connection---------------------------------------------------------->
db = MySQLdb.connect("localhost","root","bgc8g343437","sabadb")
cursor = db.cursor()
# prepare a cursor object using cursor() method
cursor = db.cursor()
#End--------------------------------------------------------------------------------->
#Form getting value---------------------------------------------------------------------------->
form = cgi.FieldStorage()
date = form.getvalue('date')
date1=date
#date1="30-09-2019"
#End---------------------------------------------------------------------------->
#Database Collecting Value-------------------------------------------------------------->
sm1_det="select builds from tgraph where date='%s'"%date1
#print(sm1_det)
cursor.execute(sm1_det)
row=cursor.fetchall()
for i in row:
	lst1.append(i)
#print(lst1)
sm2_det="select tot_time from tgraph where date='%s'"%date1
cursor.execute(sm2_det)
row=cursor.fetchall()
for i in row:
        lst2.append(i)
#print(lst2)
#date2=str(lst1[0])
#print(date)
def convertTuple(tup): 
    str =  ''.join(tup) 
    return str
for i in range(0,len(lst1)):
	str = convertTuple(lst1[i])
	lst3.append(str)
for i in range(0,len(lst2)):
        str = convertTuple(lst2[i])
        lst4.append(str)
#print(lst3)
#print(lst4)
for i in range(0,len(lst3)):
	m=lst3[i]+":"+lst4[i]
	lst5.append(m)
#print(lst5)
#Format for Highchart----------------------------------------->
concatstr4=""
for i in lst5:
        disp3=i.split(":")[0]
        l2=i.split(":")[1]
        concatstr4 = concatstr4 + "{ y: "+l2+", label :'"+ disp3 +"'},"
concatstr4=concatstr4[:-1]
concatstr4=concatstr4
#print("concatstr4"+concatstr4)
#End--------------------------------------------------------------------->
#printing Html Content---------------------------------------------------------------------------------->
print "Content-type:text/html\r\n\r\n"
print "<html>"
#print "<center><head><u>Proposal Completion TIME</u></head></center>"
#print "<style> #topcornerlogin{position:absolute;right:20px;top:20px;}</style>"
#print "<center><table border=5>"
#print "<thead 'bgcolor='red'>"
#print "<center>DATE: %s</center>"% (date)
print'''<body bgcolor="#E6E6FA">'''
print '''<center><h3 style="background-color:#3cb371;">Proposal completion Time</h3></center>\n'''
print "    <hr />\n"
print "    <center><table border color \"blue\" bgcolor=\"white\" border=2>\n"
print "    <tr><td  height='30'><center><b>Builds</center></td><td><center><b>Time</center></td></tr>"
for i in lst5:
	disp1=i.split(":")[0]
	disp2=i.split(":")[1]
	print "    <tr><td height='30' ><center>&nbsp%s&nbsp</center></td> <td ><center>&nbsp%s&nbsp</center></td></tr>\n"%(disp1,disp2)
print "    </table></center>\n"
print "</body>"
print "</html>"
#for line in :
#print "<center>DATE: %s</center>"% (date1)
#print "<center>DATE: %s</center>"% (date2)
#print"<center><head><u>%s</u></head></center>"% (lst1[1])
#print'''<!DOCTYPE HTML><html><head>  <script>window.onload = function () {var chart = new CanvasJS.Chart("chartContainer", {animationEnabled: true,title:{text:"Build Completion Time"},axisX:{interval: 1},axisY2:{interlacedColor: "rgba(1,77,101,.2)",gridColor: "rgba(1,77,101,.1)",title: "Time"},data: [{type: "bar",name: "companies",axisYType: "secondary",color: "#014D65",dataPoints: [{ y: 1.51, label :'6201.241p01'},{ y: 1.58, label :'6201.240p17'},{ y: 1.55, label :'6201.240p16'},{ y: 1.58, label :'6201.240p15'},{ y: 1.43, label :'6201.240p14'}]}]});chart.render();}</script></head><body><div id="chartContainer" style="height: 300px; width: 100%;"></div><script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script></body></html>'''
print"<!DOCTYPE HTML><html><head>  <script>window.onload = function () {var chart = new CanvasJS.Chart(\"chartContainer\", {animationEnabled: true,title:{text:\"Graphical View\"},axisX:{interval: 1},axisY2:{interlacedColor: \"rgba(1,77,101,.2)\",gridColor: \"rgba(1,77,101,.1)\",title: \"Time\"},data: [{type: \"bar\",name: \"companies\",axisYType: \"secondary\",color: \"#014D65\",dataPoints: ["+concatstr4+"]}]});chart.render();}</script></head><body><div id=\"chartContainer\" style=\"height: 300px; width: 100%;\"></div><script src=\"https://canvasjs.com/assets/script/canvasjs.min.js\"></script></body></html>"
