=========
ToolEmbed
=========

.. _Anchor-root-toolembed:

ToolEmbed is used to add resources (binaries, configuration files) to a DFIR ORC binary. It takes an XML configuration file as input.
To understand why this is needed and what happens when ``DFIR-Orc.exe`` is executed, please refer to :doc:`architecture`. A :doc:`tutorial <tuto>` presents how to configure and reconfigure binaries.

In daily life, when using a repository as `DFIR ORC configuration GitHub <https://github.com/dfir-orc/dfir-orc-config>`_, one can directly edit configuration files and run the script ``Configure.cmd``, which essentially sets a few environment variables and runs ToolEmbed. 

ToolEmbed is also able to extract all the resources from a configured binary, thanks to the ``/dump`` option. This can be useful to quickly edit a configuration and obtain a new configured binary.The :doc:`tutorial<tuto>` illustrates this scenario. 

The layout of the XML configuration file is as follows:

| <`toolembed <#toolembed-toolembed-element>`_ attributes="..." >
|    <`input <#toolembed-input-element>`_ > *value* </input>
|    <`output <#toolembed-output-element>`_ > *value* </output>
|    <`run <#toolembed-run-element>`_ attributes="..."></run>
|    <`run32 <#toolembed-run32-element>`_ attributes="..."></run32>
|    <`run64 <#toolembed-run64-element>`_ attributes="..."></run64>
|    <`file <#toolembed-file-element>`_ attributes="..." />
|    <`pair <#toolembed-pair-element>`_ attributes="..." />
|    <`archive <#toolembed-archive-element>`_ attributes="..." >
|        <`file <#toolembed-archive-file-element>`__ attributes="..." />
|    <`/archive <#toolembed-archive-element>`_>
| <`/toolembed <#toolembed-toolembed-element>`_>


Here is a typical ToolEmbed configuration file.

.. code:: xml

    <toolembed>
        <input>.\tools\DFIR-Orc_x86.exe</input>
        <output>.\output\DFIR-Orc.exe</output>

        <run32 args="WolfLauncher">self:#</run32>
        <run64 args="WolfLauncher">7z:#Tools|DFIR-Orc_x64.exe</run64>

        <file name="WOLFLAUNCHER_CONFIG" path=".\config\DFIR-ORC_config.xml"/>

        <file name="GetHives_config.xml" path=".\config\GetHives_config.xml"/>
        <file name="GetUserHives_config.xml" path=".\config\GetUserHives_config.xml"/>
        <file name="GetSamHive_config.xml" path=".\config\GetSamHive_config.xml"/>
        <file name="GetEvents_config.xml" path=".\config\GetEvents_config.xml"/>
        <file name="NTFSInfo_config.xml" path=".\config\NTFSInfo_config.xml"/>
        <file name="NTFSInfoHashPE_config.xml" path=".\config\NTFSInfoHashPE_config.xml"/>
        <file name="FatInfo_config.xml" path=".\config\FatInfo_config.xml"/>
        <file name="FatInfoHashPE_config.xml" path=".\config\FatInfoHashPE_config.xml"/>
        <file name="GetArtefacts_config.xml" path=".\config\GetArtefacts_config.xml"/>
        <file name="GetYaraSamples_config.xml" path=".\config\GetYaraSamples_config.xml"/>
        <file name="ruleset.yara" path=".\config\ruleset.yara"/>

        <archive name="Tools" format="7z" compression="Ultra">
            <file name="DFIR-Orc_x64.exe" path=".\tools\DFIR-Orc_x64.exe"/>
            <file name="autorunsc.exe" path=".\tools\autorunsc.exe"/>
        </archive>
    </toolembed>


-----
Usage
-----

There are two  most classical ways to use ToolEmbed:

*  The following command allows to obtain a configured binary, using an XML configuration file specifying all necessary elements.

.. code:: bat
    
    DFIR-Orc.exe ToolEmbed /config=DFIR-Orc_embed.xml

* The line below allows to extract resources from a configured binary in a directory of choice.

.. code:: bat

    DFIR-Orc.exe ToolEmbed /dump=Configured-binary.exe /out=dump-dir\

.. _toolembed-toolembed-element:

``toolembed`` Element
=====================

*optional=no, default=N/A*

Root element.

`Back to Root <#anchor-root-toolembed>`_

.. _toolembed-input-element:

``input`` Element, ``/input=<Path>`` Option
===========================================

*optional=no except with /dump option, default=N/A*

This element contains the path to the binary which ToolEmbed uses as a **Mothership** (see :ref:`here<architecture-config-process>`).
This base is augmented with new resources to create the output of ToolEmbed.
This input file remains unmodified by ToolEmbed.
Environment variables will be substituted.

The element is compulsory in an XML configuration file, and during a configuration operation. On the contrary, when dumping resources from a configured binary, it is irrelevant.

Example
-------

.. code:: xml

    <input>.\tools\DFIR-Orc_x86.exe</input>

 
`Back to Root <#anchor-root-toolembed>`_

.. _toolembed-output-element:

``output`` Element, ``/out=<Path>`` Option
==========================================

*optional=no, default=N/A*

This element contains the path to the output file created by ToolEmbed.
It is first created as a copy of the input file and, then, the specified resources are added.
Environment variables will be substituted.

For details on the ``output`` element syntax, please refer to the :doc:`output documentation <configuring_tool_output>`.

Example
-------

.. code:: xml

    <output>.\output\DFIR-Orc.exe</output>


`Back to Root <#anchor-root-toolembed>`_

.. _toolembed-run-element:

``run`` Element, ``/run=<Ressource>`` Option
================================================

*optional=yes, default=N/A*

This element specifies the unconfigured binary which should run. See :doc:`architecture` for details.
This element can be overridden by ``run32`` or ``run64`` elements (or options).

Attributes
----------
* **args** *(optional=yes, default=N/A)*
    The optional ``args`` attribute allows the addition of arguments. This yields a command line starting with the specified binary, followed by the optional args, then potentially followed by arguments passed on by Mothership.

Example
-------

.. code:: xml

    <input>.\tools\DFIR-Orc_x86.exe</input>
    ...
    <run args="WolfLauncher">self:#</run>

This example results in the Mothership binary relaunching itself with the added argument "WolfLauncher" (which results in the execution of the code of WolfLauncher, the scheduler for DFIR ORC).
Notation ``self:#`` and resources are documented in :doc:`resources`.

`Back to Root <#anchor-root-toolembed>`_

.. _toolembed-run32-element:

``run32`` Element, ``/run32=<Ressource>`` Option
================================================

*optional=yes, default=N/A*

This element specifies the unconfigured binary which should run on 32-bit platforms. See :doc:`architecture` for details.
When specified this element overrides a ``run`` element (or option).

Attributes
----------
* **args** *(optional=yes, default=N/A)*
    The optional ``args`` attribute allows the addition of arguments. This yields a command line starting with the specified binary, followed by the optional args, then potentially followed by arguments passed on by Mothership.

Example
-------

.. code:: xml

    <input>.\tools\DFIR-Orc_x86.exe</input>
    ...
    <run32 args="WolfLauncher">self:#</run32>

This example results in the Mothership binary relaunching itself with the added argument "WolfLauncher" (the scheduler for DFIR ORC).
Notation ``self:#`` and resources are documented in :doc:`resources`.

`Back to Root <#anchor-root-toolembed>`_

.. _toolembed-run64-element:

``run64`` Element, ``/run64=<Ressource>`` Option
================================================

*optional=yes, default=N/A*

This element specifies the unconfigured binary which should run on 64-bit platforms. See :doc:`architecture` for details.
When specified this element overrides a ``run`` element (or option).

Attributes
-----------
* **args** *(optional=yes, default=N/A)*
    The optional ``args`` attribute allows the addition of an argument (before all transmitted arguments)

Example
-------

.. code:: xml

    <run64 args="WolfLauncher">7z:#Tools|Orc_x64.exe</run64>

This example results in the launch of ``Orc_x64.exe`` contained in the 7z archive Tools, with the added argument "WolfLauncher" (the scheduler for DFIR ORC).
Notation ``7z:#Tools`` and resources are documented in :doc:`resources`.

`Back to Root <#anchor-root-toolembed>`_

.. _toolembed-file-element:

``file`` Element, ``/AddFile=<Path>,<Name>`` Option
===================================================

*optional=yes, default=N/A*

The file element provides a simple way to embed a file as a resource in the destination binary.

Attributes
-----------

* **name** *(optional=no, default=N/A)*
    The name of the resource to be created in the target binary
* **path** *(optional=no, default=N/A)*
    The path to the file to be added to the resource

Example
-------

.. code:: xml

   <file name="WOLFLAUNCHER_CONFIG" path=".\config\DFIR-ORC_config.xml"/>

This creates a resource named WOLFLAUNCHER_CONFIG which contains the ``.\config\DFIR-ORC_config.xml`` file.
On a command line, the equivalent resource is created by using ``/AddFile=.\config\DFIR-ORC_config.xml,WOLFLAUNCHER_CONFIG``. 

`Back to Root <#anchor-root-toolembed>`_

.. _toolembed-pair-element:

``pair`` Element, ``/name=<Value>`` Option
==========================================

*optional=yes, default=N/A*

This element is used internally to allow a level of indirection between a tool binary code and the configured resources.
This should not be necessary in a user-created configuration.

Attributes
-----------
* **name** *(optional=no, default=N/A)*
    The name of the resource
* **value** *(optional=no, default=N/A)*
    The string value of the resource.
    
Example
-------

.. code:: xml

    <pair name="XMLLITE_X86DLL" value="7z:#Tools|xmllite.dll" />

This line creates a resource named XMLLITE_X86DLL which contains the string "7z:#Tools|xmllite.dll".

`Back to Root <#anchor-root-toolembed>`_

.. _toolembed-archive-element:

``archive`` Element
===================

*optional=yes, default=N/A*

The archive element provides the ability to embed files in a resource but in a compressed archive (to minimize the size of the resulting binary). This element is a container for ``file`` sub-elements used to define the archive (see below).

This mechanism is deemed too complex to be described on a command line, there is no equivalent option. To use it, an XML configuration file must be passed as an argument through the ``/config`` option. 

Attributes
----------

* **name** *(optional=no, default=N/A)*
    The name attribute is the name of the resource to be created in the target binary
* **format** *(optional=no, default="cab")*
    The archive format to use to archive the files. Allowed values are:

    * cab
    * zip
    * 7z

* **compression** *(optional=yes, default="fast")*
    The level of compression in the archive (for zip and 7zip format). Supported values are:

    * None
    * Fastest
    * Fast
    * Normal
    * Maximum
    * Ultra

Example
-------

.. code:: xml

    <archive name="Tools" format="7z" compression="Ultra">
            ...
    </archive>

This creates a resource in the output file named "Tools" in the 7zip archive file format.

`Back to Root <#anchor-root-toolembed>`_

.. _toolembed-archive-file-element:

``file`` Element (in ``archive``)
=================================

The ``file`` element provides a simple way to embed a file in an archive in the configured binary.

Attributes
-----------

* **name** *(optional=no, default=N/A)*
    The name attribute is the name of the resource to be created in the target binary
* **path** *(optional=no, default=N/A)*
    The file system path to the file to be added to the resource relative to the current directory.

Example
-------

.. code:: xml

    <archive name="Tools" format="7z" compression="Ultra">
        <file name="DFIR-Orc_x64.exe" path=".\tools\DFIR-Orc_x64.exe"/>
        <file name="autorunsc.exe" path=".\tools\autorunsc.exe"/>
    </archive>

This creates a resource named "Tools" in the 7zip file format. This archive will contain two files:

* ``DFIR-Orc_x64.exe`` copied from ``.\tools\DFIR-Orc_x64.exe``
* ``autorunsc.exe`` copied from ``.\tools\autorunsc.exe``

These paths are relative to the directory where ``DFIR-Orc.exe toolembed`` is launched.

`Back to Root <#anchor-root-toolembed>`_

``/dump[=<Path>]`` Option
=========================

*optional=yes, default=N/A*

This option allows to extract the resources from a configured binary (stored at the given path), in a directory specified using ``/out``.
This option has no equivalent XML element, it just exists as a switch to revert the behavior of ToolEmbed, and when extracting resources no configuration file is needed.

.. code:: bat
    
    DFIR-Orc.exe toolembed /dump=DFIR-Orc-1.exe /out=dumpdir\

This command writes the unconfigured binaries and configurations embedded in ``dumpdir\``.

If this option is used without specifying a ``<Path>``, the resources of the executed DFIR ORC binary itself are dumped.

.. code:: bat
    
    DFIR-Orc.exe toolembed /dump /out=dumpdir\
