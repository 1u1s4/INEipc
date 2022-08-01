from datetime import datetime, timedelta


def hoy(formato="%Y-%m-%d") -> str:
    return datetime.today().strftime(formato)

def day_after(fecha: str, formato='%Y-%m-%d') -> str:
    fecha_datetime = datetime.strptime(fecha, formato)
    fecha_mas_un_dia = fecha_datetime + timedelta(days=1)
    fecha_texto = fecha_mas_un_dia.strftime(formato)
    return fecha_texto

def year_ago(fecha: str, formato='%Y-%m-%d') -> str:
    if "-" in fecha:
        separador = "-"
    elif "/" in fecha:
        separador = "/"
    formato = formato.replace('%', '').split(separador)
    fecha = fecha.split(separador)
    pos_Y = formato.index('Y')
    fecha[pos_Y] = str(int(fecha[pos_Y]) - 1)
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

def date_mini(fecha: str) -> str: # formato AA/MM
    if "-" in fecha:
        separador = "-"
    elif "/" in fecha:
        separador = "/"
    return f"{separador}".join((fecha.split("-")[0], fecha.split("-")[1]))

def mes_by_ordinal(ordinal: str, abreviado=True) -> str:
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
        if abreviado:
            return ORDINALES_MES[ordinal][0:3]
        else:
            return ORDINALES_MES[ordinal]
    except:
        return "NaN"

def mes_anio_by_abreviacion(abreviacion: str, capON=False) -> str:
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
        mes = ABREVIATURAS[abreviacion.split("-")[1]]
        anio = abreviacion.split("-")[0]
        if capON:
            return f"{mes} {anio}".capitalize()
        else:
            return f"{mes} {anio}"
    except:
        return "NaN"

def anio_mes(fecha: str) -> str:
    return "-".join((fecha.split("-")[0], mes_by_ordinal(fecha.split("-")[1])))