from django.shortcuts import render
import urllib.request, json
import csv
import pyproj
from .water import water

# Create your views here.
def googleMap(request):
    content = {}
    # twd97 資料庫為施工地點案件範圍點位
    #twd97 = "170775.9394 2544165.3128,170774.3878 2544166.4764,170787.5753 2544167.6394,170787.9633 2544165.7001,170775.9394 2544165.3128"
    #content['LatLon'] = transfer(twd97)
    # water 為淹水淺勢圖
    tmpWater = water()
    content['LowWater'] = tmpWater[0]
    content['MidWater'] = tmpWater[1]
    content['HighWater'] = tmpWater[2]
    content['THighWater'] = tmpWater[3]

    tmpGroundList = ground()
    content['LowGround'] = tmpGroundList[0]
    content['MidGround'] = tmpGroundList[1]
    content['HighGround'] = tmpGroundList[2]
    content['hole'] = hole()
    return render(request,"map.html",content)


def transfer(twd97):
    TWD97 = pyproj.Proj(init='epsg:3826')  # 定義TWD97坐標系
    WGS84 = pyproj.Proj(init='epsg:4326')  # 定義WGS84坐標系
    wgs84=""
    for line in twd97.split(','):
        t = line.split()  # separate each column, using "space"
        lon, lat = pyproj.transform(TWD97, WGS84, t[0], t[1])
        # 將TWD97坐標轉成WGS84經緯度
        wgs84 += " "+str(lat)+","+str(lon)
        print(lat,lon)
    return wgs84[1:]


def ground():
    returnList = [[],[],[]]
    # low,medium,high
    with urllib.request.urlopen(
            "https://data.tainan.gov.tw/dataset/175c9778-62d5-4bb4-b19a-1d8171632ce4/resource/1ff9b2d6-9764-45b5-940d-c72073b6b469/download/liquefaction.json") as url:
        data = json.loads(url.read().decode('utf-8-sig'))
    for ele in data['features']:
        for el in ele['geometry']['coordinates']:
            tmpstr = ""
            for e in el:
                tmpstr += " "+str(e[1]) + "," + str(e[0])
            returnList[ele['properties']['classify']].append(tmpstr[1:])
    return returnList


def hole():
    returnList = []
    file = open("result.csv",'r')
    reader = csv.reader(file)
    for row in reader:
        if row[9] == "鋪面":
            tmpList = row[13].split("X_97")[0].split(" ")
            returnList.append(" "+tmpList[1][3:]+","+tmpList[0][3:])
    return returnList

