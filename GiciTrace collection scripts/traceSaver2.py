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


db = MySQLdb.connect("localhost","root","bgc8g343437","sabadb")
cursor = db.cursor()

36 | 6201.238p11 | 2019-09-27 09:49:33 | 2019-09-27 12:04:49 | 2.15     | 2019-09-27





6102.471
{'NFXSA_NANTA_ISAM_daily': [' CFM_TRAF_ACTIVE_LTM_02', ' CFM_TRAF_ACTIVE_LTM_04'], 'NFXSA_NANTD_REDUND_daily': [' MGMT_EQM_SW_DB_18', ' MGMT_EQM_SW_DB_18'], 'NFXSA_NANTD_ISAM_daily': [' TRAF_MPLS_VPLS_08'], 'CFASB_SRNTD_NGVR_daily': [' NGVR_IGMP_V2_03', ' XDSL_GFAST_GHS_LINE_30'], 'NFXSB_NANTE_ISAM_daily': [' STAT_ERRLOG_NOTIFY_ONLY_01']}
6002.494
{'NFXSD_FANTF_REDUND_daily': [' EQMT_ACT_ACT_REDUN_13'], 'CDESA_SRNTA_MDU_BOTH_daily': [' ISVSRV_MGCTYPE_08', ' NGVR_INCOND_CLEANUP_MEGACO_CFG_06', ' ANSI_L2FWD_TRAF_17'], 'NFXSA_NANTD_ISAM_daily': [' TRAF_MPLS_VPLS_08', ' FD_AUTOSWITCH_1']}

{'NFXSE_FANTG_NGPON_MOBILITY_daily': [' EQMT_CHANNEL_MOB_CONFIG_01'], 'CDASA_SRNTE_NGVR_daily': [' ETH_IPV6_PROTOCOLGROUP_09', ' ETH_IPV6_ND_02'], 'CFERC_DRNTB_NCY_daily': [' STATMON_NCY_TRAP_09', ' XDSL_GFAST_CONF_PROF_09', ' XDSL_GFAST_CONF_PROF_15', ' FASTDSL_ALLOWED_MODE_MASK_01', ' XDSL_GFAST_CONF_PROF_85', ' XDSL_GFAST_CONF_PROF_79', ' EQMT_NTP_SYNC_NCY_03', ' MGMT_CONFD_OPERATION_VALIDATE-MESSAGES_NCY_04', ' MGMT_CONFD_OPERATION_VALIDATE-MESSAGES_NCY_06', ' EQMT_NT_CORE_DUMP_02'], 'NFXSE_FANTF_NGPON_daily': [' QOS_DSCP-PBIT_01', ' EQMT_CHANNEL_GROUP_SUBGROUP_01', ' EQMT_CHANNEL_GROUP_CLEANUP_01', ' EQMT_CHANNEL_PAIR_CLEANUP_01'], 'NFXSA_NANTD_REDUND_daily': [' EQMT_NT_REDUN_06', ' EQMT_ACT_ACT_REDUN_13', ' EQMT_NT_CORE_DUMP_02'], 'CFASB_SRNTD_NGVR_daily': [' XDSL_GFAST_GHS_ALARM_02'], 'NFXRA_NRNTA_ISAM_daily': [' Q-O-S_TRAF_GROUP2_L3FILTER_IBRIDGE_02', ' ETH_GEN_IGMPv3_91'], 'NFXSE_FANTG_FTTU_daily': [' SWMGMT_ONTSWDNLD_02', ' EQMT_ONT_41', ' MGMT_BATCH_ONT', ' EQMT_PORTPROT_TRAFFIC_MINIMAL', ' EQMT_PORTPROT_TRAFFIC_ADMINFORCEDCUT', ' PROT_VPLS_CLEANUP_01'], 'RVXSA_RANTA_NGVR_daily': [' EOAM_ORG_HHT_01', ' EOAM_STAT_COUNT_30', ' EOAM_STAT_COUNT_31', ' NGVR_L2FWD_TRAF_01', ' NGVR_L2FWD_TRAF_02', ' NGVR_L2FWD_TRAF_05', ' NGVR_L2FWD_TRAF_06', ' NGVR_QOS_MARKER_04', ' QOS_TRAF_GROUP1_TM_SUBFLOW_03', ' QOS_TRAF_GROUP1_TM_SUBFLOW_04', ' QOS_TRAF_GROUP1_TM_SUBFLOW_28', ' QOS_TRAF_GROUP1_TM_SUBFLOW_29'], 'CDESA_SRNTA_MDU_BOTH_daily': [' NGVR_SIP_ALM_05', ' NGVR_SIP_ALM_06', ' ISVSRV_MGCTYPE_08', ' NGVR_INCOND_CLEANUP_MEGACO_CFG_06', ' ANSI_L2FWD_TRAF_17'], 'NFXSA_NANTD_ISAM_daily': [' TRAF_RBVLAN_IPOE_PPP_01']}

{'NFXSD_FANTF_REDUND_daily': [' STAT_ERRLOG_RECOV_01'], 'NFXSE_FANTG_NGPON_MOBILITY_daily': [' EQMT_CHANNEL_MOB_LT_LOCK_01'], 'CDASA_SRNTE_NGVR_daily': [' NGVR_L2FWD_TRAF_20'], 'CFERC_DRNTB_NCY_daily': [' STATMON_NCY_TRAP_09', ' XDSL_GFAST_CONF_PROF_09', ' XDSL_GFAST_CONF_PROF_15', ' FASTDSL_ALLOWED_MODE_MASK_01', ' XDSL_GFAST_CONF_PROF_85', ' XDSL_GFAST_CONF_PROF_79', ' EQMT_NTP_SYNC_NCY_03', ' MGMT_CONFD_OPERATION_VALIDATE-MESSAGES_NCY_04', ' MGMT_CONFD_OPERATION_VALIDATE-MESSAGES_NCY_06', ' EQMT_NT_CORE_DUMP_02'], 'NFXSA_NANTA_ISAM_daily': [' SM_DHCP_FUNC_04'], 'NFXSB_NANTA_ISAM_daily': [' LANX_SYS_INIT_12'], 'NFXSA_NANTD_REDUND_daily': [' EQMT_NT_HITRED_09'], 'CFASB_SRNTD_NGVR_daily': [' XDSL_GFAST_GHS_ALARM_02'], 'NFXSE_FANTF_NGPON_daily': [' GPON_TSCPBIT_009', ' QOS_DSCP-PBIT_01', ' EQMT_CHANNEL_GROUP_SUBGROUP_01', ' EQMT_CHANNEL_GROUP_CLEANUP_01', ' EQMT_CHANNEL_PAIR_CLEANUP_01'], 'NFXRA_NRNTA_ISAM_daily': [' ETH_GEN_IGMP_SSM_43', ' FWM_I_BRIDGE_SC_VLAN_01'], 'NFXSE_FANTG_FTTU_daily': [' GPON_TSCPBIT_009', ' EQMT_PORTPROT_TRAFFIC_MINIMAL', ' EQMT_PORTPROT_TRAFFIC_ADMINFORCEDCUT', ' STAT_ERRLOG_RECOV_01'], 'RVXSA_RANTA_NGVR_daily': [' EOAM_ORG_HHT_01', ' EOAM_STAT_COUNT_30', ' EOAM_STAT_COUNT_31'], 'CDESA_SRNTA_MDU_BOTH_daily': [' ISVSRV_MGCTYPE_08', ' NGVR_INCOND_CLEANUP_MEGACO_CFG_06']}








def ssh_login_check(ip,username,password):
    ssh_flag=False
    try:
        SSH_CMD='ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null %s@' %username
        cli = pexpect.spawn(SSH_CMD+135.249.111.12)
        cli.maxread = 6000
        cli.timeout = 60
        cli.logfile = sys.stdout
        i = cli.expect(['password:', r'\(yes\/no\)',r'Connection refused',pexpect.EOF])
        if i == 0:
            cli.sendline(password)
        elif i == 1:
            cli.sendline("yes")
            ret1 = cli.expect(["password:",pexpect.EOF])
            if ret1 == 0:
                cli.sendline(password)
            else:
                pass
        elif i == 2:
            print "Device is not reachable"
        else:
            print "Timeout : Error in SSH connect"
        if cli.expect(["#","incorrect"],timeout=10):
            print('Unable to login')
        else:
            cli.expect([".*#","$"])
            ssh_flag=True
    except Exception as inst:
        print('Failed to Login %s' %inst)
    cli.close()
    return ssh_flag