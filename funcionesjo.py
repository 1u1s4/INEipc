from datetime import datetime, timedelta


def hoy(formato="%Y-%m-%d") -> str:
    return datetime.today().strftime(formato)

def day_after(fecha: str, separador="-") -> str:
    fecha_datetime = datetime.strptime(fecha, f"%Y{separador}%m{separador}%d")
    fecha_mas_un_dia = fecha_datetime + timedelta(days=1)
    fecha_texto = fecha_mas_un_dia.strftime(f"%Y{separador}%m{separador}%d")
    return fecha_texto

def year_ago(fecha: str) -> str: # formato AA/MM/DD
    if "-" in fecha:
        separador = "-"
    elif "/" in fecha:
        separador = "/"
    return f"{separador}".join((str(int(fecha.split("-")[0]) - 1), fecha.split("-")[1], fecha.split("-")[2]))

def month_after(fecha: str) -> str: # formato AA/MM/DD
    if "-" in fecha:
        separador = "-"
    elif "/" in fecha:
        separador = "/"
    if fecha.split("-")[1] == "12":
        return f"{separador}".join((str(int(fecha.split("-")[0]) + 1), "01", fecha.split("-")[2]))
    else:
        return f"{separador}".join((fecha.split("-")[0], str(int(fecha.split("-")[1]) + 1).rjust(2, "0"), fecha.split("-")[2]))

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