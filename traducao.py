import re
class traducao:
    def __init__(self,arq,linguagem):
        self.arq = open(arq.nome_arq)
        self.linguagem = linguagem
        self.arquivo = arq
        self.frases=list()
        self.le_info()
        arquivo = open("traducao", "a")

        for i in range (0,len(self.frases)):
            arquivo.write(self.frases[i]+'\n')


    def le_info(self):
        if (self.linguagem == "Quasm"):
            inclui=False

            self.frases.append("OPENQASM 2.0;")
            self.frases.append("include 'qelib1.inc';")
            self.frases.append(" ")
            self.frases.append("qreg q["+str(self.arquivo.n) +'];')
            self.frases.append("creg c[" + str(self.arquivo.n) + '];')
            self.frases.append(" ")

            for i in range (0,len(self.arquivo.comandos)):

                if ('medir' in self.arquivo.comandos[i]):
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