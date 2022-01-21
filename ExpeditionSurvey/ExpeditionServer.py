import os
import bottle
from bottle import static_file
from bottle.ext import sqlite

app = bottle.Bottle()
plugin = bottle.ext.sqlite.Plugin(os.path.join(os.path.dirname(__file__), 'ExpeditionSurvey.db'))
app.install(plugin)


def ff3(n: float) -> str:
    return '{:.3f}'.format(n)



@app.route('/css/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root='css')




@app.route('/')
def body(db):
    # Provide a summary of the expedition statistics.
    cur = db.cursor()

    cur.execute('select StarType, count(BodyID) as total from stars group by StarType order by total desc')
    stars = []
    for row in cur.fetchall():
        stars.append(row)

    cur.execute('select PlanetClass, count(BodyID) as total from bodies group by PlanetClass order by total desc')
    bodies = []
    for row in cur.fetchall():
        bodies.append(row)

    cur.execute('select Type, sum(count) as total from signals group by Type order by total desc')
    signals = []
    for row in cur.fetchall():
        signals.append(row)

    cur.execute('select count(timestamp), count(distinct SystemAddress), sum(JumpDist),sum(FuelUsed) from jumps')
    row = cur.fetchone()
    jumps = row[0]
    systems = row[1]
    distance = row[2]
    fuel = row[3]

    cur.execute('select PlanetClass, count(BodyID) as total from bodies where Scanned=1 group by PlanetClass order by total desc')
    scannedbodies = []
    for row in cur.fetchall():
        scannedbodies.append(row)

    cur.execute('select StarType, count(BodyID) as total from stars where WasDiscovered=0 group by StarType order by total desc')
    newstars = []
    for row in cur.fetchall():
        newstars.append(row)

    cur.execute('select PlanetClass, count(BodyID) as total from bodies where WasDiscovered=0 group by PlanetClass order by total desc')
    newbodies = []
    for row in cur.fetchall():
        newbodies.append(row)

    return bottle.template('summary', stars=stars, jumps=jumps, bodies=bodies, signals=signals, systems=systems, distance=ff3(distance), fuel=ff3(fuel), scannedbodies=scannedbodies, newstars=newstars, newbodies=newbodies)




@app.route('/jumps')
def body(db):
    cur = db.cursor()

    cur.execute('select jumps.Timestamp, jumps.SystemAddress, systems.StarSystem, jumps.JumpDist, jumps.FuelUsed, systems.BodyCount, StarCount from jumps left join systems on jumps.SystemAddress=systems.SystemAddress left join (select SystemAddress, count(stars.BodyID) as StarCount from stars group by SystemAddress) a on jumps.SystemAddress=a.SystemAddress order by Timestamp')
    jumps = []
    for row in cur.fetchall():
        starcount = 0 if row[6] is None else row[6]
        jumps.append([ row[0], row[1], row[2], ff3(row[3]), ff3(row[4]), row[5], starcount, row[5] - starcount ])

    return bottle.template('jumps', jumps=jumps)




@app.route('/systems')
def body(db):
    cur = db.cursor()
    #cur.execute('select jumps.Timestamp, jumps.SystemAddress, systems.StarSystem, jumps.JumpDist, jumps.FuelUsed, systems.BodyCount, StarCount from jumps left join systems on jumps.SystemAddress=systems.SystemAddress left join (select SystemAddress, count(stars.BodyID) as StarCount from stars group by SystemAddress) a on jumps.SystemAddress=a.SystemAddress')
    cur.execute('select * from systems order by StarSystem')

    systems = []

    for row in cur.fetchall():
        bodycount = 0 if row[5] is None else row[5]
        systems.append([ row[0], row[1], ff3(row[2]), ff3(row[3]), ff3(row[4]), bodycount ])

    return bottle.template('systems', systems=systems)




@app.route('/system/<system:int>')
def body(system, db):
    # Provide information about a specific system.
    cur = db.cursor()
    cur.execute('select * from systems where SystemAddress=?', (system,))

    #System
    row = cur.fetchone()
    systemdata = [ row[0], row[1], ff3(row[2]), ff3(row[3]), ff3(row[4]) ]

    # Stars
    cur.execute('select * from stars where SystemAddress=? order by BodyID', (system,))
    # This may return no rows if the system was not automatically scanned on entry, possibly because the commander has been there before.

    stars = []

    for row in cur.fetchall():
        stars.append(row)

    # Rings
    cur.execute('select * from rings where SystemAddress=? and ReserveLevel=? order by BodyID', (system, 'Unknown'))
    # This may return no rows if there are no asteroid belts around the stars or the system was not automatically scanned on entry.

    rings = []
    
    for row in cur.fetchall():
        rings.append(row)

    # Bodies
    cur.execute("select * from bodies where SystemAddress=? order by BodyID", (system,))
    # This may return no rows if there are no bodies other than stars, or the discovery scanner or full spectrum scanner was not used.

    bodies = []

    for row in cur.fetchall():
        bodies.append([ row[0], row[1], row[2], ff3(row[3]), row[4], row[5], row[6], row[7], ff3(row[8]), ff3(row[9]), ff3(row[10]), ff3(row[11]), ff3(row[12]), row[13], row[14], row[15], row[16] ])

    return bottle.template('system', system=systemdata, stars=stars, rings=rings, bodies=bodies)




@app.route('/body/<system:int>/<bodyid:int>')
def body(system, bodyid, db):
    cur = db.cursor()
    cur.execute("select * from bodies where SystemAddress=? and BodyID=?", (system, bodyid))

    row = cur.fetchone()
    body = [ row[0], row[1], row[2], ff3(row[3]), row[4], row[5], row[6], row[7], ff3(row[8]), ff3(row[9]), ff3(row[10]), ff3(row[11]), ff3(row[12]), row[13], row[14], row[15], row[16] ]

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
        rings.append([ row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10] ])

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
def body(discovered, db):
    cur = db.cursor()

    # Stars
    cur.execute('select * from stars where WasDiscovered=? order by SystemAddress, BodyName', (discovered,))

    stars = []

    for row in cur.fetchall():
        stars.append([ row[0], row[1], row[2], ff3(row[3]), row[4], row[5], ff3(row[6]), ff3(row[7]), ff3(row[8]), row[9], row[10], row[11], row[12], row[13] ])

    # Bodies
    cur.execute('select * from bodies where WasDiscovered=? order by SystemAddress, BodyName', (discovered,))

    bodies = []

    for row in cur.fetchall():
        bodies.append([ row[0], row[1], row[2], ff3(row[3]), row[4], row[5], row[6], row[7], ff3(row[8]), ff3(row[9]), ff3(row[10]), ff3(row[11]), ff3(row[12]), row[13], row[14], row[15], row[16] ])

    return bottle.template('discovered', stars=stars, bodies=bodies, discovered=discovered)




@app.route('/planet/terraformable/<terraform:re:.*>')
def body(terraform, db):
    cur = db.cursor()

    cur.execute('select * from bodies where TerraformState=? order by SystemAddress, BodyName', (terraform,))

    bodies = []

    for row in cur.fetchall():
        bodies.append([ row[0], row[1], row[2], ff3(row[3]), row[4], row[5], row[6], row[7], ff3(row[8]), ff3(row[9]), ff3(row[10]), ff3(row[11]), ff3(row[12]), row[13], row[14], row[15], row[16] ])

    return bottle.template('terraformable', bodies=bodies, title=f"{terraform} Bodies")




@app.route('/planet/class/<planetclass:re:.*>')
def body(planetclass, db):
    cur = db.cursor()

    cur.execute('select * from bodies where PlanetClass=? order by SystemAddress, BodyName', (planetclass,))

    bodies = []

    for row in cur.fetchall():
        bodies.append([ row[0], row[1], row[2], ff3(row[3]), row[4], row[5], row[6], row[7], ff3(row[8]), ff3(row[9]), ff3(row[10]), ff3(row[11]), ff3(row[12]), row[13], row[14], row[15], row[16] ])

    return bottle.template('terraformable', bodies=bodies, title=f"Planet Class: {planetclass}")




@app.route('/planet/atmosphere/<atmosphere:re:.*>')
def body(atmosphere, db):
    cur = db.cursor()

    cur.execute('select * from bodies where Atmosphere=? order by SystemAddress, BodyName', (atmosphere,))

    bodies = []

    for row in cur.fetchall():
        bodies.append([ row[0], row[1], row[2], ff3(row[3]), row[4], row[5], row[6], row[7], ff3(row[8]), ff3(row[9]), ff3(row[10]), ff3(row[11]), ff3(row[12]), row[13], row[14], row[15], row[16] ])

    return bottle.template('terraformable', bodies=bodies, title=f"Planet Atmosphere: {atmosphere}")




@app.route('/planet/volcanism/<volcanism:re:.*>')
def body(volcanism, db):
    cur = db.cursor()

    cur.execute('select * from bodies where Volcanism=? order by SystemAddress, BodyName', (volcanism,))

    bodies = []

    for row in cur.fetchall():
        bodies.append([ row[0], row[1], row[2], ff3(row[3]), row[4], row[5], row[6], row[7], ff3(row[8]), ff3(row[9]), ff3(row[10]), ff3(row[11]), ff3(row[12]), row[13], row[14], row[15], row[16] ])

    return bottle.template('terraformable', bodies=bodies, title=f"Planet Volcanism: {volcanism}")




@app.route('/planet/landable/<landable:re:.*>')
def body(landable, db):
    cur = db.cursor()

    cur.execute('select * from bodies where Landable=? order by SystemAddress, BodyName', (landable,))

    bodies = []

    for row in cur.fetchall():
        bodies.append([ row[0], row[1], row[2], ff3(row[3]), row[4], row[5], row[6], row[7], ff3(row[8]), ff3(row[9]), ff3(row[10]), ff3(row[11]), ff3(row[12]), row[13], row[14], row[15], row[16] ])

    return bottle.template('terraformable', bodies=bodies, title=f"Landable Planets: {landable}")




@app.route('/planet/mapped/<mapped:re:.*>')
def body(mapped, db):
    cur = db.cursor()

    cur.execute('select * from bodies where WasMapped=? order by SystemAddress, BodyName', (mapped,))

    bodies = []

    for row in cur.fetchall():
        bodies.append([ row[0], row[1], row[2], ff3(row[3]), row[4], row[5], row[6], row[7], ff3(row[8]), ff3(row[9]), ff3(row[10]), ff3(row[11]), ff3(row[12]), row[13], row[14], row[15], row[16] ])

    return bottle.template('terraformable', bodies=bodies, title=f"Previously Mapped Planets: {mapped}")




@app.route('/planet/scanned/<scanned:re:.*>')
def body(scanned, db):
    cur = db.cursor()

    cur.execute('select * from bodies where Scanned=? order by SystemAddress, BodyName', (scanned,))

    bodies = []

    for row in cur.fetchall():
        bodies.append([ row[0], row[1], row[2], ff3(row[3]), row[4], row[5], row[6], row[7], ff3(row[8]), ff3(row[9]), ff3(row[10]), ff3(row[11]), ff3(row[12]), row[13], row[14], row[15], row[16] ])

    return bottle.template('terraformable', bodies=bodies, title=f"Scanned Planets: {scanned}")




app.run(reloader=True, host='localhost', port=8002, debug=True)
