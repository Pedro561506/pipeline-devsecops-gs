"""Consultas de cartões parametrizadas."""
import sqlite3
from flask import request


def consultar_fatura(numero_cartao):
    if not numero_cartao:
        return None
    with sqlite3.connect("cartoes.db") as conn:
        return conn.execute("SELECT fatura FROM cartoes WHERE numero = ?", (numero_cartao,)).fetchone()


def buscar_cartoes_cliente():
    cpf = request.args.get("cpf", "")
    if not cpf:
        return []
    with sqlite3.connect("cartoes.db") as conn:
        return conn.execute("SELECT * FROM cartoes WHERE cpf_titular = ?", (cpf,)).fetchall()
