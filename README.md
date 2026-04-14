# Simulador de Filas em Tandem
Este projeto é a segunda etapa do desenvolvimento de um simulador de eventos discretos para redes de filas. O objetivo desta versão é expandir o simulador de fila única para suportar múltiplas filas conectadas em tandem.

## Sobre o Projeto
O simulador foi implementado utilizando a abordagem de **Avanço do Tempo Orientado a Eventos**. Ele gerencia um escalonador global e controla o consumo de números pseudoaleatórios, encerrando a simulação no exato momento em que o 100.000º número é gerado.

### Topologia Validada nesta Etapa
A simulação atual modela duas filas conectadas da seguinte forma:
* **Fila 1 (G/G/2/3):** Recebe clientes do exterior da rede (intervalo de chegada: 1 a 4). Possui 2 servidores com tempo de atendimento entre 3 e 4. 
* **Fila 2 (G/G/1/5):** Recebe 100% do tráfego proveniente da Fila 1. Não possui chegadas externas. Possui 1 servidor com tempo de atendimento entre 2 e 3.

## Como Executar
O simulador foi desenvolvido puramente em Python, sem a necessidade de bibliotecas externas.

### Pré-requisitos
* Python 3.x instalado na máquina.

### Execução via Terminal
1. Faça o clone deste repositório ou baixe o arquivo fonte (`simuladorTandem.py`).
2. Abra o terminal de comando no diretório do arquivo.
3. Execute o comando:
   ```bash
   python simuladorTandem.py
