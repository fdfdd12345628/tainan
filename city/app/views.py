from django.shortcuts import render
import itertools
import urllib,json
import csv
import os
import datetime
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.utils.timezone import make_aware
from .models import weather,hole,examination
from .water import water
from django.conf import settings
import base64
from .app import *
from django.shortcuts import redirect

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
        content["downloadURL"] = "predict.csv"
    return render(request,"downloadData.html.html",content)


def displayHole(request):
    content = {}
    content["towns"] = [ele['town'] for ele in hole.objects.values('town').distinct()]
    content["reason"] = [ele['reason'] for ele in hole.objects.values('reason').distinct()]
    holeList = hole.objects.all()
    holeList = [str(ele.positionLat) + "," + str(ele.positionLon) + "," + str(ele.id) for ele in holeList]
    content["holeList"] = holeList
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
    content["reason"] = tmpHole.reason
    content["position"] = str(tmpHole.positionLat) +" , "+ str(tmpHole.positionLon)
    content["detail"] = tmpHole.address
    content["time"] = tmpHole.occurTime.date()
    weatherDate = weather.objects.filter(date=tmpHole.occurTime.date()).first()
    content["temperature"] = str(weatherDate.temperature) + " °C "
    content["rainfall"] = str(weatherDate.rainfall) + "mm"
    return JsonResponse(content)


'''
下載不同維度區塊的資料
'''
def downloadSplitData(request, id):
    content = {}
    content["DataTitle"] = "downSplitData"+str(id)
    '''
    水平總長： 17168.92 m
    垂直總長： 12314.61 m 
    '''
    columnNum = 17168.92 // id + 1  # 根據切割長度計算欄數
    rowNum = 12314.61 // id +1
    if os.path.isfile('csv/區塊坑洞挖掘紀錄_' + str(id) + '公尺.json'):
        pass
    else:
        if os.path.isfile('csv/區塊坑洞挖掘紀錄_' + str(id) + '公尺.csv'):
            pass
        else:
            # 轉區塊坑洞機錄
            with open('csv/result_with_1year_digging.csv', 'r',encoding="utf8") as csvinput:
                with open('csv/區塊坑洞挖掘紀錄_'+str(id)+'公尺.csv', 'w+', encoding='utf8') as csvoutput:
                    writer = csv.writer(csvoutput, lineterminator='\n')
                    reader = csv.reader(csvinput)
                    all = []
                    row = next(reader)
                    row.append('splitArea')
                    all.append(row)
                    for row in reader:
                        if row[9] == "鋪面":
                            tmpList = row[13].split("X_97")[0].split(" ")
                            longitude = float(tmpList[0][3:])
                            latitude = float(tmpList[1][3:])
                            if 120.143344802625 < longitude < 120.31099515462 and 22.9608991322419 < latitude < 23.0722689885349:
                                unitX = ( (longitude - 120.143344802625) * 102409.09 ) // id + 1
                                unitY = (latitude - 22.9608991322419) * 110574 // id
                                row.append(unitY * columnNum + unitX)
                                all.append(row)
                    writer.writerows(all)
            csvoutput.close()
            csvinput.close()
            # 轉區塊施工紀錄
            with open('csv/施工紀錄.csv', 'r', encoding="utf8") as csvinput:
                with open('csv/區塊施工紀錄_' + str(id) + '公尺.csv', 'w+', encoding='utf8') as csvoutput:
                    writer = csv.writer(csvoutput, lineterminator='\n')
                    reader = csv.reader(csvinput)
                    all = []
                    row = next(reader)
                    row.append('splitArea')
                    all.append(row)
                    for row in reader:
                        tmpList = row[8].split(",")
                        longitude = float(tmpList[0][1:])
                        latitude = float(tmpList[1][1:-1])
                        if 120.143344802625 < longitude < 120.31099515462 and 22.9608991322419 < latitude < 23.0722689885349:
                            unitX = ((longitude - 120.143344802625) * 102409.09) // id + 1
                            unitY = (latitude - 22.9608991322419) * 110574 // id
                            row.append(unitY * columnNum + unitX)
                            all.append(row)
                    writer.writerows(all)
            csvoutput.close()
            csvinput.close()
        # 由csv的紀錄 轉為不同時間區段的二維分佈
        # channel_hole 坑洞的二維分佈
        with open('csv/區塊坑洞挖掘紀錄_'+str(id)+'公尺.csv', 'r', encoding='utf8') as csvinputsecond:
            reader = csv.reader(csvinputsecond)
            tmpJson = {} # record count of each splitarea
            tmpJson["data"] = []
            row = next(reader)
            startTime = datetime.datetime(2019,1,7)
            endTime = startTime + datetime.timedelta(days = 7) # 時間間隔為７天
            tmpDict = {"startTime" : startTime.strftime("%Y/%m/%d"),
                       "endTime": endTime.strftime("%Y/%m/%d")}
            #channel_hole = [[0] * int(columnNum)] * int(rowNum)
            channel_hole = [[0 for x in range(int(columnNum))] for y in range(int(rowNum))]
            for row in reversed(list(reader)):
                if startTime < datetime.datetime.strptime(row[2],'%Y/%m/%d %H:%M:%S') < endTime:
                    colN = int(float(row[15]) % columnNum -1) # 放入channel
                    rowN = int(float(row[15]) // columnNum)
                    channel_hole[rowN][colN] += 1
                else:
                    if datetime.datetime.strptime(row[2],'%Y/%m/%d %H:%M:%S') < startTime:
                        continue
                    tmpDict["channel_hole"] = channel_hole
                    tmpJson["data"].append(tmpDict)
                    startTime = startTime + datetime.timedelta(days= 7) # 時間間隔為７天 (next week)
                    endTime = endTime + datetime.timedelta(days= 7)
                    if endTime == datetime.datetime(2019,10,28): # 最後一筆
                        break
                    tmpDict = {"startTime": startTime.strftime("%Y/%m/%d"),
                               "endTime": endTime.strftime("%Y/%m/%d")}
                    channel_hole = [[0 for x in range(int(columnNum))] for y in range(int(rowNum))]
            csvinputsecond.close()
        # channel_roadwork 施工的二維分佈
        for eachdict in tmpJson["data"]:
            startTime = datetime.datetime.strptime(eachdict["startTime"],"%Y/%m/%d") - datetime.timedelta(weeks= 52) # 從一年前開始查詢
            endTime = datetime.datetime.strptime(eachdict["endTime"],"%Y/%m/%d") # 最終結束時間 即坑洞記錄時間
            '''
                endTime 要設定為 記錄週的第一天or最後一天
            '''
            channel_roadwork = [[0 for x in range(int(columnNum))] for y in range(int(rowNum))]
            with open('csv/區塊施工紀錄_' + str(id) + '公尺.csv', 'r', encoding='utf8') as csvinputthird:
                reader_roadwork = csv.reader(csvinputthird)
                next(reader_roadwork)
                for row in reader_roadwork:
                    if startTime < datetime.datetime.strptime(row[3],"%Y.%m.%d"):
                        if datetime.datetime.strptime(row[3],"%Y.%m.%d") > endTime:
                            break
                        colN = int(float(row[9]) % columnNum - 1)  # 放入channel
                        if int(float(row[9]) % columnNum) == 0:
                            rowN = int(float(row[9]) // columnNum) - 1
                        else:
                            rowN = int(float(row[9]) // columnNum)
                        channel_roadwork[rowN][colN] += 1
                    else:
                        continue
                eachdict["channel_roadwork"] = channel_roadwork
        # 人口密度的二維分佈
        population_density = [[0 for x in range(int(columnNum))] for y in range(int(rowNum))]
        PD_forArea = {"中西區":12526, "北區":12608, "東區":13864, "南區":4575, "安南區":1811, "永康區":5852, "安平區":6061, "仁德":1498, "新化":697, "歸仁":1220, "default": 8185}
        with open('csv/區塊坑洞挖掘紀錄_' + str(id) + '公尺.csv', 'r', encoding='utf8') as csvinputfourth:
            reader_populationDensity = csv.reader(csvinputfourth)
            next(reader_populationDensity)
            for row in reader_populationDensity:
                colN = int(float(row[15]) % columnNum - 1)  # 放入channel
                rowN = int(float(row[15]) // columnNum)
                if population_density[rowN][colN] == 0:
                    if row[8] in PD_forArea:
                        population_density[rowN][colN] = PD_forArea[row[8]]
            for i in range(int(rowNum)):
                for j in range(int(columnNum)):
                    if population_density[i][j] == 0:
                        population_density[i][j] = PD_forArea["default"]
            csvinputfourth.close()
        tmpJson["population_density"] = population_density
        content["json"] = tmpJson
        with open('csv/區塊坑洞挖掘與施工紀錄_'+str(id)+'公尺.json', 'w+') as outfile:
            json.dump(tmpJson, outfile)
    content["downloadURL"] = '區塊坑洞挖掘與施工紀錄_'+str(id)+'公尺.json'
    return render(request,"downloadData.html",content)


def showingPathAuto(request):
    t = datetime.datetime.today()
    date = int(str(t.year)+str(t.month)+str(t.day))
    #showingPath(request,date)
    return HttpResponseRedirect('showingPath/'+str(date))


def showingPath(request,date):
    if request.method == "GET":
        meter = "1000"
        '''
        if date == 20191216:
            route = [72,73,74,75,60,59,58,57]
        else:
            route =[75,60,59,58,57]
        '''
        #print(datetime.datetime.strftime(datetime.datetime.strptime(str(date),"%Y%m%d"),"%Y/%m/%d"))
        astarMapRaw = gen_pred_hole(datetime.datetime.strftime(datetime.datetime.strptime(str(date),"%Y%m%d")-datetime.timedelta(weeks=15),"%Y/%m/%d"))
        print(astarMapRaw)
        astarMap = []
        for ele in astarMapRaw:
            eleRow = ele // 16
            eleCol = ele % 16
            astarMap.append(eleCol+eleRow*18)
        route = astarMap
        content = {}
        with open('csv/區塊施工紀錄_' + meter + '公尺.csv', 'r', encoding="utf8") as csvinput:
            reader = csv.reader(csvinput)
            readerDic = {}
            row = next(reader)
            for row in reader:
                if row[9] in readerDic:
                    readerDic[int(float(row[9]))].append([float(row[8].split(",")[0][1:]),float(row[8].split(",")[1][1:-1])])
                else:
                    readerDic[int(float(row[9]))] = []
                    readerDic[int(float(row[9]))].append([float(row[8].split(",")[0][1:]),float(row[8].split(",")[1][1:-1])])
        routeList = []
        for spot in route:
            if spot in readerDic:
                routeList.append(readerDic[spot][0])
        content["routeList"] = routeList
        content["routeListLen"] = len(routeList)-1
        print(routeList)
        return render(request,"map.html",content)
    elif request.method == "POST":
        # create data in examination class
        # fields of positionLon, positionLat, examinationTime, photoURL
        content ={}
        if(request.POST.get("type","") == "uploadPhoto"):
            try:
                positionLon = float(request.POST.get("positionLon","120.2224724"))
                positionLat = float(request.POST.get("positionLat","22.996805"))
                saveExamination = examination.objects.create(positionLon=positionLon,positionLat=positionLat)
                saveExamination.save()
                photoByte64 = request.POST.get("photoByte64", "")
                if photoByte64 != "":
                    photoByte64 = photoByte64.split(",")[1]
                    photoURL = "."+settings.MEDIA_URL+str(saveExamination.id)+".png"
                    saveExamination.photoURL=photoURL
                    saveExamination.save()
                    imgdata = base64.b64decode(photoByte64)
                    with open(photoURL, 'wb') as f:
                        f.write(imgdata)
                return JsonResponse(content)
            except:
                return HttpResponse(500)



def pastMap(request):
    if request.method == "GET":
        content={}
        currentTime=datetime.datetime.today()
        currentTimeYest = currentTime - datetime.timedelta(days=1)
        startTime = make_aware(datetime.datetime(currentTimeYest.year,currentTimeYest.month,currentTimeYest.day,16,0,0))
        endTime = make_aware(datetime.datetime(currentTime.year,currentTime.month,currentTime.day,16,0,0))
        examinationSet = examination.objects.filter(examinationTime__range=(startTime,endTime))
        examinationList  =[ {"positionLon": ele.positionLon,
                             "positionLat": ele.positionLat,
                             "examinationTime": (ele.examinationTime + datetime.timedelta(hours=8)).strftime("%Y/%m/%d %H-%M-%S"),
                             "photoURL": ele.photoURL} for ele in examinationSet ]
        content["examinationList"] = examinationList
        return render(request,"pastMap.html",content)
    elif request.method == "POST":
        content={}
        requestDate = request.POST.get("date","")
        currentTime = datetime.datetime.strptime(requestDate,"%m/%d/%Y")
        currentTimeYest = currentTime - datetime.timedelta(days=1)
        startTime = make_aware(datetime.datetime(currentTimeYest.year, currentTimeYest.month, currentTimeYest.day, 16, 0, 0))
        endTime = make_aware(datetime.datetime(currentTime.year, currentTime.month, currentTime.day, 16, 0, 0))
        examinationSet = examination.objects.filter(examinationTime__range=(startTime, endTime))
        examinationList = [{"positionLon": ele.positionLon,
                        "positionLat": ele.positionLat,
                        "examinationTime": (ele.examinationTime + datetime.timedelta(hours=8)).strftime(
                            "%Y/%m/%d %H-%M-%S"),
                        "photoURL": ele.photoURL} for ele in examinationSet]
        content["examinationList"] = examinationList
        return JsonResponse(content)

def statistic(request):
    return render(request,"statistic.html")