import re
#classe traduz para outra linguagem
class traducao:
    def __init__(self,arq,linguagem):
        self.arq = open(arq.nome_arq)
        self.linguagem = linguagem
        self.dic=-1
        self.arquivo = arq
        self.i=0
        self.frases=list()
        self.comandos = [('Program ', 'OPENQASM 2.0;\ninclude "qelib1.inc";\n','def circuit():\n'),
                   (str(self.arquivo.n) +' 100','qreg q[' +str(self.arquivo.n) +'];\ncreg c[' +str(self.arquivo.n)+'];',
                    "q = QuantumRegister(" +str(self.arquivo.n) +"'qubit');\nc = ClassicalRegister("+str(self.arquivo.n) +"'bit')")]

        self.le_info() #lê informações do arquivo
        arquivo = open("traducao", "a")

        arquivo.write(self.comandos[0][self.dic])
        arquivo.write(self.comandos[1][self.dic])
        arquivo.write("\n\n")
        for i in range (0,len(self.frases)): #Escreve as informações
            arquivo.write(self.frases[i]+'\n')

    def le_info(self):
        if (self.linguagem == "QASM"): #Caso esteja em QASM
            self.dic =1

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
            self.dic = 2

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
            self.dic=0

            for i in range (0,len(self.arquivo.comandos)):
                self.frases.append(self.arquivo.comandos[i])

                if (i == len(self.arquivo.comandos)-2): # Último comando é medir, então antes do último, pula linha
                    self.frases.append('')








