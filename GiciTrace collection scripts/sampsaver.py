#!/usr/bin/python

#coding:utf-8
import time
import re
import os
import stat
import logging
import logging.handlers as handlers
import telnetlib
from optparse import OptionParser


parser = OptionParser()
parser.add_option("--craftIp", dest="craftIp",default='', help="Port server ip")
parser.add_option("--craftPort", dest="craftPort", help="Port server port")
parser.add_option("--LOG_FILE", dest="LOG_FILE",default='console.log', help="Log file name (eg. console.log)")
parser.add_option("--storeInterval", type="int", dest="storeInterval",default=5, help="log stored in a file every interval hours(eg. 5)")
parser.add_option("--dut_type", dest="dut_type", help="Setup type")
(options, args) = parser.parse_args()

craftIp = options.craftIp
craftPort = options.craftPort
storeInterval = options.storeInterval
LOG_FILE = options.LOG_FILE
dut_type = options.dut_type
telnetTn=''

#saba
#saba

def db_print(printStr, debugType="normal"):
  if debugType=="recv" :
    print  ("<<<" + printStr)
  elif debugType=="send" :
    print  (">>>" + printStr)
  else:
    print  ("---" + printStr)

def Telnet_send(cmd, linecmd = 1):
  global tn
  tn.write(cmd)
  db_print(cmd, "send")
  if linecmd == 1:
    tn.write("\r")

def Server_send(cmd, linecmd = 1):
  global telnetTn
  telnetTn.write(cmd)
  db_print(cmd, "send")
  if linecmd == 1:
      telnetTn.write("\r")

def lant_cmd(traceIp,tracePort):
    global telnetTn
    returnTmp = ""
    retryTimes = 0
    port=tracePort[3:5]
    tunnel_cmd="tunnel %s" %port 
    telnetTn = telnetlib.Telnet(traceIp)
    Server_send("\r",0)
    returnTmp = telnetTn.read_until(">",5)
    if ">" in returnTmp:
        pass
    else:
        returnTmp = returnTmp + telnetTn.read_until("*",10)
        while ">" not in returnTmp:
            if "login:" in returnTmp:
                Server_send("admin")
                returnTmp = telnetTn.read_until(">",3)
                continue
            elif "password:" in returnTmp:
                Server_send("PASS")
                returnTmp = telnetTn.read_until(">",3)
                continue
            else:
                retryTimes = retryTimes + 1
                if (retryTimes  >= 20):
                    db_print ("sleep 5 mins and CLI cannot be reached")
                    break
                Server_send("\r", 0)
                time.sleep(5)
                returnTmp = telnetTn.read_until("*",1)
                continue
    Server_send("enable")
    returnTmp = telnetTn.read_until("#",15)
    Server_send(tunnel_cmd)
    returnTmp = telnetTn.read_until("#",15)
    Server_send("accept")
    returnTmp = telnetTn.read_until("#",15)
    Server_send("kill connection")
    returnTmp = telnetTn.read_until("#",15)
    Server_send("exit")
    returnTmp = telnetTn.read_until("#",15)
    Server_send("exit")
    returnTmp = telnetTn.read_until("#",15)
    Server_send("exit")
    telnetTn.close()
    return returnTmp

print craftIp + ':' + craftPort
if dut_type in ['REMOTE','SDFX','SDOLT','NCDPU']:
    Username = "root"
    Password = "2x2=4"
else:    
    Username = "shell"
    Password = "nt"
if len(craftPort) == 5:
    db_print("LANTRONICS GICI")
    lant_cmd(craftIp,craftPort)
else:        
    db_print("DIGI GICI")
    cmd = '\"kill %s\"' % craftPort[2:4]
    os.system('(sleep 1;echo "root";sleep 1;echo "dbps";sleep 1;echo %s;sleep 1;echo "exit";sleep 1) | telnet %s' % (cmd, craftIp))

if dut_type in ['REMOTE','SDFX','SDOLT','NCDPU']:
    tn = telnetlib.Telnet(craftIp, craftPort, 30)
    Telnet_send("\r", 0)
    returnTmp = ""
    retryTimes = 0
    returnTmp = tn.read_until("#",5)
    if "#" in returnTmp:
      pass
    else:
      returnTmp = returnTmp + tn.read_until("*",10)
      while "#" not in returnTmp:
        if "isam-reborn login:" in returnTmp:
          Telnet_send(Username)
          returnTmp = tn.read_until("#",3)
          continue
        elif "Password:" in returnTmp:
          Telnet_send(Password)
          returnTmp = tn.read_until("#",3)
          continue
        else:
          retryTimes = retryTimes + 1
          if (retryTimes  >= 20):
            db_print ("sleep 5 mins and CLI cannot be reached")
            break
          Telnet_send("\r", 0)
          time.sleep(15)
          returnTmp = tn.read_until("*",1)
          continue
else:
    tn = telnetlib.Telnet(craftIp, craftPort, 30)  
    Telnet_send("\r", 0)
    returnTmp = ""
    retryTimes = 0
    returnTmp = tn.read_until(">",5)
    if ">" in returnTmp:
        pass
    elif "A:FAD-Chassis#" in returnTmp:
        pass
    else:
        returnTmp = returnTmp + tn.read_until("*",10)
        while ">" not in returnTmp:
            if "Login:" in returnTmp:
                Telnet_send(Username)
                returnTmp = tn.read_until(">",3)              
                continue
            else:
                retryTimes = retryTimes + 1
                if (retryTimes  >= 20):
                    db_print ("sleep 5 mins and CLI cannot be reached")
                    break
                    Telnet_send("\r", 0)
                    time.sleep(15)
                    returnTmp = tn.read_until("*",1)                    
                    continue
    #Telnet_send("bld info")


class SizedTimedRotatingFileHandler(handlers.TimedRotatingFileHandler):
      def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None,
                 delay=0, when='h', interval=1, utc=False):
        if maxBytes > 0:
            mode = 'a'
        handlers.TimedRotatingFileHandler.__init__(
            self, filename, when, interval, backupCount, encoding, delay, utc)
        self.maxBytes = maxBytes

      def shouldRollover(self, record):
        if self.stream is None:                 # delay was set...
            #print "delay was set"
            self.stream = self._open()
        if self.maxBytes > 0:                   # are we rolling over?
            #print "are we rolling over"
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)  #due to non-posix-compliant Windows feature
            if self.stream.tell() + len(msg) >= self.maxBytes:
               #print "oversize!!!!" 
               return 1
        t = int(time.time())
        if t >= self.rolloverAt:
            #print "rollover!!!!"
            return 1
        return 0

def my_SizedTimedRotatingFileHandler():
    log_filename=LOG_FILE
    logger=logging.getLogger('MyLogger')
    logger.setLevel(logging.DEBUG)
    handler=SizedTimedRotatingFileHandler(
        log_filename, when='h',interval=storeInterval,
        # encoding='bz2',  # uncomment for bz2 compression
        )
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    while True:
        con_log=tn.read_very_eager()
        time.sleep(2)
        print con_log
        logger.debug(con_log)

def my_SingleFileHandler():
    log_filename=LOG_FILE
    logger=logging.getLogger('MyLogger')
    logger.setLevel(logging.DEBUG)
    handler=FileHandler(log_filename)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    while True:
        con_log=tn.read_very_eager()
        time.sleep(2)
        print con_log
        logger.debug(con_log)        

my_SizedTimedRotatingFileHandler()


