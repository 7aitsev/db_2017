#encoding: utf-8

import psycopg2 as pg_driver
from psycopg2.extras import execute_values
import common
import sys
from random import randint
import datetime

filepath = 'planes/planes.csv'

def selectAllRows(db):
    dbrows = []
    try:
        c = db.cursor()
        c.execute('SELECT * FROM "Plane";')
        dbrows = [tuple([r[1], str(r[2]), r[3], r[4], r[5]]) for r in c.fetchall()]
    except pg_driver.Error as e:
        pass
    return dbrows

def mkTupleFromRow(row):
    name = row[0] + ' ' + row[1]
    try:
        year = int(row[2])
        if year < 1990:
            year = datetime.date(1990, 1, 1)
        else:
            year = datetime.date(year, 1, 1)
    except:
        year = datetime.date(1990, 1, 1)
    nseats = row[3].strip('0')
    try:
        nseats = int(nseats)
    except:
        nseats = 128
    service_life = randint(20, 50)
    speed = randint(200, 800)
    return tuple([name, year, service_life, speed, nseats])

def populate(db, limit):
    if 1200 < limit or 0 >= limit:
        print 'The number of rows should be in [1,1200]'
        return
    rows = common.fetch_unused_rows(db, sys.modules[__name__], limit)
    count = len(rows)
    if 0 != count:
        insert_query = 'INSERT INTO "Plane" (name, year, service_life, speed, capacity) VALUES %s'
        try:
            c = db.cursor()
            execute_values(c, insert_query, rows)
            db.commit()
        except pg_driver.Error as e:
            print e.pgerror
            db.rollback()
            return
        # execute_values does not give right cursor.rowcount (issue #540)
        print 'Inserted {} rows'.format(count)
    else:
        print 'All records for "Plane" are exhausted'

def clear(db):
    common.clear(db, 'Plane')
