"""Integrações com lista de destinos permitidos e dados JSON seguros."""
import ast
import ipaddress
import json
import operator
import os
from urllib.parse import urlparse
import requests


def enviar_webhook(url_destino, payload):
    """Permite apenas hosts HTTPS explicitamente configurados."""
    parsed = urlparse(url_destino or "")
    hosts = {h.strip().lower() for h in os.getenv("WEBHOOK_ALLOWED_HOSTS", "").split(",") if h.strip()}
    host = (parsed.hostname or "").lower()
    if (parsed.scheme != "https" or not host or host not in hosts
            or parsed.username or parsed.password or parsed.port not in (None, 443)):
        raise ValueError("Destino de webhook não permitido")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        raise ValueError("Endereço IP direto não permitido")
    # allow_redirects=False impede redirecionamento para serviços internos.
    response = requests.post(url_destino, data=payload or "", timeout=5, allow_redirects=False)
    response.raise_for_status()
    return response.text


def carregar_preferencias_notificacao(dados_serializados):
    """Aceita JSON, não payloads pickle."""
    dados = json.loads(dados_serializados or "{}")
    if not isinstance(dados, dict):
        raise ValueError("Preferências devem ser um objeto JSON")
    return dados

_OPERADORES = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
              ast.Div: operator.truediv}

def _calcular(no, profundidade=0):
    if profundidade > 12:
        raise ValueError("Expressão muito complexa")
    if isinstance(no, ast.Constant) and type(no.value) in (int, float):
        if abs(no.value) > 1000000:
            raise ValueError("Número fora do limite")
        return no.value
    if isinstance(no, ast.UnaryOp) and isinstance(no.op, (ast.UAdd, ast.USub)):
        valor = _calcular(no.operand, profundidade + 1)
        return valor if isinstance(no.op, ast.UAdd) else -valor
    if isinstance(no, ast.BinOp) and type(no.op) in _OPERADORES:
        resultado = _OPERADORES[type(no.op)](_calcular(no.left, profundidade + 1), _calcular(no.right, profundidade + 1))
        if abs(resultado) > 1000000000:
            raise ValueError("Resultado fora do limite")
        return resultado
    raise ValueError("Expressão matemática não permitida")


def calcular_limite_credito(expressao):
    if not isinstance(expressao, str) or len(expressao) > 100:
        raise ValueError("Expressão inválida")
    try:
        return _calcular(ast.parse(expressao, mode="eval").body)
    except (SyntaxError, ZeroDivisionError, OverflowError, TypeError) as exc:
        raise ValueError("Expressão inválida") from exc
