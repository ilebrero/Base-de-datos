-- Cuando dicen "buscar tal cosa dada cierta otra", buscamos por la clave primaria, ya que identifica únicamente a cada instancia
-- Es cierto que un usuario cualquiera no sabe los ids, pero como no está especificado quien hace estas consultas,
-- asumimos que son hechas por un sistema/página web, que sí conoce los IDs.


-- 1. Listado de incidentes en un rango de fechas, mostrando los datos de las personas y policías involucrados con el rol que jugó cada uno en el incidente
SELECT
	-- incidente
	i.idIncidente,
	i.tipo as TipoIncidente,
	i.fecha as FechaIncidente,
	i.idDomicilio as idDomicilioIncidente,
	-- oficial involucrado
	OficialInvolucrado.nroPlaca as nroPlacaOficialInvolucrado, 
	OficialInvolucrado.Nombre as nombreOficialInvolucrado,
	OficialInvolucrado.Apellido as apellidoOficialInvolucrado,
	OficialInvolucrado.Rango as rangoOficialInvolucrado,
	-- oficial que interviene
	OficialInterviene.nroPlaca as nroPlacaOficialInterviene, 
	OficialInterviene.Nombre as nombreOficialInterviene,
	OficialInterviene.Apellido as apellidoOficialInterviene,
	OficialInterviene.Rango as rangoOficialInterviene,
	-- civil
	Civil.idCivil,
	Civil.nombre as nombreCivil
FROM
	Incidente as i
JOIN
	OficialEstaInvolucradoEn ON OficialEstaInvolucradoEn.idIncidente = i.idIncidente
JOIN
	Oficial as OficialInvolucrado ON OficialEstaInvolucradoEn.nroPlaca = OficialInvolucrado.nroPlaca
JOIN
	OficialIntervieneEn ON OficialIntervieneEn.idIncidente = i.idIncidente
JOIN
	Oficial as OficialInterviene ON OficialIntervieneEn.nroPlaca = OficialInterviene.nroPlaca
JOIN
	Interviene as CivilInterviene ON CivilInterviene.idIncidente = i.idIncidente
JOIN
	Civil ON Civil.idCivil = CivilInterviene.idCivil
JOIN
	RolCivil ON CivilInterviene.idRolCivil = RolCivil.idRolCivil
WHERE
	i.Fecha BETWEEN '2013-01-03' AND '2013-01-09'
;

-- 2. Dada una organización delictiva, el detalle de incidentes en que participaron las personas que componen dicha organización
SELECT
	-- organizacion delictiva
	org.idOrganizacionDelictiva,
	org.nombre as NombreOrganizacionDelictiva,
	-- incidente
	Incidente.idIncidente,
	Incidente.tipo as tipoIncidente,
	Incidente.fecha as fechaIncidente
FROM
	OrganizacionDelictiva as org
JOIN
	Civil ON Civil.idOrganizacion = org.idOrganizacionDelictiva
JOIN
	Interviene as CivilInterviene ON Civil.idCivil = CivilInterviene.idCivil
JOIN
	Incidente ON Incidente.idIncidente = CivilInterviene.idIncidente
WHERE
	org.idOrganizacionDelictiva = 1
;

-- 3. La lista de todos los oficiales con sus rangos, de un departamento dado.
SELECT
	-- oficial
	Oficial.nroPlaca,
	Oficial.Nombre as NombreOficial,
	Oficial.Apellido as ApellidoOficial,
	Oficial.Rango as RangoOficial,

	-- depto
	Departamento.idDepartamento,
	Departamento.Nombre as NombreDepto
FROM
	Oficial
JOIN
	Departamento ON Departamento.idDepartamento = Oficial.idDpto
WHERE
	Departamento.idDepartamento = 1
;

-- 4. El ranking de oficiales que participaron en más incidentes
SELECT nroPlacaOficial, COUNT(*) as CantidadIncidentes
FROM 
	-- incidentes donde estuvo involucrado
	((SELECT
		OficialInvolucrado.nroPlaca as nroPlacaOficial, 
		i.idIncidente
	FROM
		Incidente as i
	JOIN
		OficialEstaInvolucradoEn ON OficialEstaInvolucradoEn.idIncidente = i.idIncidente
	JOIN
		Oficial as OficialInvolucrado ON OficialEstaInvolucradoEn.nroPlaca = OficialInvolucrado.nroPlaca)
	UNION ALL

	-- incidentes donde intervino
	(SELECT
		OficialQueInterviene.nroPlaca as nroPlacaOficial,
		i.idIncidente
	FROM
		Incidente as i
	JOIN
		OficialIntervieneEn ON OficialIntervieneEn.idIncidente = i.idIncidente
	JOIN
		Oficial as OficialQueInterviene ON OficialIntervieneEn.nroPlaca = OficialQueInterviene.nroPlaca)) as OficialIncidente
GROUP BY nroPlacaOficial
ORDER BY CantidadIncidentes DESC
;

-- 5. Los barrios con mayor cantidad de incidentes.
SELECT
	Barrio.idBarrio,
	Barrio.Nombre as NombreBarrio,
	COUNT(i.idIncidente) as CantidadIncidentes
FROM
	Incidente i
JOIN
	Domicilio ON Domicilio.idDomicilio = i.idDomicilio
JOIN
	Barrio ON Barrio.idBarrio = Domicilio.idBarrio
GROUP BY Barrio.idBarrio
ORDER BY CantidadIncidentes DESC
LIMIT 5
;

--6. Todos los oficiales sumariados que participaron de algún incidente.
SELECT
	Oficial.nroPlaca,
	Oficial.nombre as NombreOficial,
	Oficial.Apellido as ApellidoOficial
FROM
	Oficial
JOIN
	Sumario ON Sumario.nroPlaca = Oficial.nroPlaca
JOIN
	OficialEstaInvolucradoEn ON OficialEstaInvolucradoEn.nroPlaca = Oficial.nroPlaca
JOIN
	OficialIntervieneEn ON OficialIntervieneEn.nroPlaca = Oficial.nroPlaca
;

--7. Las personas involucradas en incidentes ocurridos en el barrio donde viven
SELECT
	Civil.idCivil,
	Civil.Nombre as nombreCivil
FROM
	Civil
JOIN
	Interviene ON Interviene.idCivil = Civil.idCivil
JOIN
	Incidente ON Incidente.idIncidente = Interviene.idIncidente
JOIN
	Domicilio as DomicilioIncidente ON Incidente.idDomicilio = DomicilioIncidente.idDomicilio
JOIN
	CivilDomicilio as ResideEn ON ResideEn.idCivil = Civil.idCivil
JOIN
	Domicilio as DomicilioCivil ON DomicilioCivil.idDomicilio = ResideEn.idDomicilio
WHERE
	DomicilioCivil.idBarrio = DomicilioIncidente.idBarrio
;

--8. Los superheroes que tienen una habilidad determinada
SELECT
	Superheroe.idSuperheroe,
	Superheroe.nombreDeFantasia
FROM
	Superheroe
JOIN
	HabilidadSuperheroe ON HabilidadSuperheroe.idSuperheroe = Superheroe.idSuperheroe
JOIN
	Habilidad ON Habilidad.idHabilidad = HabilidadSuperheroe.idHabilidad
WHERE
	Habilidad.idHabilidad = 3
;

--9. Los superheroes que han participado en algún incidente.
SELECT
	Superheroe.idSuperheroe,
	Superheroe.nombreDeFantasia
FROM
	Superheroe
JOIN
	SuperheroeIncidente ON SuperheroeIncidente.idSuperheroe = Superheroe.idSuperheroe
JOIN
	Incidente ON Incidente.idIncidente = SuperheroeIncidente.idIncidente
;

--10. Listado de todos los incidentes en donde estuvieron involucrados superheroes y
--    fueron causados por los "archienemigos" de los superheroes involucrados.
SELECT
	Superheroe.idSuperheroe,
	Superheroe.nombreDeFantasia
FROM
	Superheroe
JOIN
	SuperheroeIncidente ON SuperheroeIncidente.idSuperheroe = Superheroe.idSuperheroe
JOIN
	EsArchienemigo ON EsArchienemigo.idSuperheroe = Superheroe.idSuperheroe
JOIN
	Interviene as SupervillanoInterviene ON SupervillanoInterviene.idCivil = EsArchienemigo.idCivil
JOIN
	RolCivil ON RolCivil.idRolCivil = SupervillanoInterviene.idRolCivil
WHERE
	SupervillanoInterviene.idIncidente = SuperheroeIncidente.idIncidente AND
	RolCivil.nombre = 'PERPETRADOR'
;


