"""Relatórios e extratos sem execução de comandos arbitrários."""
import os
from pathlib import Path

EXTRATOS = Path(os.getenv("EXTRATOS_DIR", "/var/extratos")).resolve()


def gerar_relatorio_pdf(formato):
    """Simulação de relatório; o projeto original não inclui gerar_pdf.sh."""
    if formato != "pdf":
        raise ValueError("Formato não suportado")
    return "Relatório PDF solicitado (simulação do laboratório)"


def baixar_extrato(nome_arquivo):
    if not isinstance(nome_arquivo, str) or not nome_arquivo or nome_arquivo != Path(nome_arquivo).name:
        raise ValueError("Nome de arquivo inválido")
    caminho = (EXTRATOS / nome_arquivo).resolve()
    if not caminho.is_relative_to(EXTRATOS) or not caminho.is_file():
        raise FileNotFoundError("Extrato não encontrado")
    return caminho.read_text(encoding="utf-8")


def executar_diagnostico(comando_usuario):
    """Somente diagnósticos pré-definidos, sem shell."""
    comandos = {"saude": "ok", "versao": "simulador-cartoes-lab"}
    if comando_usuario not in comandos:
        raise ValueError("Diagnóstico não permitido")
    return comandos[comando_usuario]
