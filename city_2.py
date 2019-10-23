import requests
import csv, json

# result_file=open('./result.csv', 'r+', encoding='utf8')
weather=open('./weather.csv', 'r+', encoding='utf8')
record_title=open('./record_title.csv', 'r+', encoding='utf8')

data = {
  'json': '{"action":"login","user":2}'
}
# ,1081000167,2019/10/18 17:39:29,指定主管簽核,PC,公園管理科二股,戴佳男,路燈增設,將軍區,照明不足,路燈增設,2019/10/18,長榮里,經度:120.16957093434 緯度:23.1947298274314X_97坐標:164991.371796955 Y_97坐標:2566089.04157929

# fieldnames = ("pk","id","time","ignore", 'client', 'gov', 'ignore', 'type', 'location', 'problem', 'method', 'date', 'location_2', 'longlat', )
fieldnames=('pk','觀測時間(day)','測站氣壓(hPa)','海平面氣壓(hPa)','測站最高氣壓(hPa)','測站最高氣壓時間(LST)','測站最低氣壓(hPa)','測站最低氣壓時間(LST)','氣溫(℃)','最高氣溫(℃)','最高氣溫時間(LST)','最低氣溫(℃)','最低氣溫時間(LST)'\
                ,'露點溫度(℃)','相對溼度(%)','最小相對溼度(%)','最小相對溼度時間(LST)','風速(m/s)','風向(360degree)','最大陣風(m/s)',\
            '最大陣風風向(360degree)','最大陣風風速時間(LST)','降水量(mm)','降水時數(hour)','最大十分鐘降水量(mm)','最大十分鐘降水量起始時間(LST)',\
            '最大六十分鐘降水量(mm)','最大六十分鐘降水量起始時間(LST)','日照時數(hour)','日照率(%)','全天空日射量(MJ/㎡)','能見度(km)',\
            'A型蒸發量(mm)','日最高紫外線指數','日最高紫外線指數時間(LST)','總雲量(0~10)')
reader=csv.DictReader(weather, fieldnames)
for i in reader:
    print(type(i))
    data={
        'json':json.dumps(i)
    }
    print(data)
    response=requests.post('http://hasdoel.ml:8080/test2.test', data=data)
# response = requests.post('http://hasdoel.ml:8080/test.test', data=data)

