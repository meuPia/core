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
def _valor_msg(valor):
    if valor is True: return 'verdadeiro'
    if valor is False: return 'falso'
    if isinstance(valor, str): return '"' + str(valor) + '"'
    return str(valor)
def _elemento(tipo, valor, nome):
    # Verifica e normaliza um valor que vai entrar numa colecao tipada
    t = tipo.lower()
    if t == 'inteiro' and isinstance(valor, int) and not isinstance(valor, bool): return valor
    if t in ('real', 'float') and isinstance(valor, (int, float)) and not isinstance(valor, bool): return float(valor)
    if t in ('cadeia', 'string') and isinstance(valor, str): return _S(valor)
    if t == 'logico' and isinstance(valor, bool): return valor
    raise TypeError(nome + ' só aceita valores do tipo ' + tipo + '; recebeu ' + _valor_msg(valor))
_INICIAL = {'inteiro': 0, 'real': 0.0, 'float': 0.0, 'cadeia': '', 'string': '', 'logico': False}
def _eh_inteiro(valor):
    return isinstance(valor, int) and not isinstance(valor, bool)
class _Lista(list):
    _nome = 'a lista'
    _fora = 'da lista'
    def __init__(self, tipo, valores=()):
        self.tipo = tipo
        list.__init__(self, [_elemento(tipo, v, self._nome) for v in valores])
    @classmethod
    def receber(cls, tipo, valor):
        if type(valor) is cls and valor.tipo == tipo: return valor
        if not isinstance(valor, (list, deque)):
            raise TypeError(cls._nome + ' só recebe uma lista de valores; recebeu ' + _valor_msg(valor))
        return cls(tipo, valor)
    def _indice(self, i):
        n = len(self)
        if _eh_inteiro(i) and 0 <= i < n: return i
        if n == 0: raise IndexError('índice ' + _valor_msg(i) + ' fora ' + self._fora + ' vazia')
        raise IndexError('índice ' + _valor_msg(i) + ' fora ' + self._fora + ' de tamanho ' + str(n) + ' (use de 0 a ' + str(n - 1) + ')')
    def __getitem__(self, i): return list.__getitem__(self, self._indice(i))
    def __setitem__(self, i, valor): list.__setitem__(self, self._indice(i), _elemento(self.tipo, valor, self._nome))
    def append(self, valor): list.append(self, _elemento(self.tipo, valor, self._nome))
    def extend(self, valores): list.extend(self, [_elemento(self.tipo, v, self._nome) for v in valores])
    def __iadd__(self, valores):
        self.extend(valores)
        return self
    def inserir(self, posicao, valor):
        n = len(self)
        if not (_eh_inteiro(posicao) and 0 <= posicao <= n):
            raise IndexError('posição ' + _valor_msg(posicao) + ' fora da lista de tamanho ' + str(n) + ' (use de 0 a ' + str(n) + ')')
        list.insert(self, posicao, _elemento(self.tipo, valor, self._nome))
    def insert(self, posicao, valor): self.inserir(posicao, valor)
    def pop(self, *posicao):
        if posicao: return self.removerEm(posicao[0])
        if not self: raise ValueError('a lista está vazia')
        return list.pop(self)
    def removerEm(self, posicao): return list.pop(self, self._indice(posicao))
    def remover(self, valor):
        if valor not in self: raise ValueError('o valor ' + _valor_msg(valor) + ' não está na lista')
        list.remove(self, valor)
    def remove(self, valor): self.remover(valor)
    def buscar(self, valor): return list.index(self, valor) if valor in self else -1
    def contem(self, valor): return valor in self
    def ordenar(self): list.sort(self)
    def sort(self, *args, **kwargs): self.ordenar()
class _Vetor(_Lista):
    _nome = 'o vetor'
    _fora = 'do vetor'
    def __init__(self, tipo, n, valores=None):
        if valores is None: valores = [_INICIAL[tipo.lower()]] * n
        elif len(valores) != n: raise ValueError('o vetor tem ' + str(n) + ' posições, mas recebeu ' + str(len(valores)) + ' elementos')
        self.n = n
        _Lista.__init__(self, tipo, valores)
    @classmethod
    def receber(cls, tipo, n, valor):
        if type(valor) is cls and valor.tipo == tipo and valor.n == n: return valor
        if not isinstance(valor, (list, deque)):
            raise TypeError(cls._nome + ' só recebe uma lista de valores; recebeu ' + _valor_msg(valor))
        return cls(tipo, n, list(valor))
    def _fixo(self, *args, **kwargs):
        raise ValueError('o vetor tem tamanho fixo e não aceita adicionar nem remover elementos')
    append = extend = __iadd__ = inserir = insert = pop = removerEm = remover = remove = _fixo
    clear = appendleft = popleft = __delitem__ = _fixo


alunos = _Vetor('cadeia', 4)
notas = _Vetor('real', 4)
aprovados = _Lista('cadeia')
i = 0
def media(valores):
    global alunos, notas, aprovados, i
    soma = 0.0
    j = 0
    for j in _faixa(0, len(valores)-1, 1):
        soma = soma+valores[j]
    return soma/len(valores)

def main():
    global alunos, notas, aprovados, i
    alunos = _Vetor.receber('cadeia', 4, [_S("Rey"), _S("Ana"), _S("Luke"), _S("Bruno")])
    notas = _Vetor.receber('real', 4, [9.5, 6, 4.5, 7])
    for i in _faixa(0, len(alunos)-1, 1):
        if notas[i]>=6:
            aprovados.append(alunos[i])
    aprovados.ordenar()
    _escreva(_S("Média da turma: "), media(notas))
    _escreva(_S("Aprovados: "), aprovados.__len__())
    for i in _faixa(0, aprovados.__len__()-1, 1):
        _escreva(i+1, _S(". "), aprovados[i])
    _escreva(_S("Luke aprovado? "), aprovados.contem(_S("Luke")))

if __name__ == '__main__':
    main()