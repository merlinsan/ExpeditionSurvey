#! python

import os
import sys
import sqlite3
import cgi, cgitb

def header() -> None:
	print("Content-type: text/html\n\n")
	print("<html><head><link rel='stylesheet' href='/css/stats.css'><title>Expedition Survey</title></head><body>")

def footer() -> None:
	print("</body></html>")


cwd = os.getcwd()
dbfile = f"{cwd}\ExpeditionSurvey.db"

dbopen  = False

if not os.path.exists(dbfile):
	header()
	print(f"<p>Database {dbfile} does not exist.")
	footer()
	sys.exit()

try:
	conn	= sqlite3.connect(dbfile)
	cur		= conn.cursor()
	dbopen	= True
except Error as error: # occurs when it is not possible to open or create a database
	header()
	print(f"<p>Database {dbfile} could not be opened.</p>")
	print(f"<p>{error}</p>")
	footer()
	sys.exit()

form = cgi.FieldStorage()
sys = form.getvalue('sys')

# html to be sent to browser
# header
header()
#print('Content-type: text/html\n\n')
#print("<html>")
#print("<head>")
#print("<title>Expedition Survey</title>")
#print("</head>")
#print("<body>")

# body content
if sys is None:
	print("<h4>List of jumps made</h4>")
	print("<table>")
	print("<tr><th style='text-align:left'>Date/Time</th><th style='text-align:left'>System</th><th style='text-align:right'>Distance</th><th style='text-align:right'>Fuel Used</th></tr>")

	sql = "select jumps.timestamp, jumps.SystemAddress, systems.StarSystem, jumps.JumpDist, jumps.FuelUsed from jumps, systems where jumps.SystemAddress = systems.SystemAddress"
	for row in cur.execute(sql):
		print(f"<tr><td style='text-align:left'>{row[0]}</td><td style='text-align:left'><a href='/cgi-bin/stats.py?sys={row[1]}'>{row[2]}</a></td><td style='text-align:right'>{row[3]:.3f}</td><td style='text-align:right'>{row[4]:.03f}</td></tr>")

	print("</table>")

else:
	print("<p><a href='/cgi-bin/stats.py'>[Home]</a></p>")
	cur.execute("select * from systems where SystemAddress=?", (sys,))
	row = cur.fetchone()
	print("<h4>System Information:</h4>")
	print("<table>")
	print(f"<tr><td>System Address</td><td>{row[0]}</td></tr>")
	print(f"<tr><td>System Name</td><td>{row[1]}</td></tr>")
	print(f"<tr><td>Location (Sol)</td><td>X:{row[2]} Y:{row[3]} Z:{row[4]}</td></tr>")
	print("</table>")

	print("<h4>Stars</h4>")
	print("<table>")
	print("<tr>")
	cur.execute("select * from stars where SystemAddress=? order by BodyID", (sys,))
	for row in cur.fetchall():
		print("<td><table>")
		wasDiscovered = "Yes" if row[12] == 1 else "No"
		print(f"<tr><td colspan=2>{row[2]}</td></tr>")
		print(f"<tr><td>Distance from arrival point</td><td>{row[3]:.3f} LS</td></tr>")
		print(f"<tr><td>Type and Class</td><td>{row[4]} {row[5]}</td></tr>")
		print(f"<tr><td>Stellar Mass</td><td>{row[6]}</td></tr>")
		print(f"<tr><td>Radius</td><td>{row[7]} Km</td></tr>")
		print(f"<tr><td>Absolute Magnitude</td><td>{row[8]}</td></tr>")
		print(f"<tr><td>Age</td><td>{row[9]} Million Years</td></tr>")
		print(f"<tr><td>Surface Temperature</td><td>{row[10]} Kelvin</td></tr>")
		print(f"<tr><td>Luminosity</td><td>{row[11]}</td></tr>")
		print(f"<tr><td>Previously Discovered</td><td>{wasDiscovered}</td></tr>")
		print("</table></td>")
	print("</tr></table>")

	print("<h4>Bodies</h4>")
	cur.execute("select * from bodies where SystemAddress=? order by BodyID", (sys,))
	rows = cur.fetchall()
	if len(rows) == 0:
		print("<p>No bodies</p>")
	else:
		print("<table>")
		print("<tr><th style='text-align:left'>Name</th><th style='text-align:right'>Distance (LS)</th><th style='text-align:left'>Terraformable</th><th style='text-align:left'>Class</th><th style='text-align:left'>Atmosphere</th><th style='text-align:left'>Volcanism</th><th style='text-align:right'>Mass(EM)</th><th style='text-align:right'>Radius</th><th style='text-align:right'>Gravity</th><th style='text-align:right'>Temperature</th><th style='text-align:right'>Pressure</th><th style='text-align:left'>Landable</th><th style='text-align:left'>Discovered</th><th style='text-align:left'>Mapped</th><th style='text-align:left'>Scanned</th></tr>")
		for row in rows:
			landable   = "Yes" if row[13] == 1 else "No"
			discovered = "Yes" if row[14] == 1 else "No"
			mapped     = "Yes" if row[15] == 1 else "No"
			scanned    = "Yes" if row[16] == 1 else "No"
			print(f"<tr><td>{row[2]}</td><td style='text-align:right'>{row[3]:.3f}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td><td>{row[7]}</td><td style='text-align:right'>{row[8]:.3f}</td><td style='text-align:right'>{row[9]:.3f}</td><td style='text-align:right'>{row[10]:.3f}</td><td style='text-align:right'>{row[11]:.3f}</td><td style='text-align:right'>{row[12]:.3f}</td><td>{landable}</td><td>{discovered}</td><td>{mapped}</td><td>{scanned}</td></tr>")
		print("</table><br>")

# footer
footer()
#print("</body>")
#print("</html>")
#end of html

if dbopen:
	conn.close()
