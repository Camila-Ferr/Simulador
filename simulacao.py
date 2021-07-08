from random import randint,random
from arquivo import *
from operacao import *

## armazena informações sobre cada simulação
class simulacao:
    def __init__ (self,n,m=0,nome_arq=""):
        if nome_arq !="":
            self.arq = arquivo(nome_arq)
            self.n = self.arq.n          # quantidade de qbits
            self.vezes = self.arq.vezes  # quantidade de vezes que será feita a medição
        else:
            self.n = n
            self.vezes = -1
        self.N = 1 << self.n     # tamanho de estados
        ## cria vetor estado atual e coloca o estado inicial em |0>
        self.Estado = [0]*self.N
        self.Estado[0] = 1
        self.Estado = Matrix(self.Estado)
        self.cbits = [0]*m      # cria um vetor de bits clássicos
        self.M_op = []          # matriz referente ao conjunto de operações unitárias
        self.is_Estado = not self.arq.matrix   # Flag para decidir se a medição será operador ou estado.
        self.op_atual = Operacao(self)
        self.medicao = self.arq.medicao

        if nome_arq != "" and self.medicao==[]:
            self.medicao = "self."+ self.arq.comandos[-1]
        else: #Se for um código em outra linguagem de programação
            medir='self.medir(['
            for i in range (0,len(self.medicao)):
                medir+=str(self.medicao[i])
                if len(self.medicao)-i >1:
                    medir+=','
            medir+='])'
            self.medicao=medir
        self.arq.comandos.pop()
        self.executa(self.arq.comandos,self.arq.variaveis,self.arq.funcoes)
        eval(self.medicao)

        
    

    # execução de uma lista de operadores a partir de um arquivo
    def executa(self,comandos,variaveis,funcoes):
        self.L_isPerm = []
        ## passa pelos comandos apenas para verificar quais estão associados a permutações
        ## uma otimização possível é aplicar todas as permutações vizinhas e depois aplicar as matrizes (a fazer)
        # self.op_atual.teste(True)
        # for x in comandos:
        #     comando = "self.op_atual."+x
        #     eval(comando)
        #     self.L_isPerm.append(self.op_atual.isPerm)

        # print(self.L_isPerm)    # mostra quais operadores são permutações.
        if not self.is_Estado:    # Cria uma matriz identidade de ordem 2**n caso a saída seja uma matrix
            self.M_op = eye(2**(self.n))  
        self.op_atual.teste(False)
        for x in comandos:
            comando = "self.op_atual."+x
            try:
                eval(comando)
            except:
                nome_func = comando.split("(")[0].split('.')[-1]                
                func_atual = ''
                is_func = False
                #busca para saber se o comando é uma função.
                for func in funcoes:
                    if nome_func == func.nome:
                        func_atual = func
                        valores_func = comando.split("(")[1].split(',')
                        valores_func[-1] = valores_func[-1][:-1]
                        is_func = True
                        break
                if not is_func:
                    # Substitui as variáveis pelo seu valor.
                    for variavel in variaveis:
                        if variavel in comando:
                            comando = comando.replace(variavel,str(variaveis[variavel]))
                    eval(comando)
                else:
                    # roda a função
                    for x in func_atual.codigo:
                        comando = "self.op_atual."+x
                        try:
                            eval(comando)
                        except:
                            for variavel in func_atual.variaveis:
                                if variavel in comando:
                                    comando = comando.replace(variavel,str(valores_func[func_atual.variaveis.index(variavel)]))
                            eval(comando)
            # para simplificar, por enquanto todos os operadores são tratados como matriz
            if self.is_Estado:
                if self.op_atual.isPerm:
                    self.perm(self.op_atual.V_op.P)
                else:
                    self.Estado =  self.op_atual.M_op * self.Estado 
            else:
                if self.op_atual.isPerm:
                    self.perm_m(self.op_atual.V_op.P)
                else:
                    self.M_op = self.op_atual.M_op * self.M_op
    
    def perm(self,permut): # simula as permutações para gerar vetor de estados
        permutacao = [None]*2**self.n
        temp = []
        
        for i in range(len(permut)):
            permutacao[int(self.tratar_perm(i),base = 2)] = int(self.tratar_perm(permut[i]), base = 2)
        
        for i in range(len(permut)):
            k = [self.Estado[permutacao[i]]] 
            temp = temp + k 
        matriz = Matrix(temp)
        self.Estado = matriz
    
    def perm_m(self,permut):# Simula a permutação para gerar operador
        
        operador = []
        for i in range(2**self.n):
            linha = []
            for j in range(2**self.n):
                linha.append(self.M_op[i*2**self.n + j])
            operador.append(linha)
        
        permutacao = [None]*2**self.n
        temp = []
        
        for i in range(len(permut)):
            permutacao[int(self.tratar_perm(i),base = 2)] = int(self.tratar_perm(permut[i]), base = 2)
        
        for i in range(len(permut)):
            k = [operador[permutacao[i]]] 
            temp = temp + k 
        matriz = Matrix(temp)
        self.M_op = matriz

            
    
    ## aplica a seq. de operadores no estado atual
    def aplica_op(self):
        if self.M_op != []:
            self.Estado = self.M_op *self.Estado

    def cria_soma(self):
        prob = []
        
        for x in self.Estado:
                num = x.as_real_imag()
                num_f = (num[0]**2 + num[1]**2)
                prob.append(num_f)                
        
        soma=[None]*self.N
        soma[0]=prob[0]
        for i in range(1,self.N):
            soma[i]= soma[i-1]+prob[i]
        
        return soma    

    # Rodar.
    def medir(self,ordem):
        self.cbits = ordem

    def tratar(self,k):#
        temp = bin(2**self.n + k)[3:]
        #temp = temp[::-1]
        num = ''
        for i in self.cbits:
            num = num + temp[i]
        return num

    def tratar_perm(self,k):#
        temp = bin(2**self.n + k)[3:]
        return temp[::-1]

    def simular(self):
        if self.is_Estado:
            resultado = {}
            soma = self.cria_soma()
            size = 2**len(self.cbits)
            r = [0]*size
            for _ in range(self.vezes):
                p = random()
                
                # busca binária
                inicio=0
                fim = self.N-1
                sai = False
                while fim>=inicio and not sai:
                    k=(inicio+fim)//2
                    if p < soma[k]:
                        if p> soma[k-1]:
                            sai=True
                        fim = k-1
                    else :
                        inicio = k + 1
                if self.tratar(k) in resultado:
                    resultado[self.tratar(k)] += 1
                else:
                    resultado[self.tratar(k)] = 1
                
                r[int(str(self.tratar(k)),base = 2)] +=1
            
            
            print(resultado)
            print(r)
        else:
            print(self.M_op)
