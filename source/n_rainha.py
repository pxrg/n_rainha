#-*- encoding: utf8 -*-

import os
import random


class NRainha(object):
    """Implementacao da busca de uma solucao do problema NRainha
         Sao abordados tres solucoes:
            * Subida de encosta
            * Tempera simulada
            * Algoritmo genetico
    """

    def __init__(self, n_rainha, qtd_amostras):
        super(NRainha, self).__init__()
        self.n_rainha = n_rainha
        self.tabuleiros_iniciais = []
        self.populacao = []
        # Parametros do algoritmo genetico
        self.mutacao = 0.05
        self.cruzamento = 0.9
        self._cache = {}
        for x in xrange(qtd_amostras):
            aux = self.criar_tabuleiro()
            self.tabuleiros_iniciais.append(aux[::])
            self.populacao.append(aux[::])

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


    def criar_tabuleiro(self):
        return [random.randint(0, self.n_rainha) for x in xrange(self.n_rainha)]

    def _funcao_objetivo_unitaria(self, pop_aux, linha, col):
        conflitos = pop_aux.count(col) -1 # Verifica conflitos na horizontal
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

    def subida_encosta(self):
        tabuleiro = self.populacao[0][::]
        pos = 1
        for count in xrange(100):
            for x in xrange(pos, self.n_rainha):
                _fos_ = []
                for y in xrange(self.n_rainha):
                    _fos_.append(self._funcao_objetivo_unitaria(tabuleiro, x, y))
                min_val = min(_fos_)
                tabuleiro[x] = _fos_.index(min_val)
                if self._funcao_objetivo_tabuleiro(tabuleiro) == 0:
                    return tabuleiro
            if self._funcao_objetivo_tabuleiro(tabuleiro) == 0:
                return tabuleiro
        return None



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
                
