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

    