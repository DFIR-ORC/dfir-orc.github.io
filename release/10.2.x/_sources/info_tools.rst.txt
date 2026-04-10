Common Options & Properties
===========================

Supported Versions
------------------

File system related tools are entirely implemented in native C++, compiled with Visual Studio 2017 Update 9 and do not require any installation prior to execution on the currently :doc:`supported versions of Windows<platforms>`.

Help
----
Getting help can be done using ``/help`` or ``/?``, for configured and unconfigured binaries.

.. code:: bat

   DFIR-Orc.exe /help
   DFIR-Orc_x64.exe NTFSUtil /?



For any tool embedded by default, the same options apply. For example, both of the following commands display the help menu for NTFSUtil:

.. code:: bat

   DFIR-Orc_x64.exe NTFSUtil /help
   DFIR-Orc.exe NTFSUtil /?


Table of Contents of Common Options & Properties
------------------------------------------------

.. toctree::

   fs_implem_details
   configuring_locations
   configuring_yara
   configuring_ntfs_opt
   configuring_console_output
   configuring_process
   configuring_tool_output
