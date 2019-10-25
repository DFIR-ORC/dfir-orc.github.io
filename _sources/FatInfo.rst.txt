=======
FatInfo
=======

Description
===========

FatInfo is intended to collect details on data stored on FAT mounted volumes and raw disk images.
Basically, the tool enumerates the file system entries and outputs user-chosen details to collect in one or more CSV files.

Output
======

FatInfo can output data into a CSV file, a folder or an archive. When provided with a folder or an archive, it creates one file per FAT volume instead of a unique file, and creates a file named volstats.csv in the output archive or directory.

Each CSV file contains the following information on files and folders present on the FAT system:

* **Volume Identification:**
    * **ComputerName:** Name of the computer
    * **VolumeID:** Id of the volume
* **Standard Information:**
    * **File:** Name of the file
    * **ParentName:** Name of the parent folder
    * **FullName:** Full-path name
    * **Extension:** Optional file name extension (split path)
    * **Attributes:** FAT file system attributes
    * **SizeInBytes:** File size in bytes
* **Date Information:**
    * **CreationDate:** File creation date *"mm/dd/yyyy hh\:mm\:ss.000"*
    * **LastModificationDate:** File last write date *"mm/dd/yyyy hh\:mm\:ss.000"*
    * **LastAccessDate:** File last read access date
* **RecordInUse:** Boolean which indicates if this record was in use or free (i.e. deleted)
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
        * **SignedNotVerified:** File signature does **not** verify
        * **NotSigned:** No signature or catalog could be found for this file
    * **AuthenticodeSigner:** Signer's certificate (value of the first occurrence of the attributes szOID_COMMON_NAME, szOID_ORGANIZATIONAL_UNIT_NAME, szOID_ORGANIZATION_NAME, or szOID_RSA_emailAddr)
    * **AuthenticodeSignerThumbprint:** Signer's certificate hash
    * **AuthenticodeCA:** Signer's root CA certificate (value of the first occurrence of the attributes szOID_COMMON_NAME, szOID_ORGANIZATIONAL_UNIT_NAME, szOID_ORGANIZATION_NAME, or szOID_RSA_emailAddr)
    * **AuthenticodeCAThumbprint:** Signer's root CA certificate hash
    * **SecurityDirectory:** Base64 encoded security directory of the PE file (if present)
* **Version Information:**
    * **FileOS:** VersionInfo OS tag
    * **FileType:** VersionInfo type
    * **Version:** VersionInfo file version
    * **CompanyName:** VersionInfo company name
    * **ProductName:** VersionInfo product name
    * **OriginalFileName:** VersionInfo original file name
* **PE Header Related Information:**
    * **Platform:** PE Header platform
    * **TimeStamp:** PE Header timestamp
    * **SubSystem:** PE Header SubSystem
* **FirstBytes:** First 16 bytes (in hex) of the file content.

An output for logging purposes can be used with the syntax found in :doc:`Configuring Console Output <configuring_console_output>`.

Usage
=====

FatInfo can be used from command line or with an XML configuration file. Both provide (mostly) identical access to FatInfo functionality even if the configuration files allow for more complexity.

* Example of command-line parameters:
    This syntax is intended for simple user-friendly usage.

.. code:: bat

    DFIR-Orc.exe FatInfo F: /out=c:\TEMP\FAT.csv /logfile=c:\TEMP\FatInfo.log /Dates,File,ParentName,SizeInBytes

* Example of XML configuration file: 
    XML configuration files can be easier for detailed and more complex usage of FatInfo.

.. code:: xml

    <fatinfo>

        <output>c:\TEMP\CompleteUSN.csv</output>

        <logging file="c:\TEMP\FatInfo.log" />

        <location>F:\</location>

        <columns>
            <default>Dates</default>
            <default>File</default>
            <default>ParentName</default>
            <default>SizeInBytes</default>
        </columns>

    </fatinfo>

The XML configuration file is provided by using the parameter ``/config``:

.. code:: bat
 
    DFIR-Orc.exe FatInfo /config=c:\TEMP\FatInfoConfig.xml

.. note::

    All output-related parameters (in the configuration file and in the command line) can use environment variables.


``fatinfo`` Element
-------------------

*optional=no, default=N/A*

Root element.

Attributes
``````````

* **resurrect** *(optional=yes, default="true")*, ``/ResurrectRecords`` option:
    Configures the parser to include deleted records. This can, by design, yield unpredictable results (as we are using unreliable or partially deleted information). One can generally assume that resident attributes for those entries are valid, unlike non-resident attributes that are most likely quickly invalidated after the entry deletion. Deactivating this feature in XML can be done by writing ``resurrect="no"``. 

* **computer** *(optional=yes, default="Name of the machine on which the tool runs")*, ``/Computer=<ComputerName>`` option:
    Substitutes the content of the ComputerName column with a provided string.

* **popsysobj** *(optional=yes, default=False)*, ``/PopSysObj``:
    Probes available system objects and looks for hidden FAT filesystem. This can lead to unexpected behavior.


``output`` Element, ``/out=<Path>`` Option
------------------------------------------

*optional=yes, default=FatInfo.csv*

For details on the ``output`` element syntax, please refer to the :doc:`output documentation <configuring_tool_output>`.

``location`` Element
--------------------

*optional=no, default=N/A*

Specifies the parsed system. For details on the syntax, please refer to the :doc:`configuring locations documentation<configuring_locations>`.

When using the command line, this element must be provided in the form of a comma-separated list, as an argument at the end of the command:

.. code:: bat

    DFIR-Orc.exe FatInfo <Location1>,<Location2>
    
``columns`` Element, ``/<Column1>,...`` Option
----------------------------------------------

*optional=yes, default=Default (Alias defined below)*

Information to collect in the output. Column selection is specified using a comma-separated list of included columns.

The following examples output the file name, its parent full-path, and its MD5 hash:

* Command-line parameter:

    .. code:: bat

        /File,ParentName,MD5

* XML elements:

    .. code:: xml

        <columns>
            <default>File,ParentName,MD5</default>
        </columns>

More than one column selection can be specified, for example:

.. code:: bat

    /File,ParentName,SizeInBytes /SHA1,MD5

Or in XML form:

.. code:: xml

    <columns>
        <default>File,ParentName,SizeInBytes</default>
        <default>SHA1,MD5</default>
    </columns>

This allows groups of columns to be specified in a more convenient way.

Aliases for a set of related columns can be used, to simplify the syntax.

For instance, using the alias "Default" adds the following columns in the output CSV file:

    * File, ParentName,
    * Extension, Attributes, SizeInBytes,
    * CreationDate, LastModificationDate, LastAccessDate, and
    * RecordInUse

As an example, the following configuration yields all the columns regrouped under the alias, and MD5.

.. code:: xml 
        
    <columns>
        <default>Default</default>
        <default>MD5</default>
    </columns>
 

.. note::

    The command ``DFIR-Orc.exe FatInfo /?`` will print all column definitions along with the definition of aliases.

``add`` or ``omit`` Element, ``/(+|-)<ColumnSelection>:criteria=<value>`` Option
--------------------------------------------------------------------------------

*optional=yes, default=N/A*

FatInfo allows to selectively add or remove column content, depending on whether a specific criterion is met for a file. This can help reduce resource consumption for some columns (e.g. MD5, AuthenticodeStatus).

The available criteria for FatInfo column filters are

* **HasVersionInfo:** if file has a VERSION_INFO resource
* **HasPE:** if file has a valid PE header
* **ExtBinary:** if file has an executable extension (like .exe, .dll, .scr, .sys, …)
* **ExtArchive:** if the file has a archive extension (like .zip, .cab, …)
* **Ext=.Ext1,.Ext2,...:** if file has extension in .Ext1,.Ext2,...
* **SizeLT=<Size>, SizeGT=<Size>:** if file is smaller or bigger than a specified size. Note that size can be expressed in KB (i.e. SizeGT=25K...) or in MB (i.e. SizeLT=5M etc...).

A filter is typically defined by three elements:

#. Add or omit
#. Criteria
#. Affected Column

Example 1:

.. code:: bat

    /+SHA1:SizeLT=1M

This only computes a value put in the column SHA1 if the file size is smaller than 1 MB.

Equivalent XML syntax:

.. code:: xml

    <columns>
        <add SizeLT="1M">SHA1</add>
    </columns>

Example 2:

.. code:: bat

    /-MD5:ExtArchive

This does not compute MD5 if the file has an archive extension (.cab, .zip).

Equivalent XML syntax:

.. code:: xml

    <columns>
        <omit ExtArchive="">MD5</omit>
    </columns>

.. important:: 

    It is important to note that the following rules are applied when defining columns:

    #. All rules are evaluated for each file record. Among other things, this implies that some resource-consuming criteria (like HasPE) can impact the overall performance.
    #. The last rule to match for a file determines if a column is evaluated (when "add" is used) or not (when "omit" is used). This implies that the order in which they appear matters.


For example, the following filters

.. code:: xml

    <columns>
        <add SizeLT="1M">SHA1</add>
        <omit ExtArchive="">SHA1</omit>
    </columns>

imply that if a file is smaller than 1MB but has an .zip extension, then its SHA1 is not computed. However, if the order was to be reversed, its SHA1 would be computed and added to the CSV file, since the last matching rule would be the ``add`` filter.



Typical Usage Examples
======================

Quick Discovery of Volume Content
---------------------------------

To quickly enumerate the file system entries of FAT volumes attached to a system, the typical command line would be

.. code:: bat

    DFIR-Orc.exe FatInfo /default /out=VolumeEntries.csv *

The equivalent XML syntax would be

.. code:: xml

    <fatinfo>

        <output>VolumeEntries.csv</output>

        <location>*</location>

        <columns>
            <default>Default</default>
        </columns>
    </fatinfo>

This syntax extracts all required information from the FAT records and does not require any extra information to be pulled from the disk. This is the subset of information that can be systematically collected on systems.

Getting Detailed Information on Binaries
----------------------------------------

To obtain detailed information about binaries, based on the presence of version information, the typical syntax would be

.. code:: bat

    DFIR-Orc.exe FatInfo /Default /+Details:HasVersionInfo /out=Details.csv F:

Equivalent XML Syntax:

.. code:: xml

    <fatinfo walker="MFT">

        <output>Details.csv</output>

        <location>F:\</location>

        <columns>
            <default>Default</default>
            <add HasVersionInfo=""></add>
        </columns>
    </fatinfo>

Getting Windows PE Binaries Details
-----------------------------------

To obtain detailed information about files that contain code, based on the presence of a valid PE Header, and excluding computing cryptographic hashes for big files, the typical syntax would be

.. code:: bat

    DFIR-Orc.exe FatInfo /Default /+Hashes,Details:HasPE /-Hashes:SizeGT=1MB F:

Equivalent XML Syntax:

.. code:: xml

    <fatinfo walker="MFT">
        <output>%TEMP%\test.csv</output>

        <location>F:\</location>

        <columns>
            <default>Default</default>
            <add HasPE="">Hashes,Details</add>
            <omit SizeGT="1M">Hashes</omit>
        </columns>
    </fatinfo>



