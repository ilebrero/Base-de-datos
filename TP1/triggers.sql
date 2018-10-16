-- ##########################################################################
-- # Los oficiales que llevan adelante los sumarios son de asuntos internos #
-- ##########################################################################

DROP TRIGGER  IF EXISTS sumariosSoloDeAsuntosInternos on Sumario;
DROP FUNCTION IF EXISTS check_asuntos_internos();
    
CREATE FUNCTION check_asuntos_internos() RETURNS trigger AS $check_asuntos_internos$
    DECLARE
        check_asuntos_internos integer;

    BEGIN
        SELECT count(idDesignacion) INTO check_asuntos_internos 
        FROM Designacion d, TipoDesignacion td 
        WHERE d.nroPlaca = NEW.nroPlaca
            AND td.idTipoDesignacion = d.idTipoDesignacion
            AND td.nombre = 'ASUNTOS INTERNOS';
            
        IF check_asuntos_internos = 0 THEN
            RAISE EXCEPTION 'El oficial % no tiene una designacion en asuntos internos.', NEW.nroPlaca;
        END IF;

        RETURN NEW;
    END;
$check_asuntos_internos$ LANGUAGE plpgsql;

-- Asumo que se cambio al menos una row
CREATE TRIGGER sumariosSoloDeAsuntosInternos
    BEFORE INSERT OR UPDATE of nroPlaca on Sumario
    FOR EACH ROW
    EXECUTE PROCEDURE check_asuntos_internos();

-- #######################################################
-- # Un oficial no puede llevar a cabo su propio sumario #
-- #######################################################

DROP TRIGGER  IF EXISTS sumariosSoloDeOtros on Sumario;
DROP FUNCTION IF EXISTS check_sumario_de_otro();
    
CREATE FUNCTION check_sumario_de_otro() RETURNS trigger AS $check_sumario_de_otro$
    DECLARE
        check_sumario_de_otro integer;

    BEGIN
        SELECT count(nombre) INTO check_sumario_de_otro
        FROM Designacion d, Oficial o
        WHERE d.nroPlaca = NEW.nroPlaca
            AND d.idDesignacion = NEW.idDesignacion;

        BEGIN
            IF check_sumario_de_otro > 0 THEN
                RAISE EXCEPTION 'El oficial % no puede llevar adelante un sumario de si mismo.', NEW.nroPlaca;
            END IF;
        END;

        RETURN NEW;
    END;
$check_sumario_de_otro$ LANGUAGE plpgsql;

-- Asumo que se cambio al menos una row
CREATE TRIGGER sumariosSoloDeOtros
    BEFORE INSERT OR UPDATE on Sumario
    FOR EACH ROW
    EXECUTE PROCEDURE check_sumario_de_otro();

-- ################################################
-- # Un civil no puede relacionarce consigo mismo #
-- ################################################

DROP TRIGGER  IF EXISTS relacionesSoloConOtrosCiviles on RelacionCivil;
DROP FUNCTION IF EXISTS check_relaciones_reflexivas();
    
CREATE FUNCTION check_relaciones_reflexivas() RETURNS trigger AS $check_relaciones_reflexivas$
    BEGIN
        -- ver si esto anda
        IF NEW.idCivil1 = NEW.idCivil2 THEN
            RAISE EXCEPTION 'El civil % no puede relacionarce consigo mismo', NEW.idCivil1;
        END IF;

    RETURN NEW;
    END;
$check_relaciones_reflexivas$ LANGUAGE plpgsql;

-- Asumo que se cambio al menos una row
CREATE TRIGGER relacionesSoloConOtrosCiviles
    BEFORE INSERT OR UPDATE on RelacionCivil
    FOR EACH ROW
    EXECUTE PROCEDURE check_relaciones_reflexivas();

-- ##############################################
-- # Un superheroe no puede ser un supervillano #
-- ##############################################

DROP TRIGGER  IF EXISTS superheroesNoSonSupervillanos on Superheroe;
DROP FUNCTION IF EXISTS check_superheroe_supervillano_distintos();
    
CREATE FUNCTION check_superheroe_supervillano_distintos() RETURNS trigger AS $check_superheroe_supervillano_distintos$
    DECLARE
        supervillanos integer;

    BEGIN
        IF NEW.idCivil IS NOT NULL THEN

            BEGIN
                SELECT count(*) INTO supervillanos
                FROM supervillano s
                WHERE s.idCivil = NEW.idCivil;
                
                IF supervillanos > 0 THEN
                    RAISE EXCEPTION 'El civil(%) no puede ser superheroe y supervillano al mismo tiempo.', NEW.idCivil;
                END IF;
            END;

        END IF;
    
    RETURN NEW;
    END

$check_superheroe_supervillano_distintos$ LANGUAGE plpgsql;

-- Asumo que se cambio al menos una row
CREATE TRIGGER superheroesNoSonSupervillanos
    BEFORE INSERT OR UPDATE on Superheroe
    FOR EACH ROW
    EXECUTE PROCEDURE check_superheroe_supervillano_distintos();

-- #################################################
-- # Un superheroe no puede ser su propio contacto #
-- #################################################

DROP TRIGGER  IF EXISTS superheroeNoEsSuPropioContacto on SuperheroeCivil CASCADE;
DROP FUNCTION IF EXISTS check_superheroe_no_es_propio_contacto() CASCADE;

CREATE FUNCTION check_superheroe_no_es_propio_contacto() RETURNS trigger AS $check_superheroe_no_es_propio_contacto$
    DECLARE
        superHeroeIdentidadSecreta integer;

    BEGIN
        SELECT idCivil INTO superHeroeIdentidadSecreta
        FROM Superheroe s
        WHERE s.idSuperheroe = NEW.idSuperheroe;

        IF superHeroeIdentidadSecreta IS NOT NULL THEN
            BEGIN
                BEGIN
                    IF superHeroeIdentidadSecreta = NEW.idCivil THEN
                        RAISE EXCEPTION 'El civil(%) no puede ser un superheroe y su propio contacto a la vez.', NEW.idCivil;
                    END IF;
                END;
            END;
        END IF;

        RETURN NEW;
    END;
$check_superheroe_no_es_propio_contacto$ LANGUAGE plpgsql;

CREATE TRIGGER superheroeNoEsSuPropioContacto
    BEFORE INSERT OR UPDATE on SuperheroeCivil
    FOR EACH ROW
    EXECUTE PROCEDURE check_superheroe_no_es_propio_contacto();

-- ##################################################################
-- # Un superheroe no puede pertenecer a una organizacion delictiva #
-- ##################################################################

DROP TRIGGER  IF EXISTS superheroeNoPerteneceAOrganizacionDelictiva on Civil;
DROP FUNCTION IF EXISTS check_superheroe_no_esta_en_organizacion_delictiva();

CREATE FUNCTION check_superheroe_no_esta_en_organizacion_delictiva() RETURNS trigger AS $check_superheroe_no_esta_en_organizacion_delictiva$
    DECLARE
        superHeroeIdentidadSecreta integer;

    BEGIN
        SELECT idSuperheroe INTO superHeroeIdentidadSecreta
        FROM Superheroe s
        WHERE s.idCivil = NEW.idCivil;

        IF superHeroeIdentidadSecreta IS NOT NULL THEN
            BEGIN
                BEGIN
                    IF NEW.idOrganizacion IS NOT NULL THEN
                        RAISE EXCEPTION 'El civil(%) no puede ser un superheroe y pertenecer a una organizacion delictiva a la vez.', NEW.idCivil;
                    END IF;
                END;
            END;
        END IF;

        RETURN NEW;
    END;
$check_superheroe_no_esta_en_organizacion_delictiva$ LANGUAGE plpgsql;

CREATE TRIGGER superheroeNoPerteneceAOrganizacionDelictiva
    BEFORE INSERT OR UPDATE of idOrganizacion on Civil
    FOR EACH ROW
    EXECUTE PROCEDURE check_superheroe_no_es_propio_contacto();



-- #############################################################################
-- # Un seguimiento no puede tener conclusion si no tiene un estado finalizado #
-- #############################################################################

DROP TRIGGER  IF EXISTS noPuedeHaberSeguimientoConConclusionSinEstadoFinalizado on Seguimiento;
DROP FUNCTION IF EXISTS check_seguimiento_con_estado_finalizado_y_conclusion();

CREATE FUNCTION check_seguimiento_con_estado_finalizado_y_conclusion() RETURNS trigger AS $check_seguimiento_con_estado_finalizado_y_conclusion$
    DECLARE
        estadoFinalizado integer;

    BEGIN
        IF NEW.conclusion IS NOT NULL THEN
            SELECT count(*) INTO estadoFinalizado
            FROM Estado e
            WHERE e.numero = NEW.numero
                AND e.Nombre = 'FINALIZADO';

            BEGIN
                IF estadoFinalizado = 0 THEN
                    RAISE EXCEPTION 'El seguimiento(%) no puede tener conclusion, todavia no esta finalizado.', NEW.numero;
                END IF;
            END;
        END IF;

        RETURN NEW;
    END;
$check_seguimiento_con_estado_finalizado_y_conclusion$ LANGUAGE plpgsql;

CREATE TRIGGER noPuedeHaberSeguimientoConConclusionSinEstadoFinalizado
    BEFORE INSERT OR UPDATE on Seguimiento
    FOR EACH ROW
    EXECUTE PROCEDURE check_seguimiento_con_estado_finalizado_y_conclusion();

-- #############################################################
-- # Un Sumario no puede tener resultado si no esta finalizado #
-- #############################################################

DROP TRIGGER  IF EXISTS noPuedeHaberSumarioConresultadoSinEstadoFinalizado on Sumario;
DROP FUNCTION IF EXISTS check_sumario_con_estado_no_finalizado_y_resultado();

CREATE FUNCTION check_sumario_con_estado_no_finalizado_y_resultado() RETURNS trigger AS $check_sumario_con_estado_no_finalizado_y_resultado$
    DECLARE
        estadoFinalizado integer;

    BEGIN
        IF NEW.resultado IS NOT NULL THEN
            IF NEW.estado <> 'FINALIZADO' THEN
                RAISE EXCEPTION 'El sumario(%) no puede tener resultado, todavia no esta finalizado.', NEW.idSumario;
            END IF;
        END IF;

        RETURN NEW;
    END;
$check_sumario_con_estado_no_finalizado_y_resultado$ LANGUAGE plpgsql;

CREATE TRIGGER noPuedeHaberSumarioConresultadoSinEstadoFinalizado
    BEFORE INSERT OR UPDATE of resultado on Sumario
    FOR EACH ROW
    EXECUTE PROCEDURE check_sumario_con_estado_no_finalizado_y_resultado();