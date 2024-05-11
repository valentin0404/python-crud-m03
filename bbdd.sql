
/* Poseu el vostre número d'usuari substituint 
le alumnexx si soc l'usuari 01 posaré: alumne01_gestor_negocis*/
CREATE DATABASE IF NOT EXISTS 1dd05_gestor_negocis;

/* Aquí també */
use 1dd05_gestor_negocis;

DROP TABLE IF EXISTS client;
DROP TABLE IF EXISTS proveidor;
DROP TABLE IF EXISTS empleat;

-- TAULA

CREATE TABLE client (
	id int(3) AUTO_INCREMENT,
	nom varchar(40) NOT NULL ,
	cognom1 varchar(40),
	cognom2 varchar(40),
	telefon varchar(9),
	PRIMARY KEY  (id) 
);

CREATE TABLE proveidor (
	id int(3) AUTO_INCREMENT,
	empresa varchar(40) NOT NULL ,
	cif varchar(9),
	adreca varchar(40),
	mail varchar(40),
	PRIMARY KEY  (id) 
);

CREATE TABLE empleat (
	id int(3) AUTO_INCREMENT,
	nom varchar(40) NOT NULL ,
	cognom1 varchar(40),
	cognom2 varchar(40),
	departament varchar(40),
	PRIMARY KEY  (id) 
);