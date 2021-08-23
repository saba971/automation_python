#from subprocess import call
#call(["export", "REPO=/repo/atxuser/atc"])
#os.system("sudo ls")
#os.system("sudo export REPO=/repo/atxuser/atc")
#os.system("sudo source $REPO/env/.profile.common")
#os.system("sudo python suppressedFR.py")
import os
#cmd = 'ls'
#cmd1 = 'export REPO=/repo/atxuser/atc'
#cmd2 = 'source $REPO/env/.profile.common'
#cmd3 = 'python suppressedFR.py' 
#os.system(cmd)
#os.system(cmd1)
#os.system(cmd2)
#os.system(cmd3)
#import os
#os.system('export MY_DATA="my_export"')

#import os
#os.environ["MY_DATA"] = "my_export"

#import os 
os.environ["REPO"] = "/repo/atxuser/atc"
cmd2 = 'source $REPO/env/.profile.common'
cmd3 = 'python /root/smokeFRnotify/suppressedFR.py'
os.system(cmd2)
os.system(cmd3)

