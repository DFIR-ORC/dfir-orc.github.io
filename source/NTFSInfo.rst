
========
NTFSInfo
========

Description
===========

NTFSInfo is intended to collect details on data stored on NTFS mounted volumes, raw disk images or Volume Shadow Copies.
Basically, the tool enumerates the file system entries and outputs user-specified details to collect in one or more CSV file.

NTFSInfo can walk the file system using two different techniques: the USN journal enumeration or raw MFT parsing. Their implementation is detailed in :doc:`parser implementation details<fs_implem_details>`.

While the two parsers (MFT and USN) enumerate the file system entries, there are key differences between the two approaches:

* USN parser creates one line per USN record returned. The MFT parser, however, can potentially create multiple lines per MFT record:
    * One line per ``$FILE_NAME`` attribute (hard links)
    * One line per ``$DATA`` attribute (ADSs)

    One can identify the lines referencing the same MFT record by looking at the FRN column.

    For example, below, FRN 0x00DB00000002442B, which has two names (one long, one short) and one Alternate Data Stream, NTFSInfo output looks like:

    .. csv-table::
        :header: File, FRN
        :widths: auto
        :align: left

        GETTHI~2.ZIP, 0x00DB00000002442B
        GETTHI~2.ZIP:Zone.Identifier, 0x00DB00000002442B
        GetThis (3).zip, 0x00DB00000002442B
        GetThis (3).zip:Zone.Identifier, 0x00DB00000002442B

    If several attributes (whether ``$FILE_NAME`` or ``$DATA``) are present inside the USN record, only one line is written by the USN parser.
    In particular, the ``$FILE_NAME`` attribute is selected by the system and not the tool.

* The USN parser can enumerate Alternate Data Streams in the ADS column, one line per ADS. However, only the MFT parser will provide details on the ADS itself (size, hashes, PE Header, etc.). The USN parser will only detail the default stream.


.. _NTFSInfo-output:

Output
======

NTFSInfo can collect up to five different types of information:

* :ref:`FileInfo <ntfsinfo_fileinfo>`,
* :ref:`AttrInfo <ntfsinfo_attrinfo>`,
* :ref:`I30Info <ntfsinfo_i30info>`,
* :ref:`TimeLine <ntfsinfo_timeline>`, and
* :ref:`SecDescr <ntfsinfo_secdescr>`.

Data is stored in **CSV** files.

If no output option is specified, only the ``FileInfo`` information is collected in ``NTFSInfo.csv``.

.. note::
    For verbose logging output refer to :doc:`Configuring Console Output <configuring_console_output>`.

.. _ntfsinfo_fileinfo:

FileInfo
--------

This file contains the following information on files and folders:

* **Volume Identification:**
    * **ComputerName:** Name of the computer
    * **VolumeID:** Id of the volume
* **Standard Information:**
    * **FullName:** Full-path name
    * **File:** Name of the file
    * **ParentName:** Name of the parent folder
    * **Extension:** Optional file name extension (split path)
    * **Attributes:** FAT file system attributes
    * **SizeInBytes:** File size in bytes
* **Date Information:**
    * **CreationDate:** File creation date *"mm/dd/yyyy hh\:mm\:ss.000"*
    * **LastModificationDate:** File last write date *"mm/dd/yyyy hh\:mm\:ss.000"*
    * **LastAccessDate:** File last read access date
    * **LastAttrChangeDate:** Last Attribute change date (MFT information changed) *"mm/dd/yyyy hh\:mm\:ss.000"*
    * **FileNameCreationDate:** File name (hard link) creation date
    * **FileNameLastAccessDate:** File name (hard link) access date
    * **FileNameLastDataModificationDate:** File name (hard link) last date *data* was modified
    * **FileNameLastAttrModificationDate:** File name (hard link) last date MFT *attribute* was modified
* **FirstBytes:** First 16 bytes (in hex) of the ``$DATA`` attribute content.
* **Security:**
    * **OwnerSID:** SID of the owner for this entry
    * **Owner:** Name of the owner for this entry
    * **SecDescrID** ID of security descriptor for the file
* **PE Header related information:**
    * **Platform:** PE Header platform
    * **TimeStamp:** PE Header timestamp
    * **SubSystem:** PE Header SubSystem
* **Version Information:**
    * **FileOS:** VersionInfo OS tag
    * **FileType:** VersionInfo type
    * **Version:** VersionInfo file version
    * **CompanyName:** VersionInfo company name
    * **ProductName:** VersionInfo product name
    * **OriginalFileName:** VersionInfo original file name
* **ShortName:**
    * **Short Name** (8.3) if any
* **Cryptographic/Authenticode Information:**
    * **MD5:** Cryptographic MD5 hash (in hex)
    * **SHA1:** Cryptographic SHA1 hash (in hex)
    * **SHA256:** Cryptographic SHA256 hash (in hex)
    * **PeMD5:** Authenticode (PE) file MD5 hash
    * **PeSHA1:** Authenticode (PE) file SHA1 hash
    * **PeSHA256:** Authenticode (PE) file SHA256 hash
    * **AuthenticodeStatus:** Status of the authenticode signature for the file. Possible values are:
        * **Unknown:** Status failed to be determined
        * **Empty string:** File is not a PE
        * **SignedVerified:** File is signed and the signature verified
        * **CatalogSignedVerified:** File hash is listed in a catalog
        * **SignedNotVerified:** File signature does _not_ verify
        * **NotSigned:** No signature or catalog could be found for this file
    * **AuthenticodeSigner:** Signer's certificate (value of the first occurrence of the attributes szOID_COMMON_NAME, szOID_ORGANIZATIONAL_UNIT_NAME, szOID_ORGANIZATION_NAME, or szOID_RSA_emailAddr)
    * **AuthenticodeSignerThumbprint:** Signer's certificate hash
    * **AuthenticodeCA:** Signer's root CA certificate (value of the first occurrence of the attributes szOID_COMMON_NAME, szOID_ORGANIZATIONAL_UNIT_NAME, szOID_ORGANIZATION_NAME, or szOID_RSA_emailAddr)
    * **AuthenticodeCAThumbprint:** Signer's root CA certificate hash
    * **SecurityDirectory** Base64 encoded security directory of the PE file (if present)
* **Alternate Storage areas:**
    * **ADS:** Alternate Data Stream Information
    * **ExtendedAttribute:** Colon separated names of the extended attributes (``$EA`` attribute content)
* **Reference Numbers**
    * **USN:** Update Sequence Number (last USN added in the journal for this entry)
    * **FRN:** File Reference Number (version index of the entry in the MFT)
* **RecordInUse:** Boolean which indicates if this record was in use or free (i.e. deleted)
* **FilenameFlags:** Type of file name (POSIX=0,WIN32=1,DOS83=2)
* **FilenameID:** Attribute ID for this ``$FILE_NAME``
* **DataID:** Attribute ID for this ``$DATA``
* **Status:** File lock status (per CreateFile return value, if available)
* **OwnerID:** Owner ID for this entry (ID for quotas, not security)
* **FilenameIndex:** Index of this ``$FILE_NAME`` in this record
* **DataIndex:** Index of this ``$DATA`` in this record
* **SnapshotID:** Snapshot associated with this entry
* **SSDeep:** Fuzzyhash SSDeep
* **TLSH:** Trend Micro's TLSH
* **SignedHash:** Signed hash inside the security directory of the PE

The Attributes column may contain the following flags:

    .. csv-table::
        :header: Flag, Letter used (in this order)
        :widths: auto
        :align: left

        FILE_ATTRIBUTE_ARCHIVE, A
        FILE_ATTRIBUTE_COMPRESSED, C
        FILE_ATTRIBUTE_DIRECTORY, D
        FILE_ATTRIBUTE_ENCRYPTED, E
        FILE_ATTRIBUTE_HIDDEN, H
        FILE_ATTRIBUTE_NORMAL, N
        FILE_ATTRIBUTE_OFFLINE, O
        FILE_ATTRIBUTE_READONLY, R
        FILE_ATTRIBUTE_REPARSE_POINT, L
        FILE_ATTRIBUTE_SPARSE_FILE, P
        FILE_ATTRIBUTE_SYSTEM, S
        FILE_ATTRIBUTE_TEMPORARY, T
        FILE_ATTRIBUTE_VIRTUAL, V
        FILE_ATTRIBUTE_DEVICE, d
        FILE_ATTRIBUTE_NOT_CONTENT_INDEX, I
        FILE_ATTRIBUTE_INTEGRITY_STREAM, s
        FILE_ATTRIBUTE_NO_SCRUB_DATA, B
        FILE_ATTRIBUTE_EA, e
        FILE_ATTRIBUTE_PINNED, p
        FILE_ATTRIBUTE_UNPINNED, u
        FILE_ATTRIBUTE_RECALL_ON_OPEN, o
        FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS, a

Detailed documentation of these flags can be found at: https://docs.microsoft.com/en-us/windows/win32/fileio/file-attribute-constants

.. _ntfsinfo_attrinfo:

AttrInfo
--------

This file contains NTFS attributes related information. The output CSV file contains the following information:

.. csv-table::
    :header: Value, Description
    :widths: auto
    :align: left
    
    ComputerName, Name of the computer
    VolumeID, ID of the volume
    FRN, FRN for this attribute
    HostFRN, FRN hosting this attribute (if HostFRN != FRN then this attribute is hosted in a child MFT record)
    Type, Type of the attribute
    Name, Attribute name
    Form, Resident or NonResident
    Size, Attribute size
    Flags, Attribute flags
    Instance, Unique instance for this attribute in the file record
    Index, Attribute index for this attribute type 
    LowestVCN, Lowest virtual cluster number (VCN) covered by this attribute record.
    SnapshotID, ID of the snapshot

The Type column can have the following values:

* ``$UNUSED``
* ``$STANDARD_INFORMATION``
* ``$ATTRIBUTE_LIST``
* ``$FILE_NAME``
* ``$OBJECT_ID``
* ``$SECURITY_DESCRIPTOR``
* ``$VOLUME_NAME``
* ``$VOLUME_INFORMATION``
* ``$DATA``
* ``$INDEX_ROOT``
* ``$INDEX_ALLOCATION``
* ``$BITMAP``
* ``$REPARSE_POINT``
* ``$EA_INFORMATION``
* ``$EA``
* ``$LOGGED_UTILITY_STREAM``
* ``$FIRST_USER_DEFINED_ATTRIBUTE``
* ``$END``

The ``Flags`` attribute can have the following `values <https://docs.microsoft.com/en-us/windows/win32/devnotes/attribute-record-header>`_:

* ATTRIBUTE_FLAG_COMPRESSION_MASK (0x00FF)
* ATTRIBUTE_FLAG_SPARSE (0x8000)
* ATTRIBUTE_FLAG_ENCRYPTED (0x4000)

.. _ntfsinfo_i30info:

I30Info
-------

This file contains information from the volume ``$I30`` attributes (directories) stored ``$FILE_NAME`` copies:

.. csv-table::
    :header: Value, Description
    :widths: auto
    :align: left
    
    ComputerName, Name of the computer
    VolumeID, ID of the volume
    CarvedEntry, \"Y\" or \"N\" depending on whether this entry was carved
    FRN, File Reference Number (version index of the entry in the MFT)
    ParentFRN, FRN of the parent directory
    Name, File name
    FilenameID, Attribute ID for this ``$FILE_NAME``
    FileNameCreationDate, File name (hard link) creation date
    FileNameLastModificationDate, File name (hard link) access date
    FileNameLastAccessDate, File name (hard link) last date data was modified
    FileNameLastAttrModificationDate, File name (hard link) last date MFT attribute was modified
    SnapshotID, ID of the VSS snapshot

.. _ntfsinfo_timeline:

TimeLine
--------

This file contains information one "date/time" per line.
This file is **not** sorted.

.. csv-table::
    :header: Value, Description
    :widths: auto
    :align: left
    
    ComputerName, Name of the computer
    VolumeID, ID of the volume
    KindOfDate, Nature of the date reported.
    TimeStamp, Timestamp for this event
    FRN, File Reference Number
    FilenameID, ID of the ``$FILE_NAME`` associated with this event
    SnapshotID, ID of the VSS snapshot

The KindOfDate column can hold the following values:

* CreationTime
* LastModificationTime
* LastAccessTime
* LastChangeTime
* FileNameCreationDate
* FileNameLastModificationDate
* FileNameLastAccessDate
* FileNameLastAttrModificationDate

.. _ntfsinfo_secdescr:

SecDescr
--------

This file contains Security Descriptors information (as stored in the ``$SDS`` data stream for the volume):

.. csv-table::
    :header: Value, Description
    :widths: auto
    :align: left
    
    ComputerName, Name of the computer
    VolumeID, ID of the volume
    ID, ID of this Security Descriptor (as referred to by :ref:`SecDescrID in FileInfo <ntfsinfo_fileinfo>` column)
    Hash, Hash (*not* a Cryptographic hash)
    SDDL, Security descriptor in `SDDL format <https://docs.microsoft.com/en-us/windows/win32/secauthz/security-descriptor-definition-language>`_
    SecDescrSize, Declared size of the security descriptor (per `GetSecurityDescriptorLength <https://docs.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-getsecuritydescriptorlength>`_)
    NormalisedSize, Normalised size of the SD (per `ConvertStringSecurityDescriptorToSecurityDescriptor <https://docs.microsoft.com/en-us/windows/win32/api/sddl/nf-sddl-convertstringsecuritydescriptortosecuritydescriptorw>`_)
    DataSize, Actual stored blob size in ``$SDS`` stream (http://www.ntfs.com/ntfs-permissions-security-descriptor.htm)
    SnapshotId, VSS Snapshot ID
    
Usage
=====

NTFSInfo can be used from command line or with XML configuration file. Both provide (mostly) identical access to NTFSInfo functionality even if the configuration files allow for more complexity.

* Command-line parameters example:

..  code:: bat

    DFIR-Orc.exe NTFSInfo "%SystemDrive%\Program Files" /fileinfo=%TEMP%\test.csv /logfile=%TEMP%\NTFSInfo.log /Dates,File,ParentName,USN,FRN,LastAttrChangeDate,ADS,SizeInBytes

* XML configuration file example:

.. code:: xml

    <ntfsinfo walker="MFT">
        <fileinfo>%TEMP%\test.csv</fileinfo>
        <logging file="%TEMP%\NTFSInfo.log" />
        <location>%SystemDrive%\Program files</location>
        <columns>
            <default>Dates</default>
            <default>File</default>
            <default>ParentName</default>
            <default>USN,FRN</default>
            <default>LastAttrChangeDate</default>
            <default>ADS</default>
            <default>SizeInBytes</default>
        </columns>
    </ntfsinfo>


The XML configuration file is provided by using the parameter ``/config``:

.. code:: bat
 
    DFIR-Orc.exe NTFSInfo /config=%TEMP%\NTFSInfoConfig.xml

.. note::

    All output related parameters (in the configuration file and in the command line) can use environment variables.

``ntfsinfo`` Element
--------------------

*optional=no, default=N/A*

Root element.

Attributes
``````````

* **walker** *(optional=no, default=MFT)*, ``/Walker`` Option:

NTFSInfo can only use one parser per execution. The choice of the parser is very important as it impacts the CSV output.

.. csv-table::
    :header: Value, Description
    :widths: auto
    :align: left

    USN, "The *USN parser* can be faster under certain circumstances and is maintained only for completeness."
    MFT, "The *MFT parser* is the most complete with detailed ADS and hard links in the output."


.. important::

    - The *USN Parser* option is **DEPRECATED**
    - The *USN Parser* can be very slow on recent NTFS volumes.


Configuring the parser to parse deleted entries

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


``location`` Element
--------------------

Specify the parsed system. For details on the syntax, please refer to the :doc:`configuring locations documentation<configuring_locations>`.

When using the command line, this element must be provided in the form of a space separated list, as an argument at the end of the command:

.. code:: bat

    DFIR-Orc.exe NTFSInfo <Location1> <Location2>

``FileInfo`` Element, ``/FileInfo=<Path>`` Option
-------------------------------------------------

*optional=yes, default=NTFSInfo.csv*

``FileInfo`` contains general file information about the files in one or more volumes.

The syntax is similar to the ``output`` element or ``\out`` option used in other tools, described in the :doc:`output documentation <configuring_tool_output>`.

When provided with a directory or an archive, it creates one file per NTFS volume instead of one unique file.

If no output option is specified, only the ``FileInfo`` information is collected in a file called ``NTFSInfo.csv``.

.. note::

    The option ``/out`` has the same behavior as ``/fileinfo``.


.. _AttrInfo:

``AttrInfo`` Element, ``/AttrInfo=<Path>`` Option
-------------------------------------------------

*optional=yes, default=N/A*

``AttrInfo`` contains detail information about the attributes in ``$MFT``.

The syntax is similar to the ``output`` element or ``\out`` option used in other tools, described in the :doc:`output documentation <configuring_tool_output>`.

When provided with a directory or an archive, it creates one file per NTFS volume instead of one unique file.

.. _I30info:

``I30info`` Element, ``/I30info=<Path>`` Option
-----------------------------------------------

*optional=yes, default=N/A*

``I30Info`` contains detailed information about the data stored inside ``$I30`` attributes.

The syntax is similar to the ``output`` element or ``\out`` option used in other tools, described in the :doc:`output documentation <configuring_tool_output>`.

When provided with a directory or an archive, it creates one file per NTFS volume instead of one unique file.

.. _TimeLine:

``TimeLine`` Element, ``/TimeLine=<Path>`` Option
-------------------------------------------------

*optional=yes, default=N/A*

``TimeLine`` contains a unique view of all dated information in ``$MFT`` (``$STANDARD_INFORMATION`` and ``$FILE_NAME``)

The syntax is similar to the ``output`` element or ``\out`` option used in other tools, described in the :doc:`output documentation <configuring_tool_output>`.

When provided with a directory or an archive, it creates one file per NTFS volume instead of one unique file.

.. _SecDescr:

``SecDescr`` Element, ``/SecDescr=<Path>`` Option
-------------------------------------------------

*optional=yes, default=N/A*

``SecDescr`` contains the security descriptors for the parsed volumes.

The syntax is similar to the ``output`` element or ``\out`` option used in other tools, described in the :doc:`output documentation <configuring_tool_output>`.

When provided with a directory or an archive, it creates one file per NTFS volume instead of one unique file.

``Columns`` Element
-------------------

*optional=yes, default=N/A*

This element is a container for sub-elements that allow to define the information NTFSInfo must collect or not.

``Default`` Element (in ``Columns``), ``/<DefaultColumnSelection>,...`` Option
---------------------------------------------------------------------------------

*optional=yes, default=Default* (see "Default" alias)

NTFSInfo allows fine grained selection of information collected in ``FileInfo`` output CSVs. This allows groups of columns to be specified in a way you find convenient.

Selection is specified using a comma-separated list of columns.

The following example will output the file name, its parent full-path, and its MD5 hash.

* Command-line parameter:

..  code:: bat

    /File,ParentName,MD5

* XML elements:

..  code:: xml

    <columns>
        <default>File,ParentName,MD5</default>
    </columns>

..  note::
    *Option* or *Element* can be specified multiple times

Here is a complete list of the available columns:

    ..  csv-table::
        :header: Column name, Description
        :widths: auto
        :align: left

        ADS, "Alternate Data Stream Information"
        Attributes, "FAT file system attributes"
        AuthenticodeCA, "Authority of signer of this file's signature"
        AuthenticodeCAThumbprint, "Thumbprint of the authority of the signer of this file's signer"
        AuthenticodeSigner, "Signer of this file's signature"
        AuthenticodeSignerThumbprint, "Thumbprint of the signer of this file's signer"
        AuthenticodeStatus, "Status of this file regarding authenticode signature (SignedVerified,SignedNotVerified,NotSigned)"
        CompanyName, "VersionInfo company name"
        ComputerName, "Computer name"
        CreationDate, "File creation date"
        DataID, "``$DATA`` Attribute Instance ID"
        DataIndex, "Index of this ``$DATA`` in this record"
        EASize, "Size in bytes of the extended attributes (if present)"
        ExtendedAttribute, "Extended Attribute Information"
        Extension, "Optional file name extension (split path)"
        File, "Name of the file"
        FileNameCreationDate, "Indicates when this file created using this name"
        FilenameFlags, "``$FILE_NAME`` Attribute Flags (POSIX=0, WIN32=1, DOS83=2)"
        FilenameID, "``$FILE_NAME`` Attribute Instance ID"
        FilenameIndex, "Index of this ``$FILE_NAME`` in this record"
        FileNameLastAccessDate, "Indicates when this file was last read using this name"
        FileNameLastAttrModificationDate, "Indicates when this file's attributes were last modified using this name"
        FileNameLastModificationDate, "Indicates when this file's data was last modified using this name"
        FileOS, "VersionInfo OS tag"
        FileType, "VersionInfo type"
        FirstBytes, "First bytes of the data stream"
        FRN, "File Reference Number"
        FullName, "Full-path name"
        LastAccessDate, "File last read date (pre-vista)"
        LastAttrChangeDate, "Last Attribute Change Date"
        LastModificationDate, "File last write date"
        MD5, "Cryptographic MD5 hash (in hex)"
        OriginalFileName, "VersionInfo original file name"
        Owner, "File owner"
        OwnerId, "File owner's unique ID"
        OwnerSid, "File owner's SID"
        ParentFRN, "Parent Folder Reference Number"
        ParentName, "Name of the parent folder"
        PeMD5, "MD5 of PE file"
        PeSHA1, "SHA1 of PE file"
        PeSHA256, "SHA256 of a PE file"
        Platform, "PE Header platform"
        ProductName, "VersionInfo product name"
        RecordInUse, "Indicates if the record is in use (or freed/deleted)"
        SecDescrID, "ID of security descriptor for the file"
        SecurityDirectory, "Base64 encoded security directory of the PE file (if present)"
        SHA1, "Cryptographic SHA1 hash (in hex)"
        SHA256, "SHA256"
        ShortName, "Short Name (8.3) if any"
        SignedHash, "The signed hash inside the security directory of the PE"
        SizeInBytes, "File size in bytes"
        SnapshotID, "Snapshot associated with this entry"
        SSDeep, "Fuzzyhash SSDeep"
        SubSystem, "PE Header SubSystem"
        TimeStamp, "PE Header timestamp"
        TLSH, "Trend Micro's TLSH"
        USN, "Update Sequence Number"
        Version, "VersionInfo file version"
        VolumeID, "Volume ID"

Instead of column names, aliases can also be used. They simplify the syntax by regrouping a set of related columns.

Here is a complete list of available aliases:

    ..  csv-table::
        :header: Alias, Columns name
        :widths: auto
        :align: left

        Default, "File, ParentName, Extension, SizeInBytes, Attributes, CreationDate, LastModificationDate, LastAccessDate, LastAttrChangeDate, FileNameCreationDate, FileNameLastModificationDate, FileNameLastAccessDate, FileNameLastAttrModificationDate, USN, FRN, ParentFRN, ExtendedAttribute, ADS, FilenameID, DataID, RecordInUse, OwnerId, FilenameFlags, SecDescrID, FilenameIndex, DataIndex, SnapshotID"
        DeepScan, "File, ParentName, Extension, SizeInBytes, Attributes, CreationDate, LastModificationDate, LastAccessDate, ShortName, MD5, SHA1, Owner, Version, CompanyName, ProductName, OriginalFileName, Platform, TimeStamp, SubSystem, FileType, FileOS"
        Details, "Version, CompanyName, ProductName, OriginalFileName, Platform, TimeStamp, SubSystem, FileType, FileOS"
        Hashes, "MD5, SHA1, SHA256"
        Fuzzy, "SSDeep, TLSH"
        PeHashes, "PeSHA1, PeSHA256, PeMD5"
        Dates, "CreationDate, LastModificationDate, LastAccessDate, LastAttrChangeDate, FileNameCreationDate, FileNameLastModificationDate, FileNameLastAccessDate, FileNameLastAttrModificationDate"
        RefNums, "USN, FRN, ParentFRN"
        Authenticode, "AuthenticodeStatus, AuthenticodeSigner, AuthenticodeSignerThumbprint, AuthenticodeCA, AuthenticodeCAThumbprint, SignedHash"
        All, "LastModificationDate, LastAccessDate, LastAttrChangeDate, FileNameCreationDate, FileNameLastModificationDate, FileNameLastAccessDate, FileNameLastAttrModificationDate, USN, FRN, ParentFRN, ExtendedAttribute, ADS, FilenameID, DataID, RecordInUse, ShortName, MD5, SHA1, FirstBytes, OwnerId, OwnerSid, Owner, Version, CompanyName, ProductName, OriginalFileName, Platform, TimeStamp, SubSystem, FileType, FileOS, FilenameFlags, SHA256, PeSHA1, PeSHA256, SecDescrID, EASize, SecurityDirectory, AuthenticodeStatus, AuthenticodeSigner, AuthenticodeSignerThumbprint, AuthenticodeCA, AuthenticodeCAThumbprint, PeMD5, FilenameIndex, DataIndex, SnapshotID, SSDeep, TLSH, SignedHash"

..  note::

    The command ``DFIR-Orc.exe ntfsinfo /?`` will print all column definitions along with the definition of aliases.


``add`` and ``omit`` Elements (in ``Columns``), ``/(+|-)<ColumnSelection>:criteria=<value>`` Option
---------------------------------------------------------------------------------------------------

*optional=yes, default=N/A*

NTFSInfo allows to selectively add or remove columns content depending on a filter.
Filtering column content can help reduce resource consumption for some columns (e.g. MD5, AuthenticodeStatus).

A filter is built on an *action*, a *criterion* and the targeted column.

* Available *criteria*:

    ..  csv-table::
        :header: Criteria, Description
        :widths: auto
        :align: left

        "HasVersionInfo", "The file has a VERSION_INFO resource"
        "HasPE", "The file has a valid PE header"
        "ExtBinary", "The file has an executable extension (like .exe, .dll, .scr, .sys, ...)"
        "ExtArchive", "The file has a archive extension (like .zip, .cab, ...)"
        "Ext=.Ext1,.Ext2,...", "The file has extension in .Ext1,.Ext2,..."
        "SizeLT=size, SizeGT=size", "The file is smaller or bigger than a specified size. Note that size can be expressed in KB (i.e. SizeGT=25K...) or in MB (i.e. SizeLT=5M etc...)"


* Available *actions*:

    ..  csv-table::
        :header: Action, Description
        :widths: auto
        :align: left

        add / \+, Computes the column content
        remove / \-, Do not compute the column content

Example 1: only computes the column SHA1 if the file size is smaller than 1 MB.

* Command-line parameter:

    ..  code:: bat

        /+SHA1:SizeLT=1M

* XML element:

    ..  code:: xml

        <columns>
            <add SizeLT="1M">SHA1</add>
        </columns>

Example 2: do not compute MD5 if the file has an archive extension (.cab, .zip).

* Command-line parameter:

    ..  code:: bat

        /-MD5:ExtArchive

* XML element:

    ..  code:: xml

        <columns>
            <omit ExtArchive="">MD5</omit>
        </columns>


..  Important::
    Rules to know when defining columns:

    #. All rules are evaluated for each file record. Among other things, this implies that some resource-consuming criteria (like HasPE) can impact overall performance.
    #. Last matching rule for a file determines if a column is evaluated (if "add" is used) or not (if "omit" is used). This implies that the order in which they appear matter.

    For example:

    .. code:: xml

        <columns>
            <add SizeLT="1M">SHA1</add>
            <omit ExtArchive="">SHA1</omit>
        </columns>

    The filter implies that if a file is smaller than 1 MB but has an .zip extension, then its SHA1 is not computed. However, if the order was to be reversed, its SHA1 will be computed and added to the CSV file because the last matching rule will be the add filter.


Typical Usage Examples
======================

Quick Discovery of Volume Content
---------------------------------

To quickly enumerate the file system entries of NTFS volumes attached to a system, the typical command line would be:

..  code:: bat

    DFIR-Orc.exe NTFSInfo /default /fileinfo=VolumesEntries.csv *

The equivalent XML syntax would be:

.. code:: xml

    <ntfsinfo walker="MFT">
        <fileinfo>VolumesEntries.csv</fileinfo>
        <location>*</location>
        <columns>
            <default>Default</default>
        </columns>
    </ntfsinfo>

This syntax extracts all required information from the MFT record and does not require any extra information to be pulled from the disk. This is the subset of information that can be systematically collected on systems.

Getting Detailed Information on Binaries
----------------------------------------

To obtain detailed information about binaries, based on the presence of version information and on the system drive, the typical syntax would be:

.. code:: bat

    DFIR-Orc.exe NTFSInfo /Default /+Details:HasVersionInfo /out=Details.csv %SystemDrive%\

Equivalent XML Syntax:

..  code:: xml

    <ntfsinfo walker="MFT">
        <fileinfo>Details.csv</fileinfo>
        <location>%SystemDrive%\</location>
        <columns>
            <default>Default</default>
            <add HasVersionInfo="">Details</add>
        </columns>
    </ntfsinfo>

Getting Windows PE Binaries Details
-----------------------------------

To obtain detailed information about files that contain code, based on the presence of a valid PE Header and on the system drive, and excluding computing cryptographic hashes for big files, the typical syntax would be:

..  code:: bat

    DFIR-Orc.exe NTFSInfo /Default /+Details:HasPE /+Hashes:HasPe /-Hashes:SizeGT=1MB %SystemDrive%\

Equivalent XML Syntax:

..  code:: xml

    <ntfsinfo walker="MFT">
        <fileinfo>%TEMP%\test.csv</fileinfo>
        <location>%SystemDrive%\</location>
        <columns>
            <default>Default</default>
            <add HasPE="">Hashes,Details</add>
            <omit SizeGT="1M">Hashes</omit>
        </columns>
    </ntfsinfo>
