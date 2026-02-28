algoritmo "verifica_entrada_festa"
var
  idade, maioridade, tem_autorizacao: inteiro
inicio
  maioridade = 18

  escreva("Digite sua idade: ")
  leia(idade)

  escreva("Você tem autorização? (1 para sim, 0 para não): ")
  leia(tem_autorizacao)

  se (idade < maioridade) e (tem_autorizacao = 0) então
    escreva("Entrada negada. Menor de idade sem autorização.")
  senão
    escreva("Entrada permitida. Boa festa!")
  fim_se
fim_algoritmo
