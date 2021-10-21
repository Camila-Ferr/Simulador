import re
#classe traduz para outra linguagem
class traducao:
    def __init__(self,arq,linguagem):
        self.arq = open(arq.nome_arq)
        self.linguagem = linguagem
        self.arquivo = arq
        self.i=0
        self.frases=list()

        self.le_info() #lê informações do arquivo
        arquivo = open("traducao", "a")

        for i in range (0,len(self.frases)): #Escreve as informações
            arquivo.write(self.frases[i]+'\n')

    def le_info(self):
        if (self.linguagem == "QASM"): #Caso esteja em QASM

            self.frases.append("qreg q["+str(self.arquivo.n) +'];') #número de bits quanticos
            self.frases.append("creg c[" + str(self.arquivo.n) + '];') # número de bits clássicos
            self.frases.append(" ")

            for i in range (0,len(self.arquivo.comandos)):
                if ('medir' in self.arquivo.comandos[i]): #Se for para medir
                    self.aplica=False

                    valores = re.findall(r'\d+', self.arquivo.comandos[i])
                    for j in range (0,len(valores)):
                        self.frases.append('measure q[' +str(valores[len(valores)-j-1]) +'] -> c[' +str(valores[len(valores)-j-1])+'];')
                else: #Caso seja uma operação
                    comando =self.arquivo.comandos[i].replace('(',' q[')
                    comando= comando.replace(')', ']')
                    try:
                        comando=comando.replace(',','],q[')
                    except:
                        pass
                    self.frases.append(comando +";")

        elif (self.linguagem == "Qiskit"): #Caso o tradutor seja para Qiskit
            self.frases.append('def circuit():')
            self.frases.append("q = QuantumRegister(" +str(self.arquivo.n) +", 'qubit')") #qbits
            self.frases.append("c = ClassicalRegister(" +str(self.arquivo.n) +", 'bit')") #bits clássicos
            self.frases.append("cir = QuantumCircuit(q, c)") #circuito
            self.frases.append(" ")

            for i in range (0,len(self.arquivo.comandos)):

                if ('medir' in self.arquivo.comandos[i]): #Se for para medir
                    self.aplica = False
                    self.frases.append(" ")
                    valores = re.findall(r'\d+', self.arquivo.comandos[i])

                    for j in range (0,len(valores)):
                        self.frases.append('cir.measure(q[' +valores[len(valores)-j-1] +'], c[' +valores[len(valores)-j-1] +'])')

                else: #Caso seja comando
                    comando= self.arquivo.comandos[i].replace('(', '(q[')
                    comando=comando.replace(')', ']')
                    try:
                        comando=comando.replace(',','],q[')
                    except:
                        pass

                    if (comando[:2]!="(q"):
                        self.frases.append("cir."+comando +")")
            self.frases.append(' ')

        elif (self.linguagem == 'self'): #Se for pedido a tradução para a linguagem do simulador
            self.frases.append("Program " +str(self.arquivo.n) +" " +str(self.arquivo.vezes))
            self.frases.append(' ')

            for i in range (0,len(self.arquivo.comandos)):
                self.frases.append(self.arquivo.comandos[i])

                if (i == len(self.arquivo.comandos)-2): # Último comando é medir, então antes do último, pula linha
                    self.frases.append('')








