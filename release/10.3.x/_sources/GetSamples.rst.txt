
==========
GetSamples
==========

Description
===========

GetSamples was developed to add automatic sample collection. DFIR ORC collects multiple artefacts, which in turn allow the analyst to pivot and determine which files to examine.  GetSamples was created to identify and collect these files beforehand, to minimize the chances of having to get back to the analyzed system.

Typically, targets include binaries registered in *ASEP* (AutoStart Extension Points), startup folders, loaded in processes, etc.


.. important::

    GetSamples is **not** an automated malicious files collection tool. It is, however, an automated collection tool that could happen to collect a malicious file because it matched the collection heuristics.

GetSamples goes through 3 distinct steps.

#. Determine a list of candidate binaries

    * by using ``autorunsc.exe`` from SysInternals,
    * by enumerating loaded binaries (processes and their loaded modules), and
    * by enumerating loaded drivers.

#. Apply collection heuristics:

    * Currently, the only heuristic is to exclude signed binaries (we welcome submissions to improve here).

#. Generate a :doc:`GetThis <GetThis>` configuration file and run the tool.


Output
======

.. note::

    For verbose logging output refer to :doc:`Configuring Console Output <configuring_console_output>`.


Usage
=====

GetSamples can be used from the command line, using options or an XML configuration file. Such a file can also be embedded in a configured binary. Command-line switches and XML configurations provide (mostly) identical access to the functionalities of GetSamples, even if the configuration files allow for more complexity.  

* Example of command-line parameters:

.. code:: bat

    DFIR-Orc.exe GetSamples /MaxPerSampleBytes=16MB /MaxTotalBytes=512MB /MaxSampleCount=200000 /out=GetSamples.7z

* Example of XML configuration file:

.. code:: xml

    <GetSamples>
        <Output>GetSamples.7z</Output>
        <Samples MaxPerSampleBytes="16MB" MaxTotalBytes="512MB" MaxSampleCount="200000" />
    </GetSamples>

The XML configuration file is provided by using the parameter ``/config``:

.. code:: bat

    DFIR-Orc.exe GetSamples /config=GetSamples.xml

.. note::

    All output-related parameters (in the configuration file and on the command line) can use environment variables.


``GetSamples`` Element
----------------------

*optional=no, default=N/A*

Root element.

Attributes
``````````
* **nolimits** *(optional=yes, default=Inactive)*, ``/nolimits`` option:
    Specifies that there should be no limit when collecting the samples. The option ``/nolimits`` takes no value. In an XML file, the attribute is written ``nolimits=""``. 

.. important:: Since GetSamples relies on GetThis, the same constraint on limits exists in both tools: limits or their absence **have to be specified** for the tool to run. This can either be done using the ``nolimits`` attribute or option, or by setting upper limits in the ``samples`` element.


``Output`` Element, ``/out=<Path>`` Option
------------------------------------------

*optional=no, default=N/A*

Configures where the samples get stored. It silently relies on :doc:`GetThis <GetThis>` using a dynamically generated configuration.

The syntax is similar to the ``output`` element or ``/out`` option used in other tools, described in the :doc:`output documentation <configuring_tool_output>`.

This is mandatory: if no ``output`` element (or ``/out`` option) is specified, no sample will be collected.


``SampleInfo`` Element, ``/SampleInfo=<Path>`` Option
-----------------------------------------------------

*optional=yes, default=N/A*

This triggers the collection of information about samples in a file, such as:
    * whether the considered binary is signed and if its signature is verified, 
    * whether the binary was loaded,
    * whether the binary is listed in an ASEP (AutoStart Extension Points), and
    * whether the binary is currently part of a running process (or a started driver).

The syntax is similar to the ``output`` element or ``/out`` option **for a file output**, described in the :doc:`output documentation <configuring_tool_output>`. Only CSV format is supported.

Example:

.. code:: xml
    
    <sampleinfo encoding="utf16">Output.csv</sampleinfo>


``TimeLine`` Element, ``/TimeLine=<Path>`` Option
-------------------------------------------------

*optional=yes, default=N/A*

This triggers the collection of timeline-related information for loaded modules. The file contains
    * the time of creation (if available),
    * the ProcessId loading the modules,
    * the ParentId of the process (if available), and
    * the module file name.

The syntax is similar to the ``output`` element or ``/out`` option **for a file output**, described in the :doc:`output documentation <configuring_tool_output>`. Only CSV format is supported.

Example:

.. code:: xml
    
    <timeline encoding="utf8">Timeline.csv</timeline>



``Samples`` Element
-------------------

*optional=no (ignored if nolimits has been specified), default=N/A*

Describes the samples to collect limitations.

Attributes
``````````

* **MaxSampleCount** *(optional=see warning, default=N/A)*, ``/MaxSampleCount="<Integer>"`` Option:
    Maximum number of matching files to be collected. This value is an integer.

* **MaxPerSampleBytes** *(optional=see warning, default=N/A)*, ``/MaxPerSampleBytes="<Integer>"`` Option:
    Collects matching files smaller than the specified size. The expected value is an integer that can be followed by one of these units: *B, KB, MB, GB*. This attribute cannot be the only limiting attribute to be set.

* **MaxTotalBytes** *(optional=see warning, default=N/A)*, ``/MaxTotalBytes="<Integer>"`` Option:
    Matching files are collected until their uncompressed cumulated file size reaches the specified value. The expected value is an integer that can be followed by one of these units: *B, KB, MB, GB*.

.. warning::
    Limits must be explicitly set, either by using ``nolimits`` or by using a meaningful combination of attributes of ``samples``. 


``Autoruns`` Element, ``/Autoruns[=<Path>]`` Option
---------------------------------------------------

*optional=yes, default=N/A*

This option has multiple purposes but it is mainly used to make *DFIR ORC* execute and store *Autoruns* results.

Here is the complete usage of *Autoruns*:

- ``<Autoruns></Autoruns>`` or ``/Autoruns``: extracts and runs *autorunsc.exe* to collect *ASEP* (AutoStart Extension Points) information.
- ``<Autoruns>$path</Autoruns>`` or ``/Autoruns=<path>``:
    - If the specified XML file exists, the file is loaded and used to generate the configuration for GetThis instead of running autoruns.
    - If the file does not exist, ``autorunsc.exe`` is run and its XML output is placed in the specified file.

.. important::

  To be able to execute *SysInternals Autoruns*, ``DFIR-Orc.exe`` must have embedded it when prepared with :doc:`ToolEmbed <ToolEmbed>` (see :ref:`Archive <toolembed-archive-element>` element).


``GetThisConfig`` Element, ``/GetThisConfig=<Path>`` Option
-----------------------------------------------------------

*optional=yes, default=N/A*

The configuration file generated for GetThis is output. This will be used to store the dynamically generated XML file provided to GetThis. It can be examined later.

Example:

.. code:: xml

    <GetThisConfig>GetThisConfig.xml</GetThisConfig>


``GetThisArgs`` Element, ``/GetThisArgs="<Arg1 Arg2 ...>"``
-----------------------------------------------------------

*optional=yes, default=N/A*

Command-line arguments to be forwarded to GetThis.

Example:

.. code:: xml

    <GetThisArgs>/flushregistry /nolimits</GetThisArgs>


``TempDir`` Element, ``/TempDir=<Path>``
----------------------------------------

*optional=yes, default=N/A*

The specified directory must be used to store temporary files.

See :doc:`the command-line documentation <cli_options>`.

Example:

.. code:: xml

    <TempDir>D:\Temp</TempDir>


``NoSigCheck`` Element, ``/NoSigCheck`` Option
----------------------------------------------

*optional=yes, default=N/A*

Does not check sample signatures (those returned by *autoruns* output will still be checked).

Example:

.. code:: xml

    <NoSigCheck/>
