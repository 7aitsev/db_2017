CREATE OR REPLACE FUNCTION
rr_linear_scale(ft double precision,
        ft_min double precision, ft_max double precision,
        rating_cnt smallint)
RETURNS smallint AS $$
DECLARE res smallint;
BEGIN
    res := trunc((ft - ft_min) / ((ft_max - ft_min) / rating_cnt));
    IF (res >= rating_cnt) THEN
        res := rating_cnt - 1;
    END IF;
    RETURN rating_cnt - res;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION recalculate_ratings() RETURNS trigger AS $$
DECLARE
    
BEGIN
    WITH pilot_hours AS (
        SELECT pilot_id,
                extract(EPOCH FROM sum(flight_duration)) AS flying_time
            FROM "Flight" GROUP BY pilot_id
            ORDER BY flying_time DESC
    ), ph_stat AS (
        SELECT max(flying_time) AS ft_max, min(flying_time) AS ft_min
            FROM pilot_hours
    ), rating_cnt AS (
        SELECT COUNT(*) AS rating_cnt FROM "Rating"
    ), new_pilot AS (
        SELECT pilot_id, rr_linear_scale(
                    flying_time, ft_min, ft_max, rating_cnt
                ) AS new_rating
            FROM pilot_hours, ph_stat, rating_cnt
        EXCEPT
        SELECT * FROM "Pilot"
    )

    UPDATE "Pilot" SET rating = new_rating
        FROM new_pilot where id = pilot_id;
    
    RETURN NULL; -- is always ignored for statement-level tg fired AFTER
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_ratings AFTER INSERT ON "Flight"
    FOR EACH STATEMENT EXECUTE PROCEDURE recalculate_ratings();
