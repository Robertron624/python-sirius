import sqlite3
URL_DB = "database.db"


def seleccion(sql) -> list:
    """Ejecutar una consulta de seleccion sobre la base de datos"""
    try:
        with sqlite3.connect(URL_DB) as con:
            cur = con.cursor()
            res = cur.execute(sql).fetchall()
    except Exception as ex:
        res = None
        print('ESTE ES EL ERROR::   ', ex)
    return res


def accion(instru, datos) -> int:
    "Ejecuta una accion sobre la base de datos"
    try:
        with sqlite3.connect(URL_DB) as con:
            cur = con.cursor()
            res = cur.execute(instru, datos).rowcount
            if res != 0:
                con.commit()
    except Exception as ex:
        res = 0
        print('ESTE ES EL ERROR:   ', ex)

    return res


def eliminarimg(instru):
    try:
        with sqlite3.connect(URL_DB) as con:
            cur = con.cursor()
            res = cur.execute(instru).rowcount
            if res != 0:
                con.commit
    except Exception as ex:
        print('ESTE ES EL ERROR DE SELECCION::  ', ex)
        res = 0

    return res


def editarimg(instru):
    try:
        with sqlite3.connect(URL_DB) as con:
            cur = con.cursor()
            res = cur.execute(instru).rowcount
            if res != 0:
                con.commit
    except Exception as ex:
        res = 0
        print('ESTE ES EL ERROR::   ', ex)
    return res

def get_last_comment_id():
    try:
        with sqlite3.connect(URL_DB) as con:
            cur = con.cursor()
            res = cur.execute("SELECT MAX(id) FROM comment").fetchone()
    except Exception as ex:
        res = None
        print('ERROR::   ', ex)
    return res