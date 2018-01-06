#encoding: utf-8

import psycopg2 as pg_driver
import sys
import datetime
from random import randint

import common
import person
import flight

select_all_query = 'SELECT * FROM "Ticket";'
select_all_from_flight_and_plane_query = 'SELECT f.id, pilot_id, flight_date, flight_duration, capacity FROM "Flight" f JOIN "Plane" p ON f.plane_id = p.id;'
select_total_capacity_query = 'SELECT sum(capacity) FROM "Flight" f JOIN "Plane" p ON f.plane_id = p.id;'
insert_query = 'INSERT INTO "Ticket" (flight_id, seat, purchase_date, price, person_id) VALUES %s;'

def generate_price(flight_date, flight_duration):
    w = flight_date.weekday()
    h = float(flight_duration.seconds) / 3600
    return int(generate_price.price_per_hour * generate_price.factors[w] * h)
generate_price.factors = [2, 1.6, 1.2, 1, 1.5, 1.8, 1.9]
generate_price.price_per_hour = 2000.0

def compare_rows(a, b):
    # flight_id and seat
    return a[-5] == b[-5] and a[-4] == b[-4]

def next():
    flight_row = common.get_any_row(next.flight_rows)
    flight_id = flight_row[0]
    id_of_pilot = flight_row[1]
    person_id = id_of_pilot
    while id_of_pilot == person_id:
        person_id = common.get_any_row(next.person_rows)[0]
    capacity = flight_row[-1]
    seat = randint(1, capacity)
    flight_date = flight_row[2].date()
    purchase_date = flight_date - datetime.timedelta(days=randint(0, 6 * 30))
    if purchase_date <= datetime.date(1990, 1, 1):
        purchase_date = datetime.date(1990, 1, 1)
    price = generate_price(flight_date, flight_row[3])
    return [flight_id, seat, purchase_date, price, person_id]
next.flight_rows = []
next.person_rows = []

def hasNext():
    # simplification: there are always new records
    return True

def populate(db, count):
    try:
        next.person_rows = common.check_availability(db, person)
        next.flight_rows = common.check_availability(db, flight, select_all_from_flight_and_plane_query)
    except pg_driver.Error as e:
        print e.pgerror
        db.rollback()
        return -1

    total_seats_count = 0
    try:
        c = db.cursor()
        c.execute(select_total_capacity_query)
        total_seats_count = c.fetchall()
    except pg_driver.Error as e:
        db.rollback()
        return -1
    if 0 == total_seats_count or count > total_seats_count:
        print 'Total seats count: {}\tRequested number of tickets ({}) is too big' \
            .format(total_seats_count, count)
        return -1

    rows = common.fetch_unused_rows(db, sys.modules[__name__], count)
    return common.insert_rows(db, sys.modules[__name__], rows)

def clear(db):
    common.clear(db, 'Ticket')
