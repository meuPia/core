algoritmo "SmartCam"
usar "maker"
usar "ia"

var 
    sensor_pin, led_pin: inteiro
    presenca: inteiro
    dados_imagem: inteiro
    classe_detectada: inteiro
inicio
    // Configuração IoT
    sensor_pin <- 4
    led_pin <- 2
    iot_configurar_pino(led_pin, "saida")
    iot_configurar_pino(sensor_pin, "entrada")

    // Configuração IA
    // [Tamanho, Velocidade] -> 0=Gato, 1=Humano
    ia_definir_dados([[10, 50], [12, 45], [170, 5], [180, 4]], [0, 0, 1, 1])
    ia_criar_knn(3)
    ia_treinar()

    escreva("Sistema Armado...")

    enquanto 1 = 1 faca
        presenca <- iot_ler(sensor_pin)
        
        se presenca = 1 entao
            escreva("Movimento detectado! Analisando...")
            
            // Simula leitura de caracteristicas
            // Ex: Tamanho 175cm, Velocidade 4km/h
            classe_detectada <- ia_prever([175, 4])
            
            se classe_detectada = 1 entao
                escreva("ALERTA: Humano detectado!")
                iot_ligar(led_pin)
                iot_esperar(2000)
                iot_desligar(led_pin)
            senao
                escreva("Alarme falso: É apenas um gato.")
            fim_se
        fim_se
        
        iot_esperar(500)
    fim_enquanto
fim_algoritmo
