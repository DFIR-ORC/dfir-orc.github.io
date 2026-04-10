============================
Configuring the Yara Scanner
============================

FastFind, RegInfo and GetThis can use libyara to scan for matches on a disk.

This scan can be configured with a ``<yara />`` element:
    | <yara
    |      `source="..." <#configuring-yara-source>`_
    |      `block="..." <#configuring-yara-block>`_
    |      `overlap="..." <#configuring-yara-overlap>`_
    |      `timeout="..." <#configuring-yara-timeout>`_
    |      `scan_method="..." <#configuring-yara-scan-method>`_
    | />

A typical XML line for a ``yara`` element:

.. code:: xml

    <yara source="IOC.yara" block="2M" timeout="120" overlap="8192" />

.. _configuring-yara-source:

``source`` Attribute
====================

Comma-separated or semicolon-separated list of yara files.
This list can be actual file names or references to embedded resources or both.
When specifying file names, the paths are relative to the folder from which the configured binary is executed.

.. code:: xml

    source="res:#MyYaraContent,rules\ruleset.yara"

.. _configuring-yara-scan-method:

``scan_method`` Attribute
=========================

When scanning files, the Yara engine can read them in blocks or as one big chunk of data. Available methods are:

* ``blocks`` to read and scan files in blocks of size given by the `block <#configuring-yara-block>`_ attribute, and
* ``filemapping`` to read and scan files in one chunk using a pagefile-backed file mapping. This is *not* the same behavior as the ``yarac.exe`` binary which uses a file-backed mapping implying a sharing lock on the file which would be hazardous during live system scanning.

.. code:: xml

    scan_method="blocks"

.. note:: The ``filemapping`` value for this option is discouraged as it will consume a lot of memory for the scanning process when dealing with large files.

.. _configuring-yara-block:

``block`` Attribute
====================

Integer specifying the size in bytes of the buffer Yara will use to scan each file. The following multipliers can be suffixed to this number: K, M, G (for kilobyte, megabyte and gigabyte respectively).

.. code:: xml

    block="2M"

.. note:: One should be aware that if a rule needs a file in its entirety to find a match (such as the Hash module or the ``filesize`` variable), the size given by this attribute should be at least the file size or matches will become unreliable.

.. _configuring-yara-overlap:

``overlap`` Attribute
=====================

Integer specifying the size of the overlapping block created to scan for content that may match bytes in the region between two blocks. The following multipliers can be suffixed to this number: K, M, G (for kilobyte, megabyte and gigabyte respectively).

.. code:: xml

    overlap="4K"

.. _configuring-yara-timeout:

``timeout`` Attribute
=====================

Number of *seconds* after which the Yara engine will abort a file scan. This limit applies to each file individually.

.. code:: xml

    timeout="120"

