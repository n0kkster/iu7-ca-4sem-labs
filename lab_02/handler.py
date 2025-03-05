from sys import exit

from iops import read_data
from interp import interp_newton_3d, interp_spline_3d

def process_choice(choice: int):
    match choice:
        case 1:
            process_newton()
        case 2:
            process_spline()
        case 0:
            process_exit()

def process_newton():
    filename: str = input('Введите имя файла: ')
    body = read_data(filename)

    max_deg_z = len(body) - 1
    max_deg_y = len(body[0]) - 1
    max_deg_x = len(body[0][0]) - 1

    nx, ny, nz = map(int, input(f'Введите степени полинома Ньютона nx <= {max_deg_x}, ny <= {max_deg_y}, nz <= {max_deg_z}: ').split())
    
    if (nx > max_deg_x or ny > max_deg_y or nz > max_deg_z):
        print('Введена слишком большая степень полинома!')
        exit(1)
    
    x, y, z = map(float, input('Введите x, y, z для интерполяции: ').split())
    res = interp_newton_3d(body, x, y, z, nx, ny, nz)
    print(res)

def process_spline():
    filename: str = input('Введите имя файла: ')
    body = read_data(filename)
    
    x, y, z = map(float, input('Введите x, y, z для интерполяции: ').split())
    res = interp_spline_3d(body, x, y, z)
    print(res)

def process_exit():
    exit(1)