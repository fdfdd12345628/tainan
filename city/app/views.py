from django.shortcuts import render
import itertools
import urllib,json
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

'''
將weather.csv中資料加入db
'''
def processDataWeather(request):
    content = {}
    title = "weather"
    content["DataTitle"] = title
    file = open("csv/"+title+".csv","r", encoding='utf8')
    reader = csv.reader(file)
    bulkCreateList = []
    for row in itertools.islice(reader,6575,None):
        date=datetime.datetime.strptime(row[1],"%Y%m%d")
        for i in [8,14,22,24,26]:
            if row[i] == "T" or row[i] == "X" or row[i] == "...":
                row[i] = 0
        bulkCreateList.append(weather(date=make_aware(date),temperature=float(row[8]),relativeHumidity=float(row[14]),rainfall=float(row[22]),maxTenMinuteRainFall=float(row[24]),maxSixtyMinuteRainFall=float(row[26])))
    weather.objects.bulk_create(bulkCreateList)
    return render(request,"processData.html",content)

'''
將holeWithFloodArea.csv中資料加入db
'''
def processDataHole(request):
    content = {}
    title = "holeWithFloodArea"
    content["DataTitle"] = title
    file = open("csv/" + title + ".csv", "r", encoding='utf8')
    reader = csv.reader(file)
    bulkCreateList = []
    for row in itertools.islice(reader,1,None):
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


'''
利用開放資料平台將資料轉為csv與進入db
'''
def processDataWeatherPredict(request):
    content = {}
    title = "PredictWeather"
    content["DataTitle"] = title
    with urllib.request.urlopen(
            "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-D0047-079?Authorization=CWB-883FDC74-7C90-4E66-9737-B3DB98A00A64&downloadType=WEB&format=JSON") as url:
        data = json.loads(url.read().decode('utf-8-sig'))
    content["content"] = data['cwbopendata']['dataset']['locations']['location']
    with open('csv/predict.csv', 'w+', encoding='utf8') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        header = "區,日期,溫度,平均露點溫度,平均相對濕度,最高溫度,最低溫度,最高體感溫度,最低體感溫度,最大舒適度指數,最小舒適度指數,12小時降雨機率,風向,最大風速,天氣現象,紫外線指數,天氣描述"
        totalRow = []
        totalRow.append(header.split(","))
        for town in data['cwbopendata']['dataset']['locations']['location']:
            for i in range(len(town['weatherElement'][0]['time'])):
                newRow = []
                newRow.append(town['locationName'])
                newRow.append(town['weatherElement'][0]['time'][i]['startTime'])
                for eachMeas in town['weatherElement']:
                    if eachMeas['elementName'] == "UVI":
                        if i%2 == 1:
                            newRow.append(eachMeas['time'][i//2]['elementValue'][0]['value'])
                        else:
                            newRow.append("NONE")
                    else:
                        if isinstance(eachMeas['time'][0]['elementValue'],list):
                            newRow.append(eachMeas['time'][i]['elementValue'][0]['value'])
                        else:
                            newRow.append(eachMeas['time'][i]['elementValue']['value'])
            totalRow.append(newRow)
        writer.writerows(totalRow)
    return render(request,"processData.html",content)


def displayHole(request):
    content = {}
    content["towns"] = [ele['town'] for ele in hole.objects.values('town').distinct()]
    content["reason"] = [ele['reason'] for ele in hole.objects.values('reason').distinct()]
    return render(request,"displayHole.html",content)

'''
利用不同filter 搜尋符合的坑洞位置
'''
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
    holeList = [str(ele.positionLat)+","+str(ele.positionLon)+","+str(ele.id) for ele in holeList]
    content["holeList"] = holeList
    return JsonResponse(content)


'''
回傳該坑洞相對應詳細資料
'''
def searchHoleDetail(request):
    content = {}
    tmpHole = hole.objects.filter(id=request.POST.get("id","")).first()
    print(tmpHole)
    content["reason"] = tmpHole.reason
    content["position"] = str(tmpHole.positionLat) +" , "+ str(tmpHole.positionLon)
    content["detail"] = tmpHole.address
    content["time"] = tmpHole.occurTime.date()
    weatherDate = weather.objects.filter(date=tmpHole.occurTime.date()).first()
    content["temperature"] = str(weatherDate.temperature) + " °C "
    content["rainfall"] = str(weatherDate.rainfall) + "mm"
    return JsonResponse(content)