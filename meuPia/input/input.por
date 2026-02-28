algoritmo "media_idades"
var
	idade1, idade2, idade3: inteiro
	media_idade: inteiro
inicio
escreva("Digite a idade da primeira pessoa: ")
  leia(idade1)

  escreva("Digite a idade da segunda pessoa: ")
  leia(idade2)

  escreva("Digite a idade da terceira pessoa: ")
  leia(idade3)

  media_idade = (idade1 + idade2 + idade3) / 3

  escreva("\n")
  escreva("A média das idades é: ")
  escreva(media_idade)
  escreva(" ano(s)")
fim_algoritmo
