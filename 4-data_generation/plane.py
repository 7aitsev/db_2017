#encoding: utf-8

import sys
from random import randint
import datetime

import common

filepath = 'planes/planes.csv'
select_all_query = 'SELECT * FROM "Plane";'
insert_query = 'INSERT INTO "Plane" (name, year, service_life, speed, capacity) VALUES %s;'
limit = 251

def create_new_row(row):
    name = row[0] + ' ' + row[1]
    try:
        year = int(row[2])
        if year < 1990:
            year = datetime.date(randint(1990, 2017), 1, 1)
        else:
            year = datetime.date(year, 1, 1)
    except:
        year = datetime.date(randint(1990, 2017), 1, 1)
    nseats = row[3].strip('0')
    try:
        nseats = int(nseats)
        if nseats < 7:
            nseats = randint(7, 300)
    except:
        nseats = randint(7, 300)
    service_life = randint(20, 50)
    try:
        speed = int(int(row[4].strip('0')) * 1.64)
        if speed < 200:
            speed = randint(300, 800)
    except:
        speed = randint(300, 800)
    return [name, year, service_life, speed, nseats]

def compare_rows(a, b):
    # name, year
    return a[-5] == b[-5] and a[-4] == b[-4]

def next():
    return create_new_row(next.last_item)
next.reader = None
next.last_item = None

def hasNext():
    try:
        next.last_item = next.reader.next()
    except StopIteration as e:
        return False
    return True

def populate(db, count):
    if limit < count:
        print 'The number of rows must be in [1,{}]'.format(limit)
        return -1
    import csv
    with open(filepath, 'r') as csvfile:
        next.reader = csv.reader(csvfile)
        keys = next.reader.next() # skip the header
        rows = common.fetch_unused_rows(db, sys.modules[__name__], count)
        return common.insert_rows(db, sys.modules[__name__], rows)
