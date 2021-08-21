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
gici_logname=[]

#isam_ip="135.249.25.242"

#isam_ip=os.environ['ISAM_IP']

cwd = os.getcwd()

platform_name=sys.argv[3]
isam_ip=sys.argv[1]
print isam_ip
build=sys.argv[2]
timestamp=time.strftime('%b%d%H%M%S',time.localtime())

#tracelog=platform_name+"_"+build+"_"+isam_ip+"_"+timestamp

#print tracelog

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


#Getting the craft detail from the text file
try:
        out1=connect('10.182.198.209','cat %s/sam.txt'%cwd)
        for line in out1:
                if isam_ip in line:
			line=line.split(";")
			print "Checking Number of CRAFT IP's"
			print len(line)
			if len(line) == 6:
				print "Only one craft IP"
				list.append("%s:%s:%s"%(line[2],line[3],line[4]))
			elif len(line) > 6 :
				print "Two craft IP"
				list.append("%s:%s:%s"%(line[2],line[3],line[4]))
				list.append("%s:%s:%s"%(line[5],line[6],line[7]))
except Exception as e:
    print e
"""
print("craftIp:"+craftIp)
print("craftPort:"+craftPort)
print("duttype:"+duttype)
"""
#getting the logfile name using grep and split
try:
	for i in list:
		i=i.split(":")
		cmd2="ps -aef | grep traceSaver2.py | grep %s | grep %s"%(i[0],i[1])
		out6=connect("10.182.198.209",cmd2)
		print(out6)
		for liner2 in out6:
			print(liner2)
			gici_logname.append(liner2.split("LOG_FILE ")[1].split(" --")[0])
			#print("gici_logname:"+gici_logname)
			break

except Exception as e:
	print e

print("gici_logname:")
print gici_logname

count=0

#finding the correct process id and killing the process
try:
	for i in list:
		i=i.split(":")
		cmd1="ps -aef | grep traceSaver2.py | grep %s | grep %s | grep -v defunct | grep -v grep | awk '{print $2}'"%(i[0],i[1])
		out3=connect("10.182.198.209",cmd1)
		if len(out3)==0:
        		print("Gici_Process is not started")
		else:
    			print("Gici_Process is started")
    			for line3 in out3:
        			print(line3)
    				cmd4='kill -9 '+line3+''
    				print(cmd4)
    				out4=connect('10.182.198.209',cmd4)
    				out5=connect('10.182.198.209',cmd1)
        	    		if len(out5)==0:
					count=1
                			print("Process is killed")
            			else:
                			print("Process is not  killed")    
                    
except Exception as e:
    print e



#moving the file to the required path    
if(count==1):
	for i in gici_logname:
	
		if os.path.exists("%s/logs/%s"%(cwd,platform_name)):
			os.system("mv /root/%s %s/logs/%s"%(i,cwd,platform_name))    
			print("File is moved") 
		else:
			os.system("mkdir %s/logs/%s"%(cwd,platform_name))
			os.system("mv /root/%s %s/logs/%s"%(i,cwd,platform_name))
			print("File is moved")

else:
	print("File is not moved")
    


