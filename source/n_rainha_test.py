#!usr/bin/env python
#-*-encoding:utf-8-*-
from n_rainha import *

import unittest

def armazenar_dados(metodo, result):
    # nome_arquivo = "metodo_%s.json"%(metodo)
    # with (open(nome_arquivo, 'w')) as _file_:
    #     _file_.write(json.dumps(result))
    pass

class NRainhaTest(unittest.TestCase):
    qtd_n_rainha = 8
    qtd_amostras = 10
    DEBUG = True
    # DEBUG = False

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

    def test_ArmazenarTabuleiroInicialEmArquivoERecuperar(self):
        n_rainha = NRainha(self.qtd_n_rainha, self.qtd_amostras)
        n_rainha_2 = NRainha(self.qtd_n_rainha, self.qtd_amostras)
        self.assertEquals(n_rainha.tabuleiros_iniciais, n_rainha_2.tabuleiros_iniciais)

    def test_ValidarFuncaoObjetivo(self):
        n_rainha = NRainha(self.qtd_n_rainha, self.qtd_amostras)
        tabuleiro = range(self.qtd_n_rainha -1, -1, -1)
        # Validacao do calculo para uma unica posicao
        self.assertEquals(self.qtd_n_rainha -1, n_rainha._funcao_objetivo_unitaria(tabuleiro, tabuleiro[0], 0))
        # Validacao do calculo para o tabuleiro
        self.assertEquals((self.qtd_n_rainha -1) * self.qtd_n_rainha, n_rainha._funcao_objetivo_tabuleiro(tabuleiro))


    def test_ExecutarSubidaDeEncostaEModificarTabuleiro(self):
        n_rainha = NRainha(self.qtd_n_rainha, self.qtd_amostras)
        result = n_rainha.subida_encosta()
        self.assertEquals(self.qtd_amostras, len(result))
        armazenar_dados("subida_encosta", result)
        self.print_log("")
        for item in result:
            self.print_log(item)
            self.assertNotEquals(n_rainha.populacao[item['indice']], item['tabuleiro'])


    def test_ExecutarTemperaSimuladaEModificarTabuleiro(self):
        n_rainha = NRainha(self.qtd_n_rainha, self.qtd_amostras)
        result = n_rainha.tempera_simulada()
        self.assertEquals(self.qtd_amostras, len(result))
        armazenar_dados("tempera_simulada", result)
        self.print_log("")
        # n_rainha.imprime_tabuleiro(result[0]['tabuleiro'])
        for item in result:
            self.print_log(item)
            self.assertNotEquals(n_rainha.populacao[item['indice']], item['tabuleiro'])

    def test_AG_SelecionarIndividuos(self):
        n_rainha = NRainha(self.qtd_n_rainha, self.qtd_amostras)
        selecionados = n_rainha._seleciona_individuos(n_rainha.populacao)
        self.assertTrue(len(selecionados) == 2 )

    def test_AG_SelecionarIndividuosRealizarCruzamento(self):
        n_rainha = NRainha(self.qtd_n_rainha, self.qtd_amostras)
        selecionados = n_rainha._seleciona_individuos(n_rainha.populacao)
        self.assertEquals( 2, len(selecionados) )
        saida = n_rainha._realiza_cruzamento(selecionados[0], selecionados[1])
        self.assertNotEquals(selecionados, saida)

    def test_AG_ExecutarAlgoritomoGenetico(self):
        n_rainha = NRainha(self.qtd_n_rainha, self.qtd_amostras)
        result = n_rainha.alg_genetico(1000)
        self.assertEquals(self.qtd_amostras, len(result))
        armazenar_dados("alg_genetico", result)
        self.print_log("")
        # n_rainha.imprime_tabuleiro(result[0]['tabuleiro'])
        for item in result:
            self.print_log(item)
            self.assertNotEquals(n_rainha.tabuleiros_iniciais[item['indice']], item['tabuleiro'])





def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(NRainhaTest)
    unittest.TextTestRunner(verbosity = 2).run(suite)

if __name__ == '__main__':
    main()

