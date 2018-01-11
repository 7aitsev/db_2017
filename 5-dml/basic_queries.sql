--- select ALL from all tables
SELECT * FROM "Airport";
SELECT * FROM "Flight";
SELECT * FROM "Person";
SELECT * FROM "Pilot";
SELECT * FROM "Plane";
SELECT * FROM "Rating";
SELECT * FROM "Route";
SELECT * FROM "Ticket";

--- using LIKE, BETWEEN and IN
SELECT name, speed FROM "Plane"
    WHERE speed > 600 and name ILIKE '%company%';

SELECT name, year FROM "Plane"
    WHERE year BETWEEN '2007-01-01'::date AND '2007-12-31'::date;

SELECT name, capacity, service_life FROM "Plane"
    WHERE capacity BETWEEN 100 AND 200 AND service_life IN (27, 30, 33);

--- value expressions
SELECT year + (service_life::text || ' years')::interval
        AS expiration_date
    FROM "Plane" LIMIT 10;

SELECT name,
        bday,
        CASE WHEN age(bday) > '18 years'::interval
            THEN 'adult'
            ELSE 'minor'
        END AS adult
    FROM "Person" LIMIT 20;

--- sorting
SELECT * FROM "Ticket" ORDER BY price DESC, flight_id ASC LIMIT 10;
SELECT * FROM "Route" WHERE finished IS NOT NULL ORDER BY introduced LIMIT 10;

--- aggregate functions
SELECT AVG(age(bday)) FROM "Person" LIMIT 10;
SELECT max(flight_duration) FROM "Flight" LIMIT 10;

--- using JOIN
SELECT name, bday, phone, rating FROM "Person" JOIN "Pilot" USING(id) LIMIT 10;
SELECT name, phone FROM "Person" p LEFT JOIN "Ticket" t ON p.id = t.person_id
    WHERE t.person_id IS NULL LIMIT 10;

--- using HAVING
SELECT p.name, p.phone, COUNT(t.person_id) AS tickets
    FROM "Person" p JOIN "Ticket" t ON p.id = t.person_id
    GROUP BY p.name, p.phone, t.person_id
    HAVING COUNT(t.person_id) > 2
    ORDER BY tickets LIMIT 10;

SELECT flight_id, SUM(price) AS total_price
    FROM "Ticket"
    GROUP BY flight_id
    HAVING SUM(price) > 500000
    ORDER BY total_price DESC LIMIT 10;

--- using subqueries
SELECT name, capacity FROM "Plane"
    WHERE capacity < (SELECT AVG(capacity) FROM "Plane") LIMIT 10;

SELECT a.city FROM (
    SELECT sq.flight_id, sq.plane_id,
        (sq.tickets_cnt / p.capacity::float) AS load
        FROM (
            SELECT t.flight_id, f.plane_id, count(*) tickets_cnt
                FROM "Ticket" t JOIN "Flight" f ON t.flight_id = f.id
                GROUP BY t.flight_id, f.plane_id
        ) AS sq
        JOIN "Plane" p ON sq.plane_id = p.id
        ORDER BY load DESC LIMIT 1
    ) AS bad
    JOIN "Flight" f ON f.id = bad.flight_id
    JOIN "Route" r ON r.id = f.route_id
    JOIN "Airport" a ON a.id = r.dest_id;
   
--- using UPDATE
UPDATE "Rating" SET salary_per_hour = salary_per_hour + 2000
    WHERE salary_per_hour < 12000;

UPDATE "Route" SET finished = CURRENT_DATE
    WHERE id IN (
        SELECT id
            FROM "Route"
            WHERE finished IS NULL
                  AND extract(years from age(introduced)) > 26
    );

--- using DELETE
INSERT INTO "Ticket" (flight_id, seat, purchase_date, price, person_id)
    VALUES (7894, 4, '2017-09-20', 100000, 69888);
DELETE FROM "Ticket" WHERE price = (SELECT MAX(price) FROM "Ticket");

--- DELETE with subquery
DELETE FROM "Flight"
    WHERE id IN (
        SELECT f.id
        FROM "Flight" f LEFT JOIN "Ticket" t ON f.id = t.flight_id
        WHERE t.flight_id IS NULL
    );

--- individual 1
SELECT id, name, bday, phone, planes_count
    FROM "Person" JOIN (
        SELECT t.person_id, COUNT(DISTINCT(f.plane_id)) AS planes_count
            FROM "Ticket" t JOIN "Flight" f on f.id = t.flight_id
            WHERE f.flight_date BETWEEN '2013-09-01' AND '2017-06-01'
            GROUP BY t.person_id
            ORDER BY planes_count DESC
            LIMIT 5
    ) as p ON id = person_id;

--- individual 2
SELECT * FROM "Airport"
    WHERE id IN (
        SELECT a.id
        FROM "Airport" a
            JOIN "Route" r ON r.dest_id = a.id
            JOIN "Flight" f ON f.route_id = r.id
        WHERE f.flight_date BETWEEN '2015-03-03' AND '2015-09-09'
        GROUP BY r.id, a.id
        HAVING COUNT(a.id) < 3 LIMIT 10
    );

--- individual 3

