============
Architecture
============

.. _architecture-config-process:

Configuration Process
=====================

The **ultimate objective** of using DFIR ORC is to create a single binary file that orchestrates complex collection tasks on a system, optionally protect the result with encryption and, finally, upload them to a central collection point (SMB share, BITS server).

Compiling the source code for DFIR ORC yields what is called **unconfigured binaries**, typically named ``DFIR-Orc_x86.exe`` and ``DFIR-Orc_x64.exe``.
These binaries contain the :doc:`embedded specific tools <embedded_tool_suite>` developed as part of this project.
However, as explained in :doc:`design_principles`, the framework is meant to build a single binary, embedding **external** tools and the whole
list of data to collect. The process of creating such a binary is called **configuring DFIR ORC**. It results in a **configured binary**, typically called ``DFIR-Orc.exe``.

The configuration process takes as inputs:

* optionally, a set of external tools (from your own toolset, from Sysinternals, etc.),
* a :doc:`WolfLauncher configuration <wolf_config>` defining the collection commands to execute and their expected results,
* the configuration files needed for the tools (both external and from the pre-embedded suite) to run the commands listed in the WolfLauncher configuration file,
* an :doc:`Embed configuration <ToolEmbed>` to specify how the files listed above should be embedded in the resulting *configured binary*,
* a **Mothership**, typically ``DFIR-Orc_x86.exe`` that will be the "base" from which the configured binary is created. The Mothership is the first code to run when the configured binary is launched.

Once all these inputs are gathered, running the following :doc:`ToolEmbed <ToolEmbed>` command creates a configured binary:

.. code:: bat

    DFIR-Orc_x64.exe ToolEmbed /config=Embed.xml /out=DFIR-Orc.exe

Once the configured binary is created, it is ready for testing and, then, deployment.

To try it on a relevant set of configurations, please refer to the GitHub repository dedicated to configurations: https://github.com/dfir-orc/dfir-orc-config/.

.. _architecture-tools-cli:

Tools Invoked Directly From Command-line
========================================

Above, we go over the configuration process. It should clarify the difference between the embedded tool suite,
present in both configured and unconfigured binaries, and the external tools which only configured binaries can embed.

In the embedded suite, some tools are basic, such as NTFSUtil or DD, others are more complex, like WolfLauncher.

Each tool is usable through the configured and unconfigured binaries.
For instance, :doc:`NTFSUtil <NTFSUtil>` can enumerate the file systems present on the live system, with the command:

.. code:: bat

    DFIR-Orc_x64.exe NTFSUtil /enumlocs

:doc:`NTFSInfo <NTFSInfo>` lists the files and directories of an NTFS volume with the command:

.. code:: bat

    DFIR-Orc_x64.exe NTFSInfo /out=%temp%\test.csv c:\

:doc:`GetThis <GetThis>` collects the system software hive with:

.. code:: bat

    DFIR-Orc_x64.exe GetThis /nolimits /sample=SOFTWARE /out=%temp%\hive.7z c:\

Most tools can be configured for more advanced scenarios (like YARA rules, complex filters or search criteria) with XML configuration files.
The documentation for every embedded tool can be found :doc:`here <embedded_tool_suite>`.


.. _architecture-deployment-spe-conf:

Deployment-specific Configuration
=================================

Each DFIR ORC deployment requires its own set of parameters and settings suited to the targeted installed base (upload method, temporary folder, etc.).
To adapt a configured binary to these specifics, a :doc:`local configuration file <orc_local_config>` can be used.
Of course, :doc:`command-line options <cli_options>` also work.

All these configuration files and options are evaluated by a configured binary, ``DFIR-Orc.exe``, in the following order:

.. image:: _static/orc_configuration_input.svg

.. note:: Some execution parameters can be overridden at each step of the configuration. For instance, ``temporary`` (which specify the temporary working folder) can be defined in the WolfLauncher configuration, then overridden by the local configuration file and, finally, modified by a command-line switch.

.. _architecture-exec:

DFIR ORC Execution
==================

As explained in :doc:`platforms`, most DFIR ORC collection tasks involving the NTFS Master File Table parser (NTFSInfo, GetThis) require administrative privilege to execute successfully.

.. warning:: Administrative privilege is always requested when DFIR ORC is executed. If absent, a UAC elevation prompt may be triggered depending on the system configuration.

As seen `above <#dfir-orc-configuration-process>`_, the first code to run when a configured binary runs is called the **Mothership**.
As 64-bit platform can run 32-bit code but not the other way around, ``DFIR-Orc_x86.exe`` is the usual choice.


.. warning:: The execution sequence documented below corresponds to the usual configuration, such as the example set originally proposed in `the GitHub repository <https://github.com/dfir-orc/dfir-orc-config>`_. Fiddling with ``Embed.xml`` and :doc:`ToolEmbed` can change what happens.

The goal of a configured binary is to launch the architecture-appropriate DFIR ORC with the ``WolfLauncher`` argument. This argument launch an embedded tool, WolfLauncher, that is the command scheduler.

DFIR ORC on 32-bit Systems
---------------------------

On 32-bit systems, the configured binary is "native" to the architecture. Thus, the Mothership (here ``DFIR-Orc_x86``) can simply reexecute itself with the ``WolfLauncher`` as shown in the figure below.
Depending on what is specified in the :doc:`WolfLauncher configuration file <wolf_config>`, it will then launch embedded tools and/or external tools to proceed with the data collection.

.. image:: _static/orc_execution_x86.svg

DFIR ORC on 64-bit Systems
---------------------------

On 64-bit systems, the Mothership not being "native" to these systems, the extraction of ``DFIR-Orc_x64.exe`` is required.
It is followed by the execution of ``DFIR-Orc_x64.exe WolfLauncher``.
Depending on what is specified in the :doc:`WolfLauncher configuration file <wolf_config>`, it will then launch embedded tools and/or external tools to proceed with the data collection.

.. image:: _static/orc_execution_x64.svg

DFIR ORC can look up and use resources from its parent and grandparent processes (i.e. the Mothership and/or WolfLauncher) without having to extract them.
This avoids unnecessary file extraction to disk and allows direct use of these resources from the children tasks.
This process is typically used for 64-bit systems since resources are not available in the subprocesses but only in the Mothership binary.
