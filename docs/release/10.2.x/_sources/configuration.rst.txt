Configuration
=============

As explained in the section :doc:`intro_to_data_collection`, the configuration of DFIR ORC specify the list of programs to run and the name of the output archive containing the resulting data.

Any functional ready-to-use binary ``DFIR-Orc.exe`` embeds such a configuration as an XML resource. This latter is referred to as :doc:`a WolfLauncher configuration file <wolf_config>`.

WolfLauncher configuration can be embedded or extracted from ``DFIR-Orc.exe`` using its own ToolEmbed command, no external tool is required.

It is a usual step to extract a configuration for modification before embedding it back into ``DFIR-Orc.exe``. But it is also possible to influence the execution of ``DFIR-Orc.exe``, at least to some extent, using two other means.
Firstly, options can be gathered in a local configuration file to add or override embedded configuration elements.
Secondly, command-line options override both other levels of configuration.

Understanding how to configure of DFIR ORC is the key to unleashing its full potential.

To help getting started, a tutorial describes step by step a few scenarios.


.. toctree::
    :maxdepth: 1

    resources
    cli_options
    wolf_config
    ToolEmbed
    orc_local_config

