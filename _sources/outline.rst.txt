==========================
DFIR-ORC Execution Outline
==========================

The DFIR-ORC Execution Outline (introduced in dfir-orc v10.0.14) is a json file to summarize the dfir-orc execution context:

DFIR-ORC binary executed
========================

    * version: The schema version of the outline file
    * dfir_orc_id: The identifier of the binary version run


Example
-------

.. code:: json

    "dfir-orc": {
        "version": "1.0",
        "dfir_orc_id": "v10.0.14",
    }

DFIR-ORC execution context
==========================

    * time: The time of DFIR-ORC execution UTC
    * timestamp: The timestamp replacement string used throughout this DFIR-ORC execution in the following form: YYYYMMDD_HHMMSS (cf :doc:`WolfLauncher configuration <wolf_config>`)
    * command: The command line that started ORC execution
    * output: The configured output directory
    * temp: The configured directory fot temp files
    * archives: The archives collected and their active commands (cf :doc:`configuration`)
    * process: Detailed WolfLauncher process information (command line, environment, user context, ...)


Example
-------

.. code:: json

    "dfir-orc": {
        "time": "2020-07-31 10:51:20.937",
        "timestamp": "20200731_105120",
        "command": "\"C:\\temp\\dir-orc.exe\"",
        "output": "C:\\temp",
        "temp": "C:\\Users\\Jean\\AppData\\Local\\Temp\\WorkingTemp",
        "archives": [
            {
                "keyword": "ORC_Archive",
                "file": "ORC_WorkStation_Machine_Archive.7z",
                "commands": [
                    ... list of commands run in this archive (by their keyword)
                ]
            }
        ],
        "process": {
            "binary": "C:\\Users\\Jean\\AppData\\Local\\Temp\\DFIR-Orc_x64.exe",
            "syswow64": false,
            "command_line": "\"C:\\Users\\Jean\\AppData\\Local\\Temp\\DFIR-Orc_x64.exe\" WolfLauncher",
            "user": {
                "username": "MachineName\\UserName",
                "SID": "S-1-5-21-164153534902-4134548383802-265243332323-1001",
                "elevated": true,
                "locale": "en-US",
                "language": "English (United States)"
            },
            "environment": [
                {
                    "Name": "COMPUTERNAME",
                    "Value": "MachineName"
                },
                ...
            ]
        },
    }

System's hardware and configuration information
===============================================

    * name, fullname: This machine's names
    * type: This machine's type (WorkStation, Server, DomainController)
    * architecture: This's machine architecture (x64, x86)
    * operating_system: Detailed information about the operating system currently running DFIR-ORC:
        * description
        * version
        * language
        * locale
        * tag
        * time_zone
        * qfe
        * physical_drives
        * mounted_volumes
        * physical_memory
        * cpu
        * network

Example
-------

.. code:: json

    "dfir-orc": {
        "system": {
            "name": "MachineName",
            "fullname": "MachineName.Domain.com",
            "type": "WorkStation",
            "architecture": "x64",
            "operating_system": {
                "description": "Microsoft Windows 10 Enterprise Edition (build 19041), 64-bit",
                "version": "10.0",
                "locale": "en-US",
                "language": "English (United States)",
                "tag": [
                    "OSBuild#19041",
                    "RTM",
                    "Release#2004",
                    "Windows10",
                    "WorkStation",
                    "x64"
                ],
                "time_zone": {
                    "daylight": "Romance Daylight Time",
                    "daylight_bias": -60,
                    "standard": "Romance Standard Time",
                    "standard_bias": 0,
                    "current_bias": -60,
                    "current": "daylight"
                },
                "qfe": [
                    {
                        "hotfix_id": "KB4565627",
                        "installed_on": "7/14/2020"
                    },
                    ...
                ]
            },
            "physical_drives": [
                {
                    "path": "\\\\.\\PHYSICALDRIVE0",
                    "type": "Fixed hard disk media",
                    "serial": 0,
                    "size": 512105932800,
                    "status": "OK"
                },
                ...
            ],
            "mounted_volumes": [
                {
                    "path": "C:\\",
                    "label": "Windows",
                    "serial": 3471674564,
                    "file_system": "NTFS",
                    "device_id": "\\\\?\\Volume{214de6b9-8fa1-4b0e-9e83-3b41cdb194f9}\\",
                    "is_boot": true,
                    "is_system": false,
                    "size": 128178376704,
                    "freespace": 15089700864,
                    "type": "Fixed"
                },
                ...
            ],
            "physical_memory": {
                "current_load": 56,
                "physical": 17097428992,
                "pagefile": 22244237312,
                "available_physical": 7437279232,
                "available_pagefile": 8191057920
            },
            "cpu": [
                {
                    "name": "Intel(R) Core(TM) i7-8650U CPU @ 1.90GHz",
                    "description": "Intel64 Family 6 Model 142 Stepping 10",
                    "cores": 4,
                    "enabled_cores": 4,
                    "logical_processors": 8
                }
            ],
            "network": {
                "adapter": [
                    {
                        "name": "{AB41C39A-E91B-4DA1-B697-74FF38F4BEA0}",
                        "friendly_name": "Wi-Fi",
                        "description": "Marvell AVASTAR Wireless-AC Network Controller",
                        "physical": "F0-6E-B-CF-9D-56",
                        "dns_suffix": "home",
                        "address": [
                            {
                                "ipv6": "2a01:cb04:119:5600:b475:1fbb:8110:8dd1",
                                "mode": "unicast"
                            },
                            {
                                "ipv6": "2a01:cb04:119:5600:d77:2a0:bdd8:6835",
                                "mode": "unicast"
                            },
                            {
                                "ipv6": "fe80::b475:1fbb:8110:8dd1%22",
                                "mode": "unicast"
                            },
                            {
                                "ipv4": "192.168.1.46",
                                "mode": "unicast"
                            }
                        ],
                        "dns_server": [
                            {
                                "ipv6": "fe80::a21b:29ff:feff:4300%22"
                            },
                            {
                                "ipv4": "192.168.1.1"
                            }
                        ]
                    },
                    ...
                ]
            }
        }
    }


User Profile information
========================

    * default_profile: The default profile location
    * profiles_directory: The directory where user profiles ares created by default
    * program_data: ProgramData location
    * public_path: Public file libraries
    * profiles: List of currently system's known profiles (per HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList)
        * sid
        * path
        * user: resolved user name
        * key_last_write

Example
-------

.. code:: json

    "dfir-orc": {
        "profile_list": {
            "default_profile": "C:\\Users\\Default",
            "profiles_directory": "C:\\Users",
            "program_data": "C:\\ProgramData",
            "public_path": "C:\\Users\\Public",
            "profile": [
                {
                    "sid": "S-1-5-18",
                    "path": "C:\\WINDOWS\\system32\\config\\systemprofile",
                    "user": "NT AUTHORITY\\SYSTEM",
                    "key_last_write": "2019-12-07 09:17:27.256"
                },
                {
                    "sid": "S-1-5-19",
                    "path": "C:\\WINDOWS\\ServiceProfiles\\LocalService",
                    "user": "NT AUTHORITY\\LOCAL SERVICE",
                    "key_last_write": "2019-12-07 09:17:27.256"
                },
                {
                    "sid": "S-1-5-20",
                    "path": "C:\\WINDOWS\\ServiceProfiles\\NetworkService",
                    "user": "NT AUTHORITY\\NETWORK SERVICE",
                    "key_last_write": "2019-12-07 09:17:27.256"
                },
                {
                    "sid": "S-1-5-21-16443543502-41343243243202-264324343432-1001",
                    "path": "C:\\Users\\UserName",
                    "user": "MachineName\\UserName",
                    "local_load_time": "2020-07-26 15:42:47.209",
                    "local_unload_time": "2020-07-25 19:06:05.433",
                    "key_last_write": "2020-07-26 15:42:47.209"
                },
                ...
            ]
        }
    }