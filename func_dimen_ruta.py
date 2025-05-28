import math

# DIMENSIONAMIENTO DE RUTA BASICA

#1. HORARIO DE MAXIMA DEMANDA

import math

# ======================
# Excepciones personalizadas
# ======================

class DimensionamientoError(Exception):
    """Error general en el módulo de dimensionamiento de buses."""
    pass


# ======================
# Funciones de cálculo
# ======================


def calcular_velocidad_operacion(longitud_ruta_km, tiempo_recorrido_min):
    if tiempo_recorrido_min <= 0:
        raise DimensionamientoError("El tiempo de recorrido debe ser mayor que cero.")
    return longitud_ruta_km / (tiempo_recorrido_min / 60)

def calcular_intervalo_despacho(capacidad_total, usuarios_hmd, factor_ocupacion):
    if usuarios_hmd <= 0:
        raise DimensionamientoError("La demanda de usuarios en la hora de máxima demanda debe ser mayor que cero.")
    if capacidad_total <= 0:
        raise DimensionamientoError("La capacidad total del vehículo debe ser mayor que cero.")
    if not (0 < factor_ocupacion <= 1):
        raise DimensionamientoError("El factor de ocupación debe estar entre 0 y 1.")
    i = (60 * factor_ocupacion * capacidad_total) / usuarios_hmd
    return math.floor(i / 0.5) * 0.5

def calcular_tiempo_ciclo(tiempo_recorrido_min, tiempo_terminal):
    if tiempo_recorrido_min < 0 or tiempo_terminal < 0:
        raise DimensionamientoError("El tiempo de recorrido y el tiempo en terminal deben ser no negativos.")
    return 2 * (tiempo_recorrido_min + tiempo_terminal)

def calcular_numero_vehiculos(tiempo_ciclo, intervalo):
    if intervalo <= 0:
        raise DimensionamientoError("El intervalo debe ser mayor que cero.")
    return math.ceil(tiempo_ciclo / intervalo)

def calcular_tiempo_ciclo_corregido(N, intervalo):
    if N <= 0 or intervalo <= 0:
        raise DimensionamientoError("El número de vehículos y el intervalo deben ser mayores que cero.")
    return N * intervalo

def calcular_vehiculos_reserva(N, porcentaje=0.10):
    if N < 0:
        raise DimensionamientoError("El número de vehículos no puede ser negativo.")
    if not (0 <= porcentaje <= 1):
        raise DimensionamientoError("El porcentaje debe estar entre 0 y 1.")
    return math.ceil(N * porcentaje)

def calcular_tiempo_terminal_corregido(tiempo_ciclo_corregido, tiempo_recorrido_min):
    if tiempo_ciclo_corregido < 0 or tiempo_recorrido_min < 0:
        raise DimensionamientoError("Los tiempos no pueden ser negativos.")
    return (tiempo_ciclo_corregido - (2 * tiempo_recorrido_min)) / 2

def calcular_velocidad_comercial(longitud_ruta_km, tiempo_ciclo_corregido):
    if tiempo_ciclo_corregido <= 0:
        raise DimensionamientoError("El tiempo de ciclo corregido debe ser mayor que cero.")
    return (120 * longitud_ruta_km) / tiempo_ciclo_corregido

def calcular_eficiencia_sistema(velocidad_comercial, N):
    if N <= 0:
        raise DimensionamientoError("El número de vehículos debe ser mayor que cero.")
    return velocidad_comercial / N

def calcular_frecuencia_paso(intervalo):
    if intervalo <= 0:
        raise DimensionamientoError("El intervalo debe ser mayor que cero.")
    return 60 / intervalo

def calcular_capacidad_linea(frecuencia_paso, capacidad_total):
    if frecuencia_paso <= 0 or capacidad_total <= 0:
        raise DimensionamientoError("La frecuencia de paso y la capacidad total deben ser mayores que cero.")
    return frecuencia_paso * capacidad_total

def calcular_capacidad_linea_con_factor(capacidad_linea, factor_ocupacion):
    if not (0 < factor_ocupacion <= 1):
        raise DimensionamientoError("El factor de ocupación debe estar entre 0 y 1.")
    return capacidad_linea * factor_ocupacion

def calcular_itinerario_despacho(hora_inicio, hora_fin, intervalo):
    if not (0 <= hora_inicio < 24) or not (0 <= hora_fin <= 24) or hora_inicio >= hora_fin:
        raise DimensionamientoError("El horario debe estar en el rango de 0 a 24 y la hora de inicio debe ser menor a la hora de fin.")
    if intervalo <= 0:
        raise DimensionamientoError("El intervalo debe ser mayor que cero.")

    itinerario = []
    minutos_actuales = hora_inicio * 60
    minutos_fin = hora_fin * 60
    while minutos_actuales < minutos_fin:
        hora = int(minutos_actuales) // 60
        minuto = int(minutos_actuales) % 60
        segundos = int(round((minutos_actuales - int(minutos_actuales)) * 60))
        itinerario.append(f"{hora:02d}:{minuto:02d}:{segundos:02d}")
        minutos_actuales += intervalo
    return itinerario
