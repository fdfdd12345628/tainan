import urllib.request, json, csv

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