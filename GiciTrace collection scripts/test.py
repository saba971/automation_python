import re
import time
import datetime
import paramiko
import os
import os.path
import commands
import shutil
import MySQLdb
import urllib2
import urllib
import sys
list1=[]


list=[]
from datetime import datetime


cwd = os.getcwd()

platform_name=sys.argv[3]
isam_ip=sys.argv[1]
build=sys.argv[2]
#isam_ip="135.249.25.242"

#os.environ['GICI_check']
#a=os.environ['GICI_check']
#isam_ip=os.environ['ISAM_IP']

print "PLATFORM_NAME :   %s"%platform_name
print("isam_ip:"+isam_ip)

timestamp=time.strftime('%b%d%H%M%S',time.localtime())

tracelog=platform_name+"_"+build+"_"+isam_ip+"_"+str(timestamp)

#tracelog="/home_local/ladmin/saba/"+tracelog

print("tracelog:"+tracelog)

#ISAM_IP

def connect(atxserver,cmd1):
        try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(atxserver, port=22 ,username='root',password='T&Dfndpc#123')
                stdin, stdout, stderr = ssh.exec_command(cmd1)
                output1 = stdout.readlines()
                return output1
        except Exception,e:
                print str(e)
                print "         "+atxserver +' is not Reachable'+"\n"


#Getting craft details from the text using isam_ip
try:
        out1=connect('10.182.198.209','cat %s/sam.txt'%cwd)
        for line in out1:
                if isam_ip in line:
			line=line.split(";")
			print "Checking Number of CRAFT IP's"
			print len(line)
			if len(line) ==6 :
				print "One Craft IP"
				list.append("%s:%s:%s"%(line[2],line[3],line[4]))
			elif len(line) >6  :
				print "Two Craft IP's"
				list.append("%s:%s:%s"%(line[2],line[3],line[4]))
				list.append("%s:%s:%s"%(line[5],line[6],line[7]))

except Exception as e:
    print e
"""
print("craftIp:"+craftIp)
print("craftPort:"+craftPort)
print("dut_type:"+dut_type)
"""
#Starting the process using nohup command

print list

try:
	for i in list:
		
		i=i.split(":")
		print i
		tracelog=platform_name+"_"+build+"_"+isam_ip+"_"+str(timestamp)+"_"+i[0]+"_"+i[1]			
	        cmd = "nohup python -u %s/traceSaver2.py --craftIp %s --craftPort %s --LOG_FILE %s --storeInterval 9999  --dut_type %s  >/dev/null 2>&1 &"%(cwd,i[0],i[1],tracelog,i[2])
        	print(cmd)
        	out2=connect('10.182.198.209',cmd)
		print "Out2"
		print out2
		time.sleep(2)
        	for line2 in out2:
        		print " Line2\n" 
			print  line2
except Exception as e:
    print e


#cmd1 is to get the processid 

cmd1="ps -aef | grep traceSaver2.py | grep %s"%(isam_ip)

print(cmd1)

out3=connect("10.182.198.209",cmd1)

count=1

if len(out3)==0:
	count=0
	print(count)
	print("Gici_Process is not started")
else:
	print(out3)
	print("Gici_Process is started successfully")
    
		


try:
    jid=0
    que="SELECT MAX(id)from smoke_stat"
    cursor.execute(que)
    row=cursor.fetchone()
    jid=row[0]
    jid=jid+1
    print(jid)
    print(line[1])
    print(line[0])
    queu=cursor.execute("select platform from smoke_stat where `load` = '%s' and `platform` = '%s'" %(line[1],line[0]))
    row=cursor.fetchall()
    print(queu)
except Exception as e:
    print(e)


135.249.38.206:atxuser:alcatel01:/root/PCTA/pcta.exe
135.249.38.219
135.249.38.207:atxuser:alcatel01:/root/PCTA/pcta.exe


