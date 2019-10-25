Design Principles
=================

The Approach: One Binary to Run Them All
----------------------------------------

DFIR ORC was originally developed to address the need for reliable data collection on potentially compromised systems.
Historically, teams have been using two approaches:

* a script executing a collection of ad hoc tools one after the other,
* a monolithic tool gathering as much data possible from available APIs.

The first approach is very prone to failures if any of the tools fails, hangs, or expects user input for some reason.
It thus puts in jeopardy the complete set of collected data.
Moreover, these tools usually create a huge amount of data on disk before being able to archive or compress the whole result set in one file.
On the plus side, this approach benefits from the wide variety of tools available to accomplish efficiently live data collection required in the various technological areas (file systems, networking, memory analysis, etc.).

The second approach (monolithic) is prone to application crashes and represents an enormous amount of "reinventing the wheel".
It also carries the burden of having to integrate various tools and libraries into the same address space.
This approach, however, allows to completely control the output format for fast and meaningful data mining.

DFIR ORC takes the best of both worlds: it reuses existing or independent tools and unites them under the management of an execution engine that allows more control. Moreover, a set of specialized tools has been developed and can also be embedded.
Typically, all data-gathering activities will run under the control of a Windows Job Object putting a strict control on their execution.
Processes output data which is immediately compressed into the output file, to minimize the disk usage and churn.Whenever possible, the output will be added to the archive ASAP and deleted to minimize use of temporary files.


.. admonition:: The main design motto behind DFIR ORC
   :class: information

   **Whatever it takes, whatever happens, DFIR ORC will strive to provide valid output files in a predetermined amount of time.**

Choosing Your Arsenal: Tools to Embed
-------------------------------------

DFIR ORC can embed other tools to create a unique file that will be executed on the target systems.

The first step is to define your data collection goals, to choose appropriate tools to run on machines.

* What data do you need to collect?

    * File system related data (file lists, hashes, file signatures, …)
    * Registry
    * Live data: processes, network communications, kernel objects,
    * System configuration (network, ASEPs, …)
    * Logs, events

* What are the target platforms?

    * Obsolete platforms (XP? Vista?)
    * Modern platforms (8.1? 10?)

* How sensitive and/or personal is this information?

Next, you need to define and assemble the set of tools required to collect this information from the targeted systems.

* From DFIR ORC itself with the embedded tool set:

    * NTFSInfo,
    * FATInfo,
    * GetThis,
    * RegInfo,
    * USNInfo,
    * ObjInfo,
    * FastFind,
    * NTFSUtil,
    * GetSectors,
    * DD

* From third parties:

    * SysInternals Tools Suite (autoruns, …),
    * Tcpdump,
    * …

The flexibility allowed by the configuration enables to consider tuning tools which:

    * only run on specific Windows version or architecture,
    * have different output or command line arguments on specific Windows versions,
    * require files to be available (configurations, dependencies, …) upon execution.

A Configurable Framework
------------------------

DFIR ORC is configurable. On top of the embedded tools, the operational binary ``DFIR-Orc.exe`` embeds
an XML configuration listing all the tools to run and their options. This is the reason why we call ``DFIR-Orc.exe`` *a configured* binary.
To be able to write a valid configuration,
the exact command line required by each tool is needed, as well as a description of the intended output.

DFIR ORC also allows analysts to organize the data collected into one or more archives.
Anything can justify a choice of organization, e.g. the nature and sensitivity of the collected information.
We offer some ideas of criteria below.

* Sensitivity of information: typically, data containing sensitive information will be collected separately. DFIR ORC can encrypt each archive with a separate list of recipients. For each certificate of recipients provided, DFIR ORC will encrypt the session key. The PKCS#7 CMS standard is used to provide a cross-platform format for the encrypted file ;
* Pace and/or volume: you may want to have separate archives for quick and easy data and for long, slow, massive collection of information. This will enable a phased analysis of the data as it arrives.
* Analysis: if you delegate analysis to other teams, or collect data for other teams (potentially with a different need-to-know), you will organize this data in separate archives to ease the treatment process.
* Behavior: If a tool has known issues or is new to your arsenal, you may want to segregate its execution into a separate archive to enable the command engine to impose specific limitations.

