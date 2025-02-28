import numpy as np
import matplotlib.pyplot as plt
from numpy.typing import NDArray

def plot_functions(x: NDArray[np.float64], y: NDArray[np.float64], yp: NDArray[np.float64], ypp: NDArray[np.float64], 
                  x_inp: float, y_interp: float) -> None:
    '''Строит графики функции, первой и второй производных.'''
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))

    ax1.plot(x, y, 'b-o', label='y(x)')
    ax1.plot(x_inp, y_interp, 'ro')
    ax1.set_title('Значение функции y(x)')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.grid(True)
    ax1.legend()

    ax2.plot(x, yp, 'g-o', label="y'(x)")
    ax2.set_title("Первая производная y'(x)")
    ax2.set_xlabel('x')
    ax2.set_ylabel("y'")
    ax2.grid(True)
    ax2.legend()

    ax3.plot(x, ypp, 'r-o', label="y''(x)")
    ax3.set_title("Вторая производная y''(x)")
    ax3.set_xlabel('x')
    ax3.set_ylabel("y''")
    ax3.grid(True)
    ax3.legend()

    plt.tight_layout()
    plt.show()