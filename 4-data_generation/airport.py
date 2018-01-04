#encoding: utf-8

import sys
from random import randint

import base26
import common

filepath = 'airports/airports.csv'
select_all_query = 'SELECT * FROM "Airport";'
insert_query = 'INSERT INTO "Airport" (name, city, lat, lon, distance, code) VALUES %s;'

def create_new_row(row):
# "name","latitude_deg","longitude_deg","municipality"
    name = row[0].strip()
    city = row[3].strip()
    if "" == city:
        city = "Unknown"
    lat = row[1]
    lon = row[2]
    code = base26.toCode(create_new_row.code_idx)
    create_new_row.code_idx += 1
    distance = randint(100, 9000)
    return [name, city, lat, lon, distance, code]
create_new_row.code_idx = 0

def compare_rows(a, b):
    return a[-1] == b[-1]

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

def populate(db, limit):
    if 951 < limit:
        print 'The number of rows must be in [1,951]'
        return
    import csv
    with open(filepath, 'r') as csvfile:
        next.reader = csv.reader(csvfile)
        keys = next.reader.next() # skip the header
        rows = common.fetch_unused_rows(db, sys.modules[__name__], limit)
        common.insert_rows(db, sys.modules[__name__], rows)

def clear(db):
    #import flight
    #flight.clear(db)
    common.clear(db, 'Airport')
