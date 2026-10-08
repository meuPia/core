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

try:
    from meupia_maker.plugin_iot import *
except ImportError:
    print("Erro: O plugin 'maker' não está instalado. Execute: mpgp instale maker")
    sys.exit(1)
try:
    from meupia_ia.plugin_ia import *
except ImportError:
    print("Erro: O plugin 'ia' não está instalado. Execute: mpgp instale ia")
    sys.exit(1)

sensor_pin = 0
led_pin = 0
presenca = 0
dados_imagem = 0
classe_detectada = 0
def main():
    global sensor_pin, led_pin, presenca, dados_imagem, classe_detectada
    sensor_pin = 4
    led_pin = 2
    iot_configurar_pino(led_pin, _S("saida"))
    iot_configurar_pino(sensor_pin, _S("entrada"))
    ia_definir_dados([[10, 50], [12, 45], [170, 5], [180, 4]], [0, 0, 1, 1])
    ia_criar_knn(3)
    ia_treinar()
    _escreva(_S("Sistema Armado..."))
    while 1==1:
        presenca = iot_ler(sensor_pin)
        if presenca==1:
            _escreva(_S("Movimento detectado! Analisando..."))
            classe_detectada = ia_prever([175, 4])
            if classe_detectada==1:
                _escreva(_S("ALERTA: Humano detectado!"))
                iot_ligar(led_pin)
                iot_esperar(2000)
                iot_desligar(led_pin)
            else:
                _escreva(_S("Alarme falso: É apenas um gato."))
        iot_esperar(500)

if __name__ == '__main__':
    main()