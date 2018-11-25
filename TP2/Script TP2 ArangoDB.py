from pyArango.connection import *
import pandas as pd
from tqdm import tqdm

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
    else:
        dicc[key] = None

def vaciarTabla(tabla):
    aql = "FOR u IN " + tabla + " REMOVE u IN " + tabla
    db.AQLQuery(aql)

def inicializarTabla(tabla):
    try:
        return db.createCollection(name=tabla)
    except:
        vaciarTabla(tabla)
        return db[tabla]

def dame1aN(indice, tabla, columnas):
    if len(columnas) == 1:
        return tabla.iloc[indice][columnas[0]]
    else:
        return tabla.iloc[indice][columnas].to_dict()

#SUPERHEROE
superheroeColl = inicializarTabla("superheroe")
for index, row in tqdm(SUPERHEROE.iterrows()):
    dicc = {}

    dicc["idsuperheroe"] = row["idsuperheroe"]
    dicc["NombreDeFantasia"] = row["nombredefantasia"]
    dicc["colordisfraz"] = row["colordisfraz"]
    dicc["archienemigos"] = indicesDeMN(row["idsuperheroe"], "idsuperheroe", ESARCHIENEMIGO, "idcivil")
    dicc["habilidades"] = listaDeMN(row["idsuperheroe"],"idsuperheroe",HABILIDADSUPERHEROE, "idhabilidad",HABILIDAD, ["nombre"])
    dicc["incidentes"] = indicesDeMN(row["idsuperheroe"], "idsuperheroe", SUPERHEROEINCIDENTE, "idincidente")
    dicc["contactos"] = indicesDeMN(row["idsuperheroe"], "idsuperheroe", SUPERHEROECIVIL, "idcivil")
    puedeSerNull(dicc,"identidadSecreta",row["idcivil"])
    crear_documento(superheroeColl, str(row["idsuperheroe"]), dicc)



#SEGUIMIENTO
seguimientoColl = inicializarTabla("seguimiento")
seguimientosxIncidente = {}
for index, row in tqdm(SEGUIMIENTO.iterrows()):
    dicc = {}
    dicc["numero"] = row["numero"]
    dicc["descripcion"] = row["descripcion"]
    dicc["conclusion"] = row["conclusion"]
    dicc["estados"] = listaDeMN(row["numero"],"idseguimiento",ESTADO, "idestado",ESTADO, ["nombre","fechainicio","fechafin"])
    dicc["incidente"] = row["idincidente"]
    dicc["oficial"] = row["nroplaca"]
    seguimientosxIncidente[row["idincidente"]] = dicc
    crear_documento(seguimientoColl, str(row["numero"]), dicc)

#SUMARIO
sumarioColl = inicializarTabla("sumario")
sumariosXDesignacion = {}
for index, row in tqdm(SUMARIO.iterrows()):
    dicc = {}
    dicc["idsumario"] = row["idsumario"]
    dicc["descripcion"] = row["descripcion"]
    puedeSerNull(dicc,"resultado",row["resultado"])
    dicc["fecha"] = row["fecha"]
    dicc["estado"] = row["estado"]
    dicc["oficial"] = row["nroplaca"]
    dicc["designacion"] = row["iddesignacion"]
    if sumariosXDesignacion.get(row["iddesignacion"]):
        sumariosXDesignacion[row["iddesignacion"]] += [dicc]
    else:
        sumariosXDesignacion[row["iddesignacion"]] = [dicc]
    crear_documento(sumarioColl, str(row["idsumario"]), dicc)

#DESIGNACION
designacionColl = inicializarTabla("designacion")
designacionXNroPlaca = {}
for index, row in tqdm(DESIGNACION.iterrows()):
    dicc = {}
    dicc["iddesignacion"] = row["iddesignacion"]
    dicc["desde"] = row["desde"]
    dicc["hasta"] = row["hasta"]
    dicc["sumarios"] = sumariosXDesignacion.get(row["iddesignacion"])
    dicc["tipodesignacion"] = dame1aN(row["idtipodesignacion"], TIPODESIGNACION, ["nombre"])
    dicc["oficial"] = row["nroplaca"]
    if designacionXNroPlaca.get(row["nroplaca"]):
        designacionXNroPlaca[row["nroplaca"]] += [dicc]
    else:
        designacionXNroPlaca[row["nroplaca"]] = [dicc]
    crear_documento(designacionColl, str(row["iddesignacion"]), dicc)


#OFICIAL
oficialColl = inicializarTabla("oficial")
for index, row in tqdm(OFICIAL.iterrows()):
    dicc = {}
    dicc["nroplaca"] = row["nroplaca"]
    dicc["Nombre"] = row["nombre"]
    dicc["Apellido"] = row["apellido"]
    dicc["Rango"] = row["rango"]
    dicc["FechaIngreso"] = row["fechaingreso"]
    dicc["departamento"] = dame1aN(row["iddpto"], DEPARTAMENTO, ["nombre", "descripcion"])
    dicc["sumarios"] = indicesDeMN(row["nroplaca"], "nroplaca", SUMARIO, "idsumario")
    dicc["seguimientos"] = indicesDeMN(row["nroplaca"], "nroplaca", SEGUIMIENTO, "numero")
    dicc["incidentesInvolucradoEn"] = indicesDeMN(row["nroplaca"], "nroplaca", OFICIALINTERVIENEEN, "idincidente")
    dicc["incidentesInterviene"] = indicesDeMN(row["nroplaca"], "nroplaca", OFICIALESTAINVOLUCRADOEN, "idincidente")
    dicc["designaciones"] = designacionXNroPlaca.get(row["nroplaca"])
    #FALTAN LAS DESIGNACIONES
    crear_documento(oficialColl, str(row["nroplaca"]), dicc)

#DOMICILIO CON BARRIO
domicilios = {}
for index, row in tqdm(DOMICILIO.iterrows()):
    dicc = {}
    dicc["calle"] = row["calle"]
    dicc["altura"] = row["altura"]
    dicc["entrecalle1"] = row["entrecalle1"]
    dicc["entrecalle2"] = row["entrecalle2"]
    dicc["barrio"] = dame1aN(row["idbarrio"], BARRIO, ["nombre"])
    domicilios[row["iddomicilio"]] = dicc


#INCIDENTE
incidenteColl = inicializarTabla("incidente")
incidenteDicc = {}
for index, row in tqdm(INCIDENTE.iterrows()):
    dicc = {}
    dicc["idincidente"] = row["idincidente"]
    dicc["tipo"] = row["tipo"]
    dicc["fecha"] = row["fecha"]
    dicc["seguimiento"] = seguimientosxIncidente.get(row["idincidente"])
    dicc["oficialesInvolucradoEn"] = indicesDeMN(row["idincidente"], "idincidente", OFICIALINTERVIENEEN, "nroplaca")
    dicc["oficialesInterviene"] = indicesDeMN(row["idincidente"], "idincidente", OFICIALESTAINVOLUCRADOEN, "nroplaca")
    dicc["superheroesInvolucrados"] = indicesDeMN(row["idincidente"], "idincidente", SUPERHEROEINCIDENTE, "idsuperheroe")
    dicc["domicilio"] = domicilios[row["iddomicilio"]]

    incRol = INTERVIENE[INTERVIENE["idincidente"] == row["idincidente"]][["idcivil", "idrolcivil"]]
    incRol["rolcivil"] = [ROLCIVIL.iloc[x]["nombre"] for x in incRol["idrolcivil"].tolist()]

    dicc["civilesEnIncidente"] = incRol[["idcivil", "rolcivil"]].to_dict('records')

    crear_documento(incidenteColl, str(row["idincidente"]), dicc)
    incidenteDicc[str(row["idincidente"])] = dicc


#CIVIL
civilColl = inicializarTabla("civil")
for index, row in tqdm(CIVIL.iterrows()):
    dicc = {}
    dicc["idcivil"] = row["idcivil"]
    dicc["nombre"] = row["nombre"]

    domiciliosCivil = CIVILDOMICILIO[CIVILDOMICILIO["idcivil"] == row["idcivil"]].to_dict('records')
    listaDoms = []
    for dom in domiciliosCivil:
        domicilio = {}
        domicilio["calle"] = domicilios[dom["iddomicilio"]]["calle"]
        domicilio["altura"] = domicilios[dom["iddomicilio"]]["altura"]
        domicilio["entrecalle1"] = domicilios[dom["iddomicilio"]]["entrecalle1"]
        domicilio["entrecalle2"] = domicilios[dom["iddomicilio"]]["entrecalle2"]
        domicilio["fechadesde"] = dom["fechadesde"]
        domicilio["fechahasta"] = dom["fechahasta"]
        domicilio["barrio"] = domicilios[dom["iddomicilio"]]["barrio"]
        listaDoms.append(domicilio)
    dicc["domicilios"] = listaDoms
    dicc["contactosSuperheroe"] = indicesDeMN(row["idcivil"], "idcivil", SUPERHEROECIVIL, "idsuperheroe")
    idSuper = SUPERHEROE[SUPERHEROE["idcivil"] == row["idcivil"]]["idsuperheroe"].tolist()
    if len(idSuper) > 0: 
        dicc["esIdentidadSecretaDe"] = idSuper[0]
    else:
        dicc["esIdentidadSecretaDe"] = None

    incRol = INTERVIENE[INTERVIENE["idcivil"] == row["idcivil"]][["idincidente", "idrolcivil"]]
    incRol["rolcivil"] = [ROLCIVIL.iloc[x]["nombre"] for x in incRol["idrolcivil"].tolist()]

    dicc["incidentesCivil"] = incRol[["idincidente", "rolcivil"]].to_dict('records')
    puedeSerNull(dicc,"organizaciondelictiva",row["idorganizacion"])
    dicc["seRelacionaCon"]   = RELACIONCIVIL[RELACIONCIVIL["idcivil1"] == row["idcivil"]][["idcivil2", "fechadesde", "tipo"]].to_dict('records')
    dicc["esRelacionadoCon"] = RELACIONCIVIL[RELACIONCIVIL["idcivil2"] == row["idcivil"]][["idcivil1", "fechadesde", "tipo"]].to_dict('records')
    crear_documento(civilColl, str(row["idcivil"]), dicc)

#PERSONAINCIDENTE
personaIncidenteColl = inicializarTabla("personaIncidente")
personaIncidenteDicc = {}
for index, row in tqdm(INTERVIENE.iterrows()):
    dicc = {}
    dicc["idcivil"] = row["idcivil"]
    roles = INTERVIENE[INTERVIENE["idcivil"] == row["idcivil"]]["idrolcivil"].tolist()
    incidentes = [incidenteDicc[str(x)] for x in INTERVIENE[INTERVIENE["idcivil"] == row["idcivil"]]["idincidente"].tolist()]
    incs = []
    for rol, incidente in zip(roles, incidentes):
        inc = {}
        inc["rol"] = dame1aN(rol, ROLCIVIL, ["nombre"])
        inc["incidente"] = incidente
        incs.append(inc)
    dicc["incidentes"] = incs
    try:
        crear_documento(personaIncidenteColl, str(row["idcivil"]), dicc)
        personaIncidenteDicc[str(row["idcivil"])] = dicc
    except Exception:
        pass

#ORGANIZACIONDELICTIVA
organizaciondelictivaColl = inicializarTabla("organizaciondelictiva")
for index, row in tqdm(ORGANIZACIONDELICTIVA.iterrows()):
    dicc = {}
    dicc["idorganizaciondelictiva"] = row["idorganizaciondelictiva"]
    dicc["nombre"] = row["nombre"]
    dicc["civiles"] = indicesDeMN(row["idorganizaciondelictiva"], "idorganizacion", CIVIL, "idcivil")
    idc = []
    for c in dicc["civiles"]:
        if personaIncidenteDicc.get(str(c)):
            idc.append(personaIncidenteDicc[str(c)])
    dicc["incidentesDeCiviles"] = idc

    crear_documento(organizaciondelictivaColl, str(row["idorganizaciondelictiva"]), dicc)
