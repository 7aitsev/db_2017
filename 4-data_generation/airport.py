#encoding: utf-8

import psycopg2 as pg_driver
from psycopg2.extras import execute_values
import common
import sys
from random import randint
import base26

filepath = 'airports/airports.csv'

def selectAllRows(db):
    dbrows = []
    try:
        c = db.cursor()
        c.execute('SELECT * FROM "Airport";')
        dbrows = [tuple([r[1], r[2], r[3], r[4], r[5], r[6]]) for r in c.fetchall()]
    except pg_driver.Error as e:
        pass
    return dbrows

def mkTupleFromRow(row):
# "name","latitude_deg","longitude_deg","municipality","iso_country"
    name = row[0].strip()
    city = row[3].strip()
    if "" == city:
        city = "Unknown"
    lat = row[1]
    lon = row[2]
    code = base26.toCode(mkTupleFromRow.code_idx)
    if '' == code:
        exit()
    mkTupleFromRow.code_idx += 1
    distance = randint(100, 9000)
    return tuple([name, city, lat, lon, distance, code])
mkTupleFromRow.code_idx = 0

def compare_rows(a, b):
    return a[-1] == b[-1]

def populate(db, limit):
    if 951 < limit or 0 >= limit:
        print 'The number of rows should be in [1,951]'
        return
    rows = common.fetch_unused_rows(db, sys.modules[__name__], compare_rows, limit)
    count = len(rows)
    if 0 != count:
        insert_query = 'INSERT INTO "Airport" (name, city, lat, lon, distance, code) VALUES %s'
        try:
            c = db.cursor()
            execute_values(c, insert_query, rows)
            db.commit()
        except pg_driver.Error as e:
            print e.pgerror
            db.rollback()
            return
        print 'Inserted {} rows'.format(count)
    else:
        print 'All records for "Airport" are exhausted'

def clear(db):
    common.clear(db, 'Airport')
