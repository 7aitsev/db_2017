#!/usr/bin/python
#encoding: utf-8

import psycopg2 as pg_driver
import psycopg2.pool as pool
pg_pool = None

def init_connection(args):
    global pg_pool
    pg_pool = pool.SimpleConnectionPool(1, 2, user=args.user,
                              dbname=args.dbname, host=args.host)
    return pg_pool.getconn()

def close_connection_and_exit(rc):
    pg_pool.closeall()
    exit(rc)

def select_all_tables(db):
    tables = ['All']
    try:
        cur = db.cursor()
        cur.execute("SELECT table_name FROM information_schema.tables \
                    WHERE table_schema='public' AND table_type='BASE TABLE';")
        tables += [t[0] for t in cur.fetchall()]
        cur.close()
    except pg_driver.Error as e:
        print e.pgerror
        close_connection_and_exit(1)
    return tables

import argsreader
args = argsreader.getargs()

db = init_connection(args)
all_tables = select_all_tables(db)

import common
import person
import rating
import plane
import airport
import pilot
import route
import flight
import ticket
# Clear or populate table according to --clear option
if args.table in all_tables:
    if not args.clear:
        if 0 >= args.number and args.table != 'All':
            print 'Rows count must be positive'
        elif args.table == 'Person':
            person.populate(db, args.number)
        elif args.table == 'Rating':
            rating.populate(db, args.number)
        elif args.table == 'Plane':
            plane.populate(db, args.number)
        elif args.table == 'Airport':
            airport.populate(db, args.number)
        elif args.table == 'Pilot':
            pilot.populate(db, args.number)
        elif args.table == 'Route':
            route.populate(db, args.number)
        elif args.table == 'Flight':
            flight.populate(db, args.number)
        elif args.table == 'Ticket' or args.table == 'All':
            ticket.populate(db, args.number)
    else:
        if args.table == 'All':
            person.clear(db)
            rating.clear(db)
            pilot.clear(db)
            plane.clear(db)
            airport.clear(db)
            route.clear(db)
            flight.clear(db)
            ticket.clear(db)
        elif args.table == 'Person':
            person.clear(db)
        elif args.table == 'Rating':
            rating.clear(db)
        elif args.table == 'Plane':
            plane.clear(db)
        elif args.table == 'Airport':
            airport.clear(db)
        elif args.table == 'Pilot':
            pilot.clear(db)
        elif args.table == 'Route':
            route.clear(db)
        elif args.table == 'Flight':
            flight.clear(db)
        elif args.table == 'Ticket':
            ticket.clear(db)
else:
    print 'There is no such table: {}'.format(args.table)
    close_connection_and_exit(1)

close_connection_and_exit(0)
