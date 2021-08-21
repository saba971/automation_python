#!/usr/bin/python

import MySQLdb
import re
import os
import datetime
import os, sys
import urllib2
import urllib
import paramiko
import requests

from datetime import datetime, timedelta
import urllib
dict_mapping={}

db_stage=sys.argv[3]

jenkins_ip="135.249.27.140"
jname=sys.argv[1]
print jname
stage_name=sys.argv[2]
print stage_name
apme_cs=""
robot_cs=""
apme_exists=""
robot_exists=""

db = MySQLdb.connect("localhost","root","alcatel01","pipeline_db")
cursor = db.cursor()

url="http://%s:8080/job/%s/lastBuild/api/python?pretty=true"%(jenkins_ip,jname)
print url
fRead = eval(urllib.urlopen(url).read())
console = fRead["number"]
#console=1631
print jname
print console

burl="http://%s:8080/job/%s/%s/api/python" %(jenkins_ip,jname,console)
print burl




jsonResponse1 = eval(urllib.urlopen(burl).read())
for i in range (0,len(jsonResponse1["actions"])):
	if 'parameters' in jsonResponse1["actions"][i]:
		for j in range (0,len(jsonResponse1["actions"][i]["parameters"])):		
			if jsonResponse1["actions"][i]["parameters"][j]["name"] == "BUILD" :
				build_tar=jsonResponse1["actions"][i]["parameters"][j]["value"]
				break

print build_tar
nbuild=re.search('(.*)_(.*).tar',build_tar)
jbuild=nbuild.group(2)
total_build=jsonResponse1["displayName"]
print total_build
total_build=total_build.rstrip()
nbuild1=total_build.split(" ")
abuild=nbuild1[0]
print abuild
if len(nbuild1) == 1:
	print "Not a rerun"
	jrerun="default"
else:
	rbuild=nbuild1[1]
	if rbuild == "RERUN":
		jrerun="RERUN"



console_log_url="http://%s:8080/job/%s/%s/consoleText"%(jenkins_ip,jname,console)
print console_log_url
console_log=urllib2.Request(console_log_url)
response = urllib2.urlopen(console_log)
response_text=response.read()
response_text=response_text.split("\n")
for k in range (len(response_text)-1,-1,-1):
	download_stage=re.search(r'Starting building: ' + stage_name + ' #(.*)',response_text[k])	
	if download_stage:
		print download_stage.group()

		download_stage_url="http://" + jenkins_ip + ":8080/job/" +stage_name + "/" + download_stage.group(1)
		cs_url=download_stage_url+"/consoleText"
		print cs_url
		cs_url_response=urllib.urlopen(cs_url)
		cs_url_response=cs_url_response.read()
		cs_url_response=cs_url_response.split("\n")
#CS info can be fetched from above url
###############################################################################################CS INFO FETCH
		for i in cs_url_response:
			apme_url=re.search(r'cat ((.*)/(.*))/testsummary.log',i)
			#from the contents of post_ltb job , below log path can be known.
			#If Instant status.html is present,APME framework is used
			if apme_url:
				print "Storage_log_url  :  /storage/%s"%apme_url.group(1)

				if os.path.isfile("/storage/%s/InstantStatus.html"%apme_url.group(1)):
					apme_exists="APME"
					print apme_exists
			x=re.search(r'APME CS Version: (.*)',i)
			if x:
					print x.group()
					if apme_exists=="APME":
						print "fgr-It's apme"
						apme_cs=x.group(1)
						break
					else:
						print "ewge"
						apme_cs="-"
                for i in cs_url_response:
                        apme_url=re.search(r'cat ((.*)/(.*))/testsummary.log',i)
                        if apme_url:
                                print "Storage_log_url  :  /storage/%s"%apme_url.group(1)
				#If TEST.html is present,ROBOT framework is used.
                                if os.path.isfile("/storage/%s/ROBOT/TEST_CASE.txt"%apme_url.group(1)):
                                        robot_exists="ROBOT"
                        y=re.search(r'ROBOT CS   : (.*)',i)
                        if y:
				print i
                                if robot_exists=="ROBOT":
					print"fgr-It's robot"
                                        robot_cs=y.group(1)

                                        break
                                else:
                                        robot_cs="-"
                                        break

		print apme_cs					
		print robot_cs		
		print download_stage_url
		
		duration_link=eval(urllib.urlopen(download_stage_url+ "/api/python").read())
		end_duration= duration_link["duration"]  
		print end_duration
		timestamp= duration_link["timestamp"]
		break



##############################################################################################################CS_INFO_FETCH

jstime = datetime.fromtimestamp(timestamp/1000)

##########end_time############

jetime = jstime + timedelta(seconds=end_duration/1000)
print jetime
print " gfshghr"

jobStatus=eval(urllib.urlopen(download_stage_url + "/api/python").read())
jobStatus=jobStatus["result"]
print "jobStatus"
print jobStatus
if jobStatus == "SUCCESS":
	jstatus = "PASS"
elif jobStatus == "FAILURE" or jobStatus == "ABORTED":
	jstatus = "FAIL"



f=open("mappings.txt","r")
g=f.read()
g=g.split("\n")
for i in g:
        i=i.split(":")
        if len(i) == 2:
                dict_mapping[i[0]]=i[1]


cursor.execute("select MAX(s_no) FROM %s"%db_stage)
row = cursor.fetchone()
jid = row[0]
jid = jid + 1
print jname
print jbuild
print jstime
print jetime
print jstatus
print jrerun
print jetime-jstime

if jname[:-3] in dict_mapping.keys():
	db_name=dict_mapping[jname[:-3]]
else:
	db_name="DB_name_missing_%s"%jname[:-3]
print db_name
if jbuild == abuild:
        try:
                cursor.execute("insert into %s VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s')" %(db_stage,jid, jname, jbuild, jstime, jetime, jstatus, jrerun,db_name,apme_cs,robot_cs))
                db.commit()
        except MySQLdb.Error, e:
                print(e)
else:
	print "This is not official proposal build but might be CS run or testrun.Hence inserting update ID in build column for DB operation"
        try:
                cursor.execute("insert into %s VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s')" %(db_stage,jid, jname, abuild, jstime, jetime, jstatus, jrerun,db_name,apme_cs,robot_cs))
                db.commit()
        except MySQLdb.Error, e:
                 print(e)



