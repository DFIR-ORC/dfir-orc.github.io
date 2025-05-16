.. _wolf_config-ref:

=========================================
WolfLauncher Configuration File
=========================================


.. _Anchor-root:

The index of this section consists in the following XML skeleton file, which features all the elements that can appear in a real configuration file.

It is not a usable configuration, in the sense that it does not contain any attribute key or value, and **can exhibit incompatible elements**.
Its point is to be exhaustive from the point of view of existing usable elements.


| <`wolf <#wolf-element>`_ attributes="..." >
|    <`log <#log-element>`_ attributes="..." > *value* </log>
|    <`console <#console-element>`_ attributes="..." > *value* </console>
|    <`outline <#outline-element>`_ attributes="..." > > *value* </outline>
|    <`outcome <#outcome-element>`_ attributes="..." > > *value* </outcome>
|    <`recipient <#recipient-element>`_ attributes="..."> *value* </recipient>
|    <`upload <#upload-element>`_ *attributes="..."* />
|    <`archive <#the-archive-element>`_ attributes="...">
|        <`restrictions <#restrictions-element>`_ attributes="..." />
|        <`command <#command-element>`_ attributes="..." >
|          <`execute <#execute-element>`_ attributes="..." />
|          <`input <#input-element>`_ attributes="..." />
|          <`output <#output-element>`_ attributes="..." />
|          <`argument <#argument-element>`_ attributes="..." />
|        <`/command <#command-element>`_>
|    <`/archive <#the-archive-element>`_>
| <`/wolf <#wolf-element>`_>

.. _wolf_config-wolf-element:

``wolf`` Element
================

*optional=no, default=N/A*

Root element.

Attributes
-----------

* **childdebug** *(optional=yes, default=off)*
        Enables (or disables) the command engine to attach as a debugger to all created processes. Upon unhandled exceptions (i.e. application crashes), the command engine will capture the memory dump of the faulty process. This memory dump will then be collected to enable the analysis of the crash.
* **command_timeout** *(optional=yes, default=3 hours)*
        Configures the time (in minutes) the engine will wait for the last command(s) to complete. Upon timeout, the command engine will stop, kill any pending process and move on with archive completion.
* **archive_timeout** *(optional=yes, default=5 minutes)*
        Configures the time (in minutes) the engine will wait for the archive to complete. Upon timeout, this archive will be canceled.
* **werdontshowui** *(optional=yes, default=WER UI will appear)*
        Configures Windows Error Reporting to prevent blocking UI in case of a crash during DFIR ORC execution. WER previous configuration is restored at the end of DFIR ORC execution.

`Back to Root <#anchor-root>`_

.. _wolf_config-log-element:

``log`` Element
===============

*optional=yes, default=N/A*, `parent element: wolf <#wolf-element>`_

The log element can be used to create an optional log file of DFIR ORC execution. This file will be uploaded if an <upload/> element is specified in a :doc:`DFIR ORC local configuration file <orc_local_config>`.

The log message are passing through "sinks" like 'console' or 'file'. To configure log output a sink must be specified.

``Console`` sink element
-------------------------

*optional=yes, default=N/A*, `parent element: log <#log-element>`_

Attributes
~~~~~~~~~~~

* **level** *(optional=yes, default=critical)*
        Log level, one of 'trace', 'debug', 'info' 'error', 'warning', 'critical'.

* **backtrace** *(optional=yes, default=off)*
        Specify a log level which will trigger a log backtrace which will contain logs up to level 'debug'. Can also have the value 'off'.

``File`` sink element
----------------------

*optional=yes, default=N/A*, `parent element: log <#log-element>`_

Attributes
~~~~~~~~~~~

* **level** *(optional=yes, default=info)*
        Log level, one of 'trace', 'debug', 'info' 'error', 'warning', 'critical'.

* **backtrace** *(optional=yes, default=error)*
        Specify a log level which will trigger a log backtrace which will contain logs up to level 'debug'. Can also have the value 'off'.

``output`` Element
~~~~~~~~~~~~~~~~~~~

*optional=yes, default=N/A*, `parent element: file`

Path to the log file. Patterns are supported as with archive element (cf `archive element <#the-archive-element>`_).

Example
--------

.. code:: xml

    <log>
        <console level="critical" backtrace="off"></console>
        <file level="error" backtrace="error">
            <output disposition="truncate">ORC_{SystemType}_{FullComputerName}_{TimeStamp}.dev.log</output>
        </file>
    </log>

`Back to Root <#anchor-root>`_


``console`` Element
===================

*optional=yes, default=no console output file*, `parent element: wolf <#wolf-element>`_

With a configurated Orc in can be convenient to capture console output to a file but keeping console output visible. This elements is complementary to the usual logs as it is intended to be as human readable as possible.

``output`` Element
-------------------

*optional=yes, default=N/A*, `parent element: console`

Path to the console output file. Patterns are supported as with archive element (cf `archive element <#the-archive-element>`_).

Example
--------

.. code:: xml

    <console>
        <output>ORC_{SystemType}_{FullComputerName}_{TimeStamp}.log</output>
    </console>

.. code:: bat

        .\DFIR-Orc.exe /console:output=ORC_W7_COMPUTER_1010.log


`Back to Root <#anchor-root>`_


``outline`` Element
===================

*optional=yes, default=no outline file*, `parent element: wolf <#wolf-element>`_

The :doc:`outline <outline>` element can be used to create an optional json file of DFIR ORC execution's context.
This file will also be uploaded if an <upload/> element is specified in a :doc:`DFIR ORC local configuration file <orc_local_config>`.

Attributes
----------

* **name** *(optional=no, default=N/A)*
        Base file name of the outline file. The same patterns can be used as in the archive file names (cf `archive element <#the-archive-element>`_).

        The following patterns will be automatically substituted:

        ..  csv-table::
            :header: Pattern, Description
            :align: left
            :widths: auto

            {ComputerName}, NetBIOS computer name
            {FullComputerName},Fully qualified DNS name of physical computer (per GetComputerNameEx())
            {TimeStamp}, The current date and time in the following form: YYYYMMDD_HHMMSS
            {SystemType},"The Windows edition type running on this computer: WorkStation, Server, DomainController"

* **disposition** *(optional=yes, default=append)*
        Specifies if the outline file should:

        * be appended to an existing file -> use "append"
        * be created as a new file (and logging should fail if file exists) -> use "create_new"
        * truncate any existing file or create a new file -> use "truncate"

Example
--------

.. code:: xml

  <outline disposition='truncate' >DFIR-ORC\_{SystemType}_{ComputerName}.json</outline>

`Back to Root <#anchor-root>`_


``outcome`` Element
===================

*optional=yes, default=no outcome file*, `parent element: wolf <#wolf-element>`_

The :doc:`outcome <outcome>` element can be used to create an optional json file of DFIR ORC execution's summary.
This file will also be uploaded if an <upload/> element is specified in a :doc:`DFIR ORC local configuration file <orc_local_config>`.

Attributes
----------

* **name** *(optional=no, default=N/A)*
        Base file name of the outcome file. The same patterns can be used as in the archive file names (cf `archive element <#the-archive-element>`_).

        The following patterns will be automatically substituted:

        ..  csv-table::
            :header: Pattern, Description
            :align: left
            :widths: auto

            {ComputerName}, NetBIOS computer name
            {FullComputerName},Fully qualified DNS name of physical computer (per GetComputerNameEx())
            {TimeStamp}, The current date and time in the following form: YYYYMMDD_HHMMSS
            {SystemType},"The Windows edition type running on this computer: WorkStation, Server, DomainController"

* **disposition** *(optional=yes, default=append)*
        Specifies if the outcome file should:

        * be appended to an existing file -> use "append"
        * be created as a new file (and logging should fail if file exists) -> use "create_new"
        * truncate any existing file or create a new file -> use "truncate"

Example
--------

.. code:: xml

  <outcome disposition='truncate' >DFIR-ORC\_{SystemType}_{ComputerName}.json</outcome>

`Back to Root <#anchor-root>`_

.. _wolf_config-recipient-element:


``recipient`` Element
=====================

*optional=yes, default=N/A,* `parent element: wolf <#wolf-element>`_

The recipient element is used to create the list of recipients able to open the CMS enveloped archives. It basically consists of a list of encoded certificates.

Attributes
-----------

* **name** *(optional=no, default=N/A)*
        Name of the recipient
* **archive** *(optional=no, default=N/A)*
        Comma separated list of archive keyword specs to match against archive names. Specifies one or more archives encrypted in a CMS PKCS#7 message (cf http://tools.ietf.org/html/rfc2315).

Example
--------

.. code:: xml

  <recipient name='certfr' archive='*' >
    -----BEGIN CERTIFICATE-----
      ... value ...
    -----END CERTIFICATE-----
  </recipient>

`Back to Root <#anchor-root>`_

.. _wolf_config-upload-element:


``upload`` Element
==================

*optional=yes, default=N/A,* `parent element: wolf <#wolf-element>`_

The upload element is used to configure an optional upload operation when an archive is created.

Attributes
----------

* **job** *(optional=yes, default=none)*
        Describes the upload operation.
* **method** *(optional=no, default=N/A)*
        Describes the method to upload the files. Currently only "filecopy" (uses SMB) or "BITS" are allowed values.
* **server** *(optional=no, default=N/A)*
        Specifies the server name (e.g. `file://servername` or `http://servername`, or `https://servername`) when using BITS or SMB.
* **path** *(optional=no, default= / or \\ depending on the method)*
        Specifies the file share or folder for the upload
* **user** *(optional=yes, default=the current user (executing DFIR ORC))*
        Specifies the user name to be used to connect to the remote server.
* **password** *(optional=yes, default=N/A)*
        Specifies the password to use (for the user defined above)
* **authscheme** *(optional=yes, default=Negotiate (if a user name is specified, anonymous otherwise))*
        Specifies the authentication scheme for the connection. Possible scheme values are:

        * Anonymous
        * Basic
        * NTLM
        * Kerberos
        * Negotiate
* **operation** *(optional=yes, default=copy)*
        "copy" or "move" the archives to the upload server.
* **mode** *(optional=yes, default=sync)*
        "sync" or "async": upload can be synchronous or asynchronous (asynchronous allows DFIR ORC to exit prior to BITS jobs completes). "async" is **not** supported for "filecopy" method.
* **include** *(optional=yes, default=none)*
        Specifies a comma (or semicolon) separated list of patterns, matching the file name of archives, that determine whether an output archive from ``DFIR-Orc.exe`` will be uploaded to the specified location. When missing, all archives are uploaded (if not explicitly excluded, see below). When specified, only archives whose name matches one of the patterns will be uploaded.
* **exclude** *(optional=yes, default=none)*
        Specifies a comma (or semicolon) separated list of patterns, matching the file name of archives, that determine whether an output archive should not be uploaded. When excluded, an output archive is left intact in the output directory (i.e. regardless of the ``operation`` attribute). The ``exclude`` attribute takes precedence over the ``include`` attribute, meaning an archive whose name matches both ``include`` and ``exclude`` patterns will be excluded.

Example
-------

.. code:: xml

    <upload job="DFIR-ORC" method="BITS"
      server="http://MyBits.MyOrg.com"
      path="upload"
      user="MyORG\BITSUploadClient" password="P@ssw0rd!"
      operation="move"
      include="DFIR-ORC_*_Hives.7z" />

`Back to Root <#anchor-root>`_

.. _the-archive-element:

.. _wolf_config-archive-element:

``archive`` Element
===================

*optional=no, default=N/A,* `parent element: wolf <#wolf-element>`_

The archive element specifies the archives to be created during the execution of ``DFIR-Orc.exe WolfLauncher``.

Attributes
-----------

* **name** *(optional=no, default=N/A)*
        Configures the name of the archive

        The following patterns will be automatically substituted:

        ..  csv-table::
            :header: Pattern, Description
            :align: left
            :widths: auto
    
            {ComputerName}, NetBIOS computer name
            {FullComputerName},Fully qualified DNS name of physical computer (per GetComputerNameEx())
            {TimeStamp}, The current date and time in the following form: YYYYMMDD_HHMMSS
            {SystemType},"The Windows edition type running on this computer: WorkStation, Server, DomainController"

* **keyword** *(optional=no, default=N/A)*
        Uniquely identifies this archive
* **concurrency** *(optional=no, default=N/A)*
        Configures the number of concurrent executions
* **optional** *(optional=yes, default=archive is generated)*
        Marks an archive as optional (i.e. not generated by default)
* **repeat** *(optional=no, default=Once)*
        Configures the behavior of the engine upon rerun. Permitted values are:

        * CreateNew: a new archive is created each time ``DFIR-Orc.exe`` is run, with names suffixed by _1.7z, _2.7z, etc. An alternative is to use the {TimeStamp} pattern in the archive name.
        * Overwrite: previous archives are overwritten by new executions of ``DFIR-Orc.exe``.
        * Once: if the target file already exists (and is not empty), then this archive is skipped.

        .. note:: This is also taken into account when associated with the upload functionality.
* **compression** *(optional=yes, default=normal)*
        Configures the compression level used by the compression engine (7zip & zip only). Values can be: None, Fastest, Fast, Normal, Maximum, Ultra.
* **command_timeout** *(optional=yes, default=3 hours)*
        Per archive, override the global configured time (in minutes) the engine will wait for the last command(s) to complete. Upon timeout, the command engine will stop, kill any pending process and move on with archive completion.
* **archive_timeout** *(optional=yes, default=5 minutes)*
        Per archive, override the global configured time (in minutes) the engine will wait for the archive to complete. Upon timeout, this archive will be canceled.
* **physicalmemory** *(optional=yes, default=none)*
        Per archive condition, do not execute commands if installed memory does not match (ex: "<=32GB" will trigger only if system has less than 32GB)
* **diskfree** *(optional=yes, default=none)*
        Per archive periodic check, stop commands execution if disk free space requirement is not satisfied anymore (ex: "10GB")
* **childdebug** *(optional=yes, default=false)*
        Per archive, sets if the child process should be under the control of a debugger when running. If so, a mini dump file will be created if a crash occurs. If set to "no", explicitly disables the debugger, any other value activates the debugger. Please note that this setting is overridden by command line option or attribute attached to the wolf element.

Example
--------

.. code:: xml

  <archive name='Quick\_{ComputerName}.7z' keyword='Basic' concurrency='2' repeat='Overwrite' >
    <restrictions JobMemoryLimit='3G' JobCPULimit='30' ProcessMemoryLimit='1G'
        ElapsedTimeLimit='360' ProcessCPULimit='10' />
      ...
  </archive>

`Back to Root <#anchor-root>`_

``restrictions`` Element
========================

*optional=yes, default=N/A,* `parent element: wolf <#wolf-element>`_

This element configures the Windows job controlling the execution of subprocesses. Limits are set to the resources processes can consume. When a limit is reached, all remaining processes in the job will be terminated and the available output files will be collected into the archive.

Attributes
-----------

* **JobMemoryLimit** *(optional=yes, default=unlimited)*
        Memory limit (working set) which the processes created can collectively commit. Can be expressed with multipliers (K,M,G). Example 3G for 3GB.
* **ProcessMemoryLimit** *(optional=yes, default=unlimited)*
        Memory limit (working set) which the processes created can individually commit. Can be expressed with multipliers (K,M,G). Example 3G for 3GB.
* **ElapsedTimeLimit** *(optional=yes, default=unlimited)*
        Elapsed time (in minutes) the complete execution of the commands involved in this archive can take.
* **JobCPULimit** *(optional=yes, default=unlimited)*
        Limits the amount of CPU time which processes in the job can collectively consume before being stopped (in minutes).
* **ProcessCPULimit** *(optional=yes, default=unlimited)*
        Limits the amount of CPU time a process can use before being stopped (in minutes).

Example
--------

.. code:: xml

  <restrictions JobMemoryLimit="3G" ProcessMemoryLimit="2G" ElapsedTimeLimit="360" />

`Back to Root <#anchor-root>`_

.. _wolf_config-command-element:

``command`` Element
===================

*optional=no, default=N/A,* `parent element: archive <#the-archive-element>`_

The command executed is created with the command element. This section of the configuration describes:

* the resources needed to execute: binary, prerequisites,
* the arguments passed to the command line, and
* the output expected upon completion of the task.

Attributes
-----------

* **keyword** *(optional=no, default=N/A)*
        Uniquely identifies this task in the archive
* **timeout** *(optional=yes, default=N/A)*
        Terminate the command if the timeout is reached (in minutes).
* **winver** *(optional=yes, default=always execute)*
        Limits the execution of this command to one or several specific versions of Windows.
        The valid values of this attribute are:

        * winver="X.x": this command will only execute on Windows major version X and minor x, 
        * winver="X.x+": this command will only execute on Windows version "X.x" and successors, 
        * winver="X.x-": this command will only execute on Windows version "X.x" and predecessors.
* **queue** *(optional=yes, default=queue)*
        Configures the behavior of the archive engine for the output of this command.
        The available values for this attribute are as follows.

        * flush: the command produces a lot of output the engine must archive immediately,
        * Any other value will configure the output of this command to be queued until the next flush or the end of all the commands.
* **systemtype** *(optional=yes, default=always execute)*
        Configures if a specific command should be run depending on the system type.
        The available values for this attribute are:

        * WorkStation: for client workstations
        * Server: for general purpose servers
        * DomainController: for domain controllers

        Values can be combined with '|'. For example, Server|DomainController results in executing the command on all servers.
* **diskfree** *(optional=yes, default=none)*
        Stop command execution if disk free space requirement is not satisfied anymore (ex: "10GB")
* **optional** *(optional=yes, default=false (command not optional))*
        Marks a command execution as optional (i.e. not executed by default)

Example
--------

.. code:: xml

  <command keyword='NTFSInfo'  queue='flush'>
            <execute name='DFIR-Orc.exe' run='self:#NTFSInfo' />
            <argument>/config=res:#ntfsinfo_basic</argument>
            <output name='NTFSInfo'
                    source='Directory' filematch='\*.csv'
                    argument='/fileinfo={DirectoryName}' />
            <output name='NTFSInfo.log' source='StdOut' />
  </command>

`Back to Root <#anchor-root>`_

.. _wolf_config-execute-element:

``execute`` Element
===================

*optional=no, default=N/A,* `parent element: command <#command-element>`_

Configures the program to be executed.
It can be a local command from the file system or an embedded resource.
On 64-bit platforms, the run64 attribute is evaluated first and used if available.
If not, ``DFIR-Orc.exe WolfLauncher`` evaluates the run attribute.

Similarly, on 32-bit platforms, the run32 attribute is evaluated first and used if available.
If not, ``DFIR-Orc.exe WolfLauncher`` evaluates the run attribute.
Attributes named run, run32 and run64 can use the :doc:`resource syntax <resources>` or directly reference a file on the live system (environment variables are expanded).

Attributes
-----------

* **name** *(optional=no, default=N/A)*
        Provides the name of a temporary file to be extracted (if need be)
* **run** *(optional=yes, default=N/A)*
        Provides the reference to the binary to execute (either on the file system or as a resource)
* **run32** *(optional=yes, default=N/A)*
        Provides the reference to the binary to execute on 32-bit platforms
* **run64** *(optional=yes, default=N/A)*
        Provides the reference to the binary to execute on 64-bit platforms

Example
--------

.. code:: xml

  <execute name='ipconfig.exe' run='%windir%\System32\ipconfig.exe' />

`Back to Root <#anchor-root>`_

``input`` Element
=================

*optional=yes, default=N/A,* `parent element: command <#command-element>`_

Configures the files on which the execution depends (typically a configuration file or input file).
Command-line arguments can be passed to a tool using the argument attribute.

Attributes
-----------

* **name** *(optional=no, default=N/A)*
      Name of the extracted file
* **source** *(optional=no, default=N/A)*
      Describes the source for this input. Typically this is a resource of the ``DFIR-Orc.exe`` PE file.
* **argument** *(optional=yes, default=empty)*
      A command line argument to specify this input file to the executed command. Order is preserved.

Example
--------

.. code:: xml

  <input  name='NTFSInfo_Config.xml' source='res:#NTFSINFO_Config'
    argument='/config={FileName}' />

`Back to Root <#anchor-root>`_

``output`` Element
==================

*optional=yes, default=N/A,* `parent element: command <#command-element>`_

Configures the outputs of the command execution.
Command-line arguments to further specify the output can be passed to a tool using the argument attribute.

Attributes
-----------

* **name** *(optional=no, default=N/A)*
        This is the file name (relative to the temp dir) of the expected output of the execution
* **source** *(optional=no, default=N/A)*
        This is the type of output:

        - "StdOut" is the console output
        - "StdErr" is the error console output
        - "StdOutErr" represents the normal and error console outputs combined
        - "File" is a single output file
        - "Directory" is a list of files from a directory
* **argument** *(optional=yes, default=N/A)*
      A command-line argument to specify this output to the executed command. Order is preserved.
* **filematch** *(optional=yes, default=N/A)*
      Filters the content of the directory to a subset of expected files matching a DOS pattern (for instance \*.csv).

Examples
--------

.. code:: xml

  <output name='NTFSInfo_AllRecords'     
            source='Directory' filematch='\*.csv' 
            argument='/fileinfo={DirectoryName}' />


.. code:: xml

  <output  name='USNInfo.log' source='StdOut' />

`Back to Root <#anchor-root>`_

.. _Anchor-argument:

``argument`` Element
====================

*optional=yes, default=N/A,* `parent element: command <#command-element>`_

This element will add an argument to the command line of the executed command.

Attributes
-----------

None

Example
--------

.. code:: xml

  <argument>/config=MyConfig.xml /verbose</argument>

`Back to Root <#anchor-root>`_

