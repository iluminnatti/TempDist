import numpy as np
from time import perf_counter
import pickle

#from GetData import GetData
from interface import collect_data
from MeshF import MeshF
from plots import plot_field

#Dados recebidos pelo módulo GetData
#confirms, data, lx, ly, nx, ny, k = GetData()

#Dados recebidos pela interface
collect_data()
f = pickle.load( open("data.npy", 'rb') )
confirms, data, lx, ly, nx, ny, k = f['con'], f['dat'], f['lx'], f['ly'], int(f['nx']), int(f['ny']), f['k']

#Inserção de dados manual
# confirms = ['y', 'n', 'n', 'y']
# data = [(300, 10), (500, 00), (500, 00), (300, 10)]
# lx = 1
# ly = 1
# nx = 20
# ny = 20
# k = 1


#construção da malha
mesh = MeshF(nx-1, ny-1, lx, ly)

nodes = mesh.nodes
borders = mesh.borders

#propriedades do solver iterativo
max_it = 1e3
tol = 0.1

#lida com as condições de fronteira
T_real = np.zeros((2, 4))
C = []
for i in range(0, 4):
    T = data[i][0]
    if(confirms[i] == 'y'):
        hk = data[i][1] * mesh.deltax / k
    elif(confirms[i] == 'n'):
        hk = 0
    T_real[0][i] = T
    T_real[1][i] = hk
    if(i == 0):
        C.append('N')
    elif(i == 1):
        C.append('E')
    elif(i == 2):
        C.append('S')
    elif(i == 3):
        C.append('W')    

#printando as condições de fronteira para facilitar 
# conferência dos resultados
for i in range(0, 4):
    if(confirms[i] == 'y'):
        print(f"Fronteira {i+1} ({C[i]}) convectiva")
    elif(confirms[i] == 'n'):
        print(f"Fronteira {i} ({C[i]}) condutiva")
    print(f'Temperatura: {T_real[0][i]}')
    print(f"Coeficiente de convecção: {data[i][1]}")
print(f'condutividade térmica do condutor: {k}')
print(f'Dimensões do condutor: {ly}X{lx}')
print(f'Dimensão da malha nodal: {ny}X{nx}')

#gera os coefs das equações de balanço de energia para os
#nós convectivos
def boundary2(hk, Tc):
    '''Calcula os termos da equação linear para nós do tipo
    centro da borda convectiva:
    Ap*Tp + Aw*Tw + Ae*Te + An*Tn + bc*Tc = 0
    [ap, aw, ae, an, bc]
    '''
    ap = -2*(hk + 2)
    an = 2
    ae = 1
    aw = 1
    bc = 2*hk*Tc

    a = np.array([ap, aw, ae, an, bc])

    return a

def boundary3(hk, Tc):
    '''Calcula os termos da equação linear para nós do tipo
    quina de duas bordas convectivas:
    Ap*Tp + Aw*Tw + Ae*Te + An*Tn + bc*Tc = 0
    [ap, aw, As, an, bc]
    '''
    ap = -2*(hk + 1)
    an = 0
    As = 1
    aw = 1
    bc = 2*hk*Tc

    a = np.array([ap, aw, As, an, bc])

    return a

#Equação matricial a ser resolvida [A][T] = [B]. 
# Criaremos uma matriz [Tp] = [A][B]

dof = (nx)*(ny)
u_dof = np.ones(dof, dtype=bool) #guarda quais nós tem temperatura já coonhecida, pois está na fronteira condutora (true se não, false se sim)

Temperatures = np.ones(dof)*T_real[0][0] #1° chute
B = np.zeros(dof)
A = np.zeros((dof, dof))

#constroi os coeficiente adequando as condições de contorno
for i, node in enumerate(mesh.borders):
    conv = []
    cond = []
    for j in range(0, 4):
        if(confirms[j] == 'y'):
            conv.append(C[j])
        elif(confirms[j] == 'n'):
            cond.append(C[j])
    
    cont1 = 0
    cont2 = 0
    for a in range(0, len(cond)):
        aux = cond[a]
        if(node[aux] == -1):
            cont1+=1
    for b in range(0, len(conv)):
        aux = conv[b]
        if(node[aux] == -1):
            cont2+=1

    if(cont1 != 0):
        #fronteira condutora

        for key, value in node.items():
            if(node['N'] == -1 and 'N' in cond):
                T_w = T_real[0][0]
            elif(node['E'] == -1 and 'E' in cond):
                T_w = T_real[0][1]
            elif(node['S'] == -1 and 'S' in cond):
                T_w = T_real[0][2]
            elif(node['W'] == -1 and 'W' in cond):
                T_w = T_real[0][3] #dá pra usar for i in cond:
            if (value != -1):
                #se o nó não está em alguma borda (mas algum vizinho está), soma em B a contribuição desse vizinho 
                B[value] += T_w #temperatura da fronteira analisada aqui

        #caso contrário (algum vizinho na borda e o próprio nó na borda), 
        # a temperatura do nó é conhecida, pois é a temperatura da própria borda!
        Temperatures[i] = T_w 
        u_dof[i] = False #registra na matriz booleana que essa temperatura já é conhecida
    elif(cont2 != 0):


        '''[ap, aw, ae, an, bc]
        an = 2
        ae = 1
        aw = 1
        '''
        #segundo caso
        '''[ap, aw, As, an, bc]
        aw = 1
        As = 1
        an = 0
        bp
        '''
        # poss = [0, nx-1, dof-nx, -1]
        if(node['N'] == -1 and 'N' in conv and node['E'] == -1 and 'E' in conv):
            T_d = T_real[0][0]
            h_k = T_real[1][0]
            a = boundary3(hk, T_d)

            A[i, i] = a[0]
            A[i, node['W']] = a[1]
            # A[i, node['E']] = a[2]
            A[i, node['S']] = a[2]

            B[i] += a[4]
        elif(node['E'] == -1 and 'E' in conv and node['S'] == -1 and 'S' in conv):
            T_d = T_real[0][1]
            h_k = T_real[1][1]
            a = boundary3(hk, T_d)

            A[i, i] = a[0]
            A[i, node['W']] = a[1]
            # A[i, node['E']] = a[2]
            A[i, node['N']] = a[2]

            B[i] += a[4]
        elif(node['S'] == -1 and 'S' in conv and node['W'] == -1 and 'W' in conv):
            T_d = T_real[0][2]
            h_k = T_real[1][2]
            a = boundary3(hk, T_d)

            A[i, i] = a[0]
            #A[i, node['W']] = a[1]
            A[i, node['E']] = a[1]
            A[i, node['N']] = a[2]

            B[i] += a[4]
        elif(node['W'] == -1 and 'W' in conv and node['N'] == -1 and 'N' in conv):
            T_d = T_real[0][3]
            h_k = T_real[1][3]
            a = boundary3(hk, T_d)

            A[i, i] = a[0]
            #A[i, node['W']] = a[1]
            A[i, node['E']] = a[1]
            A[i, node['S']] = a[2]

            B[i] += a[4]
        # casos corretos abaixo
        elif(node['N'] == -1 and 'N' in conv):
            T_d = T_real[0][0]
            hk = T_real[1][0]
            a = boundary2(hk, T_d)

            A[i, i] = a[0]
            A[i, node['W']] = a[1]
            A[i, node['E']] = a[2]
            A[i, node['S']] = a[3]

            B[i] += a[4]
        elif(node['E'] == -1 and 'E' in conv):
            T_d = T_real[0][1]
            hk = T_real[1][1]
            a = boundary2(hk, T_d)

            A[i, i] = a[0]
            A[i, node['N']] = a[1]
            A[i, node['S']] = a[2]
            A[i, node['W']] = a[3]

            B[i] += a[4]
        elif(node['S'] == -1) and 'S' in conv:
            T_d = T_real[0][2]
            hk = T_real[1][2]
            a = boundary2(hk, T_d)

            A[i, i] = a[0]
            A[i, node['W']] = a[1]
            A[i, node['E']] = a[2]
            A[i, node['N']] = a[3]

            B[i] += a[4]
        elif(node['W'] == -1 and 'W' in conv):
            T_d = T_real[0][3]
            hk = T_real[1][3]
            a = boundary2(hk, T_d)

            A[i, i] = a[0]
            A[i, node['S']] = a[1]
            A[i, node['N']] = a[2]
            A[i, node['E']] = a[3]

            B[i] += a[4]


    else:
        A[i, i] = -4
        A[i, node['W']] = 1
        A[i, node['E']] = 1
        A[i, node['S']] = 1
        A[i, node['N']] = 1

# Simplifica as equações conforme bc_1
Auu = A[u_dof, :][:, u_dof]
Buu = B[u_dof]
Tuu = Temperatures[u_dof]

# Resolvendo Iterativamente
diff = max(T_real[0])
it = 1

print("Inciando a solução do sistema")
start_time = perf_counter()

while diff >= tol:
    Tuu0 = np.copy(Tuu)

    for i, tp in enumerate(Tuu):

        Bpp = np.append(Buu[:i], Buu[i+1:])

        Tuu[i] = -(np.dot(Auu[i, :i], Tuu[:i])+ np.dot(Auu[i, i+1:], Tuu[i+1:]) + Buu[i]) / Auu[i, i]
    
    diff = np.max(np.abs(Tuu-Tuu0))
    it+=1
    if it > max_it:
        print('Excedido limite de iterações')
        break

end_time = perf_counter()
print(f'Tempo de execução: {end_time - start_time}')
print(f'Número de iterações: {it}')
print(f'Erro: {diff}')
#print(f'Temperatura no centro da face sul: {Tuu[int(np.floor(nx/2))]}')

# Plots
Tplot = np.ones(dof)
for k in range(0, nx):
    Tplot[k] = T_real[0][2]#baixo
for j in range(dof-nx, dof):
    Tplot[j] = T_real[0][0]#cima
for i in range(0, ny):
    Tplot[i*nx] = T_real[0][3]#esquerda
    Tplot[i*nx + nx - 1] = T_real[0][1]#direita
    
    # Tplot[nx-1] = 0.5*(T_real[0][1] + T_real[0][2])
    # Tplot[0] = 0.5*(T_real[0][2] + T_real[0][3])
j = 0

for i, tp in enumerate(u_dof):
    if tp:
        Tplot[i] = Tuu[j]
        j += 1

shading = 'nearest'
plot_field(nx, ny, lx, ly, Tplot)

tmat = open('FigFinal/temps.txt', 'w')

np.savetxt('FigFinal/temps.txt', Tuu, fmt="%.4e", delimiter=" ")
tmat.close()