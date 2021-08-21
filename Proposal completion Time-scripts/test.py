#!/usr/bin/python
import cgitb
import cgi, cgitb ,sys
cgitb.enable()

html='''
<html>
<body>
<body bgcolor="#E6E6FA">
<center><h1 style="background-color:#3cb371;"> Proposal Completion Time</center>
<center><h2>Enter the Required Date</h2></center>
<form action="/cgi-bin/get.py" method="get">
   <center>Date: <input type="text" name="date"></center>
   <center><input type="submit" value="submit"></center>
</form>
</body>
</html>'''
print(html)
#print(date)


