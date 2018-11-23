
from datos import *

from random import choice, randrange
from itertools import chain

from datetime import date, timedelta
import datetime, sys, os



# redirige output al archivo txt
sys.stdout = open(os.getcwd() + "/data_generating_queries_res.txt", "w")

###############################################################
######################### Globals #############################
###############################################################


##############################################################################
####################### Helpers for generating content #######################
##############################################################################


def generate_date_time(fecha, hora):
    return str(fecha[0]) + "-" + str(fecha[1]) + "-" + str(fecha[2]) + " " + str(hora[0]) + ":" + str(hora[1]) + ":" + str(hora[2])

def get_day_id(f):
    return int( date(f[0], f[1], f[2]).weekday() )

def append_string_array(arr):
    return str(arr[0]) + "-" + str(arr[1]) + "-" + str(arr[2])

def generateFechaDeIngresoOficial():
    fecha_inicio = generate_date("1980-01-01", "1990-12-27")
    return datetime.date(fecha_inicio[0], fecha_inicio[1], fecha_inicio[2]).isoformat()

def generateFechaDeDesignacionDesde():
    fecha_inicio = generate_date("1991-01-01", "1996-12-27")
    return datetime.date(fecha_inicio[0], fecha_inicio[1], fecha_inicio[2]).isoformat()

def generateFechaDeDesignacionHasta():
    fecha_inicio = generate_date("1996-01-01", "2000-12-27")
    return datetime.date(fecha_inicio[0], fecha_inicio[1], fecha_inicio[2]).isoformat()

def dameFechaGeneral():
    fecha_inicio = generate_date("1980-01-01", "2000-12-27")
    return datetime.date(fecha_inicio[0], fecha_inicio[1], fecha_inicio[2]).isoformat()

def generate_random(a, b):
    begin = a
    end   = b
    
    if a > b:
        begin = b
        end   = a

    if begin == end:
        end += 1

    return randrange(begin, end)

def generate_date(begin, end):
  end_elems   = end.split("-")
  begin_elems = begin.split("-")

  year  = generate_random( int(begin_elems[0]), int(end_elems[0]) )
  month = generate_random( int(begin_elems[1]), int(end_elems[1]) )
  day   = generate_random( int(begin_elems[2]), int(end_elems[2]) )

  return [year, month, day]

def generate_time(begin, end):
    end_elems   = end.split(":")
    begin_elems = begin.split(":")

   
    hour   = generate_random( int(begin_elems[0]), int(end_elems[0]) )
    minute = generate_random( int(begin_elems[1]), int(end_elems[1]) )
    second = generate_random( int(begin_elems[2]), int(end_elems[2]) )
    
    return [hour, minute, second]

def generate_consumible(id_consumible):
    print( insert_query( "consumible",
                        ( id_consumible )
                      ) 
    )


def insert_query(table_name, values):
    if type(values) is not tuple:
        if type(values) is str:
            return "INSERT INTO " + table_name + " VALUES (\"" + str(values) + "\");"
        else:
            return "INSERT INTO " + table_name + " VALUES (" + str(values) + ");"
    elif len(values):
        s = []
        for i in values:
          if type(i) != int:
            s.append("'"+i+"'" if i != "NULL" else i)
          else:
            s.append(str(i))

        st = "({})".format(','.join(s))
        return "INSERT INTO " + table_name + " VALUES " + st + ";"


##################################################################
####################### Content generation #######################
##################################################################

    
# TABLA HABILIDAD LIMITE DE 20 CARACTERES

for i in range(len(HABILIDADES)):
  print(insert_query("Habilidad", (i,HABILIDADES[i][:20])))

# TABLA barrio LIMITE DE 20 CARACTERES

for i in range(len(BARRIO)):
  print(insert_query("Barrio", (i,BARRIO[i][:20])))

# TABLA ORGANIZACION DELICTIVA LIMITE DE 20 CARACTERES

for i in range(len(ORG_DELICTIVA)):
  print(insert_query("OrganizacionDelictiva", (i,ORG_DELICTIVA[i][:20])))

#CREATE TABLE Domicilio

for i in range(2500):
  print(insert_query("Domicilio", (i,choice(CALLES)[:20],
  randrange(1,5000), choice(CALLES)[:20], choice(CALLES)[:20],
  randrange(1,len(BARRIO)))))


# CREATE TABLE Departamento

for i in range(len(DEPARTAMENTO)):
  print(insert_query("Departamento", (i,DEPARTAMENTO[i][:20],
   choice(DESCRIPCIONES)[:100])))

# CREATE TABLE TipoDesignacion

for i in range(len(DESIGNACION)):
  print(insert_query("TipoDesignacion", (i,DESIGNACION[i][:20])))

# CREATE TABLE RolCivil

for i in range(len(ROL_CIVIL)):
  print(insert_query("RolCivil", (i,ROL_CIVIL[i][:20])))

# CREATE TABLE Oficial

OFICIALES = []
for i in range(1000):
  if i == 0:
    depto = 8
  else:
    depto = randrange(len(DEPARTAMENTO))


  unOficial = (i,choice(RANGO_OFICIAL)[:20], 
    choice(PERSONAS_NOMBRES)[:15], choice(PERSONAS_APELLIDOS)[:20],
    generateFechaDeIngresoOficial(), depto)
  OFICIALES.append(unOficial)
  print(insert_query("Oficial", unOficial))


# CREATE TABLE Designacion
# (
#     idDesignacion integer NOT NULL,
#     desde date NOT NULL,
#     hasta date NOT NULL,
#     idTipoDesignacion integer NOT NULL,
#     nroPlaca integer NOT NULL,
    
#     PRIMARY KEY (idDesignacion),
#     FOREIGN KEY (idTipoDesignacion) REFERENCES TipoDesignacion,
#     FOREIGN KEY (nroPlaca) REFERENCES Oficial
# );

TABLA_DESIGNACIONES = []
OFICIALES_DE_ASUNTOS_INTERNOS    = set()
OFICIALES_NO_DE_ASUNTOS_INTERNOS = set()

#Designaciones de asuntos internos
for i in range(len(OFICIALES)):
  unaDesignacion = (i,
    generateFechaDeDesignacionDesde(), 
    generateFechaDeDesignacionHasta(),
    2,
    randrange(len(OFICIALES))
  )

  TABLA_DESIGNACIONES.append(unaDesignacion)
  OFICIALES_DE_ASUNTOS_INTERNOS.add(i)
 
  print(insert_query("Designacion",unaDesignacion ))

#El resto de las designaciones random
for i in range(len(OFICIALES), len(OFICIALES)*4):
  tipoDesignacion = randrange(len(DESIGNACION))

  unaDesignacion = (i,
    generateFechaDeDesignacionDesde(), 
    generateFechaDeDesignacionHasta(),
    tipoDesignacion,
    randrange(len(OFICIALES))
  )

  TABLA_DESIGNACIONES.append(unaDesignacion)
  OFICIALES_NO_DE_ASUNTOS_INTERNOS.add(i)

  print(insert_query("Designacion",unaDesignacion ))


# CREATE TABLE Sumario
# (
#     idSumario integer NOT NULL,
#     resultado character(20) NOT NULL,
#     fecha date NOT NULL,
#     estado integer NOT NULL,
#     descripcion character(20) NOT NULL,
#     nroPlaca integer NOT NULL,
#     idDesginacion integer NOT NULL,
    
#     PRIMARY KEY (idSumario),
#     FOREIGN KEY (idDesginacion) REFERENCES Designacion,
#     FOREIGN KEY (nroPlaca) REFERENCES Oficial
# );

# Sumarios finalizados
for i in range(100):
  unaDesignacion = TABLA_DESIGNACIONES[randrange(len(OFICIALES)*4)]
  iterator_oficial = iter(OFICIALES_DE_ASUNTOS_INTERNOS)

  oficial = next(iterator_oficial)
  while (oficial == unaDesignacion[-1]):
    oficial = next(iterator_oficial)

  print(insert_query("Sumario", (i,
      "FINALIZADO",
      generateFechaDeDesignacionHasta(),
      choice(DESCRIPCIONES)[:20],
      choice(DESCRIPCIONES)[:20],
      oficial,
      unaDesignacion[0]
      )))

# Sumarios no finalizados
for i in range(100, 500):
  unaDesignacion = TABLA_DESIGNACIONES[randrange(len(OFICIALES)*4)]
  iterator_oficial = iter(OFICIALES_DE_ASUNTOS_INTERNOS)

  oficial = next(iterator_oficial)
  while (oficial == unaDesignacion[-1]):
    oficial = next(iterator_oficial)

  resultado = choice(RESULTADO_SUMARIO)[:20]
  while (resultado == "FINALIZADO"):
      resultado = choice(RESULTADO_SUMARIO)[:20]

  print(insert_query("Sumario", (i,
      resultado,
      generateFechaDeDesignacionHasta(),
      'NULL',
      choice(DESCRIPCIONES)[:20],
      oficial,
      unaDesignacion[0]
      )))

# CREATE TABLE Incidente

for i in range(1000):
  print(insert_query("Incidente", (i,
      choice(INCIDENTE)[:20],
      dameFechaGeneral(),
      randrange(2500))
  ))

# CREATE TABLE Seguimiento
# (
#     numero integer NOT NULL,
#     descripcion character(100) NOT NULL,
#     conclusion character(100),
#     idIncidente integer NOT NULL,
#     nroPlaca integer NOT NULL,
    
#     PRIMARY KEY (numero),
#     FOREIGN KEY (idIncidente) REFERENCES Incidente,
#     FOREIGN KEY (nroPlaca) REFERENCES Oficial
# );

for i in range(100):
  print(insert_query("Seguimiento", (i,
    choice(DESCRIPCIONES)[:100],
    "NULL",
    randrange(1000),
    choice(OFICIALES)[0]
    )))

# CREATE TABLE Estado
# (
#     idEstado integer NOT NULL,
#     nombre character(20) NOT NULL,
#     fechaInicio date NOT NULL,
#     fechaFin integer NOT NULL,
#     idSeguimiento integer NOT NULL,
    
#     PRIMARY KEY (idEstado),
#     FOREIGN KEY (idSeguimiento) REFERENCES Seguimiento
# );
for i in range(100):
  print(insert_query("Estado", (i*3,
      ESTADO[0],
      generateFechaDeDesignacionDesde(),
      generateFechaDeDesignacionHasta(),
      i
    )))
  print(insert_query("Estado", (i*3+1,
      ESTADO[1],
      generateFechaDeDesignacionDesde(),
      generateFechaDeDesignacionHasta(),
      i
    )))
  print(insert_query("Estado", (i*3+2,
      ESTADO[2],
      generateFechaDeDesignacionDesde(),
      generateFechaDeDesignacionHasta(),
      i
    )))





# CREATE TABLE Civil
# (
#     idCivil integer NOT NULL,
#     nombre character(20) NOT NULL,
#     idOrganizacion integer,
    
#     PRIMARY KEY (idCivil),
#     FOREIGN KEY (idOrganizacion) REFERENCES OrganizacionDelictiva
# );

CIVILES = []
for i in range(2500):
  if randrange(100) > 80:
    unCivil = (i,
      (choice(PERSONAS_NOMBRES)[:15] +" "+choice(PERSONAS_APELLIDOS)[:20])[:20], randrange(len(ORG_DELICTIVA))) 
  else:
    unCivil = (i,
      (choice(PERSONAS_NOMBRES)[:15] +" "+choice(PERSONAS_APELLIDOS)[:20])[:20])
  CIVILES.append(unCivil)
  print(insert_query("civil", unCivil))


#   CREATE TABLE Superheroe
# (
#     idSuperheroe int NOT NULL,
#     colorDisfraz character(15) NOT NULL,
#     nombreDeFantasia character(40) NOT NULL,
#     idCivil int NOT NULL,

#     PRIMARY KEY (idSuperheroe),
#     FOREIGN Key (idCivil) REFERENCES Civil
# );

heroes = []
for i in range(500):

  if randrange(100) > 80:
    heroe = (i,
      choice(COLORES_TRAJE)[:15],
      choice(SUPER_NOMBRES)[:40]
    )
    
  else:
    heroe =  (i,
      choice(COLORES_TRAJE)[:15],
      choice(SUPER_NOMBRES)[:40],
      randrange(2500)
    )
  heroes.append(heroe)
  print(insert_query("Superheroe", heroe))

# CREATE TABLE Supervillano
# (
#     idCivil integer NOT NULL,
    
#     PRIMARY KEY (idCivil),
#     FOREIGN KEY (idCivil) REFERENCES Civil
# );

cacos = []
for i in range(20):
  cacoId = randrange(2500)
  cacos.append(cacoId)
  print(insert_query("Supervillano", 
    (cacoId,choice(SUPER_NOMBRES)[:20])))

# CREATE TABLE EsArchienemigo
# (Archienemi
#     idSuperheroe integer NOT NULL,
#     idCivil integer NOT NULL,
    
#     PRIMARY KEY (idSuperheroe, idCivil),
#     FOREIGN KEY (idSuperheroe) REFERENCES Superheroe,
#     FOREIGN KEY (idCivil) REFERENCES Civil
# );

for i in range(100):
  print(insert_query("EsArchienemigo", 
    (i, choice(cacos))))


# CREATE TABLE HabilidadSuperHeroe
# (
#     idHabilidad integer NOT NULL,
#     idSuperheroe integer NOT NULL,
    
#     PRIMARY KEY (idSuperheroe, idHabilidad),
#     FOREIGN KEY (idSuperheroe) REFERENCES Superheroe,
#     FOREIGN KEY (idHabilidad) REFERENCES Habilidad
# );

for i in range(len(HABILIDADES)):
  usados = set()
  habilidades = []

  for l in range(0, 5):
    habilidad = choice(heroes)[0]

    if not (habilidad in usados):
      habilidades.append(habilidad)
      usados.add(habilidad) 

  for hab in habilidades:
    print(insert_query("HabilidadSuperHeroe", 
    (i,hab)))    

# CREATE TABLE SuperheroeCivil
# (
#     idSuperheroe integer NOT NULL,
#     idCivil integer NOT NULL,
    
#     PRIMARY KEY (idSuperheroe, idCivil),
#     FOREIGN KEY (idSuperheroe) REFERENCES Superheroe,
#     FOREIGN KEY (idCivil) REFERENCES Civil
# );

for i in range(1000):
  print(insert_query("SuperheroeCivil", 
    (choice(heroes)[0], i)))

# CREATE TABLE RelacionCivil
# (
#     idCivil1 integer NOT NULL,
#     idCivil2 integer NOT NULL,
#     fechaDesde date NOT NULL,
#     Tipo character(15) NOT NULL,
    
#     PRIMARY KEY (idCivil1, idCivil2, fechaDesde),
#     FOREIGN KEY (idCivil1) REFERENCES Civil,
#     FOREIGN KEY (idCivil2) REFERENCES Civil
# );

for i in range(500):
  print(insert_query("RelacionCivil", 
    (randrange(2500), randrange(2500), dameFechaGeneral(), choice(TIPO_RELACION)[:15])))



# CREATE TABLE OficialEstaInvolucradoEn
# (
#     nroPlaca integer NOT NULL,
#     idIncidente integer NOT NULL,

#     PRIMARY KEY (nroPlaca, idIncidente),
#     FOREIGN KEY (nroPlaca) REFERENCES Oficial,
#     FOREIGN KEY (idIncidente) REFERENCES Incidente
# );

for i in range(500):
  print(insert_query("OficialEstaInvolucradoEn", 
    (randrange(1000), randrange(1000))))



# CREATE TABLE OficialIntervieneEn
# (
#     nroPlaca integer NOT NULL,
#     idIncidente integer NOT NULL,

#     PRIMARY KEY (nroPlaca, idIncidente),
#     FOREIGN KEY (nroPlaca) REFERENCES Oficial,
#     FOREIGN KEY (idIncidente) REFERENCES Incidente
# );

for i in range(200):
  print(insert_query("OficialIntervieneEn", 
    (randrange(1000), randrange(1000))))

# CREATE TABLE Interviene
# (
#     idIncidente integer NOT NULL,
#     idRolCivil integer NOT NULL,
#     idCivil integer NOT NULL,

#     PRIMARY KEY (idIncidente, idRolCivil, idCivil),
#     FOREIGN KEY (idIncidente) REFERENCES Incidente,
#     FOREIGN KEY (idRolCivil) REFERENCES RolCivil,
#     FOREIGN KEY (idCivil) REFERENCES Civil
# );

for i in range(200):
  print(insert_query("Interviene", 
    (randrange(1000), randrange(len(ROL_CIVIL)), randrange(2500))))

# CREATE TABLE 
# (
#     idSuperheroe integer NOT NULL,
#     idIncidente integer NOT NULL,

#     PRIMARY KEY (idSuperheroe, idIncidente),
#     FOREIGN KEY (idSuperheroe) REFERENCES Superheroe,
#     FOREIGN KEY (idIncidente) REFERENCES Incidente
# );

for i in range(200):
  print(insert_query("SuperheroeIncidente", 
    (randrange(500), randrange(1000))))


# CREATE TABLE Contacto
# (
#     idSuperheroe integer NOT NULL,
#     idCivil integer NOT NULL,

#     PRIMARY KEY (idSuperheroe, idCivil),
#     FOREIGN KEY (idSuperheroe) REFERENCES Superheroe,
#     FOREIGN KEY (idCivil) REFERENCES Civil
# );

for i in range(200):
  print(insert_query("Contacto", 
    (randrange(500), randrange(200))))


# CREATE TABLE CivilDomicilio
# (
#     idCivil integer NOT NULL,
#     idDomicilio integer NOT NULL,
#     fechaDesde date NOT NULL,
#     fechaHasta date NOT NULL,
#     PRIMARY KEY (fechaDesde),
#     FOREIGN KEY (idDomicilio) REFERENCES Domicilio,
#     FOREIGN KEY (idCivil) REFERENCES Civil
# );

fechas=[]
for i in range(2500):
  f = dameFechaGeneral()

  while f in fechas:
      f = dameFechaGeneral()

  fechas.append(f)
  print(insert_query("CivilDomicilio", 
    (randrange(500), i, f, dameFechaGeneral())))