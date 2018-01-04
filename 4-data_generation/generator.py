#!/usr/bin/python
#encoding: utf-8

import argsreader
args = argsreader.getargs()

import psycopg2 as pg_driver

import psycopg2.pool as pool
pg_pool = pool.SimpleConnectionPool(1, 2, user=args.user, dbname=args.dbname, host=args.host)


db = pg_pool.getconn()
cur = db.cursor()
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';")
db.commit()
all_tables = [t[0] for t in cur.fetchall()]

import common
import person
import rating
import plane
import airport
# Clear or populate table according to --clear option
if args.table in ['all'] + all_tables:
    if not args.clear:
        if args.table == 'Person':
            person.populate(db, args.number)
        elif args.table == 'Rating':
            rating.populate(db, args.number)
        elif args.table == 'Plane':
            plane.populate(db, args.number)
        elif args.table == 'Airport':
            airport.populate(db, args.number)
    else:
        if args.table == 'all':
            person.clear(db)
            rating.clear(db)
            plane.clear(db)
            aiport.clear(db)
        elif args.table == 'Person':
            person.clear(db)
        elif args.table == 'Rating':
            rating.clear(db)
        elif args.table == 'Plane':
            plane.clear(db)
        elif args.table == 'Airport':
            airport.clear(db)
else:
    print 'There is no such table: {}'.format(args.table)

cur.close()
pg_pool.closeall()
exit(1)
