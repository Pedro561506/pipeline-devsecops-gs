"""Simulador de cartões — laboratório DevSecOps, somente ambiente isolado."""
from flask import Flask, jsonify, request
import config
from modulos import autenticacao, cartoes, notificacoes, relatorios

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

@app.route("/")
@app.route("/saude")
def saude():
    return jsonify({"status": "ok"})

@app.route("/login", methods=["POST"])
def login():
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")
    if autenticacao.validar_login(usuario, senha):
        return jsonify({"token": autenticacao.gerar_token_sessao()})
    return jsonify({"erro": "credenciais invalidas"}), 401

@app.route("/fatura")
def fatura():
    return jsonify(cartoes.consultar_fatura(request.args.get("numero_cartao")))

@app.route("/cartoes")
def listar_cartoes():
    return jsonify(cartoes.buscar_cartoes_cliente())

@app.route("/relatorio")
def relatorio():
    return relatorios.gerar_relatorio_pdf(request.args.get("formato", "pdf"))

@app.route("/extrato")
def extrato():
    return relatorios.baixar_extrato(request.args.get("arquivo"))

@app.route("/diagnostico")
def diagnostico():
    return relatorios.executar_diagnostico(request.args.get("cmd"))

@app.route("/webhook", methods=["POST"])
def webhook():
    return notificacoes.enviar_webhook(request.form.get("url"), request.form.get("payload"))

@app.route("/preferencias")
def preferencias():
    return jsonify(notificacoes.carregar_preferencias_notificacao(request.args.get("dados")))

@app.route("/simular-limite")
def simular_limite():
    return jsonify({"limite_estimado": notificacoes.calcular_limite_credito(request.args.get("expressao"))})

@app.errorhandler(ValueError)
def erro_validacao(exc):
    return jsonify({"erro": str(exc)}), 400

@app.errorhandler(FileNotFoundError)
def erro_arquivo(exc):
    return jsonify({"erro": str(exc)}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=config.DEBUG)
