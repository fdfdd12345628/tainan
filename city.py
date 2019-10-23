import requests
import csv, json

result_file=open('./result.csv', 'r+', encoding='utf8')
weather=open('./weather.csv', 'r+', encoding='utf8')
record_title=open('./record_title.csv', 'r+', encoding='utf8')

data = {
  'json': '{"action":"login","user":2}'
}
# ,1081000167,2019/10/18 17:39:29,指定主管簽核,PC,公園管理科二股,戴佳男,路燈增設,將軍區,照明不足,路燈增設,2019/10/18,長榮里,經度:120.16957093434 緯度:23.1947298274314X_97坐標:164991.371796955 Y_97坐標:2566089.04157929

fieldnames = ("pk","id","time","ignore", 'client', 'gov', 'ignore', 'type', 'location', 'problem', 'method', 'date', 'location_2', 'longlat', )
reader=csv.DictReader(result_file, fieldnames)
for i in reader:
    print(type(i))
    data={
        'json':json.dumps(i)
    }
    print(data)
    response=requests.post('http://hasdoel.ml:8080/test1.test', data=data)
# response = requests.post('http://hasdoel.ml:8080/test.test', data=data)

