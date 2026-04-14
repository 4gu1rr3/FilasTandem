semente = 1  
a = 1664525
c = 1013904223
M = 4294967296
aleatorios_consumidos = 0
limite_aleatorios = 100000

class FimSimulacao(Exception):
    pass

def NextRandom():
    global semente, aleatorios_consumidos
    if aleatorios_consumidos >= limite_aleatorios:
        raise FimSimulacao()
    
    aleatorios_consumidos += 1
    semente = ((a * semente) + c) % M
    return float(semente) / float(M)

def simulacao_tandem():
    tempo = 0.0
    
    # Estrutura de dados para suportar múltiplas filas
    filas = {
        1: {
            "atendentes": 2, "capacidade": 3, 
            "min_atend": 3.0, "max_atend": 4.0,
            "quant_fila": 0, "clientes_fora": 0, 
            "tempos_acumulados": [0.0] * 4 # Estados 0, 1, 2, 3
        },
        2: {
            "atendentes": 1, "capacidade": 5, 
            "min_atend": 2.0, "max_atend": 3.0,
            "quant_fila": 0, "clientes_fora": 0, 
            "tempos_acumulados": [0.0] * 6 # Estados 0, 1, 2, 3, 4, 5
        }
    }
    
    min_chegada_ext = 1.0
    max_chegada_ext = 4.0
    
    # O escalonador agora armazena: [tempo_evento, tipo_evento, id_fila]
    # O primeiro cliente chega no tempo 1.5 na Fila 1, conforme especificação
    escalonador = [[1.5, "CHEGADA", 1]]
    
    try:
        while True:
            escalonador.sort()
            evento_atual = escalonador.pop(0)
            
            tempo_evento = evento_atual[0]
            tipo_evento = evento_atual[1]
            id_fila = evento_atual[2]
            
            # Atualiza tempos acumulados de TODAS as filas com o delta
            tempo_decorrido = tempo_evento - tempo
            for f in filas.values():
                f["tempos_acumulados"][f["quant_fila"]] += tempo_decorrido
                
            tempo = tempo_evento
            fila_atual = filas[id_fila]
            
            if tipo_evento == "CHEGADA":
                # Se a chegada for na Fila 1 (exterior), agenda a próxima chegada externa
                if id_fila == 1:
                    tempo_prox = min_chegada_ext + (max_chegada_ext - min_chegada_ext) * NextRandom()
                    escalonador.append([tempo + tempo_prox, "CHEGADA", 1])
                
                if fila_atual["quant_fila"] < fila_atual["capacidade"]:
                    fila_atual["quant_fila"] += 1
                    
                    if fila_atual["quant_fila"] <= fila_atual["atendentes"]:
                        # Agenda a saída
                        t_min = fila_atual["min_atend"]
                        t_max = fila_atual["max_atend"]
                        tempo_atend = t_min + (t_max - t_min) * NextRandom()
                        escalonador.append([tempo + tempo_atend, "SAIDA", id_fila])
                else:
                    fila_atual["clientes_fora"] += 1
                    
            elif tipo_evento == "SAIDA":
                fila_atual["quant_fila"] -= 1 
                
                if fila_atual["quant_fila"] >= fila_atual["atendentes"]:
                    t_min = fila_atual["min_atend"]
                    t_max = fila_atual["max_atend"]
                    tempo_atend = t_min + (t_max - t_min) * NextRandom()
                    escalonador.append([tempo + tempo_atend, "SAIDA", id_fila])
                
                # Roteamento Tandem: Saída da Fila 1 é uma Chegada IMEDIATA na Fila 2
                if id_fila == 1:
                    escalonador.append([tempo, "CHEGADA", 2])
                    # Nota: Inserimos no escalonador com o mesmo 'tempo' para processar na próxima iteração
                    
    except FimSimulacao:
        # A simulação é interrompida no exato momento em que o 100.000º aleatório é gerado
        pass

    # --- IMPRESSÃO DOS RESULTADOS ---
    print(f"\nTempo Global da Simulação : {tempo:.4f}")
    
    for id_fila, f in filas.items():
        print(f"\n" + "="*65)
        print(f" FILA {id_fila} - G/G/{f['atendentes']}/{f['capacidade']}")
        print("="*65)
        print(f"{'Estado':<10} | {'Tempo Acumulado':<20} | {'Probabilidade':<15}")
        print("-" * 65)
        
        for i in range(f["capacidade"] + 1):
            prob = (f["tempos_acumulados"][i] / tempo) * 100 if tempo > 0 else 0.0
            print(f"{i:<10} | {f['tempos_acumulados'][i]:<20.4f} | {prob:<14.2f}%")
            
        print("-" * 65)
        print(f"Clientes Perdidos: {f['clientes_fora']}")
    print("="*65 + "\n")

# Execução
simulacao_tandem()