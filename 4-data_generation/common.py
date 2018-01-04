#encoding: utf-8

import psycopg2 as pg_driver
from psycopg2.extras import execute_values

def clear(db, table):
    cur = db.cursor()
    query = 'TRUNCATE "%s" CASCADE;'
    try:
        if table != 'all':
            # 'table' is NOT a user input, so it's OK
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

def select_all_rows(db, query):
    dbrows = []
    try:
        c = db.cursor()
        c.execute(query)
        dbrows = c.fetchall()
    except pg_driver.Error as e:
        pass
    return dbrows

def is_in_db(row, dbrows, compare_rows):
    for dbrow in dbrows:
        if compare_rows(row, dbrow):
            return True
    return False

def fetch_unused_rows(db, table, limit):
    out = []
    try:
        dbrows = select_all_rows(db, table.select_all_query)
        count = 0
        while count < limit and table.hasNext():
            row = table.next()
            if not is_in_db(row, dbrows, table.compare_rows):
                out.append(row)
                count += 1
    except pg_driver.Error as e:
        print e.pgerror
        db.rollback()
    return out

def insert_rows(db, table, rows):
    count = len(rows)
    if 0 != count:
        try:
            c = db.cursor()
            execute_values(c, table.insert_query, rows)
            db.commit()
        except pg_driver.Error as e:
            print e.pgerror
            db.rollback()
            return
        # execute_values does not give right cursor.rowcount (issue #540)
        print 'Inserted {} rows'.format(count)
    else:
        print 'All records for "{}" are exhausted'.format(table.__name__)
