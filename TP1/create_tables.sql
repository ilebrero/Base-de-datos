-- Schema: public
DROP TABLE IF EXISTS Sumario;
DROP TABLE IF EXISTS Designacion;
DROP TABLE IF EXISTS Oficial;
DROP TABLE IF EXISTS Domicilio;
DROP TABLE IF EXISTS OrganizacionDelictiva;
DROP TABLE IF EXISTS Barrio;
DROP TABLE IF EXISTS RolCivil;
DROP TABLE IF EXISTS Habilidad;
DROP TABLE IF EXISTS TipoDesignacion;
DROP TABLE IF EXISTS Departamento;

DROP SCHEMA IF EXISTS public;
CREATE SCHEMA public
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;

-- Entidades que no dependen de nadie

CREATE TABLE Departamento
(
    idDepartamento integer NOT NULL,
    nombre character(20) NOT NULL,
    descripcion character(100) NOT NULL,
    PRIMARY KEY (idDepartamento)
);

CREATE TABLE TipoDesignacion
(
    idTipoDesignacion integer NOT NULL,
    nombre character(20) NOT NULL,
    PRIMARY KEY (idTipoDesignacion)
);

CREATE TABLE Habilidad
(
    idHabilidad integer NOT NULL,
    nombre character(20) NOT NULL,
    PRIMARY KEY (idHabilidad)
);

CREATE TABLE RolCivil
(
    idRolCivil integer NOT NULL,
    nombre character(20) NOT NULL,
    PRIMARY KEY (idRolCivil)
);

CREATE TABLE Barrio
(
    idBarrio integer NOT NULL,
    nombre character(20) NOT NULL,
    PRIMARY KEY (idBarrio)
);

CREATE TABLE OrganizacionDelictiva
(
    idOrganizacionDelictiva integer NOT NULL,
    nombre character(20) NOT NULL,
    PRIMARY KEY (idOrganizacionDelictiva)
);

-- asdasd

CREATE TABLE Domicilio
(
    idDomicilio integer NOT NULL,
    calle character(20) NOT NULL,
    altura integer NOT NULL,
    entreCalle1 integer NOT NULL,
    entreCalle2 integer NOT NULL,
    idBarrio integer NOT NULL,
    
    PRIMARY KEY (idDomicilio),
    FOREIGN KEY (idBarrio) REFERENCES Barrio
);

CREATE TABLE Oficial
(
    nroPlaca integer NOT NULL,
    rango character(20) NOT NULL,
    nombre character(15) NOT NULL,
    apellido character(20) NOT NULL,
    fechaIngreso date NOT NULL,
    idDpto integer NOT NULL,
    
    PRIMARY KEY (nroPlaca),
    FOREIGN KEY (idDpto) REFERENCES Departamento
);

CREATE TABLE Designacion
(
    idDesignacion integer NOT NULL,
    desde date NOT NULL,
    hasta date NOT NULL,
    idTipoDesignacion integer NOT NULL,
    nroPlaca integer NOT NULL,
    
    PRIMARY KEY (idDesignacion),
    FOREIGN KEY (idTipoDesignacion) REFERENCES TipoDesignacion,
    FOREIGN KEY (nroPlaca) REFERENCES Oficial
);

CREATE TABLE Sumario
(
    idSumario integer NOT NULL,
    resultado character(20) NOT NULL,
    fecha date NOT NULL,
    estado integer NOT NULL,
    descripcion character(20) NOT NULL,
    nroPlaca integer NOT NULL,
    idDesginacion integer NOT NULL,
    
    PRIMARY KEY (idSumario),
    FOREIGN KEY (idDesginacion) REFERENCES Designacion,
    FOREIGN KEY (nroPlaca) REFERENCES Oficial
);