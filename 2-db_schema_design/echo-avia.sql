CREATE TABLE "Rating" (
	"rating" numeric(1) PRIMARY KEY,
	"salary_per_hour" int NOT NULL,
    CHECK ("salary_per_hour" > 0)
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Pilot" (
	"id" SERIAL PRIMARY KEY,
	"name" varchar(200) NOT NULL,
	"bday" DATE NOT NULL,
	"rating" numeric(1) REFERENCES "Rating"("rating"),
    UNIQUE ("name", "bday"),
    CHECK ("bday" >= '1970-01-01')
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Plane" (
	"id" serial NOT NULL,
	"name" varchar(100) NOT NULL,
	"year" DATE NOT NULL,
	"service_life" int NOT NULL DEFAULT '20',
	"speed" int NOT NULL,
	"capacity" int NOT NULL,
	CONSTRAINT Plane_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Airport" (
	"id" SERIAL PRIMARY KEY,
	"name" varchar(100) NOT NULL,
	"city" varchar(100) NOT NULL,
	"country" varchar(100) NOT NULL,
	"lat" numeric(8,5) NOT NULL,
	"lon" numeric(8,5) NOT NULL,
	"distance" int NOT NULL,
    UNIQUE("lat", "lon"),
    CHECK("distance" > 0)
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Client" (
	"id" SERIAL PRIMARY KEY,
	"name" varchar(200) NOT NULL,
	"bday" DATE NOT NULL,
	"phone" varchar(20) NOT NULL UNIQUE,
    UNIQUE ("name", "bday", "phone"),
    CHECK ("bday" >= '1910-01-01')
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Flight" (
	"id" SERIAL PRIMARY KEY,
	"pilot_id" int REFERENCES "Pilot"("id"),
	"aiport_id" int REFERENCES "Airport"("id"),
	"plane_id" int REFERENCES "Plane"("id"),
	"flight_date" TIMESTAMP NOT NULL,
	"flight_duration" interval NOT NULL,
    UNIQUE ("plane_id", "flight_date"),
    UNIQUE ("pilot_id", "flight_date"),
    CHECK ("flight_date" >= '2017-10-01'::date),
    CHECK ("flight_duration" >= '30 min'::interval)
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Ticket" (
	"id" SERIAL PRIMARY KEY,
	"client_id" int REFERENCES "Client"("id"),
	"flight_id" int REFERENCES "Flight"("id"),
	"seat" int NOT NULL,
	"purchase_date" DATE NOT NULL,
	"price" int NOT NULL,
    UNIQUE ("client_id", "flight_id", "seat"),
    CHECK ("price" > 0),
    CHECK ("purchase_date" >= '2017-10-01')
) WITH (
  OIDS=FALSE
);
