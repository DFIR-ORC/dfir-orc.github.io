=======
ObjInfo
=======

Description
===========

ObjInfo is a tool designed to list the set of Microsoft Windows named objects currently present on the analyzed system.

Output
======

ObjInfo creates a single CSV file that lists the currently present Windows named objects.

The resulting CSV reports the following columns:

.. csv-table::
    :header: ColumnName, Description
    :align: left
    :widths: auto

    ComputerName, The current computer name running ObjInfo
    OperatingSystem, The Microsoft Windows operating system
    ObjectType, "The reported object type (one of Type, Directory, Session, WindowStation, Event, KeyedEvent, Callback, Job, Mutant, Section, Semaphore, SymbolicLink, Device, Driver, ALPCPort, FilterConnectionPort, Key, File)"
    ObjectName, The actual object name
    ObjectPath, The full object path
    LinkTarget, "For symbolic links, the link's target"
    LinkCreationTime, "For symbolic links, the link's creation date"
    Description, Always empty (only used with FastFind tool)

As for every tool, an output for logging is also available from the command line. The syntax can be found in :doc:`Configuring Console Output <configuring_console_output>`.

.. note::
    
    The error message: "Failed to open object directory \\UMDFCommunicationPorts" is to be expected as administrators do not have enough privileges to access this object.

Usage
=====

ObjInfo is intended to be used from the command line. A typical ObjInfo command line looks like the following:

.. code:: bat
    
    DFIR-Orc.exe ObjInfo /out=C:\temp\ObjInfo.7z

``/out=<Path>`` Option
----------------------

*optional=yes, default=.\\ObjInfo.csv*

If an archive or a directory is specified as output, two files are created: one for "File" type objects and another for objects of other types.

If a file is specified, information about all objects are reported in this file.

For details on the ``/out`` option syntax, please refer to the :doc:`output documentation <configuring_tool_output>`.

