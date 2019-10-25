=======
RegInfo
=======

Description
===========

RegInfo is a registry parser which can analyze either online or offline registry files.

Online analysis uses the MFT parser and therefore allows enumeration of registry hives without the need to either rely on APIs or be able to open the registry hive file itself.
This allows the collection of registry related information by simply opening the volume (or physical drive, dd image, VSS snapshot).

This analysis works in two steps: file system parsing and hive parsing.

For file system parsing, RegInfo is based on the same parser capabilities as :doc:`GetThis <GetThis>` and :doc:`FastFind <FastFind>`.
That gives the tool unique capabilities to evade hiding techniques such as API hooking techniques, registry permissions, and sharing or permission issues.

The parsing of hive files is then accomplished by a parser which only rely on the C++ standard API.
This allows independence from third party library, permits cross platform and precise control of the output of the tool.

Offline analysis only uses this second step (hive parsing) to inspect registry hives retrieved by other tools (e.g. GetThis).

Output
======

RegInfo produces 2 kinds of files:

* one or more CSV file which contains the result of the different searches (one file for each hive),
* a variable number of .ddmp files which contain data for values, whose size exceeds a certain threshold (512 bytes).

Each CSV file can contain the following registry related information:

.. csv-table::
    :header: ColumnName, Description
    :align: left
    :widths: auto

    ComputerName, Computer name
    TemplateName, Name of the template associated with the query if any
    SearchTerm, Criteria used to match result
    LastModificationDate, Last modification date of the registry key
    KeyName, Key name
    KeyTree, Key path
    ValueName, Value name
    ValueType, Value type
    ValueSize, Size of value
    ValueFlag, Flag of value (explained below)
    ValueData, Value data when possible
    ValueDumpFile, File where the data was dumped

.. note:: The ValueData field contains only the first 512 bytes of the actual data. If the data size exceed this limit, a .ddmp file which contains the entire data is dumped alongside the CSV file.

Most of the CSV output file columns are self explanatory but some of them need to be detailed.

* SearchTerm: This column represent the type of query that matched the current result. The value displayed is the combination of values associated with ``registry_find`` element attributes.
* ValueFlag: This column can take four different values:
    * VALUE_PRESENT: the data associated with the value is present in the CSV file in the ValueData column.
    * VALUE_NOTINHIVE: the data associated with the value has a size but is not present in the hive. This can happen if the registry was not flushed before dumping a hive.
    * VALUE_HASBADCHARS: the data associated with the value contains non-printable characters. The data is not written in the CSV file but in a separate file. The full path of this file is written in the ValueDumpFile column.
    * VALUE_DUMPFILE: the data associated with the value was too long to be written in the CSV file. It is instead written in a separate file. The full path of this file is written in the ValueDumpFile column.

As for every tool, an output for logging is also available from the command line. The syntax can be found in :doc:`Configuring Console Output <configuring_console_output>`.


Usage
=====

When called from the command line, the syntax of RegInfo looks like the following:

.. code:: bat

    DFIR-Orc.exe RegInfo /config=reginfo_config.xml /out=reginfo_output.xml

``/config=<Path>`` Option
-------------------------

*optional=no, default=N/A*

Takes an XML configuration file as argument.

RegInfo is intended to be used with an XML configuration file.
A typical RegInfo configuration file looks like:

.. code:: xml

    <reginfo>

        <output encoding="UTF16">d:\test</output>

        <!-- Fields to be included inside the result file -->
        <information>ComputerName,TemplateName,SearchTerm,LastModificationDate,KeyName,KeyTree,ValueName,ValueType,ValueData</information>

        <!-- Locations to be parsed (MFT parser) -->
        <location>%SystemDrive%</location>
        <location>c:\</location>

        <!-- A search query -->
        <hive>
            <!-- FileFind like criteria on hive -->
            <ntfs_find name="SYSTEM" />
            <!-- Search query criteria -->
            <registry_find key_path_regex="\\ControlSet001\\Services\\[^\\]*" value_regex=".*"/>
        </hive>

        <!-- Another search query -->
        <hive>
            <!-- Path to an offline hive -->
            <filename>c:\temp\SOFTWARE</filename>

            <!-- Search query criterias -->
            <registry_find key="CurrentVersion" value="CurrentMajorVersionNumber" data_hex="0000000a"/>
        </hive>

    </reginfo>
    
.. note:: Hive files can also be specified on command line for *offline* registry hives. Online hives (locked by NTFS) **must** be located via the MFT parser (i.e. ``location`` and ``ntfs_find``).

``reginfo`` Element
-------------------

*optional=no, default=N/A*

Root element.

``output`` Element, ``/out=<Path>`` Option
------------------------------------------

*optional=no, default=N/A*

The value must be a directory (already existing or not) in which the tool will generate the results.
This element can also be specified from the command line with the ``/out`` option. For details on the syntax, please refer to the :doc:`output documentation <configuring_tool_output>`.

Attribute ``encoding`` allows to specify output encoding. Possible values are ``UTF8`` or ``UTF16`` (case-insensitive). Encoding can also be specified with ``/utf8`` and ``/utf16`` options.

``information`` Element
-----------------------

*optional=no, default=N/A*

Selects the columns to fill in the CSV output.

``location`` Element
--------------------

*optional=no, default=N/A*

When configuring to use the MFT parser, RegInfo can locate registry hives on a specific volume. For this purpose, one can use any syntax described in :doc:`Configuring Locations <configuring_locations>`.

``hive`` Element
----------------

*optional=no, default=N/A*

Encloses a query. One can configure different queries on different hives inside the same configuration file.

It is highly recommended to run RegInfo with a complete set of queries for better performance, especially when using the MFT parser.

``filename`` Element
--------------------

*optional=yes, default=N/A*

Used to directly specify the full path of a registry hive. This must only be used with offline hives.

``template`` Element
--------------------

*optional=yes, default=N/A*

In order to simplify both capitalization and usage, RegInfo provides a way to ``template`` search queries.
"Templated" queries are in the form of XML files and can be included in any ``hive`` tag via the ``template`` element.

This element has two attributes :

* ``name`` *(optional=no, default=N/A)*:
    Name that identify the template (it is displayed in the CSV file.)
* ``location`` *(optional=no, default="no")*:
    Path to the template file.

A standard template file typically looks like :

.. code:: xml

    <reginfo_template>

        <!-- Query terms -->
        <registry_find key="Run" />
        <registry_find key="RunOnce" value_regex=".*" />

    </reginfo_template>

The syntax used inside the element ``registry_find`` is the same as the one explained previously in :ref:`registry related elements <RegInfo_Registryfind>`.

``ntfs_find`` or ``ntfs_exclude`` Element
-----------------------------------------

*optional=no, default=N/A*

Used to specify a set of rules which matches the hive in each previously specified location. For details on the ``<ntfs_find>`` element syntax, please refer to the :doc:`ntfs_find documentation <configuring_ntfs_opt>`.

.. _RegInfo_Registryfind:

``registry_find`` Element
-------------------------

*optional=no, default=N/A*

The ``registry_find`` element is used to specify a rule on which to match a registry key, value or data.
There are different types of rules which can be combined (logical AND) to obtain the desired criteria.
Just like for ``ntfs_find``, each rule is specified as an attribute of ``registry_find``.

Here is a list and a short description of those attributes:

.. csv-table::
    :header: Attribute name, Description
    :align: left
    :widths: auto
    
    key, Short name of the key (exact match)
    key_regex, Short name of the key (regular expression match)
    key_path, Full tree key name (exact match)
    key_path_regex, Full tree key name (regular expression match)
    value, Value name (exact match)
    value_regex, Value name (regular expression match)
    value_type, Match on value type (see table below)
    data, "Match on data content, attribute value is considered as a string (exact match)"
    data_hex, "Match on data content, attribute value is a hexadecimal string either taken as is (to match DWORD or QWORD) or interpreted as binary data (exact match)"
    data_regex, "Match on data content, attribute value is considered as a string (regular expression match)"
    data_size, Match on data size (exact match)
    data_size_gt, Match if data size is greater than
    data_size_ge, Match if data size is greater than or equal
    data_size_lt, Match if size is lower than
    data_size_le, Match if size is lower than or equal
    data_contains, "Match a pattern, attribute value is a string (case-sensitive)"
    data_contains_hex, "Match a pattern, attribute value is a hexadecimal string interpreted as binary data (case-sensitive)"

The ``value_type`` attribute can only take one of the following values:

* REG_NONE
* REG_SZ
* REG_EXPAND_SZ
* REG_BINARY
* REG_DWORD
* REG_DWORD_LITTLE_ENDIAN
* REG_DWORD_BIG_ENDIAN
* REG_LINK
* REG_MULTI_SZ
* REG_RESSOURCE_LIST
* REG_FULL_RESSOURCE_DESCRIPTOR
* REG_RESSOURCE_REQUIREMENTS_LIST
* REG_QWORD
* REG_QWORD_LITTLE_ENDIAN

Matching method on data depends on the type of data:

* If registry data is of type ``REG_SZ`` or ``REG_EXPAND_SZ`` the input value in ``data`` or ``data_regex`` is transformed into a Unicode string. The same happen with ``REG_MULTI_SZ``, but in this case, the input value is tested against each string of the multi sz.
* The input for ``data_hex`` must be a valid hexadecimal string (no specific prefix is needed, yet one can still prefix the string with ``0x``). The input is transformed into raw binary and compared to the content of the data in all cases, except for ``REG_DWORD*`` and ``REG_QWORD``. In those cases, the input is transformed into a DWORD or a QWORD in the correct endianness and then compared.
* If ``data_contains`` is used to match against data of type ``REG_SZ``, ``REG_MULTI_SZ`` or ``REG_EXPAND_SZ``, the input is transformed into a Unicode string. In any other cases, it will be considered as ANSI string.
* When ``data_contains_hex`` is used, the input is transformed into raw binary and directly compared to the data content despite its type. This implies that it cannot be used to match ``REG_DWORD*`` and ``REG_QWORD``.
* All string comparisons and regex matchings are case-insensitive except for pattern matching (``data_contains*``) which is case-sensitive.

Some additional usage recommendations:

* Exact matches are always faster than regex matches. Exact matches should always be preferred when possible (even if less compact than regex matches).
* Regex matches use ECMAScript syntax and all DOS-like pattern syntax is forbidden (thus ``*`` is invalid, ``.*`` should be used instead).
* When searching for a fixed pattern to find inside a data, the usage of ``data_contains`` or ``data_contains_hex`` is to be preferred in place of ``data_regex``. They are faster as they use BoyerMoore algorithm instead of regex matching.
* Matching (regex or exact) only on key name/key path only returns the key name and its full path. To retrieve associated values and/or data, one should specify either a value or a data rule (one rule is sufficient to retrieve both the values and data). For instance: 

    .. code:: bat

        <registry_find key_path_regex="\\ControlSet001\\Services\\[^\\]*" value_regex=".*"/>

    This example retrieves every value and data under a direct subkey of ``\\ControlSet001\\Services\\``.

