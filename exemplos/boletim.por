algoritmo "Boletim"

var
    alunos: vetor[4] de cadeia
    notas: vetor[4] de real
    aprovados: lista de cadeia
    i: inteiro

funcao media(valores)
    var soma: real
    var j: inteiro
    para j de 0 ate tamanho(valores) - 1 faca
        soma <- soma + valores[j]
    fim_para
    retorne soma / tamanho(valores)
fim_funcao

inicio
    alunos <- ["Rey", "Ana", "Luke", "Bruno"]
    notas <- [9.5, 6, 4.5, 7]

    para i de 0 ate tamanho(alunos) - 1 faca
        se notas[i] >= 6 entao
            aprovados.adicionar(alunos[i])
        fim_se
    fim_para

    aprovados.ordenar()
    escreva("Média da turma: ", media(notas))
    escreva("Aprovados: ", aprovados.tamanho())
    para i de 0 ate aprovados.tamanho() - 1 faca
        escreva(i + 1, ". ", aprovados[i])
    fim_para
    escreva("Luke aprovado? ", aprovados.contem("Luke"))
fim_algoritmo
