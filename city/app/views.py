from django.shortcuts import render
import itertools
import csv
import datetime
from django.http import JsonResponse
from django.utils.timezone import make_aware
from .models import weather,hole
from .water import water

# Create your views here.
def googleMap(request):
    content = {}
    # water 為淹水淺勢圖
    tmpWater = water()
    content['LowWater'] = tmpWater[0]
    content['MidWater'] = tmpWater[1]
    content['HighWater'] = tmpWater[2]
    content['THighWater'] = tmpWater[3]

    content['hole'] = holePos()
    return render(request,"map.html",content)


def holePos():
    returnList = []
    file = open("csv/result.csv",'r', encoding='utf8')
    reader = csv.reader(file)
    for row in reader:
        if row[9] == "鋪面":
            tmpList = row[13].split("X_97")[0].split(" ")
            returnList.append(" "+tmpList[1][3:]+","+tmpList[0][3:])
    return returnList


def processDataWeather(request):
    content = {}
    title = "weather"
    content["DataTitle"] = title
    file = open("csv/"+title+".csv","r", encoding='utf8')
    reader = csv.reader(file)
    bulkCreateList = []
    for row in itertools.islice(reader,6575,7228):
        date=datetime.datetime.strptime(row[1],"%Y%m%d")
        for i in [8,14,22,24,26]:
            if row[i] == "T" or row[i] == "X":
                row[i] = 0
        bulkCreateList.append(weather(date=make_aware(date),temperature=float(row[8]),relativeHumidity=float(row[14]),rainfall=float(row[22]),maxTenMinuteRainFall=float(row[24]),maxSixtyMinuteRainFall=float(row[26])))
    weather.objects.bulk_create(bulkCreateList)
    return render(request,"processData.html",content)

def processDataHole(request):
    content = {}
    title = "holeWithFloodArea"
    content["DataTitle"] = title
    file = open("csv/" + title + ".csv", "r", encoding='utf8')
    reader = csv.reader(file)
    bulkCreateList = []
    for row in itertools.islice(reader,1,696):
        occurTime=datetime.datetime.strptime(row[2],"%Y/%m/%d %H:%M:%S")
        tmp = row[13].split("X_97")[0].split(" ")
        lon = tmp[0]
        lat = tmp[1]
        bulkCreateList.append(hole(town=row[8],positionLat=float(lat[3:]),positionLon=float(lon[3:]),occurTime=make_aware(occurTime),reason=row[7],address=row[12],flood=row[14]))
    hole.objects.bulk_create(bulkCreateList)
    return render(request,"processData.html",content)

def processDataHoleWithRoad(request):
    content = {}
    title = "holeWithFloodArea"
    content["DataTitle"] = title
    file = open("csv/" + title + ".csv", "r", encoding='utf8')
    reader = csv.reader(file)
    bulkCreateList = []
    for row in itertools.islice(reader,1,696):
        occurTime=datetime.datetime.strptime(row[2],"%Y/%m/%d %H:%M:%S")
        tmp = row[13].split("X_97")[0].split(" ")
        lon = tmp[0]
        lat = tmp[1]
        bulkCreateList.append(hole(town=row[8],positionLat=float(lat[3:]),positionLon=float(lon[3:]),occurTime=make_aware(occurTime),reason=row[7],address=row[12],flood=row[14]))
    hole.objects.bulk_create(bulkCreateList)
    return render(request,"processData.html",content)



def displayHole(request):
    content = {}
    content["towns"] = [ele['town'] for ele in hole.objects.values('town').distinct()]
    content["reason"] = [ele['reason'] for ele in hole.objects.values('reason').distinct()]
    return render(request,"displayHole.html",content)


def searchHole(request):
    content = {}
    holeList = hole.objects.all()
    filterTowns = request.POST.getlist("towns[]","")
    filterReasons = request.POST.getlist("reasons[]","")
    filterDates = request.POST.get("dates","")
    if filterTowns != "":
        holeList = holeList.filter(town__in = filterTowns)
    if filterReasons != "":
        holeList = holeList.filter(reason__in = filterReasons)
    if filterDates != "":
        filterStartDate = make_aware(datetime.datetime.strptime(filterDates.split(" - ")[0],"%m/%d/%Y"))
        filterEndDate = make_aware(datetime.datetime.strptime(filterDates.split(" - ")[1],"%m/%d/%Y"))
        holeList = holeList.filter(occurTime__range=(filterStartDate,filterEndDate))
    holeList = [str(ele.positionLat)+","+str(ele.positionLon) for ele in holeList]
    content["holeList"] = holeList
    return JsonResponse(content)