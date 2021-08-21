import os
import commands
import re
space=commands.getoutput("df -kh /")
space=space.splitlines()
for line in space:
  try:
    var=re.search('100%',line)
    var_disp=var.group(0)
  except:
    try:
      var1=re.search('[7-9][0-9]%',line)
      var1_disp=var1.group(0)
      #print var1_disp
      if var1_disp.strip('%') > '84':
        #print var1_disp 
        os.system('echo " Hi Team,\n\n Build Backup server needs cleanup. It\'s current space size is '+var1_disp+'\n\n Br,\n Akhilesh Kumar" > send_email ')
        os.system('/bin/mailx -s "Build backup server needs cleanup !!! " akhilesh.kumar3@alcatel-lucent.com,arun_kumar.deena_dayalan@nokia.com < send_email')
      else:
        os.system('echo " " > send_email')
    except:
      pass
