# ExpeditionSurvey
Provides an EDMarketConnector ([EDMC](https://github.com/EDCD/EDMarketConnector)) plugin to create a local [sqlite3](https://www.sqlite.org/index.html) database of star system information for Elite Dangerous

Whilst there are websites such as the Elite Dangerous Star Map ([EDSM](https://www.edsm.net/)) that cater for uploading a commander's information, having a local database allows for more in-depth analysis.

Multiple databases can be used to allow isolation of specific events such as an organised expedition.  The database is stored in the same folder as the plugin and will be created if it does not exist.  Moving or renaming the database will result in a new one being created with the default name.

The plugin uses the excellent Elite Dangerous Market Connector to do the extraction of information from the log files created by Elite Dangerous and uses various events to log information to the local database.  It doesn't interfere with any other plugins so EDMC will continue to send information to other sites depending on its configuration.

### Platform
This plugin has only been tested on Windows 10 at this time.  It has been tested against Horizons and Odyssey.

### Installation
The ExpeditionSurvey folder should be copied to the EDMC plugin folder and should contain the load.py script.  When EDMC is started and loads the new plugin, a database called ExpeditionSurvey.db will also be created in the same folder.  This database will continue to be used until it is moved or renamed, in which case a new one will then be created.

Plugin folder: C:\Users\\\<username>\AppData\Local\EDMarketConnector\plugins

### Bugs
There aren't any obvious ones, but testing has only been done on my own system, so further testing is required.  Please feedback any issues on github and I will endeavour to resolve them.

To help with that, EDMC has the option to change the logging level in File->Settings->Configuration:Log Level.  If this is set to DEBUG, additional information will be stored in the log file which can help isolate the issue.

The log file is stored in C:\Users\\\<username>\AppData\Local\Temp\EDMarketConnector.log

### Developments
The plugin itself is only to gather exploration information and store it in the database.  To support that I will be creating some reporting functionality, accessible from a web browser, to allow interrogation of the data.

In the ExpeditionSurvey folder there is a link called 'ExpeditionServer' which runs the following command in a new CMD window:
~~~
C:\Windows\System32\cmd.exe /k python3 -m http.server --cgi -d .\ 8001
~~~
This will start the python web server on port 8001 and can be accessed through the browser at [http://127.0.0.1:8001/cgi-bin/stats.py](http://127.0.0.1:8001/cgi-bin/stats.py)

The information available through the browser is limited at this time, but I will develop this further.  Based on the data being stored, see events below, if there is a specific requirement for any particular reporting, please raise it as an issue on github.

You may notice that I am no expert in Python, SQL, HTML or CSS, so there are no doubt improvements that can be made.  If anyone would like to contribute any improvements or features, please let me know.

### The events processed are:

#### FSDJump

This will create an instance of the star system if it has not already been created, with the SystemAddress, SystemName, X,Y,Z coordinates in light years from SOL, JumpDist, and FuelUsed.

It also creates an instance of a jump to that star system with the timestamp of that jump.  The system can be visited multiple times and all jumps will be logged in chronological order.

#### Scan

An initial scan will be done when jumping into a system which should identify the stars and any close bodies.  Using the Discovery Scanner and the Full Spectrum Scanner (FSS) will identify all of the other bodies in the system.

For stars the following information is stored:
- SystemAddress
- BodyID
- BodyName
- DistanceFromArrivalLS
- WasDiscovered
- WasMapped
- StarType
- Subclass
- StellarMass
- Radius
- AbsoluteMagnitude
- Age_MY
- SurfaceTemperature
- Luminosity

If the star has any rings, including asteroid belts, the following information is stored:
- Name
- RingClass
- MassMT
- InnerRad
- OuterRad

For planets and moons the following information is stored:
- SystemAddress
- BodyID
- BodyName
- DistanceFromArrivalLS
- WasDiscovered
- WasMapped
- TerraformState
- PlanetClass
- Atmosphere
- Volcanism
- MassEM
- Radius
- SurfaceGravity
- SurfaceTemperature
- SurfacePressure
- Landable
- Composition
- AtomosphereComposition
- Materials

If the planet has any rings the following information is stored:
- Name
- RingClass
- MassMT
- InnerRad
- OuterRad
- ReserveLevel

#### Touchdown

When landing on a planet or moon the following information is stored:
- SystemAddress
- BodyID
- BodyName
- Latitude
- Longitude

#### Docked

When docking at a station the following information is stored:
- SystemAddress
- MarketID
- timestamp
- StationName

#### SAAScanComplete

After using the Detailed Surface Scanner, the body is marked as scanned in the database.

#### SAASignalsFound FSSBodySignals

If any signals are discovered using the Full Spectrum Scanner or the Detailed Surface Scanner the following information is stored:

- SystemAddress
- BodyID
- BodyName
- Signal Type
- Signal Count

#### CodexEntry

If any codex entries are discovered the following information is stored:
- EntryID
- Name
- Category
- SubCategory
- IsNewEntry
- SystemAddress
- Region
- NearestDestination
- Trait

#### Screenshot

When a screenshot is taken using the Elite Dangerous hotkey (F10) the following information is stored:

- Filename
- System
- Body

The filename path is \\\ED_Pictures\\\<Filename>

ED_Pictures will be where pictures are stored for your platform.

e.g. C:\Users\\\<username>\Pictures\Frontier Developments\Elite Dangerous
