CREATE TABLE languages
(
  languageid SERIAL PRIMARY KEY,
  language varchar(200) NOT NULL
);

INSERT INTO languages(language)
SELECT DISTINCT language FROM imdb_movielanguages;

ALTER TABLE imdb_movielanguages
ADD COLUMN languageID INTEGER,
ADD FOREIGN KEY (languageID) REFERENCES languages(languageid);

UPDATE imdb_movielanguages as l
SET languageID = (SELECT languageid FROM languages WHERE language=l.language);

ALTER TABLE imdb_movielanguages
DROP COLUMN language;




CREATE TABLE generos
(
  generoid SERIAL PRIMARY KEY,
  genero varchar(200) NOT NULL
);

INSERT INTO generos(genero)
SELECT DISTINCT genre FROM imdb_moviegenres;

ALTER TABLE imdb_moviegenres
ADD COLUMN generoID INTEGER,
ADD FOREIGN KEY (generoID) REFERENCES generos(generoid);

UPDATE imdb_moviegenres as l
SET generoID= (SELECT generoid FROM generos WHERE genero=l.genre);

ALTER TABLE imdb_moviegenres
DROP COLUMN genre;




CREATE TABLE paises
(
  paisid SERIAL PRIMARY KEY,
  pais varchar(200) NOT NULL
);

INSERT INTO paises(pais)
SELECT DISTINCT country FROM imdb_moviecountries;

ALTER TABLE imdb_moviecountries
ADD COLUMN paisID INTEGER,
ADD FOREIGN KEY (paisID) REFERENCES paises(paisid);

UPDATE imdb_moviecountries as l
SET paisID= (SELECT paisid FROM paises WHERE pais=l.country);

ALTER TABLE imdb_moviecountries
DROP COLUMN country;



ALTER TABLE customers
ALTER COLUMN firstname DROP NOT NULL,
ALTER COLUMN lastname DROP NOT NULL,
ALTER COLUMN address1 DROP NOT NULL,
ALTER COLUMN city DROP NOT NULL,
ALTER COLUMN country DROP NOT NULL,
ALTER COLUMN region DROP NOT NULL,
ALTER COLUMN creditcardtype DROP NOT NULL,
ALTER COLUMN creditcardexpiration DROP NOT NULL;


ALTER TABLE imdb_actormovies
ADD CONSTRAINT PK_imdb_actormovies PRIMARY KEY (actorid,movieid);

ALTER TABLE imdb_directormovies
DROP CONSTRAINT imdb_directormovies_pkey,
ADD CONSTRAINT PK_imdb_directormovies PRIMARY KEY (directorid,movieid);

ALTER TABLE imdb_moviegenres
ADD CONSTRAINT PK_imdb_genresmovies PRIMARY KEY (generoid,movieid);

ALTER TABLE imdb_movielanguages
ADD CONSTRAINT PK_imdb_languagemovies PRIMARY KEY (languageid,movieid);

ALTER TABLE imdb_moviecountries
ADD CONSTRAINT PK_imdb_countrymovies PRIMARY KEY (paisid,movieid);


CREATE TABLE orderdetailcopy
(
  orderid integer NOT NULL,
  prod_id integer NOT NULL,
  price numeric, -- price without taxes when the order was paid
  quantity integer NOT NULL
);

INSERT INTO orderdetailcopy(orderid, prod_id, quantity)
SELECT orderid, prod_id, SUM(quantity) as quantity 
FROM orderdetail
GROUP BY (orderid, prod_id);

DROP TABLE orderdetail;

ALTER TABLE orderdetailcopy
RENAME TO orderdetail;

ALTER TABLE orderdetail
ADD CONSTRAINT PK_imdb_orderdetail PRIMARY KEY (orderid, prod_id),
ADD CONSTRAINT products_prodid_fkey FOREIGN KEY (prod_id)
      REFERENCES products (prod_id);

ALTER TABLE orderdetail
ADD CONSTRAINT products_orderid_fkey FOREIGN KEY (orderid)
      REFERENCES orders (orderid);

ALTER TABLE orders
ADD CONSTRAINT products_customerid_fkey FOREIGN KEY (customerid)
      REFERENCES customers (customerid);