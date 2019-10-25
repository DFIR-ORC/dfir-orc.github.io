=====================================================================
Configuring Attributes of ``ntfs_find`` and ``ntfs_exclude`` Elements
=====================================================================


Search Algorithm and Result of a Search
=======================================

FastFind, RegInfo and GetThis can select NTFS file system entries based on multiple indicators to allow the precise definition of wanted items. Those indicators are specified by using two elements:

* ``ntfs_find`` to search for an indicator,
* ``ntfs_exclude`` to reject a match.

The search is conducted as follows. Each ``ntfs_find`` element yields a (possibly combined) search clause, and the global search is conducted for records matching at least one clause.
Then, amongst matching records, those verifying any of the exclusion clauses yield by ``ntfs_exclude`` elements are eliminated.

When using several ``ntfs_find`` elements, a match is found if the artefact matches one of the elements. For instance

.. code:: xml

    <ntfs_find name="qfe.dat" />
    <ntfs_find size="104857600" />
    
indicates files should either be named "qfe.dat" **OR** their size should be 104857600 bytes to trigger a detection.

When using several ``ntfs_exclude`` elements, a match is discarded if the artefact matches one of the elements. For instance

.. code:: xml

    <ntfs_exclude name="qfe.dat" />
    <ntfs_exclude size="104857600" />
    
indicates files are rejected if they are either named "qfe.dat" **OR** their size is 104857600 bytes.

Within an element ``ntfs_find`` or ``ntfs_exclude``, attributes of different classes can be combined to specify an "AND" condition. This combined condition is evaluated on MFT records.
For instance

.. code:: xml

    <ntfs_find name="qfe.dat" size="104857600" />

indicates files should be named "qfe.dat" **AND** their size should be 104857600 bytes to trigger a detection. Furthermore

.. code:: xml

    <ntfs_exclude name="qfe.dat" size="104857600" />
    
indicates files are rejected if they are named "qfe.dat" **AND** their size is 104857600 bytes.

For every record matching a clause, each NTFS attribute involved in a match is registered. Indeed, conditions can be imposed on various types of record features, such as ``$DATA`` streams and extended attributes.
For instance, if a match is on an ADS name, only the ``$DATA`` corresponding to this ADS is registered and not the other record attributes.

The search eventually results in the set of registered NTFS artefacts which are not eliminated by any ``ntfs_exclude`` element.

.. warning:: The search algorithm defined above does not depend on the place of the ``ntfs_find`` and ``ntfs_exclude`` elements within an XML file; in particular, a ``ntfs_exclude`` element **does impact** all artefacts to be collected by an XML configuration file, independently of its position with respect to other elements. Therefore, an ``ntfs_exclude`` element should alwys be placed at the utmost level to emphasize their scope. Typically, in GetThis, ``ntfs_exclude`` elements should be placed under the ``<samples>`` element.

How the resulting set of NTFS artefacts is used depends on the tool using ``ntfs_find`` and ``ntfs_exclude``.
In general, only the NTFS attributes used for a record match are reported/collected. The only exception is that the resulting set must have at least a name and data. If a name is missing, the tool will use the first ``$FILE_NAME`` attribute. If a data is missing, the default (unnamed) ``$DATA`` is used.
For instance, for GetThis, if the only condition used is on the file name, the resulting set will have a name but no data so the tool will also retrieve the default ``$DATA`` (the file contents). This is detailed below.

Possible Attributes of a ``ntfs_find`` Element
===============================================

The list below enumerates the attributes that can be used to describe search indicators. The conditions are tested against MFT records. When an NTFS artefact matches a condition, it is registered. The whole MFT record has to match all conditions expressed in the scope of one element.

.. note:: ``*_regex`` elements should use the ECMA-script syntax. 

The conditions listed below are matched against each ``$FILE_NAME`` attribute.
The artefact registered is the ``$FILE_NAME`` attribute matching the condition.

* ``name``
    The file name coincides with the supplied string.
    ::

        name="qfe.dat"

* ``name_match``
    The file name matches the supplied expression.
    ::

        name_match="q*.dat"

* ``name_regex``
    The file name matches the regular expression.
    ::

        name_regex="q.*\.dat"

* ``path``
    The full path of the file coincides with the supplied string.
    ::

        path="\Windows\System32\drivers\mgr.sys"

* ``path_match``
    The full path of the file matches the supplied string.
    ::

        path_match="\Windows\System32\*\mgr.s?s"

* ``path_regex``
    The full path of the file matches the regular expression.
    ::

        path_regex="\\Windows\\System32\\.*\\mgr\.s.s"

The conditions listed below are matched against each ``$DATA`` attribute.
The artefact registered is the ``$DATA`` attribute matching the condition.

* ``size``
    The size of the file equals the supplied integer.
    Multipliers can be used:
    
    * 1K for 1024 bytes,
    * 1M for 1024 kilobytes,
    * 1G for 1024 megabytes.

    ::

        size="5M"

* ``size_gt``
    The size of the file is greater than the supplied integer.

    ::

        size_gt="5M"

* ``size_ge``
    The size of the file is greater than or equal to the supplied integer.

    ::

        size_ge="5M"

* ``size_lt``
    The size of the file is less than the supplied integer.

    ::

        size_lt="5M"

* ``size_le``
    The size of the file is less than or equal to the supplied integer.

    ::

        size_le="5M"

* ``ads``
    The name of an ADS coincides with the supplied string.

    ::

        ads="MyAds"

* ``ads_match``
    The file has an ADS which matches the supplied string.

    ::

        ads_match="My?ds"

* ``ads_regex``
    The file has an ADS which matches the regular expression specified.

    ::

       ads_regex="My.ds"
       ea_regex="My.A"

The conditions listed below are matched against each ``$DATA`` attribute actually stored data.
The artefact registered is the ``$DATA`` attribute matching the condition.
        
* ``md5``
    The MD5 hash of a data stream is the supplied value.

    ::

        md5="b092e1d683fc21cea137dba2a8b4b08b"

* ``sha1``
    The SHA1 hash of a data stream is the supplied value.

    ::

        sha1="be0ccf54cdb3ec100de233b393d936d2ee1c33a3"

* ``sha256``
    The SHA256 hash of a data stream is the supplied value.

    ::

        sha256="4cdb3ec100de233b393d936d2ee1c33a3..."

* ``header``
    The header of a data stream coincides with the supplied string (ANSI encoding). Up to 128 bytes can be specified.

    ::

        header="MZ"

* ``header_hex``
    The header of a data stream coincides with the supplied bytes, written in hexadecimal.
    "0x" prefix can be used and is optional. Up to 128 bytes can be specified.

    ::

        header_hex="ccf54cdb"

* ``header_regex``
    The header of a data stream matches the regular expression, against ``header_length`` bytes from the file.
    The value has to be at least that of the minimal string matching the expression, or no hits 
    are found. For example, ``header_regex="MZ" header_len="1"`` does not match any file.    
    ::

        header_regex="M[X-Y]"

* ``header_length``
    This attribute has to be used along ``header_regex``.
    It specifies the length of the header to read to make the comparison (in bytes).     
    ::

        header_length="1024"


* ``contains``
    A data stream contains the specified string (written in ASCII and case-sensitive).

    ::

        contains="Hello World"

* ``contains_hex``
    A data stream contains a specific binary array.

    ::

        contains_hex="0x0BADF00DBAADF000D"

* ``yara_rule``
    A data stream verifies one rule amongst a comma or semicolon separated list of yara rules.
    The rule specification may use "*" or "?" to match arbitrary characters.

    ::

        yara_rule="is_dll;apt??_rat"



The conditions listed below are matched against each attribute in the MFT record.
The artefact registered is the attribute matching the condition.
        
* ``attr_name``
    The name of an attribute coincides with the supplied string

    ::

        attr_name="$I30"

* ``attr_match``
    Attribute name matches the supplied string

    ::

        attr_match="?I30"

* ``attr_regex``
    Attribute name matches the regular expression

    ::

        attr_regex=".I30"

* ``attr_type``
    Attribute type is one of:

    * $STANDARD_INFORMATION
    * $ATTRIBUTE_LIST
    * $FILE_NAME
    * $OBJECT_ID
    * $SECURITY_DESCRIPTOR
    * $VOLUME_NAME
    * $VOLUME_INFORMATION
    * $DATA
    * $INDEX_ROOT
    * $INDEX_ALLOCATION
    * $BITMAP
    * $REPARSE_POINT
    * $EA_INFORMATION
    * $EA
    * $LOGGED_UTILITY_STREAM
    * $FIRST_USER_DEFINED_ATTRIBUTE
    * $END
    * Or a custom integer value.

    ::

        attr_type="$STANDARD_INFORMATION"
        attr_type="16"

For the conditions listed below, the artefact registered is the content of any extended attribute (``$EA``) associated to the record - that is to say, pairs of names and values.
        
* ``ea``
    The name associated to a value in an extended attribute of the file coincides with the supplied string.

    ::

        ea="MyEA"

* ``ea_match``
    The name associated to a value of an extended attribute of the file matches the supplied string.

    ::

        ea_match="My?A"

* ``ea_regex``
    The name associated to a value of an extended attribute of the file matches the regular expression.

    ::

        ea_regex="My.*"

.. important:: At the end of the evaluation of a clause, when a record matches, the artefacts justifying the match have been registered. This artefact list can be completed with other elements:

    * If there was no condition on the record name, there is no name amongst the artefacts registered. However, a name is needed to refer to the other artefacts registered (e.g. for GetThis). In this case, the name is chosen to be the first non-short file name listed in the record. 
    * If there was no condition on data streams or attributes, namely, if only file names are constrained, there is no registered artefact with actual content. In this case, the default ``$DATA`` stream of the record is added to the list when it exists. This allows GetThis to collect it.

Possible Attributes of a ``ntfs_exclude`` Element
==================================================

``ntfs_exclude`` elements can be used to exclude specific matches.
As explained in `the first section of this page <#search-algorithm-and-result-of-a-search>`_, 
when a record matches all attributes of an exclusion term, all NTFS artefacts related to this record are excluded from the matching set.

All ntfs_find attributes are supported by ntfs_exclude **except** extended attributes related ones (ea, ea_match, ea_regex).

.. warning:: As previously explained, the search algorithm defined above does not depend on the placement of the ``ntfs_find`` and ``ntfs_exclude`` elements; in particular, an ``ntfs_exclude`` element **does impact** all artefacts to be collected, independently of its position with respect to other elements.


Order of Evaluation of Attributes in Clauses
============================================

.. important:: Attributes evaluation order is based on cost. For instance, size is a very cheap indicator to evaluate whereas hash value is very expensive. If both are present, the evaluator will first test file size and then (if size matches) will evaluate the file's hash value. **This means that coupling a size indicator to a hash one will dramatically enhance the performance of the search**.

The evaluation order is as follows:

    * File Name:
    
        * name
        * name_match
        * name_regex

    * Path:

        * path
        * path_match
        * path_regex

    * $DATA name or size:

        * ads
        * ads_match
        * ads_regex
        * size
        * size_eq
        * size_gt
        * size_ge
        * size_lt
        * size_le

    * Verify if any of the record names are in the selected location (i.e. one of the specified directories in locations)

    * Attribute:

        * attr_type
        * attr_name
        * attr_match
        * attr_regex
        * ea
        * ea_match
        * ea_regex

    * $DATA content:

        * header
        * header_hex
        * header_regex & header_len
        * contains
        * contains_hex
        * MD5, SHA1, SHA256
        * yara_rule



Typical Usage Examples
======================

To specify the registry hives of the system, the element would be

.. code:: xml

    <ntfs_find path="\Windows\System32\config\SOFTWARE" header="regf"/>
    <nffs_find path="\Windows\System32\config\SYSTEM" header="regf"/>

To search for all user registry hives, one can use

.. code:: xml

    <ntfs_find path_match="\Users\*\NTUSER.DAT"/>
    <ntfs_find path_match="\Documents and Settings\*\NTUSER.DAT"/>

For instance, you could be interested in getting all fields named ``explorer.exe`` except the one located in ``\Windows\explorer.exe``. This can be done as follows:

.. code:: xml

    <ntfs_exclude path="\Windows\explorer.exe" />
    <ntfs_find name="explorer.exe" />

The following lines search for Windows catalogs, while excluding known ones:

.. code:: xml

    <ntfs_find path_match="\Windows\System32\catroot\*\*.cat" />
    <ntfs_exclude size="138618" md5="d2182e5de2b13d2e68ee66d1bb44fe34" />

To search for a file name qfe.dat which has a data stream whose sha1 is 7894ec01651ff3fcdf9d117f416875bbaef03b6d, which has an extended attribute with a value named toto and whose size is not 104857600, one can write

.. code:: xml

    <ntfs_find name="qfe.dat" ea="toto" sha1="7894ec01651ff3fcdf9d117f416875bbaef03b6d"/>
    <ntfs_exclude size="104857600" />

For a record with the matching file name, the NTFS artefacts registered in this case are all the data streams matching the sha1, on top of the content of matching extended attributes. All of these artefacts are eliminated if the size associated with the record is "104857600", and they are all treated by the tool using the configuration file otherwise.
