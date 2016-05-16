#!usr/bin/env python
#-*-encoding:utf-8-*-
from n_rainha import *

import unittest

class NRainhaTest(unittest.TestCase):
    qtd_n_rainha = 6
    qtd_amostras = 10
    DEBUG = False

    def print_log(self, val):
        if self.DEBUG:
            print val

    def test_GerarPopulacaoInicialAleatoria(self):
        n_rainha = NRainha(self.qtd_n_rainha, self.qtd_amostras)
        for item in n_rainha.tabuleiros_iniciais:
            self.assertTrue(n_rainha.tabuleiros_iniciais.count(item) <= 1 )

    def test_GerarPopulacaoInicialDeAcordoQuantidadeDefinida(self):
        n_rainha = NRainha(self.qtd_n_rainha, self.qtd_amostras)
        self.assertEquals(self.qtd_amostras, len(n_rainha.tabuleiros_iniciais))
        self.assertEquals(self.qtd_n_rainha, len(n_rainha.tabuleiros_iniciais[0]))

    def test_ArmazenarTabuleiroInicialEmArquivo(self):
        n_rainha = NRainha(self.qtd_n_rainha, self.qtd_amostras)
        n_rainha_2 = NRainha(self.qtd_n_rainha, self.qtd_amostras)
        self.assertEquals(n_rainha.tabuleiros_iniciais, n_rainha_2.tabuleiros_iniciais)

    def test_ExecutarSubidaDeEncostaEModificarTabuleiro(self):
        n_rainha = NRainha(self.qtd_n_rainha, self.qtd_amostras)
        result = n_rainha.subida_encosta()
        self.assertEquals(self.qtd_amostras, len(result))
        self.print_log("")
        for item in result:
            self.print_log(item)
            self.assertNotEquals(n_rainha.populacao[item['indice']], item['tabuleiro'])

    def test_CalcularAleatoriedadeTemperaSimulada(self):
        n_rainha = NRainha(self.qtd_n_rainha, self.qtd_amostras)
        anterior = 100
        for x in xrange(n_rainha.qtd_iteracoes):
            val = n_rainha.calc_tempera(x)
            self.assertLessEqual(val, anterior)
            anterior = val

    def test_ExecutarTemperaSimuladaEModificarTabuleiro(self):
        n_rainha = NRainha(self.qtd_n_rainha, self.qtd_amostras)
        result = n_rainha.tempera_simulada()
        self.assertEquals(self.qtd_amostras, len(result))
        self.print_log("")
        for item in result:
            self.print_log(item)
            self.assertNotEquals(n_rainha.populacao[item['indice']], item['tabuleiro'])



def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(NRainhaTest)
    unittest.TextTestRunner(verbosity = 2).run(suite)

if __name__ == '__main__':
    main()

