'''
simulação de circuitos quânticos

autores: Gabriela Pinheiro Costa, Luis Kowada e Camila Ferreira

ultima alteração: 11/09/2021 (CF)

pendências:   

1- Definição de funções
2- Otimização do processamento
3- *Ideia: definição de funções já salvar o matriz operador resultante.

status atual: cx,ccx,swap são permutações.
              O código traduz para QASM e Qiskit
              O código lê e traduz de QASM ou Qikist para a linguagem desenvolvida.
'''

from simulacao import *
from traducao import traducao

nome_arquivo = "traducao"
#nome_arquivo = input("Digite o nome do arquivo: ")

simu = simulacao(0,0,nome_arquivo)
simu.simular()