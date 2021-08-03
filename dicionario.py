import re
#Verifica se está em outra linguagem de programação e traduz
#implementar for com variáveis
class dicionario:
    def __init__(self, nome_arq):
        self.vezes=-1
        self.n=-1
        self.medicao=[]
        self.variaveis = {}
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

                elif ('to' in linha):
                    self.traduz = True
                    linguagem = linha.split('to ')
                    self.linguagem = linguagem[1]


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
            medicao=''
            for i in range (0,len(self.medicao)):

                if (i!=0):
                    medicao= medicao+','+str(self.medicao[i])
                else:
                    medicao=str(self.medicao[i])

            self.comandos.append('(['+medicao+')]')

        elif info[0] == 'Qiskit': #se o código for em Qiskit
            inclui=False
            entrada = self.arq.readlines()  # lê o arquivo

            for linha in entrada:
                linha = linha.strip()
                if (linha[:0] != '#'):
                    if (linha[:3] == 'def' or ('#' in linha[:1])) :
                        pass

                    elif ('ClassicalRegister' in linha):
                        separador = linha.split('(')
                        separador = separador[1].split(',')
                        classicos = int(separador[0])
                        self.medicao = [0] * (classicos-1)

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

                    elif (('int' in linha[:4]) or ('float' in linha [:6])):
                        variavel= linha.split(" ")
                        variavel=variavel[0]
                        valor=re.findall(r'\d+', linha)

                        if ('int' in linha):
                            self.variaveis[variavel] = int(valor[0])

                        elif ('float' in linha):
                            self.variaveis[variavel]=float(valor[0])

                    elif ('for' in linha):
                        for_variavel=linha.split(" ")
                        for_variavel=for_variavel[1].split(" ")
                        for_variavel=for_variavel[0]

                        inteiros = re.findall(r'\d+', linha)

                        if (len(inteiros)==1):

                            for_inicio=0
                            for_final=inteiros[0]

                        elif (len(inteiros)==2):
                            for_inicio=inteiros[0]
                            for_final=inteiros[1]
                            for_inicio = int(for_inicio)

                        for_final = int(for_final)

                        try:
                            for_final = int(for_final)
                        except:
                            for a in self.variaveis:
                                if for_final == a:
                                    for_final = self.variaveis.get(a)
                                    for_final = int(for_final)
                        inclui = True

                    elif (inclui):
                        porta=linha.split('.')
                        porta=porta[1].split('(')
                        inclui=False
                        for a in range (for_inicio,for_final):
                            comando=(porta[0]+'('+str(a) +')')
                            self.comandos.append(comando)

                    elif ('to' in linha):
                        self.traduz=True
                        linguagem = linha.split('to ')
                        self.linguagem = linguagem[1]

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




