-- 
-- Add three-letter code for each airport
-- 

-- Add collumn "code"
ALTER TABLE "Airport" ADD COLUMN "code" char(3)
	UNIQUE CHECK("code" ~ '^[A-Z]{3}$');
-- Fill appropriate fileds
UPDATE "Airport" SET "code" = 'ALD' WHERE "id" = 1;
UPDATE "Airport" SET "code" = 'PUL' WHERE "id" = 2;
UPDATE "Airport" SET "code" = 'VNU' WHERE "id" = 3;
UPDATE "Airport" SET "code" = 'DOM' WHERE "id" = 4;
UPDATE "Airport" SET "code" = 'VIT' WHERE "id" = 5;
UPDATE "Airport" SET "code" = 'CHR' WHERE "id" = 6;
-- Add constraint
ALTER TABLE "Airport" ALTER COLUMN "code" SET NOT NULL;


-- 
-- Routing information
-- 
CREATE TABLE "Route" (
	"id" SERIAL PRIMARY KEY,
    "dest_id" int NOT NULL REFERENCES "Airport"("id"),
    "freq" interval NOT NULL,
    "introduced" date NOT NULL,
    "finished" date
) WITH (
  OIDS=FALSE
);

INSERT INTO "Route" (dest_id, freq, introduced) VALUES
(1, '1 day', '2017-10-01'),
(2, '1 day', '2017-10-01'),
(3, '1 day', '2017-10-01'),
(4, '1 day', '2017-10-01'),
(5, '1 day', '2017-10-01'),
(6, '1 day', '2017-10-01');

-- Direction to "Flight"
ALTER TABLE "Flight" ADD COLUMN "direction" boolean;
UPDATE "Flight" SET "direction" = false WHERE true;
ALTER TABLE "Flight" ALTER COLUMN "direction" SET NOT NULL;

ALTER TABLE "Flight" ADD COLUMN "route_id" INT REFERENCES "Route"("id");
-- Fill "route_id": R.id -> R.dest_id -> A.id
UPDATE "Flight" SET "route_id" = R."id" FROM "Route" R,
    "Airport" A WHERE "aiport_id" = A."id" AND R."dest_id" = A."id";

-- "route_id" instead of "aiport_id"
ALTER TABLE "Flight" DROP COLUMN "aiport_id",
    ALTER COLUMN "route_id" SET NOT NULL,
    ALTER COLUMN "plane_id" SET NOT NULL;

-- No more countries
ALTER TABLE "Airport" DROP COLUMN "country";

-- 
-- Client, Pilot -> Person and Pilot
-- 
CREATE TABLE "Person" WITHOUT OIDS AS (
    SELECT * FROM "Client"
);
CREATE SEQUENCE Person_id_seq;
ALTER SEQUENCE Person_id_seq RESTART WITH 8 OWNED BY "Person"."id";
ALTER TABLE "Person" ALTER COLUMN "id" SET DEFAULT nextval('Person_id_seq');
-- Add phones
ALTER TABLE "Pilot" ADD COLUMN "phone" varchar(20);
UPDATE "Pilot" SET "phone" = '89238233' WHERE "id" = 1;
UPDATE "Pilot" SET "phone" = '89991234567' WHERE "id" = 2;
UPDATE "Pilot" SET "phone" = '88128943409' WHERE "id" = 3;
UPDATE "Pilot" SET "phone" = '84759832000' WHERE "id" = 4;
UPDATE "Pilot" SET "phone" = '89211234567' WHERE "id" = 5;

-- Merge "Pilot" into "Person"
INSERT INTO "Person" (name, bday, phone) select P."name", P."bday", P."phone" from "Pilot" P;
-- Add constraints
ALTER TABLE "Person" ADD PRIMARY KEY ("id"),
    ALTER COLUMN "name" SET NOT NULL,
    ALTER COLUMN "bday" SET NOT NULL,
    ALTER COLUMN "phone" SET NOT NULL,
    ADD CHECK("bday" >= '1910-01-01'),
    ADD UNIQUE("name", "bday", "phone");
-- Copy content of "Pilot" to "Pilot2"
CREATE TABLE "Pilot2" (
    "id" int PRIMARY KEY REFERENCES "Person"("id"),
    "rating" numeric(1) NOT NULL REFERENCES "Rating"("rating"),
    "old_id" int
) WITH (
    OIDS=FALSE
);
INSERT INTO "Pilot2" (id, rating, old_id)
    SELECT Pers.id, Pil.rating, Pil.id
    FROM "Person" Pers, "Pilot" Pil
    WHERE Pers.name = Pil.name AND Pers.bday = Pil.bday AND Pers.phone = Pil.phone;

-- Change constraint for "pilot_id"
ALTER TABLE "Flight" DROP CONSTRAINT "Flight_pilot_id_fkey";

-- Set new ids for "pilot_id"
UPDATE "Flight" SET "pilot_id" = P2."id" from "Pilot2" P2
    where "pilot_id" = P2."old_id";
-- Drop "old_id"
ALTER TABLE "Pilot2" DROP COLUMN "old_id";
-- Drop "Pilot" and rename "Pilot2"
DROP TABLE "Pilot";
ALTER TABLE "Pilot2" RENAME TO "Pilot";
-- Set FK constraint back
ALTER TABLE "Flight" ADD FOREIGN KEY ("pilot_id") REFERENCES "Pilot"("id"),
    ALTER COLUMN "pilot_id" SET NOT NULL;

-- "person_id" insted of "client_id"
ALTER TABLE "Ticket" ADD COLUMN "person_id" int REFERENCES "Person"("id");
UPDATE "Ticket" SET "person_id" = "client_id"
    FROM "Client", "Person" WHERE "Person"."id" = "Client"."id";
-- Also add NOT NULL constraint for "flight_id"
ALTER TABLE "Ticket" DROP COLUMN "client_id",
    ALTER COLUMN "flight_id" SET NOT NULL,
    ALTER COLUMN "person_id" SET NOT NULL;
-- No longer needed
DROP TABLE "Client";
