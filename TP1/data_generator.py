from data import FACTURAS, DESCUENTOS, EVENTOS_PARQUES, TARJETAS, NROS_TELEFONO, TITULARES, CATEGORIAS, PROVINCIA_O_ESTADO_PAIS, MEDIOS_DE_PAGO, DIAS, PRECIOS, CALLES, PARQUES, PARQUES_NOMBRES, EMPRESAS, EMPRESAS_NOMBRES
from data import CATEGORIAS_NOMBRES, MEDIOS_DE_PAGO_NOMBRES, DIAS_NOMBRES, PROVINCIA_O_ESTADO_PAIS_NOMBRES, EVENTOS, EVENTOS_NOMBRES, ATRACCIONES, ATRACCIONES_NOMBRES
from data import FECHA_LIMITE, TITULARES_NOMBRES, TITULARES_APELLIDOS, CATEGORIAS_MINIMO_INGRESO, CATEGORIAS_PROMEDIO_PARA_MANTENER, CANTIDAD_CONSUMOS, TODOS_CONSUMIBLES

from data import ID_CONSUMO, ID_CONSUMIBLE, FECHA_CONSUMO, COSTO_CONSUMO, ID_FACTURA_FACTURA, IMPORTE_FACTURA, FECHA_VENCIMIENTO_FACTURA, FECHA_FACTURA, IDS_CONSUMOS_FACTURA

from random import choice, randrange
from itertools import chain

from datetime import date, timedelta
import datetime, sys, os



# redirige output al archivo txt
sys.stdout = open(os.getcwd() + "/data_generating_queries_res.txt", "w")

###############################################################
######################### Globals #############################
###############################################################

id_price     = 0
id_consumo   = 0
id_factura   = 0
id_atraccion = 26 
id_factura_pagada  = 0
id_factura_consumo = 0

# categoria -> consumible -> descuento
consumibles_descuentos = {
 CATEGORIAS[0] : {},
 CATEGORIAS[1] : {},
 CATEGORIAS[2] : {},
 CATEGORIAS[3] : {},
 CATEGORIAS[4] : {}
}

# precios -> { dia -> (idConsumible, precio) }
consumibles_prices = {
  DIAS[0] : {},
  DIAS[1] : {}, 
  DIAS[2] : {}, 
  DIAS[3] : {}, 
  DIAS[4] : {}, 
  DIAS[5] : {}, 
  DIAS[6] : {}
}

#Que parques se relacionan con que atracciones
consumos       = {}
factuas_data   = {}
consumos_data  = {}
titulares_data = {}
empresas_cuits = {}
tarjetas_categorias = {}
parques_atracciones = {}

# id_titular -> [(id_factura, importe, vencimiento)]
facturas = {}

##############################################################################
####################### Helpers for generating content #######################
##############################################################################

def generate_date_time(fecha, hora):
    return str(fecha[0]) + "-" + str(fecha[1]) + "-" + str(fecha[2]) + " " + str(hora[0]) + ":" + str(hora[1]) + ":" + str(hora[2])

def get_day_id(f):
    return int( date(f[0], f[1], f[2]).weekday() )

def get_cost_with_discount(id_consumible, id_tarjeta, fecha):
    global consumibles_descuentos

    costo     = consumibles_prices[ get_day_id(fecha) ][id_consumible]
    categoria = tarjetas_categorias[id_tarjeta]

    if id_consumible in consumibles_descuentos[categoria]:
        descuento = consumibles_descuentos[categoria][id_consumible]
        costo = int( costo * ( descuento / float(100)))

    return costo

def add_consumo(id_consumo, id_tarjeta, id_consumible, fecha, costo):
    global consumos
 
    entrada = (id_consumo, id_consumible, fecha, costo)

    if id_tarjeta in consumos:
        consumos[id_tarjeta].append( entrada  )
    else: 
        consumos[id_tarjeta] = [ entrada ] 
  
    

def generate_consumption(id_consumible, id_tarjeta, fecha, hora):
    global id_consumo
    global consumibles_prices
    global consumibles_descuentos
    global consumos

    costo = get_cost_with_discount(id_consumible, id_tarjeta, fecha)

    print( insert_query("consumo",  (id_consumo,
                                     generate_date_time(fecha, hora),
                                     costo,
                                     id_tarjeta,
                                     id_consumible)))
    
    add_consumo(id_consumo, id_tarjeta, id_consumible, fecha, costo)
    id_consumo += 1
    

def add_atraction(id_parque, id_atraccion):
    global parques_atracciones

    if id_parque in parques_atracciones:
        parques_atracciones[id_parque].append(id_atraccion)
    else:
        parques_atracciones[id_parque] = [id_atraccion]	

def append_string_array(arr):
    return str(arr[0]) + "-" + str(arr[1]) + "-" + str(arr[2])

def generate_cuit(id_empresa):
    return int( str(choice([20, 27, 30])) + str(id_empresa) + str(randrange(0, 9)) )

def generate_address():
    return choice(CALLES) + " " + str(randrange(1, 3000))

def generate_phone_number():
    return "+" + str( choice(range(54)) ) + "-" + str( choice(range(10)) ) + "-011-" + str( choice(range(9999)) ) + "-" + str( choice(range(9999)) )

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

def generate_price(id_consumible):
   global id_price
   global consumibles_prices

   for id_dia in DIAS:
      price = choice( PRECIOS )

      print( insert_query( "precio",
                          ( id_price,
                            price,
                            id_dia,
                            id_consumible
                          )
                        ) 
      )

      # Guardo precio relacionado a consumible y dia para usar despues en los consumor / facturas  
      consumibles_prices [id_dia] [id_consumible] = price
      id_price += 1

def insert_query(table_name, values):
    if type(values) is not tuple:
        if type(values) is str:
            return "INSERT INTO " + table_name + " VALUES (\"" + str(values) + "\");"
        else:
            return "INSERT INTO " + table_name + " VALUES (" + str(values) + ");"
    elif len(values):
        return "INSERT INTO " + table_name + " VALUES " + str(values) + ";"

# Es el mismo id
def get_tarjeta_of_titular(id_titular):
   return id_titular

def get_sum_and_id_of_consumptions(id_titular, fecha_begin, fecha_end):
    global consumos
    
    id_tarjeta = get_tarjeta_of_titular(id_titular)
    consumo_total = 0
    ids_consumos = []

    for entrada in consumos[id_tarjeta]:
        fecha = entrada[FECHA_CONSUMO]
        fecha_consumo = date(fecha[0], fecha[1], fecha[2])

        if fecha_begin <= fecha_consumo <= fecha_end:
            consumo_total += entrada[COSTO_CONSUMO]
            ids_consumos.append( entrada[ID_CONSUMO]  )

    return (consumo_total, ids_consumos)

def add_factura(id_titular, id_factura, importe, fecha_vencimiento, fecha, ids_consumos):
    global facturas
    entrada = (id_factura, importe, fecha_vencimiento.isoformat(), fecha.isoformat(), ids_consumos)

    if id_titular in facturas:
        facturas[id_titular].append(entrada)
    else:
        facturas[id_titular] = [entrada]

def generate_factura_consumo(id_factura, ids_consumos):
    global id_factura_consumo

    for id_consumo in ids_consumos:
        print( insert_query("factura_consumo", (id_factura_consumo,
                                                id_factura,
                                                id_consumo)))
        id_factura_consumo += 1


def generate_factura(id_titular, fecha, fecha_vencimiento):
    global id_factura

    (importe, ids_consumos) = get_sum_and_id_of_consumptions(id_titular, fecha_date, fecha_vencimiento)

    if importe > 0:
        print(insert_query("factura", (id_factura,
                                       fecha.isoformat(),
                                       fecha_vencimiento.isoformat(),
                                       importe,
                                       id_titular
                                       )))

        generate_factura_consumo(id_factura, ids_consumos)
        add_factura(id_titular, id_factura, importe, fecha_vencimiento, fecha, ids_consumos)

        id_factura += 1

##################################################################
####################### Content generation #######################
##################################################################

##################
# medios de pago #
##################

for i in MEDIOS_DE_PAGO:
    ep = MEDIOS_DE_PAGO_NOMBRES[i]

    print(insert_query("medioDePago",
                      (i,
                        ep)))

########################
# provincias o estados #
########################

for i in PROVINCIA_O_ESTADO_PAIS:
    ep = PROVINCIA_O_ESTADO_PAIS_NOMBRES[i]

    print(insert_query("provinciaOEstado",
                       (i,
                        ep[0])))

########
# dias #
########

for i in DIAS:
    dia_nombre = DIAS_NOMBRES[i]
    print( insert_query( "dia",
                       ( i,
                        dia_nombre)))

##############
# categorias #
##############

for i in CATEGORIAS:
  categoria_nombre = CATEGORIAS_NOMBRES[i]
  print( insert_query( "categoria",
                     ( i,
                        categoria_nombre,
                        CATEGORIAS_MINIMO_INGRESO[i],
                        CATEGORIAS_PROMEDIO_PARA_MANTENER[i])))


############
# empresas #
############

for i in EMPRESAS:
    global empresas_cuit

    ep_id = choice(PROVINCIA_O_ESTADO_PAIS)
    cuit = generate_cuit(i)

    print(insert_query("empresaOrganizadora",
                       (cuit,
                        EMPRESAS_NOMBRES[i - 1],
                        generate_address(),
                        PROVINCIA_O_ESTADO_PAIS_NOMBRES[ep_id][1],
                        ep_id)))

    empresas_cuits[i] = cuit

###########
# parques #
###########

for i in PARQUES:
    generate_consumible(i)

    print(insert_query("parque", (i,
                                   choice(PARQUES_NOMBRES),
                                   generate_address())))

    generate_price(i)

###########
# eventos #
###########

for i in EVENTOS:
    global empresas_cuits
    generate_consumible(i)

    empresa_cuit = empresas_cuits[ choice(EMPRESAS)  ]
    fecha_inicio = generate_date("2015-01-01", "2018-05-18")
    fecha_fin    = generate_date(append_string_array(fecha_inicio), "2018-05-19")

    print(insert_query("evento", (i,
                                 choice(EVENTOS_NOMBRES),
                                 datetime.date(fecha_inicio[0], fecha_inicio[1], fecha_inicio[2]).isoformat(),
                                 datetime.date(fecha_fin[0], fecha_fin[1], fecha_fin[2]).isoformat(),
                                 generate_address(),
                                 empresa_cuit)))

    generate_price(i)

###############
# atracciones #
###############

# Cada parque tiene al menos una atraccion
for id_parque in PARQUES:
    global id_atraccion

    generate_consumible(id_atraccion)
    
    print(insert_query("atraccion", (id_atraccion,
                                     ATRACCIONES_NOMBRES[id_atraccion - 25],
                                     randrange(20,100),
                                     randrange(4, 18),
                                     randrange(40, 99),
                                     id_parque)))

    add_atraction(id_parque, id_atraccion)
    generate_price(id_atraccion)

    id_atraccion += 1

for i in range( len(PARQUES), len(ATRACCIONES) ):
    global id_atraccion

    generate_consumible(id_atraccion)

    id_parque = choice( PARQUES ) 
    print(insert_query("atraccion", (id_atraccion, 
                                    ATRACCIONES_NOMBRES[id_atraccion - 25], 
                                    randrange(20, 100), 
                                    randrange(4, 18), 
                                    randrange(40, 99), 
                                    id_parque)))

    add_atraction(id_parque, id_atraccion)
    generate_price(id_atraccion)

    id_atraccion += 1

#############
# titulares #
#############

for i in TITULARES:
    nombre   = choice(TITULARES_NOMBRES)
    apellido = choice(TITULARES_APELLIDOS)
    titulares_data[i] = (nombre, apellido)

    print( insert_query("titular", (i,
                        	   generate_address(),
                        	   nombre,
                        	   apellido,
                        	   choice(MEDIOS_DE_PAGO))))
####################
# nros de telefono #
####################

for i in NROS_TELEFONO:
    print( insert_query("nroTelefono", (i,
                                      generate_phone_number(),
                                      choice(TITULARES))))
############
# Tarjetas #
############

#Activas para Titulares
for i in TITULARES:
    print( insert_query( "tarjeta", (i,
				     '\\000',
				     't',   
				     i)))

# Inactivas random
for i in range(len(TITULARES), len(TARJETAS)):
   print( insert_query( "tarjeta", (i,
				   '\\000', #Foto default
				    'f',
				    choice( TITULARES ))))
#####################
# tarjeta categoria #
#####################

# Por ahora solamente van con una categoria, cuando se generen los datos se van a acomodar con el trigger que actualiza las categorias
for i in TARJETAS:
    global tarjetas_categoria

    categoria = choice( CATEGORIAS )

    print( insert_query( "tarjeta_categoria", (i,
                                               categoria,
					       append_string_array(generate_date("2015-01-01", "2018-05-19")))))

    tarjetas_categorias[i] = categoria

##############
# descuentos #
##############

for i in DESCUENTOS:
    global consumibles_descuentos

    id_categoria  = choice( CATEGORIAS )
    id_consumible = choice( TODOS_CONSUMIBLES )
    descuento     = choice( range(1, 99) )

    print( insert_query( "descuento", (i,
                                       descuento,
                                       id_categoria,
                                       id_consumible)))

    consumibles_descuentos[id_categoria][id_consumible] = descuento

############
# Consumos #
############

for i in TARJETAS:
    global parques_atracciones

    #A cada tarjeta le damos un random de consumos
    for consumo in range(CANTIDAD_CONSUMOS):
        id_consumible = choice( EVENTOS_PARQUES )
        fecha = generate_date("2018-03-01", FECHA_LIMITE)
        hora  = generate_time("00:00:00", "11:59:59") 
        
        #Si es evento, lo agregamos
        if id_consumible in EVENTOS:
            generate_consumption(id_consumible, i, fecha, hora)
        else:
	    #Si es parque, agregamos la entrada y algunas atracciones ese dia
            generate_consumption(id_consumible, i, fecha, hora)

            atracciones = parques_atracciones[id_consumible]
            cantidad_visitadas = choice( range(len(atracciones))  )

            for j in range(cantidad_visitadas):
                        #Puede repetir atracciones
                        atraccion_visitada = choice(atracciones)

                        hora_atraccion = generate_time("12:00:00", "23:59:59")
                        generate_consumption(atraccion_visitada, i, fecha, hora_atraccion)

###########
# factuas #
###########

# genero las facturas de los ultimos 2 meses
# Todas las facturas se emiten en la ultima semana del mes y tienen 30 dias para pagarse
# Se generan todas las facturas de todos los titulares en los ultimos dos meses
for id_titular in TITULARES:
    global facturas    
    
    fecha = FECHA_LIMITE.split("-")

    #Primer mes
    fecha_vencimiento = date( int(fecha[0]), int(fecha[1]), int(fecha[2]) )

    #Fix para levantar los dias adentro de 2018
    fecha_vencimiento = fecha_vencimiento - timedelta(days=365)

    fecha_date = fecha_vencimiento - timedelta(days=30)
    generate_factura(id_titular, fecha_date, fecha_vencimiento)

    #Segundo mes
    fecha_vencimiento = fecha_date
    fecha_date = fecha_vencimiento - timedelta(days=30)
    generate_factura(id_titular, fecha_date, fecha_vencimiento)

####################
# facturas pagadas #
####################

#La mitad de las facturas van a estar pagadas
for id_titular in TITULARES:
    global facturas
    global id_factura_pagada

    factura_data = facturas[id_titular][0]

    fecha_pago = generate_date( factura_data[FECHA_FACTURA], factura_data[FECHA_VENCIMIENTO_FACTURA] )
    id_factura = factura_data[ID_FACTURA_FACTURA]
    
    print( insert_query("facturapagada", (id_factura_pagada,
                                          append_string_array(fecha_pago),
                                          id_factura)))

    id_factura_pagada += 1
    
    
