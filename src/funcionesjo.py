from datetime import datetime, timedelta


def hoy(formato="%Y-%m-%d", inicio_de_mes=False) -> str:
    if inicio_de_mes and "%d" in formato:
        formato = formato.replace("%d", "01")
    return datetime.today().strftime(formato)

def day_after(fecha: str, formato='%Y-%m-%d') -> str:
    fecha_datetime = datetime.strptime(fecha, formato)
    fecha_mas_un_dia = fecha_datetime + timedelta(days=1)
    fecha_texto = fecha_mas_un_dia.strftime(formato)
    return fecha_texto

def year_ago(fecha: str, formato='%Y-%m-%d', inicio_de_mes=False, inicio_de_anio=False) -> str:
    if "-" in fecha:
        separador = "-"
    elif "/" in fecha:
        separador = "/"
    formato = formato.replace('%', '').split(separador)
    fecha = fecha.split(separador)
    pos_Y = formato.index('Y')
    fecha[pos_Y] = str(int(fecha[pos_Y]) - 1)
    if inicio_de_mes:
        pos_d = formato.index('d')
        fecha[pos_d] = "01"
    elif inicio_de_anio:
        pos_d = formato.index('d')
        pos_m = formato.index('m')
        fecha[pos_d] = "01"
        fecha[pos_m] = "01"
    return f"{separador}".join(fecha)

def month_after(fecha: str, formato='%Y-%m-%d') -> str:
    if "-" in fecha:
        separador = "-"
    elif "/" in fecha:
        separador = "/"
    formato = formato.replace('%', '').split(separador)
    fecha = fecha.split(separador)
    pos_m = formato.index('m')
    pos_Y = formato.index('Y')
    if fecha[pos_m] == "12":
        fecha[pos_m] = "01"
        fecha[pos_Y] = str(int(fecha[pos_Y]) + 1)
    else:
        fecha[pos_m] = str(int(fecha[pos_m]) + 1).rjust(2, "0")
    return f"{separador}".join(fecha)

def month_before(fecha: str, formato='%Y-%m-%d') -> str:
    if "-" in fecha:
        separador = "-"
    elif "/" in fecha:
        separador = "/"
    formato = formato.replace('%', '').split(separador)
    fecha = fecha.split(separador)
    pos_m = formato.index('m')
    pos_Y = formato.index('Y')
    if fecha[pos_m] == "01":
        fecha[pos_m] = "12"
        fecha[pos_Y] = str(int(fecha[pos_Y]) - 1)
    else:
        fecha[pos_m] = str(int(fecha[pos_m]) - 1).rjust(2, "0")
    return f"{separador}".join(fecha)

def date_mini(fecha: str, formato='%Y-%m-%d') -> str: # formato %Y-%m
    if "-" in fecha:
        separador = "-"
    elif "/" in fecha:
        separador = "/"
    formato = formato.replace('%', '').split(separador)
    fecha = fecha.split(separador)
    pos_m = formato.index('m')
    pos_Y = formato.index('Y')
    return f"{separador}".join((fecha[pos_Y], fecha[pos_m]))

def mes_by_ordinal(ordinal: str, abreviado=True, mes_anterior=False) -> str:
    if type(ordinal) is not str:
        ordinal = str(ordinal).rjust(2, '0')
    ORDINALES_MES = {
        "01":"Enero",
        "02":"Febrero",
        "03":"Marzo",
        "04":"Abril",
        "05":"Mayo",
        "06":"Junio",
        "07":"Julio",
        "08":"Agosto",
        "09":"Septiembre",
        "10":"Octubre",
        "11":"Noviembre",
        "12":"Diciembre"}
    try:
        if not mes_anterior:
            if abreviado:
                return ORDINALES_MES[ordinal][0:3]
            else:
                return ORDINALES_MES[ordinal]
        else:
            if abreviado:
                ordinal = str(int(ordinal) - 1).rjust(2, "0")
                return ORDINALES_MES[ordinal][0:3]
            else:
                return ORDINALES_MES[ordinal]
    except:
        return "NaN"

def mes_anio_by_abreviacion(abreviacion: str, capON: bool=False, MMAA: bool=False) -> str:
    ABREVIATURAS = {
        "Ene":"enero",
        "Feb":"febrero",
        "Mar":"marzo",
        "Abr":"abril",
        "May":"mayo",
        "Jun":"junio",
        "Jul":"julio",
        "Ago":"agosto",
        "Sep":"septiembre",
        "Oct":"octubre",
        "Nov":"noviembre",
        "Dic":"diciembre"}
    try:
        if MMAA:
            mes = ABREVIATURAS[abreviacion.split("-")[0]]
            anio = abreviacion.split("-")[1]
        else:
            mes = ABREVIATURAS[abreviacion.split("-")[1]]
            anio = abreviacion.split("-")[0]
        if capON:
            return f"{mes} {anio}".capitalize()
        else:
            return f"{mes} {anio}"
    except:
        return "NaN"

def anio_mes(fecha: str, formato='%Y-%m-%d') -> str:
    if "-" in fecha:
        separador = "-"
    elif "/" in fecha:
        separador = "/"
    formato = formato.replace('%', '').split(separador)
    fecha = fecha.split(separador)
    pos_m = formato.index('m')
    pos_Y = formato.index('Y')
    return "-".join((fecha[pos_Y], mes_by_ordinal(fecha[pos_m])))

def ultimo_dia_del_mes(fecha:str, formato='%Y-%m-%d') -> str:
    if "-" in fecha:
        separador = "-"
    elif "/" in fecha:
        separador = "/"
    formato = formato.replace('%', '').split(separador)
    fecha = fecha.split(separador)
    pos_m = formato.index('m')
    pos_d = formato.index('d')
    pos_Y = formato.index('Y')
    if fecha[pos_m] == 2:
        if es_bisiesto(int(fecha[pos_Y])):
           fecha[pos_d] = "29"
        else:
           fecha[pos_d] = "28"
    elif int(fecha[pos_m]) in (4, 6, 9, 11):
        fecha[pos_d] = "30"
    else:
        fecha[pos_d] = "31"

    return f"{separador}".join(fecha)

def es_bisiesto(anio):
	return not anio % 4 and (anio % 100 or not anio % 400)

def invertir_orden(data, Qfecha: bool = True):
    data_salida = []
    if Qfecha:
        for dato in data:
            fecha = "-".join(dato[0].split("-")[::-1])
            data_salida.append((fecha, dato[1]))
    else:
        for dato in data:
            data_salida.append(dato[::-1])
    return tuple(data_salida)