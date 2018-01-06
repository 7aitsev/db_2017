#encoding: utf-8

import psycopg2 as pg_driver
import sys
import datetime
from random import randint

import common
import pilot
import plane
import route

select_all_query = 'SELECT * FROM "Flight";'
select_all_from_route_and_airport_query = 'SELECT r.id, r.dest_id, r.freq, r.introduced, r.finished, a.distance  FROM "Route" AS r JOIN "Airport" AS a ON r.dest_id = a.id;'
insert_query = 'INSERT INTO "Flight" (pilot_id, plane_id, flight_date, flight_duration, direction, route_id) VALUES %s;'
limit = float('inf')

def generate_flight_date(route_row):
    introduced = datetime.datetime.combine(route_row[-3], datetime.time(0, 0)) # date -> date -> datetime
    freq = route_row[-4] # interval -> timedelta
    finished = route_row[-2] # date -> date
    if finished == None:
        finished = datetime.date(2018, 1, 1)
    max_times = (finished - introduced.date()).total_seconds() / freq.total_seconds()
    return freq * randint(0, int(max_times)) + introduced  # datetime -> timestamp

def generate_flight_duration(route_row, plane_row):
    distance = route_row[-1]
    speed = plane_row[-2]
    return distance // speed * 60 + randint(5, 30)

def compare_rows(a, b):
    o = (a[-4] == b[-4])
    return (o and a[-5] == b[-5]) or (o and a[-6] == b[-6])

def next():
    pilot_id = common.get_any_row(next.pilot_rows)[0]
    plane_row = common.get_any_row(next.plane_rows)
    plane_id = plane_row[0]
    route_row = common.get_any_row(next.route_rows)
    route_id = route_row[0]
    flight_date = generate_flight_date(route_row)
    flight_duration = generate_flight_duration(route_row, plane_row)
    if flight_duration < 30:
        flight_duration = 30
    flight_duration = '{} minutes'.format(flight_duration)
    direction = (randint(0, 1) == 1)
    return [pilot_id, plane_id, flight_date, flight_duration, direction, route_id]
next.route_rows = []
next.pilot_rows = []
next.plane_rows = []

def hasNext():
    # simplification: there are always new records
    return True

def populate(db, count):
    try:
        next.route_rows = common.check_availability(db, route, select_all_from_route_and_airport_query)
        next.pilot_rows = common.check_availability(db, pilot)
        next.plane_rows = common.check_availability(db, plane)
    except pg_driver.Error as e:
        print e.pgerror
        db.rollback()
        return -1
    rows = common.fetch_unused_rows(db, sys.modules[__name__], count)
    return common.insert_rows(db, sys.modules[__name__], rows)
