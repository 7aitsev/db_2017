#encoding: utf-8

import sys
from random import randint

from string import ascii_uppercase as alphabet
import common

filepath = 'airports/airports.csv'
select_all_query = 'SELECT * FROM "Airport";'
insert_query = 'INSERT INTO "Airport" (name, city, lat, lon, distance, code) VALUES %s;'
limit = 951

def toCode(num):
    if toCode.base**toCode.len_lim - 1 < num or 0 > num:
        print 'Bad number'
        return ''
    digits = []
    while 3 > len(digits):
        if 0 == num:
            digits.append(0)
        else:
            digits.append(num % toCode.base)
            num //= toCode.base

    code = ''
    for c in reversed(digits):
        code += alphabet[c]
    return code
toCode.base = 26
toCode.len_lim = 3

def create_new_row(row):
# "name","latitude_deg","longitude_deg","municipality"
    name = row[0].strip()
    city = row[3].strip()
    if "" == city:
        city = "Unknown"
    lat = row[1]
    lon = row[2]
    code = toCode(create_new_row.code_idx)
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
