=======
USNInfo
=======

Description
===========

USNInfo collects information from the USN journal. It uses the same USN journal enumeration routines as NTFSInfo, but with FSCTL_READ_USN_JOURNAL (refer to :doc:`USN parser implementation <fs_implem_details>` for more details).
The USN journal is enumerated starting with the oldest entries and ending with the most recent.

Output
======    

USNInfo can create CSV files in two ways:

* one file per NTFS Volume, or
* one file for all analyzed volumes.


.. csv-table::
    :header: ColumnName, Description
    :align: left
    :widths: auto

    Computer, The current computer name
    USN, The associated USN
    FRN, The associated FRN
    ParentFRN, The FRN of the parent directory
    Timestamp, The timestamp
    File, The file name
    FullPath, The full-path name for this entry
    FileAttributes, The attribute for the file associated with this entry
    Reason, The reason name
    VolumeID, Volume identification
    SnapshotID, Snapshot identification

As for every tool, an output for logging is also available from the command line. The syntax can be found in :doc:`Configuring Console Output <configuring_console_output>`.

Usage
=====

USNInfo is intended to be used from the command line. A typical USNInfo command line looks like the following:

.. code:: bat
    
    DFIR-Orc.exe USNInfo /out=C:\temp\USNInfo.7z *

The argument for this tool is a list of locations where a USN journal should be collected. The syntax to use is described in :doc:`Configuring Locations <configuring_locations>`: the list should be separated by spaces.
If "*" is passed as an argument, USNInfo parses all mounted volumes.

``/out=<Path>`` Option
----------------------

*optional=yes, default=.\\USNInfo.csv*

For details on the ``/out`` option syntax, please refer to the :doc:`output documentation <configuring_tool_output>`.

.. note::
    
    When specifying a folder or an archive for this option, the tool creates one file per volume.

``/Compact`` Option
-------------------

*optional=yes, default=N/A*

When using this option, the full-path column is not filled in and the reason is in hexadecimal form in the output CSV file. 

Compact format is not intended to be human readable and should be reserved for machine interpretation.
This format helps provide much smaller output files, which can be processed later using a complete NTFSInfo output.
