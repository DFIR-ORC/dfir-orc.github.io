==========================
DFIR-ORC Execution Outcome
==========================

The DFIR-ORC Execution Outcome (introduced in dfir-orc v10.1.0) is a json file to summarize the dfir-orc execution results.

Example
-------

.. code:: json

    {
        "version": "1.0",
        "dfir-orc": {
            "outcome": {
                "timestamp": "2021-02-01T14:42:34Z",
                "computer_name": "PC",
                "mothership": {
                    "sha256": "E237F80302F43D0AC04A3B866E4FB6D11F0D6A115A7D93344BC4C9D8D05FE6D5",
                    "command_line": "\"c:\\orc.exe\" /key=GetEvt_Little /overwrite"
                },
                "wolf_launcher": {
                    "sha256": "6E566AF08D5CF9B236F26B20D1B243BE4567FC5F76822108F167D76CF0B35BAD",
                    "version": "v10.1.0",
                    "command_line": "\"C:\\Users\\foo\\AppData\\Local\\Temp\\14_DFIR-Orc_x64.exe\" WolfLauncher /key=GetEvt_Little /overwrite"
                },
                "command_set": [
                    {
                        "name": "ORC_Custom",
                        "start": "2021-02-01T14:42:34Z",
                        "end": "2021-02-01T14:43:33Z",
                        "statistics": {
                            "io_counters": {
                                "read_operation": 91546,
                                "read_transfer": 2974589180,
                                "write_operation": 32,
                                "write_transfer": 8162543,
                                "other_operation": 1078,
                                "other_transfer": 756578
                            },
                            "process": 2,
                            "process_memory_peak": 3296743424,
                            "job_memory_peak": 0,
                            "active_proces": 0,
                            "terminated_process": 0,
                            "page_fault": 1194396
                        },
                        "archive": {
                            "name": "ORC_WorkStation_PC_ORC_Custom.7z",
                            "size": 8079202,
                            "files": [
                                {
                                    "name": "Config.xml",
                                    "size": 35904
                                },
                                {
                                    "name": "Event.7z",
                                    "size": 8066849
                                },
                                {
                                    "name": "Event.dev.log",
                                    "size": 53834
                                },
                                {
                                    "name": "Event.log",
                                    "size": 41672
                                }
                            ]
                        },
                        "commands": [
                            {
                                "name": "GetEVT_little",
                                "command_line": "\"C:\\Users\\user\\AppData\\...",
                                "start": "2021-02-01T14:42:34Z",
                                "end": "2021-02-01T14:43:32Z",
                                "exit_code": 0,
                                "pid": 13560,
                                "user_time": 48,
                                "kernel_time": 48,
                                "io_counters": {
                                    "read_operation": 91546,
                                    "read_transfer": 2974589180,
                                    "write_operation": 32,
                                    "write_transfer": 8162543,
                                    "other_operation": 1028,
                                    "other_transfer": 754256
                                }
                            }
                        ]
                    }
                ]
            }
        }
    }
