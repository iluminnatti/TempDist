from email import message_from_string
import numpy as np


class MeshF(object):

    def __init__(self, nx, ny, lx, ly):
        '''
        nx = número de nós no eixo x
        ny = número de nós no eixo y
        lx = largura do condutor no eixo x
        ly = largura do condutor no eixo y
        deltax = dimensão em x da região que cada nó representa
        deltay = dimensão em y da região que cada nó representa
        '''
        self.nx = nx
        self.ny = ny
        self.lx = lx
        self.ly = ly
        self.deltax = lx/nx
        self.deltay = ly/ny

        self.nodes = self.map()

    def map(self):
        '''
        Responsável por capturar a coordenada de cada nó e armazenar em um array
        '''
        nx = self.nx
        ny = self.ny
        lx = self.lx
        ly = self.ly 

        x = np.linspace(0, lx, nx+1)#divide o condutor na direção x em nx+1 pontos, contando o 0 e o lx
        y = np.linspace(0, ly, ny+1)#divide o condutor na direção y em ny+1 pontos, contando o 0 e o ly
        grid = np.meshgrid(x, y)
        '''
        A função np.meshgrid() combina todos os elementos de x com os elementos de y, ou seja, gera todos os 
        pares ordenados possíveis (x, y).
        Ela retorna um array de 2 dimensões (2 arrays): 1 (XX) com todos os valores de x de todos os 
        pares ordenados gerados e 1 (yy) com todos os valores de y de todos os pares ordenados gerados. 
        Cada linha de xx é um array que relaciona-se com a respectiva linha de yy, que também são arrays, 
        de modo que temos como resultado todos os pares ordenados gerados.
        '''
        xv = grid[0].ravel()
        yv = grid[1].ravel()
        '''
        A função ravel() basicamente junta todos os arrays em um só. Aqui, pegamos o array grid[0],
        que é um array de nx+1 dimensões, cada dimensão 1 array, e juntamos todos esse arrays em 
        1 único, conservando a ordem (é como se colássemos o início de um na ponta do outro).
        '''
        nodes = np.column_stack((xv, yv))
        '''
        Uma vez que criamos 2 arrays únicos (xv e yv), a função column_stack() basicamente recebe uma tupla
        (xv, yv) e cria um array de 2 colunas, respetivamente as colunas xv e yv. Agora, geramos
        uma matriz de 2 colunas simples, em que cada linha representa um par ordenado que representa
        a coordenada de cada nó.
        '''
        return nodes

    def border(self):
        '''
        Responsável por identificar quem são os nós vizinhos de um determinado nó dado, usando 
        uma nomenclatura baseada em pontos cardeais para identificar cada vizinho ['N', 'S', 'W', 'E'].
        Além disso, identifica também se algum vizinho está em alguma das bordas (considera-se por 'borda'
        qualquer região que esteja tão proximo da borda quanto desejado, dentro de um certo 'erro máximo'), 
        e atribui a esse vizinho o valor -1 para identificar que este encontra-se em uma borda.
             N
             |
        W -- n -- E
             |
             S
        '''
        nx = self.nx
        ny = self.ny
        lx = self.lx
        ly = self.ly 
        deltax = self.deltax
        deltay = self.deltay

        if(deltax < deltay):
            fac = deltax
        else:
            fac = deltay

        error = 1e-6 * fac

        ident = ['W', 'E', 'S', 'N']
        borders = [None] * (nx*ny)
        for i, el in enumerate(self.nodes):
            cord_x = el[0]
            cord_y = el[1]

            border = np.array([i - 1, i + 1, i - nx, i + nx])
            w_bord = abs(cord_x) <= error
            e_bord = abs(cord_x - lx) <= error
            n_bord = abs(cord_y - ly) <= error
            s_bord = abs(cord_y) <= error

            bc = np.array([w_bord, e_bord, s_bord, n_bord])
            border[bc] = -1

            borders[i] = dict(zip(ident, border))
        
        return borders
