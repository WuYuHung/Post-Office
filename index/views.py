import csv
from datetime import date, datetime, time, timedelta

import numpy as np
import pandas as pd
from django.conf import settings
from django.shortcuts import render
from sklearn.cluster import KMeans

# Create your views here.

BASE_DIR = settings.STATICFILES_DIRS[0] + '/big data'
DAY = '20180319'
OFFICE = '950580'

def sixty_eight(request):
    excel = pd.read_excel(BASE_DIR + f'/{DAY}/{OFFICE} 68 89.xlsx')
    rows = list(excel.values[1:])
    excel = pd.read_excel(BASE_DIR + f'/{DAY}/{OFFICE} 78.xlsx')
    rows78 = list(excel.values[1:])
    rows78.sort(key=lambda x:x[0])
    picks, box = [list() for i in range(2)]
    hash_map = set()
    starts = dict()
    for i in rows78:
        if i[0] in hash_map:
            continue
        else:
            hash_map.add(i[0])
            starts[i[0]] = dict(E= i[4], N=i[5], time=i[6])
            box.append(i)
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
            if duration >= timedelta(hours=1) and (abs(float(i[4]) - float(starts[i[0]]['E'])) <= 0.003 and abs(float(i[5]) - float(starts[i[0]]['N']) <= 0.003)):
                box.append(i)
                starts[i[0]]['time'] = i[6]
    box.sort(key=lambda x:x[0])
    with open(BASE_DIR + f'/6889_output.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['車牌', '狀態', '行車速度','車頭方向',	'東經',	'北緯',	'日期時間',	'累積里程數',	'路段速限',	'局號'])
        for i in box:
            writer.writerow(i)
    locations = [[i[5], i[4]] for i in box]
    return render(request, 'index.html', {'rows': locations})

def ninety(request):
    post_office = [121.1541,22.7532] # modifiey frquently
    post_office[0], post_office[1] = post_office[1], post_office[0]
    excel = pd.read_excel(BASE_DIR + f'/{DAY}/{OFFICE} 90 91.xlsx')
    rows = list(excel.values[1:])
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
            if duration >= timedelta(minutes=10):
                box.append(i)
                starts[i[0]]['time'] = i[6]
    box = [[float(i[5]), float(i[4]), 1] for i in box]
    final_box = list()
    for i in box:
        for n in final_box:
            if i[0] - 0.001 <= n[0] <= i[0] + 0.001 and i[1] - 0.001 <= n[1] <= i[1] + 0.001:
                n[2] += 1
                break
        else:
            final_box.append(i)
    final_box = [[i[0], i[1]] for i in final_box]
    clf = KMeans(n_clusters=3) # n_clusters 集為分群數量，可根據每天的車輛數進行調整
    clf.fit(final_box)
    labels = clf.predict(final_box)
    clusters = {}
    row_dict = final_box
    n = 0
    for item in labels:
        if item in clusters:
            clusters[item].append(row_dict[n])
        else:
            clusters[item] = [row_dict[n]]
        n += 1
    clusters = list(clusters.values())
    for index, i in enumerate(clusters):
        clusters[index] = [post_office] + i
    with open(BASE_DIR + f'/{DAY}/9091_{OFFICE}_output.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['N', 'E', 'Capacity'])
        for i in box:
            writer.writerow(i)
    locations = [[i[0], i[1]] for i in final_box]
    return render(request, 'index.html', {'rows': locations, 'clusters': clusters})
