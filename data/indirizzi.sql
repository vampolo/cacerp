LOAD DATA LOCAL INFILE 'indirizzi-gallicano-marzo-2011.csv'
INTO TABLE callcenter_persona
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
ESCAPED BY '"'
LINES TERMINATED BY '\n'
(cognome, nome, indirizzo, cap, citta, provincia, telefono);

