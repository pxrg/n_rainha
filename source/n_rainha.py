#-*- encoding: utf8 -*-

import os
import random
import json


class NRainha(object):
    """Implementacao da busca de uma solucao do problema NRainha
         Sao abordados tres solucoes:
            * Subida de encosta
            * Tempera simulada
            * Algoritmo genetico
    """

    def __init__(self, n_rainha, qtd_amostras, armazenar_dados = True):
        super(NRainha, self).__init__()
        self.n_rainha = n_rainha
        self.qtd_populacao = qtd_amostras
        self.tabuleiros_iniciais = []
        self.populacao = []
        self.qtd_iteracoes = 100
        # Parametros do algoritmo genetico
        self.mutacao = 0.05
        self.cruzamento = 0.9
        self._cache = {}
        if not self.carregar_dados():
            for x in xrange(qtd_amostras):
                aux = self.criar_tabuleiro()
                self.tabuleiros_iniciais.append(aux[::])
                self.populacao.append(aux[::])
            if armazenar_dados:
                self.armazenar_dados()

    def carregar_dados(self):
        nome_arquivo = "n_rainha_n%s_p%s.json"%(self.n_rainha, self.qtd_populacao)
        if os.path.exists(nome_arquivo):
            with (open(nome_arquivo, 'r')) as _file_:
                aux = _file_.read()
                obj = json.loads(aux)
                self.tabuleiros_iniciais = obj['data'][::]
                self.populacao = obj['data'][::]
            return True
        else:
            return False

    def armazenar_dados(self):
        nome_arquivo = "n_rainha_n%s_p%s.json"%(self.n_rainha, self.qtd_populacao)
        with (open(nome_arquivo, 'w')) as _file_:
            _file_.write(json.dumps({'data': self.tabuleiros_iniciais}))

    def criar_tabuleiro(self):
        return [random.randint(0, self.n_rainha -1) for x in xrange(self.n_rainha)]

    def calc_diag(self, linha, col):
        if self._cache.has_key((linha, col,)):
            return self._cache.get((linha, col,))
        diag = []
        for pos in xrange(0, self.n_rainha):
            diag.append((linha + pos, col + pos,)) # cima + esquerda
            diag.append((linha - pos, col - pos,)) # baixo + esquerda
            diag.append((linha + pos, col - pos,)) # cima + direita
            diag.append((linha - pos, col + pos,)) # baixo + direita
        diag = filter(
            lambda x: (x[0] > -1 and x[1] > -1)
            and (x != (linha, col,) and (x[0] < self.n_rainha and x[1] < self.n_rainha)),
            diag
            )
        self._cache[(linha, col,)] = diag
        return diag[::]

    def _funcao_objetivo_unitaria(self, pop_aux, linha, col):
        conflitos = pop_aux.count(col) -1 # Verifica conflitos na horizontal
        if conflitos <= 0:
            conflitos = 0
        diagonais = self.calc_diag(linha, col)
        for diag in diagonais:
            if pop_aux[diag[0]] == diag[1]:
                conflitos += 1
        return conflitos

    def _funcao_objetivo_tabuleiro(self, tabuleiro):
        conflitos = 0
        for idx, indiv in enumerate(tabuleiro):
            conflitos += self._funcao_objetivo_unitaria(tabuleiro, idx, indiv)
        return conflitos

    def _criar_objeto_resultado(self, tabuleiro, indice_populacao):
        return { 'fo' : self.n_rainha * 999, 'tabuleiro': tabuleiro,
                       'indice': indice_populacao, 'iteracao': 0 }

    def _executar_subida_encosta(self, tabuleiro, indice_populacao):
        pos = 1
        saida = self._criar_objeto_resultado(tabuleiro, indice_populacao)
        for count in xrange(self.qtd_iteracoes):
            for x in xrange(pos, self.n_rainha):
                _fos_ = []
                for y in xrange(self.n_rainha):
                    _fos_.append(self._funcao_objetivo_unitaria(tabuleiro, x, y))
                    saida['iteracao'] += 1
                min_val = min(_fos_)
                tabuleiro[x] = _fos_.index(min_val)
                fo = self._funcao_objetivo_tabuleiro(tabuleiro)
                if saida['fo'] >= fo:
                    saida['fo'] = fo
                    saida['tabuleiro'] = tabuleiro
                    saida['indice'] = indice_populacao
                if fo == 0:
                    return saida
        return saida

    def _executar_tempera_simulada(self, tabuleiro, indice_populacao):
        pos = 1
        saida = self._criar_objeto_resultado(tabuleiro, indice_populacao)
        fo = saida['fo']
        tempera_base = self.qtd_iteracoes * 0.9
        for count in xrange(self.qtd_iteracoes):
            # Valor da tempera para a iteracao
            tempera = (tempera_base - count)
            for x in xrange(pos, self.n_rainha):
                _fos_ = []
                if tempera > random.randint(0, 100):
                    tabuleiro[x] = random.randint(0, self.n_rainha -1)
                else:
                    for y in xrange(self.n_rainha):
                        _fos_.append(self._funcao_objetivo_unitaria(tabuleiro, x, y))
                        saida['iteracao'] += 1
                    min_val = min(_fos_)
                    tabuleiro[x] = _fos_.index(min_val)
                fo = self._funcao_objetivo_tabuleiro(tabuleiro)
                if saida['fo'] >= fo:
                    saida['fo'] = fo
                    saida['tabuleiro'] = tabuleiro
                    saida['indice'] = indice_populacao
                    if fo == 0:
                        return saida
        return saida


    def subida_encosta(self):
        # tabuleiro = self.populacao[0][::]
        self.resultado_sb = []
        for indice, item in enumerate(self.populacao):
            self.resultado_sb.append(self._executar_subida_encosta(item[::], indice))
        return self.resultado_sb

    def tempera_simulada(self):
        # tabuleiro = self.populacao[0][::]
        self.resultado_sb = []
        for indice, item in enumerate(self.populacao):
            self.resultado_sb.append(self._executar_tempera_simulada(item[::], indice))
        return self.resultado_sb

    def buscar_alg_genetico(self, geracao):
        for ger in xrange(geracao):
            pass

    def imprime_tabuleiro(self, tabuleiro):
        size = len(tabuleiro)
        for x in xrange(size):
            for y in xrange(size):
                if tabuleiro[y] == x:
                    print ' o ',
                else:
                    print ' x ',
            print ''

