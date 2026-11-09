"""Testes mínimos de regressão de segurança."""
import unittest
from unittest.mock import patch
from modulos import autenticacao, notificacoes, relatorios
from werkzeug.security import generate_password_hash

class TestSeguranca(unittest.TestCase):
    def test_token_aleatorio(self):
        self.assertNotEqual(autenticacao.gerar_token_sessao(), autenticacao.gerar_token_sessao())

    def test_senha(self):
        with patch.dict("os.environ", {"APP_LOGIN_USER": "aluno", "APP_PASSWORD_HASH": generate_password_hash("teste-seguro") }):
            self.assertTrue(autenticacao.validar_login("aluno", "teste-seguro"))
            self.assertFalse(autenticacao.validar_login("aluno", "errada"))

    def test_webhook_bloqueado(self):
        with self.assertRaises(ValueError):
            notificacoes.enviar_webhook("http://127.0.0.1/admin", "x")

    def test_pickle_rejeitado(self):
        with self.assertRaises(ValueError):
            notificacoes.carregar_preferencias_notificacao("800495")

    def test_expressao(self):
        self.assertEqual(notificacoes.calcular_limite_credito("2 + 3 * 4"), 14)
        with self.assertRaises(ValueError):
            notificacoes.calcular_limite_credito("__import__('os').system('id')")

    def test_traversal(self):
        with self.assertRaises(ValueError):
            relatorios.baixar_extrato("../../etc/passwd")

    def test_diagnostico_bloqueado(self):
        with self.assertRaises(ValueError):
            relatorios.executar_diagnostico("cat /etc/passwd")

if __name__ == "__main__":
    unittest.main()
