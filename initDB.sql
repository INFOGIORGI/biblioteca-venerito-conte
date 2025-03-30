DROP TABLE IF EXISTS Prestiti;
DROP TABLE IF EXISTS Utenti;
DROP TABLE IF EXISTS LibriPerAutore;
DROP TABLE IF EXISTS Libri;
DROP TABLE IF EXISTS Autori;
DROP TABLE IF EXISTS RicercheCategoria;

CREATE TABLE IF NOT EXISTS Autori(
    codA VARCHAR(20) PRIMARY KEY,
    nome VARCHAR(50),
    cognome VARCHAR(50),
    dataNascita DATE,
    dataMorte DATE
);

CREATE TABLE IF NOT EXISTS RicercheCategoria (
    categoria VARCHAR(50) PRIMARY KEY,
    nRicerche INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Libri(
    isbn CHAR(13) PRIMARY KEY,
    categoria VARCHAR(50),
    titolo VARCHAR(100),
    codA VARCHAR(20) NOT NULL,
    anno INT,
    copie INT DEFAULT 1,
    riassunto VARCHAR(100),
    FOREIGN KEY (codA) REFERENCES Autori(codA)
);

CREATE TABLE IF NOT EXISTS LibriPerAutore(
    isbn CHAR(13),
    codA VARCHAR(20),
    PRIMARY KEY (isbn, codA),
    FOREIGN KEY (isbn) REFERENCES Libri(isbn),
    FOREIGN KEY (codA) REFERENCES Autori(codA)
);

CREATE TABLE IF NOT EXISTS Utenti(
    username VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(50),
    cognome VARCHAR(50),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE IF NOT EXISTS Prestiti(
    username VARCHAR(50),
    isbn CHAR(13),
    dataPrestito DATE,
    dataRestituzione DATE,
    PRIMARY KEY (username, isbn, dataPrestito),
    FOREIGN KEY (username) REFERENCES Utenti(username),
    FOREIGN KEY (isbn) REFERENCES Libri(isbn),
    CHECK (dataRestituzione > dataPrestito)
);

INSERT INTO Autori (codA, nome, cognome, dataNascita, dataMorte)
VALUES
    ('A001', 'Giovanni', 'Verga', '1840-09-02', '1922-01-27'),
    ('A002', 'Luigi', 'Pirandello', '1867-06-28', '1936-12-10'),
    ('A003', 'Italo', 'Calvino', '1923-10-15', NULL),
    ('A004', 'Alessandro', 'Manzoni', '1785-03-07', '1873-05-22'),
    ('A005', 'Dante', 'Alighieri', '1265-06-01', '1321-09-14'),
    ('A006', 'Lev', 'Tolstoj', '1828-09-09', '1910-11-20'),
    ('A007', 'Fëdor', 'Dostoevskij', '1821-11-11', '1881-02-09'),
    ('A008', 'Virginia', 'Woolf', '1882-01-25', '1941-03-28'),
    ('A009', 'Ernest', 'Hemingway', '1899-07-21', '1961-07-02'),
    ('A010', 'Franz', 'Kafka', '1883-07-03', '1924-06-03');

INSERT INTO Libri (isbn, categoria, titolo, codA, anno, copie, riassunto) 
VALUES 
    ('9788806200501', 'Narrativa', 'I Malavoglia', 'A001', 1881, 10, 'La storia di una famiglia di pescatori siciliani e delle loro difficoltà.'),
    ('9788806220531', 'Drammatico', 'Sei personaggi in cerca d’autore', 'A002', 1921, 8, 'Un dramma teatrale in cui i personaggi cercano il loro autore.'),
    ('9788806240423', 'Fantascienza', 'Le città invisibili', 'A003', 1972, 12, 'Un viaggio immaginario attraverso città fantastiche raccontato da Marco Polo.'),
    ('9788806200518', 'Narrativa', 'I Promessi Sposi', 'A004', 1827, 15, 'La travagliata storia d’amore tra Renzo e Lucia nella Lombardia del XVII secolo.'),
    ('9788806200525', 'Poesia', 'Divina Commedia', 'A005', 1320, 5, 'Il viaggio ultraterreno di Dante tra Inferno, Purgatorio e Paradiso.'),
    ('9788806230604', 'Romanzo', 'Guerra e Pace', 'A006', 1869, 7, 'Un affresco storico e filosofico sulle guerre napoleoniche in Russia.'),
    ('9788806230611', 'Romanzo', 'Delitto e Castigo', 'A007', 1866, 10, 'Un giovane studente compie un omicidio e affronta le conseguenze morali.'),
    ('9788806230628', 'Narrativa', 'Mrs. Dalloway', 'A008', 1925, 9, 'Un romanzo sulla vita interiore di una donna nell’arco di una sola giornata.'),
    ('9788806230635', 'Romanzo', 'Il vecchio e il mare', 'A009', 1952, 6, 'La lotta di un vecchio pescatore cubano contro un enorme marlin.'),
    ('9788806230642', 'Narrativa', 'La Metamorfosi', 'A010', 1915, 11, 'La storia surreale di Gregor Samsa, che si sveglia trasformato in un insetto.');

INSERT INTO LibriPerAutore (isbn, codA)
VALUES
    ('9788806200501', 'A001'),
    ('9788806220531', 'A002'),
    ('9788806240423', 'A003'),
    ('9788806200518', 'A004'),
    ('9788806200525', 'A005'),
    ('9788806230604', 'A006'),
    ('9788806230611', 'A007'),
    ('9788806230628', 'A008'),
    ('9788806230635', 'A009'),
    ('9788806230642', 'A010');
