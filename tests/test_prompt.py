"""
tests/test_prompt.py  ->  TESTES UNITÁRIOS (sem internet, sem API, sem PDF)

Verificam a montagem do prompt em rag.montar_prompt() e a consistência
das configurações. Não chamam o Gemini e não precisam do banco vetorial.

Como rodar (na pasta do projeto):
    python -m unittest discover -s tests -v
"""

import sys
import unittest
from pathlib import Path

# Permite importar config.py e rag.py, que ficam na pasta acima de tests/.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config
from rag import montar_prompt


class TrechoFalso:
    """Imita o objeto 'documento' do LangChain: tem texto e metadados."""

    def __init__(self, texto, arquivo, pagina):
        self.page_content = texto
        self.metadata = {"arquivo": arquivo, "pagina": pagina}


class TestMontarPrompt(unittest.TestCase):
    def setUp(self):
        self.trechos = [
            TrechoFalso("Texto do primeiro trecho.", "guia.pdf", 3),
            TrechoFalso("Texto do segundo trecho.", "guia.pdf", 7),
        ]
        self.pergunta = "O que é uma VLAN?"
        self.prompt = montar_prompt(self.pergunta, self.trechos)

    def test_contem_a_pergunta(self):
        self.assertIn(self.pergunta, self.prompt)

    def test_contem_o_texto_de_todos_os_trechos(self):
        self.assertIn("Texto do primeiro trecho.", self.prompt)
        self.assertIn("Texto do segundo trecho.", self.prompt)

    def test_identifica_arquivo_e_pagina_de_cada_trecho(self):
        self.assertIn("[guia.pdf, página 3]", self.prompt)
        self.assertIn("[guia.pdf, página 7]", self.prompt)

    def test_mantem_a_ordem_dos_trechos(self):
        self.assertLess(
            self.prompt.index("Texto do primeiro trecho."),
            self.prompt.index("Texto do segundo trecho."),
        )

    def test_instrui_a_usar_somente_o_contexto(self):
        self.assertIn("SOMENTE", self.prompt)

    def test_define_frase_para_quando_nao_ha_resposta(self):
        self.assertIn("Não encontrei essa informação nas apostilas.", self.prompt)

    def test_contexto_vem_antes_da_pergunta(self):
        self.assertLess(self.prompt.index("CONTEXTO:"), self.prompt.index("PERGUNTA:"))

    def test_funciona_sem_trechos(self):
        prompt = montar_prompt("Qualquer pergunta", [])
        self.assertIn("Qualquer pergunta", prompt)
        self.assertIn("CONTEXTO:", prompt)


class TestConfig(unittest.TestCase):
    def test_sobreposicao_menor_que_o_tamanho_do_chunk(self):
        self.assertLess(config.SOBREPOSICAO_CHUNK, config.TAMANHO_CHUNK)

    def test_quantidade_de_trechos_positiva(self):
        self.assertGreater(config.QTD_TRECHOS, 0)

    def test_nome_do_modelo_gemini_definido(self):
        self.assertTrue(config.MODELO_GEMINI.strip())


if __name__ == "__main__":
    unittest.main()
