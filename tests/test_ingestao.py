"""
tests/test_ingestao.py  ->  TESTE DA DIVISÃO EM PEDAÇOS (chunks)

Usa o divisor de texto REAL do LangChain, então só roda se as bibliotecas
do projeto estiverem instaladas. Não usa PDF, internet nem a API do Gemini.

Como rodar (na pasta do projeto):
    python -m unittest discover -s tests -v
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    import config
    from ingestao import dividir_em_chunks

    BIBLIOTECAS_OK = True
except ImportError:  # bibliotecas do projeto não instaladas
    BIBLIOTECAS_OK = False


@unittest.skipUnless(BIBLIOTECAS_OK, "bibliotecas do projeto não instaladas")
class TestDividirEmChunks(unittest.TestCase):
    def setUp(self):
        # Texto sintético (sem relação com nenhum material real).
        frase = "Um roteador encaminha pacotes entre redes diferentes. "
        self.paginas = [
            {"texto": frase * 60, "arquivo": "exemplo.pdf", "pagina": 1},
            {"texto": "Texto curto da segunda página.", "arquivo": "exemplo.pdf", "pagina": 2},
        ]
        self.textos, self.metadados = dividir_em_chunks(self.paginas)

    def test_um_metadado_para_cada_pedaco(self):
        self.assertEqual(len(self.textos), len(self.metadados))

    def test_nenhum_pedaco_passa_do_tamanho_maximo(self):
        for texto in self.textos:
            self.assertLessEqual(len(texto), config.TAMANHO_CHUNK)

    def test_pagina_longa_vira_varios_pedacos(self):
        da_pagina_1 = [m for m in self.metadados if m["pagina"] == 1]
        self.assertGreater(len(da_pagina_1), 1)

    def test_pagina_curta_vira_um_pedaco_com_a_origem_correta(self):
        da_pagina_2 = [
            (t, m) for t, m in zip(self.textos, self.metadados) if m["pagina"] == 2
        ]
        self.assertEqual(len(da_pagina_2), 1)
        self.assertEqual(da_pagina_2[0][1]["arquivo"], "exemplo.pdf")


if __name__ == "__main__":
    unittest.main()
