INSERT INTO "Rating" (rating, salary_per_hour) VALUES
(1, 1000),
(2, 900),
(3, 800);

INSERT INTO "Plane" (name, year, service_life, speed, capacity) values
('A-300', '1991-01-01', 30, 890, 345),
('A-300', '1992-01-01', 30, 890, 345),
('Boeing-747', '1995-01-01', 35, 900, 460),
('Boeing-777', '1994-01-01', 33, 905, 300),
('IL-96', '1991-01-01', 36, 870, 400),
('A-320', '1990-01-01', 31, 840, 330);

INSERT INTO "Airport" (name, city, country, lat, lon, distance) VALUES
('Aldan', 'Abakan', 'Russia', 53.717564, 91.429317, 100),
('Pulkovo', 'St Petersburg', 'Russia', 59.9342, 30.3350, 100),
('Vnukovo', 'Moscow', 'Russia', 55.755, 37.6172, 400),
('Domodedovo', 'Moscow', 'Russia', 55.675, 37.61452, 500),
('Vityazevo', 'Anapa', 'Russia', 44.8857, 37.31991, 1000),
('Chrabrovo', 'Kaliningrad', 'Russia', 54.7104, 20.45244, 2000);

INSERT INTO "Pilot" (name, bday, rating) VALUES
('Irina', '1980-03-20', 2),
('Igor', '1978-12-11', 3),
('Oleg', '1981-05-05', 1),
('Olga', '1985-04-04', 1),
('Alex', '1986-03-01', 2);

INSERT INTO "Client" (name, bday, phone) VALUES
('Ivan Ivanov', '1990-01-01', '3928479832'),
('Andrey Rublev', '1973-09-09', '2398423'),
('Tatiana Maslany', '1980-11-11', '32224224'),
('Nikolay Kalka', '1985-12-12', '12432223'),
('Ekaterina Makarova', '1943-12-12', '324228823'),
('Natasha Lyonne', '1960-11-11', '899398483'),
('Kirill Sarychev', '1920-04-09', '924834999');


INSERT INTO "Flight" (pilot_id, aiport_id, plane_id, flight_date, flight_duration) VALUES
(1, 1, 4, '2017-10-01', '60 min'),
(2, 3, 3, '2017-10-02', '2 hours'),
(3, 4, 3, '2017-10-03', '3 hours'),
(4, 5, 1, '2017-10-03', '1 hour'),
(5, 6, 2, '2017-10-03', '2 hours'),
(1, 1, 4, '2017-10-04', '60 min'),
(2, 3, 3, '2017-10-04', '2 hours'),
(3, 2, 5, '2017-10-04', '3 hours'),
(4, 5, 3, '2017-10-05', '1 hour'),
(5, 3, 6, '2017-10-05', '2 hours');

INSERT INTO "Ticket" (client_id, flight_id, seat, purchase_date, price) VALUES
(1, 1, 20, '2017-10-01', 200),
(1, 2, 12, '2017-10-20', 210),
(2, 1, 21, '2017-10-02', 200),
(3, 1, 22, '2017-10-19', 200),
(4, 1, 19, '2017-10-18', 200),
(5, 1, 18, '2017-10-19', 200),
(6, 1, 18, '2017-10-19', 200),
(7, 1, 17, '2017-10-19', 200),
(7, 3, 43, '2017-10-09', 300),
(6, 4, 50, '2017-10-10', 350),
(5, 5, 1, '2017-10-11', 250),
(4, 6, 2, '2017-10-28', 266),
(3, 7, 3, '2017-10-22', 199),
(2, 8, 4, '2017-10-22', 199),
(1, 9, 5, '2017-10-17', 210),
(5, 10, 6, '2017-10-14', 222);
