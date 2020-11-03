DFIR ORC Command-line Options
==============================

DFIR ORC cannot be solely configured using command-line options. It never was and never will be possible.
DFIR ORC is configured using XML configuration files. Command-line options are too often misused, misspelled or misunderstood
by users and/or administrators. DFIR ORC aims to be error resilient and delivers its output no matter what.
That being said, command-line options can be used to change certain behaviors of a configured binary.

.. note:: Options are case insensitive.

``/out=<OutputFolder>`` Option
------------------------------

Modifies the output location of the archives. This must be an existing directory with write access for the user running ``DFIR-Orc.exe``.

.. code:: bat

    /out=<OutputFolder>
    /out=\\myServer\MyShare\OutputFolder

By default, outputs are written in the current directory a.k.a. ``.``

This option overrides the output location setting defined by the :ref:`output element <orc_local_config-output-element>` in a local configuration file.

.. note:: This option does not affect the upload location.

``/TempDir=<TempFolder>`` Option
--------------------------------

Changes the temporary folder used for temporary files.

.. code:: bat

    /tempdir=<OutputFolder>
    /tempdir=%temp%\MyTemp

By default, %TEMP%\\WorkingTemp\\ is used.

This option overrides the directory defined in the :ref:`temporary element <orc_local_config-temporary-element>` in a local configuration file.

.. _cli_options-keys:

``/Keys`` Option
----------------

This option can be used to visualize the archives and commands of a configured binary ``DFIR-Orc.exe``.
When ``/Keys`` is used, no command is executed, no archives are created.

.. code:: bat

    /Keys

An example of the output for this command is shown below.

.. code:: bat

    .\DFIR-Orc.exe /Keys

    DFIR-Orc Version 10.0.2.000

    Start time            : 10/22/2019 09:07:07.956 (UTC)

    Computer              : DESKTOP-ORBLVTG

    User                  : DESKTOP-ORBLVTG\user (elevated)

    System type           : WorkStation

    System tags           : OSBuild#18362,RTM,Release#1903,Windows10,WorkStation,x64
    Operating System      : Microsoft Windows 10 Professional (build 18362), 64-bit
    Output   directory    : C:\Temp\output (encoding=UTF8)
    Temp     directory    : C:\Temp\WorkingTemp (encoding=UTF8)
    Log file              : DFIR-ORC_WorkStation_DESKTOP-ORBLVT_20191022_090707.log
    Repeat Behavior       : No global override set (config behavior used)
    Priority              : Low

    [X] Archive: Main (file is DFIR-ORC_WorkStation_DESKTOP-ORBLVTG_Main.7z)
            [X] Command SystemInfo
            [X] Command Processes
            [X] Command GetEvents
            [X] Command Autoruns
            [X] Command NTFSInfo
            [ ] Command NTFSInfoHashPE
            [X] Command FatInfo
            [ ] Command FatInfoHashPE
            [X] Command USNInfo
            [X] Command GetArtefacts

    [X] Archive: Hives (file is DFIR-ORC_WorkStation_DESKTOP-ORBLVTG_Hives.7z)
            [X] Command GetSystemHives
            [X] Command GetUserHives
            [X] Command GetSamHive

    [ ] Archive: Yara (file is DFIR-ORC_WorkStation_DESKTOP-ORBLVTG_Yara.7z)
            [X] Command GetYara

    Finish time           : 10/22/2019 09:07:07.956 (UTC)
    Elapsed time          : 0 msecs

An ``[X]`` before an archive implies that it will be collected. However, an ``[X]`` before a command only shows the default commands run when collecting the archive. If the archive itself is not selected, the command **will not** be run.
In the previous example, the archives ``Main.7z`` and ``Hives.7z`` are computed but not ``Yara.7z``.

``/Key=<Keyword>``, ``/+Key=<Keyword>`` and ``/-Key=<Keyword>`` Options
-----------------------------------------------------------------------

Regarding the ``<Keyword>`` value:

* the list of available keywords can be obtained with the ``/Keys`` option,
* can be a comma separated list of keywords,
* are case insensitive,
* non-matching keywords are not executed nor generated (and no warning message displayed).

The ``/Key=<Keyword>`` option allows the selection of specific commands to be executed or archives to be generated.

.. code:: bat

    /Key=<Keyword>
    /Key=Main
    
The ``/+Key=<Keyword>`` option enables an optional archive or command (cf. :ref:`archive element <wolf_config-archive-element>`, :ref:`command element <wolf_config-command-element>`).

.. code:: bat

    /+Key=<Keyword>
    /+Key=GetYara

The ``/-Key=<Keyword>`` option disables an archive generation or command execution.

.. code:: bat

    /-Key=<Keyword>
    /-Key=Hives,NTFSInfo

Options ``/+Key`` and ``/-Key`` can be combined and repeated on the command line. ``/+Key`` options take effect first and then the ``/-Key`` ones.

This option overrides the attributes of the :ref:`archive element <wolf_config-archive-element>` and the :ref:`command element <wolf_config-command-element>`.

It also overrides optional settings using :ref:`key, enable_key and disable_key elements <orc_local_config-key-element>` in a local configuration file.

.. note:: "c++" syntax ``/Key+=<keyword>`` and ``/Key-=<keyword>`` is also supported.

.. note:: ``/Keys`` can be used in conjunction with ``/Key``, ``/+Key`` and ``/-Key`` to visualize the command and archives actually selected to be collected.

``/ChildDebug`` and ``/NoChildDebug`` Options
---------------------------------------------

These options respectively enable and disable the debugger of DFIR ORC.

.. code:: bat

    /ChildDebug
    /NoChildDebug

The debugger is disabled by default.

This option overrides the ``ChildDebug`` attribute set in the :ref:`wolf element <wolf_config-wolf-element>`.

``/Once``, ``/Overwrite`` and ``/CreateNew`` Options
----------------------------------------------------

These options control the behavior of the launcher when the output archives are already present in the output or upload location (cf. :ref:`archive element <wolf_config-archive-element>`).

These options apply to all archives created by the execution of ``DFIR-Orc.exe``.

.. code:: bat

    /Once
    /OverWrite
    /CreateNew

This option overrides the ``repeat`` attribute set in the :ref:`archive element <wolf_config-archive-element>` in a WolfLauncher configuration file.

``/Compression=<CompressionLevel>`` Option
------------------------------------------

This option controls the level of compression for generated archives.
Allowed values are: ``None``, ``Fastest``, ``Fast``, ``Normal``, ``Maximum``, ``Ultra``.

The override applies to all archives created by the DFIR ORC execution.

.. code:: bat

    /Compression=Fast

By default, level ``Normal`` is used.

This option overrides the ``compression`` attribute set in the :ref:`archive element <wolf_config-archive-element>` in a WolfLauncher configuration file.

``/archive_timeout=<TimeoutValue>`` Option
------------------------------------------

This option configures the number of minutes during which the archive is allowed to run **after** the last command finishes. In other words, this parameter is the timeout after which the archive is canceled at the end of command execution.

.. code:: bat

    /archive_timeout=10

By default, an archive creation has to complete within 5 minutes after the last command terminates.

This option overrides the ``archive_timeout`` attribute set in the :ref:`archive element <wolf_config-archive-element>` in a WolfLauncher configuration file.

``/command_timeout=<TimeoutValue>`` Option
------------------------------------------

This option configures the time span (in minutes) during which the command engine is allowed to run. In other words, this parameter configures the total amount of time, per archive, the commands can take to execute.

.. code:: bat

    /command_timeout=180

By default, after 3 hours, any pending command is killed, the archive is then properly completed and closed.

This option overrides the attribute ``command_timeout`` of the :ref:`archive element <wolf_config-archive-element>` in a WolfLauncher configuration file.

``/tee_cleartext`` Option
-------------------------

This option is for **testing/debugging purposes only**. It creates a clear text file alongside the encrypted file when DFIR ORC encrypts its output (cf :ref:`wolf recipient element <wolf_config-recipient-element>`).

``/no_journaling`` Option
--------------------------

This option disables the journal format inside PKCS#7 CMS messages (for encrypted archives), thus directly creating the enveloped archive inside the CMS message (at the expense of a temporary clear text file created on disk).

``/WERDontShowUI`` Option
-------------------------

When ``DFIR-Orc.exe`` and children crash (no matter whether child debug is enabled), it may happen that a user interface is shown to the user, asking for interaction.

This results in a loss of concurrent execution and ``DFIR-Orc.exe`` eventually hangs (when all concurrent runs are blocked by this UI). To prevent this, the ``WERDontShowUI`` option temporarily disables WER UI (Microsoft Windows Error Reporting).
When DFIR ORC ends, this parameter is reset to its previous value.

.. warning:: Using this option may modify twice the registry value of ``HKEY_CURRENT_USER\Software\Microsoft\Windows\Windows Error Reporting,DontShowUI``.

By default, it is disabled (i.e. WER prompts are shown).

This option overrides the ``werdontshowui`` attribute of the :ref:`wolf element <wolf_config-wolf-element>`.

``/Priority=<Level>`` Option
-------------------------------

To avoid impact on the user experience during the tool execution, ``DFIR-Orc.exe`` can be launched with a modified priority (typically below normal).

Available priority values are:

.. csv-table::
    :header: Priority level, Description
    :align: left
    :widths: auto

    ``low``,BELOW_NORMAL_PRIORITY_CLASS
    ``normal``,NORMAL_PRIORITY_CLASS
    ``high``,ABOVE_NORMAL_PRIORITY_CLASS

This option overrides the ``priority`` attribute of the :ref:`dfir-orc element <orc_local_config-dfir-orc-element>` in a local configuration file.

``/PowerState=<Requirements>`` Option
-------------------------------------

To avoid letting the computer sleep (a.k.a. going to StandBy or S3 power mode) when the user is away, this option can be used with the following values:

* ``SystemRequired``
* ``DisplayRequired``
* ``UserPresent``
* ``AwayMode``

To only prevent sleep, recommended value for this option is: ``SystemRequired,AwayMode``.

This option overrides the ``powerstate`` attribute of the :ref:`dfir-orc element <orc_local_config-dfir-orc-element>` in a local configuration file.

Mothership Specific Command-line Options
----------------------------------------

The :ref:`Mothership mechanism <architecture-exec>` allows DFIR ORC to be executed in any compatible context (Scheduled Task, Logon Script, Startup script, x86/x64...). The configuration allows the Mothership to launch the subsequent execution which suits the context. Specific command-line options can be used to customize this behavior.

``-NoWait`` Option
``````````````````

With this option, the mothership executes the command engine (i.e. WolfLauncher) with appropriate options (CREATE_SUSPENDED|CREATE_BREAKAWAY_FROM_JOB) and return immediately.
This option is typically used in startup scripts which could limit the time ``DFIR-Orc.exe`` is allowed to run.

``-WMI`` Option
```````````````

With this option, the mothership executes the command engine (i.e. WolfLauncher) using WMI (the ``Win32_Process::Create`` method).

``-PreserveJob`` Option
```````````````````````

With this option, the mothership **does not** alter the job under which it executes.
By default, the mothership attempts to modify the current job (if needed, typically to allow JOB_OBJECT_LIMIT_BREAKAWAY_OK).

.. warning:: Using this option may lead to a failure in WolfLauncher command engine if BreakAwayFromJob is not allowed. See :doc:`platforms` for more details.
