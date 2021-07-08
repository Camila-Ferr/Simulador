## vetor para indicar troca de estados (permutação) ou mudanças locais de amplitude (fase, sinal,... da amplitude)
# obs. por enquanto tenta implementar apenas permutações
from math import log2

from sympy import Matrix


class vetor:
    def __init__(self,n=3,P=[]):
        self.n = n
        self.N = 1 << n
        if P != []:
            self.P = P
            if len(P) > self.N : # A quantidade de elementos na permutação deve ser menor ou igual a que N
                self.n = round(log2(len(P)))+1
                self.N = 1 << n
            ## completa o que falta na permutação
            for i in range(len(P),self.N):
                self.P.append(i)
        else :
            self.P = self.Id()
        self.isPerm = True     # indica se o vetor é uma permutação
        self.Mat    = []       # matriz equivalente à permutação da identidade (só monta se necessário)


    ## cria e retorna uma permutação identidade de tamanho N
    def Id(self,N=0):
        P = []
        if not N :  # se N =0
            N = self.N
        for i in range(N):
            P.append(i)
        return P

    ## retorna a composição de permutações
    def perm(self,P1=[]):
        i = 0
        P_nova = []
        for i in range(self.N):
            P_nova.append(P1[self.P[i]])
        return P_nova

    ## cria matriz a partir da permutação
    def perm2mat(self):
        if self.Mat ==[]:
            # preenche a Matriz com 0's
            for i in range(self.N):
                self.Mat.append([0]*self.N)
        for i in range(self.N):
            self.Mat[i][self.P[i]] = 1
        self.Mat = Matrix(self.Mat)
        return self.Mat

    ## mostra o vetor
    def mostraV(self):
        print(self.P)

    ## mostra a Matriz
    def mostraM(self):
        for x in self.Mat:
            print(x)

    # converte um inteiro numa sequência binária em ordem inversa
    # obs. Não usado
    def dec2lista(self,k):
        num = bin(self.N + k)[3:]    # converte o número para binário
        num = list(num)[::-1]
        num = list(map(int,num))
        return num