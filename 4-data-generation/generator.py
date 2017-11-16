#!/usr/bin/python
#encoding: utf-8

import argsreader
args = argsreader.getargs()

import psycopg2 as pg_driver
from psycopg2.extras import execute_values

import psycopg2.pool as pool
pg_pool = pool.SimpleConnectionPool(1, 2, user=args.user, password=args.password,
        dbname=args.dbname, host=args.host)

def clean_exit():
    cur.close()
    pg_pool.closeall()
    exit(1)

db = pg_pool.getconn()
cur = db.cursor()
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';")
all_tables = [t[0] for t in cur.fetchall()]

def clear(table):
    query = 'TRUNCATE "%s" CASCADE;'
    try:
        if table != 'all':
            print 'Removing content from "{}"...'.format(table)
            cur.execute(query % table)
        else:
            print 'Removing content from all tables...'
            for t in all_tables:
                print t
                cur.execute(query % t)
        db.commit()
        print 'Content was removed'
    except pg_driver.Error as e:
        print 'Removing was failed'
        print e.pgerror
        db.rollback() 

# TODO move to Person class
def fetch_unused_rows(limit):
    import csv
    with open("persons/persons.csv", "r") as persons_file:
        reader = csv.reader(persons_file)
        keys = ['first_name', 'last_name', 'phone1', 'bday']
        reader.next() # skip the header
        out = []
        try:
            cur.execute('SELECT * from "Person";')
            dbrows = [tuple([r[1], str(r[2]), r[3]]) for r in cur.fetchall()]
            count = 0
            for row in reader:
                if count >= limit:
                    break
                # merge first and last names, construct a tuple
                tup = tuple([row[0] + ' ' + row[1], row[3], row[2]])
                if tup not in dbrows:
                    out += [tup]
                    count += 1
        except pg_driver.Error as e:
            print e.pgerror
            db.rollback()
        return out

# TODO move to Person class
def populate_person():
    rows = fetch_unused_rows(args.number)
    if 0 != len(rows):
        insert_query = 'INSERT INTO "Person" (name, bday, phone) VALUES %s'
        execute_values(cur, insert_query, rows)
        db.commit()
        print 'Inserted {} rows'.format(cur.rowcount)
    else:
        print 'All records for "Person" are exhausted'

# Clear or populate table according to --clear option
if args.table in ['all'] + all_tables:
    if not args.clear:
        if args.table == 'Person':
            if 1000 >= args.number and 0 < args.number:
                populate_person()
            else:
                print 'The number of rows should be in [1,1000]'
    else:
        clear(args.table)
else:
    print 'There is no such table: {}'.format(args.table)

clean_exit()
