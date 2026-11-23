import unittest
import pandas as pd
from limpeza import limpar_dados
from metricas import calcular_metricas, receita_mensal, top_cidades

class TestDataPilot(unittest.TestCase):
    def setUp(self):
        self.original = pd.DataFrame({
            "pedido_id": ["P1", "P2", "P3", "P4"],
            "data": ["2025-01-05", "2025-01-10", "2025-02-01", "2025-02-02"],
            "produto": ["A", "B", "C", "D"],
            "categoria": ["Casa", "Casa", "Tech", "Tech"],
            "cliente_id": ["C1", "C2", "C1", "C3"],
            "cidade": ["Pelotas", "Rio Grande", "Pelotas", "Bagé"],
            "canal": ["Online"] * 4,
            "quantidade": [2, 1, 1, 3],
            "preco_unitario": [10.0, 20.0, 30.0, 5.0],
            "status": ["CONCLUIDO", "cancelado", "concluido", "Cancelado"]
        })

    def test_padroniza_status_e_calcula_receita(self):
        dados = limpar_dados(self.original)
        self.assertEqual(set(dados["status"]), {"concluido", "cancelado"})
        self.assertEqual(dados.loc[dados["pedido_id"] == "P1", "receita"].iloc[0], 20.0)

    def test_remove_pedido_duplicado(self):
        repetido = pd.concat([self.original, self.original.iloc[[0]]], ignore_index=True)
        dados = limpar_dados(repetido)
        self.assertEqual(dados["pedido_id"].nunique(), 4)

    def test_metricas_consideram_concluidos(self):
        dados = limpar_dados(self.original)
        metricas = calcular_metricas(dados)
        self.assertEqual(metricas["receita_total"], 50.0)
        self.assertEqual(metricas["pedidos_concluidos"], 2)
        self.assertEqual(metricas["clientes_unicos"], 1)
        self.assertEqual(metricas["taxa_cancelamento"], 50.0)

    def test_receita_mensal(self):
        dados = limpar_dados(self.original)
        mensal = receita_mensal(dados)
        self.assertEqual(len(mensal), 2)
        self.assertEqual(float(mensal.loc[mensal["mes"] == "2025-01", "receita"].iloc[0]), 20.0)

    def test_top_cidades(self):
        dados = limpar_dados(self.original)
        cidades = top_cidades(dados)
        self.assertEqual(cidades.iloc[0]["cidade"], "Pelotas")

if __name__ == "__main__":
    unittest.main()
