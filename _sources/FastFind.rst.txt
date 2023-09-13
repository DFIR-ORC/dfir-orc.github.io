========
FastFind
========

Description
===========

The purpose of FastFind is to check for the presence of known indicators on large installed bases.

Since FastFind aims to analyze thousands of systems, it requires minimal interaction.
To achieve this goal, FastFind uses an XML configuration file embedded as a resource to specify the indicators to look for.
FastFind can leverage a collection of indicators to enable sophisticated indicator search.

FastFind can

* look up mounted file systems for known files using multiple indicators,
* look up registry hives from known signature (keys, values, ...), and
* look up Windows object directory for known objects (Pipes, Events, ...).

FastFind does **not**

* find sophisticated rootkits,
* collect data for ulterior analysis, and
* find traces of any other system compromise (i.e. it only searches for specific known threats).

FastFind is a standalone executable: it does not require any installation prior to execution. It is currently supported by the following Windows versions:

* Windows XP SP2 (Win32, x64), 
* Windows Server 2003 SP3 (Win32, x64), 
* Windows Vista SP1, SP2 (Win32, x64),
* Windows Server 2008 SP1, SP2 (Win32, x64),
* Windows Server 2012 (Win32, x64),
* Windows 7 RTM, SP1 (Win32, x64),
* Windows 8 RTM (Win32, x64),
* Windows Server 2012 NTFS volumes (Win32, x64),
* Windows 8.1 RTM (Win32, x64),
* Windows Server 2012 R2 (x64),
* Windows Server 2016,
* Windows Server 2019, and
* Windows 10 RTM ... 1903 (Win32, x64).

FastFind is using the same MFT parser as NTFSInfo but specifically targets indicator lookup.
For details on the MFT parser, please refer to :doc:`MFT parser configuration for details <fs_implem_details>`.

Output
======

Upon successful execution, FastFind outputs the result of its findings in an XML file, with one element per file system, registry or Windows object match.
It can also output up to two CSV files: one for the file system matches and one for the object matches.

Here is a sample XML output from the tool:

.. code:: xml

    <fast_find computer="JEANGABOOK" os="Microsoft Windows 10 Enterprise Edition (build 18362), 64-bit" role="WorkStation">
        <output>C:\temp\FastFind_output.xml</output>
        <filesystem>
            <filefind_match description="SHA256=E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855">
                <record frn="0x00080000000E75BC" volume_id="0xD2501A75501A6091" snapshot_id="{00000000-0000-0000-0000-000000000000}">
                    <standardinformation creation="2019-09-30 13:29:17.691" lastmodification="2019-09-30 13:33:16.007" lastaccess="2019-09-30 13:33:16.007" lastentrychange="2019-09-30 13:38:18.941" attributes="A............" />
                    <filename fullname="\temp\test.xml" creation="2019-09-30 13:29:17.691" lastmodification="2019-09-30 13:29:17.691" lastaccess="2019-09-30 13:29:17.691" lastentrychange="2019-09-30 13:29:17.691" />
                    <data filesize="0" MD5="D41D8CD98F00B204E9800998ECF8427E" SHA1="DA39A3EE5E6B4B0D3255BFEF95601890AFD80709" SHA256="E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855" />
                </record>
            </filefind_match>
            <filefind_match description="Name matches gdi*.dll">
                <record frn="0x0000000000000000" volume_id="0xB80097BC00978054" snapshot_id="{00000000-0000-0000-0000-000000000000}">
                    <i30 fullname="\Windows\SysWOW64\gdi32full.dll" parentfrn="0x00030000000789D7" creation="2019-07-30 12:01:07.896" lastmodification="2019-07-30 12:01:07.927" lastaccess="2019-07-30 12:04:46.430" lastentrychange="2019-07-30 12:05:26.670" />
                </record>
            </filefind_match>
        </filesystem>
        <registry>
            <hive volume_id="0xB80097BC00978054" snapshot_id="{00000000-0000-0000-0000-000000000000}" hive_path="\Windows\System32\config\SOFTWARE">
                <regfind_match description="KeyPath is \Microsoft\Windows\CurrentVersion\Run, Name is SecurityHealth">
                    <value key="\Microsoft\Windows\CurrentVersion\Run" value="SecurityHealth" type="REG_EXPAND_SZ" lastmodified_key="2019-10-02 15:14:29.043" data_size="88" />
                </regfind_match>
            </hive>
        </registry>
        <object>
            <object_match description="SymbolicLink'name is Partition0">
                <object type="SymbolicLink" name="Partition0" path="\Device\Harddisk0\Partition0" link_target="\Device\Harddisk0\Partition0" link_creationtime="2019-10-10 00:17:49.107" />
            </object_match>
            <object_match description="Driver'name is CNG">
                <object type="Driver" name="CNG" path="\Driver\CNG" link_target="\Driver\CNG" />
            </object_match>
        </object>
    </fast_find>

The output XML file is separated in three sections: ``filesystem``, ``registry`` and ``object``.

File System Match
-----------------

In the XML file, each file system match is enclosed inside a ``filefind_match`` element. This element has an attribute ``description`` that reports the rule which matched.

In both CSV and XML outputs, the following information is retrieved for a file system match:

.. csv-table::
    :header: CSV ColumnName, XML Attribute, Description
    :align: left
    :widths: auto
    
    ComputerName, computer (``fast_find`` element), Name of the computer
    VolumeID, volume_id (``record`` element), Id of the volume
    SnapshotID, snapshot_id (``record`` element), Snapshot associated with this entry
    FRN,frn (``record`` element), FRN of this entry
    ParentFRN, parentfrn (``filename`` or ``i30`` element), FRN of the parent directory
    FullName, fullname (``filename`` or ``i30`` element), Full pathname for this entry
    SizeInBytes, filesize (``data`` element), File size in bytes
    Description, description (``filefind_match`` element), The rule that matched this entry
    CreationDate, creation (``standardinformation`` element), File creation date (yyyy-MM-dd hh:mm:ss.SSS)
    LastModificationDate, lastmodification (``standardinformation`` element), File last write date (yyyy-MM-dd hh:mm:ss.SSS)
    LastAccessDate, lastaccess (``standardinformation`` element), File last read access date (yyyy-MM-dd hh:mm:ss.SSS)
    LastAttrChangeDate, lastentrychange (``standardinformation`` element), File last attribute change date (yyyy-MM-dd hh:mm:ss.SSS)
    FileNameCreationDate, creation (``filename`` or ``i30`` element), File name (hard link) creation date (yyyy-MM-dd hh:mm:ss.SSS)
    FileNameLastModificationDate, lastmodification (``filename`` or ``i30`` element), File name (hard link) last modification date (yyyy-MM-dd hh:mm:ss.SSS)
    FileNameLastAccessDate, lastaccess (``filename`` or ``i30`` element), File name (hard link) last read access date (yyyy-MM-dd hh:mm:ss.SSS)
    FileNameLastAttrChangeDate, lastentrychange (``filename`` or ``i30`` element), File name (hard link) last attribute change date (yyyy-MM-dd hh:mm:ss.SSS)
    MD5, MD5 (``data`` element), Cryptographic MD5 hash
    SHA1, SHA1 (``data`` element), Cryptographic SHA1 hash
    SHA256, SHA256 (``data`` element), Cryptographic SHA256 hash
    

Registry Match
--------------

In the XML output file, each parsed hive, whether FastFind found a match in it or not, is listed in a ``hive`` element.
If a match was found, it is enclosed inside a ``regfind_match`` element.
This element has an attribute ``description`` that reports the rule which matched.

The following information is retrieved for a file system match:

.. csv-table::
    :header: XML Attribute, Description
    :align: left
    :widths: auto
    
    computer (``fast_find`` element), Name of the computer
    volume_id (``hive`` element), Id of the volume
    snapshot_id (``hive`` element), Snapshot associated with this entry
    hive_path (``hive`` element), Full path of the hive
    description (``regfind_match`` element), The rule that matched this entry
    key (``value`` element), Registry key (full path)
    value (``value`` element), Key value
    type (``value`` element), Type of the key data
    lastmodified_key (``value`` element), Registry key last modification date (yyyy-MM-dd hh:mm:ss.SSS)
    data_size (``value`` element), Size of the data

Windows Object Match
--------------------

In the XML file, each object match is enclosed inside an ``object_match`` element. This element has an attribute ``description`` that reports the rule which matched.

In both CSV and XML outputs, the following information is retrieved for a file system match:

.. csv-table::
    :header: CSV ColumnName, XML Attribute, Description
    :align: left
    :widths: auto
    
    ComputerName, computer (``fast_find`` element), Name of the computer
    OperatingSystem, os (``fast_find`` element), OS version (full string)
    Description, description (``object_match`` element), The rule that matched this entry
    ObjectType, type (``object`` element), Type of the object (Mutex Driver etc.)
    ObjectName, name (``object`` element), Name of the object
    ObjectPath, path (``object`` element), Path of the object
    LinkTarget, link_target (``object`` element), Target for the symbolic link (when the object is a symbolic link)
    LinkCreationTime, link_creationtime (``object`` element), Link creation date (yyyy-MM-dd hh:mm:ss.SSS)


As for every tool, an output for logging is also available from the command line. The syntax can be found in :doc:`Configuring Console Output <configuring_console_output>`.

Usage
=====

FastFind can be used from the command line using the following syntax:

.. code:: bat

    DFIR-Orc.exe FastFind /config=fastfind.xml /out=fastfind_output.xml
    
``/config=<Path>`` Option
-------------------------

*optional=no, default=N/A*

Takes an XML configuration file as argument.

A typical XML configuration file looks like the following:

.. code:: xml

    <fastfind version="Test 2.0">
        <filesystem>
            <location shadows="yes">%SystemDrive%</location>
            <yara source="yara.rules" block="2M" timeout="120" overlap="8192" scan_method="filemapping" />
            <ntfs_find size="694160" md5="1CECAFE147F1CC3E2B9804B8CDA593C9"/>
            <ntfs_find name="ntdll.dll" yara_rule="is_dll"/>
            <ntfs_find name_match="gdi*.dll"/>
            <ntfs_exclude path="\Windows\System32\ntdll.dll"/>
            <ntfs_exclude path_match="\Windows\System32\gdi*.dll"/>
            <ntfs_exclude sha1="c766364efd9c9b5aa3a7140a69f0cf5b147bc476"/>
            <ntfs_exclude size="14966411"/>
            <ntfs_exclude contains="bcryptprimitives.pdb"/>
        </filesystem>
        <registry>
            <location>%SystemDrive%\</location>
            <hive name="NTUSER">
                <ntfs_find name="NTUSER.DAT"/>
                <registry_find key_path="\Software\Microsoft\Internet Explorer\Main" value="Check_Associations" data="no"/>
            </hive>
            <hive name="SOFTWARE">
                <ntfs_find name="SOFTWARE"/>
                <registry_find key_path="\Microsoft\Windows\CurrentVersion\Run" value="SecurityHealth"/>
            </hive>
        </registry>
        <object>
            <object_find type="Mutant" name="foo"/>
            <object_find type="File" name="foobar"/>
        </object>
    </fastfind>

The XML configuration file for FastFind contains:

* A root element ``<fastfind>`` with a ``version`` attribute that is displayed when the tool runs (typically identifying the campaign),
* A section ``<filesystem>`` to look for specific files,
* A section ``<registry>`` to look for registry keys or values,
* A section ``<object>`` to look for windows objects.

In each of these sections, three additional elements can be specified:

* locations to specify where to look for, following the syntax described in :doc:`Configuring Locations <configuring_locations>`,
* yara rules, following the syntax described in :doc:`Configuring Yara scanner <configuring_yara>`, and
* a collection of indicators to search for:
    * ``ntfs_find`` and ``ntfs_exclude`` elements for file system indicators. The syntax is detailed in the :doc:`ntfs_find documentation <configuring_ntfs_opt>`,
    * ``registry_find`` elements for registry indicators. The syntax is detailed in the :ref:`RegInfo <RegInfo_Registryfind>`,
    * ``object_find`` elements for object indicators. The syntax is detailed in the :doc:`ObjInfo <ObjInfo>`.

The ``<filesystem>`` element accept the following 'resurrect' attribute to specify that deleted entries should be parsed.

* **resurrect** *(optional=yes, default=no)*, ``/ResurrectRecords=<yes|no|resident>`` Option

The MFT parser can be configured to include deleted records. This option can provide information about recently deleted file system entries.
This can, by design, incur unpredictable results (as we are using unreliable or partially deleted information).
One can generally assume that resident attributes for those entries are valid unlike nonresident attributes that are most likely quickly invalidated after the entry deletion.
Use the option value ``resident`` to limit parsed deleted entries to resident ones.

..  csv-table::
    :header: Value, Description
    :widths: auto
    :align: left

    *yes*, "Enable deleted records recovery"
    *resident*, "Enabled deleted resident records only recovery"
    *no*,  "Do not try to recover deleted records"


Others available command line options are:

``/out=<Path>`` Option
-----------------------

*optional=yes, default=N/A*

This option allows to specify a XML file or a directory to output results.
For details on the ``/out`` option syntax, please refer to the :doc:`output documentation <configuring_tool_output>`.

Whether this option is used or not, the tool outputs its result to the console.

``/filesystem=<Path>`` Option
-----------------------------

*optional=yes, default=N/A*

Adds matching indicator information about the file system in a CSV file. File name provided in ``<Path>`` value must have a ``.csv`` extension and if a full path is not specified, file is created in the current directory.

``/object=<Path>`` Option
-------------------------

*optional=yes, default=N/A*

Adds matching indicator information about Windows objects in a CSV file. File name provided in ``<Path>`` value must have a ``.csv`` extension and if a full path is not specified, file is created in the current directory.

``/registry=<Path>`` Option
-------------------------

*optional=yes, default=N/A*

Adds matching indicator information about the registry in a CSV file. File name provided in ``<Path>`` value must have a ``.csv`` extension and if a full path is not specified, file is created in the current directory.

``/SkipDeleted`` Option
-----------------------

*optional=yes, default=Inactive*

Ignores deleted files. They are matched against by default.

``/Names=<File1>,...`` Option
-----------------------------

*optional=yes, default=N/A*

Adds one or more filenames to the list of indicators.

  .. code:: bat

    /Names=MyFile.txt,My*.sys,*.txt#EAName

``/Version=<VersionString>`` Option
-----------------------------------

*optional=yes, default=N/A*

Specifies a version string. Overrides the value in XML file.

  .. code:: bat

    /Version="Diskpart V1.0"
    

``/Yara=<YaraFile1>,...`` Option
--------------------------------

*optional=yes, default=N/A*

This option allows to provide a comma-separated or semicolon-separated list of yara files. Those rules are added to the ones specified in the configuration file if they exist.
