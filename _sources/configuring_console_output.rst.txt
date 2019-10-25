===================================
Configuring Console Output, Logging
===================================

Tools default console output is sent to the default output console (CONOUT$).
It can be configured to log into a file, output verbose logs, and/or print information to an attached debugger console.

Usage
=====

In XML configuration file, the console output is configured within the ``logging`` element.

``file`` Attribute, ``/logfile=<File>`` Option
-----------------------------------------------

Logs to a file. The log file is created if it does not exist or truncated if it does.
The containing folder must exist and be writeable (or no logging is performed).

Unlike console output, the logging is only written to the file every 1048576 bytes (or 1MB) and at the end of the tool execution.
This implies that tool progress cannot be followed from log file using "tail -f" tools.

    .. code:: xml

        <logging file="c:\Temp\dfir-orc.log"/>

    ::

        /logfile=c:\Temp\dfir-orc.log

``noconsole`` Attribute, ``/noconsole`` Option
-----------------------------------------------

This option disabled console output.

    .. code:: xml

        <logging noconsole=""/>

    ::

        /noconsole

``verbose`` Attribute, ``/verbose`` Option
------------------------------------------

Enables verbose output

    .. code:: xml

        <logging verbose=""/>

    ::

        /verbose

``debug`` Attribute, ``/debug`` Option
--------------------------------------

Enables debug logging. The debug mode also adds debug related traces like source file name and line number where the output is logged.

    .. code:: xml

        <logging debug=""/>

    ::

        /debug

Example of debug logging:

.. code:: bat

    [NTFSInfo_Output.cpp:86] Orc.Exe Version 10.0
    [NTFSInfo_Output.cpp:87] Start time: 10/08/2019 12:47:50.159 (UTC)
    [NTFSInfo_Output.cpp:89] Walker used  : MFT
    [NTFSInfo_Output.cpp:90] Output file  : NTFSInfo.csv
    [NTFSInfo_Output.cpp:94]


Typical Usage Example
=====================

.. code:: bat

    .\DFIR-Orc.exe NTFSInfo /noconsole /debug /logfile=c:\temp\ntfsinfo.log

This example does not output anything to the console (quiet mode), log information directly into an attached debugger and create "c:\\temp\\ntfsinfo.log" containing the console output.

The equivalent XML syntax is:

.. code:: xml

    <logging file="c:\temp\ntfsinfo.log" noconsole="" debug="" />