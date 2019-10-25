====================================
Implementation Details About Parsers
====================================

MFT Parser
==========

To circumvent strict ACLs or restrictive sharing status of files, we have implemented a Master File Table (MFT) parser allowing to directly open the volume itself (``\\.\C:``) and read disk geometry and information.
From here, it is possible to locate the boot sector that provides information about the location of the $MFT
extents (or segments). The MFT can then be read, record by record.

The MFT records are parsed to read attributes like $FILE_NAME and $DATA ones.
Using this data, NTFS metadata information can be deduced.
One of the immediate benefits of using an MFT parser is the ability to compute cryptographic
hashes of locked or secured (DACLed) files, as well as being able to read their contents.

USN Parser
==========

The USN parser is based on a specific FSCTL called ``FSCTL_ENUM_USN_DATA``.

.. _FSCTL_ENUM_USN_DATA: http://msdn.microsoft.com/en-us/library/aa364563(VS.85).aspx

FSCTL_ENUM_USN_DATA does not walk through the change journal.
It is a fallback path for when a change journal does not record all the information requested by an application.
This call walks through the MFT to identify files changed between two USN identifiers.

If the identifiers specified are zero and MAXLONGLONG, this effectively walks through every file on the volume (whether USN is active or not).

The USN parser is now deprecated and should not be used (it was the first parser implemented).


The MFT parser provides multiple benefits over the USN parser:

* Much faster
* Less fragile to malware interfering (does not rely on CreateFile or NtOpenFile)
* Feature complete

