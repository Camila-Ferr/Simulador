from math import *
from sympy import I, Matrix, symbols, eye
from sympy.physics.quantum import TensorProduct
from vetor import *


# armazena operadores (gates).
class Operacao:
    def __init__(self, circuito):
        self.circ = circuito
        self.n = circuito.n
        self.N = circuito.N
        self.Estado = circuito.Estado
        self.flag_M = False  # Indica se os operadores aplicados até o momento são vetores ou matrizes
        self.isPerm = False  # indica se a operação atual é uma permutação
        self.V_op = []
        self.M_op = []
        self.test = False

    # indica se deve executar a porta, ou apenas verificar se é uma permutação ou matriz
    def teste(self, t=False):
        if t == 0:
            self.test = t

    #
    ####    Implementação dos operadores (gates)
    #
    #
    #
    # k = bit inicial, t = repetições e theta,phi,lam = ângulos

    ''' Os gates e suas definições podem ser encontrados no site:
        https://quantum-computing.ibm.com/composer/docs/iqx/operations_glossary
    '''

    # define uma permutação
    ## Implementa um operador genérico através da sua permutação
    # P = permutação.
    def perm(self, k, t, P):
        self.isPerm = True
        if self.test:
            return self.isPerm

        nova_perm = []
        for i in range(2 ** self.n):
            n_num = ""
            num = bin(i + 2 ** self.n)[3:]
            n_num += num[:self.n - (k + t)]
            n_num += bin(P[int(num[self.n - (k + t):self.n - k], base=2)] + 2 ** t)[-t:]
            n_num += num[self.n - k:]
            n_num = int(n_num, base=2)

            nova_perm.append(n_num)

        self.V_op = vetor(self.n, nova_perm)

    # x - NOT
    ## inverte o estado do bit
    def x(self, k, t=1):
        self.isPerm = True
        if self.test:
            return self.isPerm
        V = vetor(self.n)

        for j in range(0, t):
            cont = 0
            trava = 0
            # permut = []

            for i in range(int(2 ** (self.n))):
                if cont == 2 ** (k + j):
                    if trava < 2 ** (k + j) - 1:
                        trava += 1
                    else:
                        trava = 0
                        cont = 0
                else:

                    V.P[i], V.P[i + 2 ** (k + j)] = V.P[i + 2 ** (k + j)], V.P[i]
                    cont += 1
        self.V_op = V

    # h - hadamard gate
    def h(self, k, t=1):
        self.isPerm = False
        if self.test:
            return self.isPerm
        op = Matrix([1])
        for i in range(self.n):
            if i >= k and i < k + t:
                had = Matrix([[1, 1], [1, -1]])
                had = had * 2 ** (-0.5)

                op = TensorProduct(op, had)
            else:
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = self.flag_M_atual = True
        self.M_op = op


    # z - Pauli Z gate
    ## Esta porta pode ser associada a um vetor ao em vez de matriz
    def z(self, k, t=1):
        self.isPerm = False
        op = Matrix([1])
        for i in range(self.n):
            if i >= k and i < k + t:
                pz = Matrix([[1, 0], [0, -1]])
                op = TensorProduct(op, pz)
            else:
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

    # s - S gate
    def s(self, k, t=1):
        self.isPerm = False
        op = Matrix([1])
        for i in range(self.n):
            if i >= k and i < k + t:
                ps = Matrix([[1, 0], [0, I]])
                op = TensorProduct(op, ps)
            else:
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

    # sdg - gate usado no algoritmo de Shor
    def sdg(self, k, t=1):
        self.isPerm = False
        op = Matrix([1])
        for i in range(self.n):
            if i >= k and i < k + t:
                ps = Matrix([[1, 0], [0, -I]])
                op = TensorProduct(op, ps)
            else:
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

    # y - Pauli Y gate
    def y(self, k, t=1, test=False):
        self.isPerm = False
        if self.test:
            return self.isPerm
        op = Matrix([1])
        for i in range(self.n):
            if i >= k and i < k + t:
                py = Matrix([[0, -I], [I, 0]])
                op = TensorProduct(op, py)
            else:
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

    # t - T gate
    def t(self, k, t=1, test=False):
        self.isPerm = False
        if self.test:
            return self.isPerm
        op = Matrix([1])
        for i in range(self.n):
            if i >= k and i < k + t:
                pt = Matrix([[1, 0], [0, e ** (I * pi / 4)]])
                op = TensorProduct(op, pt)
            else:
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

    # tdg - T-dagger gate
    def tdg(self, k, t=1):
        self.isPerm = False
        if self.test:
            return self.isPerm
        op = Matrix([1])
        for i in range(self.n):
            if i >= k and i < k + t:
                pt = Matrix([[1, 0], [0, e ** (-I * pi / 4)]])
                op = TensorProduct(op, pt)
            else:
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

    # u3 - U gate
    ## Esse gate consegue gerar qualquer gate de 1 bit.
    def u3(self, theta, phi, lam, k, t=1):
        op = Matrix([1])
        for i in range(self.n):
            if i >= k and i < k + t:
                pt = Matrix([[cos(theta / 2), -e ** (I * lam) * sin(theta / 2)],
                             [e ** (I * phi) * sin(theta / 2), e ** (I * (phi + lam)) * cos(theta / 2)]])
                op = TensorProduct(op, pt)
            else:
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

    # u2 - U2 gate
    def u2(self, phi, lam, k, t=1):
        op = Matrix([1])
        for i in range(self.n):
            if i >= k and i < k + t:
                pt = Matrix([[1, -e ** (I * lam)], [e ** (I * phi), e ** (I * (phi + lam))]])
                op = TensorProduct(op, pt)
            else:
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

    # u1 - U1 gate
    def u1(self, lam, k, t=1):
        op = Matrix([1])
        for i in range(self.n):
            if i >= k and i < k + t:
                pt = Matrix([[1, 0], [0, e ** (I * lam)]])
                op = TensorProduct(op, pt)
            else:
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

    # rx - RX gate
    def rx(self, theta, k, t=1):
        op = Matrix([1])
        for i in range(self.n):
            if i >= k and i < k + t:
                pt = Matrix([[cos(theta / 2), -I * sin(theta / 2)], [-I * sin(theta / 2), cos(theta / 2)]])
                op = TensorProduct(op, pt)
            else:
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

        # ry - RY gate

    def ry(self, theta, k, t=1):
        op = Matrix([1])
        for i in range(self.n):
            if i >= k and i < k + t:
                pt = Matrix([[cos(theta / 2), -sin(theta / 2)], [sin(theta / 2), cos(theta / 2)]])
                op = TensorProduct(op, pt)
            else:
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

        # rz - RZ gate

    def rz(self, theta, k, t=1):
        op = Matrix([1])
        for i in range(self.n):
            if i >= k and i < k + t:
                pt = Matrix([[e ** (-I * (theta / 2)), 0], [0, e ** (I * (theta / 2))]])
                op = TensorProduct(op, pt)
            else:
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

        #

    ##gates com 2 bits.
    #

    # cx - CNOT gate
    ## veri = dígito verificador, target = bit alvo
    def cx(self, veri, target):
        self.isPerm = True
        if self.test:
            return self.isPerm
        V = vetor(self.n)

        for i in range(2 ** self.n):
            i_bit = list(bin(2 ** self.n + i)[3:])

            resp = ''
            if i_bit[self.n - 1 - veri] == '1':
                for j in range(self.n):
                    if j == (self.n - 1 - target):
                        resp += str((int(i_bit[j]) + 1) % 2)
                    else:
                        resp += i_bit[j]
                V.P[i] = int(resp, base=2)
            else:
                V.P[i] = i

        self.V_op = V

    # ch - Controlled Hadamard
    def ch(self, k):
        self.isPerm = False
        if self.test:
            return self.isPerm
        op = Matrix([1])
        for i in range(self.n):
            if i == k:
                control_z = Matrix(
                    [[1, 0, 0, 0], [0, 2 ** (-0.5), 0, 2 ** (-0.5)], [0, 0, 1, 0], [0, 2 ** (-0.5), 0, -2 ** (0.5)]])
                op = TensorProduct(op, control_z)
            elif i != (k + 1):
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

        # cy - Controlled Y gate

    def cy(self, k):
        self.isPerm = False
        if self.test:
            return self.isPerm
        op = Matrix([1])
        for i in range(self.n):
            if i == k:
                control_z = Matrix([[1, 0, 0, 0], [0, 0, 0, -I], [0, 0, 1, 0], [0, I, 0, 0]])
                op = TensorProduct(op, control_z)
            elif i != (k + 1):
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

    # cz - Controlled Z gate
    def cz(self, k):
        self.isPerm = False
        if self.test:
            return self.isPerm
        op = Matrix([1])
        for i in range(self.n):
            if i == k:
                control_z = Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])
                op = TensorProduct(op, control_z)
            elif i != (k + 1):
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

    # cs - Controlled S gate
    def cs(self, k):
        self.isPerm = False
        if self.test:
            return self.isPerm
        op = Matrix([1])
        for i in range(self.n):
            if i == k:
                cphase = Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, I]])
                op = TensorProduct(op, cphase)
            elif i != (k + 1):
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

    # crx - Controlled RX gate
    def crx(self, theta, k):
        self.isPerm = False
        if self.test:
            return self.isPerm
        op = Matrix([1])
        for i in range(self.n):
            if i == k:
                control_z = Matrix([[1, 0, 0, 0], [0, cos(theta / 2), 0, -I * sin(theta / 2)], [0, 0, 1, 0],
                                    [0, -I * sin(theta / 2), 0, cos(theta / 2)]])
                op = TensorProduct(op, control_z)
            elif i != (k + 1):
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

    # cry - Controlled RY gate
    def cry(self, theta, k):
        self.isPerm = False
        if self.test:
            return self.isPerm
        op = Matrix([1])
        for i in range(self.n):
            if i == k:
                control_z = Matrix([[1, 0, 0, 0], [0, cos(theta / 2), 0, -sin(theta / 2)], [0, 0, 1, 0],
                                    [0, sin(theta / 2), 0, cos(theta / 2)]])
                op = TensorProduct(op, control_z)
            elif i != (k + 1):
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

    # crz - Controlled RZ gate
    def crz(self, theta, k):
        self.isPerm = False
        if self.test:
            return self.isPerm
        op = Matrix([1])
        for i in range(self.n):
            if i == k:
                control_z = Matrix(
                    [[1, 0, 0, 0], [0, e ** (-I * (theta / 2)), 0, 0], [0, 0, 1, 0], [0, 0, 0, e ** (I * (theta / 2))]])
                op = TensorProduct(op, control_z)
            elif i != (k + 1):
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

        # cu1 - Controlled U1 gate

    def cu1(self, theta, k):
        self.isPerm = False
        if self.test:
            return self.isPerm
        op = Matrix([1])
        for i in range(self.n):
            if i == k:
                control_z = Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, e ** (I * (theta))]])
                op = TensorProduct(op, control_z)
            elif i != (k + 1):
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

        # cu3 - Controlled U3 gate

    def cu3(self, theta, phi, lam, k):
        self.isPerm = False
        if self.test:
            return self.isPerm
        op = Matrix([1])
        for i in range(self.n):
            if i == k:
                control_z = Matrix(
                    [[1, 0, 0, 0], [0, cos(theta / 2), 0, -e ** (I * lam) * sin(theta / 2)], [0, 0, 1, 0],
                     [0, e ** (I * phi) * sin(theta), 0, e ** (I * (phi + lam) * cos(theta / 2))]])
                op = TensorProduct(op, control_z)
            elif i != (k + 1):
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

    # swap - Swap gate
    ## Troca os estados de 2 bits
    ## bit1 = primeiro bit, bit2 = segundo bit. (a ordem não importa)
    def swap(self, bit1, bit2):
        self.isPerm = True
        if self.test:
            return self.isPerm
        V = vetor(self.n)

        for i in range(2 ** self.n):
            i_bit = list(bin(2 ** self.n + i)[3:])

            resp = ''
            for j in range(self.n):
                if j == (self.n - 1 - bit1):
                    resp += i_bit[self.n - 1 - bit2]
                elif j == (self.n - 1 - bit2):
                    resp += i_bit[self.n - 1 - bit1]
                else:
                    resp += i_bit[j]
            V.P[i] = int(resp, base=2)

        self.V_op = V

    # rxx - RXX gate
    def rxx(self, theta, k):
        self.isPerm = False
        if self.test:
            return self.isPerm
        op = Matrix([1])
        for i in range(self.n):
            if i == k:
                control_z = Matrix(
                    [[cos(theta / 2), 0, 0, -I * sin(theta / 2)], [0, cos(theta / 2), -I * sin(theta / 2), 0],
                     [0, -I * sin(theta / 2), cos(theta / 2), 0], [-I * sin(theta / 2), 0, 0, cos(theta / 2)]])
                op = TensorProduct(op, control_z)
            elif i != (k + 1):
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

    # czz - Controlled ZZ gate
    def czz(self, theta, k):
        self.isPerm = False
        if self.test:
            return self.isPerm
        op = Matrix([1])
        for i in range(self.n):
            if i == k:
                control_z = Matrix([[e ** (-I * (theta / 2)), 0, 0, 0], [0, e ** (I * (theta / 2)), 0, 0],
                                    [0, 0, e ** (I * (theta / 2)), 0], [0, 0, 0, e ** (-I * (theta / 2))]])
                op = TensorProduct(op, control_z)
            elif i != (k + 1):
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

    # cfs - Condicional Phase Shift
    def cfs(self, k, t):
        self.isPerm = False
        if self.test:
            return self.isPerm

        op = Matrix([1])
        for i in range(self.n):
            if i == k:
                num = e ** ((pi * 2 * I / 2 ** t))
                phase_shift = Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, num]])
                op = TensorProduct(op, phase_shift)
            elif i != (k + 1):
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op

    #
    ## gates com 3 bits.
    #

    # ccx - Toffoli gate
    ## veri1 e veri2 = dígitos verificadores, target = bit alvo
    def ccx(self, veri1, veri2, target):
        self.isPerm = True
        if self.test:
            return self.isPerm
        V = vetor(self.n)

        for i in range(2 ** self.n):
            i_bit = list(bin(2 ** self.n + i)[3:])

            resp = ''
            if i_bit[self.n - 1 - veri1] == '1' and i_bit[self.n - 1 - veri2] == '1':
                for j in range(self.n):
                    if j == (self.n - 1 - target):
                        resp += str((int(i_bit[j]) + 1) % 2)
                    else:
                        resp += i_bit[j]
                V.P[i] = int(resp, base=2)
            else:
                V.P[i] = i

        self.V_op = V

    # cswap - Controlled Swap gate
    def cswap(self, veri1,veri2,veri3):
        self.isPerm = True
        if self.test:
            return self.isPerm

        V = vetor(self.n)

        for i in range(2 ** self.n):
            i_bit = list(bin(2 ** self.n + i)[3:])

            resp = ''
            if (i_bit[self.n - 1 - veri1] == '1') and (i_bit[self.n - 1 - veri2] != i_bit[self.n - 1 - veri3]):
                    for j in range(self.n):
                        if (j == (self.n - 1 - veri3)) or (j==(self.n-1-veri2)):
                            resp += str((int(i_bit[j]) + 1) % 2)
                        else:
                            resp += i_bit[j]
                    V.P[i] = int(resp, base=2)
            else:
                V.P[i] = i

            self.V_op = V

    # gen_op - Operador genérico
    ## Implementa qualquer gate através da dua matriz
    ## q_bits = quantidade de bits do gate, matriz = matriz
    def gen_op(self, k, q_bits, matriz):
        self.isPerm = False
        if self.test:
            return self.isPerm
        op = Matrix([1])
        for i in range(self.n):
            if i == k:
                op = TensorProduct(op, Matrix(matriz))
            elif i < k or i > (k + q_bits - 1):
                op = TensorProduct(op, Matrix([[1, 0], [0, 1]]))

        self.flag_M = True
        self.M_op = op