#encoding: utf-8

import psycopg2 as pg_driver
from psycopg2.extras import execute_values
import common
import sys

def populate(db, limit):
    if(0 > limit):
        print 'The number of rows should be positive'
        return
    ratings = []
    idx = 1
    while idx <= limit:
        print '{}) Enter salary per hour: '.format(idx)
        try:
            salary = int(input())
        except:
            print sys.exc_info()[0]
            return 
        if(0 > salary):
            print 'The value has to be a positive number'
            continue

        ratings += [tuple([idx, salary])]
        idx += 1
    insert_query = 'INSERT INTO "Rating" (rating, salary_per_hour) VALUES %s'
    try:
        c = db.cursor()
        execute_values(c, insert_query, ratings)
        db.commit()
    except pg_driver.Error as e:
        print e.pgerror
        db.rollback()
        return
    print 'Inserted {} rows'.format(len(ratings))

def clear(db):
    common.clear(db, 'Rating');
