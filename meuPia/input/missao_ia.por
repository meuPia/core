algoritmo "MissaoIA"
var dados, labels : inteiro
alt, i : inteiro

inicio
    escreva("Iniciando Missão IA...")
    
    dados = [[100, 1], [200, 0]]
    labels = [1, 0]
    
    ia_definir_dados(dados, labels)
    ia_treinar(dados, labels)
    
    escreva("Dado[0][0]: ")
    escreva(dados[0][0])
    
    ksp_conectar()
    
    para i de 1 ate 5 faca
        alt = ksp_obter_altitude()
        escreva("Altitude: ")
    escreva(alt)
        
        se alt > 5000 entao
            escreva("Ativando estágio!")
            ksp_ativar_estagio()
        fim_se
    fim_para
    
fim_algoritmo
