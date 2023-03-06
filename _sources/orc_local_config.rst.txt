=================================
DFIR ORC Local Configuration File
=================================

DFIR ORC can be locally configured to specify a limited set of configuration elements. Typically, those elements are the client's specific configuration options (like the upload method, priority, temporary folder, etc.). The local configuration can be specified using:


    - The ``/local=<LocalConfigFile>`` command-line option
    - A file in the same directory as DFIR ORC, with the same base name and .xml extension, e.g.:

        - ``<SomeDirectory>\\DFIR-Orc.exe``
        - ``<SomeDirectory>\\DFIR-Orc.xml``

.. _anchor-root:

The index of this sections consists in the following XML skeleton file, which features all the elements that can appear
in a real configuration file.
It is not a usable configuration, in the sense that it does not contain any attribute key or value, and can exhibit incompatible elements.
Its point is to be exhaustive from the point of view of existing usable elements.

| <`dfir-orc <#dfir-orc-element>`_ *attributes="..."*>
|      <`temporary <#temporary-element>`_> *value* <`/temporary <#temporary-element>`_>
|      <`output <#output-element>`_> *value* <`/output <#output-element>`_>
|      <`upload <#upload-element>`_ *attributes="..."* />
|      <`recipient <#recipient-element>`_ *attributes="..."*> *value* <`/recipient <#recipient-element>`_>
|      <`key <#key-element>`_> *value*  <`/key <#key-element>`_>
|      <`enable_key <#enable-key-and-disable-key-elements>`_> *value* <`/enable_key <#enable-key-and-disable-key-elements>`_>
|      <`disable_key <#enable-key-and-disable-key-elements>`_> *value* <`/disable_key <#enable-key-and-disable-key-elements>`_>
|      <`log <#log-element>`_ *attributes="..."> *value* <`/log <#log-element>`_>
| <`/dfir-orc <#dfir-orc-element>`_>

.. _orc_local_config-dfir-orc-element:

``dfir-orc`` Element
====================

*optional=no, default=N/A*

Root element

Attributes
----------

* **priority** *(optional=yes, default=normal)*
        Configures Windows process (and thread) priority class. Available values for this attribute are: Low, Normal & High.
* **powerstate** *(optional=yes, default=unmodified power state)*
        Configures DFIR ORC's main thread power state to optionally prevent the system from going to sleep when DFIR ORC is running. Allowed value is a comma separated list of

        * SystemRequired
        * Displayrequired
        * UserPresent
        * AwayMode.

        When only looking to prevent sleep, recommended value for this option is SystemRequired,AwayMode.
        More information on power states: https://docs.microsoft.com/en-us/windows/desktop/api/winbase/nf-winbase-setthreadexecutionstate

`Back to Root <#anchor-root>`_

.. _orc_local_config-temporary-element:

``temporary`` Element
=====================

*optional=yes, default=%temp%*, `parent element: dfir-orc <#dfir-orc-element>`_

This element configures the location of temporary files created by the tool. The inner text of this element contains the name of the folder. Environment variables will be substituted.

Attributes
----------

None

Example
-------

.. code:: xml

  <temporary>%Temp%\WorkingTemp</temporary>

`Back to Root <#anchor-root>`_

.. _orc_local_config-output-element:

``output`` Element
==================

*optional=no, default='.'*, `parent element: dfir-orc <#dfir-orc-element>`_

This element configures the folder where the various archives will be created. A local drive or a remote SMB share can be specified (in the latter, the upload syntax should be privileged to reduce network congestion). Environment variables will be substituted.

Attributes
----------

None

Example
-------

.. code:: xml

  <output>%Temp%</output>


`Back to Root <#anchor-root>`_


.. _orc_local_config-upload-element:

``upload`` Element
==================

*optional=yes, default=no upload*, `parent element: dfir-orc <#dfir-orc-element>`_

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


.. _orc_local_config-recipient-element:

``recipient`` Element
=====================

*optional=yes, default=N/A*, `parent element: dfir-orc <#dfir-orc-element>`_

The recipient element is used to create the list of recipients able to open the enveloped CMS archives. It basically consists of a list of encoded certificates. This element is used to add a recipient's certificate to the list of possible recipients for individual archives. This element implies encryption of the archives specified in its compulsory archive attribute.

Attributes
----------

* **name** *(optional=no, default=N/A)*
        Name of the recipient
* **archive** *(optional=no, default=Does not encrypt any archive)*
        Comma separated list of archive keyword specs to match against archive names. Specifies one or more archives encrypted in a CMS PKCS#7 message (cf http://tools.ietf.org/html/rfc2315 )

Example
-------

.. code:: xml

  <recipient name='certfr' archive='*' >
    -----BEGIN CERTIFICATE-----
    MIIC7TCCAdmgAwIBAgIQR5AF92Ti8qtEwuT3PMVrJzAJBgUrDgMCHQUAMBIxEDAO
    BgNVBAMTB0NFUlQtRlIwHhcNMDQxMjMxMjIwMDAwWhcNMTQxMjMxMjIwMDAwWjAS
    MRAwDgYDVQQDEwdDRVJULUZSMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKC
    AQEAiufyRATXw5Kc/DUcEr/5nNygcbluyS5gkUd1pGaUqKHMSMEVOBzYqcvq3cMw
    4shAL3TSgYdoOJaLG4ErvyRU87fWYRcwiHzGdFg89E3pBEWnyV3j3fR0fVB5t3MD
    jbooTGI/qQGl1l3MZ+bOiHkYcIG50R5343VT5vjRLmPv16iopGczLXKkNFxN480f
    BnCF8HcJesFiMIDUI+d9OWpLJNDSCerouMr75HVD47+gBKKgH2PrxWozk2L6R9gQ
    l8/6xzM4VKiNt4BTGfChG8AnO8sJzPETjJaDXrIGaYVLxU4OxFh/a9x61dlM/5A/
    TASXpLhXrsi+ib3YLLl+pNh+aQIDAQABo0cwRTBDBgNVHQEEPDA6gBD47GaJKs91
    qsThQIQ7f8Y5oRQwEjEQMA4GA1UEAxMHQ0VSVC1GUoIQR5AF92Ti8qtEwuT3PMVr
    JzAJBgUrDgMCHQUAA4IBAQBgvEE7qyLVV+Y5B0sR5VuPmfeqakOxBxLmb8VoTNKn
    /7ai1XwtJeWD1vumKx5Q29GiUfVhvBgn0zhjM5syVDFCqEcp+eu6l2XbN8uvllCY
    daTOT/9UylLxu1L/epiWiYtqRZOO/9i1fyqrkguIww7EjXXT3ybL5U/BakEC2Yg5
    6vUoxbo2EbA1UoMWurRxYNYxyFfHpvBYXFf4uDaAFIVMtEgH5VkKyM3Kj2hi/PJH
    /a30ndTWVSY/82hoRGCa+SkevR5VbDsxTqHtEHys4K+ETVTNXp29HwG+1YG7BTTc
    4VdFRqUm7e3o6VUArFar8I01oHiHzqKJiu1Omm2Fkmc1
    -----END CERTIFICATE-----
  </recipient>


`Back to Root <#anchor-root>`_

.. _orc_local_config-key-element:

``key`` Element
===============

*optional=yes, default=N/A*, `parent element: dfir-orc <#dfir-orc-element>`_

The key element allows to select only specific commands to be executed or archives to be generated. All non-matching keywords or archives are not executed or generated. This element is exclusive with ``enable_key`` and ``disable_key``.

Attributes
----------

None

Example
-------


.. code:: xml

  <dfir-orc>
    <key>ORC_Quick</ key>
    <key>GetRam_winpmem1,Flashback</key>
  </dfir-orc>


`Back to Root <#anchor-root>`_

.. _orc_local_config-enable-key-and-disable-key-elements:

``enable_key`` and ``disable_key`` Elements
===========================================

*optional=yes, default=N/A*, `parent element: dfir-orc <#dfir-orc-element>`_

The ``enable_key`` element will enable an optional archive or command (cf. `archive element <wolf_config.html#the-archive-element>`_ , `command element <wolf_config.html#command-element>`_).
The ``disable_key`` element will disable an archive generation or command execution. Elements ``enable_key`` and ``disable_key`` can be combined and repeated. All ``enable_key`` elements take effect before the ``disable_key`` elements. Keywords are case insensitive. The data in the element can be a comma separated list of keywords.

Attributes
----------

None

Example
-------


.. code:: xml

  <dfir-orc>
      <disable_key>DFIR-ORC_Detail</disable_key>
      <enable_key>GetRam_winpmem1</enable_key>
  </dfir-orc>

`Back to Root <#anchor-root>`_


.. _orc_local_config-log-element:

``log`` Element
===============

*optional=yes, default=N/A*, `parent element: dfir-orc <#dfir-orc-element>`_

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
