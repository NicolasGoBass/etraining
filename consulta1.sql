CREATE DATABASE IF NOT EXISTS CASOS_COVID;
USE Prueba3;
CREATE TABLE gender (
    id_gender INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(45)
);

CREATE TABLE type_contagion (
    id_type_contagion INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(45)
);

CREATE TABLE status (
    id_status INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(45)
);

CREATE TABLE department (
    id_department INT PRIMARY KEY,
    name VARCHAR(45)
);

CREATE TABLE municipality (
    id_municipality INT PRIMARY KEY,
    name VARCHAR(200),
    id_department INT,
    FOREIGN KEY (id_department) REFERENCES department(id_department)
);

CREATE TABLE cases (
    id_case INT PRIMARY KEY,
    id_municipality INT,
    age INT,
    id_gender INT,
    id_type_contagion INT,
    id_status INT,
    date_symptom DATETIME NULL,
    date_death DATETIME NULL,
    date_diagnosis DATETIME NULL,
    date_recovery DATETIME NULL,
    FOREIGN KEY (id_municipality) REFERENCES municipality(id_municipality),
    FOREIGN KEY (id_gender) REFERENCES gender(id_gender),
    FOREIGN KEY (id_type_contagion) REFERENCES type_contagion(id_type_contagion),
    FOREIGN KEY (id_status) REFERENCES status(id_status)
);