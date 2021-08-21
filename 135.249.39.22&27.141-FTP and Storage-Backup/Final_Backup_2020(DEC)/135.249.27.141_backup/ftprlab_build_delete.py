import os,commands,datetime,re
#MAILNLY PROVIDE WRITE PERMISSIONS TO THE FILES MENTIONED IN THIS SCRIPT
#This script is executed every two hours and is responsible for maintaing space in /ftpserver/RLAB
#fetches daily builds older than 14 days and appends to the below file
#------------------------------------------------------------------------------------->
#For All builds deletion
status, output = commands.getstatusoutput("find /ftpserver/RLAB/*tar -mtime +14")
#print(output)
f = open("ftpserver_RLAB_deleted_files.txt", "a+")
f.write(output)
time=datetime.datetime.now()
time=str(time)
f.write("\n\n")
f.write(time)
f.write("\n\n\n\n\n\n")
#os.system("find /ftpserver/RLAB/*tar -mtime +7 -exec rm {} \;")
#deletes the builds mentioned in above file one by one
output=output.split("\n")
print("Deleting Builds older than 14 days---------->")
for i in output:
	print(i)
	os.system("rm -f %s"%i)
#---------------------------------------------------------------------------------------->
#This below block is for deleting smoke proposals alone.
#below command fetches smoke builds older than a day (if space issue is seen remove the "+" symbol eg : -mtime 1" and run the script
#For smoke proposals alone
print("Proposal Deletion---------------->")
status, output = commands.getstatusoutput("find /ftpserver/RLAB/*tar -mtime +1")
output=output.split("\n")
for i in output:
	print(i)
print"ZAGRAA Deletion"
for i in output:
        a=re.match(r'/ftpserver/RLAB/ZA(.*)([0-9]*).tar',i)
        if a:
                os.system("rm -f %s"%i)
                f.write(i)
                f.write("\n")
                print i
for i in output:
        a=re.match(r'/ftpserver/RLAB/ZA(.*)([0-9]*).extra.tar',i)
        if a:
                os.system("rm -f %s"%i)
                f.write(i)
                f.write("\n")
                print i
#-------------------------------------------------------------------------------------------------------->
#HSDeletion

print"lightspan_2103 deletion"
for i in output:
	a=re.match(r'/ftpserver/RLAB/lightspan_2103.0(.*)9(.*).tar',i)
        if a:
		m=i.split('/ftpserver/RLAB/lightspan_2103.')[1].split(".")[0]
		if(len(m)>3):
                	os.system("rm -f %s"%i)
                	f.write(i)
                	f.write("\n")
			print("lightspan_2103 deleted Build------>")
                	print i
		else:
			print("lightspan_2103 Not deleted Build---->")
			print(i)
for i in output:
        a=re.match(r'/ftpserver/RLAB/lightspan_2103.0(.*)9(.*).extra.tar',i)
        if a:
                m=i.split('/ftpserver/RLAB/lightspan_2103.')[1].split(".")[0]
                if(len(m)>3):
                        os.system("rm -f %s"%i)
                        f.write(i)
                        f.write("\n")
			print("lightspan_2103 deleted Build------>")
                        print i
                else:
			print("lightspan_2103 Not deleted Build---->")
                        print("Not deleted")
                        print(i)
print "SD_65 deletion"
for i in output:
        a=re.match(r'/ftpserver/RLAB/SD_65.0(.*)9(.*).tar',i)
        if a:
                m=i.split('/ftpserver/RLAB/SD_65.')[1].split(".")[0]
                if(len(m)>3):
                        os.system("rm -f %s"%i)
                        f.write(i)
                        f.write("\n")
			print("65 deleted Build---->")
                        print i
                else:
                        print("65 Not deleted Build-------->")
                        print(i)
for i in output:
        a=re.match(r'/ftpserver/RLAB/SD_65.0(.*)9(.*).extra.tar',i)
        if a:
                m=i.split('/ftpserver/RLAB/SD_65.')[1].split(".")[0]
                if(len(m)>3):
                        os.system("rm -f %s"%i)
                        f.write(i)
                        f.write("\n")
			print("65 deleted Build-------->")
                        print i
                else:
                        print("65 Not deleted Build--------->")
                        print(i)
print "2103-omci deletion"
for i in output:
        a=re.match(r'/ftpserver/RLAB/lightspan-omci_2103.0(.*)9(.*).tar',i)
        if a:
                m=i.split('/ftpserver/RLAB/lightspan-omci_2103.')[1].split(".")[0]
                if(len(m)>3):
                        os.system("rm -f %s"%i)
                        f.write(i)
                        f.write("\n")
			print("lightspan-omci_2103 Deleted Build------>")
                        print i
                else:
                        print("lightspan-omci_2103 Not deleted Build----->")
                        print(i)
#MS-deletion
#------------------------------------------------------------------------------------------>
print"lightspan_2012 deletion"
for i in output:
        a=re.match(r'/ftpserver/RLAB/lightspan_2012.0(.*)9(.*).tar',i)
        if a:
                m=i.split('/ftpserver/RLAB/lightspan_2012.')[1].split(".")[0]
                if(len(m)>3):
                        os.system("rm -f %s"%i)
                        f.write(i)
                        f.write("\n")
			print("lightspan_2012 Deleted Build------>")
                        print i
                else:
                        print(" lightspan_2012 Not deleted------>")
                        print(i)
for i in output:
        a=re.match(r'/ftpserver/RLAB/lightspan_2012.0(.*)9(.*).extra.tar',i)
        if a:
                m=i.split('/ftpserver/RLAB/lightspan_2012.')[1].split(".")[0]
                if(len(m)>3):
                        os.system("rm -f %s"%i)
                        f.write(i)
                        f.write("\n")
			print("lightspan_2012 Deleted Build------>")
                        print i
                else:
                        print(" lightspan_2012 Not deleted------>")
                        print(i)

print "SD_64 deletion"
for i in output:
        a=re.match(r'/ftpserver/RLAB/SD_64.0(.*)9(.*).tar',i)
        if a:
                m=i.split('/ftpserver/RLAB/SD_64.')[1].split(".")[0]
                if(len(m)>3):
                        os.system("rm -f %s"%i)
                        f.write(i)
                        f.write("\n")
			print("64 Deleted Build------>")
                        print i
                else:
                        print("64 Not deleted Build----->")
                        print(i)
for i in output:
        a=re.match(r'/ftpserver/RLAB/SD_64.0(.*)9(.*).extra.tar',i)
        if a:
                m=i.split('/ftpserver/RLAB/SD_64.')[1].split(".")[0]
                if(len(m)>3):
                        os.system("rm -f %s"%i)
                        f.write(i)
                        f.write("\n")
			print("64 Deleted Build------>")
                        print i
                else:
                        print("64 Not deleted Build----->")
                        print(i)

print "omci deletion"
for i in output:
        a=re.match(r'/ftpserver/RLAB/lightspan-omci_2012.0(.*)9(.*).tar',i)
        if a:
                m=i.split('/ftpserver/RLAB/lightspan-omci_2012.')[1].split(".")[0]
                if(len(m)>3):
                        os.system("rm -f %s"%i)
                        f.write(i)
                        f.write("\n")
			print("lightspan-omci_2012 Not deleted Build----->")
                        print i
                else:
                        print("lightspan-omci_2012 Not deleted Build------>")
                        print(i)

#-------------------------------------------------------------------------------------------------->
#memory check in ftpserver and deleting files
'''
def memory_limit_check(memory_limit_exceed_date):
        status, output = commands.getstatusoutput("df -kh /ftpserver/ | grep /ftpserver")
        a=re.search(r'([0-9]*)% /ftpserver',output)
        if a:
                if int(a.group(1)) <= 80:
                        print "Memory limit is fine"
                        return
                else:
'''
