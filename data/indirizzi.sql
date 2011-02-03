LOAD DATA LOCAL INFILE '/home/goshawk/Projects/cacerp/cacerp/data/gallicano2010.csv'
INTO TABLE callcenter_persona
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
ESCAPED BY '"'
LINES TERMINATED BY '\n'
(cognome, nome, indirizzo, numero_civico, cap, citta, provincia, telefono);

