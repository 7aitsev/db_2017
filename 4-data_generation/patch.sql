ALTER TABLE "Flight" DROP CONSTRAINT "Flight_flight_date_check",
                     ADD CHECK (flight_date >= '1990-01-01'::date);
ALTER TABLE "Ticket" DROP CONSTRAINT "Ticket_purchase_date_check",
                     ADD CHECK (purchase_date >= '1990-01-01'::date);

--- remove rows which viloate unique(flight_id, seat) constraint
WITH
ranked AS (
    SELECT id,
           flight_id, seat,
           row_number() OVER (PARTITION BY flight_id, seat order by seat) AS rank
    FROM "Ticket"
)
DELETE FROM "Ticket" WHERE id IN (SELECT id FROM ranked WHERE rank > 1);
ALTER TABLE "Ticket" ADD UNIQUE (flight_id, seat);

ALTER TABLE "Plane" ADD UNIQUE (name, year),
                    ADD CHECK (year >= '1990-01-01'::date),
                    ADD CHECK (service_life >= 20),
                    ADD CHECK (speed >= 200);
