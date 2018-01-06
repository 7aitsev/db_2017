#encoding: utf-8

import psycopg2 as pg_driver
import sys
from random import randint
from datetime import date

import common
import person
import rating

select_all_query = 'SELECT * FROM "Pilot";'
insert_query = 'INSERT INTO "Pilot" (id, rating) VALUES %s;'
limit = person.limit

def compare_rows(a, b):
    return a[0] == b[0] # by id

def next():
    person_id = next.person_rows[next.i][0]
    rating_id = next.rating_rows[randint(0, len(next.rating_rows) - 1)][0]
    return [person_id, rating_id]
next.person_rows = []
next.person_rows_len = 0
next.rating_rows = []
next.i = 0
next.min_age = date(date.today().year - 18,
                    date.today().month, date.today().day)

def hasNext():
    bday = next.min_age
    while bday >= next.min_age and next.i != next.person_rows_len:
        person_row = next.person_rows[next.i]
        next.i += 1
        bday = person_row[2]
    return next.person_rows_len != next.i

def populate(db, count):
    try:
        # check whether "Rating" has rows and if not, populate the table in an ineractive mode
        next.rating_rows = common.select_all_rows(db, rating.select_all_query)
        if 0 == len(next.rating_rows):
            inserted_rows_count = common.populate_interactive(db, rating)
            if 0 >= inserted_rows_count:
                print '"Rating" does not have records'
                return -1
            next.rating_rows = common.select_all_rows(db, rating.select_all_query)
        # fetch all records from "Person" and decide populate the table or not
        next.person_rows = common.select_all_rows(db, person.select_all_query)
        rows = common.fetch_unused_rows(db, sys.modules[__name__], count)
        next.person_rows_len = len(rows)
        if next.person_rows_len < count:
            print 'Unused rows in "Person": {}'.format(next.person_rows_len)
            rv = common.populate_interactive(db, person)
            next.person_rows_len += rv
            if next.person_rows_len < count:
                print '"Person" does not have enough records'
                return -1
            next.i = 0
            next.person_rows = common.select_all_rows(db, person.select_all_query)
            next.person_rows_len = len(next.person_rows)
            rows = common.fetch_unused_rows(db, sys.modules[__name__], count)
    except pg_driver.Error as e:
        print e.pgerror
        return -1
    return common.insert_rows(db, sys.modules[__name__], rows)

def clear(db):
    common.clear(db, 'Ticket')
    common.clear(db, 'Flight')
    common.clear(db, 'Pilot')
