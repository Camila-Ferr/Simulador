import re
class traducao:
    def __init__(self,arq,linguagem,medicao):
        self.arq = open(arq.nome_arq)
        self.linguagem = linguagem
        self.arquivo = arq
        self.medicao = medicao
        self.aplica=True
        self.frases=list()
        self.le_info()
        arquivo = open("traducao", "a")

        for i in range (0,len(self.frases)):
            arquivo.write(self.frases[i]+'\n')


    def le_info(self):
        if (self.linguagem == "QASM"):

            self.frases.append("OPENQASM 2.0;")
            self.frases.append("include 'qelib1.inc';")
            self.frases.append(" ")
            self.frases.append("qreg q["+str(self.arquivo.n) +'];')
            self.frases.append("creg c[" + str(self.arquivo.n) + '];')
            self.frases.append(" ")

            for i in range (0,len(self.arquivo.comandos)):
                if ('medir' in self.arquivo.comandos[i]):
                    self.aplica=False

                    valores = re.findall(r'\d+', self.arquivo.comandos[i])

                    for j in range (0,len(valores)):
                        self.frases.append('measure q[' +str(valores[j]) +'] -> c[' +str(valores[j])+'];')

                else:
                    comando =self.arquivo.comandos[i].replace('(',' q[')
                    comando= comando.replace(')', ']')
                    try:
                        comando=comando.replace(',','],q[')
                    except:
                        pass
                    self.frases.append(comando +";")
            if (self.aplica):
                for i in range (0,len(self.medicao)):
                    self.frases.append("measure q["+str(self.medicao[i]) +"]-> c["+str(self.medicao[i])+"];")

        elif (self.linguagem == "Qiskit"):
            self.frases.append('def circuit():')
            self.frases.append("q = QuantumRegister(" +str(self.arquivo.n) +", 'qubit')")
            self.frases.append("c = ClassicalRegister(" +str(self.arquivo.n) +", 'bit')")
            self.frases.append("cir = QuantumCircuit(q, c)")
            self.frases.append(" ")

            for i in range (0,len(self.arquivo.comandos)):

                if ('medir' in self.arquivo.comandos[i]):
                    self.aplica = False
                    self.frases.append(" ")
                    valores = re.findall(r'\d+', self.arquivo.comandos[i])

                    for j in range (0,len(valores)):
                        self.frases.append('cir.measure(q[' +valores[j] +'], c[' +valores[j] +'])')

                else:
                    comando= self.arquivo.comandos[i].replace('(', '(q[')
                    comando=comando.replace(')', ']')
                    try:
                        comando=comando.replace(',','],q[')
                    except:
                        pass

                    if (comando[:2]!="(q"):
                        self.frases.append("cir."+comando +")")
            self.frases.append(' ')
            if (self.aplica):
                for j in range(0, len(self.medicao)):
                    self.frases.append('cir.measure(q[' + str(self.medicao[j]) + '], c[' + str(self.medicao[j]) + '])')
                self.frases.append('')
            self.frases.append("return cir")






