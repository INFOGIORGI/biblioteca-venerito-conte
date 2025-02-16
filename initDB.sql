DROP TABLE IF EXISTS Autori;
DROP TABLE IF EXISTS Libri;
DROP TABLE IF EXISTS LibriPerAutore;
DROP TABLE IF EXISTS Utenti;
DROP TABLE IF EXISTS Prestiti;

CREATE TABLE IF NOT EXISTS Autori(
    codA varchar(20) PRIMARY KEY,
    nome varchar(20),
    cognome varchar(20),
    dataNascita date,
    dataMorte date
);


CREATE TABLE IF NOT EXISTS Libri(
    isbn char(13) PRIMARY KEY,
    categoria varchar(20),
    titolo varchar(20),
    codA varchar(20),
    prezzo double(4, 2),
    anno int(255),
    copie int(255),
    FOREIGN KEY(codA) REFERENCES Autori(codA)
);


CREATE TABLE IF NOT EXISTS LibriPerAutore(
    isbn char(13),
    codA varchar(20),
    PRIMARY KEY(isbn, codA),
    FOREIGN KEY(isbn) REFERENCES Libri(isbn),
    FOREIGN KEY(codA) REFERENCES Autori(codA)
);

CREATE TABLE IF NOT EXISTS Utenti(
    username varchar(20) PRIMARY KEY,
    nome varchar(20),
    cognome varchar(20),
    email varchar(20)
);

CREATE TABLE IF NOT EXISTS Prestiti(
    username varchar(20),
    isbn char(13),
    dataPrestito date,
    dataRestituizione date,
    PRIMARY KEY(username, isbn, dataPrestito),
    FOREIGN KEY(username) REFERENCES Utenti(username),
    FOREIGN KEY(isbn) REFERENCES Libri(isbn),
    CHECK(dataRestituizione > dataPrestito)
);