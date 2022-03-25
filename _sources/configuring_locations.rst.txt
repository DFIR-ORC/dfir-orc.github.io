=====================
Configuring Locations
=====================

A location is an access path to a specific NTFS volume. Typically, an access path can be:

* a mounted volume path, such as:

    * ``\\.\HarddiskVolume6``,

    * ``E:\``,

    * ``\\?\Volume{3f0e57c9-debc-403d-b614-feb223750981}``,

    * ``\\.\Harddisk0Partition4``;

* a system storage path, such as

    * ``\\.\STORAGE#Volume#...``;

* a physical drive path, such as

    * ``\\.\PHYSICALDRIVE0,offset=512,size=2199023255040,sector=512``;

* an interface path, such as 

    * ``\\.\IDE#DiskVBOX_HARDDISK...offset=105906176,size=37474009088,sector=512``, 

    * ``\\.\USBSTOR#Disk&Ven_Kingston&...,offset=1048576,size=62007541760,sector=512``, 

    * ``\\.\SCSI#Disk&Ven_Msft&...,offset=1048576,size=136362065920,sector=512``;

* a disk image path, such as

    * ``MyImage.dd``.

* an environment variable or a dynamic variable, such as

    * ``%SYSTEMDRIVE%``

    * ``{UserProfiles``}

Paths, file names and namespaces notations are `documented on the MSDN <https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file>`_.
    
.. note:: When using the drive letter notation, a specific folder inside the volume can also be specified. This will cause the tools to collect information recursively only for entries that are subentities of the selected folders (the selected folder is excluded).

For some tools of the embedded tool suite (GetThis, NTFSInfo, FastFind,...), the location has to be specified.

Multiple locations to be inspected can either be passed as parameters on the command line:

.. code:: bat

    DFIR-Orc.exe NTFSInfo c: f:\Users \\.\PhysicalDrive0

or as a set of ``location`` elements in an XML configuration file with the following syntax:

.. code:: xml

    <location>C:</location>
    <location>F:\Users</location>
    <location>\\.\PhysicalDrive0</location>

Environment variables are supported.

The special wildcard ``*`` can be used to inspect all mounted NTFS volumes on the system.

.. code:: bat

    DFIR-Orc.exe NTFSInfo *

The equivalent XML syntax is:

.. code:: xml

    <location>*</location>
    
The locations specified in a file are all resolved before starting any actual parsing. Then, the most general locations to parse are determined.
Possible location attributes documented below such as ``altitude`` and ``shadows`` are taken into account globally: their value apply on all locations. The last occurrence within an XML file sets the global value of the attribute.

Locations
=========

Locations for Mounted Volumes
-----------------------------

Locations are simply added using full path names:

.. code:: xml

    <location>C:\Windows</location>
    <location>D:\MyFiles</location>
    <location>G:\Documents</location>
    <location>{UserProfiles}\Downloads</location>

File System Entries are enumerated recursively for the specified locations.

The MFT parser has the ability to parse a mounted volume without using the drive letter convention. Typically, one can refer to a volume using the volume ID convention:


    ``\\?\Volume{4564119e-eb6c-11e0-92aa-442a60da9b94}``

This syntax can be used as a command-line argument:

.. code:: bat

    DFIR-Orc.exe NTFSInfo \\?\Volume{4564119e-eb6c-11e0-92aa-442a60da9b94}

It can also appear in an XML configuration file:

.. code:: xml

    <location>\\?\Volume{4564119e-eb6c-11e0-92aa-442a60da9b94}</location>

Mounted volumes can also be specified using the following syntax:

    ``\\?\GLOBALROOT\Device\HarddiskVolume3``

Locations for Physical Drives
-----------------------------

The MFT parser has the ability to parse the physical drive (non-mounted volumes).
When the syntax ``\\.\PhysicalDrive0`` is used, then the partitions of the disk are enumerated and all NTFS volumes are parsed.
One can also refer to a specific NTFS partition on a drive using the following convention:

    ``\\.\PhysicalDrive0,part=3``
   
In this example, 0 is the physical drive number and 3 is the enumerated partition number.

This syntax can be used as a command-line argument:

.. code:: bat

    .\DFIR-Orc.exe NTFSInfo \\.\PhysicalDrive0,part=3

or in a configuration file as follows:

.. code:: xml

    <location>\\.\PhysicalDrive0,part=3</location>

In case the partition table is invalid or missing, one can use the following syntax:

.. code:: xml

    <location>\\.\PhysicalDrive0,offset=1048576,size=214748364800,sector=512</location>

When using this notation

   * offset=1048576 represents the location of the NTFS volume in bytes,
   * size=214748364800 is the size in bytes of the partition (optional),
   * sector=512 is the size in bytes of the physical sector (optional).

.. warning:: Please note that the order matters: offset must come before size and then sector.

Locations for Disk Images (.dd)
-------------------------------

The MFT parser has the ability to parse full disk images.

On a command line, the appropriate syntax is:

.. code:: bat

    DFIR-Orc.exe NTFSInfo "F:\TestCases\disk_image.dd"

while in a configuration file, one can use:

.. code:: xml

    <location>F:\TestCases\disk_image.dd</location>

The partition table of the image is located, parsed, and then all NTFS partitions are parsed. 


Locations for Volumes and Partitions of an Image (.dd)
------------------------------------------------------

The MFT parser can parse partitions of raw or dd images. This requires the presence of the NTFS signature in the header of the image.

The syntax below can be used as a command-line argument:

.. code:: bat

    DFIR-Orc.exe NTFSInfo "F:\TestCases\d_image.dd"

or in a configuration file as follows:

.. code:: xml

    <location>F:\TestCases\d_image.dd</location>

When dealing with the image of a disk, parsing can be done by specifying the partition:

.. code:: bat

    DFIR-Orc.exe NTFSInfo "F:\TestCases\d_image.dd,part=N"

This command will parse the N-th partition in the order of the table.

The following command is also available, to parse the volume located at ``<Offset>``, whose size is ``<Length>`` bytes, with sectors of ``<Size>`` bytes.


.. code:: bat

    DFIR-Orc.exe NTFSInfo "F:\TestCases\d_image.dd,offset=<Offset>,length=<Length>,sector=<Size>"

.. warning:: Please note that the order of offset, size and sector has to be respected.


Locations for Volume Shadow Copies
----------------------------------

Explicit Volume Shadow Copy
```````````````````````````

The MFT parser has the ability to parse volume shadow copies (VSS).

On a command line, one can use:

.. code:: bat

    DFIR-Orc.exe NTFSInfo \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy10

and in a configuration file, the following line works:

.. code:: xml

    <location>\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy10</location>

.. _configuring_locations-automatic shadow:

Automatic Shadow Copies Addition
````````````````````````````````

The volume shadow copies can be enumerated and added to the list of parsed locations.
This feature can be enabled by adding the attribute ``shadows="yes"`` in a ``location`` element:

.. code:: xml

    <location shadows="yes">c:\</location>

The location must be a mounted volume: parsing shadow copies is not supported for physical drive, raw disk images, or interfaces.

Using ``shadows="yes"`` activates VSS parsing, not using it (rather than ``shadows="no"``) does not activate parsing. As noted in introduction, the presence of this attribute in an XML file sets the option globally.  

The wildcard ``*`` is also supported:

.. code:: xml

    <location shadows="yes">*</location>

It is also possible to select 'newest', 'mid', 'oldest' or specific GUID of a shadow copy:

.. code:: xml

    <location shadows="newest,oldest,{04c16363-68ec-4f94-a956-abd80375c89f}">*</location>

The ``/shadows`` option can also be used on command lines and applies to all mounted volumes otherwise selected.


Locations for Offline MFT
-------------------------

The MFT parser can be used to parse the Master File Table in an offline manner, that is to say, the volume does not have to be parsed - or even present. 
The following command allows to dump the MFT:

.. code:: bat 

    DFIR-Orc.exe GetThis /sample=$Mft /out=d:\temp C:

Then the result can be passed to NTFSInfo.
This allows the MFT to be parsed without malware potentially intervening in the parsing (though it could still tamper with the capture).

The syntax is as follows:

.. code:: bat

    DFIR-Orc.exe NTFSInfo d:\temp\$MFT_data

or when using the XML configuration file:
    
.. code:: xml

    <location>d:\temp\$MFT_data</location>


Location variables
------------------

Environment variables (ex: ``SYSTEMROOT``) are resolved when executing DFIR-Orc.

The syntax is as follows:

.. code:: xml

    <location>%SYSTEMROOT%</location>

DFIR-Orc can also define some dynamic variable like ``UserProfiles``.

.. code:: xml

    <location>{UserProfiles}\Downloads</location>

* ``UserProfiles``: This variable will be expanded to the paths stored in ``HKLM/SOFTWARE/Microsoft/Windows NT/CurrentVersion/ProfileList``. Once expanded it will have the same behavior as with multiple `<Location>...` for each a user profile directory.


Usage
=====

``altitude`` Attribute, ``/Altitude=<Strategy>`` Option
-------------------------------------------------------

The location altitude defines the strategy used to translate a given location into the optimal access path to the volume. There are three strategies available for the altitude selection:

* ``Lowest`` (default): translates the location to the lowest-level access path available for the volume,
* ``Highest``: translates the location to the highest-level access path available for the volume,
* ``Exact``: uses the given location as the exact access path and does not attempt altitude translation.

For instance, if the location provided is ``C:`` and the altitude is set to choose the lowest-level access path available, then the tools internally translate the mounted volume path into an interface path (e.g., ``\\.\IDE#DiskVBOX_HARDDISK...``), if available, and use the latter to collect data.

Selecting the lowest possible altitude is useful for avoiding potential malware hooks in the driver stack. 

.. note:: There are some cases where the lowest possible altitude is not the interface path. This typically happens when using Full Volume Encryption software such as BitLocker. In this case, the physical drive and interface paths cannot be used and the altitude selector remains at the mounted volume level in order to read the decrypted data.

.. warning:: Some volume encryption solutions do not alter the NTFS Volume Boot Record, tricking the altitude selector into believing the volume is a non-encrypted NTFS volume. This situation results in the choice of a wrong access path translation, thus preventing normal data collection. To avoid such problems **in this specific case only**, altitude selection should be set to use the ``Exact`` strategy and the location should be a mounted volume path.

Altitude selection can either be configured via the command line

.. code:: bat

    /Altitude=Exact|Highest|Lowest

or via the ``altitude`` attribute of the ``location`` element:

.. code:: xml

    <location altitude="highest">C:\Windows</location>

.. note:: Even if the attribute ``altitude`` can be set on all ``location`` element, only the last occurrence in an XML file is taken into account for the complete set of ``location`` elements.

.. _configuring_locations-knowlocations:

``knownlocations`` Attribute, ``/knownlocations`` Option
--------------------------------------------------------

Some tools (NTFSInfo, FastFind, GetSamples, USNInfo, GetThis) provides the ``/knownlocations`` option in command line or the equivalent ``<knownlocations/>`` element in their XML configuration file.

This option collects information on the following locations of interest:

.. csv-table::
    :header: "Identifier", "Typical path"
    :widths: 20, 40

    "CSIDL_PROGRAMS","Start Menu\\Programs"
    "CSIDL_FAVORITES","<user name>\\Favorites"
    "SIDL_STARTUP","Start Menu\\Programs\\Startup"
    "SIDL_BITBUCKET","<desktop>\\Recycle Bin"
    "CSIDL_STARTMENU","<user name>\\Start Menu"
    "CSIDL_DESKTOPDIRECTORY","<user name>\\Desktop"
    "CSIDL_COMMON_STARTMENU","All Users\\Start Menu"
    "CSIDL_COMMON_STARTUP","All Users\\Startup"
    "CSIDL_COMMON_DESKTOPDIRECTORY","All Users\\Desktop"
    "CSIDL_APPDATA","<user name>\\Application Data"
    "CSIDL_LOCAL_APPDATA","<user name>\\Local Settings\\Application Data (non roaming)"
    "CSIDL_ALTSTARTUP","non localized startup"
    "CSIDL_COMMON_ALTSTARTUP","non localized common startup"
    "CSIDL_COMMON_FAVORITES",""
    "CSIDL_INTERNET_CACHE",""
    "CSIDL_COOKIES",""
    "CSIDL_HISTORY",""
    "CSIDL_COMMON_APPDATA","All Users\\Application Data"
    "CSIDL_WINDOWS","GetWindowsDirectory()"
    "CSIDL_PROGRAM_FILES","C:\\Program Files"
    "CSIDL_PROFILE","%USERPROFILE%"
    "CSIDL_PROGRAM_FILESX86","C:\\Program Files"
    "CSIDL_COMMON_ADMINTOOLS","All Users\\Start Menu\\Programs\\Administrative Tools"
    "CSIDL_ADMINTOOLS","<user name>\\Start Menu\\Programs\\Administrative Tools"
    "%Path%","Each directory in %Path% is added"
    "%ALLUSERSPROFILE%","All User profile"
    "%temp%","%temp% is added if it exists"
    "%tmp%","%tmp% is added if it exists"
    "%APPDATA%",""

For more information, please refer to `the reference page for KnownLocations <https://docs.microsoft.com/en-us/windows/win32/shell/csidl>`_.

.. note::
    
    Known locations cannot be used as a ``location`` value.

.. _configuring_locations-shadows:

``shadows`` Attribute, ``/shadows`` Option
------------------------------------------

This option enable the processing of the shadow copy volumes from all the specified ``location``. Multiple of the following values can be assigned:

* ``no`` (default): Disable every volume shadow copy processing.
* ``yes``: enable every volume shadow copy processing.
* ``<empty>`` (shadows without value): Same as ``yes``.
* ``oldest``: process eldest volume shadow copy.
* ``mid``: process the "mid-N" volume shadow copy between the oldest and the newest.
* ``newest``: process only the most recent volume shadow copy.
* ``GUID``: process only the volume shadow copy with the specified GUID (Shadow Copy ID given by ``vssadmin list shadows``).

Example enabling the processing of the ``newest`` and ``oldest`` volume shadow copy:

.. code:: bat

    /Shadows=oldest,newest

or via the ``shadows`` attribute of the ``location`` element:

.. code:: xml

    <location shadows="oldest,newest">*</location>

See also :ref:`above <configuring_locations-automatic shadow>`.

.. _configuring_locations-exclude:

``exclude`` Attribute, ``/Exclude="<DriveList>"`` Option
--------------------------------------------------------
Specify volume(s) to exclude from any processing. This can be particularly helpful when ``location`` value is wildcard '*'. It is also possible to exclude a "normal" volume when only its shadow copy volumes must be processed.

Example processing all volumes but the 'D':

.. code:: xml

    <location exclude="D:">*</location>

Example processing only volume shadow copy from the system drive but not the mounted volume itself:

.. code:: xml

    <location exclude="%SYSTEMDRIVE%" shadows="yes">%SYSTEMDRIVE%</location>

Finally a XML configuration can be overloaded using the command line to remove exclusion:

.. code:: bat

    /Exclude=""

Or specify another one:

.. code:: bat

    /Exclude="C:"

