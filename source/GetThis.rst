=======
GetThis
=======

Description
===========

GetThis was originally developed to assist with malicious sample collection but quickly evolved into a general purpose file collection tool.

GetThis is using the same MFT parser as :doc:`NTFSInfo <NTFSInfo>`, but specifically targeted to sample collection.
For details on the MFT parser used in GetThis, please refer to :doc:`MFT parser configuration for details <fs_implem_details>`.

While enumerating the specified file systems, GetThis searches for specific file indicators to collect. Once a potential sample is identified, it creates a copy of this file in the output directory (or archive). This tool also has the ability to collect information about Alternate Data Streams, Extended Attributes and "any" NTFS attribute. Various conditions and patterns can be defined to restrict the search to interesting matches. The complete search algorithm is detailed in :doc:`configuring_ntfs_opt`.


GetThis has the ability to bypass file system locks and permissions and therefore allows collection of

* in-use registry files,
* Pagefile, Hyberfil,
* event log files,
* files with restrictive ACLs,
* files opened with exclusive rights (i.e. non-shared),
* malware using file-level API hooking.

The copy is made by locating file extents (a.k.a. segments) on disk directly via the volume handle to avoid sharing violation and strict DACLs issues.

To prevent interference from anti-virus software, it is recommended to store the samples in a password-protected archive. The encryption occurs  *in memory* when the data is extracted from the disk, before any temporary file is created (i.e. clear text samples do not hit the disk). 
To use this feature, please refer to this documentation: :ref:`cfg-tool-output-pwd`.

Output
======

When collecting a sample, GetThis creates a file in the output directory (or archive) with the logic below to compute its file name:

* White space characters are replaced with underscore (_). 
* (Deprecated) In case a XOR pattern was provided, a prefix is added to the file name with *XOR_<XORPATTERN>* to be able to unXOR the sample later. 
* The file name is prefixed with the File Reference Number (a.k.a. FRN) of the **parent** of the file. This helps identifying samples from the same folder, while preserving a reasonable length for the sample names.
* One of the keywords ``data``, ``strings`` or ``raw`` is appended at the end of the sample name, depending on what is retrieved. If the resulting file name already exists in the output directory, the suffix ``_1_data`` is added (and then  ``_2_data`` and so on).

For example, when the full-path name of a sample is ``C:\Windows\System32\kernel32.dll``, the collected sample is named: ``0000000000000026_kernel32.dll_data`` (where 0000000000000026 is the FRN for ``C:\windows\system32``).
The same sample collected with the deprecated XOR pattern ``0x0BADF00D`` is named ``XOR_0BADFOOD_0000000000000026_kernel32.dll_data``.

Along with the sample, GetThis collects information about the location of a matching NTFS record, the file it describes and hashes to help identify the collected content. To fully grasp the NTFS attributes collected and represented in the columns in cases more complicated than files, please refer to :doc:`configuring_ntfs_opt`.

This information is, by default, stored in a CSV file named ``GetThis.csv``, which is organized as follows:

.. csv-table::
    :header: ColumnName, Description
    :align: left
    :widths: auto

    ComputerName, Name of the computer
    VolumeID, Id of the volume
    ParentFRN, FRN of the parent directory
    FRN, FRN of this entry
    FullName, Full path name for this entry
    SampleName, Name of the corresponding sample
    SizeInBytes, File size in bytes
    MD5, Cryptographic MD5 hash
    SHA1, Cryptographic SHA1 hash
    FindMatch, The content of the ntfs_find conditions (or /sample command line option) which were satisfied for the element to be collected
    ContentType, Type can be ``data`` or ``raw`` or ``strings``.
    CreationDate, File creation date (yyyy-MM-dd hh:mm:ss.SSS)
    LastModificationDate, File last write date (yyyy-MM-dd hh:mm:ss.SSS)
    LastAccessDate, File last read access date (yyyy-MM-dd hh:mm:ss.SSS)
    LastAttrChangeDate, File last attribute change date (yyyy-MM-dd hh:mm:ss.SSS)
    FileNameCreationDate, File name (hard link) creation date (yyyy-MM-dd hh:mm:ss.SSS)
    FileNameLastModificationDate, File name (hard link) last modification date (yyyy-MM-dd hh:mm:ss.SSS)
    FileNameLastAccessDate, File name (hard link) last read access date (yyyy-MM-dd hh:mm:ss.SSS)
    FileNameLastAttrModificationDate, File name (hard link) last attribute change date (yyyy-MM-dd hh:mm:ss.SSS)
    AttrType, Type of the collected NTFS attribute 
    AttrName, Name of the collected NTFS attribute
    AttrID, ID of the collected NTFS attribute
    SnapshotID, Snapshot associated with this entry
    SHA256, Cryptographic SHA256 hash
    SSDeep, Fuzzy hash SSDeep
    YaraRules, List of the yara rules matching with the sample


An output for logging purposes can be used with the syntax found in :doc:`Configuring Console Output <configuring_console_output>`.

Usage
=====

GetThis can be used in two mutually exclusive manners, etiher with command-line parameters or with an XML configuration file.
The XML syntax is to be preferred as it provides a better access to GetThis functionalities, especially the limit settings and yara rules.

A typical command-line parameter syntax looks like the following:

.. code:: bat

    DFIR-Orc.exe GetThis /sample=git.exe /out=git.7z "C:\Program Files\git\bin" /nolimits

.. _getthis-xml-example:

A typical XML configuration file looks like the following:

.. code:: xml

    <getthis>
        <location>%SystemDrive%\</location>
        <yara block="20M" overlap="2M" timeout="20" source="GetThisSample.yara" />
        <samples MaxPerSampleBytes="50MB" MaxSampleCount="15000" MaxTotalBytes="1024MB" >
            <sample name="git" MaxPerSampleBytes="50MB" MaxSampleCount="150" MaxTotalBytes="150MB">
                <ntfs_find path="\Program Files\git\bin\git.exe" />
            </sample>
            <sample name="WSTCODEC" MaxPerSampleBytes="50MB" MaxSampleCount="150" MaxTotalBytes="150MB">
                <ntfs_find path="\Windows\System32\DRIVERS\WSTCODEC.SYS" />
            </sample>
            <sample name="notdll" MaxPerSampleBytes="80MB">
                <ntfs_find name_match="\*.dll"  yara_rule="is_not_dll" />
            </sample>
        </samples>
    </getthis>

In this example, all samples collected using the ``<ntfs_find path="\Program Files\Git\bin\git.exe" />`` indicator will be added to a 7zip folder named "git", modulo the restrictions set in the attributes, which are documented below. 

The XML configuration file is supplied to GetThis with the ``/config`` option:

.. code:: bat

    DFIR-Orc.exe GetThis /config=<TypicalConfig>.xml



``getthis`` Element
-------------------

*optional=no, default=N/A*

Root element.

Attributes
``````````

* **nolimits** *(optional=yes, default=Inactive)*, ``/nolimits`` option:
    Specifies that there should be no limit when collecting the samples. The option ``/nolimits`` takes no value. In an XML file, the attribute is written ``nolimits=""``. 

.. warning::
    Limits must be explicitly set, either by using ``nolimits`` or by using a meaningful combination of attributes of ``samples``. Details are provided :ref:`below <getthis-limits>`.

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

* **reportall** *(optional=yes, default=Inactive)*, ``/reportall`` option:
    When using limits, GetThis potentially does not collect files that would have been collected otherwise. Nevertheless, the ``reportall`` option can be added so that the output CSV file contains information about all matching data from the disk, and not just the collected ones. When using the command line, this switch can be activated with the option ``/reportall``, which takes no value. In an XML file, the attribute is written ``reportall=""``.
* **flushregistry** *(optional=yes, default=Inactive)*, ``/flushregistry`` option:
    GetThis is collecting data as it lies on the disk. If the file is **currently being written** or if part of the "current" state of the data is present in an application or in NTFS cache structures, then the collected data may be incorrect, incomplete or appear corrupted. GetThis is **not** an appropriate tool to collect volatile information with high fidelity. You *must* expect that collection of pagefiles, registry hives, etc., can lead to corrupt or incomplete files. When using this attribute, GetThis calls ``RegFlushKey`` for both ``HKEY_USERS`` and ``HKEY_LOCAL_MACHINE`` and can help retrieve more reliable hives. In an XML file, use ``flushregistry=""``.
* **hash** *(optional=yes, default="MD5,SHA1")*, ``/hash="<Hash1,...>"`` option:
   Comma-separated list of hashes to compute for the collected samples. MD5 and SHA1 cannot be suppressed.  There is only one other possible hash algorithm for the time being: SHA256.

* **fuzzyhash** *(optional=yes, default=None)*, ``/fuzzyhash="<FHash1,...>"`` option:
    Comma-separated list of fuzzy hashes to compute for the collected samples. Possible values is SSDeep.

.. important::

    The ``hash`` and ``fuzzyhash`` options are ignored when using ``/XOR``.

``output`` Element, ``/out=<Path>`` Option
------------------------------------------

*optional=yes, default=.\\GetThis.7z*

This element can also be specified from the command line. For details on the ``output`` element syntax, please refer to the :doc:`output documentation <configuring_tool_output>`.

A XOR pattern can be provided to be applied to the collected sample (whether it is in a folder or in an archive), the syntax is the following:

* XML element:

.. code:: xml

    <output XOR="0x0BADF00D">
        PathToDirOrArchive
    </output> 

* Command-line option:

.. code:: bat

    /out=PathToDirOrArchive /XOR=0x0BADF00D

.. note::

    The ``/XOR`` option is **DEPRECATED**. To prevent interference from anti-viruses, one should use a password-protected archive.
    
``location`` Element
--------------------

*optional=no, default=N/A*

Selectively collect samples in specific folders inside volumes. For this purpose, one can use any syntax described in :doc:`Configuring Locations <configuring_locations>`.

When using the command line, this element must be provided as a comma-separated list, as an argument at the end of the command:

.. code:: bat

    DFIR-Orc.exe GetThis /sample=git.exe /out=git.7z <Location1>, <Location2>

``yara`` Element or ``/yara=<Path>`` Option
--------------------------------------------

*optional=yes, default=N/A*

Used to specify yara rules. Please refer to :doc:`configuring_yara` for details on the ``yara`` element.
The option should indicate the path to a file containing yara rules. 


``samples`` Element
-------------------

*optional=no, default=N/A*

Describes the samples to collect.

Attributes
``````````

.. _getthis-limits:

Specifying Limits
*****************

To help control the amount of data collected, GetThis requires limits to be specified to the number and size of samples that can be collected.
Those can be specified using three attributes:

* **MaxSampleCount** *(optional=yes, default=N/A)*, ``/MaxSampleCount="<Integer>"`` Option:
    Maximum number of matching files to be collected. This value is an integer.

* **MaxPerSampleBytes** *(optional=yes, default=N/A)*, ``/MaxPerSampleBytes="<Integer>"`` Option:
    Collects matching files smaller than the specified size. The expected value is an integer that can be followed by one of these units: *B, KB, MB, GB*.

* **MaxTotalBytes** *(optional=yes, default=N/A)*, ``/MaxTotalBytes="<Integer>"`` Option:
    Matching files are collected until their uncompressed cumulated file size reaches the specified value. The expected value is an integer that can be followed by one of these units: *B, KB, MB, GB*.

Limits can be set globally on the ``samples`` element or locally on the ``sample`` element, documented below. When limits are evaluated, the closest attributes are taken into account first, and then the more general ones. If any criterion is not met, then the sample is not collected; otherwise, the sample is collected, and all the evaluated attributes take it into account for future restrictions.  

.. important:: The tool does not run unless limits are explicitly waived (using ``nolimits``) or a combination of the ``samples`` attributes that determine the maximum size of the collection.

.. code:: xml

    <samples MaxPerSampleBytes="500MB" MaxSampleCount="150" >

        <sample name="git" MaxPerSampleBytes="50MB" >
            <ntfs_find path="\Program Files\Git\bin\git.exe" />
        </sample>

        <sample name="WSTCODEC" MaxSampleCount="15" >
            <ntfs_find path="\Windows\System32\DRIVERS\WSTCODEC.SYS" />
        </sample>
    
    </samples>

In this example, GetThis does not collect more than 150 files, but stops collecting the *WSTCODEC* group when 15 of them are found.
Additionally, a single match in the *git* group cannot be larger than 50 MB and no single file bigger than 500 MB is collected.

When examining :ref:`the XML file example at the top of this section <getthis-xml-example>`, one can notice that

   * the restriction imposed on the size of an individual sample is bound to 80 MB by the last ``sample`` element and 50 MB by the global ``samples`` element. This still bounds any sample to 50 MB. 
   * every time a sample is collected for the first ``sample`` element, its size is added to the total number of bytes collected for in the context of this ``sample`` element, but is also added to the number of bytes collected in the context of the global ``samples`` element.


Retrieved Content: the Content Attribute
****************************************

The ``content`` attribute allows to define an algorithm to retrieve the data to be collected.

In more details, GetThis relies on the MFT parser to find NTFS attributes matching constraints defined by ``ntfs_find`` and ``ntfs_exclude`` elements. The default data getting collected from a matching NTFS attribute is specified in :doc:`configuring_ntfs_opt`. The ``content`` attribute can be used to influence the way in which the collection of this data is realized. However, it does not influence which NTFS attribute is being collected: the ``content`` requirement is applied to alternate data streams and extended attributes in the same way as it is applied to the default ``$DATA`` stream of files.

.. csv-table::
    :header: Value, Description
    :align: left
    :widths: auto
    :delim: ;

    data; (Default value) Collects the data for the attribute
    strings; Collects only the strings (ASCII & Unicode) with min and max ranges. It is possible to specify a minimum and maximum length with the syntax ``content="strings:min=<Int>,max=<Int>"``. By default, the minimum is set to 3 and the maximum to 1024.
    raw; Collects the data "as is" from the disk (i.e. compressed if data is NTFS compressed)

The syntax is as follows:

.. code:: xml

    <samples content="data" >
        <sample name="git" content="strings" >
            <ntfs_find path="\Program Files\Git\bin\git.exe" />
        </sample>
        <sample name="WSTCODEC" content="strings:min=5,max=512" >
            <ntfs_find path="\Windows\System32\DRIVERS\WSTCODEC.SYS" />
        </sample>
    </samples>


For the first element, strings of the samples get collected, with the default parameters.
The output does not contain any formatting, just one line per string found. Empty lines represent buffers with no valid strings found.
The second element results in the collection of the strings of at least 5 and at most 512 ASCII/Unicode characters of matching samples.

.. important:: The output is UTF-8 encoded.

Depending on the content specified, the retrieved samples are suffixed as follows:

* **_data** for the complete data of the attribute,
* **_strings** when only strings are copied,
* **_raw** when raw data is collected.

When using the command line, this switch can be activated with the option ``/content``.


``ntfs_exclude`` Element
------------------------

*optional=yes, default=N/A*

This element allows to exclude NTFS attributes **from all the searches configured in the XML file**. 
The complete specification of the search algorithm and the syntax to use are detailed in :doc:`configuring_ntfs_opt`. 
While the most classical use of this element is path-related, a lot more precise NTFS constraints can be configured.

.. warning:: The scope of an ``ntfs_exclude`` element is the whole configuration file.

``sample`` Element, ``/sample=<FileName>`` Option
--------------------------------------------------

*optional=no, default=N/A*

This element regroups ``ntfs_find`` elements.

This element can have the same attributes as ``samples``: ``MaxSampleCount``, ``MaxPerSampleBytes``, ``MaxTotalBytes`` and ``content``.
Within a given ``sample`` element, the same restrictions apply.

The samples matching this group can be stored in a single folder inside the output archive (or folder). 
The folder name is specified using the ``name`` attribute. This can be leveraged during triage.

When used as an option on the command line, the supported values are:

* **/sample=<FileName.txt>** for to look for a file named FileName.txt,
* **/sample=<FileName.txt:AnADS>** for to look for a file named FileName.txt that has a $DATA attribute named "AnADS" (aka Alternate Data Stream) , and
* **/sample=<FileName.txt#AnEA>** for to look for a file named FileName.txt that has a $EA attribute (a.k.a Extended Attribute) with a value called "AnEA".

.. warning:: When using the **option**, a **file name**, rather than a file path, is required.

``ntfs_find`` Element
---------------------

*optional=no, default=N/A*

It is this element which specifies a set of rules to identify the NTFS attributes to be collected. 
The complete specification of the search algorithm and the syntax to use are detailed in :doc:`configuring_ntfs_opt`. 
While the most classical use of this element is path-related, it is possible to search for alternate data streams, extended attributes, streams with specific hashes, etc. 


Additional Command-line Usage
-----------------------------

.. important::

    The ``/extract`` option is **DEPRECATED**. It is documented for the sake of completeness.

GetThis supports cabinet extraction with support for XOR pattern recognition.

Syntax is:

* Output file specification: ``/extract=PathToCab.7z``
* Output Directory: ``/out=c:\temp``

The typical extraction syntax is:

.. code:: bat

    DFIR-Orc.exe GetThis /extract=c:\Data\Samples.cab /out=c:\temp

.. note:: There is no need to specify a XOR pattern. If the content is XORed by GetThis, names are prefixed by ``XOR_XORPATTERN``. In this case, the ``XOR_PATTERN`` is used to XOR file content before being written to output directory.


Typical Usage Examples
======================

Samples with Wildcards
----------------------

The typical command line to collect all samples matching "ker*.dll" on the system drive would be:

.. code:: bat

    DFIR-Orc.exe GetThis /nolimits /sample=ker*.dll /out=%TEMP% %SystemDrive%\

Equivalent XML Syntax:

.. code:: xml

    <getthis nolimits="">

        <output>%TEMP%</output>

        <location>%SystemDrive%\</location>

        <samples>
            <sample>
                <ntfs_find name_match="ker*.dll" />
            </sample>
        </samples>

    </getthis>

Samples from an Alternate Data Stream
-------------------------------------

The typical command line to collect all samples, residing in an **Alternate Data Stream** named ``calc.exe`` in any file of the file system is:

.. code:: bat

    DFIR-Orc.exe GetThis /nolimits /sample=*:calc.exe /out=%TEMP% %SystemDrive%\

Equivalent XML Syntax:

.. code:: xml

    <getthis nolimits="" >

        <output>%TEMP%</output>

        <location>%SystemDrive%\</location>
        
        <samples>
            <sample name="calc" >
                <ntfs_find ads="calc.exe" />
            </sample>
        </samples>

    </getthis>


The syntax for *Alternate Data Stream* sample collection is typically:

.. code:: bat

    DFIR-Orc.exe GetThis /sample=HostFileName.txt:Malware*.exe

In this example, GetThis looks for any **ADS** matching Malware*.exe in a record named ``HostFileName.txt``.

Samples from an Extended Attribute
----------------------------------

The syntax for **Extended Attribute** sample collection is typically:

.. code:: bat
    
    DFIR-Orc.exe GetThis /sample=HostFileName.txt#Malware*.exe

Equivalent XML Syntax:

.. code:: xml

    <getthis nolimits="" >

        <output>%TEMP%</output>

        <location>%SystemDrive%\temp</location>
        
        <samples>
            <sample name="Malware" >
                <ntfs_find name="HostFileName.txt" ea_match="Malware*.exe" />
            </sample>
        </samples>

    </getthis>


In this example, GetThis looks for any extended attribute matching Malware*.exe in a record named ``HostFileName.txt``.
