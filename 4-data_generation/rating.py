#encoding: utf-8

import sys

import common

select_all_query = 'SELECT * FROM "Rating";'
insert_query = 'INSERT INTO "Rating" (rating, salary_per_hour) VALUES %s'
limit = 9

def compare_rows(a, b):
    return False

def next():
    next.i += 1
    while True:
        print '{}) Enter salary per hour:'.format(next.i),
        try:
            salary = int(input())
        except:
            print sys.exc_info()[0]
            continue
        if(0 > salary):
            print 'The value has to be a positive number'
            continue
        return [next.i, salary]
next.i = 0

def hasNext():
    return True

def populate(db, count):
    if limit < count:
        print 'The number of rows must be in [1,{}]'.format(limit)
        return -1
    rows = common.fetch_unused_rows(db, sys.modules[__name__], count)
    return common.insert_rows(db, sys.modules[__name__], rows)

def clear(db):
    common.clear(db, 'Pilot');
    common.clear(db, 'Rating');
