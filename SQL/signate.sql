create schema signate;



create table train (
	datetid timestamp,
	y int,
	week char,
	soldout boolean,
	name varchar,
	kcal int,
	remarks varchar,
	event varchar,
	payday boolean,
	weather varchar,
	precipitation float,
	temperature float
);


create table test (
	datetid timestamp,
	y int,
	week char,
	soldout boolean,
	name varchar,
	kcal int,
	remarks varchar,
	event varchar,
	payday boolean,
	weather varchar,
	precipitation float,
	temperature float
);



create table wk_train (
	datetid text,
	y text,
	week text,
	soldout text,
	name text,
	kcal text,
	remarks text,
	event text,
	payday text,
	weather text,
	precipitation text,
	temperature text
);


create table wk_test (
	datetid text,
	y text,
	week text,
	soldout text,
	name text,
	kcal text,
	remarks text,
	event text,
	payday text,
	weather text,
	precipitation text,
	temperature text
);
