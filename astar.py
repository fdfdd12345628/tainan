import json, math
import numpy as np
from PIL import Image


def construct(came_from, end, start):
    path_list = []
    current = int(came_from.flat[end])
    while True:
        try:
            if path_list[len(path_list) - 1] == current:
                return path_list
        except IndexError:
            pass

        path_list.append(current)
        # if path_list[len(path_list)-1]==current

        if current == start:
            return path_list
        current = int(came_from.flat[current])


def h(data, came_from, current_node, target_node, start_node):
    if target_node == None:
        return 500
    start_x = current_node // data.shape[1]
    start_y = current_node % data.shape[1]
    end_x = target_node // data.shape[1]
    end_y = target_node % data.shape[1]
    result = math.sqrt((start_x - end_x) ** 2 + (start_y - end_y) ** 2)
    return result


def d(data, came_from, current_node, target_node, start_node):
    start_x = current_node // data.shape[1]
    start_y = current_node % data.shape[1]
    end_x = target_node // data.shape[1]
    end_y = target_node % data.shape[1]
    result = -(data.flat[target_node] * 1)
    # print(data.flat[target_node])
    # print(data.flat[current_node])
    # result += math.sqrt((start_x - end_x) ** 2 + (start_y - end_y) ** 2)
    path = construct(came_from, current_node, start_node)
    # child_node=0
    for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Adjacent squares
        try:
            # chile_node = data.flat[current + data.shape[1] * new_position[0] + new_position[1]]
            # chile_node = data[current // data.shape[1] + new_position[0] + 1][
            #   current % data.shape[1] + new_position[1]]
            if current_node // data.shape[1] + new_position[0] == data.shape[0] or current_node // data.shape[1] \
                    + new_position[0] < 0:
                continue
            if current_node % data.shape[1] + new_position[0] == data.shape[1] or current_node % data.shape[1] \
                    + new_position[1] < 0:
                continue
            chile_node = current_node + data.shape[1] * new_position[0] + new_position[1]
        except:
            pass
        if chile_node in path:
            pass
            # result -= 0.03

    return result


def pre(data):
    data = data[1:-1, 1:-1]
    return data
    pass


# def h(data, came_from, data_start, target_end):
#     pass


def a_star(data, start=None, end=None, blocks=0):
    data = pre(data)
    if start is None:
        start = np.argmax(data)
    g_score = np.ones(data.shape) * 1000
    f_score = np.ones(data.shape) * 1000
    open_set = {start: 0}
    close_set = {}
    g_score.flat[start] = 0
    f_score.flat[start] = h(data, None, start, end, None)
    came_from_list = np.zeros(data.shape, dtype=np.int)
    walked = {}
    if start is None:
        start = np.argmax(data)
    while len(open_set) != 0:
        # current_min=f_score.max
        current = np.argmax(f_score)
        for i in open_set:
            if f_score.flat[i] < f_score.flat[current]:
                current = i
        if current == np.argmax(f_score):
            break
        # current = np.argmin(f_score)
        if end != None:
            if current == end:
                path = construct(came_from_list, end, start)
                result = np.zeros(data.shape, dtype=int)
                for i in path:
                    result.flat[i] = 1
                return construct(came_from_list, end, start)  # came_from_list
        else:
            # with np.argmin(g_score) as end:
            # temp_end=np.argmin(g_score)
            temp_end = 0
            for i in open_set:
                if g_score.flat[i] < g_score.flat[temp_end]:
                    temp_end = i
            path = construct(came_from_list, temp_end, start)
            total = len(path)
            if total >= blocks:
                return path

        del (open_set[current])

        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Adjacent squares
            try:
                # chile_node = data.flat[current + data.shape[1] * new_position[0] + new_position[1]]
                # chile_node = data[current // data.shape[1] + new_position[0] + 1][
                #   current % data.shape[1] + new_position[1]]
                if current // data.shape[1] + new_position[0] == data.shape[0] or current // data.shape[1] + \
                        new_position[0] < 0:
                    continue
                if current % data.shape[1] + new_position[0] == data.shape[1] or current % data.shape[1] + new_position[
                    1] < 0:
                    continue
                chile_node = current + data.shape[1] * new_position[0] + new_position[1]
                if chile_node >= data.size:
                    continue
            except IndexError as e:
                continue
            if chile_node in walked:
                continue
            tentative_gScore = g_score.flat[current] + d(data, came_from_list, current, chile_node, start)  # d()
            if tentative_gScore < g_score.flat[chile_node]:
                walked[current] = 0
                came_from_list.flat[chile_node] = current
                g_score.flat[chile_node] = tentative_gScore
                f_score.flat[chile_node] = tentative_gScore + h(data, came_from_list, current, chile_node, start)
                if chile_node not in open_set:
                    open_set[chile_node] = 0

    return None


if __name__ == '__main__':
    # test=np.array(range(100))
    # test=np.reshape(test, (10, 10))
    # test=pre(test)
    # print(test)
    with open('區塊坑洞挖掘與施工紀錄_1000公尺.json', 'r+', encoding='utf8') as file:
        raw = Image.open('map_pred1.bmp')
        test = np.array(raw)
        test = test[:, :, 0]
        # json_data = json.loads(raw)
    # print(json_data)
    # test = np.array(json_data['data'][15]['channel_hole'])
    '''for i in range(10)[::-1]:
        path = a_star(test, np.argmax(test), blocks=i)
        if path is not None:
            break'''
    path = a_star(test, blocks=15)
    print(path)
    test = test[1:-1, 1:-1]
    path_array = np.zeros(test.shape)
    for i in path:
        path_array.flat[i] = 1
    pass
