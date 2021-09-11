import re
#Verifica se está em outra linguagem de programação e traduz
class dicionario:
    def __init__(self, nome_arq):
        self.vezes=-1
        self.n=-1
        self.medicao=[]
        self.variaveis = {}
        self.comandos=[]
        self.arq = open(nome_arq)  # arquivo deve preexistir
        self.i = 0 #contador para inverter a medição
        self.traduz = False
        self.le_info()

        for a in range (0,(len(self.medicao)//2)):
            aux=self.medicao[self.i]
            self.medicao[self.i]=self.medicao[len(self.medicao)-self.i-1]
            self.medicao[len(self.medicao)-self.i-1]=aux
            self.i +=1


        self.comandos.append('medir(' + str(self.medicao) + ')')

    def le_info (self):
        info = self.arq.readline().split() # Armazena a primeira linha

        if (info[0] == 'QASM'): #Se o código for em QASM

            entrada = self.arq.readlines()#lê o arquivo

            for linha in entrada:
                linha = linha.strip()

                if (linha[:4] == 'qreg'): #qbits
                    separador = linha.split('[')
                    numero = separador[1].split(']')
                    numero = numero[0]
                    self.n = numero #número de qbits

                elif (linha[:4] == 'creg') :#bits clássicos
                    separador = linha.split('[')
                    separador= separador[1].split(']')
                    classicos = int (separador[0])

                elif (linha[:7] == 'barrier') : #Barreira
                    pass

                elif (linha[:7] == 'measure'):  # Medir qbits
                    separador = linha.split('[')
                    numero = separador[1].split(']')
                    self.medicao.append (int((numero[0])))

                elif ('*' in linha): #Se for pedido a tradução para outra linguagem
                    self.traduz = True
                    linguagem = linha.split('* ')
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

            medicao='' #salvando a ordem de medida
            for i in range (0,len(self.medicao)):

                if (i!=0):
                    medicao= medicao+','+str(self.medicao[i])
                else:
                    medicao=str(self.medicao[i])

        elif info[0] == 'Qiskit': #se o código for em Qiskit
            inclui=False
            entrada = self.arq.readlines()  # lê o arquivo

            for linha in entrada:
                linha = linha.strip()
                if (linha[:0] != '#'):
                    if (linha[:3] == 'def' or '#' in linha[:1]) : #comentário
                        pass

                    elif ('QuantumRegister' in linha): #qbits quânticos
                        separador = linha.split('(')
                        numero = separador[1].split(',')
                        self.n = numero[0]

                    elif ('ClassicalRegister' in linha): #bits clássicos
                        separador = linha.split('(')
                        separador = separador[1].split(',')
                        classicos = int(separador[0])

                    elif ('measure' in linha):  #medição
                        separador = linha.split('[')
                        numero = separador[1].split(']')
                        self.medicao.append(int(numero[0]))

                    elif ('=' in linha[:5]) : #variáveis
                        variavel= linha.split()
                        valor=variavel[2]

                        for i in range (0,len(variavel)):
                            if variavel[i] != " ":
                                variavel = variavel[i]
                                break
                        try:
                            self.variaveis[variavel]=float(valor)
                        except:
                                pass

                    elif ('for' in linha): #Se tiver for na linha

                        inteiros = re.findall(r'\d+', linha)

                        if (len(inteiros)==1): #Se só houver um inteiro
                            variavel = linha.split('(')
                            variavel=variavel[1].split(')')
                            variavel=variavel[0]

                            try: #Se dentro do parenteses só tiver um inteiro
                                int(variavel)
                                for_inicio=0
                                for_final=variavel

                            except: #Se tiver uma variável e um inteiro
                                variavel=variavel.split(',')
                                for_inicio = variavel[0]
                                for_final = variavel[1]

                                try: #Se o final for a variável
                                    for_final = int(for_final)
                                except:
                                    for a in self.variaveis:
                                        if for_final == a:
                                            for_final = self.variaveis.get(a)
                                            for_final = int(for_final)
                                try: #Se o início for a variável
                                    for_inicio = int(for_inicio)
                                except:
                                    for a in self.variaveis:
                                        if for_inicio == a:
                                            for_inicio = self.variaveis.get(a)
                                            for_inicio = int(for_inicio)

                        elif (len(inteiros)==2): #Se houver os 2 inteiros
                            for_inicio=inteiros[0]
                            for_final=inteiros[1]
                            for_inicio = int(for_inicio)
                            for_final=int(for_final)
                        inclui = True

                    elif (inclui): #entrou no for
                        porta=linha.split('.')
                        porta=porta[1].split('(')
                        inclui=False
                        for a in range (for_inicio,for_final):
                            comando=(porta[0]+'('+str(a) +')')
                            self.comandos.append(comando)

                    elif ('*' in linha): #traduz para alguma outra linguagem
                        self.traduz=True
                        linguagem = linha.split('* ')
                        self.linguagem = linguagem[1]

                    else: #Operação
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



