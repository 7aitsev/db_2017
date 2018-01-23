CREATE OR REPLACE FUNCTION check_new_flight() RETURNS trigger AS $$
DECLARE
    N interval := '1 hour';

    last_fdate "Flight".flight_date%TYPE;
    last_fduration "Flight".flight_duration%TYPE;
    last_airport_id "Route".dest_id%TYPE; -- current aiport id
    target_route "Route";
    target_airport_id "Route".dest_id%TYPE; -- destination airport id
    frequency "Route".freq%TYPE;
    introduced "Route".introduced%TYPE;
    finished "Route".finished%TYPE;
    can_fly_after timestamp;
BEGIN
    SELECT * INTO STRICT target_route
        FROM "Route"
        WHERE id = NEW.route_id;
    IF (target_route.finished IS NOT NULL
        AND target_route.finished <= NEW.flight_date::date
        OR target_route.introduced > NEW.flight_date::date) THEN
        RAISE EXCEPTION 'Invalid flight date for the route (id=%)',
            NEW.route_id;
    END IF;

    SELECT f.flight_date, f.flight_duration,
            CASE WHEN f.direction THEN r.dest_id ELSE 0 END AS airport_id,
            r.freq, r.introduced, r.finished
        INTO last_fdate, last_fduration, last_airport_id,
            frequency, introduced, finished
        FROM "Flight" f
        JOIN "Route" r ON f.route_id = r.id
        WHERE plane_id = NEW.plane_id
        ORDER BY flight_date DESC 
        LIMIT 1;
    IF (FOUND) THEN
        IF (FALSE = NEW.direction) THEN
            target_airport_id := 0;
        ELSE
            target_airport_id := target_route.dest_id;
        END IF;

        IF (last_airport_id != 0 AND target_airport_id != 0) THEN
            RAISE EXCEPTION 'The flight must end in Echo-Avia';
        ELSIF (target_airport_id = last_airport_id) THEN
            RAISE EXCEPTION 'The plain (id=%) is '
                'already in the target airport (id=%)',
                NEW.plane_id, target_airport_id;
        ELSIF (last_airport_id != 0
            AND last_airport_id != target_route.dest_id) THEN
            RAISE EXCEPTION 'The airport (id=%) of departure does not go '
                'through the route', last_airport_id;
        END IF;
        
        can_fly_after := last_fduration + last_fdate + N;
        IF (NEW.flight_date < can_fly_after) THEN
            RAISE EXCEPTION 'The flight cannot be made '
                'at the specified time: too early';
        END IF;
    ELSE
        RAISE NOTICE 'It is the first flight for the plane (id=%)',
            NEW.plane_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_on_new_flight BEFORE INSERT ON "Flight"
    FOR EACH ROW EXECUTE PROCEDURE check_new_flight();
