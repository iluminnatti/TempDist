import matplotlib.pyplot as plt
import numpy as np

def plot_field(nx, ny, lx, ly, values):
    '''Faz o plot utilizando-se dos dados da matriz final obtida'''

    x = np.linspace(0, lx, nx+1)
    y = np.linspace(0, ly, ny+1)
    x, y = np.meshgrid(x, y)

    z = values.reshape((nx, ny))
    z_min, z_max = np.abs(z).min(), np.abs(z).max()

    fig, ax = plt.subplots()

    c = ax.pcolormesh(x, y, z, cmap='coolwarm', vmin=z_min, vmax=z_max)
    ax.set_title('Distribuição de temperaturas do sistema')

    #define os limites dos dados como os limites do plot

    ax.axis([x.min(), x.max(), y.min(), y.max()])
    fig.colorbar(c, ax=ax)
    plt.savefig("./FigFinal/TempDist.png", bbox_inches='tight')

    plt.show()