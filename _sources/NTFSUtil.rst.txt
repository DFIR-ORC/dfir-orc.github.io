========
NTFSUtil
========

Description
===========

NTFSUtil is intended to be used as a Swiss Army knife NTFS tool to provide a collection of useful features 
to investigate NTFS-related information.
Currently, NTFSUtil covers the following functionalities:

* USN journal controlled expansion,
* location inspection, 
* MFT record inspection, and
* NTFS volume data dump.


Usage
=====

``/USN`` Option
---------------

NTFSUtil can be used to display current USN journal configuration using the syntax below.

.. code:: bat

   DFIR-Orc.exe NTFSUtil /USN \\.\c:

The output is as follows.

.. code:: bat

     NTFSUtil - various NTFS related utilities Version 10.0.0.000

     Start time            : 10/02/2019 18:39:11.878 (UTC)

     Computer              : DESKTOP-8B106QG
     Volume name           : \\.\C:
     Maximum size    : 32 MB, (33554432 bytes)
     Allocation delta: 8 MB, (8388608 bytes)
     Finish time           : 10/02/2019 18:39:11.878 (UTC)
     Elapsed time          : 0 msecs

USN journal configuration can be modified with the ``/configure`` syntax.
The available arguments are the following:

* ``/MaxSize=<MaxSize>`` can be used to set the USN journal maximum size to <MaxSize> bytes and has to be combined with ``/Delta=<AllocDelta>``.
* ``/SizeAtLeast=<Size>`` can be used to set the USN journal maximum size to be **at least** <Size> bytes (the size of the journal is modified only if current value is smaller than <Size>, the tool does nothing otherwise). This option has to be combined with ``/Delta=<AllocDelta>``.
* ``/Delta=<AllocDelta>``, which sets the USN journal allocation delta size to <AllocDelta> bytes, and should complete options above.

For all these options, the usual file size multipliers can be used (1K, 1M, 1G).

The ``USN`` option of NTFSUtil is quite different from all other tools proposed in the embedded tool suite. Indeed, they *write* on the disk.
The ambition is to be able to safely increase the size of the USN journal by setting a new maximum size if (and only if) the new setting expands the size of the journal.
Obviously, this only makes sense when planning to collect the USN journal sometime in the future.

For example, the command line below 

.. code:: bat
   
    .\DFIR-Orc.exe NTFSUtil /USN \\.\C: /configure /SizeAtLeast=40M /Delta=512K

outputs

.. code:: bat

    .\DFIR-Orc.exe NTFSUtil /USN \\.\C: /configure /SizeAtLeast=100M /Delta=12M

    NTFSUtil - various NTFS related utilities Version 10.0.2.000
    
    Start time            : 10/03/2019 11:40:07.492 (UTC)
    
    Computer              : DESKTOP-8B106QG
    Volume name           : \\.\C:
    Maximum size    : 40 MB, (41943040 bytes)
    Allocation delta: 10 MB, (10485760 bytes)
    Configure USN   : Successfully configured USN journal for volume \\.\C:
    Maximum size    : 100 MB, (104857600 bytes)
    Allocation delta: 12 MB, (12582912 bytes)
    Finish time           : 10/03/2019 11:40:07.523 (UTC)
    Elapsed time          : 31 msecs

or with a different value:

.. code:: bat

    .\DFIR-Orc.exe NTFSutil /USN \\.\C: /configure /SizeAtLeast=20M /Delta=12M

    NTFSUtil - various NTFS related utilities Version 10.0.2.000

    Start time            : 10/03/2019 11:45:09.260 (UTC)

    Computer              : DESKTOP-ORBLVTG
    Volume name           : \\.\c:
    Maximum size    : 100 MB, (104857600 bytes)
    Allocation delta: 12 MB, (12582912 bytes)
    Configure USN   : USN journal for volume \\.\c: is bigger than sizeatleast
    Maximum size    : 100 MB, (104857600 bytes)
    Allocation delta: 12 MB, (12582912 bytes)
    Finish time           : 10/03/2019 11:45:09.260 (UTC)
    Elapsed time          : 0 msecs

It seems that augmenting the delta allocation size can behave differently depending on Windows versions.
It is not a bug of NTFSUtil, just the absence of more detailed documentation about the underlying API used.

.. _NTFSUtil-vss:
    
``/vss`` Option
---------------

NTFSUtil can display information about volume shadow copies (VSS) present on the system.

The code to deal with VSS depends on the architecture. As a result, the following behavior is expected on a 64-bit system.

.. code:: bat

    .\DFIR-Orc.exe NTFSUtil /vss

.. code:: bat
 
    NTFSUtil - various NTFS related utilities Version 10.0.0.000

    Start time            : 10/03/2019 12:00:54.220 (UTC)

    Computer              : DESKTOP-8B106QG
    WARNING (hr=0x80042302): Failed to initialise VSS service, most likely cause: you are running a 32 bits process on x64 system
    ERROR (hr=0x80042302): Failed to list volume shadow copies.


To mimic what happens when ``DFIR-Orc.exe`` uses WolfLaucher to choose an architecture-appropriate unconfigured binary, it is possible to run the command below.

.. code:: bat
  
    .\DFIR-Orc_x64.exe NTFSUtil /vss

.. code:: bat
 
    NTFSUtil - various NTFS related utilities Version 10.0.0.000

    Start time            : 10/03/2019 12:23:07.755 (UTC)

    Computer              : DESKTOP-8B106QG

    VSS Snapshot :
    -> guid             : {DDE981E2-0B1D-41D8-8CA5-BA4D87B7D2CA}
    -> device instance  : \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1
    -> volume name      : \\?\Volume{4cada720-c048-4361-96f8-56ae661f8fca}\
    -> creation time    : 2019-07-24 09:36:44.481
    -> attributes       : VSS_VOLSNAP_ATTR_PERSISTENT|VSS_VOLSNAP_ATTR_CLIENT_ACCESSIBLE|VSS_VOLSNAP_ATTR_NO_AUTO_RELEASE|VSS_VOLSNAP_ATTR_DIFFERENTIAL|VSS_VOLSNAP_ATTR_AUTORECOVER

    VSS Snapshot :
    -> guid             : {A90EC9F3-2125-4C12-9579-0F5ACEE8E6A4}
    -> device instance  : \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy2
    -> volume name      : \\?\Volume{4cada720-c048-4361-96f8-56ae661f8fca}\
    -> creation time    : 2019-07-24 09:37:07.722
    -> attributes       : VSS_VOLSNAP_ATTR_PERSISTENT|VSS_VOLSNAP_ATTR_CLIENT_ACCESSIBLE|VSS_VOLSNAP_ATTR_NO_AUTO_RELEASE|VSS_VOLSNAP_ATTR_DIFFERENTIAL|VSS_VOLSNAP_ATTR_AUTORECOVER
    Finish time           : 10/03/2019 12:23:07.978 (UTC)
    Elapsed time          : 219 msecs


When another option (e.g. ``/enumlocs``) treats VSS, the same behavior is expected.


.. _NTFSUtil-enumlocs:

``/enumlocs`` Option
--------------------

NTFSUtil can enumerate the available locations on a live system.
This can help select the locations and be familiar with the various possibilities offered by the MFT parser.

.. code:: bat

    DFIR-Orc.exe NTFSUtil /enumlocs

The output looks as follows.

.. code::
    
    NTFSUtil - various NTFS related utilities Version 10.0.0.000

    Start time            : 10/03/2019 15:23:45.247 (UTC)
    
    Computer              : DESKTOP-8B106QG
    WARNING (hr=0x80042302): Failed to initalise VSS service, most likely cause: you are running a 32 bits process on x64 system
    WARNING (hr=0x80042302): VSS functionatility is not available
    WARNING (Fonction incorrecte, hr=0x80070001): IOCTL_STORAGE_QUERY_PROPERTY does not support StorageAccessAlignmentProperty for this device "\\.\HarddiskVolume16"
    WARNING (Fonction incorrecte, hr=0x80070001): IOCTL_STORAGE_QUERY_PROPERTY does not support StorageAccessAlignmentProperty for this device "\\?\Volume{bd14675a-c284-11e9-8e1b-fb1948d83d59}"
    
    Serial Number 0x40B699C7B699BDBA
        DiskInterfaceVolume   : \\.\SCSI#Disk&Ven_TOSHIBA&Prod_MQ01ACF050#4&132ac043&0&000000#{53f56307-b6bf-11d0-94f2-00a0c91efb8b},offset=1048576,size=523238912,sector=512 - NTFS - Valid (serial : 0x40b699c7b699bdba)
        PhysicalDriveVolume   : \\.\PHYSICALDRIVE0,offset=1048576,size=523238912,sector=512 - NTFS - Valid (serial : 0x40b699c7b699bdba)
        MountedVolume         : \\.\HarddiskVolume1 - NTFS - Valid (serial : 0x40b699c7b699bdba)
    
    Serial Number 0x4A9B3EE8
        DiskInterfaceVolume   : \\.\SCSI#Disk&Ven_TOSHIBA&Prod_MQ01ACF050#4&132ac043&0&000000#{53f56307-b6bf-11d0-94f2-00a0c91efb8b},offset=524288000,size=104857088,sector=512 - FAT32 - Valid (serial : 0x4a9b3ee8)
        PhysicalDriveVolume   : \\.\PHYSICALDRIVE0,offset=524288000,size=104857088,sector=512 - FAT32 - Valid (serial : 0x4a9b3ee8)
        MountedVolume         : \\.\HarddiskVolume2 - FAT32 - Valid (serial : 0x4a9b3ee8)
    
    Serial Number 0x60669DB9669D9080 "C:\" 
        DiskInterfaceVolume   : \\.\SCSI#Disk&Ven_TOSHIBA&Prod_MQ01ACF050#4&132ac043&0&000000#{53f56307-b6bf-11d0-94f2-00a0c91efb8b},offset=645922816,size=499461914112,sector=512 - NTFS - Valid (serial : 0x60669db9669d9080)
        PhysicalDriveVolume   : \\.\PHYSICALDRIVE0,offset=645922816,size=499461914112,sector=512 - NTFS - Valid (serial : 0x60669db9669d9080)
        MountedVolume         : \\?\Volume{4cada720-c048-4361-96f8-56ae661f8fca} - NTFS - Valid (serial : 0x60669db9669d9080)
        MountedVolume         : \\.\HarddiskVolume4 - NTFS - Valid (serial : 0x60669db9669d9080)
    
    Serial Number 0x692A9CF683CEB91 "D:\" 
        DiskInterfaceVolume   : \\.\USBSTOR#Disk&Ven\_&Prod_USB_DISK_2.0&Rev_PMAP#90007947C54F9A42&0#{53f56307-b6bf-11d0-94f2-00a0c91efb8b},offset=1048576,size=7745830912,sector=512 - NTFS - Valid (serial : 0x692a9cf683ceb91)
        PhysicalDriveVolume   : \\.\PHYSICALDRIVE1,offset=1048576,size=7745830912,sector=512 - NTFS - Valid (serial : 0x692a9cf683ceb91)
        MountedVolume         : \\.\HarddiskVolume16 - NTFS - Valid (serial : 0x692a9cf683ceb91)
        MountedVolume         : \\?\Volume{bd14675a-c284-11e9-8e1b-fb1948d83d59} - NTFS - Valid (serial : 0x692a9cf683ceb91)
    Finish time           : 10/03/2019 15:23:45.357 (UTC)
    Elapsed time          : 110 msecs
        

Explanations as to why the VSS-related message appears can be found in the paragraph :ref:`NTFSUtil-vss`.
On a 64-bit system, using ``DFIR-Orc_x64.exe /enumlocs`` will list the device instances for each snapshot:

.. code::

    Serial Number 0x60669DB9669D9080 "C:\"
        DiskInterfaceVolume   : \\.\SCSI#Disk&Ven_TOSHIBA&Prod_MQ01ACF050#4&132ac043&0&000000#{53f56307-b6bf-11d0-94f2-00a0c91efb8b},offset=645922816,size=499461914112,sector=512 - NTFS - Valid (serial : 0x60669db9669d9080)
        PhysicalDriveVolume   : \\.\PHYSICALDRIVE0,offset=645922816,size=499461914112,sector=512 - NTFS - Valid (serial : 0x60669db9669d9080)
        MountedVolume         : \\?\Volume{4cada720-c048-4361-96f8-56ae661f8fca} - NTFS - Valid (serial : 0x60669db9669d9080)
        MountedVolume         : \\.\HarddiskVolume4 - NTFS - Valid (serial : 0x60669db9669d9080)
        Snapshot              : \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1 - NTFS - Valid (serial : 0x60669db9669d9080)
        Snapshot              : \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy2 - NTFS - Valid (serial : 0x60669db9669d9080)

The third and fourth warning messages come from a known bug to be addressed shortly, pertaining to an API change to query for hardware properties.
When this message appears, physical sector size defaults to the logical sector size returned by the IOCTL_DISK_GET_DRIVE_GEOMETRY_EX call.



``/loc`` Option
---------------

This option displays location details as they are interpreted by the readers.
This syntax can be used with any of the provided location (see :doc:`configuring_locations`).

This option takes as argument the location about which details are desired.

.. code:: bat

    .\DFIR-Orc.exe NTFSUtil /loc \\.\PhysicalDrive0

.. code:: bat
        
    NTFSUtil - various NTFS related utilities Version 10.0.0.000

    Start time            : 10/02/2019 18:50:13.579 (UTC)
    
    Computer              : DESKTOP-8B106QG
    Volume name           : \\.\PhysicalDrive0
    
    
    \\.\PhysicalDrive0 is a physical drive device
    
    
    \\.\PhysicalDrive0 contains the following partition table:
    
        Partition NTFS - number : 1 - start offset : 0x100000 - end offset : 0x1f3ffe00 - size : 0x1f2ffe00 - flags : SYSTEM
        Partition ESP - number : 2 - start offset : 0x1f400000 - end offset : 0x257ffe00 - size : 0x63ffe00 - flags : NONE
        Partition MICROSOFT_RESERVED - number : 3 - start offset : 0x25800000 - end offset : 0x267ffe00 - size : 0xfffe00 - flags : NONE
        Partition NTFS - number : 4 - start offset : 0x26800000 - end offset : 0x7470bffe00 - size : 0x744a3ffe00 - flags : NONE
    
    
    Location \\.\PhysicalDrive0 is parsed as:
    
        PhysicalDrive_0_Offset_1048576
    
    
        PhysicalDrive_0_Offset_524288000
    
    
        PhysicalDrive_0_Offset_629145600
    
    
        PhysicalDrive_0_Offset_645922816
    
    Finish time           : 10/02/2019 18:50:13.593 (UTC)
    Elapsed time          : 0 msecs 
    

``/record=<FRN>`` Option
------------------------

NTFSUtil can provide detailed information about MFT records.
The drive name has to be provided as an argument.

For instance, the command line below provides details about a directory ``TOOLS/``, the 70th record
of drive ``D:``.


.. code:: bat 

    DFIR-Orc.exe NTFSUtil /record=70 D:

.. code:: bat

    NTFSUtil - various NTFS related utilities Version 10.0.0.000

    Start time            : 10/03/2019 15:22:49.280 (UTC)
    
    Computer              : DESKTOP-8B106QG
    Volume name           : D:
    WARNING (Fonction incorrecte, hr=0x80070001): IOCTL_STORAGE_QUERY_PROPERTY does not support StorageAccessAlignmentProperty for this device "\\.\D:"
    
    RECORD 0x0001000000000046 (in use)
    
    ATTRIBUTES[04]:
    
        ID=00: Name="",Type=$STANDARD_INFORMATION,Form=R
        ID=02: Name="",Type=$FILE_NAME,Form=R
        ID=03: Name="",Type=$OBJECT_ID,Form=R
        ID=01: Name="$I30",Type=$INDEX_ROOT,Form=R
    
    $STANDARD_INFORMATION:
    
        FileAttributes      : .............
        CreationTime        : 2019-10-02 18:37:11.630
        LastModificationTime: 2019-10-03 12:23:30.964
        LastAccessTime      : 2019-10-03 12:23:30.964
        LastChangeTime      : 2019-10-03 15:10:53.093
        OwnerID             : 0
        SecurityID          : 265
    
    $FILE_NAMES[01]:
    
        [00]FileName            : "TOOLS"
        [00]ParentDirectory     : 0x0001000000000028
        [00]CreationTime        : 2019-10-02 18:37:11.630
        [00]LastModificationTime: 2019-10-02 18:37:11.630
        [00]LastAccessTime      : 2019-10-02 18:37:11.630
        [00]LastChangeTime      : 2019-10-02 18:37:11.630
        [00]FileNameFlags       : FILE_NAME_WIN32|FILE_NAME_DOS83
        [00]FileNameID          : 2
    
    
    
    $INDEX_ROOT("$I30")
    
        IndexedAttributeType: 30 ($FILE_NAME)
        SizePerIndex        : 4096
        BlocksPerIndex      : 1
    
        [00]IndexedAttrOwner    : 0x0001000000000047
        [00]FileName            : "autorunsc.exe"
        [00]ParentDirectory     : 0x0001000000000046
        [00]CreationTime        : 2019-10-02 18:37:11.755
        [00]LastModificationTime: 2019-10-02 18:37:14.022
        [00]LastAccessTime      : 2019-10-02 18:37:14.022
        [00]LastChangeTime      : 2019-10-02 18:37:14.022
        [00]FileNameFlags       : FILE_NAME_WIN32
    
        [01]IndexedAttrOwner    : 0x0001000000000047
        [01]FileName            : "AUTORU~1.EXE"
        [01]ParentDirectory     : 0x0001000000000046
        [01]CreationTime        : 2019-10-02 18:37:11.755
        [01]LastModificationTime: 2019-10-02 18:37:14.022
        [01]LastAccessTime      : 2019-10-02 18:37:14.022
        [01]LastChangeTime      : 2019-10-02 18:37:14.022
        [01]FileNameFlags       : FILE_NAME_DOS83
    
        [02]IndexedAttrOwner    : 0x0001000000000049
        [02]FileName            : "DFIR-Orc_x64.exe"
        [02]ParentDirectory     : 0x0001000000000046
        [02]CreationTime        : 2019-10-02 18:37:14.475
        [02]LastModificationTime: 2019-10-02 18:37:15.473
        [02]LastAccessTime      : 2019-10-02 18:37:15.473
        [02]LastChangeTime      : 2019-10-02 18:37:15.473
        [02]FileNameFlags       : FILE_NAME_WIN32
    
        [03]IndexedAttrOwner    : 0x0001000000000049
        [03]FileName            : "DFIR-O~1.EXE"
        [03]ParentDirectory     : 0x0001000000000046
        [03]CreationTime        : 2019-10-02 18:37:14.475
        [03]LastModificationTime: 2019-10-02 18:37:15.473
        [03]LastAccessTime      : 2019-10-02 18:37:15.473
        [03]LastChangeTime      : 2019-10-02 18:37:15.473
        [03]FileNameFlags       : FILE_NAME_DOS83
    
    
    
    Record found, stopping enumeration
    Finish time           : 10/03/2019 15:22:50.600 (UTC)
    Elapsed time          : 1 sec(s), 329 msecs


Explanations related to the warning can be found in the paragraph :ref:`NTFSUtil-enumlocs`.


``/hexdump`` Option
------------------- 

This option mostly applies to files with a ``$DATA`` stream. It takes three arguments.  
On top of the drive letter, arguments ``/Offset`` and ``/Size`` should contain the offset and size to dump. 
These can be easily retrieved from the output of the ``/record`` option. 


In the example below, the file ``DFIR-Orc_x64.exe``, with record number 0x000100000000049, is dumped. 
Option ``/record`` allows to determine the offset and size of its ``$DATA`` stream.

.. code:: bat

    .\DFIR-Orc.exe NTFSUtil /record=0x000100000000049 D:\

.. code::
    
    NTFSUtil - various NTFS related utilities Version 10.0.0.000

    Start time            : 10/03/2019 15:17:15.672 (UTC)
    
    Computer              : DESKTOP-8B106QG
    Volume name           : D:
    WARNING (Fonction incorrecte, hr=0x80070001): IOCTL_STORAGE_QUERY_PROPERTY does not support StorageAccessAlignmentProperty for this device "\\.\D:"
    
    RECORD 0x0001000000000049 (in use)
    
    ATTRIBUTES[04]:
    
        ID=00: Name="",Type=$STANDARD_INFORMATION,Form=R
        ID=03: Name="",Type=$FILE_NAME,Form=R
        ID=02: Name="",Type=$FILE_NAME,Form=R
        ID=04: Name="",Type=$DATA,Form=NR
    
    $STANDARD_INFORMATION:
    
        FileAttributes      : A..........T.
        CreationTime        : 2019-10-02 18:37:14.475
        LastModificationTime: 2019-10-02 18:37:15.473
        LastAccessTime      : 2019-10-02 18:37:15.473
        LastChangeTime      : 2019-10-02 18:37:15.473
        OwnerID             : 0
        SecurityID          : 266
    
    $FILE_NAMES[02]:
    
        [00]FileName            : "DFIR-O~1.EXE"
        [00]ParentDirectory     : 0x0001000000000046
        [00]CreationTime        : 2019-10-02 18:37:14.475
        [00]LastModificationTime: 2019-10-02 18:37:14.475
        [00]LastAccessTime      : 2019-10-02 18:37:14.475
        [00]LastChangeTime      : 2019-10-02 18:37:14.475
        [00]FileNameFlags       : FILE_NAME_DOS83
        [00]FileNameID          : 3
    
        [01]FileName            : "DFIR-Orc_x64.exe"
        [01]ParentDirectory     : 0x0001000000000046
        [01]CreationTime        : 2019-10-02 18:37:14.475
        [01]LastModificationTime: 2019-10-02 18:37:14.475
        [01]LastAccessTime      : 2019-10-02 18:37:14.475
        [01]LastChangeTime      : 2019-10-02 18:37:14.475
        [01]FileNameFlags       : FILE_NAME_WIN32
        [01]FileNameID          : 2
    
    
    
    $DATA[01]:
    
        [00]DataName            : ""
        [00]DataSize            : 0x00000000005D8600
        [00]AllocatedSize       : 0x00000000005D9000
    
        [00]Extent[01]:
    
            [00]: LowestVCN=0x0000000000000000 /Offset=0x000000000D295000 /Size=0x00000000005D9000
    
    
    
    
    Record found, stopping enumeration
    Finish time           : 10/03/2019 15:17:15.785 (UTC)
    Elapsed time          : 109 msecs
    
.. code:: bat

    .\DFIR-Orc.exe NTFSUtil /hexdump  /Offset=0x000000000D295000 /Size=0x00000000005D9000 D:


.. code:: bat

    NTFSUtil - various NTFS related utilities Version 10.0.0.000

    Start time            : 10/03/2019 15:18:32.752 (UTC)
    
    Computer              : DESKTOP-8B106QG
    Volume name           : D:
    WARNING (Fonction incorrecte, hr=0x80070001): IOCTL_STORAGE_QUERY_PROPERTY does not support StorageAccessAlignmentProperty for this device "\\.\D:"
    [0000] 4D 5A 90 00 03 00 00 00 04 00 00 00 FF FF 00 00  MZ..............
    [0016] B8 00 00 00 00 00 00 00 40 00 00 00 00 00 00 00  ........@.......
    [0032] 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
    [0048] 00 00 00 00 00 00 00 00 00 00 00 00 38 01 00 00  ............8...
    [0064] 0E 1F BA 0E 00 B4 09 CD 21 B8 01 4C CD 21 54 68  ........!..L.!Th
    [0080] 69 73 20 70 72 6F 67 72 61 6D 20 63 61 6E 6E 6F  is program canno
    [0096] 74 20 62 65 20 72 75 6E 20 69 6E 20 44 4F 53 20  t be run in DOS
    [0112] 6D 6F 64 65 2E 0D 0D 0A 24 00 00 00 00 00 00 00  mode....$.......
    [0128] 55 D2 E6 79 11 B3 88 2A 11 B3 88 2A 11 B3 88 2A  U..y...*...*...*
    [0144] A5 2F 79 2A 1E B3 88 2A A5 2F 7B 2A AA B3 88 2A  ./y*...*./{*...*
    [0160] A5 2F 7A 2A 0F B3 88 2A 18 CB 0F 2A 15 B3 88 2A  ./z*...*...*...*
    [0176] 8F 13 4F 2A 13 B3 88 2A 43 DB 8C 2B 35 B3 88 2A  ..O*...*C..+5..*
    [0192] 43 DB 8B 2B 1A B3 88 2A 18 CB 0B 2A 12 B3 88 2A  C..+...*...*...*
    [0208] 43 DB 8D 2B 9


Explanations related to the warning can be found in the paragraph :ref:`NTFSUtil-enumlocs`.
    
``/mft`` Option
---------------

This option displays information about the Master File Table (MFT):

* number of records in MFT,
* location of the MFT extents
* information about the number of entries successfully parsed by the MFT walker.


It takes as argument the drive name. 

.. code:: bat

     .\DFIR-Orc.exe NTFSUtil /mft C:

.. code::

    NTFSUtil - various NTFS related utilities Version 10.0.0.000

    Start time            : 10/03/2019 15:14:25.444 (UTC)
    
    Computer              : DESKTOP-8B106QG
    Volume name           : D:
    WARNING (Fonction incorrecte, hr=0x80070001): IOCTL_STORAGE_QUERY_PROPERTY does not support StorageAccessAlignmentProper
    ty for this device "\\.\D:"
    
    Master File Table for volume D:\
            contains 256 records
            is located at ofset 0x0000000000004000 in the volume
    
    MFT has 1 segments:
            [0] Offset=0x0000000000004000, Size=0x0000000000040000, Allocated=0x0000000000040000, LowestVCN=0x00000000000000
    00
                    FILE(0x0000000000000000) inSequence
    
    Successfully walked 162 records (out of 256 elements, 63.28%)


Explanations related to the warning can be found in the paragraph :ref:`NTFSUtil-enumlocs`.

``/bitlocker`` Option
---------------

This option displays information about the meta data location (incl. protectors) on mounted BitLocker volumes or images.

Two syntaxes for this command:
* online: 
.. code:: bat

     .\DFIR-Orc.exe NTFSUtil /bitlocker

    The result of the command looks like:

    .. code:: bat
        BitLocker locations:

                \\.\PHYSICALDRIVE0,offset=129256914944,size=380912008704,sector=512
                        SectorSize: 512
                        Metadata offset[0]: 0x4d00000
                        Metadata   size[0]: 65536
                        Metadata offset[1]: 0x44d00000
                        Metadata   size[1]: 65536
                        Metadata offset[2]: 0x84d00000
                        Metadata   size[2]: 65536

                \\.\PHYSICALDRIVE0,offset=407896064,size=128849018368,sector=512
                        SectorSize: 512
                        Metadata offset[0]: 0x30bb24000
                        Metadata   size[0]: 65536
                        Metadata offset[1]: 0x30bb34000
                        Metadata   size[1]: 65536
                        Metadata offset[2]: 0x30bb44000
                        Metadata   size[2]: 65536

                \\.\PHYSICALDRIVE1,offset=33554432,size=393836756992,sector=512
                        SectorSize: 512
                        Metadata offset[0]: 0x4e00000
                        Metadata   size[0]: 65536
                        Metadata offset[1]: 0x44e00000
                        Metadata   size[1]: 65536
                        Metadata offset[2]: 0x84e00000
                        Metadata   size[2]: 65536

* offline:
.. code:: bat

     .\DFIR-Orc.exe NTFSUtil /bitlocker F:\BitLocker.vhd,offset=16777216"
    

    The result of the command looks like:

    .. code:: bat
        BitLocker locations:

                F:\Hyper-V\Virtual Hard Disks\BitLocker.vhd,offset=16777216
                        SectorSize: 512
                        Metadata offset[0]: 0x2200000
                        Metadata   size[0]: 65536
                        Metadata offset[1]: 0x9200000
                        Metadata   size[1]: 65536
                        Metadata offset[2]: 0x10200000
                        Metadata   size[2]: 65536
