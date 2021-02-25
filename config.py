

colore = {0:'green',1:'red',2:'blue',3:'yellow',4:'black'}
stile = {0:'solid',1:'dashed', 2:'dashdot', 3:'dotted',4:'solid'}
tracciato_qaria=['stazione_id','data','inquinante','valore']
tracciato_meteo=['IdSensore','Data','Valore','Stato','idOperatore']
d_stazioni = {
    'temperature': [8162,5909,2001,5920,5897,5911],
    'umidita': [6179,6597,6174,2002,6185],
    'precipitazioni': [14121,9341,8149,5908,19373,2006]
}

d_stazioni_lombardia={
    'precipitazioni': [22011,5933,22022,5858,14545,8222,2103,43,35,100,40,113,19,20,1366,30890,34,135,42,11,21,8170,8171,8169,2452,9113,2278,10666,14121,12724,4008,24416,11025,2336,8161,9119,14700,2129,6846,2465,19365,17450,6986,2395,9341,8228,19335,9863,2417,8174,4041,17561,5929,8115,9115,5918,8095,8206,2195,9104,19347,8193,6819,9102,14141,9111,2441,8224,8029,14197,8094,8230,9123,17572,8097,2116,17551,8010,8199,8176,8155,46,5128,14120,9095,9109,4065,14119,14365,2535,8149,8139,6723,8006,10443,19344,5927,8160,4089,8197,8004,5048,9106,9101,2596,9118,8211,8167,9816,9122,5921,14765,8163,14567,14712,5916,19295,7043,8021,9096,8195,19443,2477,8587,14384,8208,19390,14253,14128,9110,8179,9308,9098,19356,2239,5908,5894,9097,8182,5884,8015,2492,8213,14605,8126,10373,122,19428,8137,8001,8583,5940,8201,30536,14499,2377,9099,5938,5870,8219,10585,19373,4033,8692,14443,5857,9103,9117,9090,17600,9105,8217,8190,8188,5861,8098,8152,8226,14118,8221,17487,9093,5900,10554,12023,10376,10574,9322,2065,9329,8103,8185,5946,4049,5923,5876,17459,2152,2408,4057,5856,9325,8131,5872,14527,14586,30533,9094,14224,2251,2385,8135,14171,32398,14241,2626,14280,8122,14724,14517,5882,14661,9,9933,14018,8165,4112,30525,9100,8018,14406,8150,4016,2006,17446,2368,19417,116,2502,32382,9114,6792,5902,17131,30539,2140,9116,14741,9092,8172,8111,5934,5859,14664,19377,19403,9108,9107,17437,9091,8215,2614,9120,14476,14131,8173,5887,5931,10465,5878,2206,19309,5860,4025,19026,9112,6694,8025,2089,2046,41],
    'umidita':[22006,19294,32339,32336,6159,22026,14547,2527,4043,32404,2271,9386,2448,6175,10661,6163,4002,24411,12719,2064,17583,14165,19308,2362,6191,17463,6184,14446,14292,19346,2111,14402,6170,2389,17491,14569,32244,2486,19364,2188,11011,9311,11008,4083,6189,11100,14370,9392,14627,9939,8030,4067,9130,2097,6176,14265,6186,14529,9813,11114,6161,14145,32262,17435,4051,11045,10470,9382,4035,14728,19376,14745,9391,6169,8585,9395,17536,9398,9399,6183,14089,14607,6179,32253,19334,6164,4059,19343,9396,2201,6167,6180,32238,14687,6796,9393,12026,14191,17002,19416,6994,6603,14218,11116,6728,32250,6194,4018,2621,32259,14039,19402,14588,32373,14238,10381,9394,6421,2434,32241,14501,9380,14473,6193,9388,6197,2401,11021,11158,14648,32247,14519,6160,14351,11984,32394,19442,2460,6597,4010,2246,19427,2236,9383,6835,9397,2498,2415,19355,14320,6187,9381,2374,6158,14769,6407,7047,2147,11020,10571,5122,17472,2123,11190,19389,14072,6157,9390,8011,9387,6174,6824,14132,9384,9869,14667,2472,14055,6850,6172,6699,7030,14001,2612,2083,17465,2135,2328,2002,6185,10552,9820,2040,12754,4027],
    'temperature':[22003,5865,19293,5910,9027,22023,14546,8223,29,8146,1367,30889,133,54,1346,13,99,30,112,28,9024,8133,8134,2447,2270,14257,10658,6698,5932,4001,24408,12716,14725,8166,7046,2613,8164,8013,14092,9034,9014,9017,5890,19401,17585,19363,2497,8162,19415,8178,5873,14665,11044,9002,14528,11216,4042,5939,14125,5968,14139,5864,14130,5863,8584,5909,2388,5922,2235,9020,17488,8140,14242,19426,17573,14058,8116,5941,10551,8016,8200,11007,5935,2524,19441,9026,2414,14684,6727,19354,14518,9004,2096,17443,2134,8218,8186,9008,10570,5895,17451,2361,4066,5928,2001,19342,14478,6992,8198,9938,9310,9001,8002,8207,9819,8096,19345,14221,14606,9030,5903,19333,8214,2187,14500,8145,2459,9018,8005,32370,8151,8196,5901,17562,12025,17001,5966,8027,5888,2373,14766,5868,6823,9015,9021,9007,8019,17432,14367,8229,19375,14348,2471,5920,8180,32401,19388,14645,8225,5917,9033,2063,8216,5121,2122,8092,9868,6849,115,2245,8007,9812,5866,9022,5969,8136,2082,121,4082,6834,9016,8187,17552,8189,9031,10469,2485,8127,8104,9011,4017,8212,2400,14399,2110,2200,8191,4058,5924,2327,14317,4050,5877,8227,5897,10377,14587,7029,32391,8588,19307,17460,8123,5871,2146,14075,14194,14014,14284,9023,5947,5883,8220,6795,9009,8157,9003,2433,4034,5867,17580,14568,8168,5911,9029,2620,14445,8209,8138,4009,9012,8184,9019,9006,9005,8202,9025,9010,5930,9013,8008,14742,53,2039,11144]
}

nome_colonna_data='data'
nome_colonna_valore='valore'

nome_colonna_data_meteo='Data'
nome_colonna_valore_meteo='Valore'

sep_qaria=','
skip_qaria=1

sep_meteo=','
skip_meteo=0