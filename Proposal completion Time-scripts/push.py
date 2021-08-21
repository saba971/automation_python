import os,re,urllib,urllib2
import re
import time
import datetime
import paramiko
import os
import os.path
import commands
import shutil
import MySQLdb
import operator
from functools import reduce
list1=[]
list2=[]
list3=[]
list4=[]
list6=[]
list7=[]
list8=[]
first=[]
pull=[]
second=[]
mylist1=[]
db = MySQLdb.connect("localhost","root","bgc8g343437","sabadb")
cursor = db.cursor()
def hour(n):
        days = n // 86400
        hours = n // 3600 % 24
        minutes = n // 60 % 60
        seconds = n % 60
        return hours
def minute(n):
        days = n // 86400
        hours = n // 3600 % 24
        minutes = n // 60 % 60
        seconds = n % 60
        return minutes
#super batch cose --------------------------------------------------------------------------->
print("super-batch start")
url="http://bldsrv014.be.alcatel-lucent.com:9082/view/MS_PULLME/job/MSHS_FTP-superbatch-request/lastBuild/api/python"
print url
stage_name_check= eval(urllib.urlopen(url).read())
for i in range(0,len(stage_name_check["actions"])):
        #print i
        if stage_name_check["actions"][i]["_class"] == "hudson.model.CauseAction" :
                stage_name_upstreamProject=stage_name_check["actions"][i]["causes"][0]["upstreamProject"]
                stage_name_upstreamBuild=stage_name_check["actions"][i]["causes"][0]["upstreamBuild"]
                break
print stage_name_upstreamProject
print stage_name_upstreamBuild
print stage_name_check["timestamp"]
print stage_name_check["displayName"]
#if(os.path.isfile"%s"%stage_name_check["displayName"]):
time=stage_name_check["timestamp"]
time=time/1000
print(time)
#time = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
time=str(time)
#print time
#build_id=stage_name_check["displayName"]+":"+time
build_id=int(stage_name_check["id"])
print(build_id)
n3=10
for i in range(0,n3):
        list4.append(build_id)
        build_id=build_id-1
print(list3)
for i in range(0,len(list4)):
         list4[i]=str(list4[i])
for i in list4:
        url='http://bldsrv014.be.alcatel-lucent.com:9082/view/MS_PULLME/job/MSHS_FTP-superbatch-request/'+i+'/api/python'
        print(url)
        stage_name_check= eval(urllib.urlopen(url).read())
        build_name3= stage_name_check["displayName"]
	time=stage_name_check["timestamp"]
        time=int(time)
        time=time/1000
        #print(time)
        #time = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
        time=str(time)
        print(time)
        #time1=hour(time)
        #print(time1)
        build_id1=stage_name_check["displayName"]+":"+time
	mylist1.append(build_id1)
for i in mylist1:
	i=i.split(":")[0]
	pull.append(i)
print(pull)
#push code-------------------------------------------------------------------------------->
'''
for root, dirs, files in os.walk("/var/www/cgi-bin/sample"):
    for filename in files:
        mylist1.append(filename)

for root, dirs, files in os.walk("/var/www/cgi-bin/sample"):
    for filename in files:
        filename=filename.split(":")[0]
        pull.append(filename)
print(pull)
'''
#push code
url="http://bldsrv014.be.alcatel-lucent.com:9082/view/MS_PULLME/job/MSHS_Push-2-central/lastBuild/api/python"
print(url)
stage_name_check= eval(urllib.urlopen(url).read())
m=stage_name_check["displayName"]
#pull.append(m)
#print(pull)
build_id=int(stage_name_check["id"])
n=3
for i in range(0,n):
        list1.append(build_id)
        build_id=build_id-1
print(list1)
for i in range(0,len(list1)):
        list1[i]=str(list1[i])
print"push"
for i in list1:
        url='http://bldsrv014.be.alcatel-lucent.com:9082/view/MS_PULLME/job/MSHS_Push-2-central/'+i+'/api/python'
        print(url)
        stage_name_check= eval(urllib.urlopen(url).read())
        build_name= stage_name_check["displayName"]
        time=stage_name_check["timestamp"]
        t1=time/1000
        #time = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
        #n=hour(t1)
        m1=str(t1)
        for i in pull:
                if build_name == i:
                        print(i)
                        q=i+":"+m1
                        list8.append(q)
                        print("insert")
                else:
                        pass
url2="http://bldsrv014.be.alcatel-lucent.com:9082/view/MS_PULLME/job/Mainstream-Pull-me-strip/lastBuild/api/python"
print(url2)
stage_name_check= eval(urllib.urlopen(url2).read())
build_id2=int(stage_name_check["id"])
n=3
for i in range(0,n):
        list2.append(build_id2)
        build_id2=build_id2-1
print(list2)
for i in range(0,len(list2)):
        list2[i]=str(list2[i])
print"strip1"
for i in list2:
        url='http://bldsrv014.be.alcatel-lucent.com:9082/view/MS_PULLME/job/Mainstream-Pull-me-strip/'+i+'/api/python'
        print(url)
        stage_name_check= eval(urllib.urlopen(url).read())
        build_name2= stage_name_check["displayName"]
        time=stage_name_check["timestamp"]
        t2=time/1000
        #time = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
        #time=str(time)
        #m2=hour(t2)
        m2=str(t2)
        print(m2)
        for i in pull:
                if build_name2 == i:
                        print(i)
                        r=i+":"+m2
                        list8.append(r)
                        print("insert")
                else:
                        pass
url3="http://bldsrv014.be.alcatel-lucent.com:9082/view/MS_PULLME/job/Hardening_Pull-me-strip/lastBuild/api/python"
print(url3)
stage_name_check= eval(urllib.urlopen(url3).read())
build_id3=int(stage_name_check["id"])
n4=3
for i in range(0,n4):
        list3.append(build_id3)
        build_id3=build_id3-1
print(list3)
for i in range(0,len(list3)):
        list3[i]=str(list3[i])
print"strip2"
for i in list3:
        url='http://bldsrv014.be.alcatel-lucent.com:9082/view/MS_PULLME/job/Hardening_Pull-me-strip/'+i+'/api/python'
        print(url)
        stage_name_check= eval(urllib.urlopen(url).read())
        build_name3= stage_name_check["displayName"]
        time=stage_name_check["timestamp"]
        t3=time/1000
        #time = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
        #time = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
        #time=str(time)
        #m3=hour(t3)
        m3=str(t3)
        print(m3)
        for i in pull:
                if build_name3 == i:
                        print(i)
                        s=i+":"+m3
                        list8.append(s)
                        print("insert")
                else:
                        pass
print(mylist1)
print(list8)
p1=[]
p2=[]
p3=[]
p4=[]
p5=[]
for i in mylist1:
        i=i.split(":")[0]
        p1.append(i)
#print(p1)
for i in list8:
        i=i.split(":")[0]
        p2.append(i)
#print(p2)
for element in p1:
    if element in p2:
        p3.append(element)
#print(p3)
for i in list8:
        q=i.split(":")[0]
        for j in mylist1:
                r=j.split(":")[0]
                if q in r:
                        t=j+":"+i.split(":")[1]
                        p4.append(t)

print(p4)
for i in p4:
        f=int(i.split(":")[2])-int(i.split(":")[1])
        #print(f)
        h=hour(f)
        #print(h)
        m=minute(f)
        #print(m)
	m=str(m)
	if len(m)<2:
		m="0"+m
		m=str(m)
        tot=str(h)+"."+str(m)
        tot=str(tot)
        i=i+":"+tot
        p5.append(i)
print(p5)
dbs=[]
dbs=p5[:]
print(dbs)
concatstr = "["
concatstr2 = "["
concatstr3 = "["
concatstr4 = ""
build_type="Build Completion Time"
for i in p5:
        disp=i.split(":")[0]
        l=i.split(":")[3]
        concatstr =concatstr +"["+"'"+ disp +"'"+","+l+"],"
concatstr=concatstr[:-1]
concatstr=concatstr+"]"
print(concatstr)
for i in p5:
	disp2=i.split(":")[0]
	l1=i.split(":")[3]
	concatstr2=concatstr2 +"'"+ disp2 +"'"+","
	concatstr3=concatstr3 + l1 +","
concatstr2=concatstr2[:-1]
concatstr3=concatstr3[:-1]
concatstr2=concatstr2+"]"
concatstr3=concatstr3+"]"
print("concatstr2"+concatstr2)
print("concatstr3"+concatstr3)
for i in p5:
        disp3=i.split(":")[0]
        l2=i.split(":")[3]
        concatstr4 = concatstr4 + "{ y: "+l2+", label :'"+ disp3 +"'},"
concatstr4=concatstr4[:-1]
concatstr4=concatstr4
print("concatstr4"+concatstr4)
#Database Storage  script---------------------------------------------------------------->>
print(dbs)
p7=[]
que="SELECT max(s_no)from tgraph"
cursor.execute(que)
row=cursor.fetchone()
jid=row[0]
print(jid)
sm1_det="select builds from tgraph"
cursor.execute(sm1_det)
row=cursor.fetchall()
tup=[]
for i in row:
	tup.append(i)
print(tup)
p7=list(reduce(operator.concat, tup))
print(p7)
p8=[]
try:
	count=0
	for i in dbs:
		bld=i.split(":")[0]
		p8.append(bld)
		st_time=i.split(":")[1]
		st_time=int(st_time)
		st_time=datetime.datetime.fromtimestamp(st_time).strftime('%d-%m-%Y %H:%M:%S')
		date=st_time.split(" ")[0]
		en_time=i.split(":")[2]
		en_time=int(en_time)
		en_time=datetime.datetime.fromtimestamp(en_time).strftime('%d-%m-%Y %H:%M:%S')
		tot_time=i.split(":")[3]
		print(bld)
		for j in p7:
			if j==bld:
				count=1
				#print(bld)
				#print("insert")
				#jid=jid+1
				#print(jid)
				#sm1_det="insert into tgraph values('%s','%s','%s','%s','%s')" % (jid,bld,st_time,en_time,tot_time)
				#cursor.execute(sm1_det)
			#else:
				#print("insert")
				#jid=jid+1
				#sm1_det="insert into tgraph values('%s','%s','%s','%s','%s')" % (jid,bld,st_time,en_time,tot_time)
				#cursor.execute(sm1_det)
		if(count==0):
			jid=jid+1
			print(jid)
			sm1_det="insert into tgraph values('%s','%s','%s','%s','%s','%s')" % (jid,bld,st_time,en_time,tot_time,date)
			cursor.execute(sm1_det)		
except Exception as e:
        print(e)

db.commit()
db.close()
#End--------------------------------------------------------------------------------------->>
file_wr=open("s1.html",'w')
#file_wr.write("<html><head><script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js\"></script><script src=\"http://code.highcharts.com/highcharts.js\"></script><script src=\"http://code.highcharts.com/modules/exporting.js\"></script><style>a{border: 1px solid gray;border-radius: 10px;padding: 10px;text-decoration:none;float:left;margin:4px;text-align:center;display: block;color: green;}</style><script>$(function(){var chartype='line';var chartTitle='line Chart';var chartCategories = ['DAY1', 'DAY2', 'DAY3', 'DAY4', 'DAY5'];var chartData= [{name: 'Year 1800',data: [110, 31, 635, 203, 2]}, {name: 'Year 1900',data: [133, 156, 947, 408, 6]}, {name: 'Year 2008',data: [973, 914, 4054, 732, 34]}];setDynamicChart(chartype, chartTitle, chartCategories, chartData);chartype = 'line';chartTitle= 'Platform Utilization Percent';chartData= [{type: 'pie',name: 'Utilization percent',data:"+concatstr +";setDynamicChart(chartype, chartTitle, chartCategories, chartData);function setDynamicChart(chartype, smoke, chartCategories, chartData){$('#container').highcharts({chart: {type: chartype},title: {text: chartTitle},xAxis: {categories: chartCategories},yAxis: {min: 0,title: {text: 'Utilization Time'}},plotOptions: {pie: {allowPointSelect: true,cursor: 'pointer'}},series: chartData});}});</script></head><body><div id=\"container\" style=\"width: 50%;min-width: 310px; height: 400px; margin: 0 auto\"></div></body>")
#file_wr.write("<html><head><script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js\"></script><script src=\"http://code.highcharts.com/highcharts.js\"></script><script src=\"http://code.highcharts.com/modules/exporting.js\"></script><style>a{border: 1px solid gray;border-radius: 10px;padding: 10px;text-decoration:none;float:left;margin:4px;text-align:center;display: block;color: green;}</style><script>$(function(){var chartype='column';var chartTitle='column chart';var chartCategories = ['DAY1', 'DAY2', 'DAY3', 'DAY4', 'DAY5'];var chartData= [{name: 'Year 1800',data: [110, 31, 635, 203, 2]}, {name: 'Year 1900',data: [133, 156, 947, 408, 6]}, {name: 'Year 2008',data: [973, 914, 4054, 732, 34]}];setDynamicChart(chartype, chartTitle, chartCategories, chartData);chartype = 'line';chartTitle= '"+build_type+" Utilization Chart';chartCategories = ['PLATFORMS', 'DAY2', 'DAY3', 'DAY4', 'DAY5', 'DAY6','DAY7'];chartData= "+concatstr +";setDynamicChart(chartype, chartTitle, chartCategories, chartData);function setDynamicChart(chartype, smoke, chartCategories, chartData){$('#container').highcharts({chart: {type: 'column'},title: {text: chartTitle},xAxis: {categories: chartCategories},yAxis: {min: 0,max: 50,tickInterval: 5,title: {text: 'UTILIZATION PERCENTS'}},plotOptions: {column: {pointWidth: 20,pointPadding: 0,groupPadding: 0,borderWidth: 0}},series: chartData});}});</script></head><body><div id=\"container\" style=\"width: 100%;min-width: 400px; height: 600px; margin: 0 auto\"></div></body>")
#file_wr.write("<html><head><script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js\"></script><script src=\"http://code.highcharts.com/highcharts.js\"></script><script src=\"http://code.highcharts.com/modules/exporting.js\"></script><div id=\"container\" style=\"min-width: 400px; height: 500px; margin: 0 auto\"></div><style>a{border: 1px solid gray;border-radius: 10px;padding: 10px;text-decoration:none;float:left;margin:4px;text-align:center;display: block;color: green;}</style><script> Highcharts.chart('container', {chart: {type: 'column' },title: {text: '"+build_type+"'},subtitle: {text: '' },xAxis: {type: 'category',labels: {rotation: -45,style: {fontSize: '13px', fontFamily: 'Verdana, sans-serif'}}},yAxis: { min: 0,title: {text: 'Time'}},legend: {enabled: false},tooltip: {pointFormat: 'Time: <b>{point.y:.1f} %</b>'},series: [{name: 'Population',data: "+concatstr+",dataLabels: {enabled: true,rotation: -90,color: '#FFFFFF',align: 'right',format: '{point.y:.1f}',y: 10,style: {fontSize: '13px',fontFamily: 'Verdana, sans-serif'}}}]});</script></head>")
#file_wr.write("<script src=\"https://code.jquery.com/jquery-3.1.1.min.js\"></script><script src=\"https://code.highcharts.com/highcharts.js\"></script><script src=\"https://cod.highcharts.com/highcharts-more.js\"></script><script src=\"https://code.highcharts.com/modules/exporting.js\"></script><div id=\"container\"></div><button id=\"plain\">Plain</button><button id=\"inverted\">Inverted</button><button id=\"polar\">Polar</button><style>#container {min-width: 320px;max-width: 600px;margin: 0 auto;}</style><script>var chart = Highcharts.chart('container', {title: {text: 'Build Completion Time'},subtitle: {text: 'Build'},xAxis: {categories: "+concatstr2+"},series: [{type: 'column',colorByPoint: true,data: "+concatstr3+",showInLegend: false}]});$('#plain').click(function () {chart.update({chart: {inverted: false,polar: false},subtitle: {text: 'Build'}});});$('#inverted').click(function () {chart.update({chart: {inverted: true,polar: false},subtitle: {text: 'Build'}});});$('#polar').click(function () {chart.update({chart: {inverted: false,polar: true},subtitle: {text: 'Polar'} });});</script>")
file_wr.write("<!DOCTYPE HTML><html><head>  <script>window.onload = function () {var chart = new CanvasJS.Chart(\"chartContainer\", {animationEnabled: true,title:{text:\"Build Completion Time\"},axisX:{interval: 1},axisY2:{interlacedColor: \"rgba(1,77,101,.2)\",gridColor: \"rgba(1,77,101,.1)\",title: \"Time\"},data: [{type: \"bar\",name: \"companies\",axisYType: \"secondary\",color: \"#014D65\",dataPoints: ["+concatstr4+"]}]});chart.render();}</script></head><body><div id=\"chartContainer\" style=\"height: 300px; width: 100%;\"></div><script src=\"https://canvasjs.com/assets/script/canvasjs.min.js\"></script></body></html>")

file_wr.close()
os.system('cp -rf "/var/www/cgi-bin/s1.html" "/var/www/html/s1.html"')

