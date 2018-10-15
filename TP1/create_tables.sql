-- Schema: public
DROP TABLE IF EXISTS Contacto;
DROP TABLE IF EXISTS EsArchienemigo;
DROP TABLE IF EXISTS Interviene;
DROP TABLE IF EXISTS OficialIntervieneEn;
DROP TABLE IF EXISTS OficialEstaInvolucradoEn;
DROP TABLE IF EXISTS RelacionCivil;
DROP TABLE IF EXISTS CivilDomicilio;
DROP TABLE IF EXISTS SuperheroeCivil;
DROP TABLE IF EXISTS HabilidadSuperHeroe;
DROP TABLE IF EXISTS SuperheroeSupervillano;
DROP TABLE IF EXISTS Supervillano;
DROP TABLE IF EXISTS SuperheroeIncidente;
DROP TABLE IF EXISTS Superheroe;
DROP TABLE IF EXISTS Civil;
DROP TABLE IF EXISTS Estado;
DROP TABLE IF EXISTS Seguimiento;
DROP TABLE IF EXISTS Incidente;
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

CREATE TABLE Incidente
(
    idIncidente integer NOT NULL,
    tipo character(20) NOT NULL,
    fecha date NOT NULL,
    idDomicilio integer NOT NULL,
    
    PRIMARY KEY (idIncidente),
    FOREIGN KEY (idDomicilio) REFERENCES Domicilio
);

CREATE TABLE Seguimiento
(
    numero integer NOT NULL,
    descripcion character(100) NOT NULL,
    conclusion character(100),
    idIncidente integer NOT NULL,
    nroPlaca integer NOT NULL,
    
    PRIMARY KEY (numero),
    FOREIGN KEY (idIncidente) REFERENCES Incidente,
    FOREIGN KEY (nroPlaca) REFERENCES Oficial
);

CREATE TABLE Estado
(
    idEstado integer NOT NULL,
    nombre character(20) NOT NULL,
    fechaInicio date NOT NULL,
    fechaFin integer NOT NULL,
    idSeguimiento integer NOT NULL,
    
    PRIMARY KEY (idEstado),
    FOREIGN KEY (idSeguimiento) REFERENCES Seguimiento
);

CREATE TABLE Civil
(
    idCivil integer NOT NULL,
    nombre character(20) NOT NULL,
    idOrganizacion integer,
    
    PRIMARY KEY (idCivil),
    FOREIGN KEY (idOrganizacion) REFERENCES OrganizacionDelictiva
);

CREATE TABLE Superheroe
(
    idSuperheroe int NOT NULL,
    colorDisfraz character(15) NOT NULL,
    nombreDeFantasia character(40) NOT NULL,
    idCivil int NOT NULL,

    PRIMARY KEY (idSuperheroe),
    FOREIGN Key (idCivil) REFERENCES Civil
);

CREATE TABLE Supervillano
(
    idCivil integer NOT NULL,
    nombreDeVillano character(40) NOT NULL,
    
    PRIMARY KEY (idCivil),
    FOREIGN KEY (idCivil) REFERENCES Civil
);

-------------- Relaciones M-N --------------------

CREATE TABLE SuperheroeSupervillano
(
    idSuperheroe integer NOT NULL,
    idCivil integer NOT NULL,
    
    PRIMARY KEY (idSuperheroe, idCivil),
    FOREIGN KEY (idSuperheroe) REFERENCES Superheroe,
    FOREIGN KEY (idCivil) REFERENCES Civil
);

CREATE TABLE HabilidadSuperHeroe
(
    idHabilidad integer NOT NULL,
    idSuperheroe integer NOT NULL,
    
    PRIMARY KEY (idSuperheroe, idHabilidad),
    FOREIGN KEY (idSuperheroe) REFERENCES Superheroe,
    FOREIGN KEY (idHabilidad) REFERENCES Habilidad
);

CREATE TABLE SuperheroeCivil
(
    idSuperheroe integer NOT NULL,
    idCivil integer NOT NULL,
    
    PRIMARY KEY (idSuperheroe, idCivil),
    FOREIGN KEY (idSuperheroe) REFERENCES Superheroe,
    FOREIGN KEY (idCivil) REFERENCES Civil
);

CREATE TABLE CivilDomicilio
(
    idCivil integer NOT NULL,
    idDomicilio integer NOT NULL,
    
    PRIMARY KEY (idDomicilio, idCivil),
    FOREIGN KEY (idDomicilio) REFERENCES Domicilio,
    FOREIGN KEY (idCivil) REFERENCES Civil
);

CREATE TABLE RelacionCivil
(
    idCivil1 integer NOT NULL,
    idCivil2 integer NOT NULL,
    fechaDesde date NOT NULL,
    Tipo character(15) NOT NULL,
    
    PRIMARY KEY (idCivil1, idCivil2, fechaDesde),
    FOREIGN KEY (idCivil1) REFERENCES Civil,
    FOREIGN KEY (idCivil2) REFERENCES Civil
);

CREATE TABLE OficialEstaInvolucradoEn
(
    nroPlaca integer NOT NULL,
    idIncidente integer NOT NULL,

    PRIMARY KEY (nroPlaca, idIncidente),
    FOREIGN KEY (nroPlaca) REFERENCES Oficial,
    FOREIGN KEY (idIncidente) REFERENCES Incidente
);

CREATE TABLE OficialIntervieneEn
(
    nroPlaca integer NOT NULL,
    idIncidente integer NOT NULL,

    PRIMARY KEY (nroPlaca, idIncidente),
    FOREIGN KEY (nroPlaca) REFERENCES Oficial,
    FOREIGN KEY (idIncidente) REFERENCES Incidente
);

CREATE TABLE Interviene
(
    idIncidente integer NOT NULL,
    idRolCivil integer NOT NULL,
    idCivil integer NOT NULL,

    PRIMARY KEY (idIncidente, idRolCivil, idCivil),
    FOREIGN KEY (idIncidente) REFERENCES Incidente,
    FOREIGN KEY (idRolCivil) REFERENCES RolCivil,
    FOREIGN KEY (idCivil) REFERENCES Civil
);

CREATE TABLE EsArchienemigo
(
    idSuperheroe integer NOT NULL,
    idCivil integer NOT NULL,

    PRIMARY KEY (idSuperheroe, idCivil),
    FOREIGN KEY (idSuperheroe) REFERENCES Superheroe,
    FOREIGN KEY (idCivil) REFERENCES Civil
);

CREATE TABLE SuperheroeIncidente
(
    idSuperheroe integer NOT NULL,
    idIncidente integer NOT NULL,

    PRIMARY KEY (idSuperheroe, idIncidente),
    FOREIGN KEY (idSuperheroe) REFERENCES Superheroe,
    FOREIGN KEY (idIncidente) REFERENCES Incidente
);

CREATE TABLE Contacto
(
    idSuperheroe integer NOT NULL,
    idCivil integer NOT NULL,

    PRIMARY KEY (idSuperheroe, idCivil),
    FOREIGN KEY (idSuperheroe) REFERENCES Superheroe,
    FOREIGN KEY (idCivil) REFERENCES Civil
);