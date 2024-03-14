"""
Module provides the leakage configurations for LeakDB.
"""

NET1_LEAKAGES = """{
    "1": [
        {
            "node_id": "13",
            "leak_diameter": 0.130441139276,
            "leak_type": "incipient",
            "leak_start_time": 5179,
            "leak_end_time": 17219,
            "leak_peak_time": 7294
        }
    ],
    "2": [
        {
            "node_id": "31",
            "leak_diameter": 0.112552807234,
            "leak_type": "incipient",
            "leak_start_time": 8746,
            "leak_end_time": 9651,
            "leak_peak_time": 9464
        }
    ],
    "3": [
        {
            "node_id": "21",
            "leak_diameter": 0.163745594742,
            "leak_type": "incipient",
            "leak_start_time": 13246,
            "leak_end_time": 15745,
            "leak_peak_time": 14976
        },
        {
            "node_id": "2",
            "leak_diameter": 0.121521861063,
            "leak_type": "incipient",
            "leak_start_time": 15519,
            "leak_end_time": 15841,
            "leak_peak_time": 15614
        }
    ],
    "5": [
        {
            "node_id": "22",
            "leak_diameter": 0.0233169171761,
            "leak_type": "abrupt",
            "leak_start_time": 16470,
            "leak_end_time": 17410,
            "leak_peak_time": 16470
        }
    ],
    "6": [
        {
            "node_id": "22",
            "leak_diameter": 0.0471622993939,
            "leak_type": "abrupt",
            "leak_start_time": 11969,
            "leak_end_time": 17153,
            "leak_peak_time": 11969
        }
    ],
    "8": [
        {
            "node_id": "21",
            "leak_diameter": 0.145796530287,
            "leak_type": "incipient",
            "leak_start_time": 3880,
            "leak_end_time": 9353,
            "leak_peak_time": 3995
        }
    ],
    "9": [
        {
            "node_id": "23",
            "leak_diameter": 0.195973224019,
            "leak_type": "incipient",
            "leak_start_time": 10223,
            "leak_end_time": 12011,
            "leak_peak_time": 10899
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0779124382695,
            "leak_type": "incipient",
            "leak_start_time": 17473,
            "leak_end_time": 17477,
            "leak_peak_time": 17474
        }
    ],
    "13": [
        {
            "node_id": "21",
            "leak_diameter": 0.0239252086139,
            "leak_type": "incipient",
            "leak_start_time": 9063,
            "leak_end_time": 10304,
            "leak_peak_time": 9496
        }
    ],
    "15": [
        {
            "node_id": "13",
            "leak_diameter": 0.0758751350112,
            "leak_type": "incipient",
            "leak_start_time": 11471,
            "leak_end_time": 16644,
            "leak_peak_time": 13523
        }
    ],
    "16": [
        {
            "node_id": "13",
            "leak_diameter": 0.117051105178,
            "leak_type": "abrupt",
            "leak_start_time": 12905,
            "leak_end_time": 16372,
            "leak_peak_time": 12905
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0462569756528,
            "leak_type": "abrupt",
            "leak_start_time": 9176,
            "leak_end_time": 12775,
            "leak_peak_time": 9176
        }
    ],
    "17": [
        {
            "node_id": "23",
            "leak_diameter": 0.115650215568,
            "leak_type": "incipient",
            "leak_start_time": 3313,
            "leak_end_time": 17011,
            "leak_peak_time": 4341
        }
    ],
    "21": [
        {
            "node_id": "13",
            "leak_diameter": 0.181583734244,
            "leak_type": "abrupt",
            "leak_start_time": 5005,
            "leak_end_time": 9540,
            "leak_peak_time": 5005
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0241807407851,
            "leak_type": "incipient",
            "leak_start_time": 2619,
            "leak_end_time": 3793,
            "leak_peak_time": 3722
        }
    ],
    "22": [
        {
            "node_id": "21",
            "leak_diameter": 0.0560776911041,
            "leak_type": "abrupt",
            "leak_start_time": 15971,
            "leak_end_time": 16013,
            "leak_peak_time": 15971
        }
    ],
    "23": [
        {
            "node_id": "12",
            "leak_diameter": 0.0871017787565,
            "leak_type": "abrupt",
            "leak_start_time": 3188,
            "leak_end_time": 17512,
            "leak_peak_time": 3188
        }
    ],
    "24": [
        {
            "node_id": "32",
            "leak_diameter": 0.0421180705667,
            "leak_type": "abrupt",
            "leak_start_time": 10682,
            "leak_end_time": 14642,
            "leak_peak_time": 10682
        }
    ],
    "29": [
        {
            "node_id": "31",
            "leak_diameter": 0.0535862909815,
            "leak_type": "abrupt",
            "leak_start_time": 8623,
            "leak_end_time": 12979,
            "leak_peak_time": 8623
        }
    ],
    "30": [
        {
            "node_id": "22",
            "leak_diameter": 0.0856410426333,
            "leak_type": "abrupt",
            "leak_start_time": 7103,
            "leak_end_time": 8301,
            "leak_peak_time": 7103
        }
    ],
    "33": [
        {
            "node_id": "12",
            "leak_diameter": 0.0846211083323,
            "leak_type": "incipient",
            "leak_start_time": 13565,
            "leak_end_time": 14425,
            "leak_peak_time": 14353
        }
    ],
    "35": [
        {
            "node_id": "32",
            "leak_diameter": 0.0829157263789,
            "leak_type": "incipient",
            "leak_start_time": 14987,
            "leak_end_time": 17311,
            "leak_peak_time": 16402
        }
    ],
    "41": [
        {
            "node_id": "23",
            "leak_diameter": 0.116963589792,
            "leak_type": "incipient",
            "leak_start_time": 1202,
            "leak_end_time": 14007,
            "leak_peak_time": 5208
        }
    ],
    "42": [
        {
            "node_id": "23",
            "leak_diameter": 0.0709564153576,
            "leak_type": "abrupt",
            "leak_start_time": 14569,
            "leak_end_time": 14702,
            "leak_peak_time": 14569
        }
    ],
    "43": [
        {
            "node_id": "12",
            "leak_diameter": 0.166765409481,
            "leak_type": "incipient",
            "leak_start_time": 15081,
            "leak_end_time": 17333,
            "leak_peak_time": 17230
        }
    ],
    "44": [
        {
            "node_id": "21",
            "leak_diameter": 0.139373087704,
            "leak_type": "incipient",
            "leak_start_time": 10373,
            "leak_end_time": 10995,
            "leak_peak_time": 10466
        }
    ],
    "45": [
        {
            "node_id": "12",
            "leak_diameter": 0.164319545224,
            "leak_type": "abrupt",
            "leak_start_time": 7404,
            "leak_end_time": 10392,
            "leak_peak_time": 7404
        },
        {
            "node_id": "32",
            "leak_diameter": 0.184152793832,
            "leak_type": "abrupt",
            "leak_start_time": 8799,
            "leak_end_time": 12854,
            "leak_peak_time": 8799
        }
    ],
    "46": [
        {
            "node_id": "23",
            "leak_diameter": 0.0286741244255,
            "leak_type": "abrupt",
            "leak_start_time": 3111,
            "leak_end_time": 14354,
            "leak_peak_time": 3111
        }
    ],
    "47": [
        {
            "node_id": "22",
            "leak_diameter": 0.0803650559959,
            "leak_type": "incipient",
            "leak_start_time": 16915,
            "leak_end_time": 17511,
            "leak_peak_time": 17425
        }
    ],
    "48": [
        {
            "node_id": "22",
            "leak_diameter": 0.06914879806,
            "leak_type": "abrupt",
            "leak_start_time": 15460,
            "leak_end_time": 15829,
            "leak_peak_time": 15460
        },
        {
            "node_id": "21",
            "leak_diameter": 0.158845909467,
            "leak_type": "incipient",
            "leak_start_time": 13220,
            "leak_end_time": 16917,
            "leak_peak_time": 14971
        }
    ],
    "49": [
        {
            "node_id": "13",
            "leak_diameter": 0.0396389138015,
            "leak_type": "incipient",
            "leak_start_time": 15971,
            "leak_end_time": 16000,
            "leak_peak_time": 15973
        }
    ],
    "50": [
        {
            "node_id": "32",
            "leak_diameter": 0.0601958790157,
            "leak_type": "abrupt",
            "leak_start_time": 12623,
            "leak_end_time": 15772,
            "leak_peak_time": 12623
        }
    ],
    "54": [
        {
            "node_id": "21",
            "leak_diameter": 0.0900788042737,
            "leak_type": "abrupt",
            "leak_start_time": 7724,
            "leak_end_time": 11147,
            "leak_peak_time": 7724
        }
    ],
    "56": [
        {
            "node_id": "32",
            "leak_diameter": 0.0236813788609,
            "leak_type": "incipient",
            "leak_start_time": 1030,
            "leak_end_time": 9554,
            "leak_peak_time": 8169
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0764799703654,
            "leak_type": "abrupt",
            "leak_start_time": 12609,
            "leak_end_time": 17348,
            "leak_peak_time": 12609
        }
    ],
    "57": [
        {
            "node_id": "2",
            "leak_diameter": 0.118360957615,
            "leak_type": "abrupt",
            "leak_start_time": 1663,
            "leak_end_time": 16423,
            "leak_peak_time": 1663
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0250172119573,
            "leak_type": "abrupt",
            "leak_start_time": 12292,
            "leak_end_time": 13367,
            "leak_peak_time": 12292
        }
    ],
    "58": [
        {
            "node_id": "12",
            "leak_diameter": 0.137079895903,
            "leak_type": "abrupt",
            "leak_start_time": 10618,
            "leak_end_time": 11826,
            "leak_peak_time": 10618
        }
    ],
    "59": [
        {
            "node_id": "21",
            "leak_diameter": 0.135650372888,
            "leak_type": "incipient",
            "leak_start_time": 1940,
            "leak_end_time": 2537,
            "leak_peak_time": 2035
        },
        {
            "node_id": "23",
            "leak_diameter": 0.132646814111,
            "leak_type": "incipient",
            "leak_start_time": 11859,
            "leak_end_time": 12900,
            "leak_peak_time": 12021
        }
    ],
    "60": [
        {
            "node_id": "23",
            "leak_diameter": 0.133514547856,
            "leak_type": "incipient",
            "leak_start_time": 13434,
            "leak_end_time": 16747,
            "leak_peak_time": 13928
        }
    ],
    "63": [
        {
            "node_id": "21",
            "leak_diameter": 0.16475881019,
            "leak_type": "incipient",
            "leak_start_time": 10793,
            "leak_end_time": 12431,
            "leak_peak_time": 12312
        },
        {
            "node_id": "32",
            "leak_diameter": 0.102561917358,
            "leak_type": "abrupt",
            "leak_start_time": 12836,
            "leak_end_time": 13636,
            "leak_peak_time": 12836
        }
    ],
    "64": [
        {
            "node_id": "21",
            "leak_diameter": 0.143045818364,
            "leak_type": "incipient",
            "leak_start_time": 5967,
            "leak_end_time": 15372,
            "leak_peak_time": 11504
        },
        {
            "node_id": "32",
            "leak_diameter": 0.139739160219,
            "leak_type": "abrupt",
            "leak_start_time": 14843,
            "leak_end_time": 16929,
            "leak_peak_time": 14843
        }
    ],
    "65": [
        {
            "node_id": "2",
            "leak_diameter": 0.152227483819,
            "leak_type": "abrupt",
            "leak_start_time": 15101,
            "leak_end_time": 15310,
            "leak_peak_time": 15101
        }
    ],
    "66": [
        {
            "node_id": "21",
            "leak_diameter": 0.0717761972067,
            "leak_type": "incipient",
            "leak_start_time": 10927,
            "leak_end_time": 10991,
            "leak_peak_time": 10988
        }
    ],
    "67": [
        {
            "node_id": "21",
            "leak_diameter": 0.028598560118,
            "leak_type": "abrupt",
            "leak_start_time": 3588,
            "leak_end_time": 7509,
            "leak_peak_time": 3588
        },
        {
            "node_id": "13",
            "leak_diameter": 0.188045653459,
            "leak_type": "incipient",
            "leak_start_time": 7779,
            "leak_end_time": 14728,
            "leak_peak_time": 10788
        }
    ],
    "68": [
        {
            "node_id": "10",
            "leak_diameter": 0.151967052156,
            "leak_type": "abrupt",
            "leak_start_time": 13672,
            "leak_end_time": 16656,
            "leak_peak_time": 13672
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0888818065897,
            "leak_type": "incipient",
            "leak_start_time": 12954,
            "leak_end_time": 15209,
            "leak_peak_time": 13562
        }
    ],
    "69": [
        {
            "node_id": "10",
            "leak_diameter": 0.199482617886,
            "leak_type": "incipient",
            "leak_start_time": 1666,
            "leak_end_time": 7260,
            "leak_peak_time": 3419
        }
    ],
    "70": [
        {
            "node_id": "10",
            "leak_diameter": 0.170471881207,
            "leak_type": "abrupt",
            "leak_start_time": 5563,
            "leak_end_time": 6291,
            "leak_peak_time": 5563
        },
        {
            "node_id": "23",
            "leak_diameter": 0.161336557391,
            "leak_type": "incipient",
            "leak_start_time": 3094,
            "leak_end_time": 14513,
            "leak_peak_time": 8090
        }
    ],
    "71": [
        {
            "node_id": "23",
            "leak_diameter": 0.0867630449059,
            "leak_type": "incipient",
            "leak_start_time": 13317,
            "leak_end_time": 16610,
            "leak_peak_time": 14384
        }
    ],
    "72": [
        {
            "node_id": "12",
            "leak_diameter": 0.156150233241,
            "leak_type": "incipient",
            "leak_start_time": 931,
            "leak_end_time": 7507,
            "leak_peak_time": 3002
        }
    ],
    "73": [
        {
            "node_id": "10",
            "leak_diameter": 0.0260352811872,
            "leak_type": "abrupt",
            "leak_start_time": 10772,
            "leak_end_time": 13028,
            "leak_peak_time": 10772
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0664258067869,
            "leak_type": "incipient",
            "leak_start_time": 14786,
            "leak_end_time": 17257,
            "leak_peak_time": 16480
        }
    ],
    "74": [
        {
            "node_id": "2",
            "leak_diameter": 0.113256046302,
            "leak_type": "incipient",
            "leak_start_time": 5671,
            "leak_end_time": 8379,
            "leak_peak_time": 5705
        }
    ],
    "78": [
        {
            "node_id": "22",
            "leak_diameter": 0.157988251243,
            "leak_type": "abrupt",
            "leak_start_time": 7203,
            "leak_end_time": 8532,
            "leak_peak_time": 7203
        }
    ],
    "81": [
        {
            "node_id": "21",
            "leak_diameter": 0.191570509935,
            "leak_type": "incipient",
            "leak_start_time": 9707,
            "leak_end_time": 11925,
            "leak_peak_time": 11599
        }
    ],
    "82": [
        {
            "node_id": "10",
            "leak_diameter": 0.163174349552,
            "leak_type": "incipient",
            "leak_start_time": 4860,
            "leak_end_time": 7419,
            "leak_peak_time": 5328
        },
        {
            "node_id": "2",
            "leak_diameter": 0.0281776693939,
            "leak_type": "incipient",
            "leak_start_time": 15736,
            "leak_end_time": 16087,
            "leak_peak_time": 15965
        }
    ],
    "83": [
        {
            "node_id": "31",
            "leak_diameter": 0.147724606685,
            "leak_type": "abrupt",
            "leak_start_time": 12106,
            "leak_end_time": 16378,
            "leak_peak_time": 12106
        }
    ],
    "84": [
        {
            "node_id": "22",
            "leak_diameter": 0.128966087163,
            "leak_type": "incipient",
            "leak_start_time": 13160,
            "leak_end_time": 14197,
            "leak_peak_time": 13365
        }
    ],
    "85": [
        {
            "node_id": "10",
            "leak_diameter": 0.0657860263053,
            "leak_type": "incipient",
            "leak_start_time": 8647,
            "leak_end_time": 15484,
            "leak_peak_time": 11687
        }
    ],
    "86": [
        {
            "node_id": "23",
            "leak_diameter": 0.195710418216,
            "leak_type": "abrupt",
            "leak_start_time": 13561,
            "leak_end_time": 14418,
            "leak_peak_time": 13561
        }
    ],
    "87": [
        {
            "node_id": "22",
            "leak_diameter": 0.0316490768182,
            "leak_type": "abrupt",
            "leak_start_time": 7923,
            "leak_end_time": 9637,
            "leak_peak_time": 7923
        }
    ],
    "88": [
        {
            "node_id": "32",
            "leak_diameter": 0.162582571771,
            "leak_type": "abrupt",
            "leak_start_time": 9355,
            "leak_end_time": 10129,
            "leak_peak_time": 9355
        }
    ],
    "89": [
        {
            "node_id": "21",
            "leak_diameter": 0.171502006225,
            "leak_type": "incipient",
            "leak_start_time": 7661,
            "leak_end_time": 15536,
            "leak_peak_time": 10235
        },
        {
            "node_id": "2",
            "leak_diameter": 0.0938216588945,
            "leak_type": "abrupt",
            "leak_start_time": 10938,
            "leak_end_time": 15867,
            "leak_peak_time": 10938
        }
    ],
    "90": [
        {
            "node_id": "21",
            "leak_diameter": 0.08697206891,
            "leak_type": "incipient",
            "leak_start_time": 1403,
            "leak_end_time": 4484,
            "leak_peak_time": 3826
        }
    ],
    "91": [
        {
            "node_id": "21",
            "leak_diameter": 0.139197486648,
            "leak_type": "abrupt",
            "leak_start_time": 16470,
            "leak_end_time": 17248,
            "leak_peak_time": 16470
        },
        {
            "node_id": "31",
            "leak_diameter": 0.183804239704,
            "leak_type": "abrupt",
            "leak_start_time": 4646,
            "leak_end_time": 10869,
            "leak_peak_time": 4646
        }
    ],
    "92": [
        {
            "node_id": "23",
            "leak_diameter": 0.106041358879,
            "leak_type": "incipient",
            "leak_start_time": 4256,
            "leak_end_time": 10521,
            "leak_peak_time": 6171
        }
    ],
    "93": [
        {
            "node_id": "10",
            "leak_diameter": 0.0972418673281,
            "leak_type": "abrupt",
            "leak_start_time": 15974,
            "leak_end_time": 17505,
            "leak_peak_time": 15974
        },
        {
            "node_id": "12",
            "leak_diameter": 0.0226798574783,
            "leak_type": "incipient",
            "leak_start_time": 4667,
            "leak_end_time": 12014,
            "leak_peak_time": 9244
        }
    ],
    "96": [
        {
            "node_id": "22",
            "leak_diameter": 0.0954050657418,
            "leak_type": "abrupt",
            "leak_start_time": 3750,
            "leak_end_time": 16200,
            "leak_peak_time": 3750
        }
    ],
    "97": [
        {
            "node_id": "22",
            "leak_diameter": 0.112087534437,
            "leak_type": "abrupt",
            "leak_start_time": 1116,
            "leak_end_time": 5072,
            "leak_peak_time": 1116
        }
    ],
    "103": [
        {
            "node_id": "12",
            "leak_diameter": 0.0573337003942,
            "leak_type": "abrupt",
            "leak_start_time": 2473,
            "leak_end_time": 9305,
            "leak_peak_time": 2473
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0424385375713,
            "leak_type": "incipient",
            "leak_start_time": 15723,
            "leak_end_time": 16055,
            "leak_peak_time": 15747
        }
    ],
    "104": [
        {
            "node_id": "32",
            "leak_diameter": 0.0774275945395,
            "leak_type": "incipient",
            "leak_start_time": 901,
            "leak_end_time": 7231,
            "leak_peak_time": 4041
        }
    ],
    "105": [
        {
            "node_id": "13",
            "leak_diameter": 0.0808967664931,
            "leak_type": "incipient",
            "leak_start_time": 6180,
            "leak_end_time": 13982,
            "leak_peak_time": 12945
        }
    ],
    "106": [
        {
            "node_id": "31",
            "leak_diameter": 0.157292143249,
            "leak_type": "incipient",
            "leak_start_time": 12761,
            "leak_end_time": 16393,
            "leak_peak_time": 14969
        }
    ],
    "107": [
        {
            "node_id": "22",
            "leak_diameter": 0.119317045918,
            "leak_type": "abrupt",
            "leak_start_time": 15949,
            "leak_end_time": 17045,
            "leak_peak_time": 15949
        },
        {
            "node_id": "12",
            "leak_diameter": 0.0881506984001,
            "leak_type": "abrupt",
            "leak_start_time": 1166,
            "leak_end_time": 15854,
            "leak_peak_time": 1166
        }
    ],
    "109": [
        {
            "node_id": "21",
            "leak_diameter": 0.063680864474,
            "leak_type": "incipient",
            "leak_start_time": 3937,
            "leak_end_time": 6273,
            "leak_peak_time": 4651
        },
        {
            "node_id": "2",
            "leak_diameter": 0.0438422446946,
            "leak_type": "incipient",
            "leak_start_time": 12793,
            "leak_end_time": 14726,
            "leak_peak_time": 13482
        }
    ],
    "110": [
        {
            "node_id": "10",
            "leak_diameter": 0.133483237937,
            "leak_type": "incipient",
            "leak_start_time": 16437,
            "leak_end_time": 16543,
            "leak_peak_time": 16515
        },
        {
            "node_id": "22",
            "leak_diameter": 0.025596524534,
            "leak_type": "incipient",
            "leak_start_time": 16569,
            "leak_end_time": 17371,
            "leak_peak_time": 16617
        }
    ],
    "112": [
        {
            "node_id": "23",
            "leak_diameter": 0.102908713075,
            "leak_type": "abrupt",
            "leak_start_time": 4456,
            "leak_end_time": 8925,
            "leak_peak_time": 4456
        }
    ],
    "113": [
        {
            "node_id": "21",
            "leak_diameter": 0.101060511525,
            "leak_type": "incipient",
            "leak_start_time": 2752,
            "leak_end_time": 5199,
            "leak_peak_time": 5190
        }
    ],
    "115": [
        {
            "node_id": "22",
            "leak_diameter": 0.0883408435582,
            "leak_type": "incipient",
            "leak_start_time": 17196,
            "leak_end_time": 17274,
            "leak_peak_time": 17202
        }
    ],
    "116": [
        {
            "node_id": "22",
            "leak_diameter": 0.138300088782,
            "leak_type": "incipient",
            "leak_start_time": 7294,
            "leak_end_time": 10765,
            "leak_peak_time": 8597
        },
        {
            "node_id": "13",
            "leak_diameter": 0.140648022267,
            "leak_type": "incipient",
            "leak_start_time": 8313,
            "leak_end_time": 16829,
            "leak_peak_time": 11414
        }
    ],
    "118": [
        {
            "node_id": "13",
            "leak_diameter": 0.124578413946,
            "leak_type": "abrupt",
            "leak_start_time": 59,
            "leak_end_time": 8068,
            "leak_peak_time": 59
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0716115569903,
            "leak_type": "abrupt",
            "leak_start_time": 14391,
            "leak_end_time": 15426,
            "leak_peak_time": 14391
        }
    ],
    "120": [
        {
            "node_id": "23",
            "leak_diameter": 0.118475201363,
            "leak_type": "incipient",
            "leak_start_time": 10362,
            "leak_end_time": 13332,
            "leak_peak_time": 13032
        }
    ],
    "121": [
        {
            "node_id": "23",
            "leak_diameter": 0.069637557616,
            "leak_type": "abrupt",
            "leak_start_time": 2725,
            "leak_end_time": 13538,
            "leak_peak_time": 2725
        }
    ],
    "122": [
        {
            "node_id": "10",
            "leak_diameter": 0.131728973423,
            "leak_type": "abrupt",
            "leak_start_time": 4459,
            "leak_end_time": 17166,
            "leak_peak_time": 4459
        },
        {
            "node_id": "31",
            "leak_diameter": 0.173103557007,
            "leak_type": "abrupt",
            "leak_start_time": 5301,
            "leak_end_time": 11960,
            "leak_peak_time": 5301
        }
    ],
    "123": [
        {
            "node_id": "21",
            "leak_diameter": 0.16602170924,
            "leak_type": "incipient",
            "leak_start_time": 16001,
            "leak_end_time": 16485,
            "leak_peak_time": 16073
        }
    ],
    "124": [
        {
            "node_id": "22",
            "leak_diameter": 0.040744007591,
            "leak_type": "abrupt",
            "leak_start_time": 4124,
            "leak_end_time": 4460,
            "leak_peak_time": 4124
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0480329231045,
            "leak_type": "incipient",
            "leak_start_time": 12317,
            "leak_end_time": 14757,
            "leak_peak_time": 13212
        }
    ],
    "125": [
        {
            "node_id": "12",
            "leak_diameter": 0.0400402569948,
            "leak_type": "abrupt",
            "leak_start_time": 10210,
            "leak_end_time": 10363,
            "leak_peak_time": 10210
        }
    ],
    "126": [
        {
            "node_id": "23",
            "leak_diameter": 0.0625271119796,
            "leak_type": "abrupt",
            "leak_start_time": 16151,
            "leak_end_time": 17173,
            "leak_peak_time": 16151
        }
    ],
    "128": [
        {
            "node_id": "10",
            "leak_diameter": 0.0587192612545,
            "leak_type": "abrupt",
            "leak_start_time": 14057,
            "leak_end_time": 17285,
            "leak_peak_time": 14057
        }
    ],
    "129": [
        {
            "node_id": "21",
            "leak_diameter": 0.163850753545,
            "leak_type": "abrupt",
            "leak_start_time": 7921,
            "leak_end_time": 14473,
            "leak_peak_time": 7921
        }
    ],
    "131": [
        {
            "node_id": "12",
            "leak_diameter": 0.124736189639,
            "leak_type": "abrupt",
            "leak_start_time": 11311,
            "leak_end_time": 14340,
            "leak_peak_time": 11311
        }
    ],
    "132": [
        {
            "node_id": "21",
            "leak_diameter": 0.0523180980211,
            "leak_type": "abrupt",
            "leak_start_time": 826,
            "leak_end_time": 6178,
            "leak_peak_time": 826
        }
    ],
    "134": [
        {
            "node_id": "23",
            "leak_diameter": 0.158896707384,
            "leak_type": "abrupt",
            "leak_start_time": 14664,
            "leak_end_time": 15573,
            "leak_peak_time": 14664
        }
    ],
    "135": [
        {
            "node_id": "22",
            "leak_diameter": 0.181210181818,
            "leak_type": "abrupt",
            "leak_start_time": 14807,
            "leak_end_time": 16435,
            "leak_peak_time": 14807
        },
        {
            "node_id": "23",
            "leak_diameter": 0.05394042479,
            "leak_type": "incipient",
            "leak_start_time": 13050,
            "leak_end_time": 14405,
            "leak_peak_time": 13700
        }
    ],
    "137": [
        {
            "node_id": "21",
            "leak_diameter": 0.0799831419674,
            "leak_type": "incipient",
            "leak_start_time": 9534,
            "leak_end_time": 12393,
            "leak_peak_time": 11080
        }
    ],
    "140": [
        {
            "node_id": "13",
            "leak_diameter": 0.173836178562,
            "leak_type": "incipient",
            "leak_start_time": 16968,
            "leak_end_time": 17265,
            "leak_peak_time": 16976
        }
    ],
    "142": [
        {
            "node_id": "23",
            "leak_diameter": 0.0650602521923,
            "leak_type": "incipient",
            "leak_start_time": 11609,
            "leak_end_time": 17192,
            "leak_peak_time": 16785
        }
    ],
    "143": [
        {
            "node_id": "32",
            "leak_diameter": 0.0365179618636,
            "leak_type": "abrupt",
            "leak_start_time": 3301,
            "leak_end_time": 3831,
            "leak_peak_time": 3301
        }
    ],
    "144": [
        {
            "node_id": "2",
            "leak_diameter": 0.16309125237,
            "leak_type": "incipient",
            "leak_start_time": 10733,
            "leak_end_time": 17058,
            "leak_peak_time": 15755
        }
    ],
    "145": [
        {
            "node_id": "31",
            "leak_diameter": 0.0239322357774,
            "leak_type": "incipient",
            "leak_start_time": 5893,
            "leak_end_time": 15182,
            "leak_peak_time": 11321
        }
    ],
    "146": [
        {
            "node_id": "22",
            "leak_diameter": 0.0680604147542,
            "leak_type": "abrupt",
            "leak_start_time": 9934,
            "leak_end_time": 15372,
            "leak_peak_time": 9934
        }
    ],
    "147": [
        {
            "node_id": "21",
            "leak_diameter": 0.0595565120451,
            "leak_type": "incipient",
            "leak_start_time": 5969,
            "leak_end_time": 11632,
            "leak_peak_time": 7521
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0324098353278,
            "leak_type": "abrupt",
            "leak_start_time": 7137,
            "leak_end_time": 10445,
            "leak_peak_time": 7137
        }
    ],
    "149": [
        {
            "node_id": "13",
            "leak_diameter": 0.173477898885,
            "leak_type": "incipient",
            "leak_start_time": 16839,
            "leak_end_time": 17158,
            "leak_peak_time": 16964
        }
    ],
    "150": [
        {
            "node_id": "10",
            "leak_diameter": 0.182959766108,
            "leak_type": "incipient",
            "leak_start_time": 16358,
            "leak_end_time": 16542,
            "leak_peak_time": 16488
        }
    ],
    "151": [
        {
            "node_id": "31",
            "leak_diameter": 0.0387006470348,
            "leak_type": "incipient",
            "leak_start_time": 8388,
            "leak_end_time": 10016,
            "leak_peak_time": 9295
        }
    ],
    "153": [
        {
            "node_id": "12",
            "leak_diameter": 0.164312395767,
            "leak_type": "abrupt",
            "leak_start_time": 12569,
            "leak_end_time": 17086,
            "leak_peak_time": 12569
        },
        {
            "node_id": "13",
            "leak_diameter": 0.159362761416,
            "leak_type": "abrupt",
            "leak_start_time": 14785,
            "leak_end_time": 16216,
            "leak_peak_time": 14785
        }
    ],
    "155": [
        {
            "node_id": "21",
            "leak_diameter": 0.112511213183,
            "leak_type": "abrupt",
            "leak_start_time": 203,
            "leak_end_time": 15688,
            "leak_peak_time": 203
        }
    ],
    "156": [
        {
            "node_id": "13",
            "leak_diameter": 0.0349630540691,
            "leak_type": "incipient",
            "leak_start_time": 4618,
            "leak_end_time": 9682,
            "leak_peak_time": 5617
        }
    ],
    "158": [
        {
            "node_id": "12",
            "leak_diameter": 0.101229209505,
            "leak_type": "incipient",
            "leak_start_time": 14531,
            "leak_end_time": 15449,
            "leak_peak_time": 14541
        }
    ],
    "159": [
        {
            "node_id": "2",
            "leak_diameter": 0.101409743012,
            "leak_type": "abrupt",
            "leak_start_time": 3729,
            "leak_end_time": 9384,
            "leak_peak_time": 3729
        }
    ],
    "160": [
        {
            "node_id": "23",
            "leak_diameter": 0.056049707891,
            "leak_type": "abrupt",
            "leak_start_time": 10228,
            "leak_end_time": 13940,
            "leak_peak_time": 10228
        }
    ],
    "162": [
        {
            "node_id": "32",
            "leak_diameter": 0.118289863118,
            "leak_type": "abrupt",
            "leak_start_time": 12603,
            "leak_end_time": 16637,
            "leak_peak_time": 12603
        }
    ],
    "163": [
        {
            "node_id": "12",
            "leak_diameter": 0.0419536220504,
            "leak_type": "incipient",
            "leak_start_time": 14832,
            "leak_end_time": 17178,
            "leak_peak_time": 15980
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0895178799461,
            "leak_type": "abrupt",
            "leak_start_time": 4834,
            "leak_end_time": 7501,
            "leak_peak_time": 4834
        }
    ],
    "164": [
        {
            "node_id": "12",
            "leak_diameter": 0.0912186222282,
            "leak_type": "abrupt",
            "leak_start_time": 6089,
            "leak_end_time": 10816,
            "leak_peak_time": 6089
        }
    ],
    "166": [
        {
            "node_id": "13",
            "leak_diameter": 0.0838654322869,
            "leak_type": "incipient",
            "leak_start_time": 682,
            "leak_end_time": 10903,
            "leak_peak_time": 1423
        }
    ],
    "167": [
        {
            "node_id": "2",
            "leak_diameter": 0.172978743034,
            "leak_type": "abrupt",
            "leak_start_time": 5069,
            "leak_end_time": 11545,
            "leak_peak_time": 5069
        }
    ],
    "169": [
        {
            "node_id": "13",
            "leak_diameter": 0.0722588675804,
            "leak_type": "abrupt",
            "leak_start_time": 9260,
            "leak_end_time": 9658,
            "leak_peak_time": 9260
        },
        {
            "node_id": "2",
            "leak_diameter": 0.0434289486128,
            "leak_type": "abrupt",
            "leak_start_time": 17065,
            "leak_end_time": 17446,
            "leak_peak_time": 17065
        }
    ],
    "170": [
        {
            "node_id": "2",
            "leak_diameter": 0.139038844112,
            "leak_type": "abrupt",
            "leak_start_time": 8856,
            "leak_end_time": 10901,
            "leak_peak_time": 8856
        }
    ],
    "172": [
        {
            "node_id": "12",
            "leak_diameter": 0.179902542897,
            "leak_type": "abrupt",
            "leak_start_time": 1796,
            "leak_end_time": 2207,
            "leak_peak_time": 1796
        }
    ],
    "174": [
        {
            "node_id": "13",
            "leak_diameter": 0.155884207274,
            "leak_type": "incipient",
            "leak_start_time": 14390,
            "leak_end_time": 17412,
            "leak_peak_time": 17267
        }
    ],
    "176": [
        {
            "node_id": "23",
            "leak_diameter": 0.0659836079034,
            "leak_type": "abrupt",
            "leak_start_time": 4272,
            "leak_end_time": 14390,
            "leak_peak_time": 4272
        }
    ],
    "178": [
        {
            "node_id": "23",
            "leak_diameter": 0.0483083161753,
            "leak_type": "abrupt",
            "leak_start_time": 15837,
            "leak_end_time": 16132,
            "leak_peak_time": 15837
        }
    ],
    "179": [
        {
            "node_id": "23",
            "leak_diameter": 0.116052219122,
            "leak_type": "abrupt",
            "leak_start_time": 12902,
            "leak_end_time": 14127,
            "leak_peak_time": 12902
        }
    ],
    "180": [
        {
            "node_id": "13",
            "leak_diameter": 0.183513083391,
            "leak_type": "abrupt",
            "leak_start_time": 17207,
            "leak_end_time": 17228,
            "leak_peak_time": 17207
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0816329849677,
            "leak_type": "abrupt",
            "leak_start_time": 7773,
            "leak_end_time": 8656,
            "leak_peak_time": 7773
        }
    ],
    "181": [
        {
            "node_id": "23",
            "leak_diameter": 0.0277660077171,
            "leak_type": "incipient",
            "leak_start_time": 1874,
            "leak_end_time": 16686,
            "leak_peak_time": 11383
        }
    ],
    "183": [
        {
            "node_id": "13",
            "leak_diameter": 0.141049369334,
            "leak_type": "abrupt",
            "leak_start_time": 10184,
            "leak_end_time": 11107,
            "leak_peak_time": 10184
        }
    ],
    "184": [
        {
            "node_id": "13",
            "leak_diameter": 0.161510461282,
            "leak_type": "incipient",
            "leak_start_time": 15354,
            "leak_end_time": 16681,
            "leak_peak_time": 15956
        }
    ],
    "185": [
        {
            "node_id": "12",
            "leak_diameter": 0.166048642583,
            "leak_type": "incipient",
            "leak_start_time": 15584,
            "leak_end_time": 17492,
            "leak_peak_time": 16687
        }
    ],
    "186": [
        {
            "node_id": "31",
            "leak_diameter": 0.171095169274,
            "leak_type": "abrupt",
            "leak_start_time": 5395,
            "leak_end_time": 7776,
            "leak_peak_time": 5395
        }
    ],
    "187": [
        {
            "node_id": "21",
            "leak_diameter": 0.0596810633891,
            "leak_type": "abrupt",
            "leak_start_time": 1829,
            "leak_end_time": 9612,
            "leak_peak_time": 1829
        }
    ],
    "188": [
        {
            "node_id": "12",
            "leak_diameter": 0.111708363793,
            "leak_type": "incipient",
            "leak_start_time": 5306,
            "leak_end_time": 9921,
            "leak_peak_time": 8444
        }
    ],
    "192": [
        {
            "node_id": "22",
            "leak_diameter": 0.0413358513736,
            "leak_type": "incipient",
            "leak_start_time": 7999,
            "leak_end_time": 11610,
            "leak_peak_time": 9447
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0470999866305,
            "leak_type": "abrupt",
            "leak_start_time": 9698,
            "leak_end_time": 10084,
            "leak_peak_time": 9698
        }
    ],
    "193": [
        {
            "node_id": "31",
            "leak_diameter": 0.17625648185,
            "leak_type": "abrupt",
            "leak_start_time": 6316,
            "leak_end_time": 14807,
            "leak_peak_time": 6316
        }
    ],
    "194": [
        {
            "node_id": "12",
            "leak_diameter": 0.101155705832,
            "leak_type": "abrupt",
            "leak_start_time": 14725,
            "leak_end_time": 15274,
            "leak_peak_time": 14725
        }
    ],
    "195": [
        {
            "node_id": "13",
            "leak_diameter": 0.0643859850527,
            "leak_type": "abrupt",
            "leak_start_time": 6001,
            "leak_end_time": 13666,
            "leak_peak_time": 6001
        }
    ],
    "196": [
        {
            "node_id": "32",
            "leak_diameter": 0.141632172375,
            "leak_type": "abrupt",
            "leak_start_time": 12230,
            "leak_end_time": 17355,
            "leak_peak_time": 12230
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0973119869176,
            "leak_type": "abrupt",
            "leak_start_time": 1439,
            "leak_end_time": 11037,
            "leak_peak_time": 1439
        }
    ],
    "198": [
        {
            "node_id": "21",
            "leak_diameter": 0.102006586176,
            "leak_type": "incipient",
            "leak_start_time": 6737,
            "leak_end_time": 11113,
            "leak_peak_time": 9320
        },
        {
            "node_id": "23",
            "leak_diameter": 0.170352506676,
            "leak_type": "abrupt",
            "leak_start_time": 7925,
            "leak_end_time": 15149,
            "leak_peak_time": 7925
        }
    ],
    "199": [
        {
            "node_id": "32",
            "leak_diameter": 0.0481291421181,
            "leak_type": "abrupt",
            "leak_start_time": 16926,
            "leak_end_time": 17397,
            "leak_peak_time": 16926
        }
    ],
    "202": [
        {
            "node_id": "31",
            "leak_diameter": 0.15966311389,
            "leak_type": "incipient",
            "leak_start_time": 2250,
            "leak_end_time": 5070,
            "leak_peak_time": 4166
        }
    ],
    "203": [
        {
            "node_id": "32",
            "leak_diameter": 0.122396617556,
            "leak_type": "incipient",
            "leak_start_time": 15457,
            "leak_end_time": 16901,
            "leak_peak_time": 16499
        }
    ],
    "205": [
        {
            "node_id": "22",
            "leak_diameter": 0.0313538517182,
            "leak_type": "abrupt",
            "leak_start_time": 5247,
            "leak_end_time": 14429,
            "leak_peak_time": 5247
        }
    ],
    "206": [
        {
            "node_id": "31",
            "leak_diameter": 0.172554502399,
            "leak_type": "incipient",
            "leak_start_time": 10788,
            "leak_end_time": 16699,
            "leak_peak_time": 12769
        }
    ],
    "207": [
        {
            "node_id": "10",
            "leak_diameter": 0.182705254604,
            "leak_type": "abrupt",
            "leak_start_time": 8939,
            "leak_end_time": 9336,
            "leak_peak_time": 8939
        },
        {
            "node_id": "22",
            "leak_diameter": 0.0766891913954,
            "leak_type": "abrupt",
            "leak_start_time": 13779,
            "leak_end_time": 14683,
            "leak_peak_time": 13779
        }
    ],
    "208": [
        {
            "node_id": "13",
            "leak_diameter": 0.0373021770735,
            "leak_type": "abrupt",
            "leak_start_time": 16465,
            "leak_end_time": 17195,
            "leak_peak_time": 16465
        }
    ],
    "210": [
        {
            "node_id": "22",
            "leak_diameter": 0.0606058796357,
            "leak_type": "incipient",
            "leak_start_time": 17337,
            "leak_end_time": 17444,
            "leak_peak_time": 17401
        }
    ],
    "211": [
        {
            "node_id": "13",
            "leak_diameter": 0.0879331172294,
            "leak_type": "abrupt",
            "leak_start_time": 727,
            "leak_end_time": 15198,
            "leak_peak_time": 727
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0226213168905,
            "leak_type": "incipient",
            "leak_start_time": 2490,
            "leak_end_time": 11489,
            "leak_peak_time": 8049
        }
    ],
    "213": [
        {
            "node_id": "23",
            "leak_diameter": 0.0822584531838,
            "leak_type": "abrupt",
            "leak_start_time": 9243,
            "leak_end_time": 9354,
            "leak_peak_time": 9243
        }
    ],
    "214": [
        {
            "node_id": "12",
            "leak_diameter": 0.188415023135,
            "leak_type": "abrupt",
            "leak_start_time": 9270,
            "leak_end_time": 17233,
            "leak_peak_time": 9270
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0576893777673,
            "leak_type": "abrupt",
            "leak_start_time": 7748,
            "leak_end_time": 7908,
            "leak_peak_time": 7748
        }
    ],
    "215": [
        {
            "node_id": "23",
            "leak_diameter": 0.111591332343,
            "leak_type": "incipient",
            "leak_start_time": 10244,
            "leak_end_time": 10485,
            "leak_peak_time": 10473
        }
    ],
    "216": [
        {
            "node_id": "23",
            "leak_diameter": 0.15584345655,
            "leak_type": "abrupt",
            "leak_start_time": 10605,
            "leak_end_time": 13022,
            "leak_peak_time": 10605
        }
    ],
    "217": [
        {
            "node_id": "32",
            "leak_diameter": 0.044567358085,
            "leak_type": "incipient",
            "leak_start_time": 8878,
            "leak_end_time": 15210,
            "leak_peak_time": 11909
        }
    ],
    "218": [
        {
            "node_id": "31",
            "leak_diameter": 0.131767170516,
            "leak_type": "incipient",
            "leak_start_time": 3920,
            "leak_end_time": 15353,
            "leak_peak_time": 6953
        }
    ],
    "220": [
        {
            "node_id": "13",
            "leak_diameter": 0.0478107577771,
            "leak_type": "incipient",
            "leak_start_time": 4865,
            "leak_end_time": 14698,
            "leak_peak_time": 8968
        }
    ],
    "222": [
        {
            "node_id": "31",
            "leak_diameter": 0.180964487909,
            "leak_type": "incipient",
            "leak_start_time": 11567,
            "leak_end_time": 16520,
            "leak_peak_time": 11644
        }
    ],
    "224": [
        {
            "node_id": "13",
            "leak_diameter": 0.194157009921,
            "leak_type": "incipient",
            "leak_start_time": 3529,
            "leak_end_time": 8432,
            "leak_peak_time": 8277
        }
    ],
    "225": [
        {
            "node_id": "21",
            "leak_diameter": 0.11843832245,
            "leak_type": "incipient",
            "leak_start_time": 11964,
            "leak_end_time": 12702,
            "leak_peak_time": 11981
        },
        {
            "node_id": "13",
            "leak_diameter": 0.0419763562063,
            "leak_type": "abrupt",
            "leak_start_time": 5264,
            "leak_end_time": 14480,
            "leak_peak_time": 5264
        }
    ],
    "226": [
        {
            "node_id": "12",
            "leak_diameter": 0.164737719443,
            "leak_type": "abrupt",
            "leak_start_time": 4359,
            "leak_end_time": 11102,
            "leak_peak_time": 4359
        }
    ],
    "227": [
        {
            "node_id": "12",
            "leak_diameter": 0.0868727264746,
            "leak_type": "abrupt",
            "leak_start_time": 12088,
            "leak_end_time": 14383,
            "leak_peak_time": 12088
        },
        {
            "node_id": "21",
            "leak_diameter": 0.0544123622871,
            "leak_type": "incipient",
            "leak_start_time": 6146,
            "leak_end_time": 15894,
            "leak_peak_time": 9950
        }
    ],
    "228": [
        {
            "node_id": "23",
            "leak_diameter": 0.159287366959,
            "leak_type": "incipient",
            "leak_start_time": 6359,
            "leak_end_time": 8303,
            "leak_peak_time": 8131
        }
    ],
    "229": [
        {
            "node_id": "32",
            "leak_diameter": 0.185109362715,
            "leak_type": "incipient",
            "leak_start_time": 17180,
            "leak_end_time": 17490,
            "leak_peak_time": 17271
        }
    ],
    "230": [
        {
            "node_id": "12",
            "leak_diameter": 0.0886526468946,
            "leak_type": "abrupt",
            "leak_start_time": 774,
            "leak_end_time": 8646,
            "leak_peak_time": 774
        },
        {
            "node_id": "13",
            "leak_diameter": 0.148812881539,
            "leak_type": "incipient",
            "leak_start_time": 921,
            "leak_end_time": 15268,
            "leak_peak_time": 13943
        }
    ],
    "231": [
        {
            "node_id": "22",
            "leak_diameter": 0.0964199514842,
            "leak_type": "incipient",
            "leak_start_time": 3525,
            "leak_end_time": 10642,
            "leak_peak_time": 8428
        }
    ],
    "232": [
        {
            "node_id": "21",
            "leak_diameter": 0.166500344909,
            "leak_type": "abrupt",
            "leak_start_time": 6359,
            "leak_end_time": 17379,
            "leak_peak_time": 6359
        }
    ],
    "233": [
        {
            "node_id": "32",
            "leak_diameter": 0.0915884864333,
            "leak_type": "incipient",
            "leak_start_time": 5821,
            "leak_end_time": 10379,
            "leak_peak_time": 7030
        }
    ],
    "234": [
        {
            "node_id": "10",
            "leak_diameter": 0.0555951235073,
            "leak_type": "abrupt",
            "leak_start_time": 9764,
            "leak_end_time": 10911,
            "leak_peak_time": 9764
        },
        {
            "node_id": "32",
            "leak_diameter": 0.169432918838,
            "leak_type": "abrupt",
            "leak_start_time": 11435,
            "leak_end_time": 13866,
            "leak_peak_time": 11435
        }
    ],
    "235": [
        {
            "node_id": "13",
            "leak_diameter": 0.160716827501,
            "leak_type": "abrupt",
            "leak_start_time": 16882,
            "leak_end_time": 17417,
            "leak_peak_time": 16882
        }
    ],
    "236": [
        {
            "node_id": "13",
            "leak_diameter": 0.0497433061278,
            "leak_type": "incipient",
            "leak_start_time": 16617,
            "leak_end_time": 16959,
            "leak_peak_time": 16619
        }
    ],
    "237": [
        {
            "node_id": "12",
            "leak_diameter": 0.18018129856,
            "leak_type": "abrupt",
            "leak_start_time": 15465,
            "leak_end_time": 15773,
            "leak_peak_time": 15465
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0322623810142,
            "leak_type": "abrupt",
            "leak_start_time": 8054,
            "leak_end_time": 14925,
            "leak_peak_time": 8054
        }
    ],
    "238": [
        {
            "node_id": "13",
            "leak_diameter": 0.110003695473,
            "leak_type": "abrupt",
            "leak_start_time": 16449,
            "leak_end_time": 16812,
            "leak_peak_time": 16449
        }
    ],
    "239": [
        {
            "node_id": "21",
            "leak_diameter": 0.045736227725,
            "leak_type": "abrupt",
            "leak_start_time": 14067,
            "leak_end_time": 14793,
            "leak_peak_time": 14067
        },
        {
            "node_id": "13",
            "leak_diameter": 0.0201692040496,
            "leak_type": "incipient",
            "leak_start_time": 14443,
            "leak_end_time": 17410,
            "leak_peak_time": 15507
        }
    ],
    "242": [
        {
            "node_id": "23",
            "leak_diameter": 0.118451968263,
            "leak_type": "abrupt",
            "leak_start_time": 5305,
            "leak_end_time": 16449,
            "leak_peak_time": 5305
        }
    ],
    "243": [
        {
            "node_id": "10",
            "leak_diameter": 0.146448717081,
            "leak_type": "abrupt",
            "leak_start_time": 15791,
            "leak_end_time": 16222,
            "leak_peak_time": 15791
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0290169454856,
            "leak_type": "abrupt",
            "leak_start_time": 15394,
            "leak_end_time": 15791,
            "leak_peak_time": 15394
        }
    ],
    "244": [
        {
            "node_id": "21",
            "leak_diameter": 0.166555914198,
            "leak_type": "abrupt",
            "leak_start_time": 9814,
            "leak_end_time": 11861,
            "leak_peak_time": 9814
        },
        {
            "node_id": "23",
            "leak_diameter": 0.17935128506,
            "leak_type": "incipient",
            "leak_start_time": 3772,
            "leak_end_time": 10340,
            "leak_peak_time": 7714
        }
    ],
    "246": [
        {
            "node_id": "23",
            "leak_diameter": 0.189465735051,
            "leak_type": "incipient",
            "leak_start_time": 8224,
            "leak_end_time": 9977,
            "leak_peak_time": 8990
        }
    ],
    "247": [
        {
            "node_id": "12",
            "leak_diameter": 0.17500058017,
            "leak_type": "abrupt",
            "leak_start_time": 16432,
            "leak_end_time": 16986,
            "leak_peak_time": 16432
        }
    ],
    "248": [
        {
            "node_id": "13",
            "leak_diameter": 0.0411354198723,
            "leak_type": "incipient",
            "leak_start_time": 7839,
            "leak_end_time": 17254,
            "leak_peak_time": 15121
        }
    ],
    "249": [
        {
            "node_id": "13",
            "leak_diameter": 0.105090290395,
            "leak_type": "incipient",
            "leak_start_time": 3623,
            "leak_end_time": 8394,
            "leak_peak_time": 8253
        }
    ],
    "250": [
        {
            "node_id": "12",
            "leak_diameter": 0.0519441074817,
            "leak_type": "incipient",
            "leak_start_time": 14563,
            "leak_end_time": 17516,
            "leak_peak_time": 16380
        }
    ],
    "252": [
        {
            "node_id": "21",
            "leak_diameter": 0.057329015111,
            "leak_type": "abrupt",
            "leak_start_time": 14486,
            "leak_end_time": 17509,
            "leak_peak_time": 14486
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0772403418291,
            "leak_type": "abrupt",
            "leak_start_time": 16185,
            "leak_end_time": 16476,
            "leak_peak_time": 16185
        }
    ],
    "253": [
        {
            "node_id": "22",
            "leak_diameter": 0.0796389212759,
            "leak_type": "incipient",
            "leak_start_time": 5662,
            "leak_end_time": 14044,
            "leak_peak_time": 6913
        }
    ],
    "254": [
        {
            "node_id": "13",
            "leak_diameter": 0.0463813110764,
            "leak_type": "abrupt",
            "leak_start_time": 15165,
            "leak_end_time": 16292,
            "leak_peak_time": 15165
        }
    ],
    "257": [
        {
            "node_id": "12",
            "leak_diameter": 0.11054050189,
            "leak_type": "incipient",
            "leak_start_time": 8589,
            "leak_end_time": 12687,
            "leak_peak_time": 9977
        }
    ],
    "258": [
        {
            "node_id": "2",
            "leak_diameter": 0.160939585898,
            "leak_type": "incipient",
            "leak_start_time": 8144,
            "leak_end_time": 15664,
            "leak_peak_time": 15044
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0522495662645,
            "leak_type": "incipient",
            "leak_start_time": 5627,
            "leak_end_time": 9931,
            "leak_peak_time": 8228
        }
    ],
    "259": [
        {
            "node_id": "22",
            "leak_diameter": 0.0732701582622,
            "leak_type": "abrupt",
            "leak_start_time": 14061,
            "leak_end_time": 14924,
            "leak_peak_time": 14061
        }
    ],
    "260": [
        {
            "node_id": "21",
            "leak_diameter": 0.191205485514,
            "leak_type": "abrupt",
            "leak_start_time": 8622,
            "leak_end_time": 15021,
            "leak_peak_time": 8622
        }
    ],
    "261": [
        {
            "node_id": "22",
            "leak_diameter": 0.194147983991,
            "leak_type": "incipient",
            "leak_start_time": 9170,
            "leak_end_time": 13790,
            "leak_peak_time": 12413
        }
    ],
    "262": [
        {
            "node_id": "21",
            "leak_diameter": 0.16246711523,
            "leak_type": "abrupt",
            "leak_start_time": 3906,
            "leak_end_time": 5500,
            "leak_peak_time": 3906
        }
    ],
    "264": [
        {
            "node_id": "2",
            "leak_diameter": 0.173542336466,
            "leak_type": "incipient",
            "leak_start_time": 4377,
            "leak_end_time": 17136,
            "leak_peak_time": 9546
        }
    ],
    "265": [
        {
            "node_id": "10",
            "leak_diameter": 0.0698451703804,
            "leak_type": "abrupt",
            "leak_start_time": 16233,
            "leak_end_time": 17465,
            "leak_peak_time": 16233
        }
    ],
    "267": [
        {
            "node_id": "23",
            "leak_diameter": 0.069356130538,
            "leak_type": "incipient",
            "leak_start_time": 206,
            "leak_end_time": 11288,
            "leak_peak_time": 1234
        }
    ],
    "268": [
        {
            "node_id": "22",
            "leak_diameter": 0.0517994877761,
            "leak_type": "incipient",
            "leak_start_time": 10151,
            "leak_end_time": 13925,
            "leak_peak_time": 11478
        },
        {
            "node_id": "12",
            "leak_diameter": 0.0469776528531,
            "leak_type": "incipient",
            "leak_start_time": 15701,
            "leak_end_time": 15961,
            "leak_peak_time": 15869
        }
    ],
    "269": [
        {
            "node_id": "32",
            "leak_diameter": 0.0212043372214,
            "leak_type": "incipient",
            "leak_start_time": 16517,
            "leak_end_time": 16654,
            "leak_peak_time": 16627
        }
    ],
    "270": [
        {
            "node_id": "13",
            "leak_diameter": 0.166391137112,
            "leak_type": "abrupt",
            "leak_start_time": 15292,
            "leak_end_time": 16858,
            "leak_peak_time": 15292
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0403312678352,
            "leak_type": "incipient",
            "leak_start_time": 8816,
            "leak_end_time": 10328,
            "leak_peak_time": 9720
        }
    ],
    "271": [
        {
            "node_id": "22",
            "leak_diameter": 0.15759341041,
            "leak_type": "abrupt",
            "leak_start_time": 1029,
            "leak_end_time": 6379,
            "leak_peak_time": 1029
        },
        {
            "node_id": "23",
            "leak_diameter": 0.113659114351,
            "leak_type": "abrupt",
            "leak_start_time": 15056,
            "leak_end_time": 15465,
            "leak_peak_time": 15056
        }
    ],
    "272": [
        {
            "node_id": "13",
            "leak_diameter": 0.138199398865,
            "leak_type": "incipient",
            "leak_start_time": 5540,
            "leak_end_time": 6000,
            "leak_peak_time": 5882
        }
    ],
    "273": [
        {
            "node_id": "21",
            "leak_diameter": 0.189264720806,
            "leak_type": "incipient",
            "leak_start_time": 9504,
            "leak_end_time": 15501,
            "leak_peak_time": 10913
        }
    ],
    "276": [
        {
            "node_id": "2",
            "leak_diameter": 0.032351442305,
            "leak_type": "abrupt",
            "leak_start_time": 11835,
            "leak_end_time": 14702,
            "leak_peak_time": 11835
        }
    ],
    "277": [
        {
            "node_id": "31",
            "leak_diameter": 0.0586285707475,
            "leak_type": "abrupt",
            "leak_start_time": 12229,
            "leak_end_time": 15076,
            "leak_peak_time": 12229
        }
    ],
    "278": [
        {
            "node_id": "21",
            "leak_diameter": 0.0879901481337,
            "leak_type": "abrupt",
            "leak_start_time": 11364,
            "leak_end_time": 13113,
            "leak_peak_time": 11364
        },
        {
            "node_id": "23",
            "leak_diameter": 0.178353829097,
            "leak_type": "abrupt",
            "leak_start_time": 7273,
            "leak_end_time": 11353,
            "leak_peak_time": 7273
        }
    ],
    "280": [
        {
            "node_id": "13",
            "leak_diameter": 0.116075412754,
            "leak_type": "incipient",
            "leak_start_time": 10407,
            "leak_end_time": 14239,
            "leak_peak_time": 13560
        }
    ],
    "281": [
        {
            "node_id": "22",
            "leak_diameter": 0.0933383753704,
            "leak_type": "incipient",
            "leak_start_time": 4537,
            "leak_end_time": 12176,
            "leak_peak_time": 9720
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0216371398777,
            "leak_type": "incipient",
            "leak_start_time": 14772,
            "leak_end_time": 15790,
            "leak_peak_time": 15591
        }
    ],
    "282": [
        {
            "node_id": "31",
            "leak_diameter": 0.114488958672,
            "leak_type": "abrupt",
            "leak_start_time": 13002,
            "leak_end_time": 13810,
            "leak_peak_time": 13002
        }
    ],
    "283": [
        {
            "node_id": "22",
            "leak_diameter": 0.12020844167,
            "leak_type": "incipient",
            "leak_start_time": 2259,
            "leak_end_time": 16393,
            "leak_peak_time": 5027
        },
        {
            "node_id": "2",
            "leak_diameter": 0.148558285889,
            "leak_type": "incipient",
            "leak_start_time": 570,
            "leak_end_time": 11012,
            "leak_peak_time": 4601
        }
    ],
    "284": [
        {
            "node_id": "21",
            "leak_diameter": 0.0321621197447,
            "leak_type": "abrupt",
            "leak_start_time": 316,
            "leak_end_time": 6981,
            "leak_peak_time": 316
        },
        {
            "node_id": "31",
            "leak_diameter": 0.150714124407,
            "leak_type": "incipient",
            "leak_start_time": 4161,
            "leak_end_time": 8705,
            "leak_peak_time": 7637
        }
    ],
    "285": [
        {
            "node_id": "12",
            "leak_diameter": 0.10379324989,
            "leak_type": "abrupt",
            "leak_start_time": 12668,
            "leak_end_time": 16126,
            "leak_peak_time": 12668
        }
    ],
    "286": [
        {
            "node_id": "31",
            "leak_diameter": 0.137229541879,
            "leak_type": "incipient",
            "leak_start_time": 1893,
            "leak_end_time": 15385,
            "leak_peak_time": 9529
        }
    ],
    "288": [
        {
            "node_id": "22",
            "leak_diameter": 0.118377352742,
            "leak_type": "abrupt",
            "leak_start_time": 17154,
            "leak_end_time": 17216,
            "leak_peak_time": 17154
        }
    ],
    "290": [
        {
            "node_id": "32",
            "leak_diameter": 0.0816145455952,
            "leak_type": "abrupt",
            "leak_start_time": 6052,
            "leak_end_time": 13088,
            "leak_peak_time": 6052
        }
    ],
    "291": [
        {
            "node_id": "21",
            "leak_diameter": 0.0720611226379,
            "leak_type": "incipient",
            "leak_start_time": 13667,
            "leak_end_time": 14650,
            "leak_peak_time": 13926
        }
    ],
    "292": [
        {
            "node_id": "32",
            "leak_diameter": 0.112424306987,
            "leak_type": "abrupt",
            "leak_start_time": 5252,
            "leak_end_time": 10883,
            "leak_peak_time": 5252
        }
    ],
    "293": [
        {
            "node_id": "13",
            "leak_diameter": 0.0438464792413,
            "leak_type": "incipient",
            "leak_start_time": 10040,
            "leak_end_time": 15703,
            "leak_peak_time": 13792
        }
    ],
    "294": [
        {
            "node_id": "32",
            "leak_diameter": 0.0987499588371,
            "leak_type": "abrupt",
            "leak_start_time": 5218,
            "leak_end_time": 13842,
            "leak_peak_time": 5218
        }
    ],
    "295": [
        {
            "node_id": "12",
            "leak_diameter": 0.157342218997,
            "leak_type": "abrupt",
            "leak_start_time": 9856,
            "leak_end_time": 16204,
            "leak_peak_time": 9856
        },
        {
            "node_id": "13",
            "leak_diameter": 0.121032665448,
            "leak_type": "incipient",
            "leak_start_time": 807,
            "leak_end_time": 8244,
            "leak_peak_time": 2610
        }
    ],
    "296": [
        {
            "node_id": "13",
            "leak_diameter": 0.0416012120007,
            "leak_type": "incipient",
            "leak_start_time": 9488,
            "leak_end_time": 13858,
            "leak_peak_time": 12676
        }
    ],
    "297": [
        {
            "node_id": "32",
            "leak_diameter": 0.112222056121,
            "leak_type": "abrupt",
            "leak_start_time": 589,
            "leak_end_time": 5529,
            "leak_peak_time": 589
        }
    ],
    "298": [
        {
            "node_id": "21",
            "leak_diameter": 0.0678504250777,
            "leak_type": "abrupt",
            "leak_start_time": 5586,
            "leak_end_time": 10655,
            "leak_peak_time": 5586
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0713467033849,
            "leak_type": "incipient",
            "leak_start_time": 15575,
            "leak_end_time": 17449,
            "leak_peak_time": 15794
        }
    ],
    "299": [
        {
            "node_id": "21",
            "leak_diameter": 0.035369936932,
            "leak_type": "abrupt",
            "leak_start_time": 14857,
            "leak_end_time": 16438,
            "leak_peak_time": 14857
        }
    ],
    "301": [
        {
            "node_id": "23",
            "leak_diameter": 0.129216274795,
            "leak_type": "abrupt",
            "leak_start_time": 2996,
            "leak_end_time": 5661,
            "leak_peak_time": 2996
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0831910956518,
            "leak_type": "abrupt",
            "leak_start_time": 13989,
            "leak_end_time": 16794,
            "leak_peak_time": 13989
        }
    ],
    "303": [
        {
            "node_id": "12",
            "leak_diameter": 0.14226800288,
            "leak_type": "abrupt",
            "leak_start_time": 13421,
            "leak_end_time": 15526,
            "leak_peak_time": 13421
        },
        {
            "node_id": "23",
            "leak_diameter": 0.122992681279,
            "leak_type": "abrupt",
            "leak_start_time": 7979,
            "leak_end_time": 12171,
            "leak_peak_time": 7979
        }
    ],
    "304": [
        {
            "node_id": "21",
            "leak_diameter": 0.139876434397,
            "leak_type": "abrupt",
            "leak_start_time": 17051,
            "leak_end_time": 17404,
            "leak_peak_time": 17051
        }
    ],
    "305": [
        {
            "node_id": "32",
            "leak_diameter": 0.103169433261,
            "leak_type": "abrupt",
            "leak_start_time": 7837,
            "leak_end_time": 11820,
            "leak_peak_time": 7837
        }
    ],
    "308": [
        {
            "node_id": "31",
            "leak_diameter": 0.0497544789696,
            "leak_type": "incipient",
            "leak_start_time": 13780,
            "leak_end_time": 15010,
            "leak_peak_time": 14434
        }
    ],
    "309": [
        {
            "node_id": "13",
            "leak_diameter": 0.0767672636821,
            "leak_type": "abrupt",
            "leak_start_time": 10861,
            "leak_end_time": 12215,
            "leak_peak_time": 10861
        }
    ],
    "310": [
        {
            "node_id": "22",
            "leak_diameter": 0.15198613235,
            "leak_type": "incipient",
            "leak_start_time": 11802,
            "leak_end_time": 11897,
            "leak_peak_time": 11851
        }
    ],
    "311": [
        {
            "node_id": "31",
            "leak_diameter": 0.147945482709,
            "leak_type": "incipient",
            "leak_start_time": 16257,
            "leak_end_time": 16391,
            "leak_peak_time": 16302
        }
    ],
    "312": [
        {
            "node_id": "21",
            "leak_diameter": 0.063616611924,
            "leak_type": "abrupt",
            "leak_start_time": 10613,
            "leak_end_time": 14834,
            "leak_peak_time": 10613
        }
    ],
    "315": [
        {
            "node_id": "2",
            "leak_diameter": 0.0566030529168,
            "leak_type": "incipient",
            "leak_start_time": 1022,
            "leak_end_time": 6833,
            "leak_peak_time": 6586
        }
    ],
    "316": [
        {
            "node_id": "12",
            "leak_diameter": 0.0354400719868,
            "leak_type": "abrupt",
            "leak_start_time": 3935,
            "leak_end_time": 15885,
            "leak_peak_time": 3935
        },
        {
            "node_id": "2",
            "leak_diameter": 0.0614003753661,
            "leak_type": "incipient",
            "leak_start_time": 17198,
            "leak_end_time": 17420,
            "leak_peak_time": 17413
        }
    ],
    "317": [
        {
            "node_id": "21",
            "leak_diameter": 0.16228520533,
            "leak_type": "incipient",
            "leak_start_time": 5334,
            "leak_end_time": 13334,
            "leak_peak_time": 6137
        }
    ],
    "318": [
        {
            "node_id": "22",
            "leak_diameter": 0.0534379257962,
            "leak_type": "abrupt",
            "leak_start_time": 170,
            "leak_end_time": 488,
            "leak_peak_time": 170
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0484881807901,
            "leak_type": "abrupt",
            "leak_start_time": 11842,
            "leak_end_time": 15006,
            "leak_peak_time": 11842
        }
    ],
    "319": [
        {
            "node_id": "10",
            "leak_diameter": 0.150946739057,
            "leak_type": "abrupt",
            "leak_start_time": 11817,
            "leak_end_time": 16312,
            "leak_peak_time": 11817
        },
        {
            "node_id": "12",
            "leak_diameter": 0.0702630641051,
            "leak_type": "abrupt",
            "leak_start_time": 7185,
            "leak_end_time": 16758,
            "leak_peak_time": 7185
        }
    ],
    "320": [
        {
            "node_id": "21",
            "leak_diameter": 0.0294204315267,
            "leak_type": "incipient",
            "leak_start_time": 13190,
            "leak_end_time": 16287,
            "leak_peak_time": 15072
        }
    ],
    "322": [
        {
            "node_id": "32",
            "leak_diameter": 0.0873086804126,
            "leak_type": "abrupt",
            "leak_start_time": 15979,
            "leak_end_time": 16594,
            "leak_peak_time": 15979
        }
    ],
    "325": [
        {
            "node_id": "32",
            "leak_diameter": 0.163145985385,
            "leak_type": "abrupt",
            "leak_start_time": 7897,
            "leak_end_time": 14790,
            "leak_peak_time": 7897
        }
    ],
    "326": [
        {
            "node_id": "31",
            "leak_diameter": 0.0895512629823,
            "leak_type": "incipient",
            "leak_start_time": 8785,
            "leak_end_time": 10422,
            "leak_peak_time": 9511
        }
    ],
    "327": [
        {
            "node_id": "22",
            "leak_diameter": 0.0795501290163,
            "leak_type": "abrupt",
            "leak_start_time": 3551,
            "leak_end_time": 13778,
            "leak_peak_time": 3551
        }
    ],
    "329": [
        {
            "node_id": "12",
            "leak_diameter": 0.046079962482,
            "leak_type": "incipient",
            "leak_start_time": 12174,
            "leak_end_time": 15943,
            "leak_peak_time": 13420
        }
    ],
    "330": [
        {
            "node_id": "31",
            "leak_diameter": 0.0289846985934,
            "leak_type": "incipient",
            "leak_start_time": 8101,
            "leak_end_time": 11551,
            "leak_peak_time": 10165
        }
    ],
    "332": [
        {
            "node_id": "21",
            "leak_diameter": 0.134452394568,
            "leak_type": "incipient",
            "leak_start_time": 5003,
            "leak_end_time": 10306,
            "leak_peak_time": 7673
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0591492663449,
            "leak_type": "abrupt",
            "leak_start_time": 8785,
            "leak_end_time": 12877,
            "leak_peak_time": 8785
        }
    ],
    "333": [
        {
            "node_id": "21",
            "leak_diameter": 0.0531993394981,
            "leak_type": "abrupt",
            "leak_start_time": 3608,
            "leak_end_time": 15910,
            "leak_peak_time": 3608
        }
    ],
    "334": [
        {
            "node_id": "12",
            "leak_diameter": 0.0331116160026,
            "leak_type": "incipient",
            "leak_start_time": 3340,
            "leak_end_time": 15841,
            "leak_peak_time": 5412
        }
    ],
    "335": [
        {
            "node_id": "22",
            "leak_diameter": 0.0739176123128,
            "leak_type": "incipient",
            "leak_start_time": 10638,
            "leak_end_time": 15226,
            "leak_peak_time": 12636
        },
        {
            "node_id": "31",
            "leak_diameter": 0.144407797692,
            "leak_type": "abrupt",
            "leak_start_time": 17331,
            "leak_end_time": 17353,
            "leak_peak_time": 17331
        }
    ],
    "336": [
        {
            "node_id": "31",
            "leak_diameter": 0.0859511773572,
            "leak_type": "incipient",
            "leak_start_time": 4081,
            "leak_end_time": 5976,
            "leak_peak_time": 5667
        }
    ],
    "337": [
        {
            "node_id": "13",
            "leak_diameter": 0.0345052941055,
            "leak_type": "abrupt",
            "leak_start_time": 10786,
            "leak_end_time": 14222,
            "leak_peak_time": 10786
        }
    ],
    "341": [
        {
            "node_id": "22",
            "leak_diameter": 0.173361091421,
            "leak_type": "incipient",
            "leak_start_time": 16622,
            "leak_end_time": 16658,
            "leak_peak_time": 16633
        }
    ],
    "342": [
        {
            "node_id": "23",
            "leak_diameter": 0.114524848779,
            "leak_type": "abrupt",
            "leak_start_time": 9501,
            "leak_end_time": 15001,
            "leak_peak_time": 9501
        },
        {
            "node_id": "32",
            "leak_diameter": 0.162601408185,
            "leak_type": "incipient",
            "leak_start_time": 16420,
            "leak_end_time": 16431,
            "leak_peak_time": 16430
        }
    ],
    "343": [
        {
            "node_id": "21",
            "leak_diameter": 0.120555702306,
            "leak_type": "incipient",
            "leak_start_time": 5334,
            "leak_end_time": 9435,
            "leak_peak_time": 8218
        }
    ],
    "344": [
        {
            "node_id": "10",
            "leak_diameter": 0.171904088625,
            "leak_type": "abrupt",
            "leak_start_time": 8014,
            "leak_end_time": 9141,
            "leak_peak_time": 8014
        },
        {
            "node_id": "2",
            "leak_diameter": 0.0981686816449,
            "leak_type": "incipient",
            "leak_start_time": 16619,
            "leak_end_time": 17323,
            "leak_peak_time": 17212
        }
    ],
    "345": [
        {
            "node_id": "23",
            "leak_diameter": 0.0790367215721,
            "leak_type": "abrupt",
            "leak_start_time": 7222,
            "leak_end_time": 11752,
            "leak_peak_time": 7222
        },
        {
            "node_id": "32",
            "leak_diameter": 0.162370285507,
            "leak_type": "abrupt",
            "leak_start_time": 16720,
            "leak_end_time": 17170,
            "leak_peak_time": 16720
        }
    ],
    "347": [
        {
            "node_id": "10",
            "leak_diameter": 0.0519809409881,
            "leak_type": "incipient",
            "leak_start_time": 10257,
            "leak_end_time": 16456,
            "leak_peak_time": 12769
        }
    ],
    "348": [
        {
            "node_id": "21",
            "leak_diameter": 0.187028496841,
            "leak_type": "incipient",
            "leak_start_time": 5177,
            "leak_end_time": 7014,
            "leak_peak_time": 5830
        }
    ],
    "349": [
        {
            "node_id": "22",
            "leak_diameter": 0.0436529203221,
            "leak_type": "abrupt",
            "leak_start_time": 5306,
            "leak_end_time": 12085,
            "leak_peak_time": 5306
        }
    ],
    "350": [
        {
            "node_id": "31",
            "leak_diameter": 0.026661830562,
            "leak_type": "incipient",
            "leak_start_time": 13243,
            "leak_end_time": 17379,
            "leak_peak_time": 14121
        }
    ],
    "351": [
        {
            "node_id": "12",
            "leak_diameter": 0.176092629308,
            "leak_type": "abrupt",
            "leak_start_time": 7728,
            "leak_end_time": 14456,
            "leak_peak_time": 7728
        }
    ],
    "353": [
        {
            "node_id": "31",
            "leak_diameter": 0.105319459793,
            "leak_type": "abrupt",
            "leak_start_time": 13866,
            "leak_end_time": 15583,
            "leak_peak_time": 13866
        }
    ],
    "354": [
        {
            "node_id": "21",
            "leak_diameter": 0.164857465453,
            "leak_type": "incipient",
            "leak_start_time": 7437,
            "leak_end_time": 16522,
            "leak_peak_time": 9362
        }
    ],
    "355": [
        {
            "node_id": "13",
            "leak_diameter": 0.199530584388,
            "leak_type": "incipient",
            "leak_start_time": 3829,
            "leak_end_time": 11969,
            "leak_peak_time": 9805
        }
    ],
    "356": [
        {
            "node_id": "2",
            "leak_diameter": 0.0641375552295,
            "leak_type": "abrupt",
            "leak_start_time": 16207,
            "leak_end_time": 17427,
            "leak_peak_time": 16207
        }
    ],
    "357": [
        {
            "node_id": "10",
            "leak_diameter": 0.0299481116386,
            "leak_type": "abrupt",
            "leak_start_time": 10242,
            "leak_end_time": 15876,
            "leak_peak_time": 10242
        }
    ],
    "358": [
        {
            "node_id": "31",
            "leak_diameter": 0.108775211179,
            "leak_type": "abrupt",
            "leak_start_time": 7511,
            "leak_end_time": 11756,
            "leak_peak_time": 7511
        }
    ],
    "359": [
        {
            "node_id": "21",
            "leak_diameter": 0.0410986484197,
            "leak_type": "incipient",
            "leak_start_time": 13943,
            "leak_end_time": 15143,
            "leak_peak_time": 14586
        },
        {
            "node_id": "31",
            "leak_diameter": 0.19937800353,
            "leak_type": "incipient",
            "leak_start_time": 16502,
            "leak_end_time": 17441,
            "leak_peak_time": 17163
        }
    ],
    "360": [
        {
            "node_id": "22",
            "leak_diameter": 0.127034010165,
            "leak_type": "abrupt",
            "leak_start_time": 12074,
            "leak_end_time": 17431,
            "leak_peak_time": 12074
        }
    ],
    "363": [
        {
            "node_id": "31",
            "leak_diameter": 0.0726422158182,
            "leak_type": "abrupt",
            "leak_start_time": 15608,
            "leak_end_time": 17037,
            "leak_peak_time": 15608
        }
    ],
    "364": [
        {
            "node_id": "2",
            "leak_diameter": 0.167037216051,
            "leak_type": "incipient",
            "leak_start_time": 7766,
            "leak_end_time": 13988,
            "leak_peak_time": 13509
        }
    ],
    "365": [
        {
            "node_id": "22",
            "leak_diameter": 0.124664680747,
            "leak_type": "incipient",
            "leak_start_time": 249,
            "leak_end_time": 5356,
            "leak_peak_time": 3656
        }
    ],
    "367": [
        {
            "node_id": "13",
            "leak_diameter": 0.035114875272,
            "leak_type": "incipient",
            "leak_start_time": 6254,
            "leak_end_time": 8578,
            "leak_peak_time": 7001
        }
    ],
    "368": [
        {
            "node_id": "31",
            "leak_diameter": 0.114704960516,
            "leak_type": "incipient",
            "leak_start_time": 3681,
            "leak_end_time": 4319,
            "leak_peak_time": 3844
        }
    ],
    "369": [
        {
            "node_id": "13",
            "leak_diameter": 0.153823951585,
            "leak_type": "abrupt",
            "leak_start_time": 11646,
            "leak_end_time": 13620,
            "leak_peak_time": 11646
        }
    ],
    "370": [
        {
            "node_id": "22",
            "leak_diameter": 0.023012208252,
            "leak_type": "incipient",
            "leak_start_time": 11284,
            "leak_end_time": 17503,
            "leak_peak_time": 17111
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0630712408016,
            "leak_type": "incipient",
            "leak_start_time": 16904,
            "leak_end_time": 17137,
            "leak_peak_time": 17058
        }
    ],
    "372": [
        {
            "node_id": "21",
            "leak_diameter": 0.186384706702,
            "leak_type": "abrupt",
            "leak_start_time": 11254,
            "leak_end_time": 12016,
            "leak_peak_time": 11254
        },
        {
            "node_id": "13",
            "leak_diameter": 0.0593179460882,
            "leak_type": "abrupt",
            "leak_start_time": 1003,
            "leak_end_time": 14987,
            "leak_peak_time": 1003
        }
    ],
    "373": [
        {
            "node_id": "12",
            "leak_diameter": 0.198355588471,
            "leak_type": "abrupt",
            "leak_start_time": 8302,
            "leak_end_time": 9780,
            "leak_peak_time": 8302
        },
        {
            "node_id": "31",
            "leak_diameter": 0.122181464293,
            "leak_type": "incipient",
            "leak_start_time": 671,
            "leak_end_time": 14812,
            "leak_peak_time": 2199
        }
    ],
    "374": [
        {
            "node_id": "32",
            "leak_diameter": 0.0543064888381,
            "leak_type": "abrupt",
            "leak_start_time": 15836,
            "leak_end_time": 16641,
            "leak_peak_time": 15836
        }
    ],
    "379": [
        {
            "node_id": "22",
            "leak_diameter": 0.0541124505502,
            "leak_type": "abrupt",
            "leak_start_time": 12018,
            "leak_end_time": 17446,
            "leak_peak_time": 12018
        }
    ],
    "380": [
        {
            "node_id": "10",
            "leak_diameter": 0.0455576580438,
            "leak_type": "abrupt",
            "leak_start_time": 16545,
            "leak_end_time": 16625,
            "leak_peak_time": 16545
        }
    ],
    "381": [
        {
            "node_id": "21",
            "leak_diameter": 0.133330222168,
            "leak_type": "abrupt",
            "leak_start_time": 5091,
            "leak_end_time": 16882,
            "leak_peak_time": 5091
        }
    ],
    "383": [
        {
            "node_id": "10",
            "leak_diameter": 0.18095246604,
            "leak_type": "incipient",
            "leak_start_time": 10629,
            "leak_end_time": 14386,
            "leak_peak_time": 11355
        }
    ],
    "385": [
        {
            "node_id": "32",
            "leak_diameter": 0.119494966994,
            "leak_type": "incipient",
            "leak_start_time": 10456,
            "leak_end_time": 14350,
            "leak_peak_time": 10932
        },
        {
            "node_id": "31",
            "leak_diameter": 0.093019714927,
            "leak_type": "incipient",
            "leak_start_time": 17140,
            "leak_end_time": 17482,
            "leak_peak_time": 17476
        }
    ],
    "386": [
        {
            "node_id": "13",
            "leak_diameter": 0.165751655367,
            "leak_type": "abrupt",
            "leak_start_time": 10440,
            "leak_end_time": 10814,
            "leak_peak_time": 10440
        }
    ],
    "388": [
        {
            "node_id": "12",
            "leak_diameter": 0.091674029973,
            "leak_type": "incipient",
            "leak_start_time": 8827,
            "leak_end_time": 12011,
            "leak_peak_time": 9213
        }
    ],
    "389": [
        {
            "node_id": "22",
            "leak_diameter": 0.188706036324,
            "leak_type": "abrupt",
            "leak_start_time": 12205,
            "leak_end_time": 12543,
            "leak_peak_time": 12205
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0585066405687,
            "leak_type": "abrupt",
            "leak_start_time": 5274,
            "leak_end_time": 12899,
            "leak_peak_time": 5274
        }
    ],
    "390": [
        {
            "node_id": "21",
            "leak_diameter": 0.143687902701,
            "leak_type": "abrupt",
            "leak_start_time": 11109,
            "leak_end_time": 14093,
            "leak_peak_time": 11109
        }
    ],
    "391": [
        {
            "node_id": "31",
            "leak_diameter": 0.057487083925,
            "leak_type": "incipient",
            "leak_start_time": 16292,
            "leak_end_time": 16954,
            "leak_peak_time": 16765
        }
    ],
    "392": [
        {
            "node_id": "21",
            "leak_diameter": 0.116901955917,
            "leak_type": "incipient",
            "leak_start_time": 1814,
            "leak_end_time": 8571,
            "leak_peak_time": 7281
        }
    ],
    "393": [
        {
            "node_id": "22",
            "leak_diameter": 0.0458781867708,
            "leak_type": "incipient",
            "leak_start_time": 2319,
            "leak_end_time": 17507,
            "leak_peak_time": 13418
        },
        {
            "node_id": "21",
            "leak_diameter": 0.133412925534,
            "leak_type": "incipient",
            "leak_start_time": 9219,
            "leak_end_time": 9912,
            "leak_peak_time": 9833
        }
    ],
    "395": [
        {
            "node_id": "12",
            "leak_diameter": 0.0739842700571,
            "leak_type": "incipient",
            "leak_start_time": 15625,
            "leak_end_time": 15679,
            "leak_peak_time": 15648
        }
    ],
    "396": [
        {
            "node_id": "32",
            "leak_diameter": 0.137740964633,
            "leak_type": "abrupt",
            "leak_start_time": 16837,
            "leak_end_time": 16862,
            "leak_peak_time": 16837
        }
    ],
    "401": [
        {
            "node_id": "31",
            "leak_diameter": 0.168511943046,
            "leak_type": "abrupt",
            "leak_start_time": 7602,
            "leak_end_time": 11336,
            "leak_peak_time": 7602
        }
    ],
    "404": [
        {
            "node_id": "22",
            "leak_diameter": 0.0450040434347,
            "leak_type": "abrupt",
            "leak_start_time": 7809,
            "leak_end_time": 10759,
            "leak_peak_time": 7809
        },
        {
            "node_id": "12",
            "leak_diameter": 0.0884663750055,
            "leak_type": "incipient",
            "leak_start_time": 8411,
            "leak_end_time": 11293,
            "leak_peak_time": 10518
        }
    ],
    "405": [
        {
            "node_id": "13",
            "leak_diameter": 0.0740781120421,
            "leak_type": "incipient",
            "leak_start_time": 5738,
            "leak_end_time": 9002,
            "leak_peak_time": 8096
        }
    ],
    "406": [
        {
            "node_id": "2",
            "leak_diameter": 0.053823575111,
            "leak_type": "incipient",
            "leak_start_time": 4837,
            "leak_end_time": 17354,
            "leak_peak_time": 11469
        }
    ],
    "407": [
        {
            "node_id": "32",
            "leak_diameter": 0.0367588131304,
            "leak_type": "incipient",
            "leak_start_time": 12646,
            "leak_end_time": 14758,
            "leak_peak_time": 14522
        }
    ],
    "410": [
        {
            "node_id": "21",
            "leak_diameter": 0.101989497059,
            "leak_type": "incipient",
            "leak_start_time": 11056,
            "leak_end_time": 13267,
            "leak_peak_time": 12321
        }
    ],
    "411": [
        {
            "node_id": "31",
            "leak_diameter": 0.129392573071,
            "leak_type": "abrupt",
            "leak_start_time": 16075,
            "leak_end_time": 16146,
            "leak_peak_time": 16075
        }
    ],
    "414": [
        {
            "node_id": "23",
            "leak_diameter": 0.160405750622,
            "leak_type": "abrupt",
            "leak_start_time": 8756,
            "leak_end_time": 13816,
            "leak_peak_time": 8756
        }
    ],
    "415": [
        {
            "node_id": "22",
            "leak_diameter": 0.163968411758,
            "leak_type": "incipient",
            "leak_start_time": 7721,
            "leak_end_time": 12810,
            "leak_peak_time": 12718
        },
        {
            "node_id": "13",
            "leak_diameter": 0.151923504054,
            "leak_type": "abrupt",
            "leak_start_time": 4778,
            "leak_end_time": 17368,
            "leak_peak_time": 4778
        }
    ],
    "417": [
        {
            "node_id": "32",
            "leak_diameter": 0.169670127382,
            "leak_type": "abrupt",
            "leak_start_time": 5509,
            "leak_end_time": 14774,
            "leak_peak_time": 5509
        }
    ],
    "418": [
        {
            "node_id": "31",
            "leak_diameter": 0.182239057646,
            "leak_type": "incipient",
            "leak_start_time": 15062,
            "leak_end_time": 17479,
            "leak_peak_time": 15630
        }
    ],
    "419": [
        {
            "node_id": "13",
            "leak_diameter": 0.158649331259,
            "leak_type": "incipient",
            "leak_start_time": 8793,
            "leak_end_time": 17085,
            "leak_peak_time": 12092
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0963864633633,
            "leak_type": "incipient",
            "leak_start_time": 12427,
            "leak_end_time": 16698,
            "leak_peak_time": 16035
        }
    ],
    "420": [
        {
            "node_id": "21",
            "leak_diameter": 0.131369825512,
            "leak_type": "incipient",
            "leak_start_time": 15085,
            "leak_end_time": 15541,
            "leak_peak_time": 15175
        }
    ],
    "421": [
        {
            "node_id": "31",
            "leak_diameter": 0.193176109693,
            "leak_type": "incipient",
            "leak_start_time": 9657,
            "leak_end_time": 11177,
            "leak_peak_time": 10325
        }
    ],
    "422": [
        {
            "node_id": "10",
            "leak_diameter": 0.145680373782,
            "leak_type": "incipient",
            "leak_start_time": 11427,
            "leak_end_time": 14461,
            "leak_peak_time": 12852
        }
    ],
    "425": [
        {
            "node_id": "13",
            "leak_diameter": 0.12955730559,
            "leak_type": "abrupt",
            "leak_start_time": 6062,
            "leak_end_time": 6818,
            "leak_peak_time": 6062
        },
        {
            "node_id": "31",
            "leak_diameter": 0.042713246044,
            "leak_type": "abrupt",
            "leak_start_time": 16945,
            "leak_end_time": 17068,
            "leak_peak_time": 16945
        }
    ],
    "426": [
        {
            "node_id": "12",
            "leak_diameter": 0.114113863452,
            "leak_type": "abrupt",
            "leak_start_time": 2338,
            "leak_end_time": 5417,
            "leak_peak_time": 2338
        }
    ],
    "427": [
        {
            "node_id": "32",
            "leak_diameter": 0.0469872170994,
            "leak_type": "incipient",
            "leak_start_time": 17271,
            "leak_end_time": 17479,
            "leak_peak_time": 17347
        }
    ],
    "429": [
        {
            "node_id": "21",
            "leak_diameter": 0.0638729262758,
            "leak_type": "incipient",
            "leak_start_time": 6928,
            "leak_end_time": 10871,
            "leak_peak_time": 10182
        }
    ],
    "430": [
        {
            "node_id": "23",
            "leak_diameter": 0.120318542329,
            "leak_type": "incipient",
            "leak_start_time": 7014,
            "leak_end_time": 10494,
            "leak_peak_time": 8220
        }
    ],
    "432": [
        {
            "node_id": "10",
            "leak_diameter": 0.128430493204,
            "leak_type": "abrupt",
            "leak_start_time": 7194,
            "leak_end_time": 16206,
            "leak_peak_time": 7194
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0301161742477,
            "leak_type": "incipient",
            "leak_start_time": 741,
            "leak_end_time": 14282,
            "leak_peak_time": 791
        }
    ],
    "433": [
        {
            "node_id": "12",
            "leak_diameter": 0.147212822254,
            "leak_type": "abrupt",
            "leak_start_time": 13390,
            "leak_end_time": 17373,
            "leak_peak_time": 13390
        }
    ],
    "434": [
        {
            "node_id": "10",
            "leak_diameter": 0.147777213537,
            "leak_type": "abrupt",
            "leak_start_time": 13973,
            "leak_end_time": 14382,
            "leak_peak_time": 13973
        }
    ],
    "435": [
        {
            "node_id": "32",
            "leak_diameter": 0.152567712902,
            "leak_type": "abrupt",
            "leak_start_time": 12165,
            "leak_end_time": 12574,
            "leak_peak_time": 12165
        }
    ],
    "436": [
        {
            "node_id": "22",
            "leak_diameter": 0.039468872684,
            "leak_type": "incipient",
            "leak_start_time": 1632,
            "leak_end_time": 11263,
            "leak_peak_time": 7473
        }
    ],
    "438": [
        {
            "node_id": "21",
            "leak_diameter": 0.161681932044,
            "leak_type": "abrupt",
            "leak_start_time": 13748,
            "leak_end_time": 14372,
            "leak_peak_time": 13748
        }
    ],
    "439": [
        {
            "node_id": "23",
            "leak_diameter": 0.0486955218988,
            "leak_type": "abrupt",
            "leak_start_time": 6120,
            "leak_end_time": 6839,
            "leak_peak_time": 6120
        }
    ],
    "442": [
        {
            "node_id": "13",
            "leak_diameter": 0.0945624781091,
            "leak_type": "abrupt",
            "leak_start_time": 11232,
            "leak_end_time": 11802,
            "leak_peak_time": 11232
        },
        {
            "node_id": "2",
            "leak_diameter": 0.0857056884466,
            "leak_type": "abrupt",
            "leak_start_time": 15920,
            "leak_end_time": 16381,
            "leak_peak_time": 15920
        }
    ],
    "444": [
        {
            "node_id": "13",
            "leak_diameter": 0.136785460296,
            "leak_type": "abrupt",
            "leak_start_time": 595,
            "leak_end_time": 1828,
            "leak_peak_time": 595
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0457434437584,
            "leak_type": "incipient",
            "leak_start_time": 12611,
            "leak_end_time": 17010,
            "leak_peak_time": 16513
        }
    ],
    "445": [
        {
            "node_id": "31",
            "leak_diameter": 0.0783863295855,
            "leak_type": "incipient",
            "leak_start_time": 8836,
            "leak_end_time": 13267,
            "leak_peak_time": 10549
        }
    ],
    "446": [
        {
            "node_id": "23",
            "leak_diameter": 0.114688539931,
            "leak_type": "abrupt",
            "leak_start_time": 2993,
            "leak_end_time": 14382,
            "leak_peak_time": 2993
        }
    ],
    "447": [
        {
            "node_id": "23",
            "leak_diameter": 0.189730235412,
            "leak_type": "incipient",
            "leak_start_time": 3339,
            "leak_end_time": 8500,
            "leak_peak_time": 4352
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0312170182067,
            "leak_type": "abrupt",
            "leak_start_time": 2513,
            "leak_end_time": 7508,
            "leak_peak_time": 2513
        }
    ],
    "448": [
        {
            "node_id": "13",
            "leak_diameter": 0.162236056017,
            "leak_type": "abrupt",
            "leak_start_time": 9560,
            "leak_end_time": 9946,
            "leak_peak_time": 9560
        }
    ],
    "450": [
        {
            "node_id": "12",
            "leak_diameter": 0.177573732197,
            "leak_type": "incipient",
            "leak_start_time": 14281,
            "leak_end_time": 17427,
            "leak_peak_time": 16108
        }
    ],
    "451": [
        {
            "node_id": "23",
            "leak_diameter": 0.152066705472,
            "leak_type": "abrupt",
            "leak_start_time": 137,
            "leak_end_time": 4254,
            "leak_peak_time": 137
        }
    ],
    "452": [
        {
            "node_id": "10",
            "leak_diameter": 0.142140061464,
            "leak_type": "abrupt",
            "leak_start_time": 2192,
            "leak_end_time": 16961,
            "leak_peak_time": 2192
        },
        {
            "node_id": "12",
            "leak_diameter": 0.115188849591,
            "leak_type": "incipient",
            "leak_start_time": 14715,
            "leak_end_time": 16984,
            "leak_peak_time": 16630
        }
    ],
    "454": [
        {
            "node_id": "21",
            "leak_diameter": 0.165597076487,
            "leak_type": "abrupt",
            "leak_start_time": 10166,
            "leak_end_time": 12404,
            "leak_peak_time": 10166
        },
        {
            "node_id": "13",
            "leak_diameter": 0.0785370671159,
            "leak_type": "incipient",
            "leak_start_time": 6286,
            "leak_end_time": 9284,
            "leak_peak_time": 8252
        }
    ],
    "455": [
        {
            "node_id": "21",
            "leak_diameter": 0.106653041493,
            "leak_type": "abrupt",
            "leak_start_time": 1909,
            "leak_end_time": 6705,
            "leak_peak_time": 1909
        }
    ],
    "460": [
        {
            "node_id": "12",
            "leak_diameter": 0.142158586517,
            "leak_type": "abrupt",
            "leak_start_time": 10133,
            "leak_end_time": 15145,
            "leak_peak_time": 10133
        }
    ],
    "461": [
        {
            "node_id": "23",
            "leak_diameter": 0.0890623447577,
            "leak_type": "abrupt",
            "leak_start_time": 613,
            "leak_end_time": 9496,
            "leak_peak_time": 613
        }
    ],
    "463": [
        {
            "node_id": "13",
            "leak_diameter": 0.029299640875,
            "leak_type": "incipient",
            "leak_start_time": 3017,
            "leak_end_time": 13598,
            "leak_peak_time": 9548
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0488410187197,
            "leak_type": "abrupt",
            "leak_start_time": 3771,
            "leak_end_time": 8875,
            "leak_peak_time": 3771
        }
    ],
    "465": [
        {
            "node_id": "22",
            "leak_diameter": 0.183495075818,
            "leak_type": "incipient",
            "leak_start_time": 2979,
            "leak_end_time": 9410,
            "leak_peak_time": 8527
        },
        {
            "node_id": "23",
            "leak_diameter": 0.117620977354,
            "leak_type": "abrupt",
            "leak_start_time": 15686,
            "leak_end_time": 16598,
            "leak_peak_time": 15686
        }
    ],
    "467": [
        {
            "node_id": "21",
            "leak_diameter": 0.0798416578934,
            "leak_type": "incipient",
            "leak_start_time": 6601,
            "leak_end_time": 16313,
            "leak_peak_time": 13877
        }
    ],
    "469": [
        {
            "node_id": "31",
            "leak_diameter": 0.086020378245,
            "leak_type": "incipient",
            "leak_start_time": 10267,
            "leak_end_time": 13890,
            "leak_peak_time": 11938
        }
    ],
    "470": [
        {
            "node_id": "23",
            "leak_diameter": 0.185982729208,
            "leak_type": "incipient",
            "leak_start_time": 14710,
            "leak_end_time": 16634,
            "leak_peak_time": 15319
        }
    ],
    "471": [
        {
            "node_id": "13",
            "leak_diameter": 0.177647717332,
            "leak_type": "incipient",
            "leak_start_time": 5910,
            "leak_end_time": 8865,
            "leak_peak_time": 6703
        }
    ],
    "472": [
        {
            "node_id": "21",
            "leak_diameter": 0.0530991360926,
            "leak_type": "abrupt",
            "leak_start_time": 1326,
            "leak_end_time": 11406,
            "leak_peak_time": 1326
        },
        {
            "node_id": "31",
            "leak_diameter": 0.151417513527,
            "leak_type": "incipient",
            "leak_start_time": 6846,
            "leak_end_time": 11374,
            "leak_peak_time": 7898
        }
    ],
    "473": [
        {
            "node_id": "21",
            "leak_diameter": 0.0486772549226,
            "leak_type": "abrupt",
            "leak_start_time": 12427,
            "leak_end_time": 16046,
            "leak_peak_time": 12427
        }
    ],
    "475": [
        {
            "node_id": "10",
            "leak_diameter": 0.143473498295,
            "leak_type": "incipient",
            "leak_start_time": 1177,
            "leak_end_time": 7180,
            "leak_peak_time": 6312
        },
        {
            "node_id": "22",
            "leak_diameter": 0.197012712536,
            "leak_type": "abrupt",
            "leak_start_time": 13621,
            "leak_end_time": 14283,
            "leak_peak_time": 13621
        }
    ],
    "477": [
        {
            "node_id": "13",
            "leak_diameter": 0.0440392174384,
            "leak_type": "abrupt",
            "leak_start_time": 3107,
            "leak_end_time": 8207,
            "leak_peak_time": 3107
        }
    ],
    "478": [
        {
            "node_id": "12",
            "leak_diameter": 0.0834363898188,
            "leak_type": "incipient",
            "leak_start_time": 10848,
            "leak_end_time": 14018,
            "leak_peak_time": 11778
        },
        {
            "node_id": "31",
            "leak_diameter": 0.096616251708,
            "leak_type": "incipient",
            "leak_start_time": 399,
            "leak_end_time": 7059,
            "leak_peak_time": 5775
        }
    ],
    "479": [
        {
            "node_id": "13",
            "leak_diameter": 0.193139467119,
            "leak_type": "incipient",
            "leak_start_time": 9218,
            "leak_end_time": 12147,
            "leak_peak_time": 10117
        }
    ],
    "481": [
        {
            "node_id": "13",
            "leak_diameter": 0.0968422242982,
            "leak_type": "abrupt",
            "leak_start_time": 8482,
            "leak_end_time": 15461,
            "leak_peak_time": 8482
        }
    ],
    "482": [
        {
            "node_id": "10",
            "leak_diameter": 0.189600794333,
            "leak_type": "abrupt",
            "leak_start_time": 17184,
            "leak_end_time": 17321,
            "leak_peak_time": 17184
        }
    ],
    "483": [
        {
            "node_id": "13",
            "leak_diameter": 0.15482950951,
            "leak_type": "incipient",
            "leak_start_time": 7163,
            "leak_end_time": 14788,
            "leak_peak_time": 11236
        }
    ],
    "484": [
        {
            "node_id": "23",
            "leak_diameter": 0.0838147418684,
            "leak_type": "incipient",
            "leak_start_time": 6822,
            "leak_end_time": 8852,
            "leak_peak_time": 8782
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0609862861767,
            "leak_type": "abrupt",
            "leak_start_time": 4009,
            "leak_end_time": 8778,
            "leak_peak_time": 4009
        }
    ],
    "485": [
        {
            "node_id": "10",
            "leak_diameter": 0.113820182504,
            "leak_type": "incipient",
            "leak_start_time": 17231,
            "leak_end_time": 17233,
            "leak_peak_time": 17233
        }
    ],
    "486": [
        {
            "node_id": "32",
            "leak_diameter": 0.0432537176538,
            "leak_type": "incipient",
            "leak_start_time": 8994,
            "leak_end_time": 9801,
            "leak_peak_time": 9008
        }
    ],
    "487": [
        {
            "node_id": "22",
            "leak_diameter": 0.174561562981,
            "leak_type": "abrupt",
            "leak_start_time": 4691,
            "leak_end_time": 14798,
            "leak_peak_time": 4691
        },
        {
            "node_id": "12",
            "leak_diameter": 0.168023561116,
            "leak_type": "incipient",
            "leak_start_time": 1206,
            "leak_end_time": 7898,
            "leak_peak_time": 7763
        }
    ],
    "488": [
        {
            "node_id": "12",
            "leak_diameter": 0.0874963760922,
            "leak_type": "incipient",
            "leak_start_time": 3913,
            "leak_end_time": 10348,
            "leak_peak_time": 5810
        }
    ],
    "489": [
        {
            "node_id": "10",
            "leak_diameter": 0.076967005286,
            "leak_type": "incipient",
            "leak_start_time": 1079,
            "leak_end_time": 14694,
            "leak_peak_time": 2103
        }
    ],
    "490": [
        {
            "node_id": "13",
            "leak_diameter": 0.141107418259,
            "leak_type": "incipient",
            "leak_start_time": 2788,
            "leak_end_time": 15306,
            "leak_peak_time": 12676
        }
    ],
    "491": [
        {
            "node_id": "23",
            "leak_diameter": 0.0566171592905,
            "leak_type": "incipient",
            "leak_start_time": 17182,
            "leak_end_time": 17401,
            "leak_peak_time": 17389
        }
    ],
    "492": [
        {
            "node_id": "12",
            "leak_diameter": 0.114902003455,
            "leak_type": "abrupt",
            "leak_start_time": 13215,
            "leak_end_time": 13906,
            "leak_peak_time": 13215
        }
    ],
    "493": [
        {
            "node_id": "2",
            "leak_diameter": 0.0355684943158,
            "leak_type": "abrupt",
            "leak_start_time": 4757,
            "leak_end_time": 11637,
            "leak_peak_time": 4757
        }
    ],
    "494": [
        {
            "node_id": "32",
            "leak_diameter": 0.173997636913,
            "leak_type": "incipient",
            "leak_start_time": 812,
            "leak_end_time": 12475,
            "leak_peak_time": 9150
        }
    ],
    "495": [
        {
            "node_id": "10",
            "leak_diameter": 0.177957622372,
            "leak_type": "incipient",
            "leak_start_time": 11712,
            "leak_end_time": 15601,
            "leak_peak_time": 14188
        }
    ],
    "496": [
        {
            "node_id": "31",
            "leak_diameter": 0.164933054315,
            "leak_type": "incipient",
            "leak_start_time": 17218,
            "leak_end_time": 17360,
            "leak_peak_time": 17305
        }
    ],
    "497": [
        {
            "node_id": "10",
            "leak_diameter": 0.161290931364,
            "leak_type": "incipient",
            "leak_start_time": 13703,
            "leak_end_time": 17186,
            "leak_peak_time": 13986
        },
        {
            "node_id": "12",
            "leak_diameter": 0.0531297939237,
            "leak_type": "incipient",
            "leak_start_time": 11530,
            "leak_end_time": 17132,
            "leak_peak_time": 13455
        }
    ],
    "498": [
        {
            "node_id": "2",
            "leak_diameter": 0.0660185583444,
            "leak_type": "abrupt",
            "leak_start_time": 16230,
            "leak_end_time": 16704,
            "leak_peak_time": 16230
        }
    ],
    "500": [
        {
            "node_id": "23",
            "leak_diameter": 0.187921477956,
            "leak_type": "abrupt",
            "leak_start_time": 4429,
            "leak_end_time": 12263,
            "leak_peak_time": 4429
        }
    ],
    "501": [
        {
            "node_id": "23",
            "leak_diameter": 0.0555543916171,
            "leak_type": "incipient",
            "leak_start_time": 6518,
            "leak_end_time": 8016,
            "leak_peak_time": 6840
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0926740816135,
            "leak_type": "abrupt",
            "leak_start_time": 10424,
            "leak_end_time": 12014,
            "leak_peak_time": 10424
        }
    ],
    "505": [
        {
            "node_id": "21",
            "leak_diameter": 0.17914783836,
            "leak_type": "abrupt",
            "leak_start_time": 6317,
            "leak_end_time": 10190,
            "leak_peak_time": 6317
        }
    ],
    "506": [
        {
            "node_id": "10",
            "leak_diameter": 0.199454885609,
            "leak_type": "abrupt",
            "leak_start_time": 1027,
            "leak_end_time": 6404,
            "leak_peak_time": 1027
        }
    ],
    "507": [
        {
            "node_id": "31",
            "leak_diameter": 0.0582004949779,
            "leak_type": "incipient",
            "leak_start_time": 1121,
            "leak_end_time": 7031,
            "leak_peak_time": 3576
        }
    ],
    "508": [
        {
            "node_id": "21",
            "leak_diameter": 0.0250790401628,
            "leak_type": "incipient",
            "leak_start_time": 13716,
            "leak_end_time": 13972,
            "leak_peak_time": 13806
        }
    ],
    "510": [
        {
            "node_id": "22",
            "leak_diameter": 0.173196140988,
            "leak_type": "abrupt",
            "leak_start_time": 7421,
            "leak_end_time": 14600,
            "leak_peak_time": 7421
        }
    ],
    "511": [
        {
            "node_id": "22",
            "leak_diameter": 0.0219266337509,
            "leak_type": "abrupt",
            "leak_start_time": 8270,
            "leak_end_time": 8559,
            "leak_peak_time": 8270
        }
    ],
    "512": [
        {
            "node_id": "23",
            "leak_diameter": 0.134171201457,
            "leak_type": "abrupt",
            "leak_start_time": 10195,
            "leak_end_time": 17404,
            "leak_peak_time": 10195
        }
    ],
    "513": [
        {
            "node_id": "12",
            "leak_diameter": 0.0714957332281,
            "leak_type": "incipient",
            "leak_start_time": 7978,
            "leak_end_time": 16817,
            "leak_peak_time": 10145
        },
        {
            "node_id": "13",
            "leak_diameter": 0.077048646892,
            "leak_type": "incipient",
            "leak_start_time": 13419,
            "leak_end_time": 14493,
            "leak_peak_time": 13782
        }
    ],
    "514": [
        {
            "node_id": "23",
            "leak_diameter": 0.0907990117664,
            "leak_type": "incipient",
            "leak_start_time": 5366,
            "leak_end_time": 16228,
            "leak_peak_time": 5413
        }
    ],
    "515": [
        {
            "node_id": "22",
            "leak_diameter": 0.0391420013137,
            "leak_type": "abrupt",
            "leak_start_time": 7010,
            "leak_end_time": 13120,
            "leak_peak_time": 7010
        }
    ],
    "518": [
        {
            "node_id": "31",
            "leak_diameter": 0.0253671011543,
            "leak_type": "incipient",
            "leak_start_time": 2628,
            "leak_end_time": 13075,
            "leak_peak_time": 5120
        }
    ],
    "519": [
        {
            "node_id": "2",
            "leak_diameter": 0.0960552308616,
            "leak_type": "abrupt",
            "leak_start_time": 11276,
            "leak_end_time": 12560,
            "leak_peak_time": 11276
        }
    ],
    "520": [
        {
            "node_id": "21",
            "leak_diameter": 0.0295967672632,
            "leak_type": "abrupt",
            "leak_start_time": 16233,
            "leak_end_time": 16249,
            "leak_peak_time": 16233
        },
        {
            "node_id": "31",
            "leak_diameter": 0.146359355192,
            "leak_type": "incipient",
            "leak_start_time": 10137,
            "leak_end_time": 12708,
            "leak_peak_time": 12707
        }
    ],
    "521": [
        {
            "node_id": "32",
            "leak_diameter": 0.0879089542672,
            "leak_type": "abrupt",
            "leak_start_time": 11524,
            "leak_end_time": 14054,
            "leak_peak_time": 11524
        },
        {
            "node_id": "31",
            "leak_diameter": 0.149822557413,
            "leak_type": "abrupt",
            "leak_start_time": 6163,
            "leak_end_time": 6227,
            "leak_peak_time": 6163
        }
    ],
    "523": [
        {
            "node_id": "22",
            "leak_diameter": 0.130209646317,
            "leak_type": "incipient",
            "leak_start_time": 5505,
            "leak_end_time": 9215,
            "leak_peak_time": 6239
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0713988537805,
            "leak_type": "abrupt",
            "leak_start_time": 15279,
            "leak_end_time": 15634,
            "leak_peak_time": 15279
        }
    ],
    "524": [
        {
            "node_id": "23",
            "leak_diameter": 0.0390012132356,
            "leak_type": "incipient",
            "leak_start_time": 10938,
            "leak_end_time": 13135,
            "leak_peak_time": 11115
        }
    ],
    "525": [
        {
            "node_id": "22",
            "leak_diameter": 0.108061253529,
            "leak_type": "abrupt",
            "leak_start_time": 2688,
            "leak_end_time": 15379,
            "leak_peak_time": 2688
        },
        {
            "node_id": "12",
            "leak_diameter": 0.0674120028466,
            "leak_type": "abrupt",
            "leak_start_time": 13705,
            "leak_end_time": 14064,
            "leak_peak_time": 13705
        }
    ],
    "526": [
        {
            "node_id": "21",
            "leak_diameter": 0.169780150751,
            "leak_type": "abrupt",
            "leak_start_time": 7272,
            "leak_end_time": 11031,
            "leak_peak_time": 7272
        },
        {
            "node_id": "32",
            "leak_diameter": 0.112345516214,
            "leak_type": "abrupt",
            "leak_start_time": 954,
            "leak_end_time": 4958,
            "leak_peak_time": 954
        }
    ],
    "527": [
        {
            "node_id": "13",
            "leak_diameter": 0.066670206246,
            "leak_type": "incipient",
            "leak_start_time": 4320,
            "leak_end_time": 15027,
            "leak_peak_time": 11583
        },
        {
            "node_id": "32",
            "leak_diameter": 0.194515667395,
            "leak_type": "abrupt",
            "leak_start_time": 16982,
            "leak_end_time": 17506,
            "leak_peak_time": 16982
        }
    ],
    "528": [
        {
            "node_id": "10",
            "leak_diameter": 0.138102110377,
            "leak_type": "incipient",
            "leak_start_time": 9069,
            "leak_end_time": 17302,
            "leak_peak_time": 15653
        }
    ],
    "529": [
        {
            "node_id": "22",
            "leak_diameter": 0.0937531761272,
            "leak_type": "abrupt",
            "leak_start_time": 10802,
            "leak_end_time": 11338,
            "leak_peak_time": 10802
        },
        {
            "node_id": "12",
            "leak_diameter": 0.115413113499,
            "leak_type": "abrupt",
            "leak_start_time": 6523,
            "leak_end_time": 17338,
            "leak_peak_time": 6523
        }
    ],
    "530": [
        {
            "node_id": "2",
            "leak_diameter": 0.133242220253,
            "leak_type": "incipient",
            "leak_start_time": 7852,
            "leak_end_time": 11663,
            "leak_peak_time": 9821
        }
    ],
    "531": [
        {
            "node_id": "21",
            "leak_diameter": 0.125627361159,
            "leak_type": "incipient",
            "leak_start_time": 3769,
            "leak_end_time": 5258,
            "leak_peak_time": 5190
        }
    ],
    "532": [
        {
            "node_id": "23",
            "leak_diameter": 0.0203215063187,
            "leak_type": "incipient",
            "leak_start_time": 4967,
            "leak_end_time": 6022,
            "leak_peak_time": 5407
        },
        {
            "node_id": "31",
            "leak_diameter": 0.105398839683,
            "leak_type": "incipient",
            "leak_start_time": 17389,
            "leak_end_time": 17411,
            "leak_peak_time": 17409
        }
    ],
    "533": [
        {
            "node_id": "10",
            "leak_diameter": 0.0228439608626,
            "leak_type": "abrupt",
            "leak_start_time": 3539,
            "leak_end_time": 15600,
            "leak_peak_time": 3539
        }
    ],
    "537": [
        {
            "node_id": "21",
            "leak_diameter": 0.163578884952,
            "leak_type": "abrupt",
            "leak_start_time": 5643,
            "leak_end_time": 12218,
            "leak_peak_time": 5643
        },
        {
            "node_id": "31",
            "leak_diameter": 0.190585105678,
            "leak_type": "abrupt",
            "leak_start_time": 3248,
            "leak_end_time": 11990,
            "leak_peak_time": 3248
        }
    ],
    "538": [
        {
            "node_id": "23",
            "leak_diameter": 0.117230517396,
            "leak_type": "incipient",
            "leak_start_time": 2165,
            "leak_end_time": 10800,
            "leak_peak_time": 9956
        }
    ],
    "539": [
        {
            "node_id": "10",
            "leak_diameter": 0.0482145827921,
            "leak_type": "incipient",
            "leak_start_time": 1001,
            "leak_end_time": 3495,
            "leak_peak_time": 3452
        }
    ],
    "540": [
        {
            "node_id": "21",
            "leak_diameter": 0.127887842542,
            "leak_type": "abrupt",
            "leak_start_time": 1557,
            "leak_end_time": 5574,
            "leak_peak_time": 1557
        }
    ],
    "541": [
        {
            "node_id": "21",
            "leak_diameter": 0.175611104407,
            "leak_type": "incipient",
            "leak_start_time": 13190,
            "leak_end_time": 13692,
            "leak_peak_time": 13216
        }
    ],
    "542": [
        {
            "node_id": "21",
            "leak_diameter": 0.194153674966,
            "leak_type": "incipient",
            "leak_start_time": 1511,
            "leak_end_time": 2612,
            "leak_peak_time": 2586
        }
    ],
    "543": [
        {
            "node_id": "12",
            "leak_diameter": 0.158757189588,
            "leak_type": "incipient",
            "leak_start_time": 8414,
            "leak_end_time": 9783,
            "leak_peak_time": 8424
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0867888691043,
            "leak_type": "incipient",
            "leak_start_time": 3282,
            "leak_end_time": 15424,
            "leak_peak_time": 3406
        }
    ],
    "544": [
        {
            "node_id": "22",
            "leak_diameter": 0.134322470051,
            "leak_type": "incipient",
            "leak_start_time": 5518,
            "leak_end_time": 16737,
            "leak_peak_time": 8450
        }
    ],
    "545": [
        {
            "node_id": "13",
            "leak_diameter": 0.0233154186642,
            "leak_type": "incipient",
            "leak_start_time": 7494,
            "leak_end_time": 15302,
            "leak_peak_time": 8482
        }
    ],
    "546": [
        {
            "node_id": "32",
            "leak_diameter": 0.0709762886663,
            "leak_type": "incipient",
            "leak_start_time": 17121,
            "leak_end_time": 17363,
            "leak_peak_time": 17178
        }
    ],
    "548": [
        {
            "node_id": "21",
            "leak_diameter": 0.125247015895,
            "leak_type": "abrupt",
            "leak_start_time": 7982,
            "leak_end_time": 8751,
            "leak_peak_time": 7982
        }
    ],
    "549": [
        {
            "node_id": "21",
            "leak_diameter": 0.14784435427,
            "leak_type": "abrupt",
            "leak_start_time": 866,
            "leak_end_time": 2893,
            "leak_peak_time": 866
        }
    ],
    "550": [
        {
            "node_id": "32",
            "leak_diameter": 0.165279392788,
            "leak_type": "abrupt",
            "leak_start_time": 9352,
            "leak_end_time": 13866,
            "leak_peak_time": 9352
        }
    ],
    "551": [
        {
            "node_id": "23",
            "leak_diameter": 0.0777445552784,
            "leak_type": "incipient",
            "leak_start_time": 1060,
            "leak_end_time": 2029,
            "leak_peak_time": 1215
        }
    ],
    "552": [
        {
            "node_id": "22",
            "leak_diameter": 0.188715249361,
            "leak_type": "incipient",
            "leak_start_time": 12541,
            "leak_end_time": 13205,
            "leak_peak_time": 13038
        }
    ],
    "553": [
        {
            "node_id": "10",
            "leak_diameter": 0.0375720563013,
            "leak_type": "abrupt",
            "leak_start_time": 14651,
            "leak_end_time": 16619,
            "leak_peak_time": 14651
        }
    ],
    "554": [
        {
            "node_id": "10",
            "leak_diameter": 0.150979395439,
            "leak_type": "incipient",
            "leak_start_time": 1369,
            "leak_end_time": 15901,
            "leak_peak_time": 5438
        },
        {
            "node_id": "32",
            "leak_diameter": 0.184350212713,
            "leak_type": "abrupt",
            "leak_start_time": 1430,
            "leak_end_time": 10436,
            "leak_peak_time": 1430
        }
    ],
    "555": [
        {
            "node_id": "22",
            "leak_diameter": 0.110459233585,
            "leak_type": "abrupt",
            "leak_start_time": 409,
            "leak_end_time": 5928,
            "leak_peak_time": 409
        }
    ],
    "556": [
        {
            "node_id": "13",
            "leak_diameter": 0.0380416504228,
            "leak_type": "abrupt",
            "leak_start_time": 7129,
            "leak_end_time": 8582,
            "leak_peak_time": 7129
        },
        {
            "node_id": "32",
            "leak_diameter": 0.151396181839,
            "leak_type": "incipient",
            "leak_start_time": 11328,
            "leak_end_time": 12034,
            "leak_peak_time": 11855
        }
    ],
    "557": [
        {
            "node_id": "12",
            "leak_diameter": 0.102745830172,
            "leak_type": "abrupt",
            "leak_start_time": 744,
            "leak_end_time": 8279,
            "leak_peak_time": 744
        }
    ],
    "558": [
        {
            "node_id": "10",
            "leak_diameter": 0.020319405881,
            "leak_type": "abrupt",
            "leak_start_time": 5555,
            "leak_end_time": 16886,
            "leak_peak_time": 5555
        }
    ],
    "560": [
        {
            "node_id": "10",
            "leak_diameter": 0.17134930072,
            "leak_type": "incipient",
            "leak_start_time": 451,
            "leak_end_time": 3919,
            "leak_peak_time": 2201
        }
    ],
    "561": [
        {
            "node_id": "12",
            "leak_diameter": 0.0697600487053,
            "leak_type": "incipient",
            "leak_start_time": 5361,
            "leak_end_time": 5672,
            "leak_peak_time": 5526
        },
        {
            "node_id": "32",
            "leak_diameter": 0.178214777425,
            "leak_type": "abrupt",
            "leak_start_time": 10178,
            "leak_end_time": 10453,
            "leak_peak_time": 10178
        }
    ],
    "562": [
        {
            "node_id": "12",
            "leak_diameter": 0.179024670999,
            "leak_type": "incipient",
            "leak_start_time": 8425,
            "leak_end_time": 12481,
            "leak_peak_time": 11744
        }
    ],
    "565": [
        {
            "node_id": "32",
            "leak_diameter": 0.111300479089,
            "leak_type": "incipient",
            "leak_start_time": 12290,
            "leak_end_time": 15618,
            "leak_peak_time": 12718
        }
    ],
    "566": [
        {
            "node_id": "21",
            "leak_diameter": 0.159573255445,
            "leak_type": "incipient",
            "leak_start_time": 9942,
            "leak_end_time": 13499,
            "leak_peak_time": 10855
        },
        {
            "node_id": "23",
            "leak_diameter": 0.034405494703,
            "leak_type": "incipient",
            "leak_start_time": 13347,
            "leak_end_time": 17171,
            "leak_peak_time": 14142
        }
    ],
    "567": [
        {
            "node_id": "12",
            "leak_diameter": 0.0837169388249,
            "leak_type": "incipient",
            "leak_start_time": 11201,
            "leak_end_time": 12823,
            "leak_peak_time": 11253
        }
    ],
    "569": [
        {
            "node_id": "21",
            "leak_diameter": 0.115042063151,
            "leak_type": "abrupt",
            "leak_start_time": 12608,
            "leak_end_time": 16711,
            "leak_peak_time": 12608
        },
        {
            "node_id": "23",
            "leak_diameter": 0.138365049341,
            "leak_type": "incipient",
            "leak_start_time": 7719,
            "leak_end_time": 12754,
            "leak_peak_time": 11644
        }
    ],
    "570": [
        {
            "node_id": "32",
            "leak_diameter": 0.142498986776,
            "leak_type": "abrupt",
            "leak_start_time": 4494,
            "leak_end_time": 12987,
            "leak_peak_time": 4494
        }
    ],
    "571": [
        {
            "node_id": "31",
            "leak_diameter": 0.128453254432,
            "leak_type": "incipient",
            "leak_start_time": 15947,
            "leak_end_time": 16226,
            "leak_peak_time": 16214
        }
    ],
    "572": [
        {
            "node_id": "32",
            "leak_diameter": 0.1962529675,
            "leak_type": "incipient",
            "leak_start_time": 9098,
            "leak_end_time": 15167,
            "leak_peak_time": 9752
        }
    ],
    "573": [
        {
            "node_id": "32",
            "leak_diameter": 0.11924395659,
            "leak_type": "abrupt",
            "leak_start_time": 12907,
            "leak_end_time": 16849,
            "leak_peak_time": 12907
        }
    ],
    "574": [
        {
            "node_id": "13",
            "leak_diameter": 0.106499750347,
            "leak_type": "abrupt",
            "leak_start_time": 11199,
            "leak_end_time": 14316,
            "leak_peak_time": 11199
        }
    ],
    "575": [
        {
            "node_id": "21",
            "leak_diameter": 0.0250666682707,
            "leak_type": "abrupt",
            "leak_start_time": 3336,
            "leak_end_time": 13239,
            "leak_peak_time": 3336
        }
    ],
    "576": [
        {
            "node_id": "31",
            "leak_diameter": 0.178758076824,
            "leak_type": "abrupt",
            "leak_start_time": 7908,
            "leak_end_time": 17187,
            "leak_peak_time": 7908
        }
    ],
    "577": [
        {
            "node_id": "23",
            "leak_diameter": 0.1910285908515233,
            "leak_type": "incipient",
            "leak_start_time": 3693,
            "leak_end_time": 7375,
            "leak_peak_time": 4513
        }
    ],
    "578": [
        {
            "node_id": "2",
            "leak_diameter": 0.1831865406173088,
            "leak_type": "incipient",
            "leak_start_time": 10291,
            "leak_end_time": 16680,
            "leak_peak_time": 13588
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0739505524519,
            "leak_type": "abrupt",
            "leak_start_time": 1275,
            "leak_end_time": 13014,
            "leak_peak_time": 1275
        }
    ],
    "579": [
        {
            "node_id": "23",
            "leak_diameter": 0.175653391305,
            "leak_type": "abrupt",
            "leak_start_time": 13306,
            "leak_end_time": 16832,
            "leak_peak_time": 13306
        }
    ],
    "580": [
        {
            "node_id": "23",
            "leak_diameter": 0.151031961689,
            "leak_type": "abrupt",
            "leak_start_time": 3778,
            "leak_end_time": 17482,
            "leak_peak_time": 3778
        }
    ],
    "581": [
        {
            "node_id": "12",
            "leak_diameter": 0.125898000943,
            "leak_type": "abrupt",
            "leak_start_time": 15762,
            "leak_end_time": 16257,
            "leak_peak_time": 15762
        },
        {
            "node_id": "32",
            "leak_diameter": 0.020322665571848437,
            "leak_type": "incipient",
            "leak_start_time": 5583,
            "leak_end_time": 14246,
            "leak_peak_time": 13826
        }
    ],
    "583": [
        {
            "node_id": "2",
            "leak_diameter": 0.13220922182306133,
            "leak_type": "incipient",
            "leak_start_time": 16915,
            "leak_end_time": 17015,
            "leak_peak_time": 16956
        }
    ],
    "584": [
        {
            "node_id": "32",
            "leak_diameter": 0.17054093721527377,
            "leak_type": "incipient",
            "leak_start_time": 17055,
            "leak_end_time": 17474,
            "leak_peak_time": 17161
        }
    ],
    "585": [
        {
            "node_id": "23",
            "leak_diameter": 0.139533504809,
            "leak_type": "abrupt",
            "leak_start_time": 612,
            "leak_end_time": 14430,
            "leak_peak_time": 612
        }
    ],
    "586": [
        {
            "node_id": "2",
            "leak_diameter": 0.0467157418349,
            "leak_type": "abrupt",
            "leak_start_time": 8105,
            "leak_end_time": 16419,
            "leak_peak_time": 8105
        },
        {
            "node_id": "32",
            "leak_diameter": 0.19185605776413392,
            "leak_type": "incipient",
            "leak_start_time": 17098,
            "leak_end_time": 17180,
            "leak_peak_time": 17146
        }
    ],
    "587": [
        {
            "node_id": "12",
            "leak_diameter": 0.0612916435426,
            "leak_type": "abrupt",
            "leak_start_time": 8523,
            "leak_end_time": 10576,
            "leak_peak_time": 8523
        }
    ],
    "589": [
        {
            "node_id": "32",
            "leak_diameter": 0.04094488012635748,
            "leak_type": "incipient",
            "leak_start_time": 9505,
            "leak_end_time": 9510,
            "leak_peak_time": 9506
        }
    ],
    "590": [
        {
            "node_id": "12",
            "leak_diameter": 0.12267484411842125,
            "leak_type": "incipient",
            "leak_start_time": 16116,
            "leak_end_time": 16784,
            "leak_peak_time": 16758
        }
    ],
    "591": [
        {
            "node_id": "13",
            "leak_diameter": 0.149254280993143,
            "leak_type": "incipient",
            "leak_start_time": 3888,
            "leak_end_time": 10522,
            "leak_peak_time": 7855
        },
        {
            "node_id": "2",
            "leak_diameter": 0.09593614493349908,
            "leak_type": "incipient",
            "leak_start_time": 15906,
            "leak_end_time": 16811,
            "leak_peak_time": 16278
        }
    ],
    "593": [
        {
            "node_id": "21",
            "leak_diameter": 0.10262544634163352,
            "leak_type": "incipient",
            "leak_start_time": 14006,
            "leak_end_time": 15008,
            "leak_peak_time": 14315
        }
    ],
    "594": [
        {
            "node_id": "31",
            "leak_diameter": 0.0539402864349,
            "leak_type": "abrupt",
            "leak_start_time": 2400,
            "leak_end_time": 11971,
            "leak_peak_time": 2400
        }
    ],
    "596": [
        {
            "node_id": "12",
            "leak_diameter": 0.171857959083,
            "leak_type": "abrupt",
            "leak_start_time": 1907,
            "leak_end_time": 13377,
            "leak_peak_time": 1907
        }
    ],
    "597": [
        {
            "node_id": "10",
            "leak_diameter": 0.114656326315,
            "leak_type": "abrupt",
            "leak_start_time": 8128,
            "leak_end_time": 13840,
            "leak_peak_time": 8128
        },
        {
            "node_id": "13",
            "leak_diameter": 0.14771575552258842,
            "leak_type": "incipient",
            "leak_start_time": 11916,
            "leak_end_time": 13286,
            "leak_peak_time": 13196
        }
    ],
    "598": [
        {
            "node_id": "22",
            "leak_diameter": 0.101344361314,
            "leak_type": "abrupt",
            "leak_start_time": 7741,
            "leak_end_time": 8575,
            "leak_peak_time": 7741
        }
    ],
    "599": [
        {
            "node_id": "21",
            "leak_diameter": 0.0920283927075,
            "leak_type": "abrupt",
            "leak_start_time": 6340,
            "leak_end_time": 10842,
            "leak_peak_time": 6340
        }
    ],
    "602": [
        {
            "node_id": "13",
            "leak_diameter": 0.07759372641655421,
            "leak_type": "incipient",
            "leak_start_time": 12831,
            "leak_end_time": 17001,
            "leak_peak_time": 16975
        }
    ],
    "605": [
        {
            "node_id": "21",
            "leak_diameter": 0.0620627565944,
            "leak_type": "abrupt",
            "leak_start_time": 12354,
            "leak_end_time": 13616,
            "leak_peak_time": 12354
        }
    ],
    "606": [
        {
            "node_id": "32",
            "leak_diameter": 0.0417388357678,
            "leak_type": "abrupt",
            "leak_start_time": 3891,
            "leak_end_time": 14446,
            "leak_peak_time": 3891
        }
    ],
    "608": [
        {
            "node_id": "22",
            "leak_diameter": 0.148273327931,
            "leak_type": "abrupt",
            "leak_start_time": 3282,
            "leak_end_time": 3525,
            "leak_peak_time": 3282
        }
    ],
    "609": [
        {
            "node_id": "21",
            "leak_diameter": 0.0874981188239,
            "leak_type": "abrupt",
            "leak_start_time": 6486,
            "leak_end_time": 13827,
            "leak_peak_time": 6486
        }
    ],
    "610": [
        {
            "node_id": "13",
            "leak_diameter": 0.117769639933,
            "leak_type": "abrupt",
            "leak_start_time": 10641,
            "leak_end_time": 16933,
            "leak_peak_time": 10641
        },
        {
            "node_id": "32",
            "leak_diameter": 0.159408851089,
            "leak_type": "abrupt",
            "leak_start_time": 11988,
            "leak_end_time": 14382,
            "leak_peak_time": 11988
        }
    ],
    "611": [
        {
            "node_id": "13",
            "leak_diameter": 0.16721585244694429,
            "leak_type": "incipient",
            "leak_start_time": 2666,
            "leak_end_time": 9148,
            "leak_peak_time": 8118
        }
    ],
    "614": [
        {
            "node_id": "23",
            "leak_diameter": 0.06438189603925014,
            "leak_type": "incipient",
            "leak_start_time": 8117,
            "leak_end_time": 8524,
            "leak_peak_time": 8436
        }
    ],
    "616": [
        {
            "node_id": "22",
            "leak_diameter": 0.029617141247283107,
            "leak_type": "incipient",
            "leak_start_time": 1642,
            "leak_end_time": 5474,
            "leak_peak_time": 2815
        }
    ],
    "617": [
        {
            "node_id": "2",
            "leak_diameter": 0.05994326227495411,
            "leak_type": "incipient",
            "leak_start_time": 10568,
            "leak_end_time": 15841,
            "leak_peak_time": 15016
        },
        {
            "node_id": "31",
            "leak_diameter": 0.053489863128,
            "leak_type": "abrupt",
            "leak_start_time": 3907,
            "leak_end_time": 6664,
            "leak_peak_time": 3907
        }
    ],
    "619": [
        {
            "node_id": "12",
            "leak_diameter": 0.12467423249129443,
            "leak_type": "incipient",
            "leak_start_time": 9382,
            "leak_end_time": 10906,
            "leak_peak_time": 9474
        }
    ],
    "620": [
        {
            "node_id": "2",
            "leak_diameter": 0.0665358236502,
            "leak_type": "abrupt",
            "leak_start_time": 2024,
            "leak_end_time": 15351,
            "leak_peak_time": 2024
        },
        {
            "node_id": "23",
            "leak_diameter": 0.18363618988473776,
            "leak_type": "incipient",
            "leak_start_time": 3506,
            "leak_end_time": 17093,
            "leak_peak_time": 13332
        }
    ],
    "621": [
        {
            "node_id": "21",
            "leak_diameter": 0.18576980568,
            "leak_type": "abrupt",
            "leak_start_time": 5599,
            "leak_end_time": 15742,
            "leak_peak_time": 5599
        }
    ],
    "622": [
        {
            "node_id": "22",
            "leak_diameter": 0.14687594351374117,
            "leak_type": "incipient",
            "leak_start_time": 5241,
            "leak_end_time": 9308,
            "leak_peak_time": 7965
        },
        {
            "node_id": "13",
            "leak_diameter": 0.124012550401,
            "leak_type": "abrupt",
            "leak_start_time": 17429,
            "leak_end_time": 17469,
            "leak_peak_time": 17429
        }
    ],
    "626": [
        {
            "node_id": "21",
            "leak_diameter": 0.137655335807,
            "leak_type": "abrupt",
            "leak_start_time": 2576,
            "leak_end_time": 6224,
            "leak_peak_time": 2576
        }
    ],
    "627": [
        {
            "node_id": "13",
            "leak_diameter": 0.061340743859155666,
            "leak_type": "incipient",
            "leak_start_time": 4471,
            "leak_end_time": 8948,
            "leak_peak_time": 6939
        }
    ],
    "628": [
        {
            "node_id": "12",
            "leak_diameter": 0.120226541439,
            "leak_type": "abrupt",
            "leak_start_time": 16709,
            "leak_end_time": 17371,
            "leak_peak_time": 16709
        }
    ],
    "629": [
        {
            "node_id": "22",
            "leak_diameter": 0.152110792802,
            "leak_type": "abrupt",
            "leak_start_time": 9677,
            "leak_end_time": 14835,
            "leak_peak_time": 9677
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0873725790484,
            "leak_type": "abrupt",
            "leak_start_time": 2557,
            "leak_end_time": 12371,
            "leak_peak_time": 2557
        }
    ],
    "630": [
        {
            "node_id": "13",
            "leak_diameter": 0.1592770593262754,
            "leak_type": "incipient",
            "leak_start_time": 4762,
            "leak_end_time": 12731,
            "leak_peak_time": 7372
        }
    ],
    "631": [
        {
            "node_id": "10",
            "leak_diameter": 0.061012082161,
            "leak_type": "abrupt",
            "leak_start_time": 8999,
            "leak_end_time": 14967,
            "leak_peak_time": 8999
        },
        {
            "node_id": "2",
            "leak_diameter": 0.0590412330931,
            "leak_type": "incipient",
            "leak_start_time": 5373,
            "leak_end_time": 17192,
            "leak_peak_time": 9422
        }
    ],
    "632": [
        {
            "node_id": "21",
            "leak_diameter": 0.0550603802934,
            "leak_type": "incipient",
            "leak_start_time": 11479,
            "leak_end_time": 15801,
            "leak_peak_time": 14232
        }
    ],
    "633": [
        {
            "node_id": "21",
            "leak_diameter": 0.100780928487,
            "leak_type": "incipient",
            "leak_start_time": 1610,
            "leak_end_time": 15639,
            "leak_peak_time": 4645
        },
        {
            "node_id": "2",
            "leak_diameter": 0.137001027412,
            "leak_type": "abrupt",
            "leak_start_time": 12698,
            "leak_end_time": 13257,
            "leak_peak_time": 12698
        }
    ],
    "634": [
        {
            "node_id": "31",
            "leak_diameter": 0.0412391819489,
            "leak_type": "incipient",
            "leak_start_time": 10193,
            "leak_end_time": 17175,
            "leak_peak_time": 12914
        }
    ],
    "635": [
        {
            "node_id": "13",
            "leak_diameter": 0.052381024836723855,
            "leak_type": "incipient",
            "leak_start_time": 15702,
            "leak_end_time": 15717,
            "leak_peak_time": 15712
        }
    ],
    "636": [
        {
            "node_id": "12",
            "leak_diameter": 0.0885491645439,
            "leak_type": "abrupt",
            "leak_start_time": 6854,
            "leak_end_time": 11083,
            "leak_peak_time": 6854
        },
        {
            "node_id": "21",
            "leak_diameter": 0.0962339448921808,
            "leak_type": "incipient",
            "leak_start_time": 15010,
            "leak_end_time": 16174,
            "leak_peak_time": 15719
        }
    ],
    "638": [
        {
            "node_id": "21",
            "leak_diameter": 0.156080601468,
            "leak_type": "abrupt",
            "leak_start_time": 11028,
            "leak_end_time": 13161,
            "leak_peak_time": 11028
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0476804362563,
            "leak_type": "abrupt",
            "leak_start_time": 8473,
            "leak_end_time": 9409,
            "leak_peak_time": 8473
        }
    ],
    "639": [
        {
            "node_id": "2",
            "leak_diameter": 0.03955814550257308,
            "leak_type": "incipient",
            "leak_start_time": 11610,
            "leak_end_time": 13376,
            "leak_peak_time": 13096
        },
        {
            "node_id": "31",
            "leak_diameter": 0.19388530387688882,
            "leak_type": "incipient",
            "leak_start_time": 15999,
            "leak_end_time": 17030,
            "leak_peak_time": 16612
        }
    ],
    "640": [
        {
            "node_id": "23",
            "leak_diameter": 0.1131559177859624,
            "leak_type": "incipient",
            "leak_start_time": 3231,
            "leak_end_time": 4347,
            "leak_peak_time": 3306
        }
    ],
    "641": [
        {
            "node_id": "10",
            "leak_diameter": 0.0985512173043,
            "leak_type": "abrupt",
            "leak_start_time": 14386,
            "leak_end_time": 14716,
            "leak_peak_time": 14386
        }
    ],
    "642": [
        {
            "node_id": "31",
            "leak_diameter": 0.196578817769,
            "leak_type": "abrupt",
            "leak_start_time": 15073,
            "leak_end_time": 15235,
            "leak_peak_time": 15073
        }
    ],
    "643": [
        {
            "node_id": "22",
            "leak_diameter": 0.145367109901,
            "leak_type": "abrupt",
            "leak_start_time": 13272,
            "leak_end_time": 15975,
            "leak_peak_time": 13272
        }
    ],
    "644": [
        {
            "node_id": "22",
            "leak_diameter": 0.08537232782299449,
            "leak_type": "incipient",
            "leak_start_time": 9449,
            "leak_end_time": 15230,
            "leak_peak_time": 14557
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0471537123107,
            "leak_type": "abrupt",
            "leak_start_time": 16889,
            "leak_end_time": 17100,
            "leak_peak_time": 16889
        }
    ],
    "646": [
        {
            "node_id": "21",
            "leak_diameter": 0.0505569745293,
            "leak_type": "abrupt",
            "leak_start_time": 16761,
            "leak_end_time": 17479,
            "leak_peak_time": 16761
        }
    ],
    "648": [
        {
            "node_id": "23",
            "leak_diameter": 0.13149704725035488,
            "leak_type": "incipient",
            "leak_start_time": 7237,
            "leak_end_time": 13173,
            "leak_peak_time": 12076
        },
        {
            "node_id": "31",
            "leak_diameter": 0.1920824672549811,
            "leak_type": "incipient",
            "leak_start_time": 5599,
            "leak_end_time": 9736,
            "leak_peak_time": 7469
        }
    ],
    "650": [
        {
            "node_id": "12",
            "leak_diameter": 0.11248083328091095,
            "leak_type": "incipient",
            "leak_start_time": 8989,
            "leak_end_time": 9309,
            "leak_peak_time": 9172
        }
    ],
    "651": [
        {
            "node_id": "13",
            "leak_diameter": 0.0950388041863403,
            "leak_type": "incipient",
            "leak_start_time": 14568,
            "leak_end_time": 17335,
            "leak_peak_time": 15248
        }
    ],
    "652": [
        {
            "node_id": "12",
            "leak_diameter": 0.09013865153642919,
            "leak_type": "incipient",
            "leak_start_time": 17473,
            "leak_end_time": 17479,
            "leak_peak_time": 17478
        }
    ],
    "654": [
        {
            "node_id": "32",
            "leak_diameter": 0.12176082068739164,
            "leak_type": "incipient",
            "leak_start_time": 16893,
            "leak_end_time": 17519,
            "leak_peak_time": 17404
        }
    ],
    "655": [
        {
            "node_id": "21",
            "leak_diameter": 0.08902923404719172,
            "leak_type": "incipient",
            "leak_start_time": 510,
            "leak_end_time": 2358,
            "leak_peak_time": 1327
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0935079008937,
            "leak_type": "abrupt",
            "leak_start_time": 15236,
            "leak_end_time": 15457,
            "leak_peak_time": 15236
        }
    ],
    "657": [
        {
            "node_id": "32",
            "leak_diameter": 0.0325225847557,
            "leak_type": "abrupt",
            "leak_start_time": 6470,
            "leak_end_time": 6546,
            "leak_peak_time": 6470
        }
    ],
    "658": [
        {
            "node_id": "21",
            "leak_diameter": 0.15574006108736171,
            "leak_type": "incipient",
            "leak_start_time": 13055,
            "leak_end_time": 14575,
            "leak_peak_time": 13120
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0593887262734,
            "leak_type": "abrupt",
            "leak_start_time": 6731,
            "leak_end_time": 6869,
            "leak_peak_time": 6731
        }
    ],
    "660": [
        {
            "node_id": "10",
            "leak_diameter": 0.06661815772876965,
            "leak_type": "incipient",
            "leak_start_time": 6840,
            "leak_end_time": 9727,
            "leak_peak_time": 7101
        }
    ],
    "661": [
        {
            "node_id": "21",
            "leak_diameter": 0.0732571707539,
            "leak_type": "abrupt",
            "leak_start_time": 10688,
            "leak_end_time": 14149,
            "leak_peak_time": 10688
        }
    ],
    "662": [
        {
            "node_id": "2",
            "leak_diameter": 0.0586076093362,
            "leak_type": "abrupt",
            "leak_start_time": 11661,
            "leak_end_time": 14691,
            "leak_peak_time": 11661
        }
    ],
    "663": [
        {
            "node_id": "23",
            "leak_diameter": 0.17474996501919451,
            "leak_type": "incipient",
            "leak_start_time": 15903,
            "leak_end_time": 16249,
            "leak_peak_time": 16234
        }
    ],
    "664": [
        {
            "node_id": "23",
            "leak_diameter": 0.08408976189698052,
            "leak_type": "incipient",
            "leak_start_time": 15425,
            "leak_end_time": 15503,
            "leak_peak_time": 15441
        }
    ],
    "665": [
        {
            "node_id": "32",
            "leak_diameter": 0.07771609447392767,
            "leak_type": "incipient",
            "leak_start_time": 5283,
            "leak_end_time": 13169,
            "leak_peak_time": 7133
        },
        {
            "node_id": "31",
            "leak_diameter": 0.052182943490076024,
            "leak_type": "incipient",
            "leak_start_time": 11862,
            "leak_end_time": 12963,
            "leak_peak_time": 11915
        }
    ],
    "666": [
        {
            "node_id": "2",
            "leak_diameter": 0.0552426974703,
            "leak_type": "abrupt",
            "leak_start_time": 12627,
            "leak_end_time": 13599,
            "leak_peak_time": 12627
        }
    ],
    "667": [
        {
            "node_id": "12",
            "leak_diameter": 0.1986806636289065,
            "leak_type": "incipient",
            "leak_start_time": 407,
            "leak_end_time": 3074,
            "leak_peak_time": 3002
        }
    ],
    "672": [
        {
            "node_id": "21",
            "leak_diameter": 0.11539459540352183,
            "leak_type": "incipient",
            "leak_start_time": 4216,
            "leak_end_time": 14840,
            "leak_peak_time": 12924
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0483015654945,
            "leak_type": "abrupt",
            "leak_start_time": 562,
            "leak_end_time": 7425,
            "leak_peak_time": 562
        }
    ],
    "674": [
        {
            "node_id": "31",
            "leak_diameter": 0.17522317497462073,
            "leak_type": "incipient",
            "leak_start_time": 14084,
            "leak_end_time": 15311,
            "leak_peak_time": 15118
        }
    ],
    "675": [
        {
            "node_id": "10",
            "leak_diameter": 0.045453836687647034,
            "leak_type": "incipient",
            "leak_start_time": 17404,
            "leak_end_time": 17413,
            "leak_peak_time": 17409
        }
    ],
    "676": [
        {
            "node_id": "13",
            "leak_diameter": 0.128369814657,
            "leak_type": "abrupt",
            "leak_start_time": 3095,
            "leak_end_time": 16906,
            "leak_peak_time": 3095
        }
    ],
    "677": [
        {
            "node_id": "12",
            "leak_diameter": 0.167684793446,
            "leak_type": "abrupt",
            "leak_start_time": 10713,
            "leak_end_time": 13094,
            "leak_peak_time": 10713
        }
    ],
    "679": [
        {
            "node_id": "21",
            "leak_diameter": 0.0488659590202,
            "leak_type": "abrupt",
            "leak_start_time": 5664,
            "leak_end_time": 12278,
            "leak_peak_time": 5664
        }
    ],
    "680": [
        {
            "node_id": "12",
            "leak_diameter": 0.10493750388388894,
            "leak_type": "incipient",
            "leak_start_time": 6262,
            "leak_end_time": 9777,
            "leak_peak_time": 9776
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0398875358348,
            "leak_type": "abrupt",
            "leak_start_time": 15632,
            "leak_end_time": 16292,
            "leak_peak_time": 15632
        }
    ],
    "681": [
        {
            "node_id": "22",
            "leak_diameter": 0.19096254636599008,
            "leak_type": "incipient",
            "leak_start_time": 7434,
            "leak_end_time": 9244,
            "leak_peak_time": 9099
        },
        {
            "node_id": "2",
            "leak_diameter": 0.179331598163,
            "leak_type": "abrupt",
            "leak_start_time": 350,
            "leak_end_time": 4295,
            "leak_peak_time": 350
        }
    ],
    "682": [
        {
            "node_id": "31",
            "leak_diameter": 0.0286859690993,
            "leak_type": "abrupt",
            "leak_start_time": 9189,
            "leak_end_time": 13717,
            "leak_peak_time": 9189
        }
    ],
    "683": [
        {
            "node_id": "23",
            "leak_diameter": 0.16326962506216916,
            "leak_type": "incipient",
            "leak_start_time": 17064,
            "leak_end_time": 17405,
            "leak_peak_time": 17332
        }
    ],
    "684": [
        {
            "node_id": "13",
            "leak_diameter": 0.09385430762990632,
            "leak_type": "incipient",
            "leak_start_time": 9853,
            "leak_end_time": 16692,
            "leak_peak_time": 15842
        },
        {
            "node_id": "31",
            "leak_diameter": 0.06278430355690488,
            "leak_type": "incipient",
            "leak_start_time": 1815,
            "leak_end_time": 5669,
            "leak_peak_time": 2087
        }
    ],
    "685": [
        {
            "node_id": "13",
            "leak_diameter": 0.117940678557,
            "leak_type": "abrupt",
            "leak_start_time": 14936,
            "leak_end_time": 17118,
            "leak_peak_time": 14936
        }
    ],
    "687": [
        {
            "node_id": "13",
            "leak_diameter": 0.14047627655,
            "leak_type": "abrupt",
            "leak_start_time": 16865,
            "leak_end_time": 17472,
            "leak_peak_time": 16865
        }
    ],
    "689": [
        {
            "node_id": "12",
            "leak_diameter": 0.195565416173,
            "leak_type": "abrupt",
            "leak_start_time": 14932,
            "leak_end_time": 16187,
            "leak_peak_time": 14932
        },
        {
            "node_id": "13",
            "leak_diameter": 0.14054209522,
            "leak_type": "abrupt",
            "leak_start_time": 12863,
            "leak_end_time": 14077,
            "leak_peak_time": 12863
        }
    ],
    "690": [
        {
            "node_id": "31",
            "leak_diameter": 0.177225460801,
            "leak_type": "abrupt",
            "leak_start_time": 9717,
            "leak_end_time": 13133,
            "leak_peak_time": 9717
        }
    ],
    "691": [
        {
            "node_id": "12",
            "leak_diameter": 0.04503492433471891,
            "leak_type": "incipient",
            "leak_start_time": 6467,
            "leak_end_time": 7721,
            "leak_peak_time": 7278
        },
        {
            "node_id": "23",
            "leak_diameter": 0.1284864703327155,
            "leak_type": "incipient",
            "leak_start_time": 616,
            "leak_end_time": 8447,
            "leak_peak_time": 4569
        }
    ],
    "693": [
        {
            "node_id": "12",
            "leak_diameter": 0.150699000288,
            "leak_type": "abrupt",
            "leak_start_time": 11978,
            "leak_end_time": 12355,
            "leak_peak_time": 11978
        }
    ],
    "694": [
        {
            "node_id": "32",
            "leak_diameter": 0.095263124616,
            "leak_type": "incipient",
            "leak_start_time": 13770,
            "leak_end_time": 15274,
            "leak_peak_time": 14334
        }
    ],
    "695": [
        {
            "node_id": "31",
            "leak_diameter": 0.160115954668,
            "leak_type": "incipient",
            "leak_start_time": 17162,
            "leak_end_time": 17332,
            "leak_peak_time": 17249
        }
    ],
    "696": [
        {
            "node_id": "23",
            "leak_diameter": 0.16089620100310825,
            "leak_type": "incipient",
            "leak_start_time": 2810,
            "leak_end_time": 16789,
            "leak_peak_time": 10158
        }
    ],
    "697": [
        {
            "node_id": "21",
            "leak_diameter": 0.12014380151921793,
            "leak_type": "incipient",
            "leak_start_time": 2796,
            "leak_end_time": 7886,
            "leak_peak_time": 3199
        }
    ],
    "698": [
        {
            "node_id": "22",
            "leak_diameter": 0.171326385213,
            "leak_type": "abrupt",
            "leak_start_time": 9598,
            "leak_end_time": 16982,
            "leak_peak_time": 9598
        }
    ],
    "699": [
        {
            "node_id": "10",
            "leak_diameter": 0.1722497737734309,
            "leak_type": "incipient",
            "leak_start_time": 312,
            "leak_end_time": 9788,
            "leak_peak_time": 3179
        }
    ],
    "700": [
        {
            "node_id": "2",
            "leak_diameter": 0.0707408971147,
            "leak_type": "abrupt",
            "leak_start_time": 10538,
            "leak_end_time": 16907,
            "leak_peak_time": 10538
        }
    ],
    "701": [
        {
            "node_id": "21",
            "leak_diameter": 0.162263921856148,
            "leak_type": "incipient",
            "leak_start_time": 11295,
            "leak_end_time": 13305,
            "leak_peak_time": 12105
        }
    ],
    "702": [
        {
            "node_id": "13",
            "leak_diameter": 0.127120481236,
            "leak_type": "abrupt",
            "leak_start_time": 14634,
            "leak_end_time": 15583,
            "leak_peak_time": 14634
        }
    ],
    "705": [
        {
            "node_id": "22",
            "leak_diameter": 0.17425425464513836,
            "leak_type": "incipient",
            "leak_start_time": 16818,
            "leak_end_time": 17169,
            "leak_peak_time": 17034
        }
    ],
    "706": [
        {
            "node_id": "22",
            "leak_diameter": 0.1264842876371547,
            "leak_type": "incipient",
            "leak_start_time": 2844,
            "leak_end_time": 11144,
            "leak_peak_time": 2917
        }
    ],
    "707": [
        {
            "node_id": "2",
            "leak_diameter": 0.113509951613,
            "leak_type": "abrupt",
            "leak_start_time": 12872,
            "leak_end_time": 15707,
            "leak_peak_time": 12872
        }
    ],
    "708": [
        {
            "node_id": "31",
            "leak_diameter": 0.100503778511,
            "leak_type": "abrupt",
            "leak_start_time": 4608,
            "leak_end_time": 12017,
            "leak_peak_time": 4608
        }
    ],
    "710": [
        {
            "node_id": "22",
            "leak_diameter": 0.0276454514346,
            "leak_type": "abrupt",
            "leak_start_time": 7988,
            "leak_end_time": 16280,
            "leak_peak_time": 7988
        },
        {
            "node_id": "2",
            "leak_diameter": 0.147257666075,
            "leak_type": "abrupt",
            "leak_start_time": 16251,
            "leak_end_time": 16298,
            "leak_peak_time": 16251
        }
    ],
    "712": [
        {
            "node_id": "10",
            "leak_diameter": 0.11250526704,
            "leak_type": "abrupt",
            "leak_start_time": 8261,
            "leak_end_time": 14523,
            "leak_peak_time": 8261
        },
        {
            "node_id": "12",
            "leak_diameter": 0.0674328503207,
            "leak_type": "abrupt",
            "leak_start_time": 8614,
            "leak_end_time": 8929,
            "leak_peak_time": 8614
        }
    ],
    "713": [
        {
            "node_id": "31",
            "leak_diameter": 0.139789704277,
            "leak_type": "abrupt",
            "leak_start_time": 15381,
            "leak_end_time": 15449,
            "leak_peak_time": 15381
        }
    ],
    "714": [
        {
            "node_id": "2",
            "leak_diameter": 0.16822937346436134,
            "leak_type": "incipient",
            "leak_start_time": 5797,
            "leak_end_time": 14447,
            "leak_peak_time": 8463
        }
    ],
    "715": [
        {
            "node_id": "21",
            "leak_diameter": 0.12855191758699336,
            "leak_type": "incipient",
            "leak_start_time": 14519,
            "leak_end_time": 16020,
            "leak_peak_time": 14618
        }
    ],
    "717": [
        {
            "node_id": "31",
            "leak_diameter": 0.18199645646611357,
            "leak_type": "incipient",
            "leak_start_time": 17402,
            "leak_end_time": 17430,
            "leak_peak_time": 17427
        }
    ],
    "718": [
        {
            "node_id": "13",
            "leak_diameter": 0.15640477851401507,
            "leak_type": "incipient",
            "leak_start_time": 7804,
            "leak_end_time": 15227,
            "leak_peak_time": 13876
        }
    ],
    "719": [
        {
            "node_id": "21",
            "leak_diameter": 0.0586201723727,
            "leak_type": "abrupt",
            "leak_start_time": 14268,
            "leak_end_time": 16823,
            "leak_peak_time": 14268
        }
    ],
    "720": [
        {
            "node_id": "32",
            "leak_diameter": 0.18232552724,
            "leak_type": "abrupt",
            "leak_start_time": 7084,
            "leak_end_time": 14175,
            "leak_peak_time": 7084
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0239328958047,
            "leak_type": "abrupt",
            "leak_start_time": 2509,
            "leak_end_time": 5068,
            "leak_peak_time": 2509
        }
    ],
    "721": [
        {
            "node_id": "31",
            "leak_diameter": 0.133995473171,
            "leak_type": "abrupt",
            "leak_start_time": 12845,
            "leak_end_time": 15673,
            "leak_peak_time": 12845
        }
    ],
    "722": [
        {
            "node_id": "13",
            "leak_diameter": 0.11825359864897932,
            "leak_type": "incipient",
            "leak_start_time": 14668,
            "leak_end_time": 16350,
            "leak_peak_time": 15028
        },
        {
            "node_id": "23",
            "leak_diameter": 0.03428129104684639,
            "leak_type": "incipient",
            "leak_start_time": 16034,
            "leak_end_time": 16843,
            "leak_peak_time": 16163
        }
    ],
    "723": [
        {
            "node_id": "12",
            "leak_diameter": 0.0312299573941,
            "leak_type": "abrupt",
            "leak_start_time": 12337,
            "leak_end_time": 16917,
            "leak_peak_time": 12337
        },
        {
            "node_id": "13",
            "leak_diameter": 0.154726564224,
            "leak_type": "abrupt",
            "leak_start_time": 9555,
            "leak_end_time": 17518,
            "leak_peak_time": 9555
        }
    ],
    "725": [
        {
            "node_id": "2",
            "leak_diameter": 0.0691354306233,
            "leak_type": "abrupt",
            "leak_start_time": 4937,
            "leak_end_time": 14829,
            "leak_peak_time": 4937
        },
        {
            "node_id": "32",
            "leak_diameter": 0.02901416363345177,
            "leak_type": "incipient",
            "leak_start_time": 7209,
            "leak_end_time": 15661,
            "leak_peak_time": 11089
        }
    ],
    "727": [
        {
            "node_id": "23",
            "leak_diameter": 0.130732956351,
            "leak_type": "abrupt",
            "leak_start_time": 5791,
            "leak_end_time": 10831,
            "leak_peak_time": 5791
        }
    ],
    "728": [
        {
            "node_id": "12",
            "leak_diameter": 0.0676152787512,
            "leak_type": "abrupt",
            "leak_start_time": 1759,
            "leak_end_time": 14136,
            "leak_peak_time": 1759
        }
    ],
    "729": [
        {
            "node_id": "32",
            "leak_diameter": 0.02930232759843302,
            "leak_type": "incipient",
            "leak_start_time": 9665,
            "leak_end_time": 10597,
            "leak_peak_time": 10213
        }
    ],
    "730": [
        {
            "node_id": "21",
            "leak_diameter": 0.111955323625,
            "leak_type": "abrupt",
            "leak_start_time": 12857,
            "leak_end_time": 16005,
            "leak_peak_time": 12857
        }
    ],
    "731": [
        {
            "node_id": "13",
            "leak_diameter": 0.19576744355749512,
            "leak_type": "incipient",
            "leak_start_time": 16527,
            "leak_end_time": 16795,
            "leak_peak_time": 16666
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0830860333781,
            "leak_type": "abrupt",
            "leak_start_time": 1804,
            "leak_end_time": 12962,
            "leak_peak_time": 1804
        }
    ],
    "732": [
        {
            "node_id": "22",
            "leak_diameter": 0.195549056938,
            "leak_type": "abrupt",
            "leak_start_time": 1962,
            "leak_end_time": 11740,
            "leak_peak_time": 1962
        }
    ],
    "733": [
        {
            "node_id": "22",
            "leak_diameter": 0.06633815589942225,
            "leak_type": "incipient",
            "leak_start_time": 17095,
            "leak_end_time": 17512,
            "leak_peak_time": 17481
        }
    ],
    "735": [
        {
            "node_id": "22",
            "leak_diameter": 0.19701239861281242,
            "leak_type": "incipient",
            "leak_start_time": 15647,
            "leak_end_time": 16109,
            "leak_peak_time": 15896
        }
    ],
    "736": [
        {
            "node_id": "22",
            "leak_diameter": 0.173929738584,
            "leak_type": "abrupt",
            "leak_start_time": 311,
            "leak_end_time": 8624,
            "leak_peak_time": 311
        },
        {
            "node_id": "13",
            "leak_diameter": 0.131755930393,
            "leak_type": "abrupt",
            "leak_start_time": 6594,
            "leak_end_time": 10897,
            "leak_peak_time": 6594
        }
    ],
    "737": [
        {
            "node_id": "13",
            "leak_diameter": 0.0552277057752,
            "leak_type": "abrupt",
            "leak_start_time": 409,
            "leak_end_time": 7558,
            "leak_peak_time": 409
        }
    ],
    "738": [
        {
            "node_id": "10",
            "leak_diameter": 0.0561905304213,
            "leak_type": "abrupt",
            "leak_start_time": 14972,
            "leak_end_time": 15061,
            "leak_peak_time": 14972
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0358997209714,
            "leak_type": "abrupt",
            "leak_start_time": 2030,
            "leak_end_time": 14860,
            "leak_peak_time": 2030
        }
    ],
    "739": [
        {
            "node_id": "21",
            "leak_diameter": 0.17608749159814077,
            "leak_type": "incipient",
            "leak_start_time": 13610,
            "leak_end_time": 16570,
            "leak_peak_time": 14316
        }
    ],
    "741": [
        {
            "node_id": "21",
            "leak_diameter": 0.09339457123086922,
            "leak_type": "incipient",
            "leak_start_time": 10173,
            "leak_end_time": 10334,
            "leak_peak_time": 10317
        }
    ],
    "742": [
        {
            "node_id": "2",
            "leak_diameter": 0.0733019467552,
            "leak_type": "abrupt",
            "leak_start_time": 7262,
            "leak_end_time": 16298,
            "leak_peak_time": 7262
        }
    ],
    "743": [
        {
            "node_id": "32",
            "leak_diameter": 0.169300486708,
            "leak_type": "incipient",
            "leak_start_time": 9549,
            "leak_end_time": 12441,
            "leak_peak_time": 12270
        }
    ],
    "744": [
        {
            "node_id": "21",
            "leak_diameter": 0.112129416864,
            "leak_type": "abrupt",
            "leak_start_time": 17514,
            "leak_end_time": 17518,
            "leak_peak_time": 17514
        },
        {
            "node_id": "13",
            "leak_diameter": 0.098185900985,
            "leak_type": "abrupt",
            "leak_start_time": 17518,
            "leak_end_time": 17519,
            "leak_peak_time": 17518
        }
    ],
    "746": [
        {
            "node_id": "32",
            "leak_diameter": 0.034749013751477244,
            "leak_type": "incipient",
            "leak_start_time": 15951,
            "leak_end_time": 16074,
            "leak_peak_time": 16014
        },
        {
            "node_id": "31",
            "leak_diameter": 0.027930829054691502,
            "leak_type": "incipient",
            "leak_start_time": 11445,
            "leak_end_time": 15749,
            "leak_peak_time": 13121
        }
    ],
    "748": [
        {
            "node_id": "13",
            "leak_diameter": 0.0680982388445,
            "leak_type": "abrupt",
            "leak_start_time": 5824,
            "leak_end_time": 6669,
            "leak_peak_time": 5824
        },
        {
            "node_id": "32",
            "leak_diameter": 0.140594192118,
            "leak_type": "abrupt",
            "leak_start_time": 13654,
            "leak_end_time": 14893,
            "leak_peak_time": 13654
        }
    ],
    "750": [
        {
            "node_id": "21",
            "leak_diameter": 0.186673170273,
            "leak_type": "abrupt",
            "leak_start_time": 14189,
            "leak_end_time": 15866,
            "leak_peak_time": 14189
        },
        {
            "node_id": "2",
            "leak_diameter": 0.13381677677879367,
            "leak_type": "incipient",
            "leak_start_time": 2535,
            "leak_end_time": 13664,
            "leak_peak_time": 7369
        }
    ],
    "751": [
        {
            "node_id": "21",
            "leak_diameter": 0.0422419814221,
            "leak_type": "abrupt",
            "leak_start_time": 14474,
            "leak_end_time": 16180,
            "leak_peak_time": 14474
        },
        {
            "node_id": "13",
            "leak_diameter": 0.107921898952,
            "leak_type": "abrupt",
            "leak_start_time": 12017,
            "leak_end_time": 15009,
            "leak_peak_time": 12017
        }
    ],
    "753": [
        {
            "node_id": "12",
            "leak_diameter": 0.0793266530463196,
            "leak_type": "incipient",
            "leak_start_time": 1091,
            "leak_end_time": 14614,
            "leak_peak_time": 1701
        },
        {
            "node_id": "13",
            "leak_diameter": 0.16516685731590314,
            "leak_type": "incipient",
            "leak_start_time": 14116,
            "leak_end_time": 15006,
            "leak_peak_time": 14262
        }
    ],
    "754": [
        {
            "node_id": "13",
            "leak_diameter": 0.190328968597,
            "leak_type": "abrupt",
            "leak_start_time": 10051,
            "leak_end_time": 12417,
            "leak_peak_time": 10051
        }
    ],
    "755": [
        {
            "node_id": "2",
            "leak_diameter": 0.067547020139,
            "leak_type": "abrupt",
            "leak_start_time": 861,
            "leak_end_time": 2708,
            "leak_peak_time": 861
        }
    ],
    "756": [
        {
            "node_id": "22",
            "leak_diameter": 0.189873905785,
            "leak_type": "abrupt",
            "leak_start_time": 5531,
            "leak_end_time": 12535,
            "leak_peak_time": 5531
        }
    ],
    "758": [
        {
            "node_id": "13",
            "leak_diameter": 0.074146957725,
            "leak_type": "incipient",
            "leak_start_time": 4223,
            "leak_end_time": 13707,
            "leak_peak_time": 7905
        }
    ],
    "759": [
        {
            "node_id": "22",
            "leak_diameter": 0.176768449412,
            "leak_type": "incipient",
            "leak_start_time": 10260,
            "leak_end_time": 13325,
            "leak_peak_time": 11396
        }
    ],
    "760": [
        {
            "node_id": "32",
            "leak_diameter": 0.0618067769266,
            "leak_type": "abrupt",
            "leak_start_time": 3120,
            "leak_end_time": 13167,
            "leak_peak_time": 3120
        }
    ],
    "761": [
        {
            "node_id": "12",
            "leak_diameter": 0.0211411908229,
            "leak_type": "abrupt",
            "leak_start_time": 1248,
            "leak_end_time": 9963,
            "leak_peak_time": 1248
        }
    ],
    "762": [
        {
            "node_id": "12",
            "leak_diameter": 0.179441434812,
            "leak_type": "abrupt",
            "leak_start_time": 6837,
            "leak_end_time": 9314,
            "leak_peak_time": 6837
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0788506565356,
            "leak_type": "incipient",
            "leak_start_time": 5978,
            "leak_end_time": 12679,
            "leak_peak_time": 9107
        }
    ],
    "764": [
        {
            "node_id": "13",
            "leak_diameter": 0.0904416771983,
            "leak_type": "incipient",
            "leak_start_time": 3379,
            "leak_end_time": 14057,
            "leak_peak_time": 3727
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0887584900604,
            "leak_type": "incipient",
            "leak_start_time": 11216,
            "leak_end_time": 11931,
            "leak_peak_time": 11706
        }
    ],
    "765": [
        {
            "node_id": "22",
            "leak_diameter": 0.104296293153,
            "leak_type": "incipient",
            "leak_start_time": 13096,
            "leak_end_time": 16054,
            "leak_peak_time": 13734
        },
        {
            "node_id": "31",
            "leak_diameter": 0.164375900662,
            "leak_type": "abrupt",
            "leak_start_time": 13826,
            "leak_end_time": 14086,
            "leak_peak_time": 13826
        }
    ],
    "766": [
        {
            "node_id": "23",
            "leak_diameter": 0.113423656332,
            "leak_type": "incipient",
            "leak_start_time": 7405,
            "leak_end_time": 10182,
            "leak_peak_time": 8806
        }
    ],
    "767": [
        {
            "node_id": "23",
            "leak_diameter": 0.0221201779292,
            "leak_type": "incipient",
            "leak_start_time": 6378,
            "leak_end_time": 17085,
            "leak_peak_time": 11548
        }
    ],
    "768": [
        {
            "node_id": "12",
            "leak_diameter": 0.103051930583,
            "leak_type": "abrupt",
            "leak_start_time": 14257,
            "leak_end_time": 17334,
            "leak_peak_time": 14257
        }
    ],
    "769": [
        {
            "node_id": "10",
            "leak_diameter": 0.0948503728528,
            "leak_type": "incipient",
            "leak_start_time": 13073,
            "leak_end_time": 17032,
            "leak_peak_time": 15679
        }
    ],
    "770": [
        {
            "node_id": "12",
            "leak_diameter": 0.119568832652,
            "leak_type": "incipient",
            "leak_start_time": 15522,
            "leak_end_time": 16454,
            "leak_peak_time": 16005
        },
        {
            "node_id": "21",
            "leak_diameter": 0.120945978795,
            "leak_type": "abrupt",
            "leak_start_time": 9793,
            "leak_end_time": 12169,
            "leak_peak_time": 9793
        }
    ],
    "774": [
        {
            "node_id": "22",
            "leak_diameter": 0.0983400413748,
            "leak_type": "incipient",
            "leak_start_time": 8275,
            "leak_end_time": 9065,
            "leak_peak_time": 8527
        }
    ],
    "775": [
        {
            "node_id": "21",
            "leak_diameter": 0.154175852319,
            "leak_type": "incipient",
            "leak_start_time": 3431,
            "leak_end_time": 6350,
            "leak_peak_time": 4694
        }
    ],
    "776": [
        {
            "node_id": "21",
            "leak_diameter": 0.156046553746,
            "leak_type": "incipient",
            "leak_start_time": 4219,
            "leak_end_time": 14369,
            "leak_peak_time": 12352
        }
    ],
    "777": [
        {
            "node_id": "31",
            "leak_diameter": 0.192782544304,
            "leak_type": "incipient",
            "leak_start_time": 15522,
            "leak_end_time": 16863,
            "leak_peak_time": 16720
        }
    ],
    "778": [
        {
            "node_id": "31",
            "leak_diameter": 0.0860185887008,
            "leak_type": "abrupt",
            "leak_start_time": 7846,
            "leak_end_time": 7899,
            "leak_peak_time": 7846
        }
    ],
    "780": [
        {
            "node_id": "32",
            "leak_diameter": 0.0254649907206,
            "leak_type": "incipient",
            "leak_start_time": 14456,
            "leak_end_time": 14897,
            "leak_peak_time": 14864
        }
    ],
    "781": [
        {
            "node_id": "13",
            "leak_diameter": 0.0378034701984,
            "leak_type": "incipient",
            "leak_start_time": 16551,
            "leak_end_time": 17148,
            "leak_peak_time": 16556
        }
    ],
    "782": [
        {
            "node_id": "23",
            "leak_diameter": 0.0464720608969,
            "leak_type": "abrupt",
            "leak_start_time": 335,
            "leak_end_time": 10916,
            "leak_peak_time": 335
        }
    ],
    "783": [
        {
            "node_id": "22",
            "leak_diameter": 0.0598260722751,
            "leak_type": "incipient",
            "leak_start_time": 8874,
            "leak_end_time": 15193,
            "leak_peak_time": 13080
        }
    ],
    "784": [
        {
            "node_id": "21",
            "leak_diameter": 0.090687660573,
            "leak_type": "incipient",
            "leak_start_time": 17220,
            "leak_end_time": 17472,
            "leak_peak_time": 17255
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0632009913542,
            "leak_type": "abrupt",
            "leak_start_time": 3796,
            "leak_end_time": 15469,
            "leak_peak_time": 3796
        }
    ],
    "785": [
        {
            "node_id": "12",
            "leak_diameter": 0.102250422009,
            "leak_type": "abrupt",
            "leak_start_time": 8157,
            "leak_end_time": 9715,
            "leak_peak_time": 8157
        }
    ],
    "786": [
        {
            "node_id": "13",
            "leak_diameter": 0.132871798686,
            "leak_type": "abrupt",
            "leak_start_time": 15443,
            "leak_end_time": 16569,
            "leak_peak_time": 15443
        },
        {
            "node_id": "2",
            "leak_diameter": 0.0936711459426,
            "leak_type": "abrupt",
            "leak_start_time": 5609,
            "leak_end_time": 13907,
            "leak_peak_time": 5609
        },
        {
            "node_id": "32",
            "leak_diameter": 0.113076582964,
            "leak_type": "incipient",
            "leak_start_time": 12721,
            "leak_end_time": 16348,
            "leak_peak_time": 15412
        }
    ],
    "787": [
        {
            "node_id": "12",
            "leak_diameter": 0.149123305673,
            "leak_type": "abrupt",
            "leak_start_time": 16743,
            "leak_end_time": 17340,
            "leak_peak_time": 16743
        },
        {
            "node_id": "23",
            "leak_diameter": 0.106140354085,
            "leak_type": "abrupt",
            "leak_start_time": 7777,
            "leak_end_time": 10140,
            "leak_peak_time": 7777
        }
    ],
    "788": [
        {
            "node_id": "13",
            "leak_diameter": 0.107656251768,
            "leak_type": "abrupt",
            "leak_start_time": 15043,
            "leak_end_time": 16781,
            "leak_peak_time": 15043
        }
    ],
    "789": [
        {
            "node_id": "12",
            "leak_diameter": 0.0549215997257,
            "leak_type": "abrupt",
            "leak_start_time": 7130,
            "leak_end_time": 7176,
            "leak_peak_time": 7130
        },
        {
            "node_id": "21",
            "leak_diameter": 0.0856885932099,
            "leak_type": "abrupt",
            "leak_start_time": 10411,
            "leak_end_time": 14217,
            "leak_peak_time": 10411
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0333465382128,
            "leak_type": "abrupt",
            "leak_start_time": 7304,
            "leak_end_time": 13628,
            "leak_peak_time": 7304
        }
    ],
    "790": [
        {
            "node_id": "10",
            "leak_diameter": 0.114966466193,
            "leak_type": "incipient",
            "leak_start_time": 3865,
            "leak_end_time": 6544,
            "leak_peak_time": 4032
        },
        {
            "node_id": "31",
            "leak_diameter": 0.119843807804,
            "leak_type": "incipient",
            "leak_start_time": 11707,
            "leak_end_time": 12398,
            "leak_peak_time": 11975
        }
    ],
    "791": [
        {
            "node_id": "22",
            "leak_diameter": 0.0656157150311,
            "leak_type": "abrupt",
            "leak_start_time": 7503,
            "leak_end_time": 11512,
            "leak_peak_time": 7503
        },
        {
            "node_id": "13",
            "leak_diameter": 0.115200409361,
            "leak_type": "incipient",
            "leak_start_time": 8878,
            "leak_end_time": 10057,
            "leak_peak_time": 9337
        },
        {
            "node_id": "23",
            "leak_diameter": 0.155680147024,
            "leak_type": "incipient",
            "leak_start_time": 7608,
            "leak_end_time": 13664,
            "leak_peak_time": 9503
        },
        {
            "node_id": "32",
            "leak_diameter": 0.078658849669,
            "leak_type": "abrupt",
            "leak_start_time": 12393,
            "leak_end_time": 13986,
            "leak_peak_time": 12393
        }
    ],
    "792": [
        {
            "node_id": "2",
            "leak_diameter": 0.190003713903,
            "leak_type": "incipient",
            "leak_start_time": 4295,
            "leak_end_time": 9296,
            "leak_peak_time": 6754
        }
    ],
    "793": [
        {
            "node_id": "31",
            "leak_diameter": 0.0670355561239,
            "leak_type": "abrupt",
            "leak_start_time": 9762,
            "leak_end_time": 16089,
            "leak_peak_time": 9762
        }
    ],
    "794": [
        {
            "node_id": "13",
            "leak_diameter": 0.193968243502,
            "leak_type": "incipient",
            "leak_start_time": 6712,
            "leak_end_time": 17058,
            "leak_peak_time": 8034
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0314605561918,
            "leak_type": "incipient",
            "leak_start_time": 2672,
            "leak_end_time": 12491,
            "leak_peak_time": 6685
        }
    ],
    "795": [
        {
            "node_id": "23",
            "leak_diameter": 0.0810146898055,
            "leak_type": "abrupt",
            "leak_start_time": 16550,
            "leak_end_time": 17023,
            "leak_peak_time": 16550
        }
    ],
    "796": [
        {
            "node_id": "22",
            "leak_diameter": 0.152137715378,
            "leak_type": "incipient",
            "leak_start_time": 11942,
            "leak_end_time": 17190,
            "leak_peak_time": 13957
        }
    ],
    "797": [
        {
            "node_id": "22",
            "leak_diameter": 0.0261901599717,
            "leak_type": "incipient",
            "leak_start_time": 7579,
            "leak_end_time": 12787,
            "leak_peak_time": 12453
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0286205926727,
            "leak_type": "abrupt",
            "leak_start_time": 1945,
            "leak_end_time": 12636,
            "leak_peak_time": 1945
        }
    ],
    "798": [
        {
            "node_id": "21",
            "leak_diameter": 0.0735606323018,
            "leak_type": "abrupt",
            "leak_start_time": 16382,
            "leak_end_time": 16669,
            "leak_peak_time": 16382
        }
    ],
    "799": [
        {
            "node_id": "22",
            "leak_diameter": 0.0575815011748,
            "leak_type": "abrupt",
            "leak_start_time": 1595,
            "leak_end_time": 8655,
            "leak_peak_time": 1595
        },
        {
            "node_id": "21",
            "leak_diameter": 0.112641124041,
            "leak_type": "abrupt",
            "leak_start_time": 11918,
            "leak_end_time": 14883,
            "leak_peak_time": 11918
        }
    ],
    "800": [
        {
            "node_id": "13",
            "leak_diameter": 0.129507798065,
            "leak_type": "incipient",
            "leak_start_time": 2344,
            "leak_end_time": 16408,
            "leak_peak_time": 4357
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0524497521674,
            "leak_type": "abrupt",
            "leak_start_time": 6919,
            "leak_end_time": 13232,
            "leak_peak_time": 6919
        },
        {
            "node_id": "32",
            "leak_diameter": 0.030397580183,
            "leak_type": "abrupt",
            "leak_start_time": 3478,
            "leak_end_time": 9704,
            "leak_peak_time": 3478
        }
    ],
    "802": [
        {
            "node_id": "21",
            "leak_diameter": 0.0848848268157,
            "leak_type": "incipient",
            "leak_start_time": 16765,
            "leak_end_time": 17225,
            "leak_peak_time": 16999
        },
        {
            "node_id": "23",
            "leak_diameter": 0.114025998231,
            "leak_type": "abrupt",
            "leak_start_time": 4855,
            "leak_end_time": 5778,
            "leak_peak_time": 4855
        }
    ],
    "803": [
        {
            "node_id": "31",
            "leak_diameter": 0.0294873601333,
            "leak_type": "abrupt",
            "leak_start_time": 2301,
            "leak_end_time": 12385,
            "leak_peak_time": 2301
        }
    ],
    "804": [
        {
            "node_id": "22",
            "leak_diameter": 0.0725306848862,
            "leak_type": "incipient",
            "leak_start_time": 12493,
            "leak_end_time": 13735,
            "leak_peak_time": 13717
        },
        {
            "node_id": "31",
            "leak_diameter": 0.187338324012,
            "leak_type": "incipient",
            "leak_start_time": 1168,
            "leak_end_time": 16368,
            "leak_peak_time": 11290
        }
    ],
    "805": [
        {
            "node_id": "13",
            "leak_diameter": 0.124513234576,
            "leak_type": "incipient",
            "leak_start_time": 4098,
            "leak_end_time": 15309,
            "leak_peak_time": 7955
        },
        {
            "node_id": "31",
            "leak_diameter": 0.137522234959,
            "leak_type": "incipient",
            "leak_start_time": 7526,
            "leak_end_time": 11611,
            "leak_peak_time": 11563
        }
    ],
    "806": [
        {
            "node_id": "12",
            "leak_diameter": 0.164399742084,
            "leak_type": "abrupt",
            "leak_start_time": 1607,
            "leak_end_time": 8757,
            "leak_peak_time": 1607
        },
        {
            "node_id": "2",
            "leak_diameter": 0.136999782086,
            "leak_type": "abrupt",
            "leak_start_time": 1622,
            "leak_end_time": 8193,
            "leak_peak_time": 1622
        }
    ],
    "807": [
        {
            "node_id": "10",
            "leak_diameter": 0.153110101354,
            "leak_type": "incipient",
            "leak_start_time": 11819,
            "leak_end_time": 13703,
            "leak_peak_time": 12717
        }
    ],
    "808": [
        {
            "node_id": "22",
            "leak_diameter": 0.0692478002537,
            "leak_type": "incipient",
            "leak_start_time": 11106,
            "leak_end_time": 13768,
            "leak_peak_time": 12640
        },
        {
            "node_id": "21",
            "leak_diameter": 0.0893081316335,
            "leak_type": "incipient",
            "leak_start_time": 5597,
            "leak_end_time": 7951,
            "leak_peak_time": 5635
        }
    ],
    "809": [
        {
            "node_id": "12",
            "leak_diameter": 0.0517651964608,
            "leak_type": "abrupt",
            "leak_start_time": 988,
            "leak_end_time": 14504,
            "leak_peak_time": 988
        }
    ],
    "810": [
        {
            "node_id": "22",
            "leak_diameter": 0.118215757572,
            "leak_type": "incipient",
            "leak_start_time": 10886,
            "leak_end_time": 12515,
            "leak_peak_time": 12199
        },
        {
            "node_id": "21",
            "leak_diameter": 0.0731776917734,
            "leak_type": "abrupt",
            "leak_start_time": 1249,
            "leak_end_time": 4002,
            "leak_peak_time": 1249
        },
        {
            "node_id": "23",
            "leak_diameter": 0.155649638368,
            "leak_type": "abrupt",
            "leak_start_time": 2705,
            "leak_end_time": 6604,
            "leak_peak_time": 2705
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0774423729909,
            "leak_type": "incipient",
            "leak_start_time": 3620,
            "leak_end_time": 7901,
            "leak_peak_time": 6364
        }
    ],
    "811": [
        {
            "node_id": "23",
            "leak_diameter": 0.196635818632,
            "leak_type": "incipient",
            "leak_start_time": 9684,
            "leak_end_time": 10142,
            "leak_peak_time": 9929
        }
    ],
    "812": [
        {
            "node_id": "32",
            "leak_diameter": 0.0602338968462,
            "leak_type": "incipient",
            "leak_start_time": 15968,
            "leak_end_time": 17100,
            "leak_peak_time": 16803
        }
    ],
    "813": [
        {
            "node_id": "12",
            "leak_diameter": 0.142945060249,
            "leak_type": "incipient",
            "leak_start_time": 14755,
            "leak_end_time": 15541,
            "leak_peak_time": 15199
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0849185618995,
            "leak_type": "abrupt",
            "leak_start_time": 13441,
            "leak_end_time": 16862,
            "leak_peak_time": 13441
        }
    ],
    "815": [
        {
            "node_id": "21",
            "leak_diameter": 0.116626963731,
            "leak_type": "incipient",
            "leak_start_time": 15336,
            "leak_end_time": 17118,
            "leak_peak_time": 15405
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0695795431908,
            "leak_type": "abrupt",
            "leak_start_time": 15740,
            "leak_end_time": 16412,
            "leak_peak_time": 15740
        }
    ],
    "816": [
        {
            "node_id": "32",
            "leak_diameter": 0.0335846175017,
            "leak_type": "abrupt",
            "leak_start_time": 14021,
            "leak_end_time": 16646,
            "leak_peak_time": 14021
        }
    ],
    "818": [
        {
            "node_id": "21",
            "leak_diameter": 0.136939732428,
            "leak_type": "abrupt",
            "leak_start_time": 1581,
            "leak_end_time": 7994,
            "leak_peak_time": 1581
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0765119796053,
            "leak_type": "abrupt",
            "leak_start_time": 4162,
            "leak_end_time": 17195,
            "leak_peak_time": 4162
        }
    ],
    "821": [
        {
            "node_id": "32",
            "leak_diameter": 0.0588298917708,
            "leak_type": "abrupt",
            "leak_start_time": 2565,
            "leak_end_time": 7396,
            "leak_peak_time": 2565
        }
    ],
    "822": [
        {
            "node_id": "10",
            "leak_diameter": 0.109076583785,
            "leak_type": "incipient",
            "leak_start_time": 6242,
            "leak_end_time": 7338,
            "leak_peak_time": 7102
        }
    ],
    "823": [
        {
            "node_id": "23",
            "leak_diameter": 0.196803380147,
            "leak_type": "incipient",
            "leak_start_time": 4536,
            "leak_end_time": 14401,
            "leak_peak_time": 7181
        }
    ],
    "825": [
        {
            "node_id": "13",
            "leak_diameter": 0.0220596931154,
            "leak_type": "incipient",
            "leak_start_time": 6847,
            "leak_end_time": 8053,
            "leak_peak_time": 7801
        }
    ],
    "826": [
        {
            "node_id": "23",
            "leak_diameter": 0.15593582196,
            "leak_type": "abrupt",
            "leak_start_time": 8123,
            "leak_end_time": 11555,
            "leak_peak_time": 8123
        },
        {
            "node_id": "32",
            "leak_diameter": 0.102804054926,
            "leak_type": "abrupt",
            "leak_start_time": 11668,
            "leak_end_time": 16950,
            "leak_peak_time": 11668
        }
    ],
    "827": [
        {
            "node_id": "21",
            "leak_diameter": 0.198195185516,
            "leak_type": "abrupt",
            "leak_start_time": 4925,
            "leak_end_time": 6855,
            "leak_peak_time": 4925
        }
    ],
    "828": [
        {
            "node_id": "23",
            "leak_diameter": 0.0780595041927,
            "leak_type": "abrupt",
            "leak_start_time": 4319,
            "leak_end_time": 15362,
            "leak_peak_time": 4319
        }
    ],
    "829": [
        {
            "node_id": "13",
            "leak_diameter": 0.154095269886,
            "leak_type": "abrupt",
            "leak_start_time": 10304,
            "leak_end_time": 13042,
            "leak_peak_time": 10304
        }
    ],
    "830": [
        {
            "node_id": "21",
            "leak_diameter": 0.037023732296,
            "leak_type": "incipient",
            "leak_start_time": 9568,
            "leak_end_time": 11109,
            "leak_peak_time": 10160
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0417245995836,
            "leak_type": "abrupt",
            "leak_start_time": 11523,
            "leak_end_time": 12561,
            "leak_peak_time": 11523
        }
    ],
    "831": [
        {
            "node_id": "22",
            "leak_diameter": 0.153922552371,
            "leak_type": "incipient",
            "leak_start_time": 8984,
            "leak_end_time": 11149,
            "leak_peak_time": 9347
        },
        {
            "node_id": "12",
            "leak_diameter": 0.178579819688,
            "leak_type": "incipient",
            "leak_start_time": 12986,
            "leak_end_time": 13656,
            "leak_peak_time": 13230
        }
    ],
    "832": [
        {
            "node_id": "12",
            "leak_diameter": 0.0921501724854,
            "leak_type": "abrupt",
            "leak_start_time": 15924,
            "leak_end_time": 17410,
            "leak_peak_time": 15924
        }
    ],
    "833": [
        {
            "node_id": "12",
            "leak_diameter": 0.0345433407234,
            "leak_type": "incipient",
            "leak_start_time": 15201,
            "leak_end_time": 15377,
            "leak_peak_time": 15296
        },
        {
            "node_id": "21",
            "leak_diameter": 0.184679612157,
            "leak_type": "incipient",
            "leak_start_time": 2931,
            "leak_end_time": 3082,
            "leak_peak_time": 3026
        }
    ],
    "834": [
        {
            "node_id": "13",
            "leak_diameter": 0.094751984938,
            "leak_type": "incipient",
            "leak_start_time": 6243,
            "leak_end_time": 13375,
            "leak_peak_time": 7814
        }
    ],
    "835": [
        {
            "node_id": "12",
            "leak_diameter": 0.0442398334857,
            "leak_type": "incipient",
            "leak_start_time": 3459,
            "leak_end_time": 15513,
            "leak_peak_time": 14287
        }
    ],
    "836": [
        {
            "node_id": "22",
            "leak_diameter": 0.134595423052,
            "leak_type": "incipient",
            "leak_start_time": 8333,
            "leak_end_time": 9969,
            "leak_peak_time": 9278
        }
    ],
    "837": [
        {
            "node_id": "12",
            "leak_diameter": 0.0276144256903,
            "leak_type": "abrupt",
            "leak_start_time": 636,
            "leak_end_time": 3689,
            "leak_peak_time": 636
        }
    ],
    "838": [
        {
            "node_id": "23",
            "leak_diameter": 0.0608397391057,
            "leak_type": "incipient",
            "leak_start_time": 10856,
            "leak_end_time": 14246,
            "leak_peak_time": 12912
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0702741877208,
            "leak_type": "incipient",
            "leak_start_time": 16488,
            "leak_end_time": 16806,
            "leak_peak_time": 16778
        }
    ],
    "840": [
        {
            "node_id": "12",
            "leak_diameter": 0.0492068341012,
            "leak_type": "incipient",
            "leak_start_time": 4060,
            "leak_end_time": 4599,
            "leak_peak_time": 4485
        }
    ],
    "841": [
        {
            "node_id": "10",
            "leak_diameter": 0.0249499580813,
            "leak_type": "abrupt",
            "leak_start_time": 2204,
            "leak_end_time": 4538,
            "leak_peak_time": 2204
        },
        {
            "node_id": "31",
            "leak_diameter": 0.181819473033,
            "leak_type": "abrupt",
            "leak_start_time": 8473,
            "leak_end_time": 9708,
            "leak_peak_time": 8473
        }
    ],
    "842": [
        {
            "node_id": "31",
            "leak_diameter": 0.0698564915178,
            "leak_type": "abrupt",
            "leak_start_time": 3215,
            "leak_end_time": 3305,
            "leak_peak_time": 3215
        }
    ],
    "843": [
        {
            "node_id": "10",
            "leak_diameter": 0.055235456195,
            "leak_type": "incipient",
            "leak_start_time": 182,
            "leak_end_time": 14306,
            "leak_peak_time": 12683
        }
    ],
    "844": [
        {
            "node_id": "21",
            "leak_diameter": 0.034447800728,
            "leak_type": "incipient",
            "leak_start_time": 8873,
            "leak_end_time": 9810,
            "leak_peak_time": 9691
        },
        {
            "node_id": "31",
            "leak_diameter": 0.174083129655,
            "leak_type": "incipient",
            "leak_start_time": 7351,
            "leak_end_time": 10643,
            "leak_peak_time": 10252
        }
    ],
    "845": [
        {
            "node_id": "12",
            "leak_diameter": 0.102889895901,
            "leak_type": "incipient",
            "leak_start_time": 15102,
            "leak_end_time": 15183,
            "leak_peak_time": 15132
        }
    ],
    "846": [
        {
            "node_id": "22",
            "leak_diameter": 0.0682379845995,
            "leak_type": "incipient",
            "leak_start_time": 10949,
            "leak_end_time": 15964,
            "leak_peak_time": 13205
        },
        {
            "node_id": "31",
            "leak_diameter": 0.181353895993,
            "leak_type": "abrupt",
            "leak_start_time": 4985,
            "leak_end_time": 8641,
            "leak_peak_time": 4985
        }
    ],
    "847": [
        {
            "node_id": "12",
            "leak_diameter": 0.138454052829,
            "leak_type": "incipient",
            "leak_start_time": 388,
            "leak_end_time": 5219,
            "leak_peak_time": 3871
        }
    ],
    "848": [
        {
            "node_id": "31",
            "leak_diameter": 0.165990436692,
            "leak_type": "abrupt",
            "leak_start_time": 13969,
            "leak_end_time": 14836,
            "leak_peak_time": 13969
        }
    ],
    "849": [
        {
            "node_id": "13",
            "leak_diameter": 0.11023231497,
            "leak_type": "incipient",
            "leak_start_time": 2055,
            "leak_end_time": 4027,
            "leak_peak_time": 2545
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0285458297734,
            "leak_type": "abrupt",
            "leak_start_time": 6049,
            "leak_end_time": 12624,
            "leak_peak_time": 6049
        }
    ],
    "850": [
        {
            "node_id": "2",
            "leak_diameter": 0.0742280333904,
            "leak_type": "incipient",
            "leak_start_time": 17336,
            "leak_end_time": 17458,
            "leak_peak_time": 17348
        }
    ],
    "851": [
        {
            "node_id": "21",
            "leak_diameter": 0.121896270166,
            "leak_type": "abrupt",
            "leak_start_time": 15296,
            "leak_end_time": 16083,
            "leak_peak_time": 15296
        }
    ],
    "853": [
        {
            "node_id": "22",
            "leak_diameter": 0.111608705794,
            "leak_type": "incipient",
            "leak_start_time": 6166,
            "leak_end_time": 17349,
            "leak_peak_time": 8959
        },
        {
            "node_id": "12",
            "leak_diameter": 0.120578546483,
            "leak_type": "abrupt",
            "leak_start_time": 7518,
            "leak_end_time": 10151,
            "leak_peak_time": 7518
        }
    ],
    "854": [
        {
            "node_id": "13",
            "leak_diameter": 0.194363739296,
            "leak_type": "incipient",
            "leak_start_time": 5310,
            "leak_end_time": 7496,
            "leak_peak_time": 6731
        }
    ],
    "856": [
        {
            "node_id": "23",
            "leak_diameter": 0.134113134896,
            "leak_type": "incipient",
            "leak_start_time": 10414,
            "leak_end_time": 14435,
            "leak_peak_time": 14022
        }
    ],
    "857": [
        {
            "node_id": "23",
            "leak_diameter": 0.198099069596,
            "leak_type": "incipient",
            "leak_start_time": 14133,
            "leak_end_time": 16762,
            "leak_peak_time": 14330
        }
    ],
    "860": [
        {
            "node_id": "31",
            "leak_diameter": 0.14982908953,
            "leak_type": "incipient",
            "leak_start_time": 2203,
            "leak_end_time": 14251,
            "leak_peak_time": 4272
        }
    ],
    "864": [
        {
            "node_id": "32",
            "leak_diameter": 0.0976271859191,
            "leak_type": "incipient",
            "leak_start_time": 11325,
            "leak_end_time": 13451,
            "leak_peak_time": 11775
        }
    ],
    "865": [
        {
            "node_id": "2",
            "leak_diameter": 0.154683505589,
            "leak_type": "abrupt",
            "leak_start_time": 9895,
            "leak_end_time": 16149,
            "leak_peak_time": 9895
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0696720566239,
            "leak_type": "abrupt",
            "leak_start_time": 5578,
            "leak_end_time": 6378,
            "leak_peak_time": 5578
        }
    ],
    "866": [
        {
            "node_id": "23",
            "leak_diameter": 0.0312881544675,
            "leak_type": "incipient",
            "leak_start_time": 1992,
            "leak_end_time": 3143,
            "leak_peak_time": 2938
        }
    ],
    "867": [
        {
            "node_id": "21",
            "leak_diameter": 0.0667564615463,
            "leak_type": "incipient",
            "leak_start_time": 1884,
            "leak_end_time": 11970,
            "leak_peak_time": 11812
        }
    ],
    "868": [
        {
            "node_id": "10",
            "leak_diameter": 0.125017897502,
            "leak_type": "incipient",
            "leak_start_time": 1719,
            "leak_end_time": 2359,
            "leak_peak_time": 2279
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0673013916689,
            "leak_type": "incipient",
            "leak_start_time": 7394,
            "leak_end_time": 16299,
            "leak_peak_time": 12877
        }
    ],
    "869": [
        {
            "node_id": "32",
            "leak_diameter": 0.150522775937,
            "leak_type": "abrupt",
            "leak_start_time": 5474,
            "leak_end_time": 7813,
            "leak_peak_time": 5474
        }
    ],
    "871": [
        {
            "node_id": "21",
            "leak_diameter": 0.153039923233,
            "leak_type": "incipient",
            "leak_start_time": 1853,
            "leak_end_time": 8492,
            "leak_peak_time": 2057
        }
    ],
    "872": [
        {
            "node_id": "31",
            "leak_diameter": 0.156884048494,
            "leak_type": "incipient",
            "leak_start_time": 15918,
            "leak_end_time": 17109,
            "leak_peak_time": 16731
        }
    ],
    "873": [
        {
            "node_id": "12",
            "leak_diameter": 0.0206649118799,
            "leak_type": "abrupt",
            "leak_start_time": 171,
            "leak_end_time": 15828,
            "leak_peak_time": 171
        }
    ],
    "874": [
        {
            "node_id": "10",
            "leak_diameter": 0.0643679848155,
            "leak_type": "abrupt",
            "leak_start_time": 9276,
            "leak_end_time": 9942,
            "leak_peak_time": 9276
        },
        {
            "node_id": "23",
            "leak_diameter": 0.14783015544,
            "leak_type": "incipient",
            "leak_start_time": 3827,
            "leak_end_time": 11255,
            "leak_peak_time": 7419
        }
    ],
    "875": [
        {
            "node_id": "2",
            "leak_diameter": 0.0991553515163,
            "leak_type": "abrupt",
            "leak_start_time": 2454,
            "leak_end_time": 7753,
            "leak_peak_time": 2454
        }
    ],
    "877": [
        {
            "node_id": "32",
            "leak_diameter": 0.061063254504,
            "leak_type": "incipient",
            "leak_start_time": 7995,
            "leak_end_time": 9506,
            "leak_peak_time": 8421
        }
    ],
    "878": [
        {
            "node_id": "12",
            "leak_diameter": 0.0207697252614,
            "leak_type": "incipient",
            "leak_start_time": 495,
            "leak_end_time": 6663,
            "leak_peak_time": 1982
        }
    ],
    "879": [
        {
            "node_id": "31",
            "leak_diameter": 0.020457784408,
            "leak_type": "abrupt",
            "leak_start_time": 15663,
            "leak_end_time": 15854,
            "leak_peak_time": 15663
        }
    ],
    "880": [
        {
            "node_id": "31",
            "leak_diameter": 0.0881090773692,
            "leak_type": "abrupt",
            "leak_start_time": 9572,
            "leak_end_time": 16123,
            "leak_peak_time": 9572
        }
    ],
    "882": [
        {
            "node_id": "13",
            "leak_diameter": 0.140697442732,
            "leak_type": "abrupt",
            "leak_start_time": 4956,
            "leak_end_time": 10480,
            "leak_peak_time": 4956
        }
    ],
    "883": [
        {
            "node_id": "21",
            "leak_diameter": 0.148396287647,
            "leak_type": "incipient",
            "leak_start_time": 12954,
            "leak_end_time": 14031,
            "leak_peak_time": 12998
        },
        {
            "node_id": "31",
            "leak_diameter": 0.132631384379,
            "leak_type": "incipient",
            "leak_start_time": 7901,
            "leak_end_time": 12919,
            "leak_peak_time": 11350
        }
    ],
    "884": [
        {
            "node_id": "21",
            "leak_diameter": 0.141001001829,
            "leak_type": "incipient",
            "leak_start_time": 17307,
            "leak_end_time": 17509,
            "leak_peak_time": 17384
        },
        {
            "node_id": "23",
            "leak_diameter": 0.141459397772,
            "leak_type": "incipient",
            "leak_start_time": 14070,
            "leak_end_time": 14266,
            "leak_peak_time": 14266
        }
    ],
    "885": [
        {
            "node_id": "21",
            "leak_diameter": 0.0476322512139,
            "leak_type": "abrupt",
            "leak_start_time": 15649,
            "leak_end_time": 17472,
            "leak_peak_time": 15649
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0440053457689,
            "leak_type": "abrupt",
            "leak_start_time": 13286,
            "leak_end_time": 16097,
            "leak_peak_time": 13286
        }
    ],
    "886": [
        {
            "node_id": "10",
            "leak_diameter": 0.141358039782,
            "leak_type": "incipient",
            "leak_start_time": 7673,
            "leak_end_time": 12993,
            "leak_peak_time": 8664
        }
    ],
    "887": [
        {
            "node_id": "31",
            "leak_diameter": 0.169889410184,
            "leak_type": "abrupt",
            "leak_start_time": 10614,
            "leak_end_time": 17371,
            "leak_peak_time": 10614
        }
    ],
    "889": [
        {
            "node_id": "32",
            "leak_diameter": 0.0760229193633,
            "leak_type": "incipient",
            "leak_start_time": 6429,
            "leak_end_time": 14306,
            "leak_peak_time": 12307
        }
    ],
    "890": [
        {
            "node_id": "22",
            "leak_diameter": 0.166002383045,
            "leak_type": "incipient",
            "leak_start_time": 7775,
            "leak_end_time": 15146,
            "leak_peak_time": 8228
        },
        {
            "node_id": "12",
            "leak_diameter": 0.0298164677513,
            "leak_type": "abrupt",
            "leak_start_time": 4071,
            "leak_end_time": 6325,
            "leak_peak_time": 4071
        }
    ],
    "891": [
        {
            "node_id": "10",
            "leak_diameter": 0.139651417111,
            "leak_type": "abrupt",
            "leak_start_time": 3431,
            "leak_end_time": 7883,
            "leak_peak_time": 3431
        },
        {
            "node_id": "13",
            "leak_diameter": 0.1820352144349003,
            "leak_type": "incipient",
            "leak_start_time": 5036,
            "leak_end_time": 7346,
            "leak_peak_time": 5430
        }
    ],
    "892": [
        {
            "node_id": "32",
            "leak_diameter": 0.196319029433,
            "leak_type": "abrupt",
            "leak_start_time": 8140,
            "leak_end_time": 11933,
            "leak_peak_time": 8140
        }
    ],
    "893": [
        {
            "node_id": "2",
            "leak_diameter": 0.196795764364,
            "leak_type": "abrupt",
            "leak_start_time": 6450,
            "leak_end_time": 16106,
            "leak_peak_time": 6450
        }
    ],
    "894": [
        {
            "node_id": "21",
            "leak_diameter": 0.178882522258,
            "leak_type": "abrupt",
            "leak_start_time": 3812,
            "leak_end_time": 14973,
            "leak_peak_time": 3812
        },
        {
            "node_id": "31",
            "leak_diameter": 0.08276597323233278,
            "leak_type": "incipient",
            "leak_start_time": 14528,
            "leak_end_time": 16420,
            "leak_peak_time": 16028
        }
    ],
    "895": [
        {
            "node_id": "12",
            "leak_diameter": 0.188617126862,
            "leak_type": "abrupt",
            "leak_start_time": 11687,
            "leak_end_time": 14509,
            "leak_peak_time": 11687
        }
    ],
    "897": [
        {
            "node_id": "13",
            "leak_diameter": 0.056175542545,
            "leak_type": "abrupt",
            "leak_start_time": 11159,
            "leak_end_time": 14042,
            "leak_peak_time": 11159
        },
        {
            "node_id": "23",
            "leak_diameter": 0.068357307125,
            "leak_type": "abrupt",
            "leak_start_time": 17243,
            "leak_end_time": 17453,
            "leak_peak_time": 17243
        }
    ],
    "898": [
        {
            "node_id": "13",
            "leak_diameter": 0.182378233587,
            "leak_type": "abrupt",
            "leak_start_time": 11915,
            "leak_end_time": 15979,
            "leak_peak_time": 11915
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0658153762833,
            "leak_type": "abrupt",
            "leak_start_time": 2135,
            "leak_end_time": 9124,
            "leak_peak_time": 2135
        },
        {
            "node_id": "32",
            "leak_diameter": 0.05769372747296002,
            "leak_type": "incipient",
            "leak_start_time": 17469,
            "leak_end_time": 17471,
            "leak_peak_time": 17470
        }
    ],
    "901": [
        {
            "node_id": "12",
            "leak_diameter": 0.105275704444,
            "leak_type": "abrupt",
            "leak_start_time": 2664,
            "leak_end_time": 15273,
            "leak_peak_time": 2664
        }
    ],
    "905": [
        {
            "node_id": "13",
            "leak_diameter": 0.16316495797109762,
            "leak_type": "incipient",
            "leak_start_time": 8310,
            "leak_end_time": 12700,
            "leak_peak_time": 12226
        },
        {
            "node_id": "23",
            "leak_diameter": 0.10048067636,
            "leak_type": "abrupt",
            "leak_start_time": 11098,
            "leak_end_time": 16701,
            "leak_peak_time": 11098
        }
    ],
    "906": [
        {
            "node_id": "23",
            "leak_diameter": 0.112338561635,
            "leak_type": "abrupt",
            "leak_start_time": 543,
            "leak_end_time": 4725,
            "leak_peak_time": 543
        }
    ],
    "907": [
        {
            "node_id": "22",
            "leak_diameter": 0.06982460741429201,
            "leak_type": "incipient",
            "leak_start_time": 6708,
            "leak_end_time": 6896,
            "leak_peak_time": 6736
        },
        {
            "node_id": "21",
            "leak_diameter": 0.15371889693651677,
            "leak_type": "incipient",
            "leak_start_time": 4815,
            "leak_end_time": 11688,
            "leak_peak_time": 10392
        }
    ],
    "909": [
        {
            "node_id": "13",
            "leak_diameter": 0.118235266145,
            "leak_type": "abrupt",
            "leak_start_time": 12328,
            "leak_end_time": 16178,
            "leak_peak_time": 12328
        }
    ],
    "911": [
        {
            "node_id": "21",
            "leak_diameter": 0.0514713015298,
            "leak_type": "abrupt",
            "leak_start_time": 15353,
            "leak_end_time": 15835,
            "leak_peak_time": 15353
        }
    ],
    "912": [
        {
            "node_id": "12",
            "leak_diameter": 0.04216739477216012,
            "leak_type": "incipient",
            "leak_start_time": 16400,
            "leak_end_time": 17166,
            "leak_peak_time": 17000
        },
        {
            "node_id": "13",
            "leak_diameter": 0.12093774179638789,
            "leak_type": "incipient",
            "leak_start_time": 554,
            "leak_end_time": 12460,
            "leak_peak_time": 1861
        }
    ],
    "913": [
        {
            "node_id": "13",
            "leak_diameter": 0.0503344446071,
            "leak_type": "abrupt",
            "leak_start_time": 10366,
            "leak_end_time": 12556,
            "leak_peak_time": 10366
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0487799305851,
            "leak_type": "abrupt",
            "leak_start_time": 14821,
            "leak_end_time": 14978,
            "leak_peak_time": 14821
        }
    ],
    "914": [
        {
            "node_id": "10",
            "leak_diameter": 0.0292204025062,
            "leak_type": "abrupt",
            "leak_start_time": 16806,
            "leak_end_time": 16995,
            "leak_peak_time": 16806
        },
        {
            "node_id": "23",
            "leak_diameter": 0.06365357517448625,
            "leak_type": "incipient",
            "leak_start_time": 12148,
            "leak_end_time": 15843,
            "leak_peak_time": 12997
        }
    ],
    "915": [
        {
            "node_id": "22",
            "leak_diameter": 0.0957368762431231,
            "leak_type": "incipient",
            "leak_start_time": 3865,
            "leak_end_time": 12590,
            "leak_peak_time": 4055
        }
    ],
    "916": [
        {
            "node_id": "12",
            "leak_diameter": 0.132196160356,
            "leak_type": "abrupt",
            "leak_start_time": 16861,
            "leak_end_time": 17360,
            "leak_peak_time": 16861
        }
    ],
    "917": [
        {
            "node_id": "13",
            "leak_diameter": 0.0903245769946,
            "leak_type": "abrupt",
            "leak_start_time": 1873,
            "leak_end_time": 7350,
            "leak_peak_time": 1873
        }
    ],
    "918": [
        {
            "node_id": "12",
            "leak_diameter": 0.16145497288925337,
            "leak_type": "incipient",
            "leak_start_time": 7923,
            "leak_end_time": 13784,
            "leak_peak_time": 8821
        }
    ],
    "919": [
        {
            "node_id": "10",
            "leak_diameter": 0.19687290337,
            "leak_type": "abrupt",
            "leak_start_time": 484,
            "leak_end_time": 9855,
            "leak_peak_time": 484
        }
    ],
    "920": [
        {
            "node_id": "31",
            "leak_diameter": 0.181327022654,
            "leak_type": "abrupt",
            "leak_start_time": 54,
            "leak_end_time": 1137,
            "leak_peak_time": 54
        }
    ],
    "921": [
        {
            "node_id": "21",
            "leak_diameter": 0.193880524165,
            "leak_type": "abrupt",
            "leak_start_time": 3713,
            "leak_end_time": 15436,
            "leak_peak_time": 3713
        }
    ],
    "922": [
        {
            "node_id": "22",
            "leak_diameter": 0.1177711702,
            "leak_type": "abrupt",
            "leak_start_time": 1973,
            "leak_end_time": 10364,
            "leak_peak_time": 1973
        }
    ],
    "923": [
        {
            "node_id": "13",
            "leak_diameter": 0.188734214834,
            "leak_type": "abrupt",
            "leak_start_time": 7108,
            "leak_end_time": 8858,
            "leak_peak_time": 7108
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0237882979418,
            "leak_type": "abrupt",
            "leak_start_time": 2393,
            "leak_end_time": 10285,
            "leak_peak_time": 2393
        }
    ],
    "924": [
        {
            "node_id": "23",
            "leak_diameter": 0.04494531560255294,
            "leak_type": "incipient",
            "leak_start_time": 4543,
            "leak_end_time": 5932,
            "leak_peak_time": 5454
        },
        {
            "node_id": "31",
            "leak_diameter": 0.06384944521457378,
            "leak_type": "incipient",
            "leak_start_time": 14744,
            "leak_end_time": 17214,
            "leak_peak_time": 16242
        }
    ],
    "926": [
        {
            "node_id": "31",
            "leak_diameter": 0.1267009317911675,
            "leak_type": "incipient",
            "leak_start_time": 16388,
            "leak_end_time": 17380,
            "leak_peak_time": 17320
        }
    ],
    "927": [
        {
            "node_id": "10",
            "leak_diameter": 0.028216539219121307,
            "leak_type": "incipient",
            "leak_start_time": 11551,
            "leak_end_time": 13678,
            "leak_peak_time": 13009
        }
    ],
    "928": [
        {
            "node_id": "22",
            "leak_diameter": 0.0988121756585,
            "leak_type": "abrupt",
            "leak_start_time": 13584,
            "leak_end_time": 14580,
            "leak_peak_time": 13584
        },
        {
            "node_id": "12",
            "leak_diameter": 0.1725374221542286,
            "leak_type": "incipient",
            "leak_start_time": 17289,
            "leak_end_time": 17518,
            "leak_peak_time": 17413
        }
    ],
    "930": [
        {
            "node_id": "13",
            "leak_diameter": 0.16856407584776248,
            "leak_type": "incipient",
            "leak_start_time": 15601,
            "leak_end_time": 17311,
            "leak_peak_time": 16737
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0204719659305,
            "leak_type": "abrupt",
            "leak_start_time": 813,
            "leak_end_time": 4358,
            "leak_peak_time": 813
        }
    ],
    "931": [
        {
            "node_id": "12",
            "leak_diameter": 0.151836613511,
            "leak_type": "abrupt",
            "leak_start_time": 287,
            "leak_end_time": 13500,
            "leak_peak_time": 287
        }
    ],
    "933": [
        {
            "node_id": "13",
            "leak_diameter": 0.0219756113383,
            "leak_type": "abrupt",
            "leak_start_time": 1588,
            "leak_end_time": 3840,
            "leak_peak_time": 1588
        },
        {
            "node_id": "2",
            "leak_diameter": 0.05481515085614716,
            "leak_type": "incipient",
            "leak_start_time": 12581,
            "leak_end_time": 13894,
            "leak_peak_time": 12922
        }
    ],
    "934": [
        {
            "node_id": "22",
            "leak_diameter": 0.025506999745664446,
            "leak_type": "incipient",
            "leak_start_time": 2414,
            "leak_end_time": 10885,
            "leak_peak_time": 5107
        },
        {
            "node_id": "13",
            "leak_diameter": 0.110365880515,
            "leak_type": "abrupt",
            "leak_start_time": 10953,
            "leak_end_time": 16143,
            "leak_peak_time": 10953
        }
    ],
    "935": [
        {
            "node_id": "22",
            "leak_diameter": 0.0288903527438,
            "leak_type": "abrupt",
            "leak_start_time": 8645,
            "leak_end_time": 16012,
            "leak_peak_time": 8645
        }
    ],
    "936": [
        {
            "node_id": "10",
            "leak_diameter": 0.155902729055,
            "leak_type": "abrupt",
            "leak_start_time": 788,
            "leak_end_time": 5242,
            "leak_peak_time": 788
        },
        {
            "node_id": "31",
            "leak_diameter": 0.119787286973,
            "leak_type": "abrupt",
            "leak_start_time": 15646,
            "leak_end_time": 16243,
            "leak_peak_time": 15646
        }
    ],
    "937": [
        {
            "node_id": "10",
            "leak_diameter": 0.18500471453436532,
            "leak_type": "incipient",
            "leak_start_time": 10535,
            "leak_end_time": 16937,
            "leak_peak_time": 14378
        }
    ],
    "938": [
        {
            "node_id": "22",
            "leak_diameter": 0.18721084271075342,
            "leak_type": "incipient",
            "leak_start_time": 2211,
            "leak_end_time": 5691,
            "leak_peak_time": 4584
        },
        {
            "node_id": "21",
            "leak_diameter": 0.152483702632,
            "leak_type": "abrupt",
            "leak_start_time": 10873,
            "leak_end_time": 14177,
            "leak_peak_time": 10873
        }
    ],
    "939": [
        {
            "node_id": "13",
            "leak_diameter": 0.162529766632,
            "leak_type": "abrupt",
            "leak_start_time": 11932,
            "leak_end_time": 16059,
            "leak_peak_time": 11932
        },
        {
            "node_id": "23",
            "leak_diameter": 0.07188014490699338,
            "leak_type": "incipient",
            "leak_start_time": 9167,
            "leak_end_time": 9635,
            "leak_peak_time": 9410
        }
    ],
    "940": [
        {
            "node_id": "13",
            "leak_diameter": 0.1024248813166316,
            "leak_type": "incipient",
            "leak_start_time": 4926,
            "leak_end_time": 10961,
            "leak_peak_time": 7157
        },
        {
            "node_id": "32",
            "leak_diameter": 0.13692364475,
            "leak_type": "abrupt",
            "leak_start_time": 13315,
            "leak_end_time": 13453,
            "leak_peak_time": 13315
        }
    ],
    "941": [
        {
            "node_id": "12",
            "leak_diameter": 0.14102015993389705,
            "leak_type": "incipient",
            "leak_start_time": 14803,
            "leak_end_time": 15831,
            "leak_peak_time": 14857
        }
    ],
    "942": [
        {
            "node_id": "13",
            "leak_diameter": 0.0682530370936,
            "leak_type": "abrupt",
            "leak_start_time": 13961,
            "leak_end_time": 14326,
            "leak_peak_time": 13961
        }
    ],
    "943": [
        {
            "node_id": "13",
            "leak_diameter": 0.0208805236834,
            "leak_type": "abrupt",
            "leak_start_time": 1313,
            "leak_end_time": 16202,
            "leak_peak_time": 1313
        }
    ],
    "945": [
        {
            "node_id": "31",
            "leak_diameter": 0.05156703391819057,
            "leak_type": "incipient",
            "leak_start_time": 4005,
            "leak_end_time": 11297,
            "leak_peak_time": 6351
        }
    ],
    "946": [
        {
            "node_id": "22",
            "leak_diameter": 0.168676242858,
            "leak_type": "incipient",
            "leak_start_time": 6032,
            "leak_end_time": 16115,
            "leak_peak_time": 14866
        }
    ],
    "947": [
        {
            "node_id": "12",
            "leak_diameter": 0.0409660597486,
            "leak_type": "incipient",
            "leak_start_time": 8288,
            "leak_end_time": 11322,
            "leak_peak_time": 9120
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0310577963344,
            "leak_type": "abrupt",
            "leak_start_time": 3481,
            "leak_end_time": 5604,
            "leak_peak_time": 3481
        }
    ],
    "948": [
        {
            "node_id": "22",
            "leak_diameter": 0.0214688227785,
            "leak_type": "incipient",
            "leak_start_time": 618,
            "leak_end_time": 17261,
            "leak_peak_time": 8552
        }
    ],
    "949": [
        {
            "node_id": "10",
            "leak_diameter": 0.184780873219,
            "leak_type": "abrupt",
            "leak_start_time": 5142,
            "leak_end_time": 6135,
            "leak_peak_time": 5142
        }
    ],
    "950": [
        {
            "node_id": "31",
            "leak_diameter": 0.0216958747251,
            "leak_type": "abrupt",
            "leak_start_time": 8319,
            "leak_end_time": 12300,
            "leak_peak_time": 8319
        }
    ],
    "951": [
        {
            "node_id": "21",
            "leak_diameter": 0.164192559907,
            "leak_type": "abrupt",
            "leak_start_time": 9904,
            "leak_end_time": 15590,
            "leak_peak_time": 9904
        },
        {
            "node_id": "2",
            "leak_diameter": 0.0396315106227,
            "leak_type": "abrupt",
            "leak_start_time": 2673,
            "leak_end_time": 4019,
            "leak_peak_time": 2673
        }
    ],
    "952": [
        {
            "node_id": "12",
            "leak_diameter": 0.0957549119199,
            "leak_type": "incipient",
            "leak_start_time": 3553,
            "leak_end_time": 13676,
            "leak_peak_time": 6446
        },
        {
            "node_id": "21",
            "leak_diameter": 0.161425063144,
            "leak_type": "incipient",
            "leak_start_time": 7948,
            "leak_end_time": 13253,
            "leak_peak_time": 11856
        }
    ],
    "953": [
        {
            "node_id": "23",
            "leak_diameter": 0.195273804604,
            "leak_type": "incipient",
            "leak_start_time": 16514,
            "leak_end_time": 16689,
            "leak_peak_time": 16662
        }
    ],
    "955": [
        {
            "node_id": "21",
            "leak_diameter": 0.105855002473,
            "leak_type": "abrupt",
            "leak_start_time": 17409,
            "leak_end_time": 17511,
            "leak_peak_time": 17409
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0885169580592,
            "leak_type": "incipient",
            "leak_start_time": 6706,
            "leak_end_time": 17168,
            "leak_peak_time": 9903
        }
    ],
    "956": [
        {
            "node_id": "23",
            "leak_diameter": 0.0583965600831,
            "leak_type": "incipient",
            "leak_start_time": 16493,
            "leak_end_time": 16582,
            "leak_peak_time": 16494
        }
    ],
    "960": [
        {
            "node_id": "13",
            "leak_diameter": 0.0708432885271,
            "leak_type": "abrupt",
            "leak_start_time": 17399,
            "leak_end_time": 17463,
            "leak_peak_time": 17399
        }
    ],
    "961": [
        {
            "node_id": "22",
            "leak_diameter": 0.0782584270813,
            "leak_type": "incipient",
            "leak_start_time": 11989,
            "leak_end_time": 12574,
            "leak_peak_time": 12413
        },
        {
            "node_id": "21",
            "leak_diameter": 0.144769561505,
            "leak_type": "abrupt",
            "leak_start_time": 16107,
            "leak_end_time": 16725,
            "leak_peak_time": 16107
        }
    ],
    "962": [
        {
            "node_id": "32",
            "leak_diameter": 0.0531447858169,
            "leak_type": "incipient",
            "leak_start_time": 6356,
            "leak_end_time": 8501,
            "leak_peak_time": 6866
        }
    ],
    "966": [
        {
            "node_id": "21",
            "leak_diameter": 0.0750866822765,
            "leak_type": "abrupt",
            "leak_start_time": 9986,
            "leak_end_time": 12871,
            "leak_peak_time": 9986
        },
        {
            "node_id": "31",
            "leak_diameter": 0.126320704325,
            "leak_type": "abrupt",
            "leak_start_time": 4380,
            "leak_end_time": 15161,
            "leak_peak_time": 4380
        }
    ],
    "967": [
        {
            "node_id": "2",
            "leak_diameter": 0.0538141159929,
            "leak_type": "abrupt",
            "leak_start_time": 12978,
            "leak_end_time": 14843,
            "leak_peak_time": 12978
        }
    ],
    "969": [
        {
            "node_id": "13",
            "leak_diameter": 0.0837770426916,
            "leak_type": "abrupt",
            "leak_start_time": 3840,
            "leak_end_time": 6139,
            "leak_peak_time": 3840
        },
        {
            "node_id": "32",
            "leak_diameter": 0.064917279969,
            "leak_type": "incipient",
            "leak_start_time": 15743,
            "leak_end_time": 16337,
            "leak_peak_time": 15963
        }
    ],
    "970": [
        {
            "node_id": "32",
            "leak_diameter": 0.113685326412,
            "leak_type": "incipient",
            "leak_start_time": 16829,
            "leak_end_time": 17189,
            "leak_peak_time": 17147
        }
    ],
    "971": [
        {
            "node_id": "10",
            "leak_diameter": 0.02537838831,
            "leak_type": "incipient",
            "leak_start_time": 1455,
            "leak_end_time": 14397,
            "leak_peak_time": 9630
        },
        {
            "node_id": "13",
            "leak_diameter": 0.135462998299,
            "leak_type": "incipient",
            "leak_start_time": 16312,
            "leak_end_time": 16976,
            "leak_peak_time": 16834
        }
    ],
    "974": [
        {
            "node_id": "12",
            "leak_diameter": 0.0658169625212,
            "leak_type": "incipient",
            "leak_start_time": 3072,
            "leak_end_time": 13138,
            "leak_peak_time": 4393
        }
    ],
    "975": [
        {
            "node_id": "23",
            "leak_diameter": 0.0582078139544,
            "leak_type": "abrupt",
            "leak_start_time": 10737,
            "leak_end_time": 14985,
            "leak_peak_time": 10737
        }
    ],
    "977": [
        {
            "node_id": "23",
            "leak_diameter": 0.159763606126,
            "leak_type": "incipient",
            "leak_start_time": 1505,
            "leak_end_time": 6829,
            "leak_peak_time": 2896
        }
    ],
    "978": [
        {
            "node_id": "13",
            "leak_diameter": 0.108001775896,
            "leak_type": "incipient",
            "leak_start_time": 14891,
            "leak_end_time": 15400,
            "leak_peak_time": 15054
        },
        {
            "node_id": "23",
            "leak_diameter": 0.15819596756,
            "leak_type": "incipient",
            "leak_start_time": 768,
            "leak_end_time": 12562,
            "leak_peak_time": 6155
        }
    ],
    "980": [
        {
            "node_id": "31",
            "leak_diameter": 0.0630692303214,
            "leak_type": "abrupt",
            "leak_start_time": 5690,
            "leak_end_time": 13690,
            "leak_peak_time": 5690
        }
    ],
    "982": [
        {
            "node_id": "12",
            "leak_diameter": 0.125813819438,
            "leak_type": "abrupt",
            "leak_start_time": 8145,
            "leak_end_time": 8488,
            "leak_peak_time": 8145
        }
    ],
    "983": [
        {
            "node_id": "31",
            "leak_diameter": 0.057313025983,
            "leak_type": "incipient",
            "leak_start_time": 4392,
            "leak_end_time": 5882,
            "leak_peak_time": 5759
        }
    ],
    "984": [
        {
            "node_id": "22",
            "leak_diameter": 0.020561630606,
            "leak_type": "incipient",
            "leak_start_time": 6677,
            "leak_end_time": 14156,
            "leak_peak_time": 11309
        },
        {
            "node_id": "12",
            "leak_diameter": 0.122836275921,
            "leak_type": "incipient",
            "leak_start_time": 5632,
            "leak_end_time": 11284,
            "leak_peak_time": 8776
        }
    ],
    "985": [
        {
            "node_id": "31",
            "leak_diameter": 0.0893170237639,
            "leak_type": "incipient",
            "leak_start_time": 12678,
            "leak_end_time": 14350,
            "leak_peak_time": 14058
        }
    ],
    "987": [
        {
            "node_id": "12",
            "leak_diameter": 0.0924288945723,
            "leak_type": "incipient",
            "leak_start_time": 11893,
            "leak_end_time": 16862,
            "leak_peak_time": 16176
        },
        {
            "node_id": "21",
            "leak_diameter": 0.178216311857,
            "leak_type": "incipient",
            "leak_start_time": 7980,
            "leak_end_time": 16084,
            "leak_peak_time": 14378
        }
    ],
    "988": [
        {
            "node_id": "2",
            "leak_diameter": 0.0649615244248,
            "leak_type": "incipient",
            "leak_start_time": 14881,
            "leak_end_time": 17380,
            "leak_peak_time": 16285
        }
    ],
    "989": [
        {
            "node_id": "32",
            "leak_diameter": 0.152544628622,
            "leak_type": "abrupt",
            "leak_start_time": 10714,
            "leak_end_time": 17162,
            "leak_peak_time": 10714
        }
    ],
    "990": [
        {
            "node_id": "22",
            "leak_diameter": 0.148060582295,
            "leak_type": "incipient",
            "leak_start_time": 704,
            "leak_end_time": 6994,
            "leak_peak_time": 1384
        }
    ],
    "991": [
        {
            "node_id": "23",
            "leak_diameter": 0.194384747288,
            "leak_type": "abrupt",
            "leak_start_time": 17377,
            "leak_end_time": 17455,
            "leak_peak_time": 17377
        }
    ],
    "992": [
        {
            "node_id": "21",
            "leak_diameter": 0.0645001685133,
            "leak_type": "incipient",
            "leak_start_time": 13880,
            "leak_end_time": 16699,
            "leak_peak_time": 15947
        }
    ],
    "993": [
        {
            "node_id": "2",
            "leak_diameter": 0.0433197192394,
            "leak_type": "abrupt",
            "leak_start_time": 1390,
            "leak_end_time": 8305,
            "leak_peak_time": 1390
        }
    ],
    "995": [
        {
            "node_id": "31",
            "leak_diameter": 0.123659925448,
            "leak_type": "abrupt",
            "leak_start_time": 1328,
            "leak_end_time": 13165,
            "leak_peak_time": 1328
        }
    ],
    "996": [
        {
            "node_id": "12",
            "leak_diameter": 0.133615471374,
            "leak_type": "incipient",
            "leak_start_time": 9793,
            "leak_end_time": 12994,
            "leak_peak_time": 10636
        }
    ],
    "997": [
        {
            "node_id": "13",
            "leak_diameter": 0.148244220224,
            "leak_type": "incipient",
            "leak_start_time": 7773,
            "leak_end_time": 12771,
            "leak_peak_time": 9765
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0391237453821,
            "leak_type": "incipient",
            "leak_start_time": 7118,
            "leak_end_time": 13306,
            "leak_peak_time": 11771
        }
    ],
    "998": [
        {
            "node_id": "23",
            "leak_diameter": 0.140603342436,
            "leak_type": "incipient",
            "leak_start_time": 10477,
            "leak_end_time": 14669,
            "leak_peak_time": 12243
        }
    ],
    "1000": [
        {
            "node_id": "2",
            "leak_diameter": 0.146038778191,
            "leak_type": "abrupt",
            "leak_start_time": 8295,
            "leak_end_time": 9276,
            "leak_peak_time": 8295
        }
    ]
}"""

HANOI_LEAKAGES = """{
    "2": [
        {
            "node_id": "6",
            "leak_diameter": 0.0247058291508,
            "leak_type": "incipient",
            "leak_start_time": 15425,
            "leak_end_time": 16250,
            "leak_peak_time": 15888
        }
    ],
    "3": [
        {
            "node_id": "13",
            "leak_diameter": 0.145137485896,
            "leak_type": "incipient",
            "leak_start_time": 134,
            "leak_end_time": 8532,
            "leak_peak_time": 8484
        }
    ],
    "4": [
        {
            "node_id": "14",
            "leak_diameter": 0.161611946124,
            "leak_type": "abrupt",
            "leak_start_time": 15097,
            "leak_end_time": 15481,
            "leak_peak_time": 15097
        }
    ],
    "6": [
        {
            "node_id": "6",
            "leak_diameter": 0.102029825465,
            "leak_type": "incipient",
            "leak_start_time": 13471,
            "leak_end_time": 17483,
            "leak_peak_time": 15875
        }
    ],
    "7": [
        {
            "node_id": "10",
            "leak_diameter": 0.0389695322987,
            "leak_type": "abrupt",
            "leak_start_time": 4307,
            "leak_end_time": 15177,
            "leak_peak_time": 4307
        }
    ],
    "8": [
        {
            "node_id": "23",
            "leak_diameter": 0.051825684046,
            "leak_type": "abrupt",
            "leak_start_time": 5864,
            "leak_end_time": 11741,
            "leak_peak_time": 5864
        }
    ],
    "9": [
        {
            "node_id": "7",
            "leak_diameter": 0.189386235258,
            "leak_type": "abrupt",
            "leak_start_time": 8545,
            "leak_end_time": 16208,
            "leak_peak_time": 8545
        }
    ],
    "11": [
        {
            "node_id": "12",
            "leak_diameter": 0.0714821729357,
            "leak_type": "abrupt",
            "leak_start_time": 3611,
            "leak_end_time": 4988,
            "leak_peak_time": 3611
        }
    ],
    "13": [
        {
            "node_id": "21",
            "leak_diameter": 0.12343731842,
            "leak_type": "abrupt",
            "leak_start_time": 6587,
            "leak_end_time": 10926,
            "leak_peak_time": 6587
        },
        {
            "node_id": "30",
            "leak_diameter": 0.0701974129183,
            "leak_type": "abrupt",
            "leak_start_time": 9359,
            "leak_end_time": 12958,
            "leak_peak_time": 9359
        }
    ],
    "15": [
        {
            "node_id": "3",
            "leak_diameter": 0.190635506617,
            "leak_type": "incipient",
            "leak_start_time": 4699,
            "leak_end_time": 14674,
            "leak_peak_time": 10893
        },
        {
            "node_id": "26",
            "leak_diameter": 0.0851028565658,
            "leak_type": "abrupt",
            "leak_start_time": 2393,
            "leak_end_time": 2463,
            "leak_peak_time": 2393
        }
    ],
    "16": [
        {
            "node_id": "3",
            "leak_diameter": 0.0550355360287,
            "leak_type": "abrupt",
            "leak_start_time": 8956,
            "leak_end_time": 12632,
            "leak_peak_time": 8956
        }
    ],
    "17": [
        {
            "node_id": "20",
            "leak_diameter": 0.0225874581586,
            "leak_type": "incipient",
            "leak_start_time": 8290,
            "leak_end_time": 13199,
            "leak_peak_time": 11263
        }
    ],
    "18": [
        {
            "node_id": "29",
            "leak_diameter": 0.168659239822,
            "leak_type": "abrupt",
            "leak_start_time": 3659,
            "leak_end_time": 7209,
            "leak_peak_time": 3659
        },
        {
            "node_id": "13",
            "leak_diameter": 0.0654910819542,
            "leak_type": "abrupt",
            "leak_start_time": 637,
            "leak_end_time": 16388,
            "leak_peak_time": 637
        }
    ],
    "19": [
        {
            "node_id": "20",
            "leak_diameter": 0.187805586465,
            "leak_type": "abrupt",
            "leak_start_time": 6607,
            "leak_end_time": 16718,
            "leak_peak_time": 6607
        }
    ],
    "20": [
        {
            "node_id": "15",
            "leak_diameter": 0.12021259218,
            "leak_type": "incipient",
            "leak_start_time": 13934,
            "leak_end_time": 16115,
            "leak_peak_time": 13992
        }
    ],
    "21": [
        {
            "node_id": "7",
            "leak_diameter": 0.0326442625759,
            "leak_type": "abrupt",
            "leak_start_time": 13267,
            "leak_end_time": 16449,
            "leak_peak_time": 13267
        }
    ],
    "22": [
        {
            "node_id": "2",
            "leak_diameter": 0.139090660709,
            "leak_type": "abrupt",
            "leak_start_time": 9552,
            "leak_end_time": 11307,
            "leak_peak_time": 9552
        },
        {
            "node_id": "9",
            "leak_diameter": 0.0340948267549,
            "leak_type": "abrupt",
            "leak_start_time": 11285,
            "leak_end_time": 13459,
            "leak_peak_time": 11285
        }
    ],
    "23": [
        {
            "node_id": "4",
            "leak_diameter": 0.0651441790093,
            "leak_type": "incipient",
            "leak_start_time": 469,
            "leak_end_time": 3349,
            "leak_peak_time": 728
        }
    ],
    "24": [
        {
            "node_id": "9",
            "leak_diameter": 0.0486811771186,
            "leak_type": "abrupt",
            "leak_start_time": 2126,
            "leak_end_time": 12023,
            "leak_peak_time": 2126
        }
    ],
    "25": [
        {
            "node_id": "31",
            "leak_diameter": 0.0965776367439,
            "leak_type": "incipient",
            "leak_start_time": 15285,
            "leak_end_time": 16660,
            "leak_peak_time": 16313
        }
    ],
    "26": [
        {
            "node_id": "12",
            "leak_diameter": 0.118355690067,
            "leak_type": "abrupt",
            "leak_start_time": 764,
            "leak_end_time": 4261,
            "leak_peak_time": 764
        }
    ],
    "30": [
        {
            "node_id": "28",
            "leak_diameter": 0.0280584704018,
            "leak_type": "abrupt",
            "leak_start_time": 381,
            "leak_end_time": 5511,
            "leak_peak_time": 381
        }
    ],
    "31": [
        {
            "node_id": "28",
            "leak_diameter": 0.171546520876,
            "leak_type": "incipient",
            "leak_start_time": 13376,
            "leak_end_time": 14838,
            "leak_peak_time": 14365
        },
        {
            "node_id": "8",
            "leak_diameter": 0.0396804999104,
            "leak_type": "incipient",
            "leak_start_time": 11301,
            "leak_end_time": 16881,
            "leak_peak_time": 15601
        }
    ],
    "32": [
        {
            "node_id": "9",
            "leak_diameter": 0.0761378760036,
            "leak_type": "incipient",
            "leak_start_time": 2145,
            "leak_end_time": 4925,
            "leak_peak_time": 3481
        }
    ],
    "33": [
        {
            "node_id": "21",
            "leak_diameter": 0.155177542324,
            "leak_type": "abrupt",
            "leak_start_time": 7480,
            "leak_end_time": 13547,
            "leak_peak_time": 7480
        },
        {
            "node_id": "13",
            "leak_diameter": 0.111172999366,
            "leak_type": "incipient",
            "leak_start_time": 10526,
            "leak_end_time": 12781,
            "leak_peak_time": 12028
        }
    ],
    "34": [
        {
            "node_id": "32",
            "leak_diameter": 0.0454438923386,
            "leak_type": "incipient",
            "leak_start_time": 5999,
            "leak_end_time": 11802,
            "leak_peak_time": 6801
        },
        {
            "node_id": "9",
            "leak_diameter": 0.125395842995,
            "leak_type": "incipient",
            "leak_start_time": 7512,
            "leak_end_time": 8142,
            "leak_peak_time": 7704
        }
    ],
    "35": [
        {
            "node_id": "21",
            "leak_diameter": 0.140699467339,
            "leak_type": "abrupt",
            "leak_start_time": 15447,
            "leak_end_time": 16965,
            "leak_peak_time": 15447
        },
        {
            "node_id": "26",
            "leak_diameter": 0.138231681419,
            "leak_type": "incipient",
            "leak_start_time": 369,
            "leak_end_time": 14466,
            "leak_peak_time": 12040
        }
    ],
    "36": [
        {
            "node_id": "4",
            "leak_diameter": 0.157820228403,
            "leak_type": "incipient",
            "leak_start_time": 2472,
            "leak_end_time": 7731,
            "leak_peak_time": 7109
        }
    ],
    "37": [
        {
            "node_id": "11",
            "leak_diameter": 0.156850337739,
            "leak_type": "abrupt",
            "leak_start_time": 16000,
            "leak_end_time": 17141,
            "leak_peak_time": 16000
        },
        {
            "node_id": "16",
            "leak_diameter": 0.162956202273,
            "leak_type": "abrupt",
            "leak_start_time": 6153,
            "leak_end_time": 11101,
            "leak_peak_time": 6153
        }
    ],
    "38": [
        {
            "node_id": "3",
            "leak_diameter": 0.108921149932,
            "leak_type": "abrupt",
            "leak_start_time": 2190,
            "leak_end_time": 8321,
            "leak_peak_time": 2190
        },
        {
            "node_id": "5",
            "leak_diameter": 0.0923524726725,
            "leak_type": "abrupt",
            "leak_start_time": 14119,
            "leak_end_time": 14600,
            "leak_peak_time": 14119
        }
    ],
    "39": [
        {
            "node_id": "20",
            "leak_diameter": 0.120923567087,
            "leak_type": "incipient",
            "leak_start_time": 3282,
            "leak_end_time": 5387,
            "leak_peak_time": 5322
        }
    ],
    "40": [
        {
            "node_id": "32",
            "leak_diameter": 0.154999943749,
            "leak_type": "abrupt",
            "leak_start_time": 1814,
            "leak_end_time": 10573,
            "leak_peak_time": 1814
        }
    ],
    "41": [
        {
            "node_id": "22",
            "leak_diameter": 0.0973436769888,
            "leak_type": "abrupt",
            "leak_start_time": 6219,
            "leak_end_time": 8008,
            "leak_peak_time": 6219
        },
        {
            "node_id": "5",
            "leak_diameter": 0.078928695195,
            "leak_type": "incipient",
            "leak_start_time": 11954,
            "leak_end_time": 15828,
            "leak_peak_time": 13078
        }
    ],
    "42": [
        {
            "node_id": "4",
            "leak_diameter": 0.190164153306,
            "leak_type": "abrupt",
            "leak_start_time": 4052,
            "leak_end_time": 7202,
            "leak_peak_time": 4052
        },
        {
            "node_id": "30",
            "leak_diameter": 0.145986161671,
            "leak_type": "incipient",
            "leak_start_time": 11286,
            "leak_end_time": 13456,
            "leak_peak_time": 12945
        }
    ],
    "43": [
        {
            "node_id": "22",
            "leak_diameter": 0.0739068802101,
            "leak_type": "abrupt",
            "leak_start_time": 10850,
            "leak_end_time": 12618,
            "leak_peak_time": 10850
        }
    ],
    "45": [
        {
            "node_id": "21",
            "leak_diameter": 0.0587160854422,
            "leak_type": "abrupt",
            "leak_start_time": 11266,
            "leak_end_time": 17004,
            "leak_peak_time": 11266
        }
    ],
    "46": [
        {
            "node_id": "6",
            "leak_diameter": 0.154972390694,
            "leak_type": "abrupt",
            "leak_start_time": 1487,
            "leak_end_time": 17392,
            "leak_peak_time": 1487
        }
    ],
    "47": [
        {
            "node_id": "12",
            "leak_diameter": 0.177611612047,
            "leak_type": "incipient",
            "leak_start_time": 13532,
            "leak_end_time": 15503,
            "leak_peak_time": 14637
        },
        {
            "node_id": "8",
            "leak_diameter": 0.174502528241,
            "leak_type": "abrupt",
            "leak_start_time": 10668,
            "leak_end_time": 12765,
            "leak_peak_time": 10668
        }
    ],
    "49": [
        {
            "node_id": "23",
            "leak_diameter": 0.125453388293,
            "leak_type": "incipient",
            "leak_start_time": 9811,
            "leak_end_time": 12294,
            "leak_peak_time": 9880
        }
    ],
    "50": [
        {
            "node_id": "23",
            "leak_diameter": 0.135828534761,
            "leak_type": "abrupt",
            "leak_start_time": 8532,
            "leak_end_time": 9130,
            "leak_peak_time": 8532
        }
    ],
    "52": [
        {
            "node_id": "20",
            "leak_diameter": 0.0433286060941,
            "leak_type": "incipient",
            "leak_start_time": 11213,
            "leak_end_time": 13343,
            "leak_peak_time": 13043
        }
    ],
    "54": [
        {
            "node_id": "20",
            "leak_diameter": 0.0908900536678,
            "leak_type": "incipient",
            "leak_start_time": 1694,
            "leak_end_time": 16141,
            "leak_peak_time": 12292
        }
    ],
    "56": [
        {
            "node_id": "6",
            "leak_diameter": 0.174035887674,
            "leak_type": "incipient",
            "leak_start_time": 10059,
            "leak_end_time": 12342,
            "leak_peak_time": 10305
        },
        {
            "node_id": "19",
            "leak_diameter": 0.104993989202,
            "leak_type": "incipient",
            "leak_start_time": 3743,
            "leak_end_time": 16953,
            "leak_peak_time": 11589
        }
    ],
    "57": [
        {
            "node_id": "16",
            "leak_diameter": 0.0503146388674,
            "leak_type": "incipient",
            "leak_start_time": 13198,
            "leak_end_time": 15493,
            "leak_peak_time": 14761
        }
    ],
    "58": [
        {
            "node_id": "15",
            "leak_diameter": 0.0431859769341,
            "leak_type": "abrupt",
            "leak_start_time": 10243,
            "leak_end_time": 15423,
            "leak_peak_time": 10243
        }
    ],
    "59": [
        {
            "node_id": "21",
            "leak_diameter": 0.0756514002848,
            "leak_type": "incipient",
            "leak_start_time": 12812,
            "leak_end_time": 13496,
            "leak_peak_time": 13419
        }
    ],
    "60": [
        {
            "node_id": "4",
            "leak_diameter": 0.14936370457,
            "leak_type": "incipient",
            "leak_start_time": 508,
            "leak_end_time": 2839,
            "leak_peak_time": 1706
        }
    ],
    "61": [
        {
            "node_id": "4",
            "leak_diameter": 0.153206074968,
            "leak_type": "abrupt",
            "leak_start_time": 6114,
            "leak_end_time": 6946,
            "leak_peak_time": 6114
        },
        {
            "node_id": "19",
            "leak_diameter": 0.0952087997831,
            "leak_type": "incipient",
            "leak_start_time": 11425,
            "leak_end_time": 13513,
            "leak_peak_time": 13228
        }
    ],
    "62": [
        {
            "node_id": "15",
            "leak_diameter": 0.125846809053,
            "leak_type": "abrupt",
            "leak_start_time": 16830,
            "leak_end_time": 17016,
            "leak_peak_time": 16830
        },
        {
            "node_id": "30",
            "leak_diameter": 0.195143880396,
            "leak_type": "incipient",
            "leak_start_time": 16215,
            "leak_end_time": 16685,
            "leak_peak_time": 16606
        }
    ],
    "63": [
        {
            "node_id": "5",
            "leak_diameter": 0.0721833072728,
            "leak_type": "incipient",
            "leak_start_time": 15719,
            "leak_end_time": 16983,
            "leak_peak_time": 15794
        },
        {
            "node_id": "30",
            "leak_diameter": 0.136206791052,
            "leak_type": "abrupt",
            "leak_start_time": 8312,
            "leak_end_time": 15260,
            "leak_peak_time": 8312
        }
    ],
    "64": [
        {
            "node_id": "8",
            "leak_diameter": 0.15181267598,
            "leak_type": "incipient",
            "leak_start_time": 11648,
            "leak_end_time": 15777,
            "leak_peak_time": 12876
        }
    ],
    "66": [
        {
            "node_id": "6",
            "leak_diameter": 0.0386598798481,
            "leak_type": "incipient",
            "leak_start_time": 9815,
            "leak_end_time": 13925,
            "leak_peak_time": 10264
        },
        {
            "node_id": "3",
            "leak_diameter": 0.152982171534,
            "leak_type": "incipient",
            "leak_start_time": 11579,
            "leak_end_time": 14554,
            "leak_peak_time": 14522
        }
    ],
    "68": [
        {
            "node_id": "15",
            "leak_diameter": 0.166624130575,
            "leak_type": "abrupt",
            "leak_start_time": 15211,
            "leak_end_time": 17267,
            "leak_peak_time": 15211
        }
    ],
    "69": [
        {
            "node_id": "25",
            "leak_diameter": 0.0509632013426,
            "leak_type": "incipient",
            "leak_start_time": 16650,
            "leak_end_time": 16657,
            "leak_peak_time": 16653
        },
        {
            "node_id": "26",
            "leak_diameter": 0.126651212411,
            "leak_type": "incipient",
            "leak_start_time": 9882,
            "leak_end_time": 15806,
            "leak_peak_time": 15350
        }
    ],
    "70": [
        {
            "node_id": "17",
            "leak_diameter": 0.195288458359,
            "leak_type": "abrupt",
            "leak_start_time": 14727,
            "leak_end_time": 15295,
            "leak_peak_time": 14727
        },
        {
            "node_id": "3",
            "leak_diameter": 0.125213649722,
            "leak_type": "incipient",
            "leak_start_time": 981,
            "leak_end_time": 15723,
            "leak_peak_time": 8193
        }
    ],
    "71": [
        {
            "node_id": "9",
            "leak_diameter": 0.115247107902,
            "leak_type": "abrupt",
            "leak_start_time": 15321,
            "leak_end_time": 17105,
            "leak_peak_time": 15321
        }
    ],
    "72": [
        {
            "node_id": "15",
            "leak_diameter": 0.0300696343219,
            "leak_type": "abrupt",
            "leak_start_time": 10962,
            "leak_end_time": 13066,
            "leak_peak_time": 10962
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0700798648545,
            "leak_type": "incipient",
            "leak_start_time": 13027,
            "leak_end_time": 16036,
            "leak_peak_time": 14379
        }
    ],
    "73": [
        {
            "node_id": "16",
            "leak_diameter": 0.0573896078912,
            "leak_type": "incipient",
            "leak_start_time": 12169,
            "leak_end_time": 17272,
            "leak_peak_time": 13825
        },
        {
            "node_id": "18",
            "leak_diameter": 0.0809944803801,
            "leak_type": "abrupt",
            "leak_start_time": 13687,
            "leak_end_time": 15193,
            "leak_peak_time": 13687
        }
    ],
    "74": [
        {
            "node_id": "18",
            "leak_diameter": 0.113903284778,
            "leak_type": "abrupt",
            "leak_start_time": 8013,
            "leak_end_time": 11537,
            "leak_peak_time": 8013
        },
        {
            "node_id": "30",
            "leak_diameter": 0.0521247889439,
            "leak_type": "incipient",
            "leak_start_time": 11085,
            "leak_end_time": 13936,
            "leak_peak_time": 11490
        }
    ],
    "76": [
        {
            "node_id": "8",
            "leak_diameter": 0.171790765221,
            "leak_type": "abrupt",
            "leak_start_time": 3242,
            "leak_end_time": 5041,
            "leak_peak_time": 3242
        }
    ],
    "78": [
        {
            "node_id": "22",
            "leak_diameter": 0.159840587701,
            "leak_type": "incipient",
            "leak_start_time": 8020,
            "leak_end_time": 11506,
            "leak_peak_time": 8480
        },
        {
            "node_id": "28",
            "leak_diameter": 0.0259392296597,
            "leak_type": "incipient",
            "leak_start_time": 13280,
            "leak_end_time": 15073,
            "leak_peak_time": 13449
        }
    ],
    "79": [
        {
            "node_id": "23",
            "leak_diameter": 0.169726697713,
            "leak_type": "incipient",
            "leak_start_time": 2910,
            "leak_end_time": 14354,
            "leak_peak_time": 3173
        }
    ],
    "80": [
        {
            "node_id": "31",
            "leak_diameter": 0.0210103012602,
            "leak_type": "incipient",
            "leak_start_time": 14899,
            "leak_end_time": 17268,
            "leak_peak_time": 16010
        }
    ],
    "82": [
        {
            "node_id": "26",
            "leak_diameter": 0.0411542885258,
            "leak_type": "incipient",
            "leak_start_time": 5830,
            "leak_end_time": 13743,
            "leak_peak_time": 8848
        }
    ],
    "84": [
        {
            "node_id": "10",
            "leak_diameter": 0.131234211277,
            "leak_type": "abrupt",
            "leak_start_time": 14788,
            "leak_end_time": 14967,
            "leak_peak_time": 14788
        }
    ],
    "85": [
        {
            "node_id": "23",
            "leak_diameter": 0.101879472089,
            "leak_type": "incipient",
            "leak_start_time": 12175,
            "leak_end_time": 14630,
            "leak_peak_time": 14092
        },
        {
            "node_id": "8",
            "leak_diameter": 0.0682487007179,
            "leak_type": "abrupt",
            "leak_start_time": 16832,
            "leak_end_time": 17320,
            "leak_peak_time": 16832
        }
    ],
    "86": [
        {
            "node_id": "32",
            "leak_diameter": 0.156934727184,
            "leak_type": "abrupt",
            "leak_start_time": 4252,
            "leak_end_time": 14599,
            "leak_peak_time": 4252
        }
    ],
    "87": [
        {
            "node_id": "21",
            "leak_diameter": 0.0595156599826,
            "leak_type": "abrupt",
            "leak_start_time": 11556,
            "leak_end_time": 15593,
            "leak_peak_time": 11556
        },
        {
            "node_id": "30",
            "leak_diameter": 0.0628222102794,
            "leak_type": "abrupt",
            "leak_start_time": 7888,
            "leak_end_time": 10837,
            "leak_peak_time": 7888
        }
    ],
    "88": [
        {
            "node_id": "27",
            "leak_diameter": 0.0555270626902,
            "leak_type": "incipient",
            "leak_start_time": 15519,
            "leak_end_time": 17123,
            "leak_peak_time": 15780
        }
    ],
    "89": [
        {
            "node_id": "23",
            "leak_diameter": 0.176175381634,
            "leak_type": "abrupt",
            "leak_start_time": 13769,
            "leak_end_time": 16006,
            "leak_peak_time": 13769
        }
    ],
    "90": [
        {
            "node_id": "19",
            "leak_diameter": 0.0951044230811,
            "leak_type": "incipient",
            "leak_start_time": 10649,
            "leak_end_time": 17497,
            "leak_peak_time": 14355
        }
    ],
    "91": [
        {
            "node_id": "2",
            "leak_diameter": 0.154382659995,
            "leak_type": "incipient",
            "leak_start_time": 13187,
            "leak_end_time": 14529,
            "leak_peak_time": 14464
        }
    ],
    "93": [
        {
            "node_id": "17",
            "leak_diameter": 0.0967543069722,
            "leak_type": "incipient",
            "leak_start_time": 11248,
            "leak_end_time": 12211,
            "leak_peak_time": 12139
        }
    ],
    "94": [
        {
            "node_id": "12",
            "leak_diameter": 0.079987724065,
            "leak_type": "incipient",
            "leak_start_time": 15694,
            "leak_end_time": 15764,
            "leak_peak_time": 15704
        }
    ],
    "95": [
        {
            "node_id": "14",
            "leak_diameter": 0.0732864786504,
            "leak_type": "incipient",
            "leak_start_time": 357,
            "leak_end_time": 6612,
            "leak_peak_time": 5124
        }
    ],
    "97": [
        {
            "node_id": "5",
            "leak_diameter": 0.0870686295818,
            "leak_type": "abrupt",
            "leak_start_time": 15207,
            "leak_end_time": 16487,
            "leak_peak_time": 15207
        }
    ],
    "98": [
        {
            "node_id": "26",
            "leak_diameter": 0.170619010124,
            "leak_type": "abrupt",
            "leak_start_time": 3645,
            "leak_end_time": 6282,
            "leak_peak_time": 3645
        }
    ],
    "99": [
        {
            "node_id": "3",
            "leak_diameter": 0.0840493679989,
            "leak_type": "abrupt",
            "leak_start_time": 4620,
            "leak_end_time": 7845,
            "leak_peak_time": 4620
        },
        {
            "node_id": "9",
            "leak_diameter": 0.0710190170279,
            "leak_type": "abrupt",
            "leak_start_time": 9180,
            "leak_end_time": 12101,
            "leak_peak_time": 9180
        }
    ],
    "101": [
        {
            "node_id": "11",
            "leak_diameter": 0.111750734601,
            "leak_type": "incipient",
            "leak_start_time": 2564,
            "leak_end_time": 3589,
            "leak_peak_time": 2575
        },
        {
            "node_id": "14",
            "leak_diameter": 0.17765836394,
            "leak_type": "abrupt",
            "leak_start_time": 7685,
            "leak_end_time": 9343,
            "leak_peak_time": 7685
        }
    ],
    "102": [
        {
            "node_id": "27",
            "leak_diameter": 0.152107040692,
            "leak_type": "abrupt",
            "leak_start_time": 3756,
            "leak_end_time": 4617,
            "leak_peak_time": 3756
        },
        {
            "node_id": "5",
            "leak_diameter": 0.183183305902,
            "leak_type": "abrupt",
            "leak_start_time": 11860,
            "leak_end_time": 13645,
            "leak_peak_time": 11860
        }
    ],
    "103": [
        {
            "node_id": "27",
            "leak_diameter": 0.0243771745902,
            "leak_type": "incipient",
            "leak_start_time": 15334,
            "leak_end_time": 16089,
            "leak_peak_time": 15698
        }
    ],
    "104": [
        {
            "node_id": "2",
            "leak_diameter": 0.0548675762213,
            "leak_type": "abrupt",
            "leak_start_time": 5120,
            "leak_end_time": 12425,
            "leak_peak_time": 5120
        }
    ],
    "105": [
        {
            "node_id": "27",
            "leak_diameter": 0.042517236165,
            "leak_type": "incipient",
            "leak_start_time": 6269,
            "leak_end_time": 16852,
            "leak_peak_time": 12541
        }
    ],
    "106": [
        {
            "node_id": "2",
            "leak_diameter": 0.043710047449,
            "leak_type": "incipient",
            "leak_start_time": 8483,
            "leak_end_time": 15530,
            "leak_peak_time": 13119
        }
    ],
    "108": [
        {
            "node_id": "16",
            "leak_diameter": 0.168212596592,
            "leak_type": "incipient",
            "leak_start_time": 12176,
            "leak_end_time": 17112,
            "leak_peak_time": 12791
        },
        {
            "node_id": "18",
            "leak_diameter": 0.141069585446,
            "leak_type": "abrupt",
            "leak_start_time": 12754,
            "leak_end_time": 15253,
            "leak_peak_time": 12754
        }
    ],
    "109": [
        {
            "node_id": "27",
            "leak_diameter": 0.10277168151,
            "leak_type": "abrupt",
            "leak_start_time": 3549,
            "leak_end_time": 17126,
            "leak_peak_time": 3549
        },
        {
            "node_id": "11",
            "leak_diameter": 0.0793829251901,
            "leak_type": "incipient",
            "leak_start_time": 16938,
            "leak_end_time": 17454,
            "leak_peak_time": 17193
        }
    ],
    "110": [
        {
            "node_id": "7",
            "leak_diameter": 0.0895378918752,
            "leak_type": "incipient",
            "leak_start_time": 16240,
            "leak_end_time": 16666,
            "leak_peak_time": 16638
        }
    ],
    "111": [
        {
            "node_id": "4",
            "leak_diameter": 0.11367184142,
            "leak_type": "abrupt",
            "leak_start_time": 7170,
            "leak_end_time": 10982,
            "leak_peak_time": 7170
        }
    ],
    "113": [
        {
            "node_id": "12",
            "leak_diameter": 0.0341765172714,
            "leak_type": "abrupt",
            "leak_start_time": 3874,
            "leak_end_time": 10202,
            "leak_peak_time": 3874
        },
        {
            "node_id": "2",
            "leak_diameter": 0.179372259828,
            "leak_type": "incipient",
            "leak_start_time": 6372,
            "leak_end_time": 16608,
            "leak_peak_time": 10070
        }
    ],
    "114": [
        {
            "node_id": "28",
            "leak_diameter": 0.177054781172,
            "leak_type": "incipient",
            "leak_start_time": 17025,
            "leak_end_time": 17190,
            "leak_peak_time": 17140
        }
    ],
    "115": [
        {
            "node_id": "7",
            "leak_diameter": 0.141485416748,
            "leak_type": "incipient",
            "leak_start_time": 5957,
            "leak_end_time": 14155,
            "leak_peak_time": 12024
        }
    ],
    "116": [
        {
            "node_id": "10",
            "leak_diameter": 0.173558885014,
            "leak_type": "incipient",
            "leak_start_time": 3856,
            "leak_end_time": 9054,
            "leak_peak_time": 6289
        }
    ],
    "117": [
        {
            "node_id": "3",
            "leak_diameter": 0.187029338891,
            "leak_type": "incipient",
            "leak_start_time": 10804,
            "leak_end_time": 11310,
            "leak_peak_time": 11142
        }
    ],
    "118": [
        {
            "node_id": "18",
            "leak_diameter": 0.194616056024,
            "leak_type": "incipient",
            "leak_start_time": 5105,
            "leak_end_time": 6431,
            "leak_peak_time": 6276
        }
    ],
    "119": [
        {
            "node_id": "21",
            "leak_diameter": 0.176810868901,
            "leak_type": "abrupt",
            "leak_start_time": 17037,
            "leak_end_time": 17204,
            "leak_peak_time": 17037
        }
    ],
    "121": [
        {
            "node_id": "14",
            "leak_diameter": 0.116940442394,
            "leak_type": "abrupt",
            "leak_start_time": 8023,
            "leak_end_time": 17050,
            "leak_peak_time": 8023
        }
    ],
    "123": [
        {
            "node_id": "25",
            "leak_diameter": 0.0439730070216,
            "leak_type": "incipient",
            "leak_start_time": 16000,
            "leak_end_time": 16045,
            "leak_peak_time": 16001
        }
    ],
    "124": [
        {
            "node_id": "3",
            "leak_diameter": 0.0802858500733,
            "leak_type": "incipient",
            "leak_start_time": 12490,
            "leak_end_time": 16593,
            "leak_peak_time": 16394
        },
        {
            "node_id": "30",
            "leak_diameter": 0.0536962077585,
            "leak_type": "incipient",
            "leak_start_time": 9917,
            "leak_end_time": 12856,
            "leak_peak_time": 10671
        }
    ],
    "125": [
        {
            "node_id": "10",
            "leak_diameter": 0.170503447213,
            "leak_type": "incipient",
            "leak_start_time": 2305,
            "leak_end_time": 12867,
            "leak_peak_time": 12352
        }
    ],
    "126": [
        {
            "node_id": "30",
            "leak_diameter": 0.0651385426522,
            "leak_type": "incipient",
            "leak_start_time": 827,
            "leak_end_time": 11812,
            "leak_peak_time": 6642
        }
    ],
    "127": [
        {
            "node_id": "29",
            "leak_diameter": 0.0564689910434,
            "leak_type": "abrupt",
            "leak_start_time": 6326,
            "leak_end_time": 9864,
            "leak_peak_time": 6326
        }
    ],
    "128": [
        {
            "node_id": "13",
            "leak_diameter": 0.192694454266,
            "leak_type": "abrupt",
            "leak_start_time": 16503,
            "leak_end_time": 17322,
            "leak_peak_time": 16503
        }
    ],
    "130": [
        {
            "node_id": "27",
            "leak_diameter": 0.0559211867578,
            "leak_type": "abrupt",
            "leak_start_time": 494,
            "leak_end_time": 13685,
            "leak_peak_time": 494
        }
    ],
    "132": [
        {
            "node_id": "21",
            "leak_diameter": 0.181596324794,
            "leak_type": "abrupt",
            "leak_start_time": 4021,
            "leak_end_time": 12918,
            "leak_peak_time": 4021
        }
    ],
    "133": [
        {
            "node_id": "17",
            "leak_diameter": 0.143349944635,
            "leak_type": "abrupt",
            "leak_start_time": 666,
            "leak_end_time": 8146,
            "leak_peak_time": 666
        },
        {
            "node_id": "26",
            "leak_diameter": 0.169594027654,
            "leak_type": "incipient",
            "leak_start_time": 11909,
            "leak_end_time": 16431,
            "leak_peak_time": 16366
        }
    ],
    "134": [
        {
            "node_id": "22",
            "leak_diameter": 0.0748309903831,
            "leak_type": "incipient",
            "leak_start_time": 13653,
            "leak_end_time": 16978,
            "leak_peak_time": 13831
        }
    ],
    "135": [
        {
            "node_id": "28",
            "leak_diameter": 0.0968035521214,
            "leak_type": "abrupt",
            "leak_start_time": 17120,
            "leak_end_time": 17157,
            "leak_peak_time": 17120
        }
    ],
    "138": [
        {
            "node_id": "3",
            "leak_diameter": 0.0312656479528,
            "leak_type": "incipient",
            "leak_start_time": 764,
            "leak_end_time": 8976,
            "leak_peak_time": 1406
        },
        {
            "node_id": "19",
            "leak_diameter": 0.114151294642,
            "leak_type": "abrupt",
            "leak_start_time": 315,
            "leak_end_time": 16067,
            "leak_peak_time": 315
        }
    ],
    "139": [
        {
            "node_id": "22",
            "leak_diameter": 0.0466607017822,
            "leak_type": "incipient",
            "leak_start_time": 5295,
            "leak_end_time": 17132,
            "leak_peak_time": 12033
        }
    ],
    "140": [
        {
            "node_id": "22",
            "leak_diameter": 0.0768332613626,
            "leak_type": "incipient",
            "leak_start_time": 16733,
            "leak_end_time": 16944,
            "leak_peak_time": 16898
        }
    ],
    "141": [
        {
            "node_id": "26",
            "leak_diameter": 0.0959011857301,
            "leak_type": "incipient",
            "leak_start_time": 15673,
            "leak_end_time": 16410,
            "leak_peak_time": 16279
        },
        {
            "node_id": "7",
            "leak_diameter": 0.0330457558128,
            "leak_type": "incipient",
            "leak_start_time": 6332,
            "leak_end_time": 6637,
            "leak_peak_time": 6425
        }
    ],
    "143": [
        {
            "node_id": "18",
            "leak_diameter": 0.139882321575,
            "leak_type": "abrupt",
            "leak_start_time": 5060,
            "leak_end_time": 16142,
            "leak_peak_time": 5060
        }
    ],
    "144": [
        {
            "node_id": "6",
            "leak_diameter": 0.141996408925,
            "leak_type": "abrupt",
            "leak_start_time": 9974,
            "leak_end_time": 15627,
            "leak_peak_time": 9974
        }
    ],
    "145": [
        {
            "node_id": "7",
            "leak_diameter": 0.138151955618,
            "leak_type": "incipient",
            "leak_start_time": 19,
            "leak_end_time": 16013,
            "leak_peak_time": 5028
        }
    ],
    "147": [
        {
            "node_id": "29",
            "leak_diameter": 0.176765943356,
            "leak_type": "incipient",
            "leak_start_time": 1696,
            "leak_end_time": 12450,
            "leak_peak_time": 8715
        }
    ],
    "148": [
        {
            "node_id": "11",
            "leak_diameter": 0.140835606417,
            "leak_type": "incipient",
            "leak_start_time": 12326,
            "leak_end_time": 16434,
            "leak_peak_time": 14949
        },
        {
            "node_id": "20",
            "leak_diameter": 0.142432499371,
            "leak_type": "incipient",
            "leak_start_time": 7731,
            "leak_end_time": 8444,
            "leak_peak_time": 8175
        }
    ],
    "150": [
        {
            "node_id": "18",
            "leak_diameter": 0.128793202399,
            "leak_type": "incipient",
            "leak_start_time": 16088,
            "leak_end_time": 16651,
            "leak_peak_time": 16490
        }
    ],
    "151": [
        {
            "node_id": "4",
            "leak_diameter": 0.170143392956,
            "leak_type": "incipient",
            "leak_start_time": 1104,
            "leak_end_time": 1681,
            "leak_peak_time": 1315
        }
    ],
    "152": [
        {
            "node_id": "7",
            "leak_diameter": 0.10381758876,
            "leak_type": "abrupt",
            "leak_start_time": 15396,
            "leak_end_time": 17208,
            "leak_peak_time": 15396
        }
    ],
    "153": [
        {
            "node_id": "29",
            "leak_diameter": 0.18915527736,
            "leak_type": "incipient",
            "leak_start_time": 9440,
            "leak_end_time": 16239,
            "leak_peak_time": 10969
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0381829212018,
            "leak_type": "abrupt",
            "leak_start_time": 14588,
            "leak_end_time": 16345,
            "leak_peak_time": 14588
        }
    ],
    "154": [
        {
            "node_id": "3",
            "leak_diameter": 0.195034719747,
            "leak_type": "abrupt",
            "leak_start_time": 17346,
            "leak_end_time": 17503,
            "leak_peak_time": 17346
        },
        {
            "node_id": "13",
            "leak_diameter": 0.158996396505,
            "leak_type": "incipient",
            "leak_start_time": 15526,
            "leak_end_time": 15762,
            "leak_peak_time": 15535
        }
    ],
    "156": [
        {
            "node_id": "22",
            "leak_diameter": 0.044664705094,
            "leak_type": "abrupt",
            "leak_start_time": 14163,
            "leak_end_time": 15755,
            "leak_peak_time": 14163
        },
        {
            "node_id": "29",
            "leak_diameter": 0.0329996886385,
            "leak_type": "incipient",
            "leak_start_time": 11040,
            "leak_end_time": 13030,
            "leak_peak_time": 12498
        }
    ],
    "158": [
        {
            "node_id": "14",
            "leak_diameter": 0.0748944677364,
            "leak_type": "incipient",
            "leak_start_time": 7075,
            "leak_end_time": 8870,
            "leak_peak_time": 8142
        }
    ],
    "159": [
        {
            "node_id": "11",
            "leak_diameter": 0.176283739465,
            "leak_type": "abrupt",
            "leak_start_time": 12491,
            "leak_end_time": 15268,
            "leak_peak_time": 12491
        },
        {
            "node_id": "18",
            "leak_diameter": 0.0887668754748,
            "leak_type": "abrupt",
            "leak_start_time": 16419,
            "leak_end_time": 16594,
            "leak_peak_time": 16419
        }
    ],
    "162": [
        {
            "node_id": "25",
            "leak_diameter": 0.0605200738335,
            "leak_type": "abrupt",
            "leak_start_time": 15793,
            "leak_end_time": 16682,
            "leak_peak_time": 15793
        }
    ],
    "165": [
        {
            "node_id": "23",
            "leak_diameter": 0.0673959346015,
            "leak_type": "abrupt",
            "leak_start_time": 11044,
            "leak_end_time": 16114,
            "leak_peak_time": 11044
        }
    ],
    "167": [
        {
            "node_id": "19",
            "leak_diameter": 0.196948034459,
            "leak_type": "abrupt",
            "leak_start_time": 4453,
            "leak_end_time": 5448,
            "leak_peak_time": 4453
        }
    ],
    "169": [
        {
            "node_id": "15",
            "leak_diameter": 0.14595624642,
            "leak_type": "incipient",
            "leak_start_time": 15656,
            "leak_end_time": 16543,
            "leak_peak_time": 16390
        }
    ],
    "170": [
        {
            "node_id": "4",
            "leak_diameter": 0.161348430607,
            "leak_type": "abrupt",
            "leak_start_time": 13048,
            "leak_end_time": 13723,
            "leak_peak_time": 13048
        }
    ],
    "172": [
        {
            "node_id": "3",
            "leak_diameter": 0.0892909056358,
            "leak_type": "incipient",
            "leak_start_time": 8858,
            "leak_end_time": 11939,
            "leak_peak_time": 11218
        },
        {
            "node_id": "26",
            "leak_diameter": 0.0807635653254,
            "leak_type": "abrupt",
            "leak_start_time": 16471,
            "leak_end_time": 17096,
            "leak_peak_time": 16471
        }
    ],
    "174": [
        {
            "node_id": "19",
            "leak_diameter": 0.118963800416,
            "leak_type": "abrupt",
            "leak_start_time": 10566,
            "leak_end_time": 15016,
            "leak_peak_time": 10566
        },
        {
            "node_id": "26",
            "leak_diameter": 0.0793835566746,
            "leak_type": "abrupt",
            "leak_start_time": 8631,
            "leak_end_time": 9506,
            "leak_peak_time": 8631
        }
    ],
    "175": [
        {
            "node_id": "20",
            "leak_diameter": 0.0791956561229,
            "leak_type": "abrupt",
            "leak_start_time": 8608,
            "leak_end_time": 11929,
            "leak_peak_time": 8608
        }
    ],
    "176": [
        {
            "node_id": "17",
            "leak_diameter": 0.0702532766186,
            "leak_type": "abrupt",
            "leak_start_time": 11440,
            "leak_end_time": 13950,
            "leak_peak_time": 11440
        }
    ],
    "177": [
        {
            "node_id": "19",
            "leak_diameter": 0.0477870693732,
            "leak_type": "incipient",
            "leak_start_time": 11429,
            "leak_end_time": 12070,
            "leak_peak_time": 11446
        }
    ],
    "178": [
        {
            "node_id": "19",
            "leak_diameter": 0.0993094268679,
            "leak_type": "abrupt",
            "leak_start_time": 10346,
            "leak_end_time": 12712,
            "leak_peak_time": 10346
        }
    ],
    "179": [
        {
            "node_id": "12",
            "leak_diameter": 0.0291618759177,
            "leak_type": "abrupt",
            "leak_start_time": 2974,
            "leak_end_time": 4251,
            "leak_peak_time": 2974
        }
    ],
    "182": [
        {
            "node_id": "29",
            "leak_diameter": 0.0718976519445,
            "leak_type": "incipient",
            "leak_start_time": 13950,
            "leak_end_time": 15235,
            "leak_peak_time": 14826
        }
    ],
    "183": [
        {
            "node_id": "10",
            "leak_diameter": 0.0886896651433,
            "leak_type": "abrupt",
            "leak_start_time": 6087,
            "leak_end_time": 16681,
            "leak_peak_time": 6087
        },
        {
            "node_id": "29",
            "leak_diameter": 0.0529979684151,
            "leak_type": "abrupt",
            "leak_start_time": 13509,
            "leak_end_time": 15952,
            "leak_peak_time": 13509
        }
    ],
    "184": [
        {
            "node_id": "29",
            "leak_diameter": 0.125901859747,
            "leak_type": "incipient",
            "leak_start_time": 9437,
            "leak_end_time": 13398,
            "leak_peak_time": 10772
        },
        {
            "node_id": "31",
            "leak_diameter": 0.183504631569,
            "leak_type": "incipient",
            "leak_start_time": 8007,
            "leak_end_time": 9705,
            "leak_peak_time": 9216
        }
    ],
    "185": [
        {
            "node_id": "6",
            "leak_diameter": 0.175839835253,
            "leak_type": "incipient",
            "leak_start_time": 15050,
            "leak_end_time": 15595,
            "leak_peak_time": 15120
        },
        {
            "node_id": "15",
            "leak_diameter": 0.159620291783,
            "leak_type": "abrupt",
            "leak_start_time": 568,
            "leak_end_time": 14723,
            "leak_peak_time": 568
        }
    ],
    "186": [
        {
            "node_id": "6",
            "leak_diameter": 0.0543031191822,
            "leak_type": "abrupt",
            "leak_start_time": 9539,
            "leak_end_time": 12239,
            "leak_peak_time": 9539
        }
    ],
    "187": [
        {
            "node_id": "21",
            "leak_diameter": 0.15267266179,
            "leak_type": "abrupt",
            "leak_start_time": 6953,
            "leak_end_time": 11316,
            "leak_peak_time": 6953
        }
    ],
    "188": [
        {
            "node_id": "10",
            "leak_diameter": 0.0969041834042,
            "leak_type": "abrupt",
            "leak_start_time": 6210,
            "leak_end_time": 17464,
            "leak_peak_time": 6210
        },
        {
            "node_id": "8",
            "leak_diameter": 0.0259907654166,
            "leak_type": "incipient",
            "leak_start_time": 4783,
            "leak_end_time": 6722,
            "leak_peak_time": 5579
        }
    ],
    "189": [
        {
            "node_id": "9",
            "leak_diameter": 0.128001065264,
            "leak_type": "abrupt",
            "leak_start_time": 13295,
            "leak_end_time": 16677,
            "leak_peak_time": 13295
        }
    ],
    "190": [
        {
            "node_id": "25",
            "leak_diameter": 0.14739601147,
            "leak_type": "incipient",
            "leak_start_time": 16465,
            "leak_end_time": 16883,
            "leak_peak_time": 16815
        },
        {
            "node_id": "15",
            "leak_diameter": 0.034195396215,
            "leak_type": "incipient",
            "leak_start_time": 6420,
            "leak_end_time": 10830,
            "leak_peak_time": 9788
        }
    ],
    "191": [
        {
            "node_id": "16",
            "leak_diameter": 0.0624843358858,
            "leak_type": "abrupt",
            "leak_start_time": 10067,
            "leak_end_time": 12751,
            "leak_peak_time": 10067
        },
        {
            "node_id": "31",
            "leak_diameter": 0.136255503727,
            "leak_type": "incipient",
            "leak_start_time": 16638,
            "leak_end_time": 16706,
            "leak_peak_time": 16645
        }
    ],
    "192": [
        {
            "node_id": "12",
            "leak_diameter": 0.124925143523,
            "leak_type": "abrupt",
            "leak_start_time": 14371,
            "leak_end_time": 17274,
            "leak_peak_time": 14371
        }
    ],
    "193": [
        {
            "node_id": "10",
            "leak_diameter": 0.0957577253762,
            "leak_type": "abrupt",
            "leak_start_time": 11936,
            "leak_end_time": 17060,
            "leak_peak_time": 11936
        }
    ],
    "194": [
        {
            "node_id": "7",
            "leak_diameter": 0.123155564339,
            "leak_type": "abrupt",
            "leak_start_time": 824,
            "leak_end_time": 3931,
            "leak_peak_time": 824
        }
    ],
    "196": [
        {
            "node_id": "29",
            "leak_diameter": 0.102009338065,
            "leak_type": "incipient",
            "leak_start_time": 15749,
            "leak_end_time": 17292,
            "leak_peak_time": 15786
        }
    ],
    "198": [
        {
            "node_id": "14",
            "leak_diameter": 0.115658671242,
            "leak_type": "abrupt",
            "leak_start_time": 14773,
            "leak_end_time": 15544,
            "leak_peak_time": 14773
        }
    ],
    "199": [
        {
            "node_id": "9",
            "leak_diameter": 0.13285442029,
            "leak_type": "abrupt",
            "leak_start_time": 1239,
            "leak_end_time": 5608,
            "leak_peak_time": 1239
        }
    ],
    "200": [
        {
            "node_id": "20",
            "leak_diameter": 0.13593955187,
            "leak_type": "abrupt",
            "leak_start_time": 5199,
            "leak_end_time": 6164,
            "leak_peak_time": 5199
        }
    ],
    "202": [
        {
            "node_id": "11",
            "leak_diameter": 0.116800958953,
            "leak_type": "abrupt",
            "leak_start_time": 5465,
            "leak_end_time": 15932,
            "leak_peak_time": 5465
        },
        {
            "node_id": "7",
            "leak_diameter": 0.0375335449678,
            "leak_type": "abrupt",
            "leak_start_time": 13560,
            "leak_end_time": 16759,
            "leak_peak_time": 13560
        }
    ],
    "203": [
        {
            "node_id": "17",
            "leak_diameter": 0.101197630178,
            "leak_type": "incipient",
            "leak_start_time": 11714,
            "leak_end_time": 17292,
            "leak_peak_time": 11804
        }
    ],
    "204": [
        {
            "node_id": "26",
            "leak_diameter": 0.050003103398,
            "leak_type": "incipient",
            "leak_start_time": 16573,
            "leak_end_time": 16643,
            "leak_peak_time": 16599
        }
    ],
    "206": [
        {
            "node_id": "3",
            "leak_diameter": 0.0837434652106,
            "leak_type": "incipient",
            "leak_start_time": 16061,
            "leak_end_time": 16984,
            "leak_peak_time": 16606
        }
    ],
    "207": [
        {
            "node_id": "28",
            "leak_diameter": 0.112994190181,
            "leak_type": "incipient",
            "leak_start_time": 13923,
            "leak_end_time": 14010,
            "leak_peak_time": 14009
        }
    ],
    "208": [
        {
            "node_id": "18",
            "leak_diameter": 0.138146495021,
            "leak_type": "incipient",
            "leak_start_time": 11264,
            "leak_end_time": 15382,
            "leak_peak_time": 13890
        }
    ],
    "209": [
        {
            "node_id": "29",
            "leak_diameter": 0.154102780073,
            "leak_type": "incipient",
            "leak_start_time": 3032,
            "leak_end_time": 3220,
            "leak_peak_time": 3096
        }
    ],
    "211": [
        {
            "node_id": "23",
            "leak_diameter": 0.0773293759575,
            "leak_type": "abrupt",
            "leak_start_time": 11089,
            "leak_end_time": 12906,
            "leak_peak_time": 11089
        }
    ],
    "212": [
        {
            "node_id": "25",
            "leak_diameter": 0.0902220800323,
            "leak_type": "incipient",
            "leak_start_time": 14754,
            "leak_end_time": 15731,
            "leak_peak_time": 15576
        }
    ],
    "213": [
        {
            "node_id": "14",
            "leak_diameter": 0.107249961773,
            "leak_type": "incipient",
            "leak_start_time": 5482,
            "leak_end_time": 6915,
            "leak_peak_time": 5767
        }
    ],
    "214": [
        {
            "node_id": "10",
            "leak_diameter": 0.0719116695878,
            "leak_type": "incipient",
            "leak_start_time": 14643,
            "leak_end_time": 16197,
            "leak_peak_time": 14986
        }
    ],
    "215": [
        {
            "node_id": "25",
            "leak_diameter": 0.042206108744,
            "leak_type": "abrupt",
            "leak_start_time": 454,
            "leak_end_time": 9390,
            "leak_peak_time": 454
        },
        {
            "node_id": "28",
            "leak_diameter": 0.0302127084334,
            "leak_type": "incipient",
            "leak_start_time": 5104,
            "leak_end_time": 17041,
            "leak_peak_time": 15697
        }
    ],
    "216": [
        {
            "node_id": "26",
            "leak_diameter": 0.151264938092,
            "leak_type": "incipient",
            "leak_start_time": 13677,
            "leak_end_time": 16160,
            "leak_peak_time": 14704
        }
    ],
    "217": [
        {
            "node_id": "13",
            "leak_diameter": 0.156085386397,
            "leak_type": "abrupt",
            "leak_start_time": 13995,
            "leak_end_time": 16530,
            "leak_peak_time": 13995
        }
    ],
    "218": [
        {
            "node_id": "19",
            "leak_diameter": 0.0630225028044,
            "leak_type": "incipient",
            "leak_start_time": 15901,
            "leak_end_time": 16125,
            "leak_peak_time": 16061
        }
    ],
    "220": [
        {
            "node_id": "14",
            "leak_diameter": 0.103261606038,
            "leak_type": "abrupt",
            "leak_start_time": 9111,
            "leak_end_time": 13908,
            "leak_peak_time": 9111
        }
    ],
    "222": [
        {
            "node_id": "4",
            "leak_diameter": 0.0904163136952,
            "leak_type": "abrupt",
            "leak_start_time": 11730,
            "leak_end_time": 13018,
            "leak_peak_time": 11730
        },
        {
            "node_id": "22",
            "leak_diameter": 0.193413087398,
            "leak_type": "incipient",
            "leak_start_time": 9122,
            "leak_end_time": 13965,
            "leak_peak_time": 9199
        }
    ],
    "223": [
        {
            "node_id": "26",
            "leak_diameter": 0.103086658204,
            "leak_type": "incipient",
            "leak_start_time": 12428,
            "leak_end_time": 12929,
            "leak_peak_time": 12896
        }
    ],
    "224": [
        {
            "node_id": "7",
            "leak_diameter": 0.0585759793723,
            "leak_type": "incipient",
            "leak_start_time": 15247,
            "leak_end_time": 16137,
            "leak_peak_time": 15994
        }
    ],
    "225": [
        {
            "node_id": "12",
            "leak_diameter": 0.0263074771,
            "leak_type": "abrupt",
            "leak_start_time": 1190,
            "leak_end_time": 10206,
            "leak_peak_time": 1190
        },
        {
            "node_id": "17",
            "leak_diameter": 0.0357341693231,
            "leak_type": "abrupt",
            "leak_start_time": 14348,
            "leak_end_time": 16483,
            "leak_peak_time": 14348
        }
    ],
    "226": [
        {
            "node_id": "22",
            "leak_diameter": 0.163756679198,
            "leak_type": "abrupt",
            "leak_start_time": 2291,
            "leak_end_time": 6973,
            "leak_peak_time": 2291
        },
        {
            "node_id": "19",
            "leak_diameter": 0.0210034327331,
            "leak_type": "abrupt",
            "leak_start_time": 9515,
            "leak_end_time": 9767,
            "leak_peak_time": 9515
        }
    ],
    "227": [
        {
            "node_id": "23",
            "leak_diameter": 0.179817456866,
            "leak_type": "incipient",
            "leak_start_time": 11248,
            "leak_end_time": 14047,
            "leak_peak_time": 11734
        },
        {
            "node_id": "28",
            "leak_diameter": 0.104035782549,
            "leak_type": "incipient",
            "leak_start_time": 2379,
            "leak_end_time": 5149,
            "leak_peak_time": 2756
        }
    ],
    "228": [
        {
            "node_id": "22",
            "leak_diameter": 0.126540126678,
            "leak_type": "abrupt",
            "leak_start_time": 1595,
            "leak_end_time": 12604,
            "leak_peak_time": 1595
        }
    ],
    "229": [
        {
            "node_id": "23",
            "leak_diameter": 0.129994250054,
            "leak_type": "incipient",
            "leak_start_time": 9613,
            "leak_end_time": 9811,
            "leak_peak_time": 9734
        }
    ],
    "230": [
        {
            "node_id": "23",
            "leak_diameter": 0.0618039074987,
            "leak_type": "abrupt",
            "leak_start_time": 6462,
            "leak_end_time": 8791,
            "leak_peak_time": 6462
        }
    ],
    "232": [
        {
            "node_id": "15",
            "leak_diameter": 0.0894143892861,
            "leak_type": "abrupt",
            "leak_start_time": 15017,
            "leak_end_time": 15161,
            "leak_peak_time": 15017
        }
    ],
    "233": [
        {
            "node_id": "11",
            "leak_diameter": 0.160869757088,
            "leak_type": "abrupt",
            "leak_start_time": 7006,
            "leak_end_time": 15864,
            "leak_peak_time": 7006
        },
        {
            "node_id": "31",
            "leak_diameter": 0.117488829439,
            "leak_type": "incipient",
            "leak_start_time": 1458,
            "leak_end_time": 8534,
            "leak_peak_time": 3702
        }
    ],
    "234": [
        {
            "node_id": "27",
            "leak_diameter": 0.0614802719256,
            "leak_type": "abrupt",
            "leak_start_time": 12279,
            "leak_end_time": 14317,
            "leak_peak_time": 12279
        },
        {
            "node_id": "29",
            "leak_diameter": 0.05676870339,
            "leak_type": "incipient",
            "leak_start_time": 9795,
            "leak_end_time": 16105,
            "leak_peak_time": 12788
        }
    ],
    "235": [
        {
            "node_id": "12",
            "leak_diameter": 0.0751513661619,
            "leak_type": "incipient",
            "leak_start_time": 9925,
            "leak_end_time": 14604,
            "leak_peak_time": 11171
        }
    ],
    "236": [
        {
            "node_id": "19",
            "leak_diameter": 0.12496745294,
            "leak_type": "abrupt",
            "leak_start_time": 12481,
            "leak_end_time": 13950,
            "leak_peak_time": 12481
        }
    ],
    "241": [
        {
            "node_id": "26",
            "leak_diameter": 0.160089372753,
            "leak_type": "abrupt",
            "leak_start_time": 7073,
            "leak_end_time": 13998,
            "leak_peak_time": 7073
        }
    ],
    "242": [
        {
            "node_id": "18",
            "leak_diameter": 0.11327139369,
            "leak_type": "abrupt",
            "leak_start_time": 1825,
            "leak_end_time": 10533,
            "leak_peak_time": 1825
        }
    ],
    "243": [
        {
            "node_id": "29",
            "leak_diameter": 0.166784112157,
            "leak_type": "incipient",
            "leak_start_time": 15413,
            "leak_end_time": 16022,
            "leak_peak_time": 15695
        }
    ],
    "244": [
        {
            "node_id": "20",
            "leak_diameter": 0.0667845345324,
            "leak_type": "abrupt",
            "leak_start_time": 14582,
            "leak_end_time": 14721,
            "leak_peak_time": 14582
        }
    ],
    "245": [
        {
            "node_id": "18",
            "leak_diameter": 0.0694720341858,
            "leak_type": "incipient",
            "leak_start_time": 16152,
            "leak_end_time": 17338,
            "leak_peak_time": 17209
        },
        {
            "node_id": "21",
            "leak_diameter": 0.0421955255058,
            "leak_type": "incipient",
            "leak_start_time": 8684,
            "leak_end_time": 13112,
            "leak_peak_time": 9206
        }
    ],
    "246": [
        {
            "node_id": "26",
            "leak_diameter": 0.0565881446104,
            "leak_type": "abrupt",
            "leak_start_time": 16244,
            "leak_end_time": 16529,
            "leak_peak_time": 16244
        }
    ],
    "247": [
        {
            "node_id": "12",
            "leak_diameter": 0.0677397998996,
            "leak_type": "abrupt",
            "leak_start_time": 10302,
            "leak_end_time": 13181,
            "leak_peak_time": 10302
        }
    ],
    "248": [
        {
            "node_id": "16",
            "leak_diameter": 0.0696294927203,
            "leak_type": "incipient",
            "leak_start_time": 1104,
            "leak_end_time": 12055,
            "leak_peak_time": 5064
        }
    ],
    "250": [
        {
            "node_id": "6",
            "leak_diameter": 0.180686925582,
            "leak_type": "abrupt",
            "leak_start_time": 14902,
            "leak_end_time": 16533,
            "leak_peak_time": 14902
        },
        {
            "node_id": "15",
            "leak_diameter": 0.130758642299,
            "leak_type": "abrupt",
            "leak_start_time": 6018,
            "leak_end_time": 16627,
            "leak_peak_time": 6018
        }
    ],
    "252": [
        {
            "node_id": "14",
            "leak_diameter": 0.116981674944,
            "leak_type": "incipient",
            "leak_start_time": 7033,
            "leak_end_time": 9883,
            "leak_peak_time": 8933
        },
        {
            "node_id": "32",
            "leak_diameter": 0.170525780179,
            "leak_type": "abrupt",
            "leak_start_time": 4967,
            "leak_end_time": 16910,
            "leak_peak_time": 4967
        }
    ],
    "253": [
        {
            "node_id": "22",
            "leak_diameter": 0.0502759141357,
            "leak_type": "incipient",
            "leak_start_time": 16117,
            "leak_end_time": 16630,
            "leak_peak_time": 16318
        }
    ],
    "254": [
        {
            "node_id": "20",
            "leak_diameter": 0.148005662305,
            "leak_type": "abrupt",
            "leak_start_time": 8421,
            "leak_end_time": 15557,
            "leak_peak_time": 8421
        },
        {
            "node_id": "5",
            "leak_diameter": 0.100084750058,
            "leak_type": "abrupt",
            "leak_start_time": 4064,
            "leak_end_time": 16836,
            "leak_peak_time": 4064
        }
    ],
    "255": [
        {
            "node_id": "6",
            "leak_diameter": 0.0855749498596,
            "leak_type": "incipient",
            "leak_start_time": 13850,
            "leak_end_time": 16168,
            "leak_peak_time": 16104
        },
        {
            "node_id": "29",
            "leak_diameter": 0.107611359624,
            "leak_type": "abrupt",
            "leak_start_time": 3201,
            "leak_end_time": 12511,
            "leak_peak_time": 3201
        }
    ],
    "256": [
        {
            "node_id": "30",
            "leak_diameter": 0.0770086231232,
            "leak_type": "incipient",
            "leak_start_time": 1223,
            "leak_end_time": 4613,
            "leak_peak_time": 2639
        }
    ],
    "257": [
        {
            "node_id": "30",
            "leak_diameter": 0.167031101543,
            "leak_type": "incipient",
            "leak_start_time": 15953,
            "leak_end_time": 17515,
            "leak_peak_time": 17481
        }
    ],
    "258": [
        {
            "node_id": "13",
            "leak_diameter": 0.164131587794,
            "leak_type": "incipient",
            "leak_start_time": 11135,
            "leak_end_time": 15046,
            "leak_peak_time": 12840
        }
    ],
    "259": [
        {
            "node_id": "27",
            "leak_diameter": 0.0668545207025,
            "leak_type": "abrupt",
            "leak_start_time": 12524,
            "leak_end_time": 12685,
            "leak_peak_time": 12524
        }
    ],
    "260": [
        {
            "node_id": "19",
            "leak_diameter": 0.146851348172,
            "leak_type": "abrupt",
            "leak_start_time": 12867,
            "leak_end_time": 14913,
            "leak_peak_time": 12867
        }
    ],
    "261": [
        {
            "node_id": "6",
            "leak_diameter": 0.189480122014,
            "leak_type": "incipient",
            "leak_start_time": 1584,
            "leak_end_time": 8807,
            "leak_peak_time": 2897
        },
        {
            "node_id": "13",
            "leak_diameter": 0.0666060754412,
            "leak_type": "abrupt",
            "leak_start_time": 7607,
            "leak_end_time": 16931,
            "leak_peak_time": 7607
        }
    ],
    "262": [
        {
            "node_id": "29",
            "leak_diameter": 0.0629852199681,
            "leak_type": "incipient",
            "leak_start_time": 7702,
            "leak_end_time": 13586,
            "leak_peak_time": 9976
        }
    ],
    "263": [
        {
            "node_id": "16",
            "leak_diameter": 0.0831063946886,
            "leak_type": "incipient",
            "leak_start_time": 7093,
            "leak_end_time": 16686,
            "leak_peak_time": 10758
        },
        {
            "node_id": "14",
            "leak_diameter": 0.144875068253,
            "leak_type": "incipient",
            "leak_start_time": 4544,
            "leak_end_time": 7990,
            "leak_peak_time": 7537
        }
    ],
    "264": [
        {
            "node_id": "2",
            "leak_diameter": 0.0972780471012,
            "leak_type": "abrupt",
            "leak_start_time": 12685,
            "leak_end_time": 15607,
            "leak_peak_time": 12685
        },
        {
            "node_id": "26",
            "leak_diameter": 0.0486809302858,
            "leak_type": "abrupt",
            "leak_start_time": 12421,
            "leak_end_time": 15360,
            "leak_peak_time": 12421
        }
    ],
    "265": [
        {
            "node_id": "26",
            "leak_diameter": 0.179216009045,
            "leak_type": "abrupt",
            "leak_start_time": 4937,
            "leak_end_time": 7296,
            "leak_peak_time": 4937
        }
    ],
    "266": [
        {
            "node_id": "16",
            "leak_diameter": 0.0658940082704,
            "leak_type": "abrupt",
            "leak_start_time": 8794,
            "leak_end_time": 11618,
            "leak_peak_time": 8794
        },
        {
            "node_id": "14",
            "leak_diameter": 0.0460218116047,
            "leak_type": "incipient",
            "leak_start_time": 9758,
            "leak_end_time": 16826,
            "leak_peak_time": 12533
        }
    ],
    "268": [
        {
            "node_id": "2",
            "leak_diameter": 0.121692533075,
            "leak_type": "incipient",
            "leak_start_time": 478,
            "leak_end_time": 6543,
            "leak_peak_time": 4158
        },
        {
            "node_id": "26",
            "leak_diameter": 0.147529800567,
            "leak_type": "incipient",
            "leak_start_time": 1843,
            "leak_end_time": 3348,
            "leak_peak_time": 3169
        }
    ],
    "269": [
        {
            "node_id": "18",
            "leak_diameter": 0.10868738081,
            "leak_type": "incipient",
            "leak_start_time": 5739,
            "leak_end_time": 16704,
            "leak_peak_time": 9552
        }
    ],
    "270": [
        {
            "node_id": "4",
            "leak_diameter": 0.0486322458208,
            "leak_type": "abrupt",
            "leak_start_time": 16744,
            "leak_end_time": 17048,
            "leak_peak_time": 16744
        }
    ],
    "271": [
        {
            "node_id": "5",
            "leak_diameter": 0.126308684911,
            "leak_type": "incipient",
            "leak_start_time": 13518,
            "leak_end_time": 17477,
            "leak_peak_time": 14871
        },
        {
            "node_id": "30",
            "leak_diameter": 0.112280319246,
            "leak_type": "abrupt",
            "leak_start_time": 13270,
            "leak_end_time": 16236,
            "leak_peak_time": 13270
        }
    ],
    "272": [
        {
            "node_id": "10",
            "leak_diameter": 0.176269577614,
            "leak_type": "abrupt",
            "leak_start_time": 2397,
            "leak_end_time": 12426,
            "leak_peak_time": 2397
        },
        {
            "node_id": "8",
            "leak_diameter": 0.110501468596,
            "leak_type": "abrupt",
            "leak_start_time": 6247,
            "leak_end_time": 11937,
            "leak_peak_time": 6247
        }
    ],
    "273": [
        {
            "node_id": "15",
            "leak_diameter": 0.0521870838928,
            "leak_type": "incipient",
            "leak_start_time": 5509,
            "leak_end_time": 14910,
            "leak_peak_time": 12993
        }
    ],
    "276": [
        {
            "node_id": "11",
            "leak_diameter": 0.0907466810335,
            "leak_type": "abrupt",
            "leak_start_time": 3976,
            "leak_end_time": 11145,
            "leak_peak_time": 3976
        },
        {
            "node_id": "30",
            "leak_diameter": 0.0521950379764,
            "leak_type": "abrupt",
            "leak_start_time": 1290,
            "leak_end_time": 14057,
            "leak_peak_time": 1290
        }
    ],
    "277": [
        {
            "node_id": "9",
            "leak_diameter": 0.020914872319,
            "leak_type": "incipient",
            "leak_start_time": 16974,
            "leak_end_time": 17125,
            "leak_peak_time": 16990
        }
    ],
    "278": [
        {
            "node_id": "12",
            "leak_diameter": 0.153132238999,
            "leak_type": "abrupt",
            "leak_start_time": 3207,
            "leak_end_time": 16779,
            "leak_peak_time": 3207
        },
        {
            "node_id": "5",
            "leak_diameter": 0.184279073622,
            "leak_type": "abrupt",
            "leak_start_time": 563,
            "leak_end_time": 15268,
            "leak_peak_time": 563
        }
    ],
    "279": [
        {
            "node_id": "2",
            "leak_diameter": 0.193894690534,
            "leak_type": "abrupt",
            "leak_start_time": 12132,
            "leak_end_time": 12255,
            "leak_peak_time": 12132
        }
    ],
    "281": [
        {
            "node_id": "4",
            "leak_diameter": 0.0327381304331,
            "leak_type": "abrupt",
            "leak_start_time": 9690,
            "leak_end_time": 13194,
            "leak_peak_time": 9690
        }
    ],
    "282": [
        {
            "node_id": "10",
            "leak_diameter": 0.196854916337,
            "leak_type": "abrupt",
            "leak_start_time": 7350,
            "leak_end_time": 8782,
            "leak_peak_time": 7350
        },
        {
            "node_id": "15",
            "leak_diameter": 0.0642961111915,
            "leak_type": "incipient",
            "leak_start_time": 13312,
            "leak_end_time": 13685,
            "leak_peak_time": 13493
        }
    ],
    "283": [
        {
            "node_id": "6",
            "leak_diameter": 0.0515714009093,
            "leak_type": "abrupt",
            "leak_start_time": 4672,
            "leak_end_time": 14530,
            "leak_peak_time": 4672
        }
    ],
    "284": [
        {
            "node_id": "4",
            "leak_diameter": 0.0526550291595,
            "leak_type": "incipient",
            "leak_start_time": 2062,
            "leak_end_time": 9470,
            "leak_peak_time": 5424
        }
    ],
    "285": [
        {
            "node_id": "8",
            "leak_diameter": 0.0995483201156,
            "leak_type": "abrupt",
            "leak_start_time": 8327,
            "leak_end_time": 14895,
            "leak_peak_time": 8327
        }
    ],
    "286": [
        {
            "node_id": "17",
            "leak_diameter": 0.130591898211,
            "leak_type": "abrupt",
            "leak_start_time": 10648,
            "leak_end_time": 11486,
            "leak_peak_time": 10648
        }
    ],
    "287": [
        {
            "node_id": "10",
            "leak_diameter": 0.195925195688,
            "leak_type": "abrupt",
            "leak_start_time": 11400,
            "leak_end_time": 12018,
            "leak_peak_time": 11400
        }
    ],
    "288": [
        {
            "node_id": "11",
            "leak_diameter": 0.13457835086,
            "leak_type": "abrupt",
            "leak_start_time": 8736,
            "leak_end_time": 13162,
            "leak_peak_time": 8736
        }
    ],
    "290": [
        {
            "node_id": "18",
            "leak_diameter": 0.148511755851,
            "leak_type": "abrupt",
            "leak_start_time": 13512,
            "leak_end_time": 14465,
            "leak_peak_time": 13512
        }
    ],
    "292": [
        {
            "node_id": "3",
            "leak_diameter": 0.14983481293,
            "leak_type": "incipient",
            "leak_start_time": 6790,
            "leak_end_time": 13873,
            "leak_peak_time": 10591
        }
    ],
    "293": [
        {
            "node_id": "2",
            "leak_diameter": 0.13613342699,
            "leak_type": "incipient",
            "leak_start_time": 14431,
            "leak_end_time": 16184,
            "leak_peak_time": 15442
        }
    ],
    "294": [
        {
            "node_id": "27",
            "leak_diameter": 0.184821312629,
            "leak_type": "abrupt",
            "leak_start_time": 15100,
            "leak_end_time": 17425,
            "leak_peak_time": 15100
        },
        {
            "node_id": "26",
            "leak_diameter": 0.0728672410302,
            "leak_type": "abrupt",
            "leak_start_time": 4478,
            "leak_end_time": 11475,
            "leak_peak_time": 4478
        }
    ],
    "295": [
        {
            "node_id": "16",
            "leak_diameter": 0.159783951024,
            "leak_type": "abrupt",
            "leak_start_time": 1687,
            "leak_end_time": 10423,
            "leak_peak_time": 1687
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0983780710049,
            "leak_type": "abrupt",
            "leak_start_time": 3309,
            "leak_end_time": 12167,
            "leak_peak_time": 3309
        }
    ],
    "296": [
        {
            "node_id": "10",
            "leak_diameter": 0.10036462872,
            "leak_type": "abrupt",
            "leak_start_time": 13901,
            "leak_end_time": 14824,
            "leak_peak_time": 13901
        },
        {
            "node_id": "15",
            "leak_diameter": 0.166377464877,
            "leak_type": "incipient",
            "leak_start_time": 7416,
            "leak_end_time": 13903,
            "leak_peak_time": 8447
        }
    ],
    "298": [
        {
            "node_id": "7",
            "leak_diameter": 0.0877723760509,
            "leak_type": "abrupt",
            "leak_start_time": 1087,
            "leak_end_time": 9154,
            "leak_peak_time": 1087
        }
    ],
    "299": [
        {
            "node_id": "11",
            "leak_diameter": 0.0785533127856,
            "leak_type": "incipient",
            "leak_start_time": 2562,
            "leak_end_time": 7846,
            "leak_peak_time": 4166
        }
    ],
    "300": [
        {
            "node_id": "25",
            "leak_diameter": 0.0844451199446,
            "leak_type": "incipient",
            "leak_start_time": 2739,
            "leak_end_time": 3269,
            "leak_peak_time": 3229
        }
    ],
    "301": [
        {
            "node_id": "11",
            "leak_diameter": 0.0861548393796,
            "leak_type": "abrupt",
            "leak_start_time": 5404,
            "leak_end_time": 16360,
            "leak_peak_time": 5404
        }
    ],
    "302": [
        {
            "node_id": "12",
            "leak_diameter": 0.15810845974,
            "leak_type": "abrupt",
            "leak_start_time": 16658,
            "leak_end_time": 16871,
            "leak_peak_time": 16658
        }
    ],
    "304": [
        {
            "node_id": "32",
            "leak_diameter": 0.170021613525,
            "leak_type": "incipient",
            "leak_start_time": 16808,
            "leak_end_time": 17382,
            "leak_peak_time": 17090
        }
    ],
    "305": [
        {
            "node_id": "9",
            "leak_diameter": 0.132148779442,
            "leak_type": "incipient",
            "leak_start_time": 7152,
            "leak_end_time": 14686,
            "leak_peak_time": 13191
        }
    ],
    "306": [
        {
            "node_id": "2",
            "leak_diameter": 0.0286677836132,
            "leak_type": "incipient",
            "leak_start_time": 13968,
            "leak_end_time": 16818,
            "leak_peak_time": 15081
        }
    ],
    "308": [
        {
            "node_id": "8",
            "leak_diameter": 0.0254440799524,
            "leak_type": "abrupt",
            "leak_start_time": 13185,
            "leak_end_time": 16492,
            "leak_peak_time": 13185
        }
    ],
    "309": [
        {
            "node_id": "20",
            "leak_diameter": 0.0815545270002,
            "leak_type": "incipient",
            "leak_start_time": 9847,
            "leak_end_time": 13937,
            "leak_peak_time": 13896
        }
    ],
    "312": [
        {
            "node_id": "7",
            "leak_diameter": 0.0286518254284,
            "leak_type": "abrupt",
            "leak_start_time": 14478,
            "leak_end_time": 16074,
            "leak_peak_time": 14478
        }
    ],
    "313": [
        {
            "node_id": "6",
            "leak_diameter": 0.148853854344,
            "leak_type": "incipient",
            "leak_start_time": 9450,
            "leak_end_time": 16187,
            "leak_peak_time": 10785
        },
        {
            "node_id": "8",
            "leak_diameter": 0.112223388888,
            "leak_type": "abrupt",
            "leak_start_time": 9999,
            "leak_end_time": 16635,
            "leak_peak_time": 9999
        }
    ],
    "314": [
        {
            "node_id": "7",
            "leak_diameter": 0.143424787962,
            "leak_type": "abrupt",
            "leak_start_time": 756,
            "leak_end_time": 12436,
            "leak_peak_time": 756
        }
    ],
    "318": [
        {
            "node_id": "29",
            "leak_diameter": 0.0240111371783,
            "leak_type": "incipient",
            "leak_start_time": 2037,
            "leak_end_time": 5737,
            "leak_peak_time": 5378
        },
        {
            "node_id": "31",
            "leak_diameter": 0.146258536934,
            "leak_type": "abrupt",
            "leak_start_time": 9380,
            "leak_end_time": 11117,
            "leak_peak_time": 9380
        }
    ],
    "319": [
        {
            "node_id": "10",
            "leak_diameter": 0.0287861763587,
            "leak_type": "incipient",
            "leak_start_time": 4678,
            "leak_end_time": 16928,
            "leak_peak_time": 11614
        }
    ],
    "320": [
        {
            "node_id": "11",
            "leak_diameter": 0.0893265818314,
            "leak_type": "abrupt",
            "leak_start_time": 4423,
            "leak_end_time": 11660,
            "leak_peak_time": 4423
        },
        {
            "node_id": "20",
            "leak_diameter": 0.0871702928818,
            "leak_type": "abrupt",
            "leak_start_time": 16847,
            "leak_end_time": 17505,
            "leak_peak_time": 16847
        }
    ],
    "321": [
        {
            "node_id": "6",
            "leak_diameter": 0.0616423774139,
            "leak_type": "abrupt",
            "leak_start_time": 13276,
            "leak_end_time": 16435,
            "leak_peak_time": 13276
        }
    ],
    "322": [
        {
            "node_id": "10",
            "leak_diameter": 0.165127722502,
            "leak_type": "abrupt",
            "leak_start_time": 5109,
            "leak_end_time": 11229,
            "leak_peak_time": 5109
        }
    ],
    "323": [
        {
            "node_id": "30",
            "leak_diameter": 0.0498387045385,
            "leak_type": "abrupt",
            "leak_start_time": 12500,
            "leak_end_time": 12870,
            "leak_peak_time": 12500
        }
    ],
    "324": [
        {
            "node_id": "17",
            "leak_diameter": 0.133669612098,
            "leak_type": "incipient",
            "leak_start_time": 2168,
            "leak_end_time": 16894,
            "leak_peak_time": 3851
        }
    ],
    "325": [
        {
            "node_id": "23",
            "leak_diameter": 0.0807768501538,
            "leak_type": "incipient",
            "leak_start_time": 7426,
            "leak_end_time": 14197,
            "leak_peak_time": 9295
        },
        {
            "node_id": "31",
            "leak_diameter": 0.0452151946408,
            "leak_type": "abrupt",
            "leak_start_time": 7151,
            "leak_end_time": 14377,
            "leak_peak_time": 7151
        }
    ],
    "326": [
        {
            "node_id": "30",
            "leak_diameter": 0.0316600332193,
            "leak_type": "incipient",
            "leak_start_time": 10347,
            "leak_end_time": 12566,
            "leak_peak_time": 11259
        },
        {
            "node_id": "26",
            "leak_diameter": 0.0349037073829,
            "leak_type": "abrupt",
            "leak_start_time": 6359,
            "leak_end_time": 9872,
            "leak_peak_time": 6359
        }
    ],
    "327": [
        {
            "node_id": "20",
            "leak_diameter": 0.14212088477,
            "leak_type": "incipient",
            "leak_start_time": 7533,
            "leak_end_time": 12322,
            "leak_peak_time": 7907
        }
    ],
    "329": [
        {
            "node_id": "26",
            "leak_diameter": 0.198598148854,
            "leak_type": "incipient",
            "leak_start_time": 2712,
            "leak_end_time": 16537,
            "leak_peak_time": 10818
        }
    ],
    "330": [
        {
            "node_id": "28",
            "leak_diameter": 0.11456620918,
            "leak_type": "abrupt",
            "leak_start_time": 1275,
            "leak_end_time": 12656,
            "leak_peak_time": 1275
        },
        {
            "node_id": "8",
            "leak_diameter": 0.131667699222,
            "leak_type": "incipient",
            "leak_start_time": 7397,
            "leak_end_time": 11277,
            "leak_peak_time": 7831
        }
    ],
    "331": [
        {
            "node_id": "21",
            "leak_diameter": 0.0858627226074,
            "leak_type": "abrupt",
            "leak_start_time": 14756,
            "leak_end_time": 15617,
            "leak_peak_time": 14756
        }
    ],
    "332": [
        {
            "node_id": "12",
            "leak_diameter": 0.0863311714694,
            "leak_type": "incipient",
            "leak_start_time": 2902,
            "leak_end_time": 13960,
            "leak_peak_time": 11648
        },
        {
            "node_id": "32",
            "leak_diameter": 0.123047857501,
            "leak_type": "incipient",
            "leak_start_time": 6733,
            "leak_end_time": 7817,
            "leak_peak_time": 7576
        }
    ],
    "333": [
        {
            "node_id": "3",
            "leak_diameter": 0.104912259962,
            "leak_type": "abrupt",
            "leak_start_time": 544,
            "leak_end_time": 1649,
            "leak_peak_time": 544
        }
    ],
    "334": [
        {
            "node_id": "13",
            "leak_diameter": 0.196463467227,
            "leak_type": "incipient",
            "leak_start_time": 8724,
            "leak_end_time": 10825,
            "leak_peak_time": 9375
        },
        {
            "node_id": "8",
            "leak_diameter": 0.0707827300727,
            "leak_type": "abrupt",
            "leak_start_time": 15731,
            "leak_end_time": 16452,
            "leak_peak_time": 15731
        }
    ],
    "335": [
        {
            "node_id": "20",
            "leak_diameter": 0.0939136225637,
            "leak_type": "incipient",
            "leak_start_time": 15397,
            "leak_end_time": 16210,
            "leak_peak_time": 16096
        }
    ],
    "337": [
        {
            "node_id": "20",
            "leak_diameter": 0.0639622558056,
            "leak_type": "incipient",
            "leak_start_time": 8494,
            "leak_end_time": 11644,
            "leak_peak_time": 9215
        },
        {
            "node_id": "12",
            "leak_diameter": 0.134535879954,
            "leak_type": "abrupt",
            "leak_start_time": 3581,
            "leak_end_time": 6344,
            "leak_peak_time": 3581
        }
    ],
    "338": [
        {
            "node_id": "29",
            "leak_diameter": 0.0867095829042,
            "leak_type": "incipient",
            "leak_start_time": 16430,
            "leak_end_time": 17450,
            "leak_peak_time": 16485
        }
    ],
    "339": [
        {
            "node_id": "31",
            "leak_diameter": 0.121136749399,
            "leak_type": "incipient",
            "leak_start_time": 14496,
            "leak_end_time": 16437,
            "leak_peak_time": 15727
        }
    ],
    "341": [
        {
            "node_id": "26",
            "leak_diameter": 0.184785700783,
            "leak_type": "incipient",
            "leak_start_time": 17019,
            "leak_end_time": 17257,
            "leak_peak_time": 17233
        }
    ],
    "342": [
        {
            "node_id": "26",
            "leak_diameter": 0.166138655452,
            "leak_type": "incipient",
            "leak_start_time": 5919,
            "leak_end_time": 11371,
            "leak_peak_time": 7109
        }
    ],
    "343": [
        {
            "node_id": "5",
            "leak_diameter": 0.0567351617285,
            "leak_type": "incipient",
            "leak_start_time": 11225,
            "leak_end_time": 13583,
            "leak_peak_time": 12116
        }
    ],
    "344": [
        {
            "node_id": "21",
            "leak_diameter": 0.0291161402248,
            "leak_type": "incipient",
            "leak_start_time": 16785,
            "leak_end_time": 17280,
            "leak_peak_time": 17257
        }
    ],
    "345": [
        {
            "node_id": "11",
            "leak_diameter": 0.189836849684,
            "leak_type": "incipient",
            "leak_start_time": 15463,
            "leak_end_time": 15497,
            "leak_peak_time": 15487
        },
        {
            "node_id": "20",
            "leak_diameter": 0.148704258496,
            "leak_type": "incipient",
            "leak_start_time": 8054,
            "leak_end_time": 13219,
            "leak_peak_time": 9871
        }
    ],
    "347": [
        {
            "node_id": "17",
            "leak_diameter": 0.156694657618,
            "leak_type": "abrupt",
            "leak_start_time": 7481,
            "leak_end_time": 16963,
            "leak_peak_time": 7481
        }
    ],
    "348": [
        {
            "node_id": "8",
            "leak_diameter": 0.0555994651862,
            "leak_type": "abrupt",
            "leak_start_time": 7938,
            "leak_end_time": 15622,
            "leak_peak_time": 7938
        }
    ],
    "349": [
        {
            "node_id": "6",
            "leak_diameter": 0.100318115186,
            "leak_type": "incipient",
            "leak_start_time": 5595,
            "leak_end_time": 5784,
            "leak_peak_time": 5659
        },
        {
            "node_id": "7",
            "leak_diameter": 0.141655336011,
            "leak_type": "incipient",
            "leak_start_time": 10806,
            "leak_end_time": 15200,
            "leak_peak_time": 14147
        }
    ],
    "350": [
        {
            "node_id": "21",
            "leak_diameter": 0.0213850939852,
            "leak_type": "incipient",
            "leak_start_time": 17277,
            "leak_end_time": 17361,
            "leak_peak_time": 17321
        },
        {
            "node_id": "9",
            "leak_diameter": 0.0501141116782,
            "leak_type": "abrupt",
            "leak_start_time": 2527,
            "leak_end_time": 16913,
            "leak_peak_time": 2527
        }
    ],
    "352": [
        {
            "node_id": "22",
            "leak_diameter": 0.0634487282623,
            "leak_type": "incipient",
            "leak_start_time": 8572,
            "leak_end_time": 17057,
            "leak_peak_time": 11129
        },
        {
            "node_id": "17",
            "leak_diameter": 0.100984537662,
            "leak_type": "abrupt",
            "leak_start_time": 3303,
            "leak_end_time": 15298,
            "leak_peak_time": 3303
        }
    ],
    "353": [
        {
            "node_id": "23",
            "leak_diameter": 0.1616933326,
            "leak_type": "incipient",
            "leak_start_time": 7017,
            "leak_end_time": 13297,
            "leak_peak_time": 8895
        }
    ],
    "354": [
        {
            "node_id": "7",
            "leak_diameter": 0.0337181520242,
            "leak_type": "incipient",
            "leak_start_time": 10924,
            "leak_end_time": 15027,
            "leak_peak_time": 12067
        }
    ],
    "355": [
        {
            "node_id": "17",
            "leak_diameter": 0.029596132972,
            "leak_type": "incipient",
            "leak_start_time": 12685,
            "leak_end_time": 13861,
            "leak_peak_time": 13328
        },
        {
            "node_id": "9",
            "leak_diameter": 0.15734565259,
            "leak_type": "abrupt",
            "leak_start_time": 10870,
            "leak_end_time": 13414,
            "leak_peak_time": 10870
        }
    ],
    "357": [
        {
            "node_id": "28",
            "leak_diameter": 0.123134960357,
            "leak_type": "incipient",
            "leak_start_time": 7006,
            "leak_end_time": 14616,
            "leak_peak_time": 10824
        }
    ],
    "358": [
        {
            "node_id": "19",
            "leak_diameter": 0.0320624132281,
            "leak_type": "incipient",
            "leak_start_time": 4902,
            "leak_end_time": 16294,
            "leak_peak_time": 8045
        }
    ],
    "359": [
        {
            "node_id": "11",
            "leak_diameter": 0.115615260914,
            "leak_type": "abrupt",
            "leak_start_time": 10041,
            "leak_end_time": 15491,
            "leak_peak_time": 10041
        },
        {
            "node_id": "5",
            "leak_diameter": 0.128588704237,
            "leak_type": "abrupt",
            "leak_start_time": 1741,
            "leak_end_time": 15648,
            "leak_peak_time": 1741
        }
    ],
    "361": [
        {
            "node_id": "29",
            "leak_diameter": 0.139503270833,
            "leak_type": "abrupt",
            "leak_start_time": 2189,
            "leak_end_time": 7858,
            "leak_peak_time": 2189
        }
    ],
    "362": [
        {
            "node_id": "16",
            "leak_diameter": 0.0929016446077,
            "leak_type": "incipient",
            "leak_start_time": 13999,
            "leak_end_time": 17422,
            "leak_peak_time": 15390
        }
    ],
    "363": [
        {
            "node_id": "17",
            "leak_diameter": 0.166405814697,
            "leak_type": "incipient",
            "leak_start_time": 16431,
            "leak_end_time": 17356,
            "leak_peak_time": 16487
        }
    ],
    "364": [
        {
            "node_id": "12",
            "leak_diameter": 0.131819437011,
            "leak_type": "abrupt",
            "leak_start_time": 500,
            "leak_end_time": 4738,
            "leak_peak_time": 500
        },
        {
            "node_id": "8",
            "leak_diameter": 0.144151948318,
            "leak_type": "incipient",
            "leak_start_time": 9613,
            "leak_end_time": 14053,
            "leak_peak_time": 11756
        }
    ],
    "365": [
        {
            "node_id": "32",
            "leak_diameter": 0.0908743477505,
            "leak_type": "incipient",
            "leak_start_time": 5924,
            "leak_end_time": 7215,
            "leak_peak_time": 5969
        }
    ],
    "366": [
        {
            "node_id": "31",
            "leak_diameter": 0.109146757028,
            "leak_type": "incipient",
            "leak_start_time": 7994,
            "leak_end_time": 8093,
            "leak_peak_time": 8073
        }
    ],
    "367": [
        {
            "node_id": "27",
            "leak_diameter": 0.166929500722,
            "leak_type": "abrupt",
            "leak_start_time": 13648,
            "leak_end_time": 15075,
            "leak_peak_time": 13648
        }
    ],
    "369": [
        {
            "node_id": "8",
            "leak_diameter": 0.0832509262085,
            "leak_type": "incipient",
            "leak_start_time": 4497,
            "leak_end_time": 16979,
            "leak_peak_time": 9591
        }
    ],
    "370": [
        {
            "node_id": "27",
            "leak_diameter": 0.0561448718906,
            "leak_type": "incipient",
            "leak_start_time": 1356,
            "leak_end_time": 4892,
            "leak_peak_time": 2777
        },
        {
            "node_id": "11",
            "leak_diameter": 0.0611683396495,
            "leak_type": "abrupt",
            "leak_start_time": 14825,
            "leak_end_time": 17312,
            "leak_peak_time": 14825
        }
    ],
    "371": [
        {
            "node_id": "7",
            "leak_diameter": 0.188654328069,
            "leak_type": "incipient",
            "leak_start_time": 15261,
            "leak_end_time": 16331,
            "leak_peak_time": 15582
        }
    ],
    "372": [
        {
            "node_id": "18",
            "leak_diameter": 0.0477500498508,
            "leak_type": "abrupt",
            "leak_start_time": 13662,
            "leak_end_time": 13730,
            "leak_peak_time": 13662
        },
        {
            "node_id": "15",
            "leak_diameter": 0.125388716098,
            "leak_type": "abrupt",
            "leak_start_time": 12715,
            "leak_end_time": 17316,
            "leak_peak_time": 12715
        }
    ],
    "373": [
        {
            "node_id": "9",
            "leak_diameter": 0.178168314652,
            "leak_type": "incipient",
            "leak_start_time": 6075,
            "leak_end_time": 10709,
            "leak_peak_time": 7626
        }
    ],
    "375": [
        {
            "node_id": "26",
            "leak_diameter": 0.11480732694,
            "leak_type": "incipient",
            "leak_start_time": 12471,
            "leak_end_time": 14030,
            "leak_peak_time": 12839
        }
    ],
    "376": [
        {
            "node_id": "19",
            "leak_diameter": 0.17038777512,
            "leak_type": "abrupt",
            "leak_start_time": 2764,
            "leak_end_time": 16448,
            "leak_peak_time": 2764
        }
    ],
    "377": [
        {
            "node_id": "21",
            "leak_diameter": 0.0406077907255,
            "leak_type": "incipient",
            "leak_start_time": 260,
            "leak_end_time": 9803,
            "leak_peak_time": 2057
        },
        {
            "node_id": "31",
            "leak_diameter": 0.118434759162,
            "leak_type": "incipient",
            "leak_start_time": 14978,
            "leak_end_time": 17500,
            "leak_peak_time": 17299
        }
    ],
    "381": [
        {
            "node_id": "8",
            "leak_diameter": 0.146033765949,
            "leak_type": "abrupt",
            "leak_start_time": 16943,
            "leak_end_time": 17313,
            "leak_peak_time": 16943
        }
    ],
    "382": [
        {
            "node_id": "10",
            "leak_diameter": 0.0722957704373,
            "leak_type": "abrupt",
            "leak_start_time": 17356,
            "leak_end_time": 17417,
            "leak_peak_time": 17356
        }
    ],
    "383": [
        {
            "node_id": "15",
            "leak_diameter": 0.0662369090006,
            "leak_type": "abrupt",
            "leak_start_time": 11888,
            "leak_end_time": 14089,
            "leak_peak_time": 11888
        }
    ],
    "384": [
        {
            "node_id": "15",
            "leak_diameter": 0.159595005937,
            "leak_type": "abrupt",
            "leak_start_time": 7671,
            "leak_end_time": 10297,
            "leak_peak_time": 7671
        }
    ],
    "385": [
        {
            "node_id": "19",
            "leak_diameter": 0.0531170656314,
            "leak_type": "abrupt",
            "leak_start_time": 14647,
            "leak_end_time": 14877,
            "leak_peak_time": 14647
        }
    ],
    "387": [
        {
            "node_id": "11",
            "leak_diameter": 0.112134175956,
            "leak_type": "abrupt",
            "leak_start_time": 8618,
            "leak_end_time": 9940,
            "leak_peak_time": 8618
        }
    ],
    "388": [
        {
            "node_id": "13",
            "leak_diameter": 0.0303944749223,
            "leak_type": "abrupt",
            "leak_start_time": 11663,
            "leak_end_time": 13743,
            "leak_peak_time": 11663
        }
    ],
    "389": [
        {
            "node_id": "3",
            "leak_diameter": 0.16595925765,
            "leak_type": "incipient",
            "leak_start_time": 16344,
            "leak_end_time": 16814,
            "leak_peak_time": 16379
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0311190153235,
            "leak_type": "incipient",
            "leak_start_time": 15321,
            "leak_end_time": 15961,
            "leak_peak_time": 15887
        }
    ],
    "390": [
        {
            "node_id": "30",
            "leak_diameter": 0.1433789258,
            "leak_type": "incipient",
            "leak_start_time": 4085,
            "leak_end_time": 9648,
            "leak_peak_time": 6889
        }
    ],
    "391": [
        {
            "node_id": "11",
            "leak_diameter": 0.140839813471,
            "leak_type": "abrupt",
            "leak_start_time": 1964,
            "leak_end_time": 8242,
            "leak_peak_time": 1964
        }
    ],
    "392": [
        {
            "node_id": "15",
            "leak_diameter": 0.0260377461087,
            "leak_type": "incipient",
            "leak_start_time": 6016,
            "leak_end_time": 6470,
            "leak_peak_time": 6189
        },
        {
            "node_id": "13",
            "leak_diameter": 0.163093727803,
            "leak_type": "incipient",
            "leak_start_time": 10856,
            "leak_end_time": 15222,
            "leak_peak_time": 13778
        }
    ],
    "393": [
        {
            "node_id": "31",
            "leak_diameter": 0.0451375556918,
            "leak_type": "abrupt",
            "leak_start_time": 12520,
            "leak_end_time": 13580,
            "leak_peak_time": 12520
        }
    ],
    "394": [
        {
            "node_id": "13",
            "leak_diameter": 0.190595479654,
            "leak_type": "abrupt",
            "leak_start_time": 16364,
            "leak_end_time": 17429,
            "leak_peak_time": 16364
        }
    ],
    "396": [
        {
            "node_id": "6",
            "leak_diameter": 0.0819065497387,
            "leak_type": "incipient",
            "leak_start_time": 10167,
            "leak_end_time": 16746,
            "leak_peak_time": 14134
        }
    ],
    "398": [
        {
            "node_id": "4",
            "leak_diameter": 0.0401152606426,
            "leak_type": "incipient",
            "leak_start_time": 11192,
            "leak_end_time": 17371,
            "leak_peak_time": 14179
        }
    ],
    "400": [
        {
            "node_id": "5",
            "leak_diameter": 0.0629053307307,
            "leak_type": "abrupt",
            "leak_start_time": 7692,
            "leak_end_time": 10135,
            "leak_peak_time": 7692
        }
    ],
    "402": [
        {
            "node_id": "15",
            "leak_diameter": 0.0741328988499,
            "leak_type": "abrupt",
            "leak_start_time": 10790,
            "leak_end_time": 14566,
            "leak_peak_time": 10790
        },
        {
            "node_id": "8",
            "leak_diameter": 0.0233074431136,
            "leak_type": "incipient",
            "leak_start_time": 11528,
            "leak_end_time": 14440,
            "leak_peak_time": 14185
        }
    ],
    "403": [
        {
            "node_id": "11",
            "leak_diameter": 0.133845711856,
            "leak_type": "incipient",
            "leak_start_time": 17083,
            "leak_end_time": 17420,
            "leak_peak_time": 17226
        },
        {
            "node_id": "25",
            "leak_diameter": 0.103357322688,
            "leak_type": "incipient",
            "leak_start_time": 15776,
            "leak_end_time": 16553,
            "leak_peak_time": 16242
        }
    ],
    "405": [
        {
            "node_id": "15",
            "leak_diameter": 0.138193736251,
            "leak_type": "incipient",
            "leak_start_time": 7659,
            "leak_end_time": 15467,
            "leak_peak_time": 12359
        }
    ],
    "406": [
        {
            "node_id": "21",
            "leak_diameter": 0.177072447389,
            "leak_type": "incipient",
            "leak_start_time": 16682,
            "leak_end_time": 16953,
            "leak_peak_time": 16907
        }
    ],
    "408": [
        {
            "node_id": "20",
            "leak_diameter": 0.0609547929139,
            "leak_type": "abrupt",
            "leak_start_time": 16644,
            "leak_end_time": 16910,
            "leak_peak_time": 16644
        }
    ],
    "409": [
        {
            "node_id": "4",
            "leak_diameter": 0.0301893023019,
            "leak_type": "abrupt",
            "leak_start_time": 10967,
            "leak_end_time": 13579,
            "leak_peak_time": 10967
        },
        {
            "node_id": "22",
            "leak_diameter": 0.105943636538,
            "leak_type": "incipient",
            "leak_start_time": 9249,
            "leak_end_time": 11961,
            "leak_peak_time": 10780
        }
    ],
    "410": [
        {
            "node_id": "13",
            "leak_diameter": 0.157021570818,
            "leak_type": "abrupt",
            "leak_start_time": 2733,
            "leak_end_time": 6333,
            "leak_peak_time": 2733
        }
    ],
    "411": [
        {
            "node_id": "29",
            "leak_diameter": 0.0813426625549,
            "leak_type": "incipient",
            "leak_start_time": 1851,
            "leak_end_time": 9288,
            "leak_peak_time": 3502
        }
    ],
    "412": [
        {
            "node_id": "10",
            "leak_diameter": 0.0612915402176,
            "leak_type": "incipient",
            "leak_start_time": 6443,
            "leak_end_time": 15339,
            "leak_peak_time": 9655
        }
    ],
    "413": [
        {
            "node_id": "9",
            "leak_diameter": 0.186045170801,
            "leak_type": "abrupt",
            "leak_start_time": 6781,
            "leak_end_time": 11508,
            "leak_peak_time": 6781
        }
    ],
    "414": [
        {
            "node_id": "28",
            "leak_diameter": 0.13470313674,
            "leak_type": "incipient",
            "leak_start_time": 8293,
            "leak_end_time": 13143,
            "leak_peak_time": 8674
        },
        {
            "node_id": "30",
            "leak_diameter": 0.0864675235158,
            "leak_type": "incipient",
            "leak_start_time": 4839,
            "leak_end_time": 10642,
            "leak_peak_time": 10032
        }
    ],
    "415": [
        {
            "node_id": "26",
            "leak_diameter": 0.147068376148,
            "leak_type": "incipient",
            "leak_start_time": 7793,
            "leak_end_time": 15761,
            "leak_peak_time": 14947
        }
    ],
    "416": [
        {
            "node_id": "31",
            "leak_diameter": 0.107391752147,
            "leak_type": "abrupt",
            "leak_start_time": 17120,
            "leak_end_time": 17154,
            "leak_peak_time": 17120
        }
    ],
    "417": [
        {
            "node_id": "27",
            "leak_diameter": 0.199492886269,
            "leak_type": "incipient",
            "leak_start_time": 6392,
            "leak_end_time": 13375,
            "leak_peak_time": 6803
        }
    ],
    "419": [
        {
            "node_id": "23",
            "leak_diameter": 0.0517957132109,
            "leak_type": "abrupt",
            "leak_start_time": 8058,
            "leak_end_time": 13760,
            "leak_peak_time": 8058
        }
    ],
    "420": [
        {
            "node_id": "18",
            "leak_diameter": 0.125503197057,
            "leak_type": "abrupt",
            "leak_start_time": 15324,
            "leak_end_time": 16590,
            "leak_peak_time": 15324
        }
    ],
    "421": [
        {
            "node_id": "5",
            "leak_diameter": 0.195513409502,
            "leak_type": "abrupt",
            "leak_start_time": 13094,
            "leak_end_time": 15873,
            "leak_peak_time": 13094
        },
        {
            "node_id": "32",
            "leak_diameter": 0.087265768114,
            "leak_type": "incipient",
            "leak_start_time": 6193,
            "leak_end_time": 15117,
            "leak_peak_time": 8683
        }
    ],
    "422": [
        {
            "node_id": "14",
            "leak_diameter": 0.133002013086,
            "leak_type": "incipient",
            "leak_start_time": 5292,
            "leak_end_time": 12086,
            "leak_peak_time": 7193
        }
    ],
    "423": [
        {
            "node_id": "2",
            "leak_diameter": 0.0803364790563,
            "leak_type": "incipient",
            "leak_start_time": 130,
            "leak_end_time": 2800,
            "leak_peak_time": 2525
        },
        {
            "node_id": "32",
            "leak_diameter": 0.117568900693,
            "leak_type": "abrupt",
            "leak_start_time": 9737,
            "leak_end_time": 10395,
            "leak_peak_time": 9737
        }
    ],
    "424": [
        {
            "node_id": "32",
            "leak_diameter": 0.0583029094635,
            "leak_type": "incipient",
            "leak_start_time": 1733,
            "leak_end_time": 15484,
            "leak_peak_time": 9326
        }
    ],
    "425": [
        {
            "node_id": "11",
            "leak_diameter": 0.151575607306,
            "leak_type": "abrupt",
            "leak_start_time": 11287,
            "leak_end_time": 16879,
            "leak_peak_time": 11287
        }
    ],
    "426": [
        {
            "node_id": "31",
            "leak_diameter": 0.15141622901,
            "leak_type": "abrupt",
            "leak_start_time": 5800,
            "leak_end_time": 6035,
            "leak_peak_time": 5800
        }
    ],
    "427": [
        {
            "node_id": "4",
            "leak_diameter": 0.10871056461,
            "leak_type": "abrupt",
            "leak_start_time": 17201,
            "leak_end_time": 17430,
            "leak_peak_time": 17201
        },
        {
            "node_id": "21",
            "leak_diameter": 0.130688905206,
            "leak_type": "incipient",
            "leak_start_time": 1241,
            "leak_end_time": 15343,
            "leak_peak_time": 6240
        }
    ],
    "428": [
        {
            "node_id": "22",
            "leak_diameter": 0.0222775881689,
            "leak_type": "abrupt",
            "leak_start_time": 14599,
            "leak_end_time": 15677,
            "leak_peak_time": 14599
        },
        {
            "node_id": "5",
            "leak_diameter": 0.0434917592015,
            "leak_type": "incipient",
            "leak_start_time": 2531,
            "leak_end_time": 12192,
            "leak_peak_time": 4893
        }
    ],
    "429": [
        {
            "node_id": "22",
            "leak_diameter": 0.146521638078,
            "leak_type": "incipient",
            "leak_start_time": 14100,
            "leak_end_time": 16704,
            "leak_peak_time": 15881
        },
        {
            "node_id": "23",
            "leak_diameter": 0.18411921791,
            "leak_type": "abrupt",
            "leak_start_time": 106,
            "leak_end_time": 16432,
            "leak_peak_time": 106
        }
    ],
    "430": [
        {
            "node_id": "15",
            "leak_diameter": 0.0369035210524,
            "leak_type": "incipient",
            "leak_start_time": 8088,
            "leak_end_time": 12195,
            "leak_peak_time": 9825
        },
        {
            "node_id": "13",
            "leak_diameter": 0.0757904574392,
            "leak_type": "incipient",
            "leak_start_time": 15459,
            "leak_end_time": 16052,
            "leak_peak_time": 15955
        }
    ],
    "431": [
        {
            "node_id": "6",
            "leak_diameter": 0.148588609728,
            "leak_type": "abrupt",
            "leak_start_time": 6479,
            "leak_end_time": 10928,
            "leak_peak_time": 6479
        }
    ],
    "432": [
        {
            "node_id": "16",
            "leak_diameter": 0.0561169194073,
            "leak_type": "abrupt",
            "leak_start_time": 5785,
            "leak_end_time": 7691,
            "leak_peak_time": 5785
        }
    ],
    "434": [
        {
            "node_id": "27",
            "leak_diameter": 0.0494343817032,
            "leak_type": "incipient",
            "leak_start_time": 3561,
            "leak_end_time": 7785,
            "leak_peak_time": 6853
        }
    ],
    "435": [
        {
            "node_id": "7",
            "leak_diameter": 0.165316215665,
            "leak_type": "incipient",
            "leak_start_time": 13330,
            "leak_end_time": 13629,
            "leak_peak_time": 13534
        }
    ],
    "436": [
        {
            "node_id": "6",
            "leak_diameter": 0.0341056221168,
            "leak_type": "incipient",
            "leak_start_time": 6225,
            "leak_end_time": 11702,
            "leak_peak_time": 6403
        }
    ],
    "437": [
        {
            "node_id": "11",
            "leak_diameter": 0.197338334049,
            "leak_type": "incipient",
            "leak_start_time": 844,
            "leak_end_time": 16799,
            "leak_peak_time": 16209
        },
        {
            "node_id": "26",
            "leak_diameter": 0.0366843980311,
            "leak_type": "abrupt",
            "leak_start_time": 7605,
            "leak_end_time": 10367,
            "leak_peak_time": 7605
        }
    ],
    "438": [
        {
            "node_id": "31",
            "leak_diameter": 0.195036150437,
            "leak_type": "abrupt",
            "leak_start_time": 10823,
            "leak_end_time": 15502,
            "leak_peak_time": 10823
        }
    ],
    "439": [
        {
            "node_id": "9",
            "leak_diameter": 0.173809739842,
            "leak_type": "abrupt",
            "leak_start_time": 1168,
            "leak_end_time": 15849,
            "leak_peak_time": 1168
        }
    ],
    "442": [
        {
            "node_id": "20",
            "leak_diameter": 0.023419824224,
            "leak_type": "incipient",
            "leak_start_time": 1987,
            "leak_end_time": 5975,
            "leak_peak_time": 5582
        },
        {
            "node_id": "22",
            "leak_diameter": 0.197547222678,
            "leak_type": "abrupt",
            "leak_start_time": 17456,
            "leak_end_time": 17467,
            "leak_peak_time": 17456
        }
    ],
    "443": [
        {
            "node_id": "18",
            "leak_diameter": 0.0976284525115,
            "leak_type": "abrupt",
            "leak_start_time": 9312,
            "leak_end_time": 10768,
            "leak_peak_time": 9312
        },
        {
            "node_id": "2",
            "leak_diameter": 0.0685879282411,
            "leak_type": "abrupt",
            "leak_start_time": 14275,
            "leak_end_time": 17359,
            "leak_peak_time": 14275
        }
    ],
    "444": [
        {
            "node_id": "17",
            "leak_diameter": 0.0806438384967,
            "leak_type": "abrupt",
            "leak_start_time": 2877,
            "leak_end_time": 5112,
            "leak_peak_time": 2877
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0965438402545,
            "leak_type": "abrupt",
            "leak_start_time": 12015,
            "leak_end_time": 16665,
            "leak_peak_time": 12015
        }
    ],
    "446": [
        {
            "node_id": "18",
            "leak_diameter": 0.159812682745,
            "leak_type": "incipient",
            "leak_start_time": 16382,
            "leak_end_time": 16394,
            "leak_peak_time": 16388
        }
    ],
    "447": [
        {
            "node_id": "19",
            "leak_diameter": 0.177358792472,
            "leak_type": "abrupt",
            "leak_start_time": 13988,
            "leak_end_time": 16084,
            "leak_peak_time": 13988
        }
    ],
    "448": [
        {
            "node_id": "5",
            "leak_diameter": 0.188023071586,
            "leak_type": "incipient",
            "leak_start_time": 13124,
            "leak_end_time": 16247,
            "leak_peak_time": 15762
        },
        {
            "node_id": "32",
            "leak_diameter": 0.19496251191,
            "leak_type": "incipient",
            "leak_start_time": 15355,
            "leak_end_time": 15640,
            "leak_peak_time": 15439
        }
    ],
    "449": [
        {
            "node_id": "21",
            "leak_diameter": 0.0453112494845,
            "leak_type": "abrupt",
            "leak_start_time": 9386,
            "leak_end_time": 16764,
            "leak_peak_time": 9386
        },
        {
            "node_id": "3",
            "leak_diameter": 0.074359829878,
            "leak_type": "incipient",
            "leak_start_time": 273,
            "leak_end_time": 9265,
            "leak_peak_time": 7295
        }
    ],
    "450": [
        {
            "node_id": "6",
            "leak_diameter": 0.144720081029,
            "leak_type": "abrupt",
            "leak_start_time": 1681,
            "leak_end_time": 14239,
            "leak_peak_time": 1681
        },
        {
            "node_id": "25",
            "leak_diameter": 0.0637347215503,
            "leak_type": "incipient",
            "leak_start_time": 2832,
            "leak_end_time": 4482,
            "leak_peak_time": 3722
        }
    ],
    "452": [
        {
            "node_id": "28",
            "leak_diameter": 0.109200158193,
            "leak_type": "abrupt",
            "leak_start_time": 10272,
            "leak_end_time": 13881,
            "leak_peak_time": 10272
        }
    ],
    "453": [
        {
            "node_id": "21",
            "leak_diameter": 0.0709990941269,
            "leak_type": "incipient",
            "leak_start_time": 12801,
            "leak_end_time": 14397,
            "leak_peak_time": 13456
        }
    ],
    "454": [
        {
            "node_id": "3",
            "leak_diameter": 0.021229943137,
            "leak_type": "incipient",
            "leak_start_time": 11297,
            "leak_end_time": 15362,
            "leak_peak_time": 11833
        }
    ],
    "455": [
        {
            "node_id": "29",
            "leak_diameter": 0.027426212593,
            "leak_type": "abrupt",
            "leak_start_time": 13964,
            "leak_end_time": 16027,
            "leak_peak_time": 13964
        }
    ],
    "456": [
        {
            "node_id": "18",
            "leak_diameter": 0.186642090765,
            "leak_type": "abrupt",
            "leak_start_time": 1523,
            "leak_end_time": 2494,
            "leak_peak_time": 1523
        }
    ],
    "457": [
        {
            "node_id": "4",
            "leak_diameter": 0.0425652756351,
            "leak_type": "abrupt",
            "leak_start_time": 10768,
            "leak_end_time": 14684,
            "leak_peak_time": 10768
        },
        {
            "node_id": "28",
            "leak_diameter": 0.090961588765,
            "leak_type": "abrupt",
            "leak_start_time": 13781,
            "leak_end_time": 13932,
            "leak_peak_time": 13781
        }
    ],
    "458": [
        {
            "node_id": "2",
            "leak_diameter": 0.102047355177,
            "leak_type": "abrupt",
            "leak_start_time": 14333,
            "leak_end_time": 16951,
            "leak_peak_time": 14333
        }
    ],
    "459": [
        {
            "node_id": "12",
            "leak_diameter": 0.0260343060977,
            "leak_type": "incipient",
            "leak_start_time": 6466,
            "leak_end_time": 7820,
            "leak_peak_time": 6654
        }
    ],
    "460": [
        {
            "node_id": "16",
            "leak_diameter": 0.130984027218,
            "leak_type": "incipient",
            "leak_start_time": 14931,
            "leak_end_time": 17160,
            "leak_peak_time": 16331
        },
        {
            "node_id": "18",
            "leak_diameter": 0.0315194733883,
            "leak_type": "incipient",
            "leak_start_time": 8117,
            "leak_end_time": 9598,
            "leak_peak_time": 9126
        }
    ],
    "463": [
        {
            "node_id": "6",
            "leak_diameter": 0.0912717789295,
            "leak_type": "incipient",
            "leak_start_time": 14544,
            "leak_end_time": 16499,
            "leak_peak_time": 15620
        }
    ],
    "464": [
        {
            "node_id": "22",
            "leak_diameter": 0.0443188449872,
            "leak_type": "incipient",
            "leak_start_time": 5586,
            "leak_end_time": 11868,
            "leak_peak_time": 10636
        }
    ],
    "465": [
        {
            "node_id": "10",
            "leak_diameter": 0.110364085964,
            "leak_type": "incipient",
            "leak_start_time": 10385,
            "leak_end_time": 12186,
            "leak_peak_time": 11746
        }
    ],
    "466": [
        {
            "node_id": "11",
            "leak_diameter": 0.0970272210571,
            "leak_type": "abrupt",
            "leak_start_time": 2267,
            "leak_end_time": 16798,
            "leak_peak_time": 2267
        },
        {
            "node_id": "29",
            "leak_diameter": 0.0829569264599,
            "leak_type": "abrupt",
            "leak_start_time": 3227,
            "leak_end_time": 12814,
            "leak_peak_time": 3227
        }
    ],
    "468": [
        {
            "node_id": "13",
            "leak_diameter": 0.0394318675477,
            "leak_type": "abrupt",
            "leak_start_time": 4588,
            "leak_end_time": 12841,
            "leak_peak_time": 4588
        }
    ],
    "470": [
        {
            "node_id": "2",
            "leak_diameter": 0.14934849999,
            "leak_type": "abrupt",
            "leak_start_time": 5204,
            "leak_end_time": 6739,
            "leak_peak_time": 5204
        }
    ],
    "471": [
        {
            "node_id": "22",
            "leak_diameter": 0.0674653563986,
            "leak_type": "incipient",
            "leak_start_time": 9831,
            "leak_end_time": 12664,
            "leak_peak_time": 11100
        }
    ],
    "472": [
        {
            "node_id": "3",
            "leak_diameter": 0.0978162501455,
            "leak_type": "abrupt",
            "leak_start_time": 2213,
            "leak_end_time": 5861,
            "leak_peak_time": 2213
        }
    ],
    "473": [
        {
            "node_id": "31",
            "leak_diameter": 0.125796819179,
            "leak_type": "abrupt",
            "leak_start_time": 11073,
            "leak_end_time": 15393,
            "leak_peak_time": 11073
        }
    ],
    "474": [
        {
            "node_id": "6",
            "leak_diameter": 0.167907071107,
            "leak_type": "incipient",
            "leak_start_time": 14525,
            "leak_end_time": 17310,
            "leak_peak_time": 15631
        },
        {
            "node_id": "14",
            "leak_diameter": 0.120208417836,
            "leak_type": "abrupt",
            "leak_start_time": 14144,
            "leak_end_time": 16930,
            "leak_peak_time": 14144
        }
    ],
    "475": [
        {
            "node_id": "12",
            "leak_diameter": 0.16837482272,
            "leak_type": "abrupt",
            "leak_start_time": 1441,
            "leak_end_time": 2357,
            "leak_peak_time": 1441
        }
    ],
    "476": [
        {
            "node_id": "10",
            "leak_diameter": 0.0271493193017,
            "leak_type": "abrupt",
            "leak_start_time": 2878,
            "leak_end_time": 14620,
            "leak_peak_time": 2878
        }
    ],
    "479": [
        {
            "node_id": "14",
            "leak_diameter": 0.0449392144015,
            "leak_type": "abrupt",
            "leak_start_time": 8253,
            "leak_end_time": 10170,
            "leak_peak_time": 8253
        }
    ],
    "480": [
        {
            "node_id": "20",
            "leak_diameter": 0.0363446579052,
            "leak_type": "incipient",
            "leak_start_time": 10623,
            "leak_end_time": 15049,
            "leak_peak_time": 12412
        }
    ],
    "481": [
        {
            "node_id": "29",
            "leak_diameter": 0.189204979974,
            "leak_type": "incipient",
            "leak_start_time": 7408,
            "leak_end_time": 14006,
            "leak_peak_time": 11736
        }
    ],
    "482": [
        {
            "node_id": "17",
            "leak_diameter": 0.16831400311,
            "leak_type": "abrupt",
            "leak_start_time": 1912,
            "leak_end_time": 9171,
            "leak_peak_time": 1912
        }
    ],
    "483": [
        {
            "node_id": "20",
            "leak_diameter": 0.109311369737,
            "leak_type": "incipient",
            "leak_start_time": 4322,
            "leak_end_time": 9274,
            "leak_peak_time": 8595
        }
    ],
    "485": [
        {
            "node_id": "11",
            "leak_diameter": 0.171882784582,
            "leak_type": "abrupt",
            "leak_start_time": 10377,
            "leak_end_time": 14514,
            "leak_peak_time": 10377
        },
        {
            "node_id": "32",
            "leak_diameter": 0.1238058384,
            "leak_type": "abrupt",
            "leak_start_time": 2468,
            "leak_end_time": 8774,
            "leak_peak_time": 2468
        }
    ],
    "488": [
        {
            "node_id": "23",
            "leak_diameter": 0.166909156024,
            "leak_type": "abrupt",
            "leak_start_time": 12099,
            "leak_end_time": 13895,
            "leak_peak_time": 12099
        }
    ],
    "490": [
        {
            "node_id": "26",
            "leak_diameter": 0.083366199163,
            "leak_type": "abrupt",
            "leak_start_time": 16690,
            "leak_end_time": 16773,
            "leak_peak_time": 16690
        }
    ],
    "492": [
        {
            "node_id": "27",
            "leak_diameter": 0.0903152431614,
            "leak_type": "abrupt",
            "leak_start_time": 5248,
            "leak_end_time": 14621,
            "leak_peak_time": 5248
        }
    ],
    "494": [
        {
            "node_id": "25",
            "leak_diameter": 0.160889298569,
            "leak_type": "incipient",
            "leak_start_time": 13224,
            "leak_end_time": 14285,
            "leak_peak_time": 14107
        },
        {
            "node_id": "14",
            "leak_diameter": 0.0520855441136,
            "leak_type": "abrupt",
            "leak_start_time": 2497,
            "leak_end_time": 5647,
            "leak_peak_time": 2497
        }
    ],
    "495": [
        {
            "node_id": "17",
            "leak_diameter": 0.0864588710361,
            "leak_type": "abrupt",
            "leak_start_time": 10467,
            "leak_end_time": 17304,
            "leak_peak_time": 10467
        }
    ],
    "496": [
        {
            "node_id": "29",
            "leak_diameter": 0.189749406242,
            "leak_type": "abrupt",
            "leak_start_time": 15688,
            "leak_end_time": 17476,
            "leak_peak_time": 15688
        }
    ],
    "497": [
        {
            "node_id": "14",
            "leak_diameter": 0.047095554658,
            "leak_type": "abrupt",
            "leak_start_time": 11429,
            "leak_end_time": 14215,
            "leak_peak_time": 11429
        }
    ],
    "500": [
        {
            "node_id": "8",
            "leak_diameter": 0.141928082483,
            "leak_type": "abrupt",
            "leak_start_time": 12864,
            "leak_end_time": 13219,
            "leak_peak_time": 12864
        }
    ],
    "501": [
        {
            "node_id": "10",
            "leak_diameter": 0.0451199379305,
            "leak_type": "incipient",
            "leak_start_time": 7831,
            "leak_end_time": 13490,
            "leak_peak_time": 8897
        },
        {
            "node_id": "23",
            "leak_diameter": 0.122992186493,
            "leak_type": "incipient",
            "leak_start_time": 1122,
            "leak_end_time": 14829,
            "leak_peak_time": 9350
        }
    ],
    "502": [
        {
            "node_id": "6",
            "leak_diameter": 0.190321169259,
            "leak_type": "incipient",
            "leak_start_time": 4864,
            "leak_end_time": 10430,
            "leak_peak_time": 10073
        }
    ],
    "503": [
        {
            "node_id": "6",
            "leak_diameter": 0.18161770682,
            "leak_type": "abrupt",
            "leak_start_time": 16195,
            "leak_end_time": 17355,
            "leak_peak_time": 16195
        }
    ],
    "504": [
        {
            "node_id": "31",
            "leak_diameter": 0.0752191212991,
            "leak_type": "incipient",
            "leak_start_time": 6193,
            "leak_end_time": 8547,
            "leak_peak_time": 7451
        }
    ],
    "505": [
        {
            "node_id": "32",
            "leak_diameter": 0.10861093673,
            "leak_type": "abrupt",
            "leak_start_time": 8569,
            "leak_end_time": 10741,
            "leak_peak_time": 8569
        },
        {
            "node_id": "7",
            "leak_diameter": 0.147319586051,
            "leak_type": "abrupt",
            "leak_start_time": 7115,
            "leak_end_time": 10414,
            "leak_peak_time": 7115
        }
    ],
    "506": [
        {
            "node_id": "22",
            "leak_diameter": 0.0902916424075,
            "leak_type": "abrupt",
            "leak_start_time": 16713,
            "leak_end_time": 16836,
            "leak_peak_time": 16713
        },
        {
            "node_id": "8",
            "leak_diameter": 0.1299962236,
            "leak_type": "incipient",
            "leak_start_time": 1364,
            "leak_end_time": 2422,
            "leak_peak_time": 1748
        }
    ],
    "507": [
        {
            "node_id": "6",
            "leak_diameter": 0.0594911848218,
            "leak_type": "incipient",
            "leak_start_time": 7295,
            "leak_end_time": 13522,
            "leak_peak_time": 13343
        },
        {
            "node_id": "16",
            "leak_diameter": 0.153244752224,
            "leak_type": "incipient",
            "leak_start_time": 14706,
            "leak_end_time": 15512,
            "leak_peak_time": 14748
        }
    ],
    "508": [
        {
            "node_id": "20",
            "leak_diameter": 0.170009579965,
            "leak_type": "abrupt",
            "leak_start_time": 12204,
            "leak_end_time": 12340,
            "leak_peak_time": 12204
        },
        {
            "node_id": "30",
            "leak_diameter": 0.0592201698189,
            "leak_type": "abrupt",
            "leak_start_time": 12483,
            "leak_end_time": 13457,
            "leak_peak_time": 12483
        }
    ],
    "509": [
        {
            "node_id": "10",
            "leak_diameter": 0.180701897699,
            "leak_type": "abrupt",
            "leak_start_time": 14210,
            "leak_end_time": 14244,
            "leak_peak_time": 14210
        },
        {
            "node_id": "16",
            "leak_diameter": 0.151259152432,
            "leak_type": "incipient",
            "leak_start_time": 4250,
            "leak_end_time": 12274,
            "leak_peak_time": 10794
        }
    ],
    "510": [
        {
            "node_id": "28",
            "leak_diameter": 0.104401037312,
            "leak_type": "abrupt",
            "leak_start_time": 14148,
            "leak_end_time": 16710,
            "leak_peak_time": 14148
        }
    ],
    "511": [
        {
            "node_id": "27",
            "leak_diameter": 0.127276512297,
            "leak_type": "incipient",
            "leak_start_time": 14499,
            "leak_end_time": 15026,
            "leak_peak_time": 14856
        }
    ],
    "512": [
        {
            "node_id": "18",
            "leak_diameter": 0.101127141086,
            "leak_type": "abrupt",
            "leak_start_time": 7813,
            "leak_end_time": 14984,
            "leak_peak_time": 7813
        },
        {
            "node_id": "30",
            "leak_diameter": 0.140973757963,
            "leak_type": "incipient",
            "leak_start_time": 8646,
            "leak_end_time": 14424,
            "leak_peak_time": 14359
        }
    ],
    "514": [
        {
            "node_id": "20",
            "leak_diameter": 0.164246687069,
            "leak_type": "incipient",
            "leak_start_time": 5382,
            "leak_end_time": 10317,
            "leak_peak_time": 7989
        }
    ],
    "515": [
        {
            "node_id": "23",
            "leak_diameter": 0.0637845742116,
            "leak_type": "abrupt",
            "leak_start_time": 12600,
            "leak_end_time": 15033,
            "leak_peak_time": 12600
        },
        {
            "node_id": "30",
            "leak_diameter": 0.0433576496709,
            "leak_type": "abrupt",
            "leak_start_time": 9945,
            "leak_end_time": 14565,
            "leak_peak_time": 9945
        }
    ],
    "516": [
        {
            "node_id": "16",
            "leak_diameter": 0.101192074629,
            "leak_type": "incipient",
            "leak_start_time": 11951,
            "leak_end_time": 16236,
            "leak_peak_time": 13535
        }
    ],
    "517": [
        {
            "node_id": "18",
            "leak_diameter": 0.168562556472,
            "leak_type": "abrupt",
            "leak_start_time": 160,
            "leak_end_time": 330,
            "leak_peak_time": 160
        },
        {
            "node_id": "28",
            "leak_diameter": 0.0295305372752,
            "leak_type": "incipient",
            "leak_start_time": 15139,
            "leak_end_time": 16711,
            "leak_peak_time": 15754
        }
    ],
    "518": [
        {
            "node_id": "3",
            "leak_diameter": 0.176140469358,
            "leak_type": "incipient",
            "leak_start_time": 5889,
            "leak_end_time": 13746,
            "leak_peak_time": 9882
        },
        {
            "node_id": "9",
            "leak_diameter": 0.0609819588294,
            "leak_type": "incipient",
            "leak_start_time": 15129,
            "leak_end_time": 16675,
            "leak_peak_time": 15460
        }
    ],
    "519": [
        {
            "node_id": "15",
            "leak_diameter": 0.0939292017202,
            "leak_type": "incipient",
            "leak_start_time": 6309,
            "leak_end_time": 14644,
            "leak_peak_time": 9792
        },
        {
            "node_id": "28",
            "leak_diameter": 0.0247805377227,
            "leak_type": "incipient",
            "leak_start_time": 11079,
            "leak_end_time": 17226,
            "leak_peak_time": 15445
        }
    ],
    "521": [
        {
            "node_id": "22",
            "leak_diameter": 0.165664350913,
            "leak_type": "abrupt",
            "leak_start_time": 15727,
            "leak_end_time": 16598,
            "leak_peak_time": 15727
        }
    ],
    "522": [
        {
            "node_id": "20",
            "leak_diameter": 0.106286354619,
            "leak_type": "incipient",
            "leak_start_time": 7730,
            "leak_end_time": 8738,
            "leak_peak_time": 8333
        },
        {
            "node_id": "31",
            "leak_diameter": 0.101478672148,
            "leak_type": "abrupt",
            "leak_start_time": 12947,
            "leak_end_time": 16471,
            "leak_peak_time": 12947
        }
    ],
    "523": [
        {
            "node_id": "11",
            "leak_diameter": 0.0409973300024,
            "leak_type": "incipient",
            "leak_start_time": 16761,
            "leak_end_time": 17119,
            "leak_peak_time": 16782
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0308925879174,
            "leak_type": "incipient",
            "leak_start_time": 5979,
            "leak_end_time": 9293,
            "leak_peak_time": 6681
        }
    ],
    "524": [
        {
            "node_id": "4",
            "leak_diameter": 0.0803411735419,
            "leak_type": "incipient",
            "leak_start_time": 5904,
            "leak_end_time": 14180,
            "leak_peak_time": 12363
        },
        {
            "node_id": "30",
            "leak_diameter": 0.0386713774565,
            "leak_type": "incipient",
            "leak_start_time": 4462,
            "leak_end_time": 16999,
            "leak_peak_time": 5773
        }
    ],
    "527": [
        {
            "node_id": "5",
            "leak_diameter": 0.0639186684496,
            "leak_type": "abrupt",
            "leak_start_time": 4833,
            "leak_end_time": 10465,
            "leak_peak_time": 4833
        }
    ],
    "529": [
        {
            "node_id": "15",
            "leak_diameter": 0.105185249851,
            "leak_type": "incipient",
            "leak_start_time": 7242,
            "leak_end_time": 10073,
            "leak_peak_time": 9545
        }
    ],
    "530": [
        {
            "node_id": "18",
            "leak_diameter": 0.0698738497787,
            "leak_type": "abrupt",
            "leak_start_time": 16065,
            "leak_end_time": 17107,
            "leak_peak_time": 16065
        }
    ],
    "531": [
        {
            "node_id": "18",
            "leak_diameter": 0.148861925071,
            "leak_type": "incipient",
            "leak_start_time": 908,
            "leak_end_time": 5332,
            "leak_peak_time": 1015
        }
    ],
    "532": [
        {
            "node_id": "6",
            "leak_diameter": 0.0296715221437,
            "leak_type": "incipient",
            "leak_start_time": 14868,
            "leak_end_time": 17100,
            "leak_peak_time": 15035
        },
        {
            "node_id": "17",
            "leak_diameter": 0.0711755034542,
            "leak_type": "incipient",
            "leak_start_time": 5468,
            "leak_end_time": 16575,
            "leak_peak_time": 14166
        }
    ],
    "533": [
        {
            "node_id": "16",
            "leak_diameter": 0.184087576967,
            "leak_type": "abrupt",
            "leak_start_time": 501,
            "leak_end_time": 10645,
            "leak_peak_time": 501
        }
    ],
    "534": [
        {
            "node_id": "4",
            "leak_diameter": 0.197070085618,
            "leak_type": "abrupt",
            "leak_start_time": 992,
            "leak_end_time": 10966,
            "leak_peak_time": 992
        },
        {
            "node_id": "17",
            "leak_diameter": 0.0539420072923,
            "leak_type": "incipient",
            "leak_start_time": 9345,
            "leak_end_time": 9527,
            "leak_peak_time": 9431
        }
    ],
    "536": [
        {
            "node_id": "4",
            "leak_diameter": 0.0210628167241,
            "leak_type": "incipient",
            "leak_start_time": 1762,
            "leak_end_time": 6860,
            "leak_peak_time": 3648
        },
        {
            "node_id": "26",
            "leak_diameter": 0.11097425893,
            "leak_type": "incipient",
            "leak_start_time": 443,
            "leak_end_time": 2998,
            "leak_peak_time": 1144
        }
    ],
    "537": [
        {
            "node_id": "25",
            "leak_diameter": 0.172976805567,
            "leak_type": "incipient",
            "leak_start_time": 3185,
            "leak_end_time": 12293,
            "leak_peak_time": 6219
        }
    ],
    "539": [
        {
            "node_id": "4",
            "leak_diameter": 0.169429773705,
            "leak_type": "incipient",
            "leak_start_time": 4393,
            "leak_end_time": 11039,
            "leak_peak_time": 6385
        }
    ],
    "540": [
        {
            "node_id": "10",
            "leak_diameter": 0.0995171462475,
            "leak_type": "incipient",
            "leak_start_time": 8322,
            "leak_end_time": 10038,
            "leak_peak_time": 9616
        }
    ],
    "541": [
        {
            "node_id": "15",
            "leak_diameter": 0.165615187021,
            "leak_type": "incipient",
            "leak_start_time": 16073,
            "leak_end_time": 16391,
            "leak_peak_time": 16352
        }
    ],
    "542": [
        {
            "node_id": "22",
            "leak_diameter": 0.0487198201555,
            "leak_type": "incipient",
            "leak_start_time": 867,
            "leak_end_time": 4052,
            "leak_peak_time": 1834
        },
        {
            "node_id": "21",
            "leak_diameter": 0.115036731154,
            "leak_type": "incipient",
            "leak_start_time": 174,
            "leak_end_time": 11209,
            "leak_peak_time": 5143
        }
    ],
    "543": [
        {
            "node_id": "22",
            "leak_diameter": 0.114579909206,
            "leak_type": "abrupt",
            "leak_start_time": 2570,
            "leak_end_time": 14335,
            "leak_peak_time": 2570
        }
    ],
    "545": [
        {
            "node_id": "29",
            "leak_diameter": 0.140216393481,
            "leak_type": "incipient",
            "leak_start_time": 9410,
            "leak_end_time": 11706,
            "leak_peak_time": 9998
        }
    ],
    "549": [
        {
            "node_id": "5",
            "leak_diameter": 0.117392134706,
            "leak_type": "abrupt",
            "leak_start_time": 13603,
            "leak_end_time": 17346,
            "leak_peak_time": 13603
        },
        {
            "node_id": "30",
            "leak_diameter": 0.165369627488,
            "leak_type": "abrupt",
            "leak_start_time": 3371,
            "leak_end_time": 10954,
            "leak_peak_time": 3371
        }
    ],
    "552": [
        {
            "node_id": "5",
            "leak_diameter": 0.0898311292032,
            "leak_type": "incipient",
            "leak_start_time": 8430,
            "leak_end_time": 9041,
            "leak_peak_time": 9029
        }
    ],
    "553": [
        {
            "node_id": "19",
            "leak_diameter": 0.118064782123,
            "leak_type": "abrupt",
            "leak_start_time": 6684,
            "leak_end_time": 15851,
            "leak_peak_time": 6684
        },
        {
            "node_id": "13",
            "leak_diameter": 0.191082711872,
            "leak_type": "incipient",
            "leak_start_time": 17087,
            "leak_end_time": 17375,
            "leak_peak_time": 17245
        }
    ],
    "554": [
        {
            "node_id": "20",
            "leak_diameter": 0.11749588455,
            "leak_type": "incipient",
            "leak_start_time": 14102,
            "leak_end_time": 15672,
            "leak_peak_time": 14763
        }
    ],
    "555": [
        {
            "node_id": "27",
            "leak_diameter": 0.167019697401,
            "leak_type": "abrupt",
            "leak_start_time": 7819,
            "leak_end_time": 17276,
            "leak_peak_time": 7819
        }
    ],
    "556": [
        {
            "node_id": "26",
            "leak_diameter": 0.184700408834,
            "leak_type": "abrupt",
            "leak_start_time": 12530,
            "leak_end_time": 14646,
            "leak_peak_time": 12530
        },
        {
            "node_id": "31",
            "leak_diameter": 0.12213592003,
            "leak_type": "abrupt",
            "leak_start_time": 14975,
            "leak_end_time": 15043,
            "leak_peak_time": 14975
        }
    ],
    "557": [
        {
            "node_id": "28",
            "leak_diameter": 0.0923419339443,
            "leak_type": "abrupt",
            "leak_start_time": 1739,
            "leak_end_time": 3316,
            "leak_peak_time": 1739
        },
        {
            "node_id": "9",
            "leak_diameter": 0.13721882357,
            "leak_type": "incipient",
            "leak_start_time": 16933,
            "leak_end_time": 16976,
            "leak_peak_time": 16952
        }
    ],
    "558": [
        {
            "node_id": "19",
            "leak_diameter": 0.14860792086,
            "leak_type": "abrupt",
            "leak_start_time": 7374,
            "leak_end_time": 15957,
            "leak_peak_time": 7374
        }
    ],
    "559": [
        {
            "node_id": "27",
            "leak_diameter": 0.0921204620704,
            "leak_type": "abrupt",
            "leak_start_time": 10720,
            "leak_end_time": 15120,
            "leak_peak_time": 10720
        }
    ],
    "560": [
        {
            "node_id": "6",
            "leak_diameter": 0.140329129198,
            "leak_type": "abrupt",
            "leak_start_time": 8521,
            "leak_end_time": 10143,
            "leak_peak_time": 8521
        }
    ],
    "561": [
        {
            "node_id": "22",
            "leak_diameter": 0.107727554987,
            "leak_type": "incipient",
            "leak_start_time": 1688,
            "leak_end_time": 3920,
            "leak_peak_time": 3619
        }
    ],
    "562": [
        {
            "node_id": "25",
            "leak_diameter": 0.163652139659,
            "leak_type": "incipient",
            "leak_start_time": 17434,
            "leak_end_time": 17479,
            "leak_peak_time": 17459
        }
    ],
    "563": [
        {
            "node_id": "2",
            "leak_diameter": 0.0934684074493,
            "leak_type": "abrupt",
            "leak_start_time": 4265,
            "leak_end_time": 10390,
            "leak_peak_time": 4265
        }
    ],
    "564": [
        {
            "node_id": "3",
            "leak_diameter": 0.0727574067532,
            "leak_type": "incipient",
            "leak_start_time": 10833,
            "leak_end_time": 12074,
            "leak_peak_time": 11124
        }
    ],
    "566": [
        {
            "node_id": "19",
            "leak_diameter": 0.100258832288,
            "leak_type": "abrupt",
            "leak_start_time": 8733,
            "leak_end_time": 14894,
            "leak_peak_time": 8733
        }
    ],
    "567": [
        {
            "node_id": "11",
            "leak_diameter": 0.175208831818,
            "leak_type": "incipient",
            "leak_start_time": 9322,
            "leak_end_time": 10063,
            "leak_peak_time": 9597
        },
        {
            "node_id": "32",
            "leak_diameter": 0.0771426805891,
            "leak_type": "incipient",
            "leak_start_time": 4328,
            "leak_end_time": 14017,
            "leak_peak_time": 5835
        }
    ],
    "569": [
        {
            "node_id": "22",
            "leak_diameter": 0.178962759179,
            "leak_type": "abrupt",
            "leak_start_time": 1712,
            "leak_end_time": 11235,
            "leak_peak_time": 1712
        }
    ],
    "570": [
        {
            "node_id": "20",
            "leak_diameter": 0.179220107476,
            "leak_type": "abrupt",
            "leak_start_time": 10731,
            "leak_end_time": 16432,
            "leak_peak_time": 10731
        },
        {
            "node_id": "30",
            "leak_diameter": 0.0453649845942,
            "leak_type": "abrupt",
            "leak_start_time": 16387,
            "leak_end_time": 17251,
            "leak_peak_time": 16387
        }
    ],
    "571": [
        {
            "node_id": "15",
            "leak_diameter": 0.0943898459068,
            "leak_type": "incipient",
            "leak_start_time": 11316,
            "leak_end_time": 12078,
            "leak_peak_time": 11934
        }
    ],
    "573": [
        {
            "node_id": "4",
            "leak_diameter": 0.0607303296973,
            "leak_type": "abrupt",
            "leak_start_time": 7049,
            "leak_end_time": 11896,
            "leak_peak_time": 7049
        },
        {
            "node_id": "13",
            "leak_diameter": 0.0252074741797,
            "leak_type": "incipient",
            "leak_start_time": 3423,
            "leak_end_time": 5229,
            "leak_peak_time": 4797
        }
    ],
    "574": [
        {
            "node_id": "22",
            "leak_diameter": 0.0690120890192,
            "leak_type": "incipient",
            "leak_start_time": 4609,
            "leak_end_time": 12863,
            "leak_peak_time": 8335
        },
        {
            "node_id": "28",
            "leak_diameter": 0.121926714364,
            "leak_type": "incipient",
            "leak_start_time": 622,
            "leak_end_time": 8843,
            "leak_peak_time": 7190
        }
    ],
    "575": [
        {
            "node_id": "20",
            "leak_diameter": 0.0827857037975,
            "leak_type": "abrupt",
            "leak_start_time": 6479,
            "leak_end_time": 8897,
            "leak_peak_time": 6479
        },
        {
            "node_id": "9",
            "leak_diameter": 0.151610445022,
            "leak_type": "abrupt",
            "leak_start_time": 6343,
            "leak_end_time": 7078,
            "leak_peak_time": 6343
        }
    ],
    "576": [
        {
            "node_id": "19",
            "leak_diameter": 0.034176192581,
            "leak_type": "abrupt",
            "leak_start_time": 5910,
            "leak_end_time": 12031,
            "leak_peak_time": 5910
        }
    ],
    "577": [
        {
            "node_id": "20",
            "leak_diameter": 0.180731087774,
            "leak_type": "abrupt",
            "leak_start_time": 9773,
            "leak_end_time": 14535,
            "leak_peak_time": 9773
        }
    ],
    "579": [
        {
            "node_id": "19",
            "leak_diameter": 0.0762399699714,
            "leak_type": "abrupt",
            "leak_start_time": 5567,
            "leak_end_time": 9972,
            "leak_peak_time": 5567
        }
    ],
    "580": [
        {
            "node_id": "10",
            "leak_diameter": 0.199776081913,
            "leak_type": "abrupt",
            "leak_start_time": 14450,
            "leak_end_time": 15349,
            "leak_peak_time": 14450
        }
    ],
    "581": [
        {
            "node_id": "4",
            "leak_diameter": 0.0808374721875,
            "leak_type": "incipient",
            "leak_start_time": 5257,
            "leak_end_time": 6899,
            "leak_peak_time": 5926
        },
        {
            "node_id": "30",
            "leak_diameter": 0.100771385348,
            "leak_type": "incipient",
            "leak_start_time": 15628,
            "leak_end_time": 16570,
            "leak_peak_time": 16442
        }
    ],
    "582": [
        {
            "node_id": "7",
            "leak_diameter": 0.0425244829367,
            "leak_type": "incipient",
            "leak_start_time": 17281,
            "leak_end_time": 17338,
            "leak_peak_time": 17320
        }
    ],
    "583": [
        {
            "node_id": "22",
            "leak_diameter": 0.0801873501724,
            "leak_type": "abrupt",
            "leak_start_time": 6446,
            "leak_end_time": 13847,
            "leak_peak_time": 6446
        }
    ],
    "585": [
        {
            "node_id": "21",
            "leak_diameter": 0.0639618835267,
            "leak_type": "abrupt",
            "leak_start_time": 2492,
            "leak_end_time": 11908,
            "leak_peak_time": 2492
        },
        {
            "node_id": "14",
            "leak_diameter": 0.15857432511,
            "leak_type": "incipient",
            "leak_start_time": 9198,
            "leak_end_time": 11266,
            "leak_peak_time": 11152
        }
    ],
    "586": [
        {
            "node_id": "2",
            "leak_diameter": 0.0772260770603,
            "leak_type": "abrupt",
            "leak_start_time": 15682,
            "leak_end_time": 17118,
            "leak_peak_time": 15682
        }
    ],
    "587": [
        {
            "node_id": "4",
            "leak_diameter": 0.0431635791643,
            "leak_type": "incipient",
            "leak_start_time": 8867,
            "leak_end_time": 12776,
            "leak_peak_time": 11277
        }
    ],
    "588": [
        {
            "node_id": "18",
            "leak_diameter": 0.0478556835305,
            "leak_type": "incipient",
            "leak_start_time": 1644,
            "leak_end_time": 8584,
            "leak_peak_time": 2827
        },
        {
            "node_id": "14",
            "leak_diameter": 0.129589623173,
            "leak_type": "incipient",
            "leak_start_time": 13655,
            "leak_end_time": 15242,
            "leak_peak_time": 14088
        }
    ],
    "590": [
        {
            "node_id": "29",
            "leak_diameter": 0.189237529214,
            "leak_type": "abrupt",
            "leak_start_time": 1031,
            "leak_end_time": 10411,
            "leak_peak_time": 1031
        }
    ],
    "592": [
        {
            "node_id": "21",
            "leak_diameter": 0.0692290157477,
            "leak_type": "abrupt",
            "leak_start_time": 15492,
            "leak_end_time": 16224,
            "leak_peak_time": 15492
        }
    ],
    "593": [
        {
            "node_id": "20",
            "leak_diameter": 0.191752387558,
            "leak_type": "incipient",
            "leak_start_time": 4090,
            "leak_end_time": 5339,
            "leak_peak_time": 4384
        }
    ],
    "595": [
        {
            "node_id": "12",
            "leak_diameter": 0.135806879149,
            "leak_type": "incipient",
            "leak_start_time": 7687,
            "leak_end_time": 9069,
            "leak_peak_time": 7828
        },
        {
            "node_id": "14",
            "leak_diameter": 0.18422905383,
            "leak_type": "incipient",
            "leak_start_time": 13857,
            "leak_end_time": 15661,
            "leak_peak_time": 15532
        }
    ],
    "596": [
        {
            "node_id": "30",
            "leak_diameter": 0.129803666422,
            "leak_type": "abrupt",
            "leak_start_time": 11186,
            "leak_end_time": 11274,
            "leak_peak_time": 11186
        }
    ],
    "597": [
        {
            "node_id": "27",
            "leak_diameter": 0.170312003813,
            "leak_type": "incipient",
            "leak_start_time": 7789,
            "leak_end_time": 9668,
            "leak_peak_time": 9319
        }
    ],
    "598": [
        {
            "node_id": "21",
            "leak_diameter": 0.159195653789,
            "leak_type": "incipient",
            "leak_start_time": 11175,
            "leak_end_time": 15492,
            "leak_peak_time": 14049
        },
        {
            "node_id": "7",
            "leak_diameter": 0.109056635604,
            "leak_type": "incipient",
            "leak_start_time": 242,
            "leak_end_time": 14053,
            "leak_peak_time": 9948
        }
    ],
    "599": [
        {
            "node_id": "14",
            "leak_diameter": 0.0222630066282,
            "leak_type": "abrupt",
            "leak_start_time": 6413,
            "leak_end_time": 15171,
            "leak_peak_time": 6413
        }
    ],
    "601": [
        {
            "node_id": "16",
            "leak_diameter": 0.0739095172337,
            "leak_type": "abrupt",
            "leak_start_time": 15227,
            "leak_end_time": 15412,
            "leak_peak_time": 15227
        }
    ],
    "602": [
        {
            "node_id": "25",
            "leak_diameter": 0.0555607941128,
            "leak_type": "abrupt",
            "leak_start_time": 12050,
            "leak_end_time": 13172,
            "leak_peak_time": 12050
        }
    ],
    "603": [
        {
            "node_id": "15",
            "leak_diameter": 0.125775411437,
            "leak_type": "abrupt",
            "leak_start_time": 12676,
            "leak_end_time": 14800,
            "leak_peak_time": 12676
        }
    ],
    "604": [
        {
            "node_id": "21",
            "leak_diameter": 0.186016545475,
            "leak_type": "incipient",
            "leak_start_time": 4297,
            "leak_end_time": 17243,
            "leak_peak_time": 5501
        }
    ],
    "605": [
        {
            "node_id": "10",
            "leak_diameter": 0.115429521592,
            "leak_type": "abrupt",
            "leak_start_time": 12182,
            "leak_end_time": 12366,
            "leak_peak_time": 12182
        },
        {
            "node_id": "14",
            "leak_diameter": 0.149268934981,
            "leak_type": "incipient",
            "leak_start_time": 14978,
            "leak_end_time": 16670,
            "leak_peak_time": 15185
        }
    ],
    "606": [
        {
            "node_id": "29",
            "leak_diameter": 0.121648288864,
            "leak_type": "abrupt",
            "leak_start_time": 13032,
            "leak_end_time": 15740,
            "leak_peak_time": 13032
        }
    ],
    "607": [
        {
            "node_id": "4",
            "leak_diameter": 0.0454775987375,
            "leak_type": "incipient",
            "leak_start_time": 15146,
            "leak_end_time": 15829,
            "leak_peak_time": 15740
        },
        {
            "node_id": "14",
            "leak_diameter": 0.15136653491,
            "leak_type": "incipient",
            "leak_start_time": 5032,
            "leak_end_time": 9073,
            "leak_peak_time": 7564
        }
    ],
    "608": [
        {
            "node_id": "22",
            "leak_diameter": 0.158970240312,
            "leak_type": "abrupt",
            "leak_start_time": 4588,
            "leak_end_time": 15324,
            "leak_peak_time": 4588
        },
        {
            "node_id": "31",
            "leak_diameter": 0.173972515661,
            "leak_type": "incipient",
            "leak_start_time": 6168,
            "leak_end_time": 11230,
            "leak_peak_time": 9679
        }
    ],
    "609": [
        {
            "node_id": "27",
            "leak_diameter": 0.198457937623,
            "leak_type": "abrupt",
            "leak_start_time": 1953,
            "leak_end_time": 7640,
            "leak_peak_time": 1953
        }
    ],
    "610": [
        {
            "node_id": "17",
            "leak_diameter": 0.0861731459031,
            "leak_type": "abrupt",
            "leak_start_time": 7048,
            "leak_end_time": 13313,
            "leak_peak_time": 7048
        }
    ],
    "611": [
        {
            "node_id": "16",
            "leak_diameter": 0.0236885676401,
            "leak_type": "abrupt",
            "leak_start_time": 14008,
            "leak_end_time": 16687,
            "leak_peak_time": 14008
        }
    ],
    "612": [
        {
            "node_id": "19",
            "leak_diameter": 0.0829313238048,
            "leak_type": "incipient",
            "leak_start_time": 10304,
            "leak_end_time": 14176,
            "leak_peak_time": 13303
        }
    ],
    "613": [
        {
            "node_id": "12",
            "leak_diameter": 0.120944126758,
            "leak_type": "abrupt",
            "leak_start_time": 16715,
            "leak_end_time": 17317,
            "leak_peak_time": 16715
        },
        {
            "node_id": "30",
            "leak_diameter": 0.0721658457876,
            "leak_type": "incipient",
            "leak_start_time": 7278,
            "leak_end_time": 10105,
            "leak_peak_time": 9758
        }
    ],
    "615": [
        {
            "node_id": "23",
            "leak_diameter": 0.0800413735082,
            "leak_type": "abrupt",
            "leak_start_time": 7170,
            "leak_end_time": 14840,
            "leak_peak_time": 7170
        }
    ],
    "617": [
        {
            "node_id": "25",
            "leak_diameter": 0.194085962739,
            "leak_type": "abrupt",
            "leak_start_time": 5123,
            "leak_end_time": 6693,
            "leak_peak_time": 5123
        }
    ],
    "618": [
        {
            "node_id": "19",
            "leak_diameter": 0.156791326072,
            "leak_type": "abrupt",
            "leak_start_time": 5190,
            "leak_end_time": 13127,
            "leak_peak_time": 5190
        },
        {
            "node_id": "7",
            "leak_diameter": 0.136756114429,
            "leak_type": "abrupt",
            "leak_start_time": 9629,
            "leak_end_time": 11179,
            "leak_peak_time": 9629
        }
    ],
    "619": [
        {
            "node_id": "11",
            "leak_diameter": 0.113876720742,
            "leak_type": "incipient",
            "leak_start_time": 8212,
            "leak_end_time": 16920,
            "leak_peak_time": 8905
        }
    ],
    "620": [
        {
            "node_id": "17",
            "leak_diameter": 0.0815490623123,
            "leak_type": "incipient",
            "leak_start_time": 14202,
            "leak_end_time": 14587,
            "leak_peak_time": 14294
        }
    ],
    "621": [
        {
            "node_id": "15",
            "leak_diameter": 0.0447188887475,
            "leak_type": "incipient",
            "leak_start_time": 2137,
            "leak_end_time": 2625,
            "leak_peak_time": 2320
        }
    ],
    "623": [
        {
            "node_id": "23",
            "leak_diameter": 0.118400961059,
            "leak_type": "abrupt",
            "leak_start_time": 11990,
            "leak_end_time": 13217,
            "leak_peak_time": 11990
        }
    ],
    "625": [
        {
            "node_id": "8",
            "leak_diameter": 0.128316742658,
            "leak_type": "incipient",
            "leak_start_time": 11388,
            "leak_end_time": 11654,
            "leak_peak_time": 11402
        }
    ],
    "626": [
        {
            "node_id": "15",
            "leak_diameter": 0.0397907170216,
            "leak_type": "abrupt",
            "leak_start_time": 16739,
            "leak_end_time": 17053,
            "leak_peak_time": 16739
        }
    ],
    "627": [
        {
            "node_id": "19",
            "leak_diameter": 0.068804757403,
            "leak_type": "abrupt",
            "leak_start_time": 6617,
            "leak_end_time": 16504,
            "leak_peak_time": 6617
        },
        {
            "node_id": "31",
            "leak_diameter": 0.102243710206,
            "leak_type": "incipient",
            "leak_start_time": 7262,
            "leak_end_time": 17112,
            "leak_peak_time": 8372
        }
    ],
    "628": [
        {
            "node_id": "18",
            "leak_diameter": 0.104521376012,
            "leak_type": "abrupt",
            "leak_start_time": 15693,
            "leak_end_time": 16292,
            "leak_peak_time": 15693
        }
    ],
    "629": [
        {
            "node_id": "13",
            "leak_diameter": 0.185579248653,
            "leak_type": "incipient",
            "leak_start_time": 10728,
            "leak_end_time": 15206,
            "leak_peak_time": 12259
        }
    ],
    "630": [
        {
            "node_id": "18",
            "leak_diameter": 0.119347416583,
            "leak_type": "abrupt",
            "leak_start_time": 10419,
            "leak_end_time": 11720,
            "leak_peak_time": 10419
        }
    ],
    "631": [
        {
            "node_id": "19",
            "leak_diameter": 0.0960135682247,
            "leak_type": "abrupt",
            "leak_start_time": 1575,
            "leak_end_time": 10952,
            "leak_peak_time": 1575
        }
    ],
    "632": [
        {
            "node_id": "23",
            "leak_diameter": 0.0566056053959,
            "leak_type": "incipient",
            "leak_start_time": 15945,
            "leak_end_time": 16701,
            "leak_peak_time": 16320
        }
    ],
    "635": [
        {
            "node_id": "13",
            "leak_diameter": 0.179019876236,
            "leak_type": "abrupt",
            "leak_start_time": 14237,
            "leak_end_time": 15779,
            "leak_peak_time": 14237
        }
    ],
    "638": [
        {
            "node_id": "21",
            "leak_diameter": 0.1066216336,
            "leak_type": "abrupt",
            "leak_start_time": 2904,
            "leak_end_time": 4884,
            "leak_peak_time": 2904
        },
        {
            "node_id": "7",
            "leak_diameter": 0.0846063817832,
            "leak_type": "incipient",
            "leak_start_time": 6519,
            "leak_end_time": 12053,
            "leak_peak_time": 10087
        }
    ],
    "641": [
        {
            "node_id": "31",
            "leak_diameter": 0.0604410885354,
            "leak_type": "abrupt",
            "leak_start_time": 10887,
            "leak_end_time": 10913,
            "leak_peak_time": 10887
        }
    ],
    "642": [
        {
            "node_id": "27",
            "leak_diameter": 0.109823746369,
            "leak_type": "abrupt",
            "leak_start_time": 15838,
            "leak_end_time": 17314,
            "leak_peak_time": 15838
        },
        {
            "node_id": "11",
            "leak_diameter": 0.139221210469,
            "leak_type": "abrupt",
            "leak_start_time": 14847,
            "leak_end_time": 15084,
            "leak_peak_time": 14847
        }
    ],
    "643": [
        {
            "node_id": "13",
            "leak_diameter": 0.0270894002397,
            "leak_type": "abrupt",
            "leak_start_time": 15771,
            "leak_end_time": 17048,
            "leak_peak_time": 15771
        },
        {
            "node_id": "9",
            "leak_diameter": 0.0664494907481,
            "leak_type": "abrupt",
            "leak_start_time": 1919,
            "leak_end_time": 9591,
            "leak_peak_time": 1919
        }
    ],
    "644": [
        {
            "node_id": "11",
            "leak_diameter": 0.143680147379,
            "leak_type": "incipient",
            "leak_start_time": 13741,
            "leak_end_time": 16953,
            "leak_peak_time": 15427
        },
        {
            "node_id": "2",
            "leak_diameter": 0.0999143868373,
            "leak_type": "incipient",
            "leak_start_time": 11959,
            "leak_end_time": 13709,
            "leak_peak_time": 12374
        }
    ],
    "645": [
        {
            "node_id": "15",
            "leak_diameter": 0.108949034883,
            "leak_type": "abrupt",
            "leak_start_time": 16754,
            "leak_end_time": 17093,
            "leak_peak_time": 16754
        }
    ],
    "646": [
        {
            "node_id": "11",
            "leak_diameter": 0.0422415046533,
            "leak_type": "incipient",
            "leak_start_time": 15170,
            "leak_end_time": 16530,
            "leak_peak_time": 15933
        }
    ],
    "647": [
        {
            "node_id": "22",
            "leak_diameter": 0.0820189315056,
            "leak_type": "incipient",
            "leak_start_time": 4768,
            "leak_end_time": 12496,
            "leak_peak_time": 5117
        },
        {
            "node_id": "13",
            "leak_diameter": 0.0856642880277,
            "leak_type": "incipient",
            "leak_start_time": 11911,
            "leak_end_time": 13264,
            "leak_peak_time": 12256
        }
    ],
    "648": [
        {
            "node_id": "9",
            "leak_diameter": 0.0235719730825,
            "leak_type": "incipient",
            "leak_start_time": 15765,
            "leak_end_time": 17335,
            "leak_peak_time": 16231
        }
    ],
    "649": [
        {
            "node_id": "27",
            "leak_diameter": 0.0442718927261,
            "leak_type": "abrupt",
            "leak_start_time": 1993,
            "leak_end_time": 9331,
            "leak_peak_time": 1993
        }
    ],
    "650": [
        {
            "node_id": "4",
            "leak_diameter": 0.0983048988915,
            "leak_type": "abrupt",
            "leak_start_time": 16154,
            "leak_end_time": 16461,
            "leak_peak_time": 16154
        },
        {
            "node_id": "21",
            "leak_diameter": 0.0945896691713,
            "leak_type": "abrupt",
            "leak_start_time": 15018,
            "leak_end_time": 15385,
            "leak_peak_time": 15018
        }
    ],
    "652": [
        {
            "node_id": "7",
            "leak_diameter": 0.166341341659,
            "leak_type": "abrupt",
            "leak_start_time": 17210,
            "leak_end_time": 17438,
            "leak_peak_time": 17210
        }
    ],
    "653": [
        {
            "node_id": "31",
            "leak_diameter": 0.153367111074,
            "leak_type": "incipient",
            "leak_start_time": 9671,
            "leak_end_time": 16329,
            "leak_peak_time": 11307
        }
    ],
    "654": [
        {
            "node_id": "20",
            "leak_diameter": 0.177918352041,
            "leak_type": "abrupt",
            "leak_start_time": 13584,
            "leak_end_time": 14490,
            "leak_peak_time": 13584
        },
        {
            "node_id": "16",
            "leak_diameter": 0.136488092845,
            "leak_type": "incipient",
            "leak_start_time": 13892,
            "leak_end_time": 16859,
            "leak_peak_time": 16519
        }
    ],
    "656": [
        {
            "node_id": "8",
            "leak_diameter": 0.0353181395485,
            "leak_type": "incipient",
            "leak_start_time": 6882,
            "leak_end_time": 10789,
            "leak_peak_time": 8491
        }
    ],
    "657": [
        {
            "node_id": "27",
            "leak_diameter": 0.108335367119,
            "leak_type": "abrupt",
            "leak_start_time": 2577,
            "leak_end_time": 12894,
            "leak_peak_time": 2577
        }
    ],
    "658": [
        {
            "node_id": "10",
            "leak_diameter": 0.0545780641822,
            "leak_type": "incipient",
            "leak_start_time": 13538,
            "leak_end_time": 13549,
            "leak_peak_time": 13541
        }
    ],
    "659": [
        {
            "node_id": "21",
            "leak_diameter": 0.105551379517,
            "leak_type": "incipient",
            "leak_start_time": 6170,
            "leak_end_time": 15885,
            "leak_peak_time": 6895
        }
    ],
    "660": [
        {
            "node_id": "30",
            "leak_diameter": 0.0875901663959,
            "leak_type": "incipient",
            "leak_start_time": 2244,
            "leak_end_time": 11875,
            "leak_peak_time": 5640
        }
    ],
    "661": [
        {
            "node_id": "22",
            "leak_diameter": 0.0249782511228,
            "leak_type": "abrupt",
            "leak_start_time": 977,
            "leak_end_time": 2709,
            "leak_peak_time": 977
        },
        {
            "node_id": "12",
            "leak_diameter": 0.135160642985,
            "leak_type": "incipient",
            "leak_start_time": 16385,
            "leak_end_time": 16725,
            "leak_peak_time": 16505
        }
    ],
    "662": [
        {
            "node_id": "12",
            "leak_diameter": 0.0738739222963,
            "leak_type": "incipient",
            "leak_start_time": 2813,
            "leak_end_time": 14215,
            "leak_peak_time": 12611
        }
    ],
    "663": [
        {
            "node_id": "10",
            "leak_diameter": 0.140006054136,
            "leak_type": "abrupt",
            "leak_start_time": 7652,
            "leak_end_time": 9911,
            "leak_peak_time": 7652
        },
        {
            "node_id": "6",
            "leak_diameter": 0.135339657775,
            "leak_type": "abrupt",
            "leak_start_time": 9330,
            "leak_end_time": 12991,
            "leak_peak_time": 9330
        }
    ],
    "664": [
        {
            "node_id": "14",
            "leak_diameter": 0.0376221375749,
            "leak_type": "abrupt",
            "leak_start_time": 14359,
            "leak_end_time": 14524,
            "leak_peak_time": 14359
        },
        {
            "node_id": "28",
            "leak_diameter": 0.0596634508048,
            "leak_type": "incipient",
            "leak_start_time": 13692,
            "leak_end_time": 16524,
            "leak_peak_time": 15356
        }
    ],
    "665": [
        {
            "node_id": "6",
            "leak_diameter": 0.0865835554408,
            "leak_type": "incipient",
            "leak_start_time": 2082,
            "leak_end_time": 3852,
            "leak_peak_time": 3101
        }
    ],
    "666": [
        {
            "node_id": "21",
            "leak_diameter": 0.11021077591,
            "leak_type": "incipient",
            "leak_start_time": 2756,
            "leak_end_time": 7524,
            "leak_peak_time": 2830
        },
        {
            "node_id": "2",
            "leak_diameter": 0.174795800264,
            "leak_type": "abrupt",
            "leak_start_time": 4709,
            "leak_end_time": 7221,
            "leak_peak_time": 4709
        }
    ],
    "667": [
        {
            "node_id": "7",
            "leak_diameter": 0.111282128951,
            "leak_type": "abrupt",
            "leak_start_time": 14366,
            "leak_end_time": 14521,
            "leak_peak_time": 14366
        }
    ],
    "668": [
        {
            "node_id": "29",
            "leak_diameter": 0.12888152574,
            "leak_type": "incipient",
            "leak_start_time": 14059,
            "leak_end_time": 15317,
            "leak_peak_time": 15008
        }
    ],
    "669": [
        {
            "node_id": "18",
            "leak_diameter": 0.169507880134,
            "leak_type": "abrupt",
            "leak_start_time": 831,
            "leak_end_time": 9217,
            "leak_peak_time": 831
        }
    ],
    "670": [
        {
            "node_id": "13",
            "leak_diameter": 0.153448795881,
            "leak_type": "abrupt",
            "leak_start_time": 11811,
            "leak_end_time": 16414,
            "leak_peak_time": 11811
        },
        {
            "node_id": "7",
            "leak_diameter": 0.192945668962,
            "leak_type": "abrupt",
            "leak_start_time": 8792,
            "leak_end_time": 10829,
            "leak_peak_time": 8792
        }
    ],
    "671": [
        {
            "node_id": "15",
            "leak_diameter": 0.170107787565,
            "leak_type": "incipient",
            "leak_start_time": 1532,
            "leak_end_time": 5947,
            "leak_peak_time": 3899
        },
        {
            "node_id": "29",
            "leak_diameter": 0.060083127536,
            "leak_type": "abrupt",
            "leak_start_time": 11206,
            "leak_end_time": 13432,
            "leak_peak_time": 11206
        }
    ],
    "672": [
        {
            "node_id": "32",
            "leak_diameter": 0.138578304068,
            "leak_type": "incipient",
            "leak_start_time": 13861,
            "leak_end_time": 15343,
            "leak_peak_time": 14550
        }
    ],
    "674": [
        {
            "node_id": "7",
            "leak_diameter": 0.158453625564,
            "leak_type": "incipient",
            "leak_start_time": 11925,
            "leak_end_time": 13766,
            "leak_peak_time": 13359
        }
    ],
    "675": [
        {
            "node_id": "29",
            "leak_diameter": 0.111732321511,
            "leak_type": "abrupt",
            "leak_start_time": 7336,
            "leak_end_time": 15148,
            "leak_peak_time": 7336
        }
    ],
    "676": [
        {
            "node_id": "12",
            "leak_diameter": 0.197316336033,
            "leak_type": "abrupt",
            "leak_start_time": 4529,
            "leak_end_time": 15570,
            "leak_peak_time": 4529
        }
    ],
    "677": [
        {
            "node_id": "2",
            "leak_diameter": 0.115355140507,
            "leak_type": "incipient",
            "leak_start_time": 5239,
            "leak_end_time": 16705,
            "leak_peak_time": 12813
        },
        {
            "node_id": "26",
            "leak_diameter": 0.02702594404,
            "leak_type": "incipient",
            "leak_start_time": 15255,
            "leak_end_time": 16249,
            "leak_peak_time": 16034
        }
    ],
    "678": [
        {
            "node_id": "6",
            "leak_diameter": 0.111124829998,
            "leak_type": "incipient",
            "leak_start_time": 5494,
            "leak_end_time": 15982,
            "leak_peak_time": 9002
        },
        {
            "node_id": "15",
            "leak_diameter": 0.138603828653,
            "leak_type": "incipient",
            "leak_start_time": 16428,
            "leak_end_time": 16704,
            "leak_peak_time": 16494
        }
    ],
    "679": [
        {
            "node_id": "9",
            "leak_diameter": 0.151739911729,
            "leak_type": "abrupt",
            "leak_start_time": 8911,
            "leak_end_time": 9253,
            "leak_peak_time": 8911
        }
    ],
    "680": [
        {
            "node_id": "25",
            "leak_diameter": 0.033595870262,
            "leak_type": "incipient",
            "leak_start_time": 13392,
            "leak_end_time": 15364,
            "leak_peak_time": 13796
        },
        {
            "node_id": "30",
            "leak_diameter": 0.0783331577266,
            "leak_type": "incipient",
            "leak_start_time": 17291,
            "leak_end_time": 17476,
            "leak_peak_time": 17369
        }
    ],
    "681": [
        {
            "node_id": "8",
            "leak_diameter": 0.103350360141,
            "leak_type": "incipient",
            "leak_start_time": 12711,
            "leak_end_time": 14797,
            "leak_peak_time": 14233
        }
    ],
    "683": [
        {
            "node_id": "22",
            "leak_diameter": 0.0504212915329,
            "leak_type": "abrupt",
            "leak_start_time": 5715,
            "leak_end_time": 12253,
            "leak_peak_time": 5715
        }
    ],
    "684": [
        {
            "node_id": "19",
            "leak_diameter": 0.180296421533,
            "leak_type": "abrupt",
            "leak_start_time": 15464,
            "leak_end_time": 16099,
            "leak_peak_time": 15464
        }
    ],
    "685": [
        {
            "node_id": "13",
            "leak_diameter": 0.171153238821,
            "leak_type": "abrupt",
            "leak_start_time": 9966,
            "leak_end_time": 14359,
            "leak_peak_time": 9966
        },
        {
            "node_id": "9",
            "leak_diameter": 0.0813159795006,
            "leak_type": "abrupt",
            "leak_start_time": 10677,
            "leak_end_time": 16770,
            "leak_peak_time": 10677
        }
    ],
    "686": [
        {
            "node_id": "28",
            "leak_diameter": 0.132919330799,
            "leak_type": "abrupt",
            "leak_start_time": 2683,
            "leak_end_time": 7672,
            "leak_peak_time": 2683
        }
    ],
    "687": [
        {
            "node_id": "7",
            "leak_diameter": 0.0401933204536,
            "leak_type": "incipient",
            "leak_start_time": 2718,
            "leak_end_time": 9143,
            "leak_peak_time": 6843
        }
    ],
    "688": [
        {
            "node_id": "3",
            "leak_diameter": 0.0369652636587,
            "leak_type": "incipient",
            "leak_start_time": 11853,
            "leak_end_time": 12539,
            "leak_peak_time": 12534
        },
        {
            "node_id": "13",
            "leak_diameter": 0.10372862594,
            "leak_type": "incipient",
            "leak_start_time": 11151,
            "leak_end_time": 14154,
            "leak_peak_time": 13853
        }
    ],
    "690": [
        {
            "node_id": "5",
            "leak_diameter": 0.170584471039,
            "leak_type": "abrupt",
            "leak_start_time": 15763,
            "leak_end_time": 16699,
            "leak_peak_time": 15763
        }
    ],
    "691": [
        {
            "node_id": "18",
            "leak_diameter": 0.111332964477,
            "leak_type": "abrupt",
            "leak_start_time": 4421,
            "leak_end_time": 13297,
            "leak_peak_time": 4421
        }
    ],
    "692": [
        {
            "node_id": "22",
            "leak_diameter": 0.120547311843,
            "leak_type": "incipient",
            "leak_start_time": 10008,
            "leak_end_time": 13444,
            "leak_peak_time": 12379
        }
    ],
    "695": [
        {
            "node_id": "5",
            "leak_diameter": 0.112883105102,
            "leak_type": "incipient",
            "leak_start_time": 12981,
            "leak_end_time": 16034,
            "leak_peak_time": 14912
        }
    ],
    "698": [
        {
            "node_id": "29",
            "leak_diameter": 0.0417208775267,
            "leak_type": "abrupt",
            "leak_start_time": 13526,
            "leak_end_time": 15949,
            "leak_peak_time": 13526
        }
    ],
    "699": [
        {
            "node_id": "18",
            "leak_diameter": 0.191488074171,
            "leak_type": "abrupt",
            "leak_start_time": 3588,
            "leak_end_time": 11903,
            "leak_peak_time": 3588
        }
    ],
    "700": [
        {
            "node_id": "12",
            "leak_diameter": 0.0831737068921,
            "leak_type": "incipient",
            "leak_start_time": 8939,
            "leak_end_time": 17302,
            "leak_peak_time": 15005
        }
    ],
    "701": [
        {
            "node_id": "5",
            "leak_diameter": 0.0218872561045,
            "leak_type": "incipient",
            "leak_start_time": 14253,
            "leak_end_time": 14499,
            "leak_peak_time": 14310
        }
    ],
    "702": [
        {
            "node_id": "23",
            "leak_diameter": 0.131391780319,
            "leak_type": "incipient",
            "leak_start_time": 16492,
            "leak_end_time": 17139,
            "leak_peak_time": 16658
        },
        {
            "node_id": "28",
            "leak_diameter": 0.0536788417777,
            "leak_type": "incipient",
            "leak_start_time": 5421,
            "leak_end_time": 13585,
            "leak_peak_time": 7551
        }
    ],
    "704": [
        {
            "node_id": "27",
            "leak_diameter": 0.14880985405,
            "leak_type": "abrupt",
            "leak_start_time": 12213,
            "leak_end_time": 13772,
            "leak_peak_time": 12213
        },
        {
            "node_id": "32",
            "leak_diameter": 0.11951184474,
            "leak_type": "incipient",
            "leak_start_time": 9237,
            "leak_end_time": 14125,
            "leak_peak_time": 11335
        }
    ],
    "705": [
        {
            "node_id": "12",
            "leak_diameter": 0.1078913547,
            "leak_type": "abrupt",
            "leak_start_time": 13574,
            "leak_end_time": 16268,
            "leak_peak_time": 13574
        }
    ],
    "707": [
        {
            "node_id": "31",
            "leak_diameter": 0.0575581880063,
            "leak_type": "abrupt",
            "leak_start_time": 8206,
            "leak_end_time": 11582,
            "leak_peak_time": 8206
        }
    ],
    "708": [
        {
            "node_id": "21",
            "leak_diameter": 0.0512491316686,
            "leak_type": "incipient",
            "leak_start_time": 1563,
            "leak_end_time": 16905,
            "leak_peak_time": 5233
        }
    ],
    "709": [
        {
            "node_id": "23",
            "leak_diameter": 0.0867307466272,
            "leak_type": "incipient",
            "leak_start_time": 5956,
            "leak_end_time": 11935,
            "leak_peak_time": 6596
        }
    ],
    "711": [
        {
            "node_id": "29",
            "leak_diameter": 0.127336965645,
            "leak_type": "incipient",
            "leak_start_time": 13337,
            "leak_end_time": 13386,
            "leak_peak_time": 13381
        },
        {
            "node_id": "7",
            "leak_diameter": 0.0267626426855,
            "leak_type": "abrupt",
            "leak_start_time": 6287,
            "leak_end_time": 9143,
            "leak_peak_time": 6287
        }
    ],
    "712": [
        {
            "node_id": "6",
            "leak_diameter": 0.159583874076,
            "leak_type": "incipient",
            "leak_start_time": 9705,
            "leak_end_time": 15178,
            "leak_peak_time": 10949
        }
    ],
    "713": [
        {
            "node_id": "5",
            "leak_diameter": 0.13507185759,
            "leak_type": "incipient",
            "leak_start_time": 1512,
            "leak_end_time": 13042,
            "leak_peak_time": 4757
        }
    ],
    "714": [
        {
            "node_id": "28",
            "leak_diameter": 0.115751002383,
            "leak_type": "incipient",
            "leak_start_time": 15386,
            "leak_end_time": 17196,
            "leak_peak_time": 17029
        },
        {
            "node_id": "7",
            "leak_diameter": 0.0324017665407,
            "leak_type": "incipient",
            "leak_start_time": 17182,
            "leak_end_time": 17364,
            "leak_peak_time": 17340
        }
    ],
    "716": [
        {
            "node_id": "25",
            "leak_diameter": 0.0636810013656,
            "leak_type": "abrupt",
            "leak_start_time": 5676,
            "leak_end_time": 7605,
            "leak_peak_time": 5676
        }
    ],
    "717": [
        {
            "node_id": "15",
            "leak_diameter": 0.198510760623,
            "leak_type": "abrupt",
            "leak_start_time": 14708,
            "leak_end_time": 15247,
            "leak_peak_time": 14708
        }
    ],
    "718": [
        {
            "node_id": "16",
            "leak_diameter": 0.0708112368146,
            "leak_type": "abrupt",
            "leak_start_time": 10474,
            "leak_end_time": 11936,
            "leak_peak_time": 10474
        },
        {
            "node_id": "15",
            "leak_diameter": 0.0775595676777,
            "leak_type": "incipient",
            "leak_start_time": 7384,
            "leak_end_time": 16395,
            "leak_peak_time": 10284
        }
    ],
    "719": [
        {
            "node_id": "7",
            "leak_diameter": 0.048008615173,
            "leak_type": "incipient",
            "leak_start_time": 10648,
            "leak_end_time": 14362,
            "leak_peak_time": 13808
        }
    ],
    "720": [
        {
            "node_id": "31",
            "leak_diameter": 0.0224889123649,
            "leak_type": "abrupt",
            "leak_start_time": 10757,
            "leak_end_time": 11775,
            "leak_peak_time": 10757
        }
    ],
    "724": [
        {
            "node_id": "27",
            "leak_diameter": 0.194159150346,
            "leak_type": "incipient",
            "leak_start_time": 15014,
            "leak_end_time": 16580,
            "leak_peak_time": 15855
        },
        {
            "node_id": "25",
            "leak_diameter": 0.157912742214,
            "leak_type": "incipient",
            "leak_start_time": 10804,
            "leak_end_time": 17464,
            "leak_peak_time": 17351
        }
    ],
    "725": [
        {
            "node_id": "17",
            "leak_diameter": 0.111767725788,
            "leak_type": "incipient",
            "leak_start_time": 12226,
            "leak_end_time": 13323,
            "leak_peak_time": 12701
        },
        {
            "node_id": "8",
            "leak_diameter": 0.0382572988034,
            "leak_type": "incipient",
            "leak_start_time": 16745,
            "leak_end_time": 16923,
            "leak_peak_time": 16897
        }
    ],
    "726": [
        {
            "node_id": "11",
            "leak_diameter": 0.166836889139,
            "leak_type": "abrupt",
            "leak_start_time": 10169,
            "leak_end_time": 13416,
            "leak_peak_time": 10169
        },
        {
            "node_id": "28",
            "leak_diameter": 0.103670915779,
            "leak_type": "abrupt",
            "leak_start_time": 5284,
            "leak_end_time": 16648,
            "leak_peak_time": 5284
        }
    ],
    "727": [
        {
            "node_id": "16",
            "leak_diameter": 0.0225678445178,
            "leak_type": "abrupt",
            "leak_start_time": 10113,
            "leak_end_time": 14286,
            "leak_peak_time": 10113
        }
    ],
    "728": [
        {
            "node_id": "18",
            "leak_diameter": 0.161271028277,
            "leak_type": "incipient",
            "leak_start_time": 10611,
            "leak_end_time": 11291,
            "leak_peak_time": 11037
        }
    ],
    "729": [
        {
            "node_id": "3",
            "leak_diameter": 0.063289775212,
            "leak_type": "incipient",
            "leak_start_time": 2527,
            "leak_end_time": 15561,
            "leak_peak_time": 12643
        },
        {
            "node_id": "15",
            "leak_diameter": 0.0994187737543,
            "leak_type": "incipient",
            "leak_start_time": 3084,
            "leak_end_time": 3301,
            "leak_peak_time": 3156
        }
    ],
    "730": [
        {
            "node_id": "4",
            "leak_diameter": 0.154421675077,
            "leak_type": "abrupt",
            "leak_start_time": 6670,
            "leak_end_time": 16015,
            "leak_peak_time": 6670
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0333260216639,
            "leak_type": "incipient",
            "leak_start_time": 7329,
            "leak_end_time": 14117,
            "leak_peak_time": 10408
        }
    ],
    "731": [
        {
            "node_id": "4",
            "leak_diameter": 0.0528230775267,
            "leak_type": "incipient",
            "leak_start_time": 10715,
            "leak_end_time": 11416,
            "leak_peak_time": 10841
        },
        {
            "node_id": "17",
            "leak_diameter": 0.113364131282,
            "leak_type": "abrupt",
            "leak_start_time": 16331,
            "leak_end_time": 17481,
            "leak_peak_time": 16331
        }
    ],
    "732": [
        {
            "node_id": "8",
            "leak_diameter": 0.077508849337,
            "leak_type": "incipient",
            "leak_start_time": 8148,
            "leak_end_time": 15022,
            "leak_peak_time": 8718
        }
    ],
    "733": [
        {
            "node_id": "16",
            "leak_diameter": 0.0388168462853,
            "leak_type": "incipient",
            "leak_start_time": 1433,
            "leak_end_time": 16141,
            "leak_peak_time": 10661
        },
        {
            "node_id": "29",
            "leak_diameter": 0.0667924605716,
            "leak_type": "incipient",
            "leak_start_time": 11954,
            "leak_end_time": 16190,
            "leak_peak_time": 12013
        }
    ],
    "734": [
        {
            "node_id": "12",
            "leak_diameter": 0.0388659900311,
            "leak_type": "incipient",
            "leak_start_time": 15475,
            "leak_end_time": 15602,
            "leak_peak_time": 15574
        },
        {
            "node_id": "7",
            "leak_diameter": 0.165254929808,
            "leak_type": "incipient",
            "leak_start_time": 16211,
            "leak_end_time": 17042,
            "leak_peak_time": 16564
        }
    ],
    "735": [
        {
            "node_id": "12",
            "leak_diameter": 0.0978815731209,
            "leak_type": "abrupt",
            "leak_start_time": 3832,
            "leak_end_time": 15710,
            "leak_peak_time": 3832
        }
    ],
    "737": [
        {
            "node_id": "26",
            "leak_diameter": 0.0637286998185,
            "leak_type": "incipient",
            "leak_start_time": 9557,
            "leak_end_time": 11843,
            "leak_peak_time": 10067
        }
    ],
    "738": [
        {
            "node_id": "16",
            "leak_diameter": 0.0573744503313,
            "leak_type": "abrupt",
            "leak_start_time": 14110,
            "leak_end_time": 15696,
            "leak_peak_time": 14110
        }
    ],
    "739": [
        {
            "node_id": "26",
            "leak_diameter": 0.157852604461,
            "leak_type": "incipient",
            "leak_start_time": 6470,
            "leak_end_time": 7896,
            "leak_peak_time": 7001
        }
    ],
    "741": [
        {
            "node_id": "21",
            "leak_diameter": 0.192542005854,
            "leak_type": "incipient",
            "leak_start_time": 7615,
            "leak_end_time": 11074,
            "leak_peak_time": 8561
        }
    ],
    "743": [
        {
            "node_id": "7",
            "leak_diameter": 0.105616807202,
            "leak_type": "abrupt",
            "leak_start_time": 1620,
            "leak_end_time": 10460,
            "leak_peak_time": 1620
        }
    ],
    "745": [
        {
            "node_id": "7",
            "leak_diameter": 0.0457441017796,
            "leak_type": "incipient",
            "leak_start_time": 14986,
            "leak_end_time": 15251,
            "leak_peak_time": 15246
        }
    ],
    "747": [
        {
            "node_id": "6",
            "leak_diameter": 0.101465494397,
            "leak_type": "abrupt",
            "leak_start_time": 6069,
            "leak_end_time": 13228,
            "leak_peak_time": 6069
        }
    ],
    "749": [
        {
            "node_id": "29",
            "leak_diameter": 0.168513261347,
            "leak_type": "incipient",
            "leak_start_time": 13576,
            "leak_end_time": 16148,
            "leak_peak_time": 13642
        },
        {
            "node_id": "26",
            "leak_diameter": 0.0260653073986,
            "leak_type": "abrupt",
            "leak_start_time": 5935,
            "leak_end_time": 16366,
            "leak_peak_time": 5935
        }
    ],
    "750": [
        {
            "node_id": "4",
            "leak_diameter": 0.165532844047,
            "leak_type": "abrupt",
            "leak_start_time": 9542,
            "leak_end_time": 10917,
            "leak_peak_time": 9542
        },
        {
            "node_id": "7",
            "leak_diameter": 0.0437324333753,
            "leak_type": "incipient",
            "leak_start_time": 10438,
            "leak_end_time": 16654,
            "leak_peak_time": 13522
        }
    ],
    "752": [
        {
            "node_id": "2",
            "leak_diameter": 0.0985995091945,
            "leak_type": "incipient",
            "leak_start_time": 237,
            "leak_end_time": 5426,
            "leak_peak_time": 1507
        }
    ],
    "753": [
        {
            "node_id": "30",
            "leak_diameter": 0.0283190117639,
            "leak_type": "incipient",
            "leak_start_time": 9224,
            "leak_end_time": 13960,
            "leak_peak_time": 13362
        },
        {
            "node_id": "8",
            "leak_diameter": 0.0544786282202,
            "leak_type": "abrupt",
            "leak_start_time": 5100,
            "leak_end_time": 8682,
            "leak_peak_time": 5100
        }
    ],
    "754": [
        {
            "node_id": "10",
            "leak_diameter": 0.114712694837,
            "leak_type": "abrupt",
            "leak_start_time": 98,
            "leak_end_time": 17227,
            "leak_peak_time": 98
        }
    ],
    "755": [
        {
            "node_id": "20",
            "leak_diameter": 0.0819111790904,
            "leak_type": "abrupt",
            "leak_start_time": 16925,
            "leak_end_time": 17169,
            "leak_peak_time": 16925
        },
        {
            "node_id": "13",
            "leak_diameter": 0.0663696033678,
            "leak_type": "incipient",
            "leak_start_time": 2826,
            "leak_end_time": 16182,
            "leak_peak_time": 15961
        }
    ],
    "757": [
        {
            "node_id": "27",
            "leak_diameter": 0.18182066014,
            "leak_type": "abrupt",
            "leak_start_time": 16488,
            "leak_end_time": 17303,
            "leak_peak_time": 16488
        },
        {
            "node_id": "2",
            "leak_diameter": 0.071749639958,
            "leak_type": "abrupt",
            "leak_start_time": 9988,
            "leak_end_time": 13568,
            "leak_peak_time": 9988
        }
    ],
    "759": [
        {
            "node_id": "5",
            "leak_diameter": 0.0811669177523,
            "leak_type": "incipient",
            "leak_start_time": 10086,
            "leak_end_time": 17201,
            "leak_peak_time": 15303
        }
    ],
    "760": [
        {
            "node_id": "8",
            "leak_diameter": 0.10220850114,
            "leak_type": "abrupt",
            "leak_start_time": 5784,
            "leak_end_time": 16498,
            "leak_peak_time": 5784
        }
    ],
    "761": [
        {
            "node_id": "28",
            "leak_diameter": 0.0781130483664,
            "leak_type": "abrupt",
            "leak_start_time": 10177,
            "leak_end_time": 16111,
            "leak_peak_time": 10177
        }
    ],
    "762": [
        {
            "node_id": "4",
            "leak_diameter": 0.055449123551,
            "leak_type": "abrupt",
            "leak_start_time": 10418,
            "leak_end_time": 14883,
            "leak_peak_time": 10418
        },
        {
            "node_id": "12",
            "leak_diameter": 0.028520808397,
            "leak_type": "abrupt",
            "leak_start_time": 5823,
            "leak_end_time": 11858,
            "leak_peak_time": 5823
        }
    ],
    "763": [
        {
            "node_id": "21",
            "leak_diameter": 0.165363458505,
            "leak_type": "abrupt",
            "leak_start_time": 6769,
            "leak_end_time": 16563,
            "leak_peak_time": 6769
        }
    ],
    "764": [
        {
            "node_id": "27",
            "leak_diameter": 0.189753228463,
            "leak_type": "abrupt",
            "leak_start_time": 17386,
            "leak_end_time": 17393,
            "leak_peak_time": 17386
        },
        {
            "node_id": "3",
            "leak_diameter": 0.194261513686,
            "leak_type": "abrupt",
            "leak_start_time": 14675,
            "leak_end_time": 15774,
            "leak_peak_time": 14675
        }
    ],
    "767": [
        {
            "node_id": "29",
            "leak_diameter": 0.0423051764242,
            "leak_type": "abrupt",
            "leak_start_time": 2250,
            "leak_end_time": 7787,
            "leak_peak_time": 2250
        }
    ],
    "768": [
        {
            "node_id": "21",
            "leak_diameter": 0.130787756032,
            "leak_type": "abrupt",
            "leak_start_time": 8243,
            "leak_end_time": 9203,
            "leak_peak_time": 8243
        },
        {
            "node_id": "29",
            "leak_diameter": 0.0338978027785,
            "leak_type": "abrupt",
            "leak_start_time": 16527,
            "leak_end_time": 16885,
            "leak_peak_time": 16527
        }
    ],
    "769": [
        {
            "node_id": "9",
            "leak_diameter": 0.133882900297,
            "leak_type": "incipient",
            "leak_start_time": 9556,
            "leak_end_time": 12181,
            "leak_peak_time": 11670
        }
    ],
    "770": [
        {
            "node_id": "4",
            "leak_diameter": 0.0618561348351,
            "leak_type": "abrupt",
            "leak_start_time": 15818,
            "leak_end_time": 16539,
            "leak_peak_time": 15818
        }
    ],
    "772": [
        {
            "node_id": "10",
            "leak_diameter": 0.109598757265,
            "leak_type": "incipient",
            "leak_start_time": 7253,
            "leak_end_time": 14656,
            "leak_peak_time": 10964
        },
        {
            "node_id": "14",
            "leak_diameter": 0.0444970137022,
            "leak_type": "abrupt",
            "leak_start_time": 10175,
            "leak_end_time": 10653,
            "leak_peak_time": 10175
        }
    ],
    "774": [
        {
            "node_id": "10",
            "leak_diameter": 0.180673819695,
            "leak_type": "incipient",
            "leak_start_time": 9148,
            "leak_end_time": 14944,
            "leak_peak_time": 10145
        },
        {
            "node_id": "5",
            "leak_diameter": 0.153731154999,
            "leak_type": "incipient",
            "leak_start_time": 14072,
            "leak_end_time": 16297,
            "leak_peak_time": 15895
        }
    ],
    "776": [
        {
            "node_id": "4",
            "leak_diameter": 0.0966856135682,
            "leak_type": "incipient",
            "leak_start_time": 17387,
            "leak_end_time": 17459,
            "leak_peak_time": 17450
        },
        {
            "node_id": "7",
            "leak_diameter": 0.0912208733276,
            "leak_type": "incipient",
            "leak_start_time": 3785,
            "leak_end_time": 15677,
            "leak_peak_time": 4111
        }
    ],
    "777": [
        {
            "node_id": "10",
            "leak_diameter": 0.0343982401624,
            "leak_type": "abrupt",
            "leak_start_time": 8295,
            "leak_end_time": 16115,
            "leak_peak_time": 8295
        },
        {
            "node_id": "22",
            "leak_diameter": 0.177768292724,
            "leak_type": "abrupt",
            "leak_start_time": 7184,
            "leak_end_time": 9401,
            "leak_peak_time": 7184
        }
    ],
    "779": [
        {
            "node_id": "21",
            "leak_diameter": 0.0330090664972,
            "leak_type": "incipient",
            "leak_start_time": 5727,
            "leak_end_time": 17338,
            "leak_peak_time": 10169
        },
        {
            "node_id": "26",
            "leak_diameter": 0.160925966705,
            "leak_type": "abrupt",
            "leak_start_time": 12342,
            "leak_end_time": 16871,
            "leak_peak_time": 12342
        }
    ],
    "781": [
        {
            "node_id": "12",
            "leak_diameter": 0.18984528087,
            "leak_type": "abrupt",
            "leak_start_time": 12869,
            "leak_end_time": 17055,
            "leak_peak_time": 12869
        },
        {
            "node_id": "29",
            "leak_diameter": 0.144916635784,
            "leak_type": "abrupt",
            "leak_start_time": 14663,
            "leak_end_time": 15689,
            "leak_peak_time": 14663
        }
    ],
    "782": [
        {
            "node_id": "5",
            "leak_diameter": 0.0320397391126,
            "leak_type": "incipient",
            "leak_start_time": 16745,
            "leak_end_time": 16955,
            "leak_peak_time": 16838
        }
    ],
    "783": [
        {
            "node_id": "15",
            "leak_diameter": 0.189415721733,
            "leak_type": "abrupt",
            "leak_start_time": 2316,
            "leak_end_time": 5685,
            "leak_peak_time": 2316
        }
    ],
    "784": [
        {
            "node_id": "13",
            "leak_diameter": 0.133542116546,
            "leak_type": "incipient",
            "leak_start_time": 8313,
            "leak_end_time": 16262,
            "leak_peak_time": 9169
        }
    ],
    "785": [
        {
            "node_id": "7",
            "leak_diameter": 0.029757327184,
            "leak_type": "incipient",
            "leak_start_time": 13763,
            "leak_end_time": 15077,
            "leak_peak_time": 14688
        }
    ],
    "786": [
        {
            "node_id": "17",
            "leak_diameter": 0.195147215922,
            "leak_type": "abrupt",
            "leak_start_time": 12687,
            "leak_end_time": 14382,
            "leak_peak_time": 12687
        },
        {
            "node_id": "30",
            "leak_diameter": 0.193174546999,
            "leak_type": "incipient",
            "leak_start_time": 2855,
            "leak_end_time": 9997,
            "leak_peak_time": 3619
        }
    ],
    "789": [
        {
            "node_id": "27",
            "leak_diameter": 0.0703049186331,
            "leak_type": "abrupt",
            "leak_start_time": 9007,
            "leak_end_time": 11710,
            "leak_peak_time": 9007
        },
        {
            "node_id": "5",
            "leak_diameter": 0.0225248319166,
            "leak_type": "abrupt",
            "leak_start_time": 7474,
            "leak_end_time": 16375,
            "leak_peak_time": 7474
        }
    ],
    "790": [
        {
            "node_id": "27",
            "leak_diameter": 0.122474453899,
            "leak_type": "incipient",
            "leak_start_time": 7132,
            "leak_end_time": 8984,
            "leak_peak_time": 7621
        }
    ],
    "792": [
        {
            "node_id": "10",
            "leak_diameter": 0.0962004098996,
            "leak_type": "incipient",
            "leak_start_time": 16767,
            "leak_end_time": 16864,
            "leak_peak_time": 16835
        }
    ],
    "793": [
        {
            "node_id": "4",
            "leak_diameter": 0.0758349389702,
            "leak_type": "incipient",
            "leak_start_time": 15661,
            "leak_end_time": 16066,
            "leak_peak_time": 15960
        },
        {
            "node_id": "30",
            "leak_diameter": 0.0756750968973,
            "leak_type": "incipient",
            "leak_start_time": 11901,
            "leak_end_time": 14439,
            "leak_peak_time": 11948
        }
    ],
    "795": [
        {
            "node_id": "27",
            "leak_diameter": 0.180061403548,
            "leak_type": "abrupt",
            "leak_start_time": 1632,
            "leak_end_time": 9330,
            "leak_peak_time": 1632
        }
    ],
    "797": [
        {
            "node_id": "10",
            "leak_diameter": 0.194501425631,
            "leak_type": "incipient",
            "leak_start_time": 14919,
            "leak_end_time": 15352,
            "leak_peak_time": 15287
        },
        {
            "node_id": "15",
            "leak_diameter": 0.113286888369,
            "leak_type": "incipient",
            "leak_start_time": 39,
            "leak_end_time": 11888,
            "leak_peak_time": 4233
        }
    ],
    "798": [
        {
            "node_id": "13",
            "leak_diameter": 0.0480756636741,
            "leak_type": "incipient",
            "leak_start_time": 13578,
            "leak_end_time": 15009,
            "leak_peak_time": 14467
        }
    ],
    "799": [
        {
            "node_id": "21",
            "leak_diameter": 0.17639705122,
            "leak_type": "abrupt",
            "leak_start_time": 5242,
            "leak_end_time": 7686,
            "leak_peak_time": 5242
        },
        {
            "node_id": "9",
            "leak_diameter": 0.0637473925067,
            "leak_type": "abrupt",
            "leak_start_time": 14208,
            "leak_end_time": 17328,
            "leak_peak_time": 14208
        }
    ],
    "800": [
        {
            "node_id": "2",
            "leak_diameter": 0.128897808774,
            "leak_type": "abrupt",
            "leak_start_time": 6056,
            "leak_end_time": 15817,
            "leak_peak_time": 6056
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0941286415208,
            "leak_type": "incipient",
            "leak_start_time": 1334,
            "leak_end_time": 16147,
            "leak_peak_time": 9948
        }
    ],
    "801": [
        {
            "node_id": "4",
            "leak_diameter": 0.192066036267,
            "leak_type": "abrupt",
            "leak_start_time": 2837,
            "leak_end_time": 4000,
            "leak_peak_time": 2837
        }
    ],
    "802": [
        {
            "node_id": "20",
            "leak_diameter": 0.109942012667,
            "leak_type": "abrupt",
            "leak_start_time": 1967,
            "leak_end_time": 16943,
            "leak_peak_time": 1967
        },
        {
            "node_id": "16",
            "leak_diameter": 0.149419690317,
            "leak_type": "abrupt",
            "leak_start_time": 14508,
            "leak_end_time": 16947,
            "leak_peak_time": 14508
        }
    ],
    "803": [
        {
            "node_id": "4",
            "leak_diameter": 0.0344497930481,
            "leak_type": "abrupt",
            "leak_start_time": 3940,
            "leak_end_time": 16303,
            "leak_peak_time": 3940
        },
        {
            "node_id": "5",
            "leak_diameter": 0.157306281291,
            "leak_type": "abrupt",
            "leak_start_time": 17379,
            "leak_end_time": 17405,
            "leak_peak_time": 17379
        }
    ],
    "804": [
        {
            "node_id": "15",
            "leak_diameter": 0.0643769058164,
            "leak_type": "incipient",
            "leak_start_time": 14738,
            "leak_end_time": 14993,
            "leak_peak_time": 14914
        },
        {
            "node_id": "7",
            "leak_diameter": 0.0647064638662,
            "leak_type": "abrupt",
            "leak_start_time": 694,
            "leak_end_time": 17517,
            "leak_peak_time": 694
        }
    ],
    "805": [
        {
            "node_id": "19",
            "leak_diameter": 0.195540240682,
            "leak_type": "abrupt",
            "leak_start_time": 8950,
            "leak_end_time": 13095,
            "leak_peak_time": 8950
        },
        {
            "node_id": "9",
            "leak_diameter": 0.0752131447691,
            "leak_type": "incipient",
            "leak_start_time": 7395,
            "leak_end_time": 15800,
            "leak_peak_time": 9009
        }
    ],
    "806": [
        {
            "node_id": "21",
            "leak_diameter": 0.0250999809101,
            "leak_type": "incipient",
            "leak_start_time": 3434,
            "leak_end_time": 7902,
            "leak_peak_time": 5765
        }
    ],
    "808": [
        {
            "node_id": "10",
            "leak_diameter": 0.132638630601,
            "leak_type": "incipient",
            "leak_start_time": 11138,
            "leak_end_time": 13944,
            "leak_peak_time": 13606
        }
    ],
    "809": [
        {
            "node_id": "12",
            "leak_diameter": 0.170848102689,
            "leak_type": "abrupt",
            "leak_start_time": 9801,
            "leak_end_time": 10011,
            "leak_peak_time": 9801
        }
    ],
    "811": [
        {
            "node_id": "17",
            "leak_diameter": 0.0570727770892,
            "leak_type": "incipient",
            "leak_start_time": 2007,
            "leak_end_time": 16470,
            "leak_peak_time": 16030
        },
        {
            "node_id": "15",
            "leak_diameter": 0.15393281884,
            "leak_type": "abrupt",
            "leak_start_time": 8849,
            "leak_end_time": 11543,
            "leak_peak_time": 8849
        }
    ],
    "812": [
        {
            "node_id": "16",
            "leak_diameter": 0.108345970256,
            "leak_type": "abrupt",
            "leak_start_time": 10386,
            "leak_end_time": 15066,
            "leak_peak_time": 10386
        },
        {
            "node_id": "12",
            "leak_diameter": 0.0322626394032,
            "leak_type": "incipient",
            "leak_start_time": 10304,
            "leak_end_time": 14140,
            "leak_peak_time": 13294
        }
    ],
    "813": [
        {
            "node_id": "9",
            "leak_diameter": 0.0306416263075,
            "leak_type": "incipient",
            "leak_start_time": 2368,
            "leak_end_time": 7058,
            "leak_peak_time": 6388
        }
    ],
    "815": [
        {
            "node_id": "11",
            "leak_diameter": 0.0716102426205,
            "leak_type": "incipient",
            "leak_start_time": 10984,
            "leak_end_time": 12086,
            "leak_peak_time": 12058
        }
    ],
    "817": [
        {
            "node_id": "8",
            "leak_diameter": 0.190347008227,
            "leak_type": "incipient",
            "leak_start_time": 12802,
            "leak_end_time": 15891,
            "leak_peak_time": 12927
        },
        {
            "node_id": "9",
            "leak_diameter": 0.173607023731,
            "leak_type": "incipient",
            "leak_start_time": 3187,
            "leak_end_time": 10833,
            "leak_peak_time": 5237
        }
    ],
    "818": [
        {
            "node_id": "13",
            "leak_diameter": 0.130955631558,
            "leak_type": "incipient",
            "leak_start_time": 11558,
            "leak_end_time": 14086,
            "leak_peak_time": 13453
        }
    ],
    "819": [
        {
            "node_id": "20",
            "leak_diameter": 0.167826447268,
            "leak_type": "incipient",
            "leak_start_time": 12801,
            "leak_end_time": 16635,
            "leak_peak_time": 15716
        }
    ],
    "822": [
        {
            "node_id": "4",
            "leak_diameter": 0.0822755580247,
            "leak_type": "incipient",
            "leak_start_time": 11039,
            "leak_end_time": 15159,
            "leak_peak_time": 12333
        }
    ],
    "825": [
        {
            "node_id": "2",
            "leak_diameter": 0.0238672108159,
            "leak_type": "abrupt",
            "leak_start_time": 12141,
            "leak_end_time": 13801,
            "leak_peak_time": 12141
        }
    ],
    "826": [
        {
            "node_id": "8",
            "leak_diameter": 0.171174452758,
            "leak_type": "abrupt",
            "leak_start_time": 15346,
            "leak_end_time": 17117,
            "leak_peak_time": 15346
        },
        {
            "node_id": "9",
            "leak_diameter": 0.162930381512,
            "leak_type": "incipient",
            "leak_start_time": 14758,
            "leak_end_time": 16559,
            "leak_peak_time": 15569
        }
    ],
    "827": [
        {
            "node_id": "7",
            "leak_diameter": 0.0763047102232,
            "leak_type": "incipient",
            "leak_start_time": 3772,
            "leak_end_time": 4329,
            "leak_peak_time": 3900
        }
    ],
    "828": [
        {
            "node_id": "11",
            "leak_diameter": 0.058978694954,
            "leak_type": "abrupt",
            "leak_start_time": 17357,
            "leak_end_time": 17437,
            "leak_peak_time": 17357
        },
        {
            "node_id": "28",
            "leak_diameter": 0.0533588657971,
            "leak_type": "abrupt",
            "leak_start_time": 5345,
            "leak_end_time": 10423,
            "leak_peak_time": 5345
        }
    ],
    "831": [
        {
            "node_id": "17",
            "leak_diameter": 0.13151482058,
            "leak_type": "incipient",
            "leak_start_time": 1174,
            "leak_end_time": 11701,
            "leak_peak_time": 10010
        }
    ],
    "832": [
        {
            "node_id": "18",
            "leak_diameter": 0.0997236589799,
            "leak_type": "abrupt",
            "leak_start_time": 16407,
            "leak_end_time": 17077,
            "leak_peak_time": 16407
        }
    ],
    "833": [
        {
            "node_id": "4",
            "leak_diameter": 0.16170678122,
            "leak_type": "incipient",
            "leak_start_time": 10337,
            "leak_end_time": 11093,
            "leak_peak_time": 10533
        },
        {
            "node_id": "28",
            "leak_diameter": 0.0961637033175,
            "leak_type": "abrupt",
            "leak_start_time": 10833,
            "leak_end_time": 11358,
            "leak_peak_time": 10833
        }
    ],
    "834": [
        {
            "node_id": "30",
            "leak_diameter": 0.105047000248,
            "leak_type": "abrupt",
            "leak_start_time": 11805,
            "leak_end_time": 12135,
            "leak_peak_time": 11805
        }
    ],
    "835": [
        {
            "node_id": "25",
            "leak_diameter": 0.0624279307704,
            "leak_type": "incipient",
            "leak_start_time": 12673,
            "leak_end_time": 12824,
            "leak_peak_time": 12686
        },
        {
            "node_id": "29",
            "leak_diameter": 0.124401029726,
            "leak_type": "incipient",
            "leak_start_time": 3204,
            "leak_end_time": 13813,
            "leak_peak_time": 11582
        }
    ],
    "836": [
        {
            "node_id": "20",
            "leak_diameter": 0.103683187658,
            "leak_type": "abrupt",
            "leak_start_time": 4729,
            "leak_end_time": 15545,
            "leak_peak_time": 4729
        },
        {
            "node_id": "3",
            "leak_diameter": 0.0305555245106,
            "leak_type": "abrupt",
            "leak_start_time": 7656,
            "leak_end_time": 9922,
            "leak_peak_time": 7656
        }
    ],
    "837": [
        {
            "node_id": "21",
            "leak_diameter": 0.190505171581,
            "leak_type": "abrupt",
            "leak_start_time": 8898,
            "leak_end_time": 10284,
            "leak_peak_time": 8898
        }
    ],
    "838": [
        {
            "node_id": "10",
            "leak_diameter": 0.1014615683,
            "leak_type": "abrupt",
            "leak_start_time": 7244,
            "leak_end_time": 16169,
            "leak_peak_time": 7244
        },
        {
            "node_id": "26",
            "leak_diameter": 0.159944312277,
            "leak_type": "incipient",
            "leak_start_time": 17445,
            "leak_end_time": 17477,
            "leak_peak_time": 17451
        }
    ],
    "841": [
        {
            "node_id": "11",
            "leak_diameter": 0.124032174487,
            "leak_type": "abrupt",
            "leak_start_time": 16389,
            "leak_end_time": 16990,
            "leak_peak_time": 16389
        },
        {
            "node_id": "17",
            "leak_diameter": 0.149014897765,
            "leak_type": "abrupt",
            "leak_start_time": 12758,
            "leak_end_time": 12924,
            "leak_peak_time": 12758
        }
    ],
    "842": [
        {
            "node_id": "29",
            "leak_diameter": 0.0832303871101,
            "leak_type": "abrupt",
            "leak_start_time": 10543,
            "leak_end_time": 13588,
            "leak_peak_time": 10543
        }
    ],
    "843": [
        {
            "node_id": "19",
            "leak_diameter": 0.0644352776256,
            "leak_type": "incipient",
            "leak_start_time": 3223,
            "leak_end_time": 11244,
            "leak_peak_time": 9753
        }
    ],
    "845": [
        {
            "node_id": "18",
            "leak_diameter": 0.0625088256051,
            "leak_type": "abrupt",
            "leak_start_time": 13909,
            "leak_end_time": 15996,
            "leak_peak_time": 13909
        }
    ],
    "846": [
        {
            "node_id": "2",
            "leak_diameter": 0.11999043247,
            "leak_type": "incipient",
            "leak_start_time": 15904,
            "leak_end_time": 17136,
            "leak_peak_time": 17105
        }
    ],
    "849": [
        {
            "node_id": "20",
            "leak_diameter": 0.0926323277731,
            "leak_type": "incipient",
            "leak_start_time": 8371,
            "leak_end_time": 9765,
            "leak_peak_time": 8522
        }
    ],
    "850": [
        {
            "node_id": "2",
            "leak_diameter": 0.106150345614,
            "leak_type": "incipient",
            "leak_start_time": 2988,
            "leak_end_time": 15989,
            "leak_peak_time": 13431
        }
    ],
    "851": [
        {
            "node_id": "4",
            "leak_diameter": 0.0616868909141,
            "leak_type": "incipient",
            "leak_start_time": 1978,
            "leak_end_time": 5316,
            "leak_peak_time": 3876
        }
    ],
    "852": [
        {
            "node_id": "12",
            "leak_diameter": 0.133428449092,
            "leak_type": "abrupt",
            "leak_start_time": 11611,
            "leak_end_time": 12140,
            "leak_peak_time": 11611
        }
    ],
    "855": [
        {
            "node_id": "3",
            "leak_diameter": 0.037062391546,
            "leak_type": "incipient",
            "leak_start_time": 431,
            "leak_end_time": 13742,
            "leak_peak_time": 13287
        },
        {
            "node_id": "2",
            "leak_diameter": 0.134745624097,
            "leak_type": "incipient",
            "leak_start_time": 5461,
            "leak_end_time": 6802,
            "leak_peak_time": 6638
        }
    ],
    "856": [
        {
            "node_id": "14",
            "leak_diameter": 0.0653294354329,
            "leak_type": "abrupt",
            "leak_start_time": 3385,
            "leak_end_time": 16102,
            "leak_peak_time": 3385
        }
    ],
    "858": [
        {
            "node_id": "11",
            "leak_diameter": 0.05979893182,
            "leak_type": "incipient",
            "leak_start_time": 10725,
            "leak_end_time": 11426,
            "leak_peak_time": 11049
        },
        {
            "node_id": "31",
            "leak_diameter": 0.153279465573,
            "leak_type": "abrupt",
            "leak_start_time": 2488,
            "leak_end_time": 3927,
            "leak_peak_time": 2488
        }
    ],
    "859": [
        {
            "node_id": "7",
            "leak_diameter": 0.0332987370641,
            "leak_type": "incipient",
            "leak_start_time": 3311,
            "leak_end_time": 15098,
            "leak_peak_time": 10565
        }
    ],
    "860": [
        {
            "node_id": "7",
            "leak_diameter": 0.0445965839841,
            "leak_type": "abrupt",
            "leak_start_time": 4120,
            "leak_end_time": 8470,
            "leak_peak_time": 4120
        }
    ],
    "863": [
        {
            "node_id": "11",
            "leak_diameter": 0.0378549472039,
            "leak_type": "incipient",
            "leak_start_time": 16958,
            "leak_end_time": 17051,
            "leak_peak_time": 16987
        }
    ],
    "864": [
        {
            "node_id": "19",
            "leak_diameter": 0.196460699828,
            "leak_type": "abrupt",
            "leak_start_time": 12608,
            "leak_end_time": 17027,
            "leak_peak_time": 12608
        }
    ],
    "866": [
        {
            "node_id": "7",
            "leak_diameter": 0.069714295746,
            "leak_type": "abrupt",
            "leak_start_time": 5874,
            "leak_end_time": 6974,
            "leak_peak_time": 5874
        }
    ],
    "867": [
        {
            "node_id": "12",
            "leak_diameter": 0.0569866869045,
            "leak_type": "abrupt",
            "leak_start_time": 3872,
            "leak_end_time": 14183,
            "leak_peak_time": 3872
        },
        {
            "node_id": "31",
            "leak_diameter": 0.157178806981,
            "leak_type": "abrupt",
            "leak_start_time": 4336,
            "leak_end_time": 12297,
            "leak_peak_time": 4336
        }
    ],
    "868": [
        {
            "node_id": "7",
            "leak_diameter": 0.0705294627533,
            "leak_type": "abrupt",
            "leak_start_time": 14699,
            "leak_end_time": 17286,
            "leak_peak_time": 14699
        }
    ],
    "869": [
        {
            "node_id": "5",
            "leak_diameter": 0.0661936072381,
            "leak_type": "incipient",
            "leak_start_time": 14208,
            "leak_end_time": 15893,
            "leak_peak_time": 15461
        },
        {
            "node_id": "9",
            "leak_diameter": 0.0958931540154,
            "leak_type": "incipient",
            "leak_start_time": 14330,
            "leak_end_time": 16429,
            "leak_peak_time": 14749
        }
    ],
    "870": [
        {
            "node_id": "10",
            "leak_diameter": 0.0323069269074,
            "leak_type": "abrupt",
            "leak_start_time": 11570,
            "leak_end_time": 13359,
            "leak_peak_time": 11570
        }
    ],
    "871": [
        {
            "node_id": "2",
            "leak_diameter": 0.0893905259131,
            "leak_type": "abrupt",
            "leak_start_time": 11677,
            "leak_end_time": 16660,
            "leak_peak_time": 11677
        }
    ],
    "872": [
        {
            "node_id": "23",
            "leak_diameter": 0.0471095176833,
            "leak_type": "incipient",
            "leak_start_time": 15595,
            "leak_end_time": 17510,
            "leak_peak_time": 15685
        }
    ],
    "873": [
        {
            "node_id": "21",
            "leak_diameter": 0.108413179738,
            "leak_type": "incipient",
            "leak_start_time": 9335,
            "leak_end_time": 12957,
            "leak_peak_time": 11404
        },
        {
            "node_id": "13",
            "leak_diameter": 0.13706631937,
            "leak_type": "abrupt",
            "leak_start_time": 11170,
            "leak_end_time": 16762,
            "leak_peak_time": 11170
        }
    ],
    "874": [
        {
            "node_id": "10",
            "leak_diameter": 0.134029796429,
            "leak_type": "incipient",
            "leak_start_time": 15111,
            "leak_end_time": 16033,
            "leak_peak_time": 15158
        }
    ],
    "875": [
        {
            "node_id": "31",
            "leak_diameter": 0.096026470446,
            "leak_type": "incipient",
            "leak_start_time": 12012,
            "leak_end_time": 15516,
            "leak_peak_time": 13639
        }
    ],
    "876": [
        {
            "node_id": "6",
            "leak_diameter": 0.0738902926896,
            "leak_type": "incipient",
            "leak_start_time": 16930,
            "leak_end_time": 16954,
            "leak_peak_time": 16934
        },
        {
            "node_id": "25",
            "leak_diameter": 0.106019106164,
            "leak_type": "incipient",
            "leak_start_time": 15127,
            "leak_end_time": 17310,
            "leak_peak_time": 15518
        }
    ],
    "877": [
        {
            "node_id": "13",
            "leak_diameter": 0.116450887774,
            "leak_type": "incipient",
            "leak_start_time": 16756,
            "leak_end_time": 17420,
            "leak_peak_time": 17303
        }
    ],
    "879": [
        {
            "node_id": "2",
            "leak_diameter": 0.0514064971007,
            "leak_type": "abrupt",
            "leak_start_time": 9771,
            "leak_end_time": 10794,
            "leak_peak_time": 9771
        },
        {
            "node_id": "28",
            "leak_diameter": 0.076142588516,
            "leak_type": "incipient",
            "leak_start_time": 12526,
            "leak_end_time": 13467,
            "leak_peak_time": 12799
        }
    ],
    "881": [
        {
            "node_id": "7",
            "leak_diameter": 0.0271013631228,
            "leak_type": "incipient",
            "leak_start_time": 11239,
            "leak_end_time": 14883,
            "leak_peak_time": 13986
        }
    ],
    "882": [
        {
            "node_id": "6",
            "leak_diameter": 0.0376946973795,
            "leak_type": "incipient",
            "leak_start_time": 378,
            "leak_end_time": 12366,
            "leak_peak_time": 5475
        },
        {
            "node_id": "18",
            "leak_diameter": 0.165210691904,
            "leak_type": "incipient",
            "leak_start_time": 6395,
            "leak_end_time": 7491,
            "leak_peak_time": 6791
        }
    ],
    "883": [
        {
            "node_id": "11",
            "leak_diameter": 0.0537650293961,
            "leak_type": "incipient",
            "leak_start_time": 11467,
            "leak_end_time": 12870,
            "leak_peak_time": 12174
        },
        {
            "node_id": "18",
            "leak_diameter": 0.0984121224864,
            "leak_type": "abrupt",
            "leak_start_time": 4386,
            "leak_end_time": 8210,
            "leak_peak_time": 4386
        }
    ],
    "884": [
        {
            "node_id": "21",
            "leak_diameter": 0.116583326287,
            "leak_type": "abrupt",
            "leak_start_time": 11353,
            "leak_end_time": 11611,
            "leak_peak_time": 11353
        }
    ],
    "885": [
        {
            "node_id": "29",
            "leak_diameter": 0.0432854126238,
            "leak_type": "abrupt",
            "leak_start_time": 8444,
            "leak_end_time": 11824,
            "leak_peak_time": 8444
        }
    ],
    "888": [
        {
            "node_id": "27",
            "leak_diameter": 0.18100474738,
            "leak_type": "incipient",
            "leak_start_time": 12828,
            "leak_end_time": 16119,
            "leak_peak_time": 15864
        },
        {
            "node_id": "11",
            "leak_diameter": 0.153696454329,
            "leak_type": "abrupt",
            "leak_start_time": 17208,
            "leak_end_time": 17233,
            "leak_peak_time": 17208
        }
    ],
    "889": [
        {
            "node_id": "13",
            "leak_diameter": 0.135619987284,
            "leak_type": "abrupt",
            "leak_start_time": 6847,
            "leak_end_time": 8258,
            "leak_peak_time": 6847
        }
    ],
    "890": [
        {
            "node_id": "13",
            "leak_diameter": 0.0638514488077,
            "leak_type": "abrupt",
            "leak_start_time": 13416,
            "leak_end_time": 16260,
            "leak_peak_time": 13416
        }
    ],
    "891": [
        {
            "node_id": "17",
            "leak_diameter": 0.176333881921,
            "leak_type": "incipient",
            "leak_start_time": 7773,
            "leak_end_time": 12452,
            "leak_peak_time": 10384
        },
        {
            "node_id": "15",
            "leak_diameter": 0.127165189506,
            "leak_type": "abrupt",
            "leak_start_time": 3927,
            "leak_end_time": 6977,
            "leak_peak_time": 3927
        }
    ],
    "892": [
        {
            "node_id": "22",
            "leak_diameter": 0.0262775746737,
            "leak_type": "incipient",
            "leak_start_time": 8497,
            "leak_end_time": 12695,
            "leak_peak_time": 10642
        },
        {
            "node_id": "26",
            "leak_diameter": 0.0210154423766,
            "leak_type": "abrupt",
            "leak_start_time": 6817,
            "leak_end_time": 12666,
            "leak_peak_time": 6817
        }
    ],
    "893": [
        {
            "node_id": "4",
            "leak_diameter": 0.0227649555581,
            "leak_type": "incipient",
            "leak_start_time": 15038,
            "leak_end_time": 17308,
            "leak_peak_time": 16540
        },
        {
            "node_id": "2",
            "leak_diameter": 0.157002721772,
            "leak_type": "abrupt",
            "leak_start_time": 13281,
            "leak_end_time": 15360,
            "leak_peak_time": 13281
        }
    ],
    "894": [
        {
            "node_id": "16",
            "leak_diameter": 0.0259238361548,
            "leak_type": "abrupt",
            "leak_start_time": 7669,
            "leak_end_time": 17418,
            "leak_peak_time": 7669
        },
        {
            "node_id": "28",
            "leak_diameter": 0.0676846156613,
            "leak_type": "incipient",
            "leak_start_time": 5503,
            "leak_end_time": 7405,
            "leak_peak_time": 6499
        }
    ],
    "897": [
        {
            "node_id": "29",
            "leak_diameter": 0.143838597296,
            "leak_type": "incipient",
            "leak_start_time": 17344,
            "leak_end_time": 17366,
            "leak_peak_time": 17357
        },
        {
            "node_id": "30",
            "leak_diameter": 0.113684167321,
            "leak_type": "incipient",
            "leak_start_time": 10523,
            "leak_end_time": 15334,
            "leak_peak_time": 13259
        }
    ],
    "898": [
        {
            "node_id": "28",
            "leak_diameter": 0.147866039294,
            "leak_type": "abrupt",
            "leak_start_time": 444,
            "leak_end_time": 1830,
            "leak_peak_time": 444
        }
    ],
    "900": [
        {
            "node_id": "4",
            "leak_diameter": 0.174634586215,
            "leak_type": "incipient",
            "leak_start_time": 2189,
            "leak_end_time": 4567,
            "leak_peak_time": 3552
        },
        {
            "node_id": "28",
            "leak_diameter": 0.175924646693,
            "leak_type": "incipient",
            "leak_start_time": 3052,
            "leak_end_time": 12126,
            "leak_peak_time": 4884
        }
    ],
    "901": [
        {
            "node_id": "14",
            "leak_diameter": 0.0849161030682,
            "leak_type": "incipient",
            "leak_start_time": 1762,
            "leak_end_time": 9156,
            "leak_peak_time": 2886
        }
    ],
    "903": [
        {
            "node_id": "15",
            "leak_diameter": 0.181399259262,
            "leak_type": "abrupt",
            "leak_start_time": 13868,
            "leak_end_time": 16092,
            "leak_peak_time": 13868
        },
        {
            "node_id": "23",
            "leak_diameter": 0.0865160019448,
            "leak_type": "incipient",
            "leak_start_time": 6331,
            "leak_end_time": 9781,
            "leak_peak_time": 6693
        }
    ],
    "904": [
        {
            "node_id": "20",
            "leak_diameter": 0.114891562207,
            "leak_type": "incipient",
            "leak_start_time": 7721,
            "leak_end_time": 13158,
            "leak_peak_time": 8696
        }
    ],
    "905": [
        {
            "node_id": "4",
            "leak_diameter": 0.170224600376,
            "leak_type": "incipient",
            "leak_start_time": 16974,
            "leak_end_time": 17440,
            "leak_peak_time": 17161
        }
    ],
    "906": [
        {
            "node_id": "5",
            "leak_diameter": 0.156997134813,
            "leak_type": "abrupt",
            "leak_start_time": 11379,
            "leak_end_time": 15870,
            "leak_peak_time": 11379
        }
    ],
    "907": [
        {
            "node_id": "7",
            "leak_diameter": 0.144670221569,
            "leak_type": "abrupt",
            "leak_start_time": 15291,
            "leak_end_time": 16485,
            "leak_peak_time": 15291
        }
    ],
    "908": [
        {
            "node_id": "21",
            "leak_diameter": 0.0459085581534,
            "leak_type": "incipient",
            "leak_start_time": 14027,
            "leak_end_time": 15352,
            "leak_peak_time": 14652
        }
    ],
    "909": [
        {
            "node_id": "3",
            "leak_diameter": 0.163375410023,
            "leak_type": "abrupt",
            "leak_start_time": 1003,
            "leak_end_time": 10598,
            "leak_peak_time": 1003
        },
        {
            "node_id": "2",
            "leak_diameter": 0.0275941383502,
            "leak_type": "incipient",
            "leak_start_time": 9195,
            "leak_end_time": 16466,
            "leak_peak_time": 11462
        }
    ],
    "910": [
        {
            "node_id": "21",
            "leak_diameter": 0.0748779478815,
            "leak_type": "abrupt",
            "leak_start_time": 3552,
            "leak_end_time": 12245,
            "leak_peak_time": 3552
        },
        {
            "node_id": "30",
            "leak_diameter": 0.139273102869,
            "leak_type": "incipient",
            "leak_start_time": 13104,
            "leak_end_time": 13298,
            "leak_peak_time": 13255
        }
    ],
    "911": [
        {
            "node_id": "31",
            "leak_diameter": 0.116045320154,
            "leak_type": "incipient",
            "leak_start_time": 5069,
            "leak_end_time": 15185,
            "leak_peak_time": 10467
        }
    ],
    "912": [
        {
            "node_id": "27",
            "leak_diameter": 0.131662922088,
            "leak_type": "abrupt",
            "leak_start_time": 10994,
            "leak_end_time": 14705,
            "leak_peak_time": 10994
        },
        {
            "node_id": "32",
            "leak_diameter": 0.057869285779,
            "leak_type": "incipient",
            "leak_start_time": 1653,
            "leak_end_time": 2418,
            "leak_peak_time": 1961
        }
    ],
    "913": [
        {
            "node_id": "23",
            "leak_diameter": 0.0314429587592,
            "leak_type": "abrupt",
            "leak_start_time": 16014,
            "leak_end_time": 16944,
            "leak_peak_time": 16014
        },
        {
            "node_id": "26",
            "leak_diameter": 0.124560687412,
            "leak_type": "incipient",
            "leak_start_time": 1480,
            "leak_end_time": 15967,
            "leak_peak_time": 13773
        }
    ],
    "914": [
        {
            "node_id": "13",
            "leak_diameter": 0.110551064067,
            "leak_type": "abrupt",
            "leak_start_time": 1729,
            "leak_end_time": 12124,
            "leak_peak_time": 1729
        }
    ],
    "915": [
        {
            "node_id": "14",
            "leak_diameter": 0.18891208511,
            "leak_type": "incipient",
            "leak_start_time": 15589,
            "leak_end_time": 16275,
            "leak_peak_time": 16198
        }
    ],
    "916": [
        {
            "node_id": "8",
            "leak_diameter": 0.031248051209,
            "leak_type": "abrupt",
            "leak_start_time": 6468,
            "leak_end_time": 7504,
            "leak_peak_time": 6468
        }
    ],
    "917": [
        {
            "node_id": "18",
            "leak_diameter": 0.158817861716,
            "leak_type": "incipient",
            "leak_start_time": 13113,
            "leak_end_time": 15653,
            "leak_peak_time": 13969
        }
    ],
    "919": [
        {
            "node_id": "10",
            "leak_diameter": 0.113668932462,
            "leak_type": "incipient",
            "leak_start_time": 3720,
            "leak_end_time": 14850,
            "leak_peak_time": 6495
        }
    ],
    "920": [
        {
            "node_id": "31",
            "leak_diameter": 0.0435853286774,
            "leak_type": "incipient",
            "leak_start_time": 16655,
            "leak_end_time": 17404,
            "leak_peak_time": 16670
        }
    ],
    "921": [
        {
            "node_id": "21",
            "leak_diameter": 0.0467205248717,
            "leak_type": "incipient",
            "leak_start_time": 6533,
            "leak_end_time": 16430,
            "leak_peak_time": 6821
        },
        {
            "node_id": "5",
            "leak_diameter": 0.100189325194,
            "leak_type": "incipient",
            "leak_start_time": 11518,
            "leak_end_time": 16863,
            "leak_peak_time": 12930
        }
    ],
    "922": [
        {
            "node_id": "22",
            "leak_diameter": 0.0341031699998,
            "leak_type": "abrupt",
            "leak_start_time": 79,
            "leak_end_time": 17085,
            "leak_peak_time": 79
        },
        {
            "node_id": "26",
            "leak_diameter": 0.123557466308,
            "leak_type": "abrupt",
            "leak_start_time": 3136,
            "leak_end_time": 14109,
            "leak_peak_time": 3136
        }
    ],
    "924": [
        {
            "node_id": "29",
            "leak_diameter": 0.138544408615,
            "leak_type": "abrupt",
            "leak_start_time": 12604,
            "leak_end_time": 16921,
            "leak_peak_time": 12604
        }
    ],
    "925": [
        {
            "node_id": "2",
            "leak_diameter": 0.0447576115947,
            "leak_type": "abrupt",
            "leak_start_time": 17067,
            "leak_end_time": 17194,
            "leak_peak_time": 17067
        }
    ],
    "926": [
        {
            "node_id": "10",
            "leak_diameter": 0.0957522894106,
            "leak_type": "incipient",
            "leak_start_time": 16042,
            "leak_end_time": 16783,
            "leak_peak_time": 16386
        }
    ],
    "927": [
        {
            "node_id": "13",
            "leak_diameter": 0.153764269331,
            "leak_type": "abrupt",
            "leak_start_time": 16712,
            "leak_end_time": 17170,
            "leak_peak_time": 16712
        }
    ],
    "928": [
        {
            "node_id": "9",
            "leak_diameter": 0.0879375597166,
            "leak_type": "abrupt",
            "leak_start_time": 15926,
            "leak_end_time": 16700,
            "leak_peak_time": 15926
        }
    ],
    "930": [
        {
            "node_id": "2",
            "leak_diameter": 0.0691407516992,
            "leak_type": "abrupt",
            "leak_start_time": 1344,
            "leak_end_time": 11155,
            "leak_peak_time": 1344
        }
    ],
    "933": [
        {
            "node_id": "17",
            "leak_diameter": 0.178668306513,
            "leak_type": "incipient",
            "leak_start_time": 12644,
            "leak_end_time": 13086,
            "leak_peak_time": 12801
        },
        {
            "node_id": "5",
            "leak_diameter": 0.0377461087481,
            "leak_type": "incipient",
            "leak_start_time": 10171,
            "leak_end_time": 14662,
            "leak_peak_time": 11103
        }
    ],
    "935": [
        {
            "node_id": "3",
            "leak_diameter": 0.0391492409476,
            "leak_type": "incipient",
            "leak_start_time": 14240,
            "leak_end_time": 17133,
            "leak_peak_time": 14394
        },
        {
            "node_id": "19",
            "leak_diameter": 0.120320474403,
            "leak_type": "incipient",
            "leak_start_time": 6608,
            "leak_end_time": 6834,
            "leak_peak_time": 6617
        }
    ],
    "936": [
        {
            "node_id": "21",
            "leak_diameter": 0.0430598323607,
            "leak_type": "abrupt",
            "leak_start_time": 13391,
            "leak_end_time": 13725,
            "leak_peak_time": 13391
        }
    ],
    "937": [
        {
            "node_id": "17",
            "leak_diameter": 0.0644858617716,
            "leak_type": "abrupt",
            "leak_start_time": 10321,
            "leak_end_time": 14465,
            "leak_peak_time": 10321
        }
    ],
    "938": [
        {
            "node_id": "14",
            "leak_diameter": 0.165091163776,
            "leak_type": "abrupt",
            "leak_start_time": 6179,
            "leak_end_time": 13331,
            "leak_peak_time": 6179
        }
    ],
    "940": [
        {
            "node_id": "13",
            "leak_diameter": 0.0620539893154,
            "leak_type": "abrupt",
            "leak_start_time": 9552,
            "leak_end_time": 15013,
            "leak_peak_time": 9552
        },
        {
            "node_id": "28",
            "leak_diameter": 0.138206009373,
            "leak_type": "abrupt",
            "leak_start_time": 4806,
            "leak_end_time": 15857,
            "leak_peak_time": 4806
        }
    ],
    "942": [
        {
            "node_id": "14",
            "leak_diameter": 0.159297339708,
            "leak_type": "incipient",
            "leak_start_time": 6804,
            "leak_end_time": 8004,
            "leak_peak_time": 6994
        }
    ],
    "944": [
        {
            "node_id": "10",
            "leak_diameter": 0.0321106679981,
            "leak_type": "abrupt",
            "leak_start_time": 16658,
            "leak_end_time": 17063,
            "leak_peak_time": 16658
        }
    ],
    "945": [
        {
            "node_id": "25",
            "leak_diameter": 0.0857568770876,
            "leak_type": "abrupt",
            "leak_start_time": 5495,
            "leak_end_time": 14824,
            "leak_peak_time": 5495
        }
    ],
    "946": [
        {
            "node_id": "20",
            "leak_diameter": 0.1656434326,
            "leak_type": "incipient",
            "leak_start_time": 12687,
            "leak_end_time": 15835,
            "leak_peak_time": 13546
        }
    ],
    "947": [
        {
            "node_id": "20",
            "leak_diameter": 0.170179412668,
            "leak_type": "abrupt",
            "leak_start_time": 3903,
            "leak_end_time": 13793,
            "leak_peak_time": 3903
        },
        {
            "node_id": "17",
            "leak_diameter": 0.0489409940227,
            "leak_type": "incipient",
            "leak_start_time": 16176,
            "leak_end_time": 16999,
            "leak_peak_time": 16799
        }
    ],
    "948": [
        {
            "node_id": "12",
            "leak_diameter": 0.168646569034,
            "leak_type": "incipient",
            "leak_start_time": 647,
            "leak_end_time": 11740,
            "leak_peak_time": 8406
        }
    ],
    "949": [
        {
            "node_id": "19",
            "leak_diameter": 0.196886728707,
            "leak_type": "incipient",
            "leak_start_time": 5169,
            "leak_end_time": 6343,
            "leak_peak_time": 6086
        }
    ],
    "950": [
        {
            "node_id": "6",
            "leak_diameter": 0.186796907456,
            "leak_type": "abrupt",
            "leak_start_time": 4542,
            "leak_end_time": 8143,
            "leak_peak_time": 4542
        },
        {
            "node_id": "8",
            "leak_diameter": 0.161114604217,
            "leak_type": "abrupt",
            "leak_start_time": 6368,
            "leak_end_time": 16696,
            "leak_peak_time": 6368
        }
    ],
    "951": [
        {
            "node_id": "23",
            "leak_diameter": 0.129801393209,
            "leak_type": "incipient",
            "leak_start_time": 5039,
            "leak_end_time": 13009,
            "leak_peak_time": 6892
        }
    ],
    "952": [
        {
            "node_id": "4",
            "leak_diameter": 0.13738818186,
            "leak_type": "abrupt",
            "leak_start_time": 6440,
            "leak_end_time": 14915,
            "leak_peak_time": 6440
        }
    ],
    "956": [
        {
            "node_id": "26",
            "leak_diameter": 0.0833850518591,
            "leak_type": "abrupt",
            "leak_start_time": 8050,
            "leak_end_time": 11401,
            "leak_peak_time": 8050
        }
    ],
    "957": [
        {
            "node_id": "7",
            "leak_diameter": 0.0484678835052,
            "leak_type": "incipient",
            "leak_start_time": 10394,
            "leak_end_time": 11563,
            "leak_peak_time": 11101
        }
    ],
    "961": [
        {
            "node_id": "30",
            "leak_diameter": 0.147829608774,
            "leak_type": "abrupt",
            "leak_start_time": 5084,
            "leak_end_time": 14838,
            "leak_peak_time": 5084
        }
    ],
    "962": [
        {
            "node_id": "26",
            "leak_diameter": 0.195756702974,
            "leak_type": "incipient",
            "leak_start_time": 7817,
            "leak_end_time": 8610,
            "leak_peak_time": 8205
        }
    ],
    "963": [
        {
            "node_id": "19",
            "leak_diameter": 0.125925403945,
            "leak_type": "abrupt",
            "leak_start_time": 1120,
            "leak_end_time": 15947,
            "leak_peak_time": 1120
        }
    ],
    "964": [
        {
            "node_id": "5",
            "leak_diameter": 0.0950316715756,
            "leak_type": "incipient",
            "leak_start_time": 17486,
            "leak_end_time": 17506,
            "leak_peak_time": 17494
        }
    ],
    "966": [
        {
            "node_id": "11",
            "leak_diameter": 0.129957832715,
            "leak_type": "incipient",
            "leak_start_time": 12210,
            "leak_end_time": 13143,
            "leak_peak_time": 13142
        }
    ],
    "970": [
        {
            "node_id": "29",
            "leak_diameter": 0.0738193713408,
            "leak_type": "abrupt",
            "leak_start_time": 12772,
            "leak_end_time": 14040,
            "leak_peak_time": 12772
        }
    ],
    "974": [
        {
            "node_id": "6",
            "leak_diameter": 0.118428347123,
            "leak_type": "abrupt",
            "leak_start_time": 4881,
            "leak_end_time": 8994,
            "leak_peak_time": 4881
        },
        {
            "node_id": "19",
            "leak_diameter": 0.0323384057147,
            "leak_type": "incipient",
            "leak_start_time": 2440,
            "leak_end_time": 6643,
            "leak_peak_time": 4143
        }
    ],
    "975": [
        {
            "node_id": "22",
            "leak_diameter": 0.117829926105,
            "leak_type": "incipient",
            "leak_start_time": 10929,
            "leak_end_time": 12956,
            "leak_peak_time": 11151
        }
    ],
    "976": [
        {
            "node_id": "31",
            "leak_diameter": 0.0444725811206,
            "leak_type": "abrupt",
            "leak_start_time": 10551,
            "leak_end_time": 13574,
            "leak_peak_time": 10551
        }
    ],
    "977": [
        {
            "node_id": "27",
            "leak_diameter": 0.0762226853118,
            "leak_type": "abrupt",
            "leak_start_time": 9496,
            "leak_end_time": 13474,
            "leak_peak_time": 9496
        },
        {
            "node_id": "5",
            "leak_diameter": 0.101971662316,
            "leak_type": "abrupt",
            "leak_start_time": 16183,
            "leak_end_time": 16660,
            "leak_peak_time": 16183
        }
    ],
    "978": [
        {
            "node_id": "20",
            "leak_diameter": 0.0899820417697,
            "leak_type": "incipient",
            "leak_start_time": 9521,
            "leak_end_time": 14749,
            "leak_peak_time": 11236
        },
        {
            "node_id": "29",
            "leak_diameter": 0.0228679728454,
            "leak_type": "abrupt",
            "leak_start_time": 14736,
            "leak_end_time": 14742,
            "leak_peak_time": 14736
        }
    ],
    "981": [
        {
            "node_id": "20",
            "leak_diameter": 0.17519908368,
            "leak_type": "incipient",
            "leak_start_time": 2460,
            "leak_end_time": 3555,
            "leak_peak_time": 3072
        }
    ],
    "982": [
        {
            "node_id": "31",
            "leak_diameter": 0.0956244611123,
            "leak_type": "abrupt",
            "leak_start_time": 1935,
            "leak_end_time": 12703,
            "leak_peak_time": 1935
        }
    ],
    "984": [
        {
            "node_id": "31",
            "leak_diameter": 0.0671514715432,
            "leak_type": "abrupt",
            "leak_start_time": 374,
            "leak_end_time": 3224,
            "leak_peak_time": 374
        }
    ],
    "985": [
        {
            "node_id": "21",
            "leak_diameter": 0.124604266524,
            "leak_type": "incipient",
            "leak_start_time": 1367,
            "leak_end_time": 9200,
            "leak_peak_time": 8256
        },
        {
            "node_id": "25",
            "leak_diameter": 0.0677277826033,
            "leak_type": "incipient",
            "leak_start_time": 13205,
            "leak_end_time": 15258,
            "leak_peak_time": 14608
        }
    ],
    "986": [
        {
            "node_id": "2",
            "leak_diameter": 0.0220918677752,
            "leak_type": "abrupt",
            "leak_start_time": 2577,
            "leak_end_time": 14809,
            "leak_peak_time": 2577
        }
    ],
    "987": [
        {
            "node_id": "8",
            "leak_diameter": 0.169351909678,
            "leak_type": "incipient",
            "leak_start_time": 788,
            "leak_end_time": 3203,
            "leak_peak_time": 1056
        }
    ],
    "988": [
        {
            "node_id": "9",
            "leak_diameter": 0.189799028821,
            "leak_type": "incipient",
            "leak_start_time": 8516,
            "leak_end_time": 17401,
            "leak_peak_time": 13437
        }
    ],
    "989": [
        {
            "node_id": "4",
            "leak_diameter": 0.0258183247034,
            "leak_type": "abrupt",
            "leak_start_time": 2626,
            "leak_end_time": 10828,
            "leak_peak_time": 2626
        },
        {
            "node_id": "14",
            "leak_diameter": 0.173185860031,
            "leak_type": "incipient",
            "leak_start_time": 15729,
            "leak_end_time": 17437,
            "leak_peak_time": 15829
        }
    ],
    "990": [
        {
            "node_id": "20",
            "leak_diameter": 0.0886516267702,
            "leak_type": "incipient",
            "leak_start_time": 850,
            "leak_end_time": 14391,
            "leak_peak_time": 11289
        }
    ],
    "992": [
        {
            "node_id": "23",
            "leak_diameter": 0.0528069829976,
            "leak_type": "abrupt",
            "leak_start_time": 6385,
            "leak_end_time": 12086,
            "leak_peak_time": 6385
        }
    ],
    "993": [
        {
            "node_id": "11",
            "leak_diameter": 0.151554688997,
            "leak_type": "incipient",
            "leak_start_time": 12086,
            "leak_end_time": 14646,
            "leak_peak_time": 12927
        }
    ],
    "994": [
        {
            "node_id": "12",
            "leak_diameter": 0.0260773151805,
            "leak_type": "incipient",
            "leak_start_time": 5868,
            "leak_end_time": 13520,
            "leak_peak_time": 5897
        },
        {
            "node_id": "31",
            "leak_diameter": 0.129626832353,
            "leak_type": "incipient",
            "leak_start_time": 9436,
            "leak_end_time": 10743,
            "leak_peak_time": 10253
        }
    ],
    "995": [
        {
            "node_id": "29",
            "leak_diameter": 0.178513196806,
            "leak_type": "abrupt",
            "leak_start_time": 4793,
            "leak_end_time": 12713,
            "leak_peak_time": 4793
        },
        {
            "node_id": "26",
            "leak_diameter": 0.199975226017,
            "leak_type": "abrupt",
            "leak_start_time": 6537,
            "leak_end_time": 9298,
            "leak_peak_time": 6537
        }
    ],
    "996": [
        {
            "node_id": "12",
            "leak_diameter": 0.139275350336,
            "leak_type": "abrupt",
            "leak_start_time": 15735,
            "leak_end_time": 16888,
            "leak_peak_time": 15735
        }
    ],
    "999": [
        {
            "node_id": "31",
            "leak_diameter": 0.0660608516093,
            "leak_type": "incipient",
            "leak_start_time": 9865,
            "leak_end_time": 10526,
            "leak_peak_time": 10132
        }
    ],
    "1000": [
        {
            "node_id": "26",
            "leak_diameter": 0.178105042575,
            "leak_type": "incipient",
            "leak_start_time": 9570,
            "leak_end_time": 13348,
            "leak_peak_time": 12770
        },
        {
            "node_id": "8",
            "leak_diameter": 0.195922129769,
            "leak_type": "incipient",
            "leak_start_time": 14090,
            "leak_end_time": 15042,
            "leak_peak_time": 14793
        }
    ]
}"""
