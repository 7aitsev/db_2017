#encoding: utf-8

import psycopg2 as pg_driver

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

def is_in_db(row, dbrows, compare_rows):
    print row
    for dbrow in dbrows:
        print dbrow
        if compare_rows(row, dbrow):
            return True
    return False

def fetch_unused_rows(db, table, compare_rows, limit):
    import csv
    with open(table.filepath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        keys = reader.next() # get the header
        out = []
        try:
            dbrows = table.selectAllRows(db)
            count = 0
            for row in reader:
                if count >= limit:
                    break
                tup = table.mkTupleFromRow(row)
                if not is_in_db(tup, dbrows, compare_rows):
                    out += [tup]
                    count += 1
        except pg_driver.Error as e:
            print e.pgerror
            db.rollback()
        return out
