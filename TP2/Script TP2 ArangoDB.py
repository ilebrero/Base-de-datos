from pyArango.connection import *
import pandas as pd

conn = Connection(username="root", password="")

try:
    db = conn.createDatabase(name="tp2BasesDeDatos")
except CreationError:
    db = conn["tp2BasesDeDatos"]

#levanto las tablas en CSV a Pandas

SUPERHEROE = pd.read_csv("tablascsv/public.superheroe.csv", sep=";")
BARRIO = pd.read_csv("tablascsv/public.barrio.csv", sep=";")
CIVIL = pd.read_csv("tablascsv/public.civil.csv", sep=";")
CIVILDOMICILIO = pd.read_csv("tablascsv/public.civildomicilio.csv", sep=";")
CONTACTO = pd.read_csv("tablascsv/public.contacto.csv", sep=";")
DEPARTAMENTO = pd.read_csv("tablascsv/public.departamento.csv", sep=";")
DESIGNACION = pd.read_csv("tablascsv/public.designacion.csv", sep=";")
DOMICILIO = pd.read_csv("tablascsv/public.domicilio.csv", sep=";")
ESARCHIENEMIGO = pd.read_csv("tablascsv/public.esarchienemigo.csv", sep=";")
ESTADO = pd.read_csv("tablascsv/public.estado.csv", sep=";")
HABILIDAD = pd.read_csv("tablascsv/public.habilidad.csv", sep=";")
HABILIDADSUPERHEROE = pd.read_csv("tablascsv/public.habilidadsuperheroe.csv", sep=";")
INCIDENTE = pd.read_csv("tablascsv/public.incidente.csv", sep=";")
INTERVIENE = pd.read_csv("tablascsv/public.interviene.csv", sep=";")
OFICIAL = pd.read_csv("tablascsv/public.oficial.csv", sep=";")
OFICIALESTAINVOLUCRADOEN = pd.read_csv("tablascsv/public.oficialestainvolucradoen.csv", sep=";")
OFICIALINTERVIENEEN = pd.read_csv("tablascsv/public.oficialintervieneen.csv", sep=";")
ORGANIZACIONDELICTIVA = pd.read_csv("tablascsv/public.organizaciondelictiva.csv", sep=";")
RELACIONCIVIL = pd.read_csv("tablascsv/public.relacioncivil.csv", sep=";")
ROLCIVIL = pd.read_csv("tablascsv/public.rolcivil.csv", sep=";")
SEGUIMIENTO = pd.read_csv("tablascsv/public.seguimiento.csv", sep=";")
SUMARIO = pd.read_csv("tablascsv/public.sumario.csv", sep=";")
SUPERHEROECIVIL = pd.read_csv("tablascsv/public.superheroecivil.csv", sep=";")
SUPERHEROEINCIDENTE = pd.read_csv("tablascsv/public.superheroeincidente.csv", sep=";")
SUPERVILLANO = pd.read_csv("tablascsv/public.supervillano.csv", sep=";")
TIPODESIGNACION = pd.read_csv("tablascsv/public.tipodesignacion.csv", sep=";")

def crear_documento(coleccion, clave, dicc):
    doc = coleccion.createDocument()
    for k in dicc:
        doc[k] = dicc[k]
    doc._key = clave
    doc.save()
    
def indicesDeMN(index, columnaIndex, tabla, columnaADevolver):
    return tabla[tabla[columnaIndex] == index][columnaADevolver].tolist()

def listaDeMN(index,columnaIndex,tabla, indiceDeSegundaTabla,segundaTabla, listaDeAtributos):
    listadeIndices = indicesDeMN(index, columnaIndex, tabla, indiceDeSegundaTabla)
    tablaFiltrada = segundaTabla[segundaTabla[indiceDeSegundaTabla].isin(listadeIndices)]
    if len(listaDeAtributos) == 1:
        return tablaFiltrada[listaDeAtributos[0]].tolist()
    else:
        return tablaFiltrada[listaDeAtributos].to_dict('records')

def puedeSerNull(dicc, key, value):
    if str(value) != "nan":
        dicc[key] = value

def vaciarTabla(tabla):
    aql = "FOR u IN " + tabla + " REMOVE u IN " + tabla
    db.AQLQuery(aql)

def inicializarTabla(tabla):
    try:
        return db.createCollection(name=tabla)
    except:
        vaciarTabla(tabla)
        return db[tabla]

def dame1aN(indice, tabla):
    return tabla.iloc[indice].to_dict()

#SUPERHEROE
superheroeColl = inicializarTabla("superheroe")
for index, row in SUPERHEROE.iterrows():
    dicc = {}
    
    dicc["NombreDeFantasia"] = row["nombredefantasia"]
    dicc["colordisfraz"] = row["colordisfraz"]
    dicc["archienemigos"] = indicesDeMN(index, "idsuperheroe", ESARCHIENEMIGO, "idcivil")
    dicc["habilidades"] = listaDeMN(index,"idsuperheroe",HABILIDADSUPERHEROE, "idhabilidad",HABILIDAD, ["nombre"])
    dicc["incidentes"] = indicesDeMN(index, "idsuperheroe", SUPERHEROEINCIDENTE, "idincidente")
    dicc["contactos"] = indicesDeMN(index, "idsuperheroe", SUPERHEROECIVIL, "idcivil")
    puedeSerNull(dicc,"identidadSecreta",row["idcivil"])
    crear_documento(superheroeColl, str(index), dicc)

oficialColl = inicializarTabla("oficial")
for index, row in OFICIAL.iterrows():
    dicc = {}
    dicc["nroplaca"] = index
    dicc["Nombre"] = row["nombre"]
    dicc["Apellido"] = row["apellido"]
    dicc["Rango"] = row["rango"]
    dicc["FechaIngreso"] = row["fechaingreso"]
    dicc["departamento"] = dame1aN(row["iddpto"], DEPARTAMENTO)
    dicc["sumarios"] = indicesDeMN(index, "nroplaca", SUMARIO, "idsumario")
    dicc["seguimientos"] = indicesDeMN(index, "nroplaca", SEGUIMIENTO, "numero")
    dicc["incidentesInvolucradoEn"] = indicesDeMN(index, "nroplaca", OFICIALINTERVIENEEN, "idincidente")
    dicc["incidentesInterviene"] = indicesDeMN(index, "nroplaca", OFICIALESTAINVOLUCRADOEN, "idincidente")

    #FALTAN LAS DESIGNACIONES
    crear_documento(oficialColl, str(index), dicc)