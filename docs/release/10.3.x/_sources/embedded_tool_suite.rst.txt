Embedded Tool Suite
===================



The DFIR ORC framework relies on a suite of tools to parse and collect artefacts in a reliable manner.
This part of the documentation provides details about their behavior and configuration.


Utility tools embedded in DFIR ORC binaries are listed below. There is another tool which is not related to collection per se: :doc:`ToolEmbed <ToolEmbed>`.

*  :doc:`FatInfo`: Collects FAT metadata from the file system (file names, hashes, authenticode data, etc.)

*  :doc:`FastFind`: Locate and report on Indicators of Compromise

*  :doc:`GetSamples`: Automated sample collection

*  :doc:`GetSectors`: Collects MBR, VBR and partition slack space

*  :doc:`GetThis`: Collects sample data from the file system (files, ADS, Extended Attributes, etc.)

*  :doc:`NTFSInfo`: Collects NTFS metadata (file entries, timestamps, file hashes, authenticode data, etc.)

*  :doc:`NTFSUtil`: NTFS Master File Table inspector

*  :doc:`ObjInfo`: Collects the named object list (named pipes, mutexes, etc.)

*  :doc:`RegInfo`: Collects registry related information (without mounting hives)

*  :doc:`USNInfo`: Collects USN journal


.. toctree::
    :maxdepth: 2
    :hidden:

    info_tools
    FatInfo
    FastFind
    GetThis
    GetSamples
    GetSectors
    NTFSInfo
    NTFSUtil
    ObjInfo
    RegInfo
    USNInfo
