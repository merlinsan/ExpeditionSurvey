### Logging of systems for the "Celebration of Early Astronomy" expedition
# The information will be stored in a sqlite3 database for later reporting functions.

import logging
import os
import json
import sqlite3
from config import appname
from typing import Mapping, Any, List, Optional

plugin_name = os.path.basename(os.path.dirname(__file__))
print(plugin_name)

logger = logging.getLogger(f'{appname}.{plugin_name}')
if not logger.hasHandlers():
    level = logging.INFO
    logger.setLevel(level)
    logger_channel = logging.StreamHandler()
    logger_formatter = logging.Formatter(f'%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')
    logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    logger_formatter.default_msec_format = '%s.%03d'
    logger_channel.setFormatter(logger_formatter)
    logger.addHandler(logger_channel)

cwd = os.path.dirname(__file__)
dbfile = f"{cwd}\ExpeditionSurvey.db"

logger.info(f"Current working directory {cwd}, dbfile {dbfile}")

class This:
    # Holds modules global variables

    def __init__(self):
        self.dbopen   = False
        self.conn     = None
        self.cur      = None
        self.shutdown = False

        try:
            self.conn   = sqlite3.connect(dbfile)
            self.cur    = self.conn.cursor()
            self.dbopen = True
            logger.info("Database open")
        except sqlite3.Error as error:
            logger.critical(f"Database could not be opened: {error}")
            self.dbopen = False
        
        if self.dbopen:
            # the database may have been created if it did not exist, so create the tables if they do not exist.
            sql_create_atmospherecomp	= "CREATE TABLE IF NOT EXISTS atmospherecomposition ( SystemAddress INTEGER, BodyID INTEGER, BodyName TEXT, Name TEXT, Percent REAL, PRIMARY KEY(SystemAddress, BodyID,name) )"
            sql_create_bodies			= "CREATE TABLE IF NOT EXISTS bodies ( SystemAddress INTEGER, BodyID INTEGER, BodyName TEXT, DistanceFromArrivalLS REAL, TerraformState TEXT, PlanetClass TEXT, Atmosphere TEXT, Volcanism TEXT, MassEM REAL, Radius REAL, SurfaceGravity REAL, SurfaceTemperature REAL, SurfacePressure REAL, Landable INTEGER, WasDiscovered INTEGER, WasMapped INTEGER, Scanned INTEGER, PRIMARY KEY(SystemAddress,BodyID) )"
            sql_create_codexentries		= "CREATE TABLE IF NOT EXISTS codexentries ( EntryID INTEGER, Name TEXT, Category TEXT, SubCategory TEXT, IsNewEntry INTEGER, PRIMARY KEY(EntryID) )"
            sql_create_codexlocations	= "CREATE TABLE IF NOT EXISTS codexlocations ( EntryID INTEGER, SystemAddress INTEGER, Region TEXT, NearestDestination TEXT, PRIMARY KEY(SystemAddress,NearestDestination,EntryID) )"
            sql_create_codextraits		= "CREATE TABLE IF NOT EXISTS codextraits ( EntryID INTEGER, Trait TEXT, PRIMARY KEY(EntryID,Trait) )"
            sql_create_composition		= "CREATE TABLE IF NOT EXISTS composition ( SystemAddress INTEGER, BodyID INTEGER, BodyName TEXT, Name TEXT, Percent REAL, PRIMARY KEY(SystemAddress,BodyID,Name) )"
            sql_create_dockings			= "CREATE TABLE IF NOT EXISTS dockings ( SystemAddress INTEGER, MarketID INTEGER, Timestamp TEXT, StationName TEXT, PRIMARY KEY(Timestamp) )"
            sql_create_jumps			= "CREATE TABLE IF NOT EXISTS jumps ( Timestamp TEXT, SystemAddress INTEGER, JumpDist REAL, FuelUsed REAL )"
            sql_create_landings			= "CREATE TABLE IF NOT EXISTS landings ( SystemAddress INTEGER, BodyID INTEGER, BodyName TEXT, Latitude REAL, Longitude REAL, Timestamp TEXT )"
            sql_create_materials		= "CREATE TABLE IF NOT EXISTS materials ( SystemAddress INTEGER, BodyID INTEGER, BodyName TEXT, Name TEXT, Percent REAL, PRIMARY KEY(SystemAddress,BodyID,Name) )"
            sql_create_rings			= "CREATE TABLE IF NOT EXISTS rings ( SystemAddress INTEGER, BodyID INTEGER, BodyName TEXT, Name TEXT, RingClass TEXT, MassMT REAL, InnerRad REAL, OuterRad REAL, WasDiscovered INTEGER, WasMapped INTEGER, ReserveLevel TEXT, PRIMARY KEY(SystemAddress,BodyID,Name) )"
            sql_create_screenshots		= "CREATE TABLE IF NOT EXISTS screenshots ( Filename TEXT, System TEXT, Body TEXT )"
            sql_create_selldata		 	= "CREATE TABLE IF NOT EXISTS selldata ( Timestamp TEXT, BaseValue INTEGER, Bonus INTEGER )"
            sql_create_signals			= "CREATE TABLE IF NOT EXISTS signals ( SystemAddress INTEGER, BodyID INTEGER, BodyName TEXT, Type TEXT, Count INTEGER, PRIMARY KEY(SystemAddress,BodyID,Type) )"
            sql_create_stars			= "CREATE TABLE IF NOT EXISTS stars ( SystemAddress INTEGER, BodyID INTEGER, BodyName TEXT, DistanceFromArrivalLS REAL, StarType TEXT, Subclass INTEGER, StellarMass REAL, Radius REAL, AbsoluteMagnitude REAL, Age_MY INTEGER, SurfaceTemperature REAL, Luminosity TEXT, WasDiscovered INTEGER, WasMapped INTEGER, PRIMARY KEY(SystemAddress,BodyID) )"
            sql_create_systems			= "CREATE TABLE IF NOT EXISTS systems ( SystemAddress INTEGER, StarSystem TEXT, StarPosX REAL, StarPosY REAL, StarPosZ REAL, BodyCount INTEGER, AutoScan INTEGER DEFAULT 0, PRIMARY KEY(SystemAddress) )"

            try:
                self.cur.execute(sql_create_atmospherecomp)
                self.cur.execute(sql_create_bodies)
                self.cur.execute(sql_create_codexentries)
                self.cur.execute(sql_create_codexlocations)
                self.cur.execute(sql_create_codextraits)
                self.cur.execute(sql_create_composition)
                self.cur.execute(sql_create_dockings)
                self.cur.execute(sql_create_jumps)
                self.cur.execute(sql_create_landings)
                self.cur.execute(sql_create_materials)
                self.cur.execute(sql_create_rings)
                self.cur.execute(sql_create_screenshots)
                self.cur.execute(sql_create_selldata)
                self.cur.execute(sql_create_signals)
                self.cur.execute(sql_create_stars)
                self.cur.execute(sql_create_systems)
                self.conn.commit()
            except sqlite3.Error as error:
                self.conn.rollback()
                logger.critical(f"Database tables could not be created: {error}")
                self.conn.close()
                self.dbopen = False

this = This()


def plugin_start3(plugin_dir: str) -> str:
    # This is the first function called when the module is loaded
    logger.info("Started plugin ExpeditionSurvey")
    return "ExpeditionSurvey"


def plugin_stop() -> None:
    this.shutdown = True
    if this.dbopen:
        this.conn.close()


def store_system(SystemAddress: int, StarSystem: str, StarPosX: float, StarPosY: float, StarPosZ: float) -> None:
    sql_query = "insert or ignore into systems (SystemAddress, StarSystem, StarPosX, StarPosY, StarPosZ, BodyCount) values (?,?,?,?,?,?)"

    try:
        # BodyCount will be updated after a FSS scan complete
        this.cur.execute(sql_query, (SystemAddress, StarSystem, StarPosX, StarPosY, StarPosZ, 0))
        this.conn.commit()
        logger.debug(f"Added system {StarSystem}")
    except sqlite3.Error as error:
        this.conn.rollback()
        logger.error(f"Failed adding system {error} ({SystemAddress}, {StarSystem}, {StarPosX}, {StarPosY}, {StarPosZ}, 0)")


def store_jump(Timestamp: str, SystemAddress: int, JumpDist: float, FuelUsed: float) -> None:
    sql_query = "insert into jumps (Timestamp, SystemAddress, JumpDist, FuelUsed) values (?,?,?,?)"

    try:
        this.cur.execute(sql_query, (Timestamp, SystemAddress, JumpDist, FuelUsed))
        this.conn.commit()
        logger.debug(f"Added jump to {SystemAddress}")
    except sqlite3.Error as error:
        this.conn.rollback()
        logger.error(f"Failed adding jump {error} ({Timestamp}, {SystemAddress}, {JumpDist}, {FuelUsed})")


def store_star(SystemAddress: int, BodyID: int, BodyName: str, DistanceFromArrivalLS: float, StarType: str, Subclass: int, StellarMass: float, Radius: float, AbsoluteMagnitude: float, Age_MY: int, SurfaceTemperature: float, Luminosity: str, WasDiscovered: int, WasMapped: int):
    sql_query = "insert or ignore into stars (SystemAddress, BodyID, BodyName, DistanceFromArrivalLS, StarType, Subclass, StellarMass, Radius, AbsoluteMagnitude, Age_MY, SurfaceTemperature, Luminosity, WasDiscovered, WasMapped) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    try:
        this.cur.execute(sql_query, (SystemAddress, BodyID, BodyName, DistanceFromArrivalLS, StarType, Subclass, StellarMass, Radius, AbsoluteMagnitude, Age_MY, SurfaceTemperature, Luminosity, WasDiscovered, WasMapped))
        this.conn.commit()
        logger.debug(f"Added star {BodyName}")
    except sqlite3.Error as error:
        this.conn.rollback()
        logger.error(f"Failed adding star. {error} ({SystemAddress}, {BodyID}, {BodyName}, {DistanceFromArrivalLS}, {StarType}, {Subclass}, {StellarMass}, {Radius}, {AbsoluteMagnitude}, {Age_MY}, {SurfaceTemperature}, {Luminosity}, {WasDiscovered}, 0)")
        

def store_ring(SystemAddress: int, BodyID: int, BodyName: str, ring: List, WasDiscovered: bool, WasMapped: bool, ReserveLevel: str) -> None:
    sql_query = "insert or ignore into rings (SystemAddress, BodyID, BodyName, Name, RingClass, MassMT, InnerRad, OuterRad, WasDiscovered, WasMapped, ReserveLevel) values (?,?,?,?,?,?,?,?,?,?,?)"

    Name			= ring['Name']
    RingClass		= ring['RingClass'].replace('eRingClass_','')
    MassMT			= ring['MassMT']
    InnerRad		= ring['InnerRad'] / 1000 # convert to km
    OuterRad		= ring['OuterRad'] / 1000 # convert to km

    try:
        this.cur.execute(sql_query, (SystemAddress, BodyID, BodyName, Name, RingClass, MassMT, InnerRad, OuterRad, WasDiscovered, WasMapped, ReserveLevel))
        this.conn.commit()
        logger.debug(f"Added ring {BodyName} {Name}")
    except sqlite3.Error as error:
        this.conn.rollback()
        logger.error(f"Failed adding ring {error} ({SystemAddress}, {BodyID}, {BodyName}, {Name}, {RingClass}, {MassMT}, {InnerRad}, {OuterRad}, {WasDiscovered}, {WasMapped} {ReserveLevel})")


def journal_entry(cmdr: str, is_beta: bool, system: str, station: str, entry: Mapping[str, Any], state: Mapping[str, Any]) -> None:
    # This function is called when a journal entry is made indicating a change in state.
    # Check for the database being open first
    if not this.dbopen:
        return

    if entry['event'] not in ['Music', 'Loadout', 'Statistics', 'ReceiveText']: # ignore some noise
        logger.debug(entry)

    # Check for relevant entries and process accordingly
    if entry['event'] == 'Location' or entry['event'] == 'StartUp':
        logger.debug("Checking Location")
        # This is called to report the initial location of the player when starting EDMC
        # Use it to check the current location is stored in the database, particularly useful when a new database has been created.
        # It will not provide any information on bodies that would normally be done on a scan when jumping into a system.
        try:
            this.cur.execute("select Timestamp, SystemAddress from jumps order by Timestamp desc")
            row = this.cur.fetchone() # last jumped to
            if row == None or row[1] != entry['SystemAddress']: # either no jumps in database or the last jumped to system is not the same as that reported by Location
                logger.debug("Unmatched Location or no jumps")
                store_system(entry['SystemAddress'], entry['StarSystem'], entry['StarPos'][0], entry['StarPos'][1], entry['StarPos'][2])
                store_jump(entry['timestamp'], entry['SystemAddress'], 0.0, 0.0)  # store a jump of zero length to initialise the current location
            else:
                logger.debug("Last jumped to system is the same as location")
        except sqlite3.Error as error:
            logger.debug(f"Error reading last jump {error}")

    if entry['event'] == 'FSDJump':
        # This is called when jumping to a new system.
        # Create an instance of this system if it does not already exist
        # Create an instance of a jump into this system
        # Relevant keys :
        #	timestamp		: text
        #	SystemAddress	: integer
        #	StarSystem		: text
        #	StarPos			: array [x:real, y:real, z:real] (light years)
        #	JumpDist		: real (light years)
        #	FuelUsed		: real (tonnes)

        store_system(entry['SystemAddress'], entry['StarSystem'], entry['StarPos'][0], entry['StarPos'][1], entry['StarPos'][2])
        store_jump(entry['timestamp'], entry['SystemAddress'], entry['JumpDist'], entry['FuelUsed'])

    if entry['event'] == 'FSSDiscoveryScan':
        # This is called after the completion of the Discovery Scanner and provides a count of all the bodies in the system.
        # relevant keys :
        #	SystemAddress			: int
        #	BodyCount				: int

        SystemAddress	= entry['SystemAddress']
        BodyCount		= entry['BodyCount']

        sql_query = 'update or ignore systems set BodyCount=? where SystemAddress=?'
#		sql_data  =	( BodyCount, SystemAddress )

        try:
            this.cur.execute(sql_query, (BodyCount, SystemAddress))
            this.conn.commit()
            logger.debug(f"Updated body count for system {SystemAddress}")
        except sqlite3.Error as error:
            this.conn.rollback()
            logger.error(f"Failed updating body count for system. {error} ({SystemAddress}, {BodyCount})")

    if entry['event'] == 'Scan':
        # This is called when scanning a body either automatically or through the FSS.
        # This may be 'AutoScan' when entering the system, or 'Detailed' when done through the FSS or on approach to the body.
        # On some systems, there does not appear to be an AutoScan and the stars are not picked up.  Not sure if this is because I've been there before, or it is a populated system,
        # so need to add some functionality to check for stars not being discovered and then add them from another source, e.g. EDSM using their API.  This is probably best after the
        # FSSDiscoveryScan at which time all the stars should be identified.
        # relevant keys :
        #	timestamp				: text
        #	BodyName				: text
        #	BodyID					: integer
        #	StarSystem				: text
        #	SystemAddress			: integer
        #	DistanceFromArrivalLS	: real
        #	StarClass				: text
        #	Subclass				: int
        #	TerraformState			: text
        #	PlanetClass				: text
        #	Atmosphere				: text
        #	AtmosphereType			: text (possibly use this instead of Atmosphere value)
        #	AtmosphereComposition	: dictionary(Name:text, Percent:real)
        #	Volcanism				: text
        #	MassEM					: real
        #	StellarMass				: real
        #	AbsoluteMagnitude		: real
        #	Luminosity				: text
        #	Age_MY					: real
        #	Rings					: array
        #	Radius					: real (metres)
        #	SurfaceGravity			: real
        #	SurfaceTemperature		: real (kelvin)
        #	SurfacePressure			: real (pascals)
        #	Materials				: array
        #	Landable				: bool
        #	Composition				: dictionary(name,percent) 
        #	ReserveLevel			: text
        #	WasDiscovered			: bool
        #	WasMapped				: bool

        # Common parameters
        SystemAddress			= entry['SystemAddress']
        BodyID					= entry['BodyID']
        BodyName				= entry['BodyName']
        DistanceFromArrivalLS	= entry['DistanceFromArrivalLS']
        WasDiscovered			= entry['WasDiscovered']
        WasMapped				= entry['WasMapped']

        if 'ScanType' in entry and entry['ScanType'] == 'AutoScan':
            sql_query = "update systems set AutoScan = 1 where SystemAddress = ?"
            this.cur.execute(sql_query, (entry['SystemAddress'],))
            this.conn.commit()

        if 'StarType' in entry:
            StarType			= entry['StarType']
            Subclass			= entry['Subclass']
            StellarMass			= entry['StellarMass']
            Radius				= entry['Radius'] / 1000 # convert to km
            AbsoluteMagnitude	= entry['AbsoluteMagnitude']
            Age_MY				= entry['Age_MY']
            SurfaceTemperature	= entry['SurfaceTemperature']
            Luminosity			= entry['Luminosity']

            store_star(SystemAddress, BodyID, BodyName, DistanceFromArrivalLS, StarType, Subclass, StellarMass, Radius, AbsoluteMagnitude, Age_MY, SurfaceTemperature, Luminosity, WasDiscovered, WasMapped)

            if 'Rings' in entry:
                for ring in entry['Rings']:
                    store_ring(SystemAddress, BodyID, BodyName, ring, WasDiscovered, WasMapped, 'Unknown')

        elif 'PlanetClass' in entry:
            TerraformState		= entry['TerraformState'] if entry['TerraformState'] != "" else "Not Terraformable"
            PlanetClass			= entry['PlanetClass']
            Atmosphere			= entry['Atmosphere'].capitalize() if entry['Atmosphere'] != "" else "No Atmosphere"
            Volcanism			= entry['Volcanism'].capitalize() if entry['Volcanism'] != "" else "No Volcanism"
            MassEM				= entry['MassEM']
            Radius				= entry['Radius'] / 1000			# convert m to km
            SurfaceGravity		= entry['SurfaceGravity'] / 9.80665	# this then aligns with the value shown in ED body information
            SurfaceTemperature	= entry['SurfaceTemperature']		# kelvin
            SurfacePressure		= entry['SurfacePressure'] / 101325	# convert pascals to atmospheres
            Landable			= entry['Landable']
            # AtmosphereComposition (array name and percent)
            # TidalLock
            # Materials (array name and percent)
            # Composition
            # Rings
            # ReserveLevel

            sql_query = "insert or ignore into bodies (SystemAddress, BodyID, BodyName, DistanceFromArrivalLS, TerraformState, PlanetClass, Atmosphere, Volcanism, MassEM, Radius, SurfaceGravity, SurfaceTemperature, SurfacePressure, Landable, WasDiscovered, WasMapped, Scanned) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
#			sql_data  =                               (SystemAddress, BodyID, BodyName, DistanceFromArrivalLS, TerraformState, PlanetClass, Atmosphere, Volcanism, MassEM, Radius, SurfaceGravity, SurfaceTemperature, SurfacePressure, Landable, WasDiscovered, WasMapped, False)

            try:
                this.cur.execute(sql_query, (SystemAddress, BodyID, BodyName, DistanceFromArrivalLS, TerraformState, PlanetClass, Atmosphere, Volcanism, MassEM, Radius, SurfaceGravity, SurfaceTemperature, SurfacePressure, Landable, WasDiscovered, WasMapped, False))
                this.conn.commit()
                logger.debug(f"Added body {BodyName}")
            except sqlite3.Error as error:
                this.conn.rollback()
                logger.error(f"Failed adding body {error} ({SystemAddress}, {BodyID}, {BodyName}, {DistanceFromArrivalLS}, {TerraformState}, {PlanetClass}, {Atmosphere}, {Volcanism}, {MassEM}, {Radius}, {SurfaceGravity}, {SurfaceTemperature}, {SurfacePressure}, {Landable}, {WasDiscovered}, {WasMapped}, False)")

            if 'Rings' in entry :
                for ring in entry['Rings']:
                    ReserveLevel = entry['ReserveLevel']
                    store_ring(SystemAddress, BodyID, BodyName, ring, WasDiscovered, WasMapped, ReserveLevel)

            if 'Composition' in entry:
                composition = entry['Composition']
                sql_query = "insert or ignore into composition (SystemAddress, BodyID, BodyName, Name, Percent) values (?,?,?,?,?)"
#				sql_data  =                                    (SystemAddress, BodyID, BodyName, name, percent)

                for name in composition:
                    percent = composition[name] * 100
                    try:
                        this.cur.execute(sql_query, (SystemAddress, BodyID, BodyName, name, percent))
                        this.conn.commit()
                        logger.debug(f"Added composition ({SystemAddress}, {BodyID}, {BodyName} {name}, {percent})")
                    except sqlite3.Error as error:
                        this.conn.rollback()
                        logger.error(f"Failed adding composition {error} ({SystemAddress}, {BodyID}, {BodyName} {name}, {percent})")

            if 'Materials' in entry:
                sql_query = "insert or ignore into materials (SystemAddress, BodyID, BodyName, Name, Percent) values (?,?,?,?,?)"
#				sql_data  =                                  (SystemAddress, BodyID, BodyName, Name, Percent)

                for material in entry['Materials']:
                    Name	= material['Name'].capitalize()
                    Percent	= material['Percent']

                    try:
                        this.cur.execute(sql_query, (SystemAddress, BodyID, BodyName, Name, Percent))
                        this.conn.commit()
                        logger.debug(f"Added material ({SystemAddress}, {BodyID}, {BodyName} {Name}, {Percent})")
                    except sqlite3.Error as error:
                        this.conn.rollback()
                        logger.error(f"Failed adding material {error} ({SystemAddress}, {BodyID}, {BodyName} {Name}, {Percent})")
            
            if 'AtmosphereComposition' in entry:
                sql_query = "insert or ignore into atmospherecomposition (SystemAddress, BodyID, BodyName, Name, Percent) values (?,?,?,?,?)"
#				sql_data  =                                              (SystemAddress, BodyID, BodyName, Name, Percent)

                for composition in entry['AtmosphereComposition']:
                    Name    = composition['Name']
                    Percent = composition['Percent']
                    try:
                        this.cur.execute(sql_query, (SystemAddress, BodyID, BodyName, Name, Percent))
                        this.conn.commit()
                        logger.debug(f"Added atmospherecomposition ({SystemAddress}, {BodyID}, {BodyName}, {Name}, {Percent})")
                    except sqlite3.Error as error:
                        this.conn.rollback()
                        logger.error(f"Failed adding atmospherecomposition {error} ({SystemAddress}, {BodyID}, {BodyName}, {Name}, {Percent})")

        else:
            logger.debug(f"Scan: {entry}") # what other scans need to be checked or ignored

    if entry['event'] == 'Touchdown':
        # This is called when landing on a planet surface.
        # Relevant keys :
        #	timestame			: text
        #	Latitude			: real
        #	Longitude			: real
        #	StarSystem			: text
        #	SystemAddress		: integer
        #	Body				: text
        #	BodyID				: integer
        #	PlayerControlled	: bool - false if recalled from SRV
        Timestamp		= entry['timestamp']
        SystemAddress	= entry['SystemAddress']
        BodyID			= entry['BodyID']
        BodyName		= entry['Body']

        if entry['PlayerControlled'] == True: # only add landings that are by the player and not recalls
            Latitude		= entry['Latitude']
            Longitude		= entry['Longitude']

            sql_query = "insert into landings (SystemAddress, BodyID, BodyName, Latitude, Longitude, Timestamp) values (?,?,?,?,?,?)"
#			sql_data  =                       (SystemAddress, BodyID, BodyName, Latitude, Longitude, Timestamp)

            try:
                this.cur.execute(sql_query, (SystemAddress, BodyID, BodyName, Latitude, Longitude, Timestamp))
                this.conn.commit()
                logger.debug(f"Added landing ({SystemAddress}, {BodyID}, {BodyName}, {Latitude}, {Longitude}, {Timestamp})")
            except sqlite3.Error as error:
                this.conn.rollback()
                logger.error(f"Failed adding landing ({SystemAddress}, {BodyID}, {BodyName}, {Latitude}, {Longitude}, {Timestamp})")

    if entry['event'] == 'Docked':
        # This is called when docking on a landing pad.
        # Relevant keys :
        #	SystemAddress	: integer
        #	MarketID		: integer
        #	StationName		: text
        #	StationType		: text
        #	StarSystem		: text
        SystemAddress	= entry['SystemAddress']
        MarketID		= entry['MarketID']
        Timestamp		= entry['timestamp']
        StationName		= entry['StationName']

        sql_query = "insert into dockings (SystemAddress, MarketID, Timestamp, StationName) values (?,?,?,?)"
#		sql_data  =                       (SystemAddress, MarketID, Timestamp, StationName)

        try:
            this.cur.execute(sql_query, (SystemAddress, MarketID, Timestamp, StationName))
            this.conn.commit()
            logger.debug(f"Added docking ({SystemAddress}, {MarketID}, {Timestamp}, {StationName})")
        except sqlite3.Error as error:
            this.conn.rollback()
            logger.error(f"Failed adding docking {error} ({SystemAddress}, {MarketID}, {Timestamp}, {StationName})")

    if entry['event'] == 'Screenshot':
        logger.debug(entry)
        # This is called when taking a screenshot using the F10 key.  It does not get triggered when using the F12 key from Steam.
        # Relevant keys:
        #	Filename	: text
        #	System		: text
        #	Body		: text
        Filename	= entry['Filename']
        System		= entry['System']
        Body		= entry['Body']

        sql_query = "insert into screenshots (Filename, System, Body) values (?,?,?)"
#		sql_data  =                          (Filename, System, Body)

        try:
            this.cur.execute(sql_query, (Filename, System, Body))
            this.conn.commit()
            logger.debug(f"Added screenshot ({Filename}, {System}, {Body})")
        except sqlite3.Error as error:
            this.conn.rollback()
            logger.error(f"Failed adding screenshot {error} ({Filename}, {System}, {Body})")

    if entry['event'] == 'SAAScanComplete':
        # This is called when using the SAA scanner on a planet or rings
        # Assume the body has been added through the FSS or on approach to the body
        # Relevant keys :
        #	SystemAddress	: int
        #	BodyID			: int
        #	BodyName		: text
        SystemAddress = entry['SystemAddress']
        BodyName      = entry['BodyName']

        sql_query = "update bodies set Scanned = ? where SystemAddress = ? and BodyName = ?"

        try:
            this.cur.execute(sql_query, (True, SystemAddress, BodyName))
            this.conn.commit()
            logger.debug(f"{BodyName} scanned")
        except sqlite3.Error as error:
            this.conn.rollback()
            logger.error(f"Failed setting {BodyName} as scanned")

    if entry['event'] == 'SAASignalsFound' or entry['event'] == 'FSSBodySignals':
        # This is called when using the SAA scanner on a planet or rings or when the FSS finds signals
        # Relevant keys :
        #	SystemAddress		: int
        #	BodyID				: int
        #	BodyName			: text
        #	Signals				: array [ Type|Type_Localised : text, count : int ]
        SystemAddress = entry['SystemAddress']
        BodyID        = entry['BodyID']
        BodyName      = entry['BodyName']

        sql_query = "insert or ignore into signals (SystemAddress, BodyID, BodyName, Type, Count) values (?,?,?,?,?)"

        for signal in entry['Signals']:
            Type  = signal['Type_Localised'] if 'Type_Localised' in signal else signal['Type']
            Count = signal['Count']

            try:
                this.cur.execute(sql_query, (SystemAddress, BodyID, BodyName, Type, Count))
                this.conn.commit()
                logger.debug(f"Added signal ({SystemAddress}, {BodyID}, {BodyName}, {Type}, {Count})")
            except sqlite3.Error as error:
                this.conn.rollback()
                logger.error(f"Failed adding signal {error} ({SystemAddress}, {BodyID}, {BodyName}, {Type}, {Count})")

    if entry['event'] == 'CodexEntry':
        # Relevant keys
        #	EntryID 					: int
        #	Name_Localised				: text
        #	SubCategory_Localised		: text
        #	Category_Localised			: text
        #	Region_Localised			: text
        #	SystemAddress				: int
        #	NearestDesination_Localised	: text (may not exist)
        #	IsNewEntry					: bool (may not exist)
        #	Traits						: array (text)
        # Insert the codex entry into the CodexEntries table by EntryID
        # Insert the location into the CodexLocation
        # Insert the traits into the codextraits table
        EntryID     = entry['EntryID']
        Name        = entry['Name_Localised'] if 'Name_Localised' in entry else entry['Name']
        Category    = entry['Category_Localised'] if 'Category_Localised' in entry else entry['Category']
        SubCategory = entry['SubCategory_Localised'] if 'SubCategory_Localised' in entry else entry['SubCategory']
        IsNewEntry  = entry['IsNewEntry'] if 'IsNewEntry' in entry else False

        sql_query = "insert or ignore into codexentries (EntryID, Name, Category, SubCategory, IsNewEntry) values (?,?,?,?,?)"
#		sql_data  =                                     (EntryID, Name, Category, SubCategory, IsNewEntry)

        try:
            this.cur.execute(sql_query, (EntryID, Name, Category, SubCategory, IsNewEntry))
            this.conn.commit()
            logger.debug(f"Added codex entry ({EntryID}, {Name}, {Category}, {SubCategory}, {IsNewEntry})")
        except sqlite3.Error as error:
            this.conn.rollback()
            logger.error(f"Failed adding codex entry {error} ({EntryID}, {Name}, {Category}, {SubCategory}, {IsNewEntry})")

        SystemAddress      = entry['SystemAddress']
        Region             = entry['Region_Localised'] if 'Region_Localised' in entry else entry['Region']
        NearestDestination = entry['NearestDestination_Localised'] if 'NearestDestination_Localised' in entry else entry['NearestDestination'] if 'NearestDestination' in entry else 'No near destination'

        sql_query = "insert or ignore into codexlocations (EntryID, SystemAddress, Region, NearestDestination) values (?,?,?,?)"
#		sql_data  =                                       (EntryID, SystemAddress, Region, NearestDestination)

        try:
            this.cur.execute(sql_query, (EntryID, SystemAddress, Region, NearestDestination))
            this.conn.commit()
            logger.debug(f"Added codex location ({EntryID}, {SystemAddress}, {Region}, {NearestDestination})")
        except sqlite3.Error as error:
            this.conn.rollback()
            logger.error(f"Failed adding codex location {error} ({EntryID}, {SystemAddress}, {Region}, {NearestDestination})")

        sql_query = "insert or ignore into codextraits (EntryID, Trait) value (?,?)"
#		sql_data  =                                    (EntryID, trait)

        if 'NewTraitDiscovered' in entry:
            if 'Traits' in entry:
                for trait in entry['Traits']:
                    try:
                        this.cur.execute(sql_query, (EntryID, trait))
                        this.conn.commit()
                        logger.debug(f"Added codex trait ({EntryID}, {trait})")
                    except sqlite3.Error as error:
                        this.conn.rollback()
                        logger.debug(f"Failed adding codex trait {error} ({EntryID}, {trait})")

    if entry['event'] == 'MultiSellExplorationData' or entry['event'] == 'SellExplorationData':
        Timestamp	= entry['timestamp']
        BaseValue	= entry['BaseValue']
        Bonus		= entry['Bonus']

        sql_query = 'insert into selldata (Timestamp, BaseValue, Bonus) values (?,?,?)'
#		sql_data  =						  (Timestamp, BaseValue, Bonus)

        try:
            this.cur.execute(sql_query, (Timestamp, BaseValue, Bonus))
            this.conn.commit()
            logger.debug(f"Added sell data ({BaseValue}, {Bonus})")
        except sqlite3.Error as error:
            this.conn.rollback()
            logger.debug(f"Failed adding sell data {error} ({Timestamp}, {BaseValue}, {Bonus})")
