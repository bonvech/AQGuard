import sys
#import socket
#import time
#import datetime
#from   datetime import datetime
#import matplotlib.pyplot as plt
import pandas as pd
#import os


def convert_line(line):
    #print(line)
    line = line.strip().split(";")
    data = (line[:2] 
         + [par.strip().split("=")[1] for par in line[2:-1]] 
         + line[-1:])
    
    columns = (["date", "timestamp"] 
         + [column_from_numbers(int(par.strip().split("=")[0])) for par in line[2:-1]] 
         + ["checksum"])
    if len(line) != 105:
        print(len(line))
        #print(line)
    
    return dict(zip(columns, data))


def convert_raw_file_to_csv(filename):
    ##  open raw file
    rawdata = open(filename).readlines()
    #line = convert_line(rawdata[0])
    #print(line)
    
    ##  convert
    data = [convert_line(line) for line in rawdata]
    data = pd.DataFrame(data)
    
    ##  save files
    data.to_csv(filename[:-8].replace("raw", "table") + ".csv", index=False)
    data.to_csv(filename[:-8].replace("raw", "table") + ".txt", index=False, sep="\t")
    #print(data) 
    #print(*data.columns)
    #print(column_from_numbers(51))


def column_from_numbers(column):
    ## "timestamp	timestampUTC	averaging[s]	PM1 [痢/m設	PM2.5 [痢/m設	PM4 [痢/m設	PM10 [痢/m設	PMtot [痢/m設	CO2 [ppm]	VOC [mg/m設	SO2 [痢/m設	NO2 [痢/m設	O3 [痢/m設	CO [mg/m設	NH3 [ppm]	Cn [1/cm設	M1,0 [痠]	M2,0 [痠淫	M3,0 [痠設	x10(dCn) [痠]	x16(dCn) [痠]	x50(dCn) [痠]	x84(dCn) [痠]	x90(dCn) [痠]	T [蚓]	p [hPa]	rH [%]	wind speed [km/h]	wind direction [財	wind signal quality [%]	volume flow [l/min]	power (volume flow blower) [%]	GPS latitude [財	GPS longitude [財	global error	dCn(痠) [1/cm設	0.10373	0.111469	0.119786	0.128723	0.138327	0.148647	0.159737	0.171655	0.184462	0.198224	0.213013	0.228905	0.245984	0.264336	0.284057	0.30525	0.328024	0.352497	0.378797	0.407058	0.437427	0.470063	0.505133	0.54282	0.583319	0.626839	0.673606	0.723862	0.777868	0.835903	0.898268	0.965286	1.037304	1.114695	1.19786	1.28723	1.383267	1.48647	1.597372	1.716548	1.844616	1.982239	2.13013	2.289054	2.459835	2.643358	2.840573	3.052502	3.280243	3.524975	3.787966	4.070577	4.374274	4.70063	5.051333	5.428202	5.833189	6.26839	6.736061	7.238624	7.778682	8.359033	8.982682	9.65286	10.373039	11.146949	11.978599	12.872296	13.83267	14.864696	15.973718	17.165483	18.446162	19.82239	21.301296	22.890539	24.598353	26.433582	28.405734	30.525025	32.80243	35.249749	37.879656	40.705775	43.742744	47.006295	50.513333	54.282023	58.331887	62.683902	67.360612	72.386241	77.786821	83.590327	89.82682
    ### columns from device text datafile
    cdevice = [
        "timestamp", "timestampUTC", "averaging[s]",
        "PM1", "PM2.5", "PM4", "PM10", "PMtot", 
        "CO2 [ppm]", "VOC [mg/]", "SO2[]", "NO2 [痢/m設", "O3 [/]", "CO [mg/m]", "NH3 [ppm]", "Cn [1/cm]", 
        "M1,0 [痠]", "M2,0 [痠淫", "M3,0 [痠設", 
        "x10(dCn) [痠]", "x16(dCn) [痠]", "x50(dCn) [痠]", "x84(dCn) [痠]", "x90(dCn) [痠]",
        "T [蚓]", "p [hPa]", "rH [%]", 
        "wind speed [km/h]", "wind direction [財", "wind signal quality [%]", 
        "volume flow [l/min]", "power (volume flow blower) [%]", 
        "GPS latitude", "GPS longitude", "global error", 
        "dCn(痠) [1/cm]", 
        "0.10373",  "0.111469", "0.119786", "0.128723", "0.138327", 
        "0.148647", "0.159737", "0.171655", "0.184462", "0.198224", 
        "0.213013", "0.228905", "0.245984", "0.264336", "0.284057", 
        "0.30525",  "0.328024", "0.352497", "0.378797", "0.407058", 
        "0.437427", "0.470063", "0.505133", "0.54282",  "0.583319", 
        "0.626839", "0.673606", "0.723862", "0.777868", "0.835903", 
        '0.898268', '0.965286', '1.037304', '1.114695', '1.19786', 
        '1.28723',  '1.383267', '1.48647',  '1.597372', '1.716548', 
        '1.844616', '1.982239', '2.13013',  '2.289054', '2.459835', 
        '2.643358', '2.840573', '3.052502', '3.280243', '3.524975', 
        '3.787966', '4.070577', '4.374274', '4.70063',  '5.051333', 
        '5.428202', '5.833189', '6.26839',  '6.736061', '7.238624', 
        '7.778682', '8.359033', '8.982682', '9.65286', '10.373039', 
        '11.146949', '11.978599', '12.872296', '13.83267',  '14.864696', 
        '15.973718', '17.165483', '18.446162', '19.82239',  '21.301296', 
        '22.890539', '24.598353', '26.433582', '28.405734', '30.525025', 
        '32.80243',  '35.249749', '37.879656', '40.705775', '43.742744', 
        '47.006295', '50.513333', '54.282023', '58.331887', '62.683902', 
        '67.360612', '72.386241', '77.786821', '83.590327', '89.82682'
         ]
        
    columns_ip = {
        0: "Volume Flow",
        1: "Suction Status",
        2: "IADS Status",
        3: "Sensor Calibration Status",
        4: "Sensor LED Status",
        5: "Sensor Data Status",
        6: "Sensor Noise Status",
        23: "Aerosol pump output [%]",
        24: "Temperature of IADS [C°]",
        26: "Temperature of LED [C°]",
        27: "Volume flow [l/min]",
        35: "Air Quality Index AQI [%]",
        36: "Infection Risk Index [%]",
        40: "Air temperature [C°]",
        41: "Relative humidity [%]",
        42: "Wind speed [km/h]",
        43: "Wind direction [°]",
        44: "Precipitation intensity [l/m²/h]",
        45: "Precipitation type",
        46: "Temperature dew point [°C]",
        47: "Air pressure [hPa]",
        48: "Wind signal quality",
        50: "CO2 [ppm]",
        51: "VOC [mg/m3]",
        52: "SO2 [µg/m³]",
        53: "NO2 [µg/m³]",
        54: "O3 [µg/m³]",
        55: "CO [mg/m³]",
        56: "NH3 [ppm]",
        60: "Cn [P/cm3]",
        61: "PM1 [µg/m3]",
        62: "PM2.5 [µg/m3]",
        63: "PM4 [µg/m3]",
        64: "PM10 [µg/m3]",
        65: "PMtotal [µg/m3]",
        77: "PM2.5_CE [µg/m³]",
        78: "PM10_CE [µg/m³]",
        #110 Number concentration
        110: 0.18445,
        111: 0.19825,
        112: 0.21305,
        113: 0.2289,
        114: 0.24595,
        115: 0.2643,
        116: 0.28405,
        117: 0.30525,
        118: 0.328,
        119: 0.3525,
        120: 0.3788,
        121: 0.40705,
        122: 0.43745,
        123: 0.4701,
        124: 0.50515,
        125: 0.5428,
        126: 0.5833,
        127: 0.62685,
        128: 0.6736,
        129: 0.72385,
        130: 0.77785,
        131: 0.8359,
        132: 0.8983,
        133: 0.9653,
        134: 1.0373,
        135: 1.1147,
        136: 1.19785,
        137: 1.2872,
        138: 1.38325,
        139: 1.48645,
        140: 1.59735,
        141: 1.71655,
        142: 1.84465,
        143: 1.98225,
        144: 2.1301,
        145: 2.28905,
        146: 2.45985,
        147: 2.64335,
        148: 2.84055,
        149: 3.0525,
        150: 3.28025,
        151: 3.52495,
        152: 3.78795,
        153: 4.0706,
        154: 4.3743,
        155: 4.70065,
        156: 5.05135,
        157: 5.4282,
        158: 5.8332,
        159: 6.2684,
        160: 6.73605,
        161: 7.2386,
        162: 7.77865,
        163: 8.359,
        164: 8.98265,
        165: 9.65285,
        166: 10.37305,
        167: 11.14695,
        168: 11.9786,
        169: 12.8723,
        170: 13.83265,
        171: 14.8647,
        172: 15.97375,
        173: 17.1655
    }
        
    return columns_ip[column] if column in columns_ip.keys() else column



if __name__ == "__main__":
    filename = "data/raw/2024_07_AQ_raw.txt"
    convert_raw_file_to_csv(filename)
    