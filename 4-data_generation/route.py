#encoding: utf-8

import sys
import datetime
from random import randint

import airport
import common

select_all_query = 'SELECT * FROM "Route";'
insert_query = 'INSERT INTO "Route" (dest_id, freq, introduced, finished) VALUES %s;'
limit = float('inf')

start = datetime.date(1990, 1, 1)
end = datetime.date(2018, 1, 1)
def get_date():
    return start + datetime.timedelta(
            seconds = randint(0, int((end - start).total_seconds())))

def compare_rows(a, b):
    # simplification: routes are not comparebale
    return False

def next():
    dest_id = next.airport_rows[randint(0, len(next.airport_rows) - 1)][0]
    freq = '{} hours'.format(randint(1, 24*7))
    introduced = get_date()
    finished = introduced + datetime.timedelta(365/30 * randint(1, 36))
    if(datetime.date(2018, 1, 1) < finished):
        finished = None
    if finished != None and randint(0, 100) > 95:
        finished = None
    return [dest_id, freq, introduced, finished]
next.airport_rows = []

def hasNext():
    # simplification: there are always new routes
    return True

def populate(db, count):
    try:
        # check whether "Airport has rows and if not, populate the table in an interactive mode
        next.airport_rows = common.select_all_rows(db, airport.select_all_query)
        if 0 == len(next.airport_rows):
            print '"Airports" is empty'
            rv = common.populate_interactive(db, airport)
            if 0 >= rv:
                print 'Not enough rows in "Airport" to fulfil the operation'
                return -1
            next.airport_rows = common.select_all_rows(db, airport.select_all_query)
    except pg_driver.Error as e:
        print e.pgerror
        return -1

    # assume "Airport" has some data
    rows = common.fetch_unused_rows(db, sys.modules[__name__], count)
    return common.insert_rows(db, sys.modules[__name__], rows)
