Tutorial
========

This tutorial details the steps to obtain a **configured** DFIR ORC binary ready for deployment. 

It explains which code to compile, how to embed a configuration, how to modify a configuration, the difference between compiling and configuring...
Basically, it goes through most of the classical steps which incident responders have to follow in their daily usage of the framework.


.. warning:: Everything must be done in a Microsoft Windows environment. Only step 1 requires compiling with Visual Studio (the free edition is sufficient, see step 1 for details).

   Unconfigured and configured binaries require administrative privileges.
   **Commands below are designed to be run in an elevated Powershell shell.** It can be adapted to work in an elevated command shell prompt.

.. contents:: List of the steps
   :local:
   


1. Build
--------

This step is the only one requiring actual compilation with Microsoft's toolchain. Instructions to compile these files from the source code are detailed `here <https://github.com/DFIR-ORC/dfir-orc/blob/master/README.md>`_.

Please follow this procedure before going further.

As is explained in the section :ref:`architecture-config-process`, compiling the source code for DFIR ORC yields what is called **unconfigured binaries**, typically named ``DFIR-Orc_x86.exe`` (32-bit) and ``DFIR-Orc_x64.exe`` (64-bit).
An *unconfigured* binary contains everything needed to orchestrate the collection of artefacts (e.g. what we call WolfLauncher, illustrated :ref:`here <architecture-exec>`).
It also contains the :doc:`embedded tool suite <embedded_tool_suite>` included by default.
Thus, it can behave kind of like the *busybox* tool, and be used *as is* to run embedded tools. In fact, it is exactly what WolfLauncher does when a configured binary is run.

.. important::

    As configured binaries, unconfigured binaries **require administrative privileges** for execution.

Mini-challenge 1
````````````````
This first step illustrates how to use unconfigured binaries to run the tools embedded by default.
Find a command line to use :doc:`NTFSUtil` to display information about the USN journal of disk ``C:``.

.. container:: toggle

    .. container:: header

        **Hint  ▶**
     
    ``NTFSUtil`` needs arguments ``/USN \\.\c:``

.. container:: toggle

    .. container:: header

        **Answer  ▶**
   
    Both command lines work. 

    .. code:: powershell

      .\DFIR-Orc_x86.exe NTFSUtil /USN \\.\c:
      .\DFIR-Orc_x64.exe NTFSUtil /USN \\.\c:


.. _tuto-step-2:

2. Configure
------------

.. note:: No compilation is required after step 1.

Why is a configuration needed? Basically, an *unconfigured* binary is just a set of tools, plus a collection engine. Hence, the list of
artefacts to be collected, and how to collect them, has not been provided yet. This list is precisely what a configuration is!
Please refer to the short section :ref:`architecture-config-process` to read about the basics.

This step details how to obtain a *configured* binary from an *unconfigured* binary and the `repository of existing configurations <https://github.com/dfir-orc/dfir-orc-config>`_. 

First, clone the default configuration:

.. code:: powershell
  
   git clone https://github.com/dfir-orc/dfir-orc-config.git
   cd dfir-orc-config

Then, copy the *unconfigured* DFIR ORC binaries ``DFIR-ORC_x86.exe`` and ``DFIR-ORC_x64.exe`` in the ``tools`` folder:

.. code:: powershell

    Copy-Item <Path>\dfir-orc\build-x86\MinSizeRel\DFIR-Orc_x86.exe .\tools
    Copy-Item <Path>\dfir-orc\build-x64\MinSizeRel\DFIR-Orc_x64.exe .\tools
    
To illustrate how to include external tools into the DFIR ORC framework, we have chosen to provide an example configuration which uses ``autorunsc.exe``. Hence, you need to `download it from the Microsoft SysInternals website <https://live.sysinternals.com/autorunsc.exe>`_.

.. code:: powershell

    Invoke-WebRequest https://live.sysinternals.com/autorunsc.exe -OutFile .\tools\autorunsc.exe

Finally, run the command below in an **elevated** command prompt:

.. code:: powershell

    .\Configure.cmd

This command yields a *configured* DFIR ORC binary (named ``DFIR-Orc.exe`` by default) in the ``output`` directory.

Mini-challenge 2
````````````````

In the configuration repository, which file describes the commands which WolfLauncher (the collection engine) is going to run when the *configured* binary is executed ?

.. container:: toggle

    .. container:: header

        **Hint  ▶**
    
    Track ``autorunsc.exe``, since you know it is supposed to be run.
    
.. container:: toggle

    .. container:: header

        **Answer  ▶**

    The main configuration file, or :doc:`WolfLauncher configuration <wolf_config>`, is ``DFIR-ORC_config.xml``. Basics to read and edit it are detailed in :ref:`tuto-step-5`.

3. Test the Configuration
-------------------------

Once we have a *configured* DFIR ORC binary, we can start testing it!

Of course, we can use it to execute one of the :doc:`embedded tools <embedded_tool_suite>` (just like the *unconfigured* ones): 

.. code:: powershell

    .\output\DFIR-Orc.exe NTFSInfo /out=C_drive.csv C:\

This command will create a file named ``C_drive.csv`` in the current directory with the enumeration of the Master File Table of the volume ``C:``.


In a similar manner, GetThis can be invoked from the command line:

.. code:: powershell

    .\output\DFIR-Orc.exe GetThis /nolimits /sample=ntdll.dll /out=ntdll.7z C:\

This command will create a file called ``ntdll.7z`` in the current directory, containing all files named ``ntdll.dll`` in the ``C:`` volume.

However, configurations were introduced so that users can write these command lines once and for all.

Once a tool is run, its results are stored in an archive.
The content of archives are set by the configuration file.
Given a *configured* binary, the option `keys` lists all the archives which can be built
according to the embedded configuration.

Let's try this on the binary obtained in step 2.

.. code:: powershell

    .\output\DFIR-Orc.exe /keys 

This command outputs the result below:

.. code:: powershell  

    DFIR-Orc Version 10.0.0.000

    Start time            : 09/26/2019 14:57:55.198 (UTC)

    Computer              : JEANGABOOK
    Full Computer         : jeangabook

    User                  : JEANGABOOK\Jean (elevated)

    System type           : WorkStation

    System tags           : OSBuild#18362,RTM,Release#1903,Windows10,WorkStation,x64
    Operating System      : Microsoft Windows 10 Enterprise Edition (build 18362), 64-bit
    Output   directory    : F:\Projects\dfir-orc-config (encoding=UTF8)
    Temp     directory    : C:\Users\Jean\AppData\Local\Temp\WorkingTemp (encoding=UTF8)
    Log file              : DFIR-ORC_WorkStation_jeangabook_20190926_145755.log
    Repeat Behavior       : No global override set (config behavior used)
    Priority              : Low

    [X] Archive: Main (file is DFIR-ORC_WorkStation_jeangabook_Main.7z)
            [X] Command SystemInfo
            [X] Command Processes
            [X] Command GetEvents
            [X] Command Autoruns
            [X] Command NTFSInfo
            [ ] Command NTFSInfoHashPE
            [X] Command FatInfo
            [ ] Command FatInfoHashPE
            [X] Command USNInfo
            [X] Command GetArtefacts

    [X] Archive: Hives (file is DFIR-ORC_WorkStation_jeangabook_Hives.7z)
            [X] Command GetSystemHives
            [X] Command GetUserHives
            [X] Command GetSamHive

    [ ] Archive: Yara (file is DFIR-ORC_WorkStation_jeangabook_Yara.7z)
            [X] Command GetYara


    Finish time           : 09/26/2019 14:57:55.198 (UTC)
    Elapsed time          : 0 msecs


After the usual banner with the tool running, version information and parameters, we get a list of configured archives (Main, Hives and Yara) and the list of commands which they comprise.

[X] indicates an archive (respectively a command) that will be collected (respectively run). 

[ ] indicates an option or command that can be added to the collection via the `/key+=Yara` for instance.

The result above shows that by default, the configuration
embedded in ``DFIR-Orc.exe``

   * collects an archive named Main by running all its commands except NTFSInfoHashPE and FatInfoHashPE,
   * collects an archive named Hives containing the outputs of all three commands listed for this archive,
   * does not collect the Yara archive.

It is possible to select and deselect keys using the syntax detailed in :ref:`the command line documentation <cli_options-keys>`. As illustrated in :ref:`architecture-deployment-spe-conf`, options on the command line change the behavior of a configured binary without impacting its embedded configuration file; the changes only take effect for one execution.

For example, the following line is meant to select the Yara archive, but deselect the SAM Hive collection included in the Hives archive. Adding `/keys` at the end of the line allows a dry run: it just outputs what is set to be collected by the entire command line.

.. code:: powershell

    .\output\DFIR-Orc.exe /key+=Yara /key-=GetSamHive /keys


Mini-challenge 3
````````````````

Write a command line allowing to only get the output of SystemInfo in the Main archive, in a folder
named ``\Temp\testing``.
Run the command to test that it works (SystemInfo is very quick).

.. container:: toggle

    .. container:: header

        **Hint  ▶**
    
    Options involved are ``/out`` and ``/key``. See :doc:`the command line documentation <cli_options>`.

    
.. container:: toggle

    .. container:: header

        **Answer  ▶**

    .. code:: powershell
       
       .\output\DFIR-Orc.exe /key=SystemInfo /out=\Temp\testing


Run the command line again. What does it do? Why? How can this behavior be corrected?

.. container:: toggle

    .. container:: header

        **Hint  ▶**
    
    Option ``/overwrite`` should help. See :doc:`the command line documentation <cli_options>`.

    
.. container:: toggle

    .. container:: header

        **Answer  ▶**

    .. code:: powershell
       
       .\output\DFIR-Orc.exe /key=SystemInfo /out=\Temp\testing /overwrite

    ``DFIR-Orc.exe`` detects that some archives already exist (based on the file names) and does not overwrite them by default.


4. Use Local Configuration Files
--------------------------------

A local configuration file is meant to provide some configuration options while not using a command line.
This can be useful in some deployment scenarios.

It is an XML file which has the following skeleton, described in the section :doc:`orc_local_config`.


| <:ref:`dfir-orc <orc_local_config-dfir-orc-element>`  *attributes="..."*>
|      <:ref:`temporary <orc_local_config-temporary-element>`> *value* </temporary>
|      <:ref:`output <orc_local_config-output-element>`> *value* </output>
|      <:ref:`upload <orc_local_config-upload-element>` *attributes="..."* />
|      <:ref:`recipient <orc_local_config-recipient-element>` *attributes="..."*> *value* </recipient>
|      <:ref:`key <orc_local_config-key-element>`> *value*  </key>
|      <:ref:`enable_key <orc_local_config-enable-key-and-disable-key-elements>`> *value* </enable_key>
|      <:ref:`disable_key <orc_local_config-enable-key-and-disable-key-elements>`> *value* </disable_key>
| </dfir-orc>


As an example, we show how to write a file to run the equivalent of the command line below.

.. code:: powershell
       
       .\output\DFIR-Orc.exe /key=SystemInfo /out=\Temp\testing

The corresponding file, named ``DFIR-Orc.xml`` and which we choose to store in ``\Temp\testing\``,  looks as follows.

.. code:: xml

   <dfir-orc priority="low" powerstate="SystemRequired,AwayMode">
      <output>\Temp\testing</output>
      <key>SystemInfo</key>
   </dfir-orc>


Running DFIR ORC with this configuration can be done with this command line:

.. code:: powershell 

       .\output\DFIR-Orc.exe /local=\Temp\testing\DFIR-Orc.xml  

Encrypting the archives with a public key requires adding a ``recipient`` element in the XML file.

.. code:: xml

    <dfir-orc priority="low" powerstate="Systemrequired,AwayMode">
      <output>\Temp\testing</output>
      <key>SystemInfo</key>
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
    </dfir-orc>

Suppose now that the configuration file ``DFIR-Orc.xml`` is copied in the same repository as the configured binary ``DFIR-Orc.exe``. We can then use the command line below: the executable takes into account the XML file bearing its base name present in its running directory.


.. code:: powershell 

       .\output\DFIR-Orc.exe 



Element ``upload`` is the counterpart of the ``output`` element to configure a **remote** repository as a destination for the archives.

Mini-challenge 4
````````````````

Combine the steps above to find a way to confirm *without creating any archive* that the local configuration file is being taken into account by the following command line.

.. code:: powershell 

       .\output\DFIR-Orc.exe 


.. container:: toggle

    .. container:: header

        **Hint  ▶**
    
    As documented in :ref:`this section <architecture-deployment-spe-conf>`, command-line options can be combined with a local configuration file, and supersede it.  
    
    
.. container:: toggle

    .. container:: header

        **Answer  ▶**
    
    Adding the option ``/keys`` to the command line being tested allows to check what is going to be executed.

    .. code:: powershell
       
       .\output\DFIR-Orc.exe /keys
 
    This displays that only SystemInfo is set to execute, and that the output directory is ``\Temp\testing``.


Edit the configuration file to add the command GetSamHive, and another recipient, which can only decrypt the Hives archive.

.. container:: toggle

    .. container:: header

        **Hint  ▶**
    
    It is possible to add another ``recipient`` element next to the first one.
    
.. container:: toggle

    .. container:: header

        **Answer  ▶**
      
    Here is one possible solution.     

    .. code:: xml 

       <dfir-orc priority="low" powerstate="Systemrequired,AwayMode">
         <output>\Temp\testing</output>
         <key>SystemInfo,GetSamHive</key>
         <recipient name="certfr" archive="*" >
          -----BEGIN CERTIFICATE-----
          etc.
          -----END CERTIFICATE-----
         </recipient>
         <recipient name="Marc" archive="Hives" >
         -----BEGIN CERTIFICATE-----
         etc.
         -----END CERTIFICATE-------
         </recipient>
       </dfir-orc>


.. _tuto-step-5:

5. Edit Embedded Configurations
----------------------------------

To refer to embedded tools as resources in a configuration file, a specific syntax is used.
Please read :doc:`resources` before proceeding.

As an example, let us try to find the command lines matching some instructions in the sample configuration file ``DFIR-ORC_config.xml`` from `the repository of existing configurations <https://github.com/dfir-orc/dfir-orc-config>`_. 

First, let us focus on ``autorunsc.exe``. The file reads:

.. code:: xml

    <command keyword="Autoruns">
       <execute name="autorunsc.exe" run="7z:#Tools|autorunsc.exe"/>
       <argument>-a * -c -h -m -s -t -accepteula</argument>
       <output name="autoruns.csv" source="StdOut"/>
       <output name="autoruns.log" source="StdErr"/>
    </command>


This paragraph establishes that when command Autoruns is run, a temporary file named ``autorunsc.exe`` is extracted on disk from an archive resource embedded in ``DFIR-Orc.exe`` (see the second bullet point :doc:`here <resources>` and :ref:`here <wolf_config-execute-element>` for details). Then, this temporary binary is run with arguments ``-a * -c -h -m -s -t -accepteula``. This produces two outputs; lines output on StdOut are stored in a file named ``autoruns.csv``, while lines output on StdErr are stored in autoruns.log.

Secondly, let us detail the example of NTFSInfo. The configuration reads:

.. code:: xml

    <command keyword="NTFSInfo" queue="flush">
       <execute name="DFIR-ORC.exe" run="self:#NTFSInfo"/>
       <argument>/config=res:#NTFSInfo_config.xml</argument>
       <output name="NTFSInfo_SecDesc.7z" source="File" argument="/SecDescr={FileName}"/>
       <output name="NTFSInfo_i30Info.7z" source="File" argument="/i30info={FileName}"/>
       <output name="NTFSInfo.7z" source="File" argument="/out={FileName}"/>
       <output name="NTFSInfo.log" source="StdOutErr"/>
    </command>

This paragraph describes what should happen when the NTFSInfo command is run. As NTFSInfo is a raw, non-archived resource of the configured binary, the syntax used is ``self:#NTFSInfo``. The configuration used by NTFSInfo (`̀`res:#NTFSInfo_config.xml``) is a resource of the configured binary, named ``NTFSInfo_config.xml``. This file has been embedded in the configured binary by ToolEmbed in :ref:`tuto-step-2`. The following line in ``DFIR-ORC_embed.xml`` allows to match the resource to the original file.

.. code:: xml

    <file name="NTFSInfo_config.xml" path=".\%ORC_CONFIG_FOLDER%\NTFSInfo_config.xml"/>

Recreating the command line can dine with a little help from :ref:`this section of the documentation of NTFSInfo <NTFSInfo-output>`. Assuming that the configuration file is on the disk and in the same directory as the configured binary, this yields the following line.

.. code:: powershell

    .\DFIR-Orc.exe NTFSInfo /config=NTFSInfo_config.xml /SecDescr=NTFSInfo_SecDesc.7z /i30info=NTFSInfo_i30Info.7z /out=NTFSInfo.7z /logfile=NTFSInfo.log


Now that reading a WolfLauncher configuration file is less of a mystery, let's try to modify it by adding the hives related to the AmCache. There are `several other useful files to collect <https://www.ssi.gouv.fr/en/publication/amcache-analysis/>`_, but this is beyond the scope of this tutorial. The Amcache hive is systemwide, and it has to be collected along with transaction and temporary files. Thus, after searching for the configuration files involved in the SYSTEM hive collection, it seems reasonable to append our new requirements to ``GetSystemHives_config.xml``.
Below is an excerpt of the new configuration file to be used by ``DFIR-Orc.exe``.

.. code:: xml

    <?xml version="1.0"?>
    <getthis reportall="" flushregistry="yes">
       <location>%SystemRoot%</location>
       <samples MaxPerSampleBytes="500MB" MaxTotalBytes="2048MB">
          <sample>
             <ntfs_find name="SECURITY" header="regf"/>
          </sample>
          ...
          <sample>
             <ntfs_find name="AmCache.hve" header="regf" />
             <ntfs_find name="AmCache.hve.log1" />
             <ntfs_find name="AmCache.hve.log2" />
          </sample>
       </samples>
    </getthis>


The modified configuration has to be embedded in the configured binary somehow. There are two ways to do this.
The first possibility is to modify the file ``GetSystemHives_config.xml`` and use ToolEmbed as in :ref:`tuto-step-2` above. 

It is also possible to do this directly on a configured binary as follows.

Start by creating a directory where embedded external tools and configurations can be dumped, e.g. ``dump_dir``.

.. code:: powershell 

    .\DFIR-Orc.exe toolembed /dump=.\DFIR-Orc.exe /out=dump_dir

In ``dump_dir``, find the file ``GetSystemHives_config.xml`` and modify it. Then, run the command below to obtain a new configured binary.

.. code:: powershell 

    cd dump_dir
    ..\DFIR-Orc.exe toolembed /out=..\New_DFIR-Orc.exe /config=Embed.xml


Mini-challenge 5
````````````````

Find how to change the yara rules used in DFIR ORC, and explain **why** it works.

.. container:: toggle

    .. container:: header

        **Hint  ▶**
   
    In the configuration repository, there is a file named ``ruleset.yara`` which 
    seems a good place to start. But how is it used ? 
    
.. container:: toggle

    .. container:: header

        **Answer  ▶**
      
    Reading ``GetYaraSamples_config.xml`` reveals that it is a GetThis configuration file, which uses yara and 
    a resource named ``res:#ruleset.yara`` to collect samples matching any rules in this set. 
    Changing the file ``ruleset.yara`` and embedding it in a new configured binary is indeed the right thing to do.
    

.. _tuto-step-6:

6. The Final Challenge
----------------------

A Few Q&A to Warm Up
`````````````````````

Find out which of the following statements are false, and why.

``DFIR-Orc_x86.exe`` is a configured binary, hence I can use it to run NTFSInfo.

.. container:: toggle

    .. container:: header

      **Answer  ▶**
 
    False, but nearly true. ``DFIR-Orc_x86.exe`` is the name usually given to an **unconfigured** binary.
    Both unconfigured and configured binary can be used to run tools embedded by default such as NTFSInfo, in a busybox way.


There is no need to recompile ``DFIR-Orc_x86.exe`` and ``DFIR-Orc_x64.exe`` to add an external tool,
using ToolEmbed is sufficient to obtain a new configured binary.

.. container:: toggle

    .. container:: header

      **Answer  ▶**
 
    True.

During an incident response, I have a disconnected Windows desktop and a configured binary ``DFIR-Orc.exe``. I want to augment the time span during which archives must complete and to collect files located in a specific place on the disk. There is nothing I can do on site.

.. container:: toggle

    .. container:: header

      **Answer  ▶**
 
    False. ToolEmbed allows to extract resources from a configured binary, modify them and reconstruct a new configured binary. This is explained in :ref:`tuto-step-5`. This is necessary to add the collection of files using GetSamples or GetThis. However, changing the timeout can be done using option ``/archive_timeout`` on the command line. It will supersede the default value in the embedded configuration. 


The Final Boss
``````````````

Great forensicators know that sometimes quick wins can be found in ``Temp``.
Create a new configured binary, which uses :doc:`GetThis` to collect specifically PE files in this directory.
To guarantee that this does not create enormous archives to transfer over a network, find how to impose 
limits on the size of each file, and the total size of the cumulated samples.

.. container:: toggle

    .. container:: header

        **Hint (list of the steps) ▶**
   
    Create a specific configuration file for GetThis, find what to put inside (some useful elements to check
    out in the documentation are ``location`` [global option], ``samples`` and ``sample``).

    Then, find a way to modify ``DFIR-ORC_config.xml`` so that the new GetThis file is used. This should highlight that 
    the new file has to be embedded as a resource, so the last thing to do is to edit ``DFIR-ORC_embed.xml`` so that a resource
    is created.
    
    Eventually, reconfigure to obtain a new binary with ToolEmbed (cf :ref:`tuto-step-2`).


.. container:: toggle

    .. container:: header

      **Answer  ▶**
 
    The solution presented here is not the only way to go, but doing these modifications work. 
    Firstly, create the following file named ``GetExeInTemp_config.xml``, in the ``config`` directory of the repository of configurations cloned previously.

    .. code:: xml

         <getthis reportall="">
            <location>*</location>  
            <samples MaxPerSampleBytes="<SomeLimitOfYourChoice>" MaxTotalBytes="<SomeOtherLimitToChoose>">
               <sample>
                 <ntfs_find path_match="\Temp\*" header="MZ" />
               </sample>
            </samples>
        </getthis>

    Then insert the following command element in ``DFIR-ORC_config.xml``, e.g. in the Main archive.   


    .. code:: xml
        
         <command keyword="GetExeInTemp">
             <execute name="DFIR-Orc.exe" run="self:#GetThis" />
             <argument>/config=res:#GetExeInTemp_config.xml</argument>
             <output name="ExeInTemp.7z" source="File" argument="/out={FileName}" />
             <output name="ExeInTemp.log" source="StdOutErr" />

         </command>

     
    This addition requires that a (non-archived) resource named ``GetExeInTemp_config.xml`` is available when the configured binary runs; so we have to embed it. To do so, let us edit the file ``DFIR-ORC_embed.xml``.
    We assume the file ``GetExeInTemp.xml`` exists along all the others in the ``config/`` directory. As a result, we insert the line below to the ``DFIR-ORC_embed.xml`` file.
         
     
    .. code:: xml
     
         <file name="GetExeInTemp_config.xml" path=".\%ORC_CONFIG_FOLDER%\GetExeInTemp_config.xml"/>

     
    Eventually, reconfiguration can be done as documented in step :ref:`tuto-step-2`.

