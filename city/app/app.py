'''input: date of hole occurrences wanted to predict, output the map of prediction'''
import calendar
import datetime
import json
import os
import time

import cv2
import numpy as np
from PIL import Image
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

from .astar import a_star

# import keras

model = load_model('test.h5')




# input: the date people want to know about the occurrences of holls *format: "year/month/day"
# output: image or np array helping to calculate the best path to walk 
def gen_pred_hole(date):
    nearest_Monday_year, nearest_Monday_month, nearest_Monday_day = date_processing(date)
    data_map = data_processing(nearest_Monday_year, nearest_Monday_month,
                               nearest_Monday_day)  # maps with two channels (working records, and holes)
    '''
    '''
    gen_map_images(data_map)
    print('second sstep' + str(datetime.datetime.now()))
    time.sleep(0)
    X = gen_X()
    print('third sstep' + str(datetime.datetime.now()))
    time.sleep(0)
    y_pred = predict(X)
    # print(y_pred.shape)
    gen_result_map(y_pred)
    return gen_walk_path()

# process input (date) to the right format 
def date_processing(date):
    date_result = time.strptime(date, "%Y/%m/%d")
    weekday = calendar.weekday(date_result.tm_year, date_result.tm_mon, date_result.tm_mday)    
    nearest_Monday = datetime.datetime(date_result.tm_year, date_result.tm_mon, date_result.tm_mday) - datetime.timedelta(days=weekday)
    nearest_Monday_year = str(nearest_Monday.year)
    if nearest_Monday.month < 10:
        nearest_Monday_month = "0" + str(nearest_Monday.month)
    else:
        nearest_Monday_month = str(nearest_Monday.month)
    
    if nearest_Monday.day < 10:
        nearest_Monday_day = "0" + str(nearest_Monday.day)
    else:
        nearest_Monday_day = str(nearest_Monday.day)
        
    return nearest_Monday_year, nearest_Monday_month, nearest_Monday_day
        
# data (feature) processing
def data_processing(nearest_Monday_year, nearest_Monday_month, nearest_Monday_day):
    # parse the json file
    with open('csv/區塊坑洞挖掘與施工紀錄_1000公尺.json', 'r') as f:
        split_1000m_data = json.load(f)
    for week_data in split_1000m_data['data']:
        if week_data['endTime'] == nearest_Monday_year + "/" + nearest_Monday_month + "/" + nearest_Monday_day:       
            end_week_index = split_1000m_data['data'].index(week_data)
            # process data
            ch_hole = []   # channel for hole data
            ch_road = []   # channel for road working record

            for week in range(end_week_index - 2, end_week_index + 1):   # create maps for two channels
                ch_hole.append([])
                ch_road.append([])
                for hole_one_week in reversed(split_1000m_data['data'][week]['channel_hole']):
                    ch_hole[len(ch_hole) - 1].append(hole_one_week)
                for roadwork_one_week in reversed(split_1000m_data['data'][week]['channel_roadwork']):
                    ch_road[len(ch_road) - 1].append(roadwork_one_week)
                    
            data_map = []   # store maps with two channels
            for map_num in range(0, len(ch_hole)):   # convert map into two channels (ch_hole combines with ch_road)
                data_map.append([])
                data_map[len(data_map) - 1].append(ch_hole[map_num])
                data_map[len(data_map) - 1].append(ch_road[map_num])
    return data_map
        
# generate map images 
def gen_map_images(data_map):
    if not os.path.exists('map_helping_pred'):
        os.makedirs('map_helping_pred')   # create directory to store map image to help predict (model input)
    curdir = os.getcwd()
    os.chdir("map_helping_pred")   # change directory to where images to be stored
    map_transfromed = map_scale(data_map)   # scale the num in grid and let it btw [0, 256]
    for map_num in range(0, len(data_map)):
        map_one_week = np.zeros((13, 18, 3), dtype=np.uint8)
        for i in range(0, map_one_week.shape[0]):
            for j in range(0, map_one_week.shape[1]):
                map_one_week[i][j][0] = map_transfromed[map_num][0][i][j]
                map_one_week[i][j][1] = map_transfromed[map_num][1][i][j]
        filename = 'map_helping_pred' + str(map_num) + '.bmp'
        cv2.imwrite(filename, map_one_week)
        print(filename + "done!!")
        
    os.chdir(curdir)

# scale the num in every grid to be in [0, 1], and * 255 for three channels        
def map_scale(map_list):
    min_max_scaler = MinMaxScaler() 
    map_transformed = []
    for map_num in range(0, len(map_list)):
        ch_hole_temp = np.array(map_list[map_num][0])
        ch_hole_temp = (min_max_scaler.fit_transform(ch_hole_temp)) * 255
        ch_road_temp = np.array(map_list[map_num][1])
        ch_road_temp = (min_max_scaler.fit_transform(ch_road_temp)) * 255
        map_transformed.append([])
        map_transformed[len(map_transformed) - 1].append(ch_hole_temp)
        map_transformed[len(map_transformed) - 1].append(ch_road_temp)
        
        #print(map_transformed[map_num][1])
    return map_transformed
        
# generate X data (features) to help predict
def gen_X():
    map_images = []
    curdir = os.getcwd()
    os.chdir("map_helping_pred")
    for week in range(0, 3):
        map_image = Image.open('map_helping_pred' + str(week) + '.bmp')
        map_image = np.array(map_image)
        map_images.append(map_image)
        
    X = []
    X.append(map_images)
    X = np.array(X)
    os.chdir(curdir)
    return X

# load in model and predict the result
def predict(X):
    # pickle.load(open("convlstm.pickle.dat", "rb"))
    # print('loaded'+str(datetime.datetime.now()))
    # log_dir = "logs/profile/" #  + datetime.now().strftime("%Y%m%d-%H%M%S")
    # tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1, profile_batch=1)
    y_pred = model.predict(X, )

    return y_pred

# generate y_pred map to indicate the result of prediction (holes)
def gen_result_map(y_pred):
    map_result = np.zeros((3, 13, 18), dtype=np.float)
    for i in range(0, map_result.shape[1]):
        for j in range(0, map_result.shape[2]):
            ###### threshold ######
            if y_pred[0][i][j][0] > 0.03:
                map_result[2][i][j] = y_pred[0][i][j][0]   # channel 'red'
    
    map_result = result_map_scale(map_result)
    map_result_2 = np.zeros((13, 18, 3), dtype=np.float)
    for i in range(0, y_pred.shape[1]):
        for j in range(0, y_pred.shape[2]):
            map_result_2[i][j][2] = map_result[2][i][j]   # channel 'red'

    # calculate level of risk or not
    # risk_level_deter(map_result_2)
    cv2.imwrite("result.bmp", map_result_2)

# scale the num in every grid to be in [0, 1], and * 255 for red channels        
def result_map_scale(map_result):
    min_max_scaler = MinMaxScaler() 
    map_result[2] = min_max_scaler.fit_transform(map_result[2]) * 255
        
    return map_result

# generate the best path to walk through
def gen_walk_path():    
    #map_pred = Image.open('map_result.bmp')
    map_pred = Image.open('result.bmp')
    map_pred = np.array(map_pred)
    map_pred_1ch = np.zeros((13, 18))
    for i in range(0, 13):
        for j in range(0, 18):
            map_pred_1ch[i][j] = map_pred[i][j][0]
    result = a_star(map_pred_1ch, blocks=20)
    '''
    data=np.zeros(shape=(11, 16))
    for i in result:
        data.flat[i]=1
    '''
    #os.chdir("../")   # change directory to where images stored
    returnList = [result,map_pred]
    return returnList
