===================================
Configuring Console Output, Logging
===================================

Multiple log output are available and they can be use simultaneously. Existing output are console, file and limited syslog.

**Syslog use is currently limited to WolfLauncher high level logs**.

Usage
=====

In XML configuration file, the console output and the file output are configured within the ``log`` element.


``log`` Element
===============

*optional=yes, default=N/A*, `parent element: wolf <#wolf-element>`_

The log element can be used to create an optional log file of DFIR ORC execution. This file will be uploaded if an <upload/> element is specified in a :doc:`DFIR ORC local configuration file <orc_local_config>`.

The log message are passing through "sinks" like 'console' or 'file'. To configure log output a sink must be specified.

``Console`` sink element, ``/log:console,...`` Option
------------------------------------------------------

*optional=yes, default=N/A*, `parent element: log`

``level`` Attribute, ``/log:console,level=<Level>,...`` Option
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*optional=yes, default=critical*, `parent element: console`

Log level is one of 'trace', 'debug', 'info' 'error', 'warning', 'critical'.

``backtrace`` Attribute, ``/log:console,backtrace=<Level>,...`` Option
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*optional=yes, default=off*, `parent element: console`

Specify a log level which will trigger a log backtrace which will contain logs up to level 'debug'.

Value is one of 'trace', 'debug', 'info' 'error', 'warning', 'critical', off.

``File`` sink element, ``/log:file,...`` Option
------------------------------------------------

*optional=yes, default=N/A*, `parent element: log`

The logging can be written to the file at the end of the tool execution.
This implies that tool progress cannot be followed from log file using "tail 

``level`` Attribute, ``/log:file,level=<Level>,...`` Option
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*optional=yes, default=info*, `parent element: file`

Log level is one of 'trace', 'debug', 'info' 'error', 'warning', 'critical'.

``backtrace`` Attribute, ``/log:file,backtrace=<Level>,...`` Option
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*optional=yes, default=error*, `parent element: file`

Specify a log level which will trigger a log backtrace which will contain logs up to level 'debug'.

Value is one of 'trace', 'debug', 'info' 'error', 'warning', 'critical', off.


``output`` Element, ``/log:file,output=Path>,...`` Option
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*optional=yes, default=N/A*, `parent element: file`

Path to the log file. Patterns are supported as with archive element (cf `archive element <#the-archive-element>`_).

``Syslog`` sink element, ``/log:syslog,...`` Option
----------------------------------------------------

*optional=yes, default=N/A*, `parent element: log`

Redirect high level logs to a syslog server.

**Currently 'syslog' use is restricted to WolfLauncher**.

``level`` Attribute, ``/log:syslog,level=<Level>,...`` Option
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*optional=yes, default=info*, `parent element: syslog`

Log level is one of 'trace', 'debug', 'info' 'error', 'warning', 'critical'.

``backtrace`` Attribute, ``/log:syslog,backtrace=<Level>,...`` Option
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*optional=yes, default=off*, `parent element: syslog`

Specify a log level which will trigger a log backtrace which will contain logs up to level 'debug'.

Value is one of 'trace', 'debug', 'info' 'error', 'warning', 'critical', off.

``host`` Attribute, ``/log:syslog,host=<ip4_or_ip6>,...`` Option
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*optional=no, default=N/A*, `parent element: syslog`

Address of the syslog server

``port`` Attribute, ``/log:syslog,port=<port>,...`` Option
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*optional=yes, default=514*, `parent element: syslog`

Port of the syslog server.

Example
--------

.. code:: xml

    <log>
        <console level="critical" backtrace="off"></console>
        <file level="error" backtrace="error">
            <output disposition="truncate">ORC_{SystemType}_{FullComputerName}_{TimeStamp}.dev.log</output>
        </file>
        <syslog>
            <host>127.0.0.1</host>
            <port>514</port>
        </syslog>
    </log>

.. code:: bat

    dfir-orc.exe \
        /log:console,level=critical,backtrace=off \
        /log:file,level=debug,backtrace=error,output="dfir-orc.log" \
        /log:syslog,host=127.0.0.1,port=514 ...

`Back to Root <#anchor-root>`_


``noconsole`` Attribute, ``/noconsole`` Option
-----------------------------------------------

This option disabled console output.

    .. code:: xml

        <logging noconsole=""/>

    ::

        /noconsole

``verbose`` Attribute, ``/verbose`` Option
------------------------------------------

Enables verbose output. **XML is deprecated**.

    .. code:: xml

        <logging verbose=""/>

    ::

        /verbose

``debug`` Attribute, ``/debug`` Option
--------------------------------------

Enables debug logging for Console and File log output. **XML is deprecated**.

    .. code:: xml

        <logging debug=""/>

    ::

        /debug

Example of debug logging:

.. code:: bat

    2021-02-08T17:43:41.200Z [I] WolfLauncher v10.1.0-rc3-115-ge4123652(orc.git 66613f2cdbc7fd9241eb9acabfab7a6ac19a242b


Typical Usage Example
=====================

.. code:: bat

    .\DFIR-Orc.exe NTFSInfo /noconsole /debug /log:file,level=error,output=c:\temp\ntfsinfo.log

This example does not output anything to the console (quiet mode), log information directly into an attached debugger and create "c:\\temp\\ntfsinfo.log" containing the console output.

The equivalent XML syntax is:

.. code:: xml

    <logging file="c:\temp\ntfsinfo.log" noconsole="" debug="" />