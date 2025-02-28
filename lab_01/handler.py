from sys import exit
import numpy as np
from numpy.typing import NDArray

from iops import read_data
from ui import print_table
from interp import newton_interp, hermite_interp, invert_derivs, solve_system
from visual import plot_functions

def process_choice(choice: int) -> None:
    match choice:
        case 1:
            process_newton()
        case 2:
            process_hermit()
        case 3: 
            process_comparison()
        case 4:
            process_find_root()
        case 5:
            process_solve_system()
        case 0:
            process_exit()
            
def process_newton() -> None:
    x, y = read_data('newton')
    max_deg = len(x)
    n: int = int(input(f'Введите степень полинома Ньютона (<= {max_deg}): '))
    
    if (n > max_deg):
        print('Введена слишком большая степень полинома!')
        exit(1)
    
    x_inp: float = float(input('Введите x для интерполяции: '))
    
    print_table(x, y)
    res = newton_interp(x, y, x_inp, n)
    
    print(f'y({x_inp}) = {res:.6f}')
    print('-' * 44)
    # plot_functions(x, y, yp, ypp, x_inp, res)
    
    
def process_hermit() -> None:
    x, y, yp, ypp = read_data('hermite')
    max_deg = len(x)
    n: int = int(input(f'Введите количество узлов полинома Эрмита (<= {max_deg}): '))
    
    if (n > max_deg):
        print('Введено слишком большое количество узлов!')
        exit(1)
        
    x_inp: float = float(input('Введите x для интерполяции: '))

    print_table(x, y, yp, ypp)
    res = hermite_interp(x, y, yp, ypp, x_inp, n)
    
    print(f'y({x_inp}) = {res:.6f}')
    print('-' * 76)
    plot_functions(x, y, yp, ypp, x_inp, res)

def process_comparison() -> None:
    x, y, yp, ypp = read_data('hermite')
    max_deg = len(x)
    n: int = int(input(f'Введите количество узлов полинома Эрмита (степень полинома Ньютона) для сравнения (<= {max_deg}): '))
    
    if (n > max_deg):
        print('Введено слишком большое количество узлов!')
        exit(1)
        
    x_inp: float = float(input('Введите x для сравнения: '))
    
    print('-' * 44)
    print(f'|{"Степень":^10}|{"Ньютон":^15}|{"Эрмит":^15}|')
    print('-' * 44)
    for i in range(1, n + 1):
        res_newton = newton_interp(x, y, x_inp, i)
        res_hermite = hermite_interp(x, y, yp, ypp, x_inp, i)
        print(f'|{i:^10}|{res_newton:^15.6f}|{res_hermite:^15.6f}|')
    print('-' * 44)

def process_find_root() -> None:
    x, y, yp, ypp = read_data('hermite')
    
    rev_yp, rev_ypp = invert_derivs(yp, ypp)
    y = y[1:6]
    x = x[1:6]
    rev_yp = rev_yp[1:6]
    rev_ypp = rev_ypp[1:6]
    
    y_indices = np.argsort(y)
    y = y[y_indices]
    x = x[y_indices]
    rev_yp = rev_yp[y_indices]
    rev_ypp = rev_ypp[y_indices]
        
    print_table(y, x, rev_yp, rev_ypp)

    max_deg = len(y)
    n: int = int(input(f'Введите количество узлов полинома Эрмита (степень полинома Ньютона) (<= {max_deg}): '))
    
    if (n > max_deg):
        print('Введено слишком большое количество узлов!')
        exit(1)
    
    root_newton = newton_interp(y, x, 0.0, n)
    root_hermite = hermite_interp(y, x, rev_yp, rev_ypp, 0.0, n);
        
    print(f'Корень функции при интерполяции полиномом Ньютона: {root_newton:.6f}')
    print(f'Корень функции при интерполяции полиномом Эрмита: {root_hermite:.6f}')

    # plot_functions(y, x, rev_yp, rev_ypp, 0, root_hermite)

def process_solve_system() -> None:
    x1, y1 = read_data('newton')
    x2, y2 = read_data('newton')

    max_deg = min(len(x1), len(x2))
    n: int = int(input(f'Введите количество узлов полинома Эрмита (степень полинома Ньютона) (<= {max_deg}): '))
    
    if (n > max_deg):
        print('Введено слишком большое количество узлов!')
        exit(1)
        
    x, y = solve_system(y1, x1, x2, y2, n)
    print(f'Решение системы: ({x:.6f}; {y:.6f})')

def process_exit() -> None:
    exit(1)