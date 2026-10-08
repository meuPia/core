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


idade1 = 0
idade2 = 0
idade3 = 0
media_idade = 0
def main():
    global idade1, idade2, idade3, media_idade
    _escreva(_S("Digite a idade da primeira pessoa: "))
    idade1 = int(input())
    _escreva(_S("Digite a idade da segunda pessoa: "))
    idade2 = int(input())
    _escreva(_S("Digite a idade da terceira pessoa: "))
    idade3 = int(input())
    media_idade = (idade1+idade2+idade3)/3
    _escreva(_S("\n"))
    _escreva(_S("A média das idades é: "))
    _escreva(media_idade)
    _escreva(_S(" ano(s)"))

if __name__ == '__main__':
    main()