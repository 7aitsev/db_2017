#encoding: utf-8

import psycopg2 as pg_driver
from psycopg2.extras import execute_values
import common

class Person:

    filepath = 'persons/persons.csv'

    def selectAllRows(self, db):
        dbrows = []
        try:
            c = db.cursor()
            c.execute('SELECT * FROM "Person";')
            dbrows = [tuple([r[1], str(r[2]), r[3]]) for r in c.fetchall()]
        except pg_driver.Error as e:
            pass
        return dbrows

    def mkTupleFromRow(self, row):
        return tuple([row[0] + ' ' + row[1], row[3], row[2]])

def populate(db, limit):
    if 1000 < limit or 0 >= limit:
        print 'The number of rows should be in [1,1000]'
        return
    person = Person()
    rows = common.fetch_unused_rows(db, person, limit)
    count = len(rows)
    if 0 != count:
        insert_query = 'INSERT INTO "Person" (name, bday,phone) VALUES %s'
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
