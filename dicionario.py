import re
#Verifica se está em outra linguagem de programação e traduz
class dicionario:
    def __init__(self, nome_arq):
        self.vezes=-1
        self.n=-1
        self.medicao=[]
        self.comandos=[]
        self.arq = open(nome_arq)  # arquivo deve preexistir
        self.i = 0 #contador para inverter a medição
        self.le_info()

    def le_info(self):
        info = self.arq.readline().split() # Armazena a primeira linha

        if (info[0] == 'QASM'): #Se o código for em QASM
            entrada = self.arq.readlines()#lê o arquivo

            for linha in entrada:
                linha = linha.strip()

                if (linha[:4] == 'qreg'): #número de qbits
                    separador = linha.split('[')
                    numero = separador[1].split(']')
                    numero = numero[0]
                    self.n = numero


                elif (linha[:7] == 'barrier') : #Barreira
                    pass

                elif (linha[:4] == 'creg') :#bits clássicos
                    separador = linha.split('[')
                    separador= separador[1].split(']')
                    classicos = int (separador[0])
                    self.medicao=[0]*classicos

                elif (linha[:7] == 'measure'):  # Medir qbits
                    separador = linha.split('[')
                    numero = separador[1].split(']')
                    self.medicao[len(self.medicao) - self.i-1] = int(numero[0])
                    self.i= self.i+1

                else: #Operações
                    try:
                        porta = linha.split(' ')
                        inteiros = re.findall(r'\d+', porta[1])
                        if (len(inteiros) == 3):
                            self.comandos.append(porta[0] +'(' +inteiros[0] +',' +inteiros[1] +','+inteiros[2] +')')
                        elif (len(inteiros) == 2):
                            self.comandos.append(porta[0] + '(' + inteiros[0] + ',' + inteiros[1]  + ')')
                        else:
                            self.comandos.append(porta[0] + '(' + inteiros[0]+ ')')
                    except:
                        pass
        elif info[0] == 'Qiskit': #se o código for em Qiskit
            entrada = self.arq.readlines()  # lê o arquivo

            for linha in entrada:
                linha = linha.strip()

                if (linha[:3] == 'def') :
                    pass

                elif ('ClassicalRegister' in linha):
                    separador = linha.split('(')
                    separador = separador[1].split(',')
                    classicos = int(separador[0])
                    self.medicao = [0] * classicos

                elif ('QuantumRegister' in linha):
                    separador = linha.split('(')
                    numero = separador[1].split(',')
                    self.n = numero[0]

                elif ('QuantumCircuit' in linha):
                    circuito = linha.split(' ')
                    circuito = circuito[0]

                elif ('measure' in linha):
                    separador = linha.split('[')
                    numero = separador[1].split(']')
                    self.medicao[len(self.medicao) - self.i - 1] = int(numero[0])
                    self.i = self.i + 1

                else:
                    try:
                        porta = linha.split('.')
                        porta = porta[1].split('(')
                        inteiros = re.findall(r'\d+', porta[1])
                        if (len(inteiros) == 3):
                            self.comandos.append(porta[0] +'(' +inteiros[0] +',' +inteiros[1] +','+inteiros[2] +')')
                        elif (len(inteiros) == 2):
                            self.comandos.append(porta[0] + '(' + inteiros[0] + ',' + inteiros[1]  + ')')
                        else:
                            self.comandos.append(porta[0] + '(' + inteiros[0]+ ')')
                    except:
                        pass





