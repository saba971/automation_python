#!/usr/bin/python

import re
import os
import commands
import urllib
import smtplib
import subprocess
import datetime

#os.system("source main.sh")
urllink="http://135.249.26.35/suppressFR.html"
toemail=""
Resolved_FR_list=[]
eftime = datetime.date.today().strftime('%Y-%m-%d')
now = datetime.datetime.now()
current_time=now.strftime('%Y-%m-%d %H:%M:%S')

def Countdays(sdate,edate):
        date_format = "%Y-%m-%d"
        a = datetime.datetime.strptime(sdate, date_format)
        b = datetime.datetime.strptime(edate, date_format)
        delta = b - a
        return delta

def FRnotificationemail():

        SERVER = "localhost"
#        TO = ['vijaya_ganesh.m@nokia.com','umapathy.gajendran@nokia.com','arun_kumar.deena_dayalan@nokia.com','kannan.govindaraju@nokia.com']
	TO = ['arun_kumar.deena_dayalan@nokia.com','kannan.govindaraju@nokia.com','sabanayagam.thambaranathan@nokia.com']
#	TO = ['umapathy.gajendran@nokia.com']
        FROM = "remotelab-chn@groups.nokia.com"
        SUBJECT = "LSR2109/ISR6502 Smoke suppresed Testcases - FR verification notification"

        TEXT = "Hi Team,"
        TEXT0 = "\n"
        TEXT1 = "Please check below link for smoke suppressed FR's state,\n"
        TEXT2 = "%s"%urllink
        TEXT3 = "\n"
        TEXT4 = "Regards"
        TEXT5 = "RemoteLab"


        message = """\
From: %s
To: %s
Subject: %s

%s
%s
%s
%s
%s
%s
%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT,TEXT0,TEXT1,TEXT2,TEXT3,TEXT4,TEXT5)

# Send the mail

        server = smtplib.SMTP(SERVER)
        server.sendmail(FROM, TO, message)
        server.quit()

link = "http://aww.sh.bel.alcatel.be/tools/Logs/ETSI/ATCSuppressed.txt"
f = urllib.urlopen(link)
file = open("FR_ATC.txt", "w")
file.write(f.read())
print file.close()


with open('FR_ATC.txt') as f:
  text_lines=f.read().split("\n")

for line in text_lines:
  if line.find('ALU') != -1:
  #  var = re.search(r'([a-zA-Z0-9\-\_]+)\s+(.*)\s+(.*)\s+(.*)\s+(.*)\s+(.*)',line)
    var = re.search(r'(.*)\s+(.*)\s+(.*)\s+(.*)\s+(.*)\s+(.*)',line)
    if var is None:
      continue
    else:
       if (var.group(2) == "R6.5.02" or var.group(2) == "R21.09" or var.group(2) == "R6.5.01" or var.group(2)== "R21.06"):
        print var.group(1)+"  <=====>  "+var.group(5)
        cmd = "/repo/atxuser/atc/cm4/tools/BELL/src/cmtools/cnfmgnt/scm/scm sql -nh -nl -q \"select FORMTYPE,STATUS,PLANNEDREL from v_ddts_ircrfr where formname = \'%s\' \" /dev/stdout"%(var.group(3))
        output=commands.getoutput(cmd)
        new=re.search(r'("(.*)";"(.*)";"(.*)")',output)
        cmd1 = "/repo/atxuser/atc/cm4/tools/BELL/src/cmtools/cnfmgnt/scm/scm sql -nh -nl -q \"SELECT ADDED_DATE from ASAM_DBA.T_BLD_TI_AEI where FR = \'%s\' \" /dev/stdout"%(var.group(3))
        output1=commands.getoutput(cmd1)
        new1=re.search(r'("(.*)")',output1)
        sttime=new1.group(2)
        tot = Countdays(sttime,eftime)	      	      			
        pending_day=str(tot.days)	
        if var.group(5) == 'TARGET' or var.group(5) == 'X':	
#        	var_list="Testcase is "+var.group(1)+" and FR is  "+var.group(3)+" state = "+new.group(3)+" Release = "+var.group(2)
	  if var.group(5) == 'X':
	    setup_env="TARGET&HOST"
	  else:
            setup_env=var.group(5)
#          var_list=var.group(1)+"\t\t\t\t\t"+var.group(3)+"\t"+new.group(3)+"\t"+var.group(2)+"\t"+setup_env+"\t"+new.group(4)+"\t"+new1.group(2)+"\t"+pending_day
	  var_list=var.group(1)+";"+var.group(3)+";"+new.group(3)+";"+var.group(2)+";"+setup_env+";"+new.group(4)+";"+new1.group(2)+";"+pending_day+";"
          Resolved_FR_list.append(var_list)
#	print Resolved_FR_list

print Resolved_FR_list
#FRnotificationemail(Resolved_FR_list)

with open("FR_final.txt",'w') as filehandle:
  for val in Resolved_FR_list:
  	filehandle.write('%s\n' % val)


file_wr=open("/var/www/html/suppressFR.html",'w')
file_wr.write("<!DOCTYPE html>\n")
file_wr.write('<html lang="en">\n')
file_wr.write("<head>\n")
file_wr.write('<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css" integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4" crossorigin="anonymous">\n')


file_wr.write('<style>\n')
file_wr.write('#hname{\n')
file_wr.write('        position:fixed;\n')
file_wr.write('        top:7px;\n')
file_wr.write('        left:453px;\n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('textarea,input[type="text"],input[type="password"],input[type="datetime"],input[type="datetime-local"],input[type="date"],input[type="month"],input[type="time"],input[type="week"],input[type="number"],input[type="email"],input[type="url"],input[type="search"],input[type="tel"],input[type="color"],.uneditable-input{background-color:#ffffff;border:1px solid #cccccc;-webkit-box-shadow:inset 0 1px 1px rgba(0, 0, 0, 0.075);-moz-box-shadow:inset 0 1px 1px rgba(0, 0, 0, 0.075);box-shadow:inset 0 1px 1px rgba(0, 0, 0, 0.075);-webkit-transition:border linear .2s, box-shadow linear .2s;-moz-transition:border linear .2s, box-shadow linear .2s;-o-transition:border linear .2s, box-shadow linear .2s;transition:border linear .2s, box-shadow linear .2s;}textarea:focus,input[type="text"]:focus,input[type="password"]:focus,input[type="datetime"]:focus,input[type="datetime-local"]:focus,input[type="date"]:focus,input[type="month"]:focus,input[type="time"]:focus,input[type="week"]:focus,input[type="number"]:focus,input[type="email"]:focus,input[type="url"]:focus,input[type="search"]:focus,input[type="tel"]:focus,input[type="color"]:focus,.uneditable-input:focus{border-color:rgba(82, 168, 236, 0.8);outline:0;outline:thin dotted \9;-webkit-box-shadow:inset 0 1px 1px rgba(0,0,0,.075), 0 0 8px rgba(82,168,236,.6);-moz-box-shadow:inset 0 1px 1px rgba(0,0,0,.075), 0 0 8px rgba(82,168,236,.6);box-shadow:inset 0 1px 1px rgba(0,0,0,.075), 0 0 8px rgba(82,168,236,.6);}\n')
file_wr.write('select,input[type="file"]{height:30px;*margin-top:4px;line-height:20px;}\n')
file_wr.write('select{width:150px;border:1px solid #cccccc;background-color:#ffffff;}\n')
file_wr.write('\n')
file_wr.write(' *     DEMO STYLE\n')
file_wr.write(' *     */\n')
file_wr.write('\n')
file_wr.write('@import "https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700";\n')
file_wr.write('body {\n')
file_wr.write("    font-family: 'Poppins', sans-serif;\n")
file_wr.write('    background: #fafafa;\n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('p {\n')
file_wr.write("    font-family: 'Poppins', sans-serif;\n")
file_wr.write('    font-size: 1.1em;\n')
file_wr.write('    font-weight: 300;\n')
file_wr.write('    line-height: 1.7em\n')
file_wr.write('    color: #999;\n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('a,\n')
file_wr.write('a:hover,\n')
file_wr.write('a:focus {\n')
file_wr.write('    color: inherit;\n')
file_wr.write('    text-decoration: none;\n')
file_wr.write('    transition: all 0.3s;\n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('.navbar {\n')
file_wr.write('    padding: 5px 0px;\n')
file_wr.write('    background: #fff;\n')
file_wr.write('    border: none;\n')
file_wr.write('    border-radius: 0;\n')
file_wr.write('    margin-bottom: 40px;\n')
file_wr.write('    box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);\n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('.navbar-btn {\n')
file_wr.write('    box-shadow: none;\n')
file_wr.write('    outline: none !important;\n')
file_wr.write('    border: none;\n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('.line {\n')
file_wr.write('    width: 100%;\n')
file_wr.write('    height: 1px;\n')
file_wr.write('    border-bottom: 1px dashed #ddd;\n')
file_wr.write('    margin: 40px 0;\n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('/* ---------------------------------------------------\n')
file_wr.write(' *     SIDEBAR STYLE\n')
file_wr.write(' *     ----------------------------------------------------- */\n')
file_wr.write('\n')
file_wr.write('.wrapper {\n')
file_wr.write('    display: flex;\n')
file_wr.write('    width: 100%;\n')
file_wr.write('    align-items: stretch;\n')
file_wr.write(' }\n')
file_wr.write(' x\n')
file_wr.write('\n')
file_wr.write('#sidebar {\n')
file_wr.write('    min-width: 250px;\n')
file_wr.write('    max-width: 250px;\n')
file_wr.write('    background: #262626;\n')
file_wr.write('    color: #fff;\n')
file_wr.write('    transition: all 0.3s;\n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('#sidebar.active {\n')
file_wr.write('    margin-left: -250px;\n')
file_wr.write('    \n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('#sidebar .sidebar-header {\n')
file_wr.write('    padding: 20px;\n')
file_wr.write('    background: #6d7fcc;\n')
file_wr.write('    \n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('#sidebar ul.components {\n')
file_wr.write('    padding: 60px 0;\n')
file_wr.write('    position:auto ;\n')
file_wr.write('\n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('#sidebar ul p {\n')
file_wr.write('    color: #fff;\n')
file_wr.write('    padding: 50px;\n')
file_wr.write('    \n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('#sidebar ul li a {\n')
file_wr.write('    padding: 7px;\n')
file_wr.write('    font-size:0.9em;\n')
file_wr.write('    display: block;\n')
file_wr.write('    \n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('#sidebar ul li a:hover {\n')
file_wr.write('    color: #262626;\n')
file_wr.write('    background: #fff;\n')
file_wr.write('    \n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('#sidebar ul li.active>a,\n')
file_wr.write('a[aria-expanded="true"] {\n')
file_wr.write('    color: #fff;\n')
file_wr.write('    background: #262626;\n')
file_wr.write('    \n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('a[data-toggle="collapse"] {\n')
file_wr.write('    position: relative;\n')
file_wr.write('    \n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('.dropdown-toggle::after {\n')
file_wr.write('    display: block;\n')
file_wr.write('    position: absolute;\n')
file_wr.write('    top: 50%;\n')
file_wr.write('    right: 20px;\n')
file_wr.write('    transform: translateY(-50%);\n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('ul ul a {\n')
file_wr.write('    font-size: 0.9em !important;\n')
file_wr.write('    padding-left: 30px !important;\n')
file_wr.write('    background: #262626;\n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('ul.CTAs {\n')
file_wr.write('    padding: 20px;\n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('ul.CTAs a {\n')
file_wr.write('    text-align: center;\n')
file_wr.write('    font-size: 0.9em !important;\n')
file_wr.write('    display: block;\n')
file_wr.write('    border-radius: 5px;\n')
file_wr.write('    margin-bottom: 5px;\n')
file_wr.write('}\n')
file_wr.write('a.download {\n')
file_wr.write('    background: #fff;\n')
file_wr.write('    color: #262626;\n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('a.article,\n')
file_wr.write('a.article:hover {\n')
file_wr.write('    background: #262626 !important;\n')
file_wr.write('    color: #fff !important;\n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('/* ---------------------------------------------------\n')
file_wr.write(' *     CONTENT STYLE\n')
file_wr.write(' *     ----------------------------------------------------- */\n')
file_wr.write('\n')
file_wr.write('#content {\n')
file_wr.write('    width: 100%;\n')
file_wr.write('    padding: 20px;\n')
file_wr.write('    min-height: 100vh;\n')
file_wr.write('    transition: all 0.3s;\n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('/* ---------------------------------------------------\n')
file_wr.write(' *     MEDIAQUERIES\n')
file_wr.write(' *     ----------------------------------------------------- */\n')
file_wr.write('\n')
file_wr.write('@media (max-width: 768px) {\n')
file_wr.write('    #sidebar {\n')
file_wr.write('        margin-left: -50px;\n')
file_wr.write('    }\n')
file_wr.write('    #sidebar.active {\n')
file_wr.write('        margin-left: 0;\n')
file_wr.write('    }\n')
file_wr.write('    #sidebarCollapse span {\n')
file_wr.write('        display: none;\n')
file_wr.write('    }\n')
file_wr.write('}\n')
file_wr.write('\n')
file_wr.write('</style>\n')

file_wr.write("<script>\n")	
file_wr.write("        function exportTableToExcel(tableID, filename = ''){\n")
file_wr.write("    var downloadLink;\n")
file_wr.write("    var dataType = 'application/vnd.ms-excel';\n")
file_wr.write("    var tableSelect = document.getElementById(tableID);\n")
file_wr.write("    var tableHTML = tableSelect.outerHTML.replace(/ /g, '%20');\n")
file_wr.write("    \n")
file_wr.write("    // Specify file name\n")
file_wr.write("    filename = filename?filename+'.xls':'excel_data.xls';\n")
file_wr.write("    \n")
file_wr.write("    // Create download link element\n")
file_wr.write('    downloadLink = document.createElement("a");\n')
file_wr.write("    \n")
file_wr.write("    document.body.appendChild(downloadLink);\n")
file_wr.write("    \n")
file_wr.write("    if(navigator.msSaveOrOpenBlob){\n")
file_wr.write("        var blob = new Blob(['\ufeff', tableHTML], {\n")
file_wr.write("            type: dataType\n")
file_wr.write("        });\n")
file_wr.write("        navigator.msSaveOrOpenBlob( blob, filename);\n")
file_wr.write("    }else{\n")
file_wr.write("        // Create a link to the file\n")
file_wr.write("        downloadLink.href = 'data:' + dataType + ', ' + tableHTML;\n")
file_wr.write("    \n")
file_wr.write("        // Setting the file name\n")
file_wr.write("        downloadLink.download = filename;\n")
file_wr.write("        \n")
file_wr.write("        //triggering the function\n")
file_wr.write("        downloadLink.click();\n")
file_wr.write("    }\n")
file_wr.write("}\n")
file_wr.write("</script> \n")


file_wr.write(' <br>\n')
file_wr.write('  <div class="wrapper">\n')
file_wr.write('        <!-- Sidebar  -->\n')
file_wr.write('  <!-- Page Content  -->\n')
file_wr.write('        <div id="content">\n')
file_wr.write('            <nav class="navbar navbar-dark bg-dark fixed-top navbar-expand-lg navbar-light bg-light">\n')
file_wr.write('                <div class="container-fluid">\n')
file_wr.write(' <ul class="navbar-nav mr-auto">\n')
file_wr.write('<div id="hname">\n')
file_wr.write('  <ion-navbar>\n')
file_wr.write('  <h5><font color="white"><center>\n')
file_wr.write('      Automated Regression Testing as a Service - ARTaaS </center></font>\n')
file_wr.write('      <font color="white" size="2"><center><i>\n')
file_wr.write('          (Formerly Known as Remote Lab - RLAB) </i></font></h5></center>\n')
file_wr.write('      </ion-navbar>\n')
file_wr.write('</div>\n')
file_wr.write('    </ul>\n')
file_wr.write('                    <div class="collapse navbar-collapse" id="navbarSupportedContent">\n')
file_wr.write('                        <ul class="nav navbar-nav ml-auto">\n')
file_wr.write('&nbsp&nbsp\n')
file_wr.write('                        </ul>\n')
file_wr.write('                    </div>\n')
file_wr.write('                </div><br><br>\n')
file_wr.write('            </nav>\n')
file_wr.write('<br> \n')
file_wr.write(' <head><center><h2 style="color:DarkGreen">ATC Suppressed/Suspend in RLAB Regression Testing</h2></center> <a href="http://aww.sh.bel.alcatel.be/tools/dslam/bm/buildlog/cgi-bin/TI_filter.cgi/" style="float: right;">TI Suppress tool</a>\n')
file_wr.write('<meta http-equiv="X-UA-Compatible" content="IE=edge">\n')
file_wr.write(' <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css" integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4" crossorigin="anonymous">\n')
file_wr.write('  <link rel="stylesheet" href="/home/akuma078/RemoteLab/welcome/static/style1.css"\n')
file_wr.write(' <!-- Font Awesome JS -->\n')
file_wr.write('    <script defer src="https://use.fontawesome.com/releases/v5.0.13/js/solid.js" integrity="sha384-tzzSw1/Vo+0N5UhStP3bvwWPq+uvzCMfrN1fEFe+xBmv1C/AtVX5K0uZtmcHitFZ" crossorigin="anonymous"></script>\n')
file_wr.write('    <script defer src="https://use.fontawesome.com/releases/v5.0.13/js/fontawesome.js" integrity="sha384-6OIrr52G08NpOFSZdxxz1xdNSndlD4vdcf/q2myIUVO0VsqaGHJsB0RaBE01VTOY" crossorigin="anonymous"></script>      \n')
file_wr.write('<script src="http://cdn.jsdelivr.net/webshim/1.12.4/extras/modernizr-custom.js"></script>\n')
file_wr.write('<!-- polyfiller file to detect and load polyfills -->\n')
file_wr.write('<script src="http://cdn.jsdelivr.net/webshim/1.12.4/polyfiller.js"></script>\n')
file_wr.write("</head>\n")
file_wr.write("<body>\n")
#file_wr.write('<a href="http://aww.sh.bel.alcatel.be/tools/dslam/bm/buildlog/cgi-bin/TI_filter.cg/" style="float: right;">TI Suppress tool</a>')
#file_wr.write('<center><h1>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp FR SMOKE SUPPRESSED</h1></center>')
#file_wr.write('<center>Last updated@: '+current_time+'</center>')
c=[]
with open("FR_final.txt") as fp:
        for line in fp:
                line=line.rstrip("\n").split(";")
                c.append(line[0])
lyns=[]
for x in c:
        if x not in lyns:
                lyns.append(x)
count=str(len(lyns))
file_wr.write('<center><h6> &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp Last updated@: '+current_time+'</center>  </h6>')
file_wr.write(' <br>')
file_wr.write(' <style="float: right;>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp Unique Test Case Count: '+count+'</style>')
file_wr.write('<button style="float: right"')
file_wr.write(' onclick="exportTableToExcel')
file_wr.write("('tblData')")
file_wr.write('">Export to xsl</button> &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp')
#file_wr.write('<p align="right"><a href="http://aww.sh.bel.alcatel.be/tools/dslam/bm/buildlog/cgi-bin/TI_filter.cgi/">TI Suppress tool</a></p>')

file_wr.write("<hr />\n")
file_wr.write('<center><table border color "blue" bgcolor="white" border=1 id="tblData">\n')
file_wr.write('<tr><td height="40" width="400"><b>&nbsp&nbspTestcase</b></td><td><b>&nbsp&nbsp FR Id</b></td><td><b>&nbsp&nbsp TimeState</b></td><td><b>&nbsp&nbsp Release Setup</b></td><td><b>&nbsp&nbsp ATC/SW</b></td><td><b>&nbsp&nbsp SUP/SUS DATE</b></td><td width="100"><b>&nbsp&nbsp SUP/SUS</b></td><td><b>&nbsp&nbsp Pending Days</b></td></tr>\n')

with open("FR_final.txt") as fp:
	for line in fp:
		line=line.rstrip("\n").split(";")
		file_wr.write('    <tr><td height="40"><center>'+line[0]+'</center></td><td ><center>'+line[1]+'</center></td><td ><center>'+line[2]+'</center></td><td ><center>'+line[3]+'</center></td><td ><center>'+line[4]+'</center></td><td ><center> '+line[5]+'</center></td><td ><center>'+line[6]+'</center></td>  <td ><center> '+line[7]+'</center></td></tr>\n')
file_wr.write("</table></center>\n")
file_wr.write("\n")
file_wr.write("\n")
file_wr.write("<hr/>\n")
file_wr.write("</body>\n")
file_wr.write("</html>\n")
file_wr.close()

FRnotificationemail()
