"""Autenticação simplificada para o laboratório (credenciais via ambiente)."""
import os
import secrets
from werkzeug.security import check_password_hash, generate_password_hash


def gerar_hash_senha(senha):
    """Gera hash de senha com scrypt e salt aleatório."""
    return generate_password_hash(senha, method="scrypt")


def validar_login(usuario, senha):
    """Exige usuário e hash de senha configurados externamente."""
    if not isinstance(usuario, str) or not isinstance(senha, str):
        return False
    esperado_usuario = os.getenv("APP_LOGIN_USER")
    hash_esperado = os.getenv("APP_PASSWORD_HASH")
    if not esperado_usuario or not hash_esperado:
        return False
    return secrets.compare_digest(usuario, esperado_usuario) and check_password_hash(hash_esperado, senha)


def gerar_token_sessao():
    """Token criptograficamente imprevisível."""
    return secrets.token_urlsafe(32)
