import urllib.request, json, csv
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def water():
    returnList = [[],[],[],[]]
    with urllib.request.urlopen(
            "https://data.tainan.gov.tw/dataset/693903b4-5412-459c-bc3d-f62a12e7187b/resource/d57633ea-f32e-46f5-a083-35d95c1b0631/download/cityq500.json") as url:
        data = json.loads(url.read().decode('utf-8-sig'))

    for ele in data['features']:
        for el in ele['geometry']['coordinates']:
            for eltmp in el:
                tmpstr = ""
                for e in eltmp:
                    tmpstr += " "+str(e[1]) + "," + str(e[0])
                returnList[ele['properties']['CLASS']-1].append(tmpstr[1:])
    with urllib.request.urlopen(
            "https://data.tainan.gov.tw/dataset/693903b4-5412-459c-bc3d-f62a12e7187b/resource/85dd0e50-e7a0-43c8-ae82-3c518d265f58/download/countyq500.json") as url:
        data = json.loads(url.read().decode('utf-8-sig'))

    for ele in data['features']:
        for el in ele['geometry']['coordinates']:
            for eltmp in el:
                tmpstr = ""
                for e in eltmp:
                    tmpstr += " "+str(e[1]) + "," + str(e[0])
                returnList[ele['properties']['CLASS']-1].append(tmpstr[1:])
    return returnList

def polyWater():
    returnList = [[],[],[],[]]
    with urllib.request.urlopen(
            "https://data.tainan.gov.tw/dataset/693903b4-5412-459c-bc3d-f62a12e7187b/resource/d57633ea-f32e-46f5-a083-35d95c1b0631/download/cityq500.json") as url:
        data = json.loads(url.read().decode('utf-8-sig'))

    for ele in data['features']:
        for el in ele['geometry']['coordinates']:
            for eltmp in el:
                tmp =[]
                for e in eltmp:
                    tmp.append([float(e[1]),float(e[0])])
                returnList[ele['properties']['CLASS']-1].append(tmp)
    with urllib.request.urlopen("https://data.tainan.gov.tw/dataset/693903b4-5412-459c-bc3d-f62a12e7187b/resource/85dd0e50-e7a0-43c8-ae82-3c518d265f58/download/countyq500.json") as url:
        data = json.loads(url.read().decode('utf-8-sig'))
    for ele in data['features']:
        for el in ele['geometry']['coordinates']:
            for eltmp in el:
                tmp = []
                for e in eltmp:
                    tmp.append([float(e[1]), float(e[0])])
                returnList[ele['properties']['CLASS'] - 1].append(tmp)
    return returnList

def hole():
    returnDict = {}
    file = open("../csv/result.csv",'r')
    reader = csv.reader(file)
    for row in reader:
        if row[9] == "鋪面":
            tmpList = row[13].split("X_97")[0].split(" ")
            returnDict[row[0]] = [float(tmpList[1][3:]), float(tmpList[0][3:])]
    return returnDict

'''
'''
tmpList = polyWater()
ansDict = {}
disDict = []
classify = 4
pointDict = hole()
count = 0
for level in tmpList[::-1]:
    print(classify)
    for route in level:
        polygon=Polygon(np.array(route))
        for key in list(pointDict.keys()):
            point = Point(pointDict[key][0],pointDict[key][1])
            if point.within(polygon):
                count +=1
                ansDict[key] = classify
                del pointDict[key]
    calculateDict = {}
    for route in level:
        polygon = Polygon(np.array(route))
        for key in list(pointDict.keys()):
            point = Point(pointDict[key][0],pointDict[key][1])
            if key in calculateDict:
                calculateDict[key] = min(polygon.exterior.distance(point),calculateDict[key])
            else:
                calculateDict[key] = polygon.exterior.distance(point)
    disDict.append(calculateDict)
    classify -= 1
with open('../csv/result.csv','r') as csvinput:
    with open('../csv/holeWithFloodArea.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)
        all = []
        row = next(reader)
        row.append('flood')
        row.append('distance_to_4')
        row.append('distance_to_3')
        row.append('distance_to_2')
        row.append('distance_to_1')
        all.append(row)

        for row in reader:
            if row[9] == "鋪面":
                if row[0] in ansDict:
                    row.append(ansDict[row[0]])
                    row.append(0)
                    row.append(0)
                    row.append(0)
                    row.append(0)
                else:
                    row.append(-1)
                    row.append(disDict[0][row[0]])
                    row.append(disDict[1][row[0]])
                    row.append(disDict[2][row[0]])
                    row.append(disDict[3][row[0]])
                all.append(row)

        writer.writerows(all)
