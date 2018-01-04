#encoding: utf-8

import psycopg2 as pg_driver
import sys
from random import randint

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
    next.i += 1
    return [person_id, rating_id]
next.person_rows = []
next.rating_rows = []
next.i = 0

def hasNext():
    return len(next.person_rows) != next.i

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
        person_rows_count = len(rows)
        if person_rows_count < count:
            print 'Unused rows in "Person": {}'.format(person_rows_count)
            rv = common.populate_interactive(db, person)
            person_rows_count += rv
            if person_rows_count < count:
                print '"Person" does not have enough records'
                return -1
            next.i = 0
            next.person_rows = common.select_all_rows(db, person.select_all_query)
            rows = common.fetch_unused_rows(db, sys.modules[__name__], count)
    except pg_driver.Error as e:
        print e.pgerror
        return -1
    return common.insert_rows(db, sys.modules[__name__], rows)

def clear(db):
    #import flight
    #flight.clear(db)
    common.clear(db, 'Pilot')
