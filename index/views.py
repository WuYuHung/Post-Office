from django.shortcuts import render
from django.conf import settings
import csv
from pprint import pprint
# Create your views here.

BASE_DIR = settings.STATICFILES_DIRS[0]

def index(request):
    with open(BASE_DIR + '/positions.csv', 'r', encoding='big5') as f:
        rows = list(csv.reader(f))[1:]
    differ = list()
    rows = sorted(rows, key = lambda x:(x[0], x[1]))[3:]
    pprint(rows)
    pprint(rows)
    print(len(rows))
    for index, i in enumerate(rows):
        if index != len(rows) - 1:
            differ.append(abs(float(i[1]) - float(rows[index + 1][1])) <= 0.0001 or abs(float(i[0]) - float(rows[index + 1][0])) <= 0.0001)
    differ += [False]
    print('*****', sum(map(int, differ)))
    rows = [j for index, j in enumerate(rows) if not differ[index]]
    print(len(rows))
    return render(request, 'index.html', {'rows': rows})