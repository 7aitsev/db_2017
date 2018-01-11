#encoding: utf-8

import psycopg2 as pg_driver
from psycopg2.extras import execute_values
from random import randint

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
    try:
        c = db.cursor()
        c.execute(query)
        return c.fetchall()
    except pg_driver.Error as e:
        pass

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
                dbrows.append(row)
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
            return -1
        # execute_values does not give right cursor.rowcount (issue #540)
        print 'Inserted {} rows to {}'.format(count, table.__name__)
        return count
    else:
        print 'All records for "{}" are exhausted'.format(table.__name__)
        return 0

def populate_interactive(db, table):
    while True:
        print 'Enter rows count to insert into "{}":'.format(table.__name__),
        try:
            count = int(input())
        except ValueError:
            print 'Bad number'
            continue
        if 0 >= count or table.limit < count:
            print 'The number of rows must be in [1,{}]'.format(table.limit)
            continue
        return table.populate(db, count)

def check_availability(db, table, use_this_query=None):
    try:
        # check whether <table> has rows and if not, populate the table in an interactive mode
        res = select_all_rows(db, table.select_all_query)
        if 0 == len(res):
            print '"{}" is empty'.format(table.__name__)
            rv = populate_interactive(db, table)
            if 0 >= rv:
                raise pg_driver.Error('Not enough rows in "{}" to fulfil the operation'.format(table.__name__))
        query = table.select_all_query if use_this_query == None else use_this_query
        return select_all_rows(db, query)
    except pg_driver.Error as e:
        pass

def get_any_row(rows):
    return rows[randint(0, len(rows) - 1)]
