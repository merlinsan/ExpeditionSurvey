import os
import bottle
from bottle import static_file
from bottle.ext import sqlite

app = bottle.Bottle()
plugin = bottle.ext.sqlite.Plugin(os.path.join(os.path.dirname(__file__), 'ExpeditionSurvey.db'))
app.install(plugin)

def ff3(n: float) -> str:
    return '{:.3f}'.format(n)

def boolean(n: int) -> str:
    return 'Yes' if n else 'No'

@app.route('/css/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root='css')

@app.route('/')
def jumps(db):
    cur = db.cursor()
#    cur.execute('select jumps.Timestamp, systems.SystemAddress, systems.StarSystem, jumps.JumpDist, jumps.FuelUsed, systems.BodyCount, count(stars.BodyID) from jumps left join systems on jumps.SystemAddress == systems.SystemAddress left join stars on jumps.SystemAddress == stars.SystemAddress group by jumps.SystemAddress order by jumps.Timestamp')
    cur.execute('select jumps.Timestamp, jumps.SystemAddress, systems.StarSystem, jumps.JumpDist, jumps.FuelUsed, systems.BodyCount, StarCount from jumps left join systems on jumps.SystemAddress=systems.SystemAddress left join (select SystemAddress, count(stars.BodyID) as StarCount from stars group by SystemAddress) a on jumps.SystemAddress=a.SystemAddress')
    jumps = []
    distance = 0.0
    fuel = 0.0

    for row in cur.fetchall():
        starcount = 0 if row[6] is None else row[6]
        jumps.append([ row[0], row[1], row[2], row[3], ff3(row[4]), row[5], starcount, row[5] - starcount ])
        distance +=  row[3]
        fuel += row[4]

    return bottle.template('jumps', jumps=jumps, distance=ff3(distance), fuel=ff3(fuel), totaljumps=len(jumps)-1 if len(jumps) else 0)

@app.route('/system/<system:int>')
def system(system, db):
    cur = db.cursor()
    cur.execute('select * from systems where SystemAddress=?', (system,))

    #System
    row = cur.fetchone()
    systemdata = [ row[0], row[1], ff3(row[2]), ff3(row[3]), ff3(row[4]) ]

    # Stars
    cur.execute('select * from stars where SystemAddress=? order by BodyID', (system,))

    stars = []

    for row in cur.fetchall():
        stars.append([ row[2], ff3(row[3]), row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], boolean(row[12]) ])

    # Rings
    cur.execute('select * from rings where SystemAddress=? and ReserveLevel=? order by BodyID', (system, 'Unknown'))

    rings = []
    
    for row in cur.fetchall():
        rings.append([ row[3], row[4], row[5], row[6], row[7], boolean(row[8]) ])

    # Bodies
    cur.execute("select * from bodies where SystemAddress=? order by BodyID", (system,))

    bodies = []

    for row in cur.fetchall():
        bodies.append([ row[0], row[1], row[2], ff3(row[3]), row[4], row[5], row[6], row[7], ff3(row[8]), ff3(row[9]), ff3(row[10]), ff3(row[11]), ff3(row[12]), boolean(row[13]), boolean(row[14]), boolean(row[15]), boolean(row[16]) ])

    return bottle.template('system', system=systemdata, stars=stars, rings=rings, bodies=bodies)

@app.route('/body/<system:int>/<bodyid:int>')
def body(system, bodyid, db):
    cur = db.cursor()
    cur.execute("select * from bodies where SystemAddress=? and BodyID=?", (system, bodyid))

    row = cur.fetchone()
    body = [ row[0], row[1], row[2], ff3(row[3]), row[4], row[5], row[6], row[7], ff3(row[8]), ff3(row[9]), ff3(row[10]), ff3(row[11]), ff3(row[12]), boolean(row[13]), boolean(row[14]), boolean(row[15]), boolean(row[16]) ]

    # body composition
    cur.execute('select * from composition where SystemAddress=? and BodyID=? order by Percent Desc', (system, bodyid))
    # ( SystemAddress INTEGER, BodyID INTEGER, BodyName TEXT, Name TEXT, Percent REAL )
    # probably 3 rows

    composition = []

    for row in cur.fetchall():
        composition.append([ row[3], ff3(row[4]) ])
    
    # atmospheric composition
    cur.execute('select * from atmospherecomposition where SystemAddress=? and BodyID=? order by Percent Desc', (system, bodyid))
    # ( SystemAddress INTEGER, BodyID INTEGER, BodyName TEXT, name TEXT, percent REAL )
    # 0 or more rows

    atmosphere = []

    for row in cur.fetchall():
        atmosphere.append([ row[3], ff3(row[4]) ])

    # landings
    cur.execute('select * from landings where SystemAddress=? and BodyID=? order by Timestamp', (system, bodyid))
    # ( SystemAddress INTEGER, BodyID INTEGER, BodyName TEXT, Latitude REAL, Longitude REAL, Timestamp TEXT )
    # 0 or more rows

    landings = []

    for row in cur.fetchall():
        landings.append([ ff3(row[3]), ff3(row[4]), row[5] ])

    # materials
    cur.execute('select * from materials where SystemAddress=? and BodyID=? order by Percent Desc', (system, bodyid))
    # ( SystemAddress INTEGER, BodyID INTEGER, BodyName TEXT, Name TEXT, Percent REAL )
    # 0 or more rows

    materials = []

    for row in cur.fetchall():
        materials.append([ row[3], ff3(row[4]) ])

    # rings
    cur.execute('select * from rings where SystemAddress=? and BodyID=? order by Name', (system, bodyid))
    # ( SystemAddress INTEGER, BodyID INTEGER, BodyName TEXT, Name TEXT, RingClass TEXT, MassMT REAL, InnerRad REAL, OuterRad REAL, WasDiscovered INTEGER, WasMapped INTEGER, ReserveLevel TEXT )
    # 0 or more rows

    rings = []

    for row in cur.fetchall():
        rings.append([ row[3], row[4], row[5], row[6], row[7], boolean(row[8]), boolean(row[9]), row[10] ])

    # screenshots
    # cur.execute('select * from screenshots where SystemAddress=? and BodyID=?', (system, bodyid))
    # ( Filename TEXT, System TEXT, Body TEXT )
    # 0 or more rows
    # row = None
    # screenshots = []

    # while row := cur.fetchone():
    #    screenshots.append([ row[0] ])

    # signals
    cur.execute('select * from signals where SystemAddress=? and BodyID=? order by Type', (system, bodyid))
    # ( SystemAddress INTEGER, BodyID INTEGER, BodyName TEXT, Type TEXT, Count INTEGER )
    # 0 or more rows

    signals = []

    for row in cur.fetchall():
        signals.append([ row[3], row[4] ])

    return bottle.template('body', body=body, composition=composition, atmosphere=atmosphere, landings=landings, materials=materials, rings=rings, signals=signals)

@app.route('/discovered/<discovered:int>')
def discovered(discovered, db):
    cur = db.cursor()

    # Stars
    cur.execute('select * from stars where WasDiscovered=? order by SystemAddress, BodyName', (discovered,))

    stars = []

    for row in cur.fetchall():
        stars.append([ row[0], row[1], row[2], ff3(row[3]), row[4], row[5], ff3(row[6]), ff3(row[7]), ff3(row[8]), row[9], row[10], row[11] ])

    # Bodies
    cur.execute('select * from bodies where WasDiscovered=? order by SystemAddress, BodyName', (discovered,))

    bodies = []

    for row in cur.fetchall():
        bodies.append([ row[0], row[1], row[2], ff3(row[3]), row[4], row[5], row[6], row[7], ff3(row[8]), ff3(row[9]), ff3(row[10]), ff3(row[11]), ff3(row[12]), boolean(row[13]), boolean(row[14]), boolean(row[15]), boolean(row[16]) ])

    return bottle.template('discovered', stars=stars, bodies=bodies, discovered=discovered)

@app.route('/terraformable/<terraform:int>')
def body(terraform, db):
    cur = db.cursor()

    cur.execute('select * from bodies where TerraformState=? order by SystemAddress, BodyName', ('Terraformable' if terraform==1 else 'Not Terraformable',))

    bodies = []

    for row in cur.fetchall():
        bodies.append([ row[0], row[1], row[2], ff3(row[3]), row[4], row[5], row[6], row[7], ff3(row[8]), ff3(row[9]), ff3(row[10]), ff3(row[11]), ff3(row[12]), boolean(row[13]), boolean(row[14]), boolean(row[15]), boolean(row[16]) ])

    return bottle.template('terraformable', bodies=bodies, title='Terraformable Bodies' if terraform==1 else 'Non-terraformable Bodies')

@app.route('/planetclass/<pclass:re:.*>')
def body(pclass, db):
    cur = db.cursor()

    cur.execute('select * from bodies where PlanetClass=? order by SystemAddress, BodyName', (pclass,))

    bodies = []

    for row in cur.fetchall():
        bodies.append([ row[0], row[1], row[2], ff3(row[3]), row[4], row[5], row[6], row[7], ff3(row[8]), ff3(row[9]), ff3(row[10]), ff3(row[11]), ff3(row[12]), boolean(row[13]), boolean(row[14]), boolean(row[15]), boolean(row[16]) ])

    return bottle.template('terraformable', bodies=bodies, title='Planet Classification')

app.run(reloader=True, host='localhost', port=8002, debug=True)
