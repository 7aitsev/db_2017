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

# Clear or populate table according to --clear option
if args.table in all_tables:
    if not args.clear:
        if 0 >= args.number and args.table != 'All':
            print 'Rows count must be positive'
        elif args.table == 'All':
            if None != args.number:
                print '-n (--number) option is being ignored'
            count = 0
            while 0 >= count:
                print 'Enter rows count for "Ticket":',
                try:
                    count = int(input())
                except ValueError:
                    print 'Bad number'
                    continue
                if 0 >= count:
                    print 'Number of rows must be positive'
                    continue
            import ticket
            ticket.populate(db, count)
        else:
            import importlib
            t = importlib.import_module(args.table.lower())
            t.populate(db, args.number)
    else:
        import common
        if args.table == 'All':
            common.clear(db, 'Airport')
            common.clear(db, 'Plane')
            common.clear(db, 'Person')
            common.clear(db, 'Rating')
        else:
            common.clear(db, args.table)
else:
    print 'There is no such table: {}'.format(args.table)
    close_connection_and_exit(1)

close_connection_and_exit(0)
