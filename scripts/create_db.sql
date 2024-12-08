-- reset database --
DROP DATABASE :db;
CREATE DATABASE :db;
\c :db;


-- clean data --
DROP TABLE IF EXISTS dailyreference CASCADE;

-- dailyreference --
CREATE TABLE dailyreference
(
	id UUID primary key NOT NULL UNIQUE,
	date date NOT NULL,
    currencies json
);
CREATE INDEX idx_dailyreference_date ON dailyreference (date);