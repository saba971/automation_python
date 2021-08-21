#!/usr/bin/python

import MySQLdb
import re
import os
import datetime
import os, sys
import urllib2
import urllib
import paramiko

platform_name=os.environ["PIPELINE_NAME"]
isam_ip=os.environ["ISAM_IP"]
build=os.environ["BUILD"]
print "ISAM_IP  %s"%isam_ip
db_stage="build_preparation"

jenkins_ip="135.249.31.94"
jname=os.environ['PIPELINE_NAME']
print jname
stage_name=os.environ['STAGE_NAME']
print stage_name

ssh_client =paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(jenkins_ip,username="atxuser",password="alcatel01")  
channel = ssh_client.invoke_shell()


cmd1="cd jenkins_datbase_scripts;python %s.py %s %s %s"%(db_stage,jname,stage_name,db_stage)
channel = ssh_client.invoke_shell()
stdin = channel.makefile('wb')
stdout = channel.makefile('rb')

stdin.write(cmd1+"\n")
stdin.write('exit\n')
result= stdout.read()
print result
stdout.close()
stdin.close()
ssh_client.close()

url="%sapi/python"%os.environ['BUILD_URL']
print url
stage_name_check= eval(urllib.urlopen(url).read())
print "check"
              
for i in range(0,len(stage_name_check["actions"])):
                             print i
                             if stage_name_check["actions"][i]["_class"] == "hudson.model.CauseAction" :
								stage_name_upstreamProject=stage_name_check["actions"][i]["causes"][0]["upstreamProject"]
								stage_name_upstreamBuild=stage_name_check["actions"][i]["causes"][0]["upstreamBuild"]
								break
print stage_name_upstreamProject
print stage_name_upstreamBuild

upstream_url="%sjob/%s/%s"%(os.environ["JENKINS_URL"],stage_name_upstreamProject,stage_name_upstreamBuild)
print upstream_url
upstream_url_check=eval(urllib.urlopen(upstream_url + "/api/python").read())
print " hewlooelwoe"
print upstream_url_check["result"]
if upstream_url_check["result"] == "SUCCESS":

	ssh_client =paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect("10.182.198.209",username="root",password="T&Dfndpc#123")  
	channel = ssh_client.invoke_shell()
	
	cmd2="cd /root/saba/;python test.py %s %s %s"%(isam_ip,build,platform_name)
	channel = ssh_client.invoke_shell()
	stdin = channel.makefile('wb')
	stdout = channel.makefile('rb')

	stdin.write(cmd2+"\n")
	stdin.write('exit\n')
	result= stdout.read()


	print result
else:
	print "Build preparation failed.So not starting GICI process."

stdout.close()
stdin.close()
ssh_client.close()




Code to add in jenkins :


platform_name=os.environ["PIPELINE_NAME"]
isam_ip=os.environ["ISAM_IP"]
build=os.environ["BUILD"]
print "ISAM_IP  %s"%isam_ip
db_stage="build_preparation"

jenkins_ip="135.249.27.140"
jname=os.environ['PIPELINE_NAME']
print jname
stage_name=os.environ['STAGE_NAME']
print stage_name



upstream_url="%sjob/%s/%s"%(os.environ["JENKINS_URL"],stage_name_upstreamProject,stage_name_upstreamBuild)
print upstream_url
upstream_url_check=eval(urllib.urlopen(upstream_url + "/api/python").read())
print " hewlooelwoe"
print upstream_url_check["result"]
if upstream_url_check["result"] == "SUCCESS":

	ssh_client =paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect("10.182.198.209",username="root",password="T&Dfndpc#123")  
	channel = ssh_client.invoke_shell()
	
	cmd2="cd /root/saba/;python test.py %s %s %s"%(isam_ip,build,platform_name)
	channel = ssh_client.invoke_shell()
	stdin = channel.makefile('wb')
	stdout = channel.makefile('rb')

	stdin.write(cmd2+"\n")
	stdin.write('exit\n')
	result= stdout.read()




Kill process:






platform_name=os.environ["PIPELINE_NAME"]
isam_ip=os.environ["ISAM_IP"]
build=os.environ["BUILD"]
print "ISAM_IP  %s"%isam_ip
db_stage="build_preparation"

jenkins_ip="135.249.27.140"
jname=os.environ['PIPELINE_NAME']
print jname
stage_name=os.environ['STAGE_NAME']
print stage_name



upstream_url="%sjob/%s/%s"%(os.environ["JENKINS_URL"],stage_name_upstreamProject,stage_name_upstreamBuild)
print upstream_url
upstream_url_check=eval(urllib.urlopen(upstream_url + "/api/python").read())
print " hewlooelwoe"
print upstream_url_check["result"]
if upstream_url_check["result"] == "SUCCESS":

	ssh_client =paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect("10.182.198.209",username="root",password="T&Dfndpc#123")  
	channel = ssh_client.invoke_shell()
	
	cmd2="cd /root/saba/;python testk.py %s %s %s"%(isam_ip,build,platform_name)
	channel = ssh_client.invoke_shell()
	stdin = channel.makefile('wb')
	stdout = channel.makefile('rb')

	stdin.write(cmd2+"\n")
	stdin.write('exit\n')
	result= stdout.read()






#Gici script:

platform_name=os.environ["PIPELINE_NAME"]
isam_ip=os.environ["ISAM_IP"]
build=os.environ["BUILD"]
print "ISAM_IP  %s"%isam_ip
db_stage="build_preparation"

jenkins_ip="135.249.27.140"
jname=os.environ['PIPELINE_NAME']
print jname
stage_name=os.environ['STAGE_NAME']
print stage_name

url="%sapi/python"%os.environ['BUILD_URL']
print url
stage_name_check= eval(urllib.urlopen(url).read())
print "check"
	
for i in range(0,len(stage_name_check["actions"])):
		print i
		if stage_name_check["actions"][i]["_class"] == "hudson.model.CauseAction" :
			stage_name_upstreamProject=stage_name_check["actions"][i]["causes"][0]["upstreamProject"]
			stage_name_upstreamBuild=stage_name_check["actions"][i]["causes"][0]["upstreamBuild"]
			break
print stage_name_upstreamProject
print stage_name_upstreamBuild

upstream_url="%sjob/%s/%s"%(os.environ["JENKINS_URL"],stage_name_upstreamProject,stage_name_upstreamBuild)
print upstream_url
upstream_url_check=eval(urllib.urlopen(upstream_url + "/api/python").read())
print " hewlooelwoe"
print upstream_url_check["result"]
if upstream_url_check["result"] == "SUCCESS":

	ssh_client =paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect("10.182.198.209",username="root",password="T&Dfndpc#123")  
	channel = ssh_client.invoke_shell()
	
	cmd2="cd /root/saba/;python test.py %s %s %s"%(isam_ip,build,platform_name)
	channel = ssh_client.invoke_shell()
	stdin = channel.makefile('wb')
	stdout = channel.makefile('rb')

	stdin.write(cmd2+"\n")
	stdin.write('exit\n')
	result= stdout.read()
    
    
    
    #Gici Script

platform_name=os.environ["PIPELINE_NAME"]
isam_ip=os.environ["ISAM_IP"]
build=os.environ["BUILD"]
print "ISAM_IP  %s"%isam_ip
db_stage="build_preparation"

jenkins_ip="135.249.27.140"
jname=os.environ['PIPELINE_NAME']
print jname
stage_name=os.environ['STAGE_NAME']
print stage_name




url="%sapi/python"%os.environ['BUILD_URL']
print url
stage_name_check= eval(urllib.urlopen(url).read())
print "check"
	
for i in range(0,len(stage_name_check["actions"])):
		print i
		if stage_name_check["actions"][i]["_class"] == "hudson.model.CauseAction" :
			stage_name_upstreamProject=stage_name_check["actions"][i]["causes"][0]["upstreamProject"]
			stage_name_upstreamBuild=stage_name_check["actions"][i]["causes"][0]["upstreamBuild"]
			break
print stage_name_upstreamProject
print stage_name_upstreamBuild


upstream_url="%sjob/%s/%s"%(os.environ["JENKINS_URL"],stage_name_upstreamProject,stage_name_upstreamBuild)
print upstream_url
upstream_url_check=eval(urllib.urlopen(upstream_url + "/api/python").read())
print " hewlooelwoe"
print upstream_url_check["result"]
if upstream_url_check["result"] == "SUCCESS" or upstream_url_check["result"] == "FAILURE" :

	ssh_client =paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect("10.182.198.209",username="root",password="T&Dfndpc#123")  
	channel = ssh_client.invoke_shell()
	
	cmd2="cd /root/saba/;python testk.py %s %s %s"%(isam_ip,build,platform_name)
	channel = ssh_client.invoke_shell()
	stdin = channel.makefile('wb')
	stdout = channel.makefile('rb') 

	stdin.write(cmd2+"\n")
	stdin.write('exit\n')
	result= stdout.read()
    
    
    
    
    
    
    
    
    
Codes to be added in jenkins:

Download code:

#Gici script

print"Executing gici script"

platform_name=os.environ["PIPELINE_NAME"]
isam_ip=os.environ["ISAM_IP"]
build=os.environ["BUILD"]
print "ISAM_IP  %s"%isam_ip
db_stage="build_preparation"

jenkins_ip="135.249.27.140"
jname=os.environ['PIPELINE_NAME']
print jname
stage_name=os.environ['STAGE_NAME']
print stage_name

url="%sapi/python"%os.environ['BUILD_URL']
print url
stage_name_check= eval(urllib.urlopen(url).read())
print "check"
	
for i in range(0,len(stage_name_check["actions"])):
		print i
		if stage_name_check["actions"][i]["_class"] == "hudson.model.CauseAction" :
			stage_name_upstreamProject=stage_name_check["actions"][i]["causes"][0]["upstreamProject"]
			stage_name_upstreamBuild=stage_name_check["actions"][i]["causes"][0]["upstreamBuild"]
			break
print stage_name_upstreamProject
print stage_name_upstreamBuild

upstream_url="%sjob/%s/%s"%(os.environ["JENKINS_URL"],stage_name_upstreamProject,stage_name_upstreamBuild)
print upstream_url
upstream_url_check=eval(urllib.urlopen(upstream_url + "/api/python").read())
print " hewlooelwoe"
print upstream_url_check["result"]
if upstream_url_check["result"] == "SUCCESS":

	ssh_client =paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect("10.182.198.209",username="root",password="T&Dfndpc#123")  
	channel = ssh_client.invoke_shell()
	
	cmd2="cd /root/saba/;python test.py %s %s %s"%(isam_ip,build,platform_name)
	channel = ssh_client.invoke_shell()
	stdin = channel.makefile('wb')
	stdout = channel.makefile('rb')

	stdin.write(cmd2+"\n")
	stdin.write('exit\n')
	result= stdout.read()
    
Activation code:


#Gici Script

print"Executing gici script"

platform_name=os.environ["PIPELINE_NAME"]
isam_ip=os.environ["ISAM_IP"]
build=os.environ["BUILD"]
print "ISAM_IP  %s"%isam_ip
db_stage="build_preparation"

jenkins_ip="135.249.27.140"
jname=os.environ['PIPELINE_NAME']
print jname
stage_name=os.environ['STAGE_NAME']
print stage_name




url="%sapi/python"%os.environ['BUILD_URL']
print url
stage_name_check= eval(urllib.urlopen(url).read())
print "check"
	
for i in range(0,len(stage_name_check["actions"])):
		print i
		if stage_name_check["actions"][i]["_class"] == "hudson.model.CauseAction" :
			stage_name_upstreamProject=stage_name_check["actions"][i]["causes"][0]["upstreamProject"]
			stage_name_upstreamBuild=stage_name_check["actions"][i]["causes"][0]["upstreamBuild"]
			break
print stage_name_upstreamProject
print stage_name_upstreamBuild


upstream_url="%sjob/%s/%s"%(os.environ["JENKINS_URL"],stage_name_upstreamProject,stage_name_upstreamBuild)
print upstream_url
upstream_url_check=eval(urllib.urlopen(upstream_url + "/api/python").read())
print " hewlooelwoe"
print upstream_url_check["result"]
if upstream_url_check["result"] == "SUCCESS" or upstream_url_check["result"] == "FAILURE" :

	ssh_client =paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect("10.182.198.209",username="root",password="T&Dfndpc#123")  
	channel = ssh_client.invoke_shell()
	
	cmd2="cd /root/saba/;python testk.py %s %s %s"%(isam_ip,build,platform_name)
	channel = ssh_client.invoke_shell()
	stdin = channel.makefile('wb')
	stdout = channel.makefile('rb') 

	stdin.write(cmd2+"\n")
	stdin.write('exit\n')
    result= stdout.read()
