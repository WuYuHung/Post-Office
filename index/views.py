import csv
from datetime import date, datetime, time, timedelta
from pprint import pprint

import numpy as np
from django.conf import settings
from django.shortcuts import render

# Create your views here.

BASE_DIR = settings.STATICFILES_DIRS[0] + '/big data'

def index(request):
    with open(BASE_DIR + '/positions.csv', 'r', encoding='big5') as f:
        rows = list(csv.reader(f))[1:]
    differ = list()
    rows = sorted(rows, key = lambda x:(x[0], x[1]))[3:]
    print(len(rows))
    for index, i in enumerate(rows):
        if index != len(rows) - 1:
            differ.append(abs(float(i[1]) - float(rows[index + 1][1])) <= 0.0001 or abs(float(i[0]) - float(rows[index + 1][0])) <= 0.0001)
    differ += [False]
    print('*****', sum(map(int, differ)))
    rows = [j for index, j in enumerate(rows) if not differ[index]]
    print(len(rows))
    return render(request, 'index.html', {'rows': rows})

def sixty_eight(request):
    with open(BASE_DIR + '/20180312/100600 68 89.csv', 'r') as f:
        rows = list(csv.reader(f))[1:]
    with open(BASE_DIR + '/20180312/100600 78.csv', 'r') as f:
        rows += list(csv.reader(f))[1:]
    starts = dict()
    box = list()
    rows.sort(key=lambda x:x[0])
    print(rows)
    for i in rows:
        if i[0] not in starts:
            starts[i[0]] = dict(E= i[4], N=i[5], time=i[6])
            box.append(i)
        else:
            time_split = [list(map(int, i.split(' ')[2].split(':'))) for i in (starts[i[0]]['time'], i[6])]
            if '下' in starts[i[0]]['time'].split(' ')[1] and time_split[0][0] != 12:
                time_split[0][0] += 12
            if '下' in i[6].split(' ')[1] and time_split[1][0] != 12:
                time_split[1][0] += 12
            start_time = time(time_split[0][0], time_split[0][1], time_split[0][2])
            end_time = time(time_split[1][0], time_split[1][1], time_split[1][2])
            duration = datetime.combine(date.min, end_time) - datetime.combine(date.min, start_time)
            if duration >= timedelta(hours=1) and (abs(float(i[4]) - float(starts[i[0]]['E']) <= 0.005 and abs(float(i[5]) - float(starts[i[0]]['N']) <= 0.005))):
                box.append(i)
                starts[i[0]]['time'] = i[6]
    pprint(box)
    with open(BASE_DIR + '/6889_output.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['車牌', '狀態', '行車速度',	'車頭方向',	'東經',	'北緯',	'日期時間',	'累積里程數',	'路段速限',	'局號'])
        for i in box:
            writer.writerow(i)
    locations = [[i[5], i[4]] for i in box]
    return render(request, 'index.html', {'rows': locations})

def ninety(request):
    with open(BASE_DIR + '/9091.csv', 'r', encoding='big5') as f:
        rows = list(csv.reader(f))[1:]
    starts = dict()
    box = list()
    rows.sort(key=lambda x:x[0])
    for i in rows:
        if i[0] not in starts:
            starts[i[0]] = dict(E= i[4], N=i[5], time=i[6])
            box.append(i)
        else:
            time_split = [list(map(int, i.split(' ')[2].split(':'))) for i in (starts[i[0]]['time'], i[6])]
            if '下' in starts[i[0]]['time'].split(' ')[1] and time_split[0][0] != 12:
                time_split[0][0] += 12
            if '下' in i[6].split(' ')[1] and time_split[1][0] != 12:
                time_split[1][0] += 12
            start_time = time(time_split[0][0], time_split[0][1], time_split[0][2])
            end_time = time(time_split[1][0], time_split[1][1], time_split[1][2])
            duration = datetime.combine(date.min, end_time) - datetime.combine(date.min, start_time)
            if duration >= timedelta(minutes=30):
                box.append(i)
                starts[i[0]]['time'] = i[6]
    box = [[float(i[5]), float(i[4]), 1] for i in box]
    print(box)
    final_box = list()
    for i in box:
        for n in final_box:
            if i[0] - 0.005 <= n[0] <= i[0] + 0.005 and i[1] - 0.005 <= n[1] <= i[1] + 0.005:
                n[2] += 1
                break
        else:
            final_box.append(i)
    print(final_box)
    with open(BASE_DIR + '/9091_output.csv', 'w', encoding='big5') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['N', 'E', 'Capacity'])
        for i in box:
            writer.writerow(i)
    locations = [[i[0], i[1]] for i in final_box]
    return render(request, 'index.html', {'rows': locations})
