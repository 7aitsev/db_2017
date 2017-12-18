#encoding: utf-8

import psycopg2 as pg_driver
from psycopg2.extras import execute_values
import common
import datetime
import random
from names import get_full_name

filepath = 'persons/persons.csv'

def selectAllRows(db):
    dbrows = []
    try:
        c = db.cursor()
        c.execute('SELECT * FROM "Person";')
        dbrows = [tuple([r[1], str(r[2]), r[3]]) for r in c.fetchall()]
    except pg_driver.Error as e:
        pass
    return dbrows

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

def generate_rows(n):
    return [[get_full_name()[:200], get_bday(), get_phone()] for i in range(n)]

def mkTupleFromRow(row):
    return tuple([row[0] + ' ' + row[1], row[3], row[2]])

def populate(db, limit):
    if 100000 < limit or 0 >= limit:
        print 'The number of rows should be in [1,100000]'
        return
    #rows = common.fetch_unused_rows(db, person, limit)
    rows = generate_rows(limit)
    count = len(rows)
    if 0 != count:
        insert_query = 'INSERT INTO "Person" (name, bday, phone) VALUES %s'
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
        print 'All records for "Person" are exhausted'

def clear(db):
    common.clear(db, 'Person')
