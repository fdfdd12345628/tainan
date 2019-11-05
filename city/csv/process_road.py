import os, csv, json, pprint, datetime, re, pytz, pyproj, sys
from multiprocessing import Pool
from itertools import product


# pprint.pprint(total_digging_data)
# pprint.pprint(total_result_data)
def count_every_distance(data):
    if (len(data[0]) == 0):
        print(data[0])
        return None
    num = 0
    geod = pyproj.Geod(ellps='WGS84')
    for digging in data[2]:
        # print(digging)
        if len(digging) > 3:
            continue
        # print(data[1] - digging[1])
        if datetime.timedelta(days=360) > (data[1] - digging[1]):
            # print('success1')
            a, b, distance = geod.inv(data[0][0], data[0][1], digging[0][0], digging[0][1])
            if distance < 50:
                # print('success')
                num += 1
                print('success'+str(num))
    return num
    pass


def count():
    # po=Pool(os.cpu_count())

    record_title = open('record_title.csv', 'r+', encoding='utf8', newline='')
    record_title_road = open('record_tile_road.csv', 'w+', encoding='utf8', newline='')

    result = open('result.csv', 'r+', encoding='utf8')

    record_title_reader = csv.reader(record_title)
    result_reader = csv.reader(result)
    total_digging_data = []
    total_result_data = []
    back_result=[]
    for i in result_reader:
        total_result_data.append(i)
        back_result.append(i[:])
        lon = re.search('^經度:\d{1,}.\d{1,}', i[13])
        lat = re.search('緯度:\d{1,}.\d{1,}', i[13])
        try:
            lon = float(lon.group()[3:])
            lat = float(lat.group()[3:])
            i.append([lon, lat])
            time = datetime.datetime.strptime(i[2], '%Y/%m/%d %H:%M:%S')
            # time=datetime.datetime.fromisoformat(time.isoformat(), )
            time = time.replace(tzinfo=pytz.timezone('Asia/Taipei'))
            i.append(time)
        except Exception as e:
            i.append([])
            i.append([])
    
    for i in record_title_reader:
        try:
            # a=json.loads(i[8])
            # print(a)

            total_digging_data.append(i)
        except:
            pass

    for pk, i in enumerate(total_digging_data):
        if pk==0:
            continue
        a = json.loads(i[8])
        i.append(a)
        if len(i[3])<2:
            continue
        time = datetime.datetime.strptime(i[3], '%Y.%m.%d')
        time = datetime.datetime.fromisoformat(time.isoformat(), )
        time = time.replace(tzinfo=pytz.timezone('Asia/Taipei'))
        i.append(time)

            # i.append(total_result_data)
        del (i[0:9])
        # print(i)
        # sleep(3)
        # except:
        #     i.append([])

    for i in total_result_data:
        del (i[0:14])
        # print(i)
        i.append(total_digging_data)

    # pprint.pprint(total_digging_data)
    # count_num = None
    # pprint.pprint(total_result_data)
    # with Pool(os.cpu_count()) as po:
    #     count_num = po.map(count_every_distance, total_result_data)
    print(back_result[0].append('hakjdfh'))
    print(back_result[0])
    for i in total_result_data:
        # print(i[0])
        # print(i[2])
        i.append(count_every_distance(i))

    # pprint.pprint(total_result_data[1])
    print(total_result_data[0][3])
    test = open('result_with_1year_digging.csv', 'w+', encoding='utf8', newline='')
    test_writer = csv.writer(test)
    for i, data in enumerate(total_result_data):
        
        # print(i)
        a=back_result[i].append(data[3])
        print(a)
        test_writer.writerow(back_result[i])


if __name__=='__main__':
    sys.exit(count())

