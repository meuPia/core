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


matriz = 0
x = 0
def main():
    global matriz, x
    matriz = [[1, 2], [3, 4]]
    x = matriz[0][1]
    _escreva(x)

if __name__ == '__main__':
    main()