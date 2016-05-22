#-*- encoding: utf8 -*-

import os
import random
import json
import time


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
        self.taxa_mutacao = 0.05
        self.taxa_cruzamento = 0.9
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

    def _funcao_objetivo_unitaria(self, tab_aux, linha, col):
        """Funcao que calcula a funcao objetivo para uma unica peca"""
        # Verifica conflitos na horizontal
        conflitos = tab_aux.count(col) -1
        # if conflitos <= 0:
        #     conflitos = 0
        # Gera uma lista com as diagonais para a posicao
        diagonais = self.calc_diag(linha, col)
        tam_tab = len(tab_aux) - 1
        # Verifica para as diagonais se existe algum conflito
        for diag in diagonais:
            if tab_aux[diag[0]] == diag[1]:
                conflitos += 1
        return conflitos

    def _funcao_objetivo_tabuleiro(self, tabuleiro):
        """Funcao que calcula a funcao objetivo para todo o tabuleiro"""
        conflitos = 0
        for idx, indiv in enumerate(tabuleiro):
            conflitos += self._funcao_objetivo_unitaria(tabuleiro, idx, indiv)
        return conflitos

    def _criar_objeto_resultado(self, tabuleiro, indice_populacao):
        """Objeto de saida apos processamento """
        return { 'fo' : self.n_rainha * 999, 'tabuleiro': tabuleiro,
                       'indice': indice_populacao, 'iteracao': 0,
                       'inicio':  time.time(), 'termino': time.time()}

    def _selecionar_menor_fo_para_coluna(self, tabuleiro, x, saida):
        """Realiza o calculo de conflitos para cada linha na coluna informada
             e seleciona o menor valor encontrado
        """
        _fos_ = []
        for y in xrange(self.n_rainha):
            fo = self._funcao_objetivo_unitaria(tabuleiro, x, y)
            _fos_.append(fo)
            saida['iteracao'] += 1
        min_val = min(_fos_)
        tabuleiro[x] = _fos_.index(min_val)

    def _validar_saida_tabuleiro(self, tabuleiro, saida, indice_populacao):
        fo = self._funcao_objetivo_tabuleiro(tabuleiro)
        if saida['fo'] >= fo:
            saida['fo'] = fo
            saida['tabuleiro'] = tabuleiro
            saida['indice'] = indice_populacao

    def _executar_subida_encosta(self, tabuleiro, indice_populacao):
        pos = 1
        saida = self._criar_objeto_resultado(tabuleiro, indice_populacao)
        for count in xrange(self.qtd_iteracoes):
            for x in xrange(pos, self.n_rainha):
                self._selecionar_menor_fo_para_coluna(tabuleiro, x, saida)
                self._validar_saida_tabuleiro(tabuleiro, saida, indice_populacao)
                if saida['fo'] == 0:
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
                if tempera > random.randint(0, 100):
                    tabuleiro[x] = random.randint(0, self.n_rainha -1)
                else:
                    self._selecionar_menor_fo_para_coluna(tabuleiro, x, saida)
                self._validar_saida_tabuleiro(tabuleiro, saida, indice_populacao)
                if saida['fo'] == 0:
                    return saida
        return saida

    def subida_encosta(self):
        """ Metodo que para cada item da populacao e realizada
              a subida encosta """
        self.resultado_sb = []
        for indice, item in enumerate(self.populacao):
            saida = self._executar_subida_encosta(item[::], indice)
            saida['termino'] = time.time()
            self.resultado_sb.append(saida)
        return self.resultado_sb

    def tempera_simulada(self):
        """ Metodo que para cada item da populacao e realizada
              a tempera simulada"""
        self.resultado_sb = []
        for indice, item in enumerate(self.populacao):
            saida = self._executar_tempera_simulada(item[::], indice)
            saida['termino'] = time.time()
            self.resultado_sb.append(saida)
        return self.resultado_sb

    def _seleciona_individuos(self, populacao):
        # return self._seleciona_individuos_roleta(populacao[::])
        return self._seleciona_individuos_torneio(populacao[::])

    def _seleciona_individuos_torneio(self, populacao):
        selecao = []
        while len(selecao) < 2 and len(populacao) > 0:
            tam_pop = len(populacao) - 1
            a = random.randint(0, tam_pop)
            b = random.randint(0, tam_pop)
            while a == b:
                b = random.randint(0, tam_pop)
            indiv_a = populacao[a]
            indiv_b = populacao[b]
            fo_a = self._funcao_objetivo_tabuleiro(indiv_a)
            fo_b = self._funcao_objetivo_tabuleiro(indiv_b)
            if fo_a < fo_b:
                selecao.append(indiv_a)
                populacao.remove(indiv_a)
            else:
                selecao.append(indiv_b)
                populacao.remove(indiv_b)
        return selecao

    def _seleciona_individuos_roleta(self, populacao):
        _fos_ = []
        total_fo = 0.0
        for idx, item in enumerate(populacao):
            fo = self._funcao_objetivo_tabuleiro(item)
            if fo == 0:
                print idx, item
            total_fo += fo
            _fos_.append((fo, idx))
        _fos_.sort()
        selecao = []
        while len(selecao) < 2:
            porcentagem = random.random() * total_fo
            acumulado = 0
            for item in _fos_:
                fo_item = item[0]
                if fo_item == 0:
                    fo_item = 1
                acumulado += total_fo / fo_item
                if (porcentagem < acumulado) and selecao.count(self.populacao[item[1]]) == 0:
                    selecao.append(self.populacao[item[1]])
                    break

        del _fos_, total_fo
        return selecao

    def _realiza_cruzamento(self, pai_1, pai_2):
        individuo_1  = pai_1[::]
        individuo_2  = pai_2[::]
        posicao_corte = (len(individuo_1) / 2)
        if random.random() < self.taxa_cruzamento:
            if random.random() < 0.5:
                posicao_corte -= 1
            aux = individuo_1[posicao_corte:]
            individuo_1[posicao_corte:] = individuo_2[posicao_corte:]
            individuo_2[posicao_corte:] = aux
        return [individuo_1, individuo_2]

    def _realiza_mutacao(self, individuo):
        if random.random() < self.taxa_mutacao:
            individuo[random.randint(0, self.n_rainha - 1)] = random.randint(0, self.n_rainha - 1)
        return individuo

    def _avaliar_populacao(self, saida, populacao, geracao):
        for idx, item_pop in enumerate(populacao):
            obj_saida = self._criar_objeto_resultado(item_pop, idx)
            obj_saida['iteracao'] = geracao
            obj_saida['fo'] = self._funcao_objetivo_tabuleiro(item_pop)
            if obj_saida['fo'] < saida[idx]['fo'] :
                saida[idx] = obj_saida

    def alg_genetico(self, geracao):
        saida = [self._criar_objeto_resultado(None, 0) for e in xrange(len(self.populacao))]
        for ger in xrange(geracao):
            nova_populacao = []
            while len(nova_populacao) < len(self.populacao):
                # executa selecao
                pai_1, pai_2 = self._seleciona_individuos(self.populacao)
                # realiza o cruzamento
                filhos = self._realiza_cruzamento(pai_1, pai_2)
                # verifica mutacao
                self._realiza_mutacao(filhos[0])
                self._realiza_mutacao(filhos[1])
                # Adiciona a nova populacao
                nova_populacao.extend(filhos)
            # substitui populacao
            self.populacao = None
            self.populacao = nova_populacao
            self._avaliar_populacao(saida, self.populacao, ger)
        return saida

    def imprime_tabuleiro(self, tabuleiro):
        size = len(tabuleiro)
        for x in xrange(size):
            for y in xrange(size):
                if tabuleiro[y] == x:
                    print ' o ',
                else:
                    print ' x ',
            print ''

