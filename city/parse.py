import csv
import json
import urllib.request, json
with urllib.request.urlopen("https://data.tainan.gov.tw/dataset/fd25ecb9-7fd3-41e0-b016-6a4427e3ea55/resource/6b7a7899-0ac3-4988-af4d-80fec3a21c90/download/57676_.json") as url:
    data = json.loads(url.read().decode('utf-8-sig'))

#f = csv.writer(open("test.csv", "w+"))

# Write CSV Header, If you dont need that, remove this line
RowList = "TOWN_CODE、TOWN_NAME、AC_NO、CASE_ID、CONST_NAME、LOCATION、A_UN、ABE_DA、AEN_DA、ADG_DA、DACO_TI、AREA_TA、UN_NA、UR_NA、UR_DR、UR_TI、PURP、PH_URLS、DG_STATUS、CL_DA、CHG_TYPE、CBE_DA、CEN_DA、LASTMOD、POLY_LIST".split("、")
#f.writerow(RowList)
with open('names.csv', 'w', newline='') as csvfile:
    fieldnames = RowList
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for x in data:
        writer.writerow(x)
'''
for x in data:

    f.writerow([x["TOWN_CODE"],x["TOWN_NAME"],x["AC_NO"],x["CASE_ID"],x["CONST_NAME"],x["LOCATION"],
                x["A_UN"],x["ABE_DA"],x["AEN_DA"],x["ADG_DA"],x["DACO_TI"],x["AREA_TA"],x["UN_NA"],x["UR_NA"],x["UR_DR"],
                x["UR_TI"],x["PURP"],x["PH_URLS"],x["DG_STATUS"],x["CL_DA"],x["CBE_DA"],x["CEN_DA"],x["LASTMOD"],x["POLY_LIST"],])
    '''
# 無 變更類型