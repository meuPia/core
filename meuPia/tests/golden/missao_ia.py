# -*- coding: utf-8 -*-
import sys
import math
import heapq
class _S(str):
    def __add__(self, other):
        if other is True: other = 'verdadeiro'
        elif other is False: other = 'falso'
        return _S(str(self) + str(other))
    def __radd__(self, other):
        if other is True: other = 'verdadeiro'
        elif other is False: other = 'falso'
        return _S(str(other) + str(self))
def _texto(valor):
    if valor is True: return 'verdadeiro'
    if valor is False: return 'falso'
    return str(valor)
def _escreva(*valores):
    print(''.join(_texto(v) for v in valores))
def _faixa(inicio, fim, passo):
    # Intervalo do laco 'para': inclui o fim nos dois sentidos
    if passo == 0: raise ValueError('passo do laço para não pode ser zero')
    return range(inicio, fim + 1, passo) if passo > 0 else range(inicio, fim - 1, passo)
from collections import deque
class FilaPrioridade:
    def __init__(self):
        self.heap = []
    def inserir(self, item):
        heapq.heappush(self.heap, item)
    def remover(self):
        return heapq.heappop(self.heap)
    def espiar(self):
        return self.heap[0] if self.heap else None
    def len(self):
        return len(self.heap)
    def __len__(self):
        return len(self.heap)


dados = 0
labels = 0
alt = 0
i = 0
def main():
    global dados, labels, alt, i
    _escreva(_S("Iniciando Missão IA..."))
    dados = [[100, 1], [200, 0]]
    labels = [1, 0]
    ia_definir_dados(dados, labels)
    ia_treinar(dados, labels)
    _escreva(_S("Dado[0][0]: "))
    _escreva(dados[0][0])
    ksp_conectar()
    for i in _faixa(1, 5, 1):
        alt = ksp_obter_altitude()
        _escreva(_S("Altitude: "))
        _escreva(alt)
        if alt>5000:
            _escreva(_S("Ativando estágio!"))
            ksp_ativar_estagio()

if __name__ == '__main__':
    main()