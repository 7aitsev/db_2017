#encoding: utf-8

import sys
import datetime
import random
from names import get_full_name

import common

filepath = 'persons/persons.csv'
select_all_query = 'SELECT * FROM "Person";'
insert_query = 'INSERT INTO "Person" (name, bday, phone) VALUES %s;'
limit = float('inf')

start = datetime.date(1910, 1, 1)
end = datetime.date(2018, 1, 1)
def get_bday():
    return start + datetime.timedelta(
            seconds = random.randint(0, int((end - start).total_seconds())))

def get_phone():
    n = '0000000000'
    while '9' in n[3:6] or n[3:6]=='000' or n[6]==n[7]==n[8]==n[9]:
        n = str(random.randint(10**9, 10**10-1))
    return '8-' + n[:3] + '-' + n[3:6] + '-' + n[6:]

def compare_rows(a, b):
    # phone, bday and name
    return a[-1] == b[-1] and a[-2] == b[-2] and a[-3] == b[-3]

def next():
    return [get_full_name()[:200], get_bday(), get_phone()]

def hasNext():
    return True

def populate(db, count):
    if limit < count:
        print 'The number of rows should be in [1,{}]'.format(table.limit)
        return -1
    rows = common.fetch_unused_rows(db, sys.modules[__name__], count)
    return common.insert_rows(db, sys.modules[__name__], rows)

def clear(db):
    common.clear(db, 'Pilot')
    common.clear(db, 'Person')
