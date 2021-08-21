import re
import time
import datetime
import paramiko 
import os
import os.path
import commands
import MySQLdb
db = MySQLdb.connect("localhost","uma","alcatel01","TESTDB" )
cursor = db.cursor()
date=datetime.date.today().strftime("%b %d")
my_list=[]
ch1_list=[]
ch2_list=[]
ch3_list=[]
smoke3_list=['CDASA_SRNTE_NGVR_smoke03','CDASB_SRNTG_NGVR_smoke03','CDESA_SRNTA_MDU_BOTH_smoke03','CDESB_SRNTF_MDU_BOTH_smoke03','CDESC_SRNTI_MDU_BOTH_smoke03',' CFASB_SRNTD_NC_DPU_smoke03','CFASB_SRNTD_NGVR_smoke03','CFASD_SRNTH_NGVR_smoke03' 'CFASJ_SRNTM_NBN_4F_smoke03','CFERC_DRNTB_NCY_smoke03','CFXRA_CFNTB_DF_16GW_smoke03','CFXRA_CFNTB_NGPON_smoke03','CFXSA_CFNTA_FTTU_smoke03','CFXSC_CFNTC_GPON_suite-FTTU_smoke03','FERC_DRNTB_NCY_smoke03','CFXRA_CFNTB_DF_16GW_smoke03','CFXRA_CFNTB_NGPON_smoke03','CFXSA_CFNTA_FTTU_smoke03','CFXSC_CFNTC_GPON_suite-FTTU_smoke03','NFXSA_NANTE_FTTU_smoke03','NFXSA_NANTE_ISAM_smoke03','NFXSB_NANTA_ISAM_smoke03','NFXSB_NANTD_ISAM_smoke03','NFXSD_FANTF_FTTU_smoke03','NFXSE_FANTF_FTTU_smoke03','NFXSF_FANTF_NGPON_smoke03','NFXSF_FANTG_FTTU_smoke03','NNI_RANTA_NNI_smoke03','RVXSA_RANTA_NGVR_BOTH_smoke03','RVXSA_RANTA_NGVR_smoke03','RVXSA_RANTB_NGVR_smoke03','VSRMA_SRNTB_NGVR_smoke03','V4_NANTA_ICONIC_smoke03','NFXSF_FANT_FTTU_FELTB_REMOTE_smoke03']
#print(len(smoke3_list))
output1=''
output2=''
os.system('clear')
disp1='1'
disp2='smoke03'
disp3='135.249.31.163'
disp4='2018'
def getdate(timestamp):

	ntimestamp = timestamp.split("-")
	timestamp1 = ntimestamp[0]
	month=timestamp1[1:2]
	if len(month) == 1:
		month='0'+month
	date=timestamp1[2:4]
	if len(date) == 1:
		date='0'+date
	year=timestamp1[4:8]
	new_date='-'.join([year,month,date])
	return new_date

def connect(atxserver,cmd1):
	try:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(atxserver, port=22 ,username='atxuser',password='alcatel01')
		stdin, stdout, stderr = ssh.exec_command(cmd1)
		output1 = stdout.readlines()
		return output1
	except Exception,e:
		print str(e)
		print "         "+atxserver +' is not Reachable'+"\n"
out1=connect('135.249.31.163','ls -lrt /ftpserver/RLAB/ | grep "SD_58.*p*"')

for liner1 in out1:
	liner1=liner1.rstrip("\n")
	#print liner1
	if date in liner1:
		liner1=liner1.split(date)
		if not 'extra' in liner1[1]:
			if not'NCY' in liner1[1] and 'p' in liner1[1]:
				my_list.append(liner1[1].split(" ")[2].strip().replace(".tar",""))
					
var1_disp = "NA = NA"
var2_disp="NA = NA"
var3_disp="NA = NA"
var4_disp="NA = NA"
var5_disp="NA = NA"
var6_disp="NA = NA"
var7_disp="NA = NA"
var8_disp="NA = NA"
var9_disp="NA = NA"
var10_disp="NA = NA"
var11_disp="NA = NA"
var12_disp="NA = NA"


FO = open('sam.txt', 'w')
cnt=0
for i in range(0,len(my_list)):
	build =my_list[i]
	print(build)
	out2=connect('135.249.31.163','ls -lrt /tftpboot/atx/logs/*/'+build+'/* | grep "MERCUR"')
	if not ' No such file or directory' in out2:
		for liner in out2:
			liner=liner.rstrip("\n")
			cnt+=1
			print(liner)
			FO.write(liner.split('s/')[1].split('/SD')[0]+';')
			FO.write(build+';')
			FO.write(liner.split('/')[6].split(':')[0]+';')
			try:
				liner=liner.rstrip(":")+"/ATX_Runtime_Stats"
				liner="cat "+liner 
				out3=connect('135.249.31.163',liner)
				for line in out3:
					line=line.rstrip("\n")
					try:
						var1=re.search('Queued Duration(.*)',line)
						var1_disp = var1.group(0)
					except:
						try:
							var2=re.search('Repo Duration(.*)',line)
							var2_disp = var2.group(0)
						except:
							try:
								var3=re.search('LoadPreparation Duration(.*)',line)
								var3_disp = var3.group(0)
							except:
								try:
									var4=re.search('Load Donwload Duration(.*)',line)
									var4_disp = var4.group(0)
								except:
									try:
										var5=re.search('Load Activation Duration(.*)',line)
										var5_disp = var5.group(0)
									except:
										try:
											var6=re.search('System Config Duration(.*)',line)
											var6_disp = var6.group(0)
										except:
											try:
												var7=re.search('LT Check Duration(.*)',line)
												var7_disp = var7.group(0)
											except:
												try:
													var8=re.search('Load Commit Duration(.*)',line)
													var8_disp = var8.group(0)
												except:
													try:
														var9=re.search('Pre LTB Duration(.*)',line)
														var9_disp = var9.group(0)
													except:
														try:
															var10=re.search('Post LTB Duration(.*)',line)
															var10_disp = var10.group(0)
														except:
															try:
																var11=re.search('LTB Duration(.*)',line)
																var11_disp = var11.group(0)
															except:
																try:
																	var12=re.search('Total Run Duration(.*)',line)
																	var12_disp = var12.group(0)

																except:
																	pass        

				FO.write(var1_disp.split("=")[1].strip()+';'+var2_disp.split("=")[1].strip()+';'+var3_disp.split("=")[1].strip()+';'+var4_disp.split("=")[1].strip()+';'+var5_disp.split("=")[1].strip()+';'+var6_disp.split("=")[1].strip()+';'+var7_disp.split("=")[1].strip()+';'+var8_disp.split("=")[1].strip()+';'+var9_disp.split("=")[1].strip()+';'+var10_disp.split("=")[1].strip()+';'+var11_disp.split("=")[1].strip()+';'+var12_disp.split("=")[1].strip()+'\n')
			except:
				pass
FO.close()
try:
	for line in open('sam.txt','r'):
		line=line.rstrip("\n").split(";")
		org=getdate(line[2])
		print(org)
		jid=0
                que="SELECT MAX(id)from smoke_stat"
                cursor.execute(que)
                row=cursor.fetchone()
                jid=row[0]
		jid=jid+1
		print(jid)
		#queu="select platform from smoke_stat where `load` = '%s' and `platform` = '%s'"%(line[1],line[0])
		#print(queu)
		print(line[1])
		print(line[0])
		queu=cursor.execute("select platform from smoke_stat where `load` = '%s' and `platform` = '%s'" %(line[1],line[0]))
		row=cursor.fetchall()
		print(queu)
		if(queu!=0):
			print'false'
		else:
			print'insert'
	file_wr=open("build.html",'w')
        file_wr.write("<!DOCTYPE html>\n")
        file_wr.write('<html lang="en">\n')
        file_wr.write("<head>\n")
        file_wr.write("</head>\n")
        file_wr.write("<body>\n")
        file_wr.write('<center><h1 > SMOKE RUNTIME DETAILS</h1></center>\n')
        #file_wr.write("                <center><h2 > "+build+" status </h2></center>\n")
        file_wr.write("    <hr />\n")
        file_wr.write('    <center><table border color "blue" bgcolor="white" border=1>\n')
        file_wr.write('    <tr><td>week</td><td>Load</td><td>Platform</td><td>Timestamp</td><td>Queued Duration</td><td width="400">Repo Duration</td><td>LoadPreparation Duration</td><td>Load Donwload Duration</td>\
<td>Load Activation Dauration</td><td>System Config Duration</td><td>LT Check Duration</td><td>Load Commit Duration</td><td>Pre LTB Duration </td>\
<td>Post LTB Duration</td><td>LTB Duration</td><td>Total Run Duration</td></tr>\n')
	for line in open('sam.txt','r'):
		line=line.rstrip("\n").split(";") 
		if line[0]=="Platform":
                	pass
                elif(line[3]=='NA'and line[4]=='NA'and line[5]=='NA'and line[6]=='NA'and line[7]=='NA'and line[8]=='NA'and line[9]=='NA'and line[10]=='NA'and line[11]=='NA'and line[12]=='NA'and line[13]=='NA'and line[14]=='NA'):
                        print('')
                else:
                        file_wr.write('    <tr><td >'+line[1]+'</td> <td >'+line[0]+'</td><td >'+line[2]+'</td><td >'+line[3]+'</td><td >'+line[4]+'</td><td > '+line[5]+'</td><td >'+line[6]+'</td>  <td > '+line[7]+'</td><td > '+line[8]+'</td><td >'+line[9]+'</td>  <td > '+line[10]+ '</td><td > '+line[11]+'</td><td > '+line[12]+'</td><td>'+line[13]+'</td><td>'+line[14]+'</td></tr>\n')
	file_wr.write("    </table></center>\n")
	file_wr.write("\n")
	file_wr.write("\n")
	file_wr.write("</body>\n")
	file_wr.write("</html>\n")
	file_wr.close()
except:
	pass
db.commit()
db.close()









