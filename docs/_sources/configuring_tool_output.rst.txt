=======================
Configuring Tool Output
=======================

DFIR ORC tools configure their output in a unified way.
The syntax is simple and straightforward:

* Command line argument:

    .. code:: bat

        /out=<MyOutput>

* XML configuration file:

    .. code:: xml

        <output>MyOutput</output>

Where <MyOutput> can be a file (usually CSV), a directory or an archive.

.. note:: The option ``/out`` can vary in some tools typically when they have more than one output like NTFSInfo (see MyTool.exe -h for details).

File Output
===========

The simplest form of output:

.. code:: bat

    MyTool.exe /out=c:\temp\foo.csv

In this example, if ``C:\temp`` directory doesn't exist, it is created. If the directory already exists, it must be writable. If the output file already exists, it is overwritten.


The CSV file is only written to every 1048576 bytes (or 1 MB) and at the end of the tool execution.
This implies that tool progress cannot be followed using tools like "tail -f".

The following tools do not support this output:

* :doc:`GetSectors`,
* :doc:`GetThis`,
* :doc:`GetSamples`,
* :doc:`NTFSUtil`,
* :doc:`RegInfo`.

Directory Output
================

Directory output takes the form:

.. code:: bat

    MyTool.exe /out=c:\temp\test

In this example, if ``C:\temp\test`` directory doesn't exist, it is created. If a parent directory doesn't exist, it is also created. Already existing directories must be writable.

The following tools do not support this output:

* :doc:`FastFind`,
* :doc:`NTFSUtil`.

Archive Output
==============

The simplest form of output for an archive is:

.. code:: bat

    MyTool.exe /out=c:\temp\foo.zip

In this example, if ``C:\temp`` directory doesn't exist, it is created. If the directory already exists, it must be writable. If the output archive already exists, it is overwritten.

The archive format is selected based on extension of "foo":

* Foo.zip selects the zip format.
* Foo.7z selects the LZMA/7zip format (www.7zip.org).
* Foo.cab selects the MSCF Microsoft cabinet format.

The following tools do not follow this output syntax:

* :doc:`FastFind`,
* :doc:`NTFSUtil`,
* :doc:`RegInfo`.

Compression (only for zip and 7z Format)
----------------------------------------

The level of compression in the archive can be specified using either an XML configuration file (with a ``compression`` attribute) or a command-line option (with the ``/compression`` option).
Supported values are:

* None
* Fastest
* Fast
* Normal
* Maximum
* Ultra

.. code:: xml

    <output compression="fast">MyOutput.7z</output>

.. code:: bat
        
    MyTool.exe /out=c:\temp\foo.zip /compression=Normal

.. _cfg-tool-output-pwd:

Password (only for zip and 7z Format)
-------------------------------------

.. warning:: The only tools supporting this option are GetThis and GetSamples.

The output archive can be password protected by providing either the ``/password`` option or a ``password`` attribute for the ``output`` element in an XML configuration file.

.. code:: xml

    <output password="avproof">MyOutput.7z</output>
    
.. code:: bat

    MyTool.exe /out=MyOutput.7z /password="avproof"
    
This password should not be regarded as a security feature but can be used to evade anti-viruses when collecting malicious samples.
In order to encrypt archives, one should use the corresponding feature in :ref:`wolf_config <wolf_config-recipient-element>`.

File Character Encoding
=======================

To reduce output file size and ease file analysis on Linux systems (that seems to have issues with UTF16), the default encoding for CSV is UTF8.
The command-line options ``/utf8`` and ``/utf16`` can be used to explicitly control the encoding of the output.

Also, XML configuration files elements ``output`` can have an optional attribute ``encoding``:

.. code:: xml

    <output encoding="utf16">c:\temp</output>

Or

.. code:: xml

    <output encoding="utf8">c:\temp\test.csv</output>
