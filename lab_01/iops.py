from sys import exit
import numpy as np
from numpy.typing import NDArray
from typing import Tuple

def read_data_hermite(filename: str) -> Tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    x: list[float] = []
    y: list[float] = []
    yp: list[float] = []
    ypp: list[float] = []
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                parts = line.split()
                if len(parts) == 4:
                    x.append(float(parts[0]))
                    y.append(float(parts[1]))
                    yp.append(float(parts[2]))
                    ypp.append(float(parts[3]))
                else:
                    print('Некорректная структура файла!')
                    exit(1)
    except FileNotFoundError:
        print('Указанный файл не найден!')
        exit(1)

    return np.array(x), np.array(y), np.array(yp), np.array(ypp)

def read_data_newton(filename: str) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
    x: list[float] = []
    y: list[float] = []
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 2:
                    x.append(float(parts[0]))
                    y.append(float(parts[1]))
                else:
                    print('Некорректная структура файла!')
                    exit(1)
    except FileNotFoundError:
        print('Указанный файл не найден!')
        exit(1)

    return np.array(x), np.array(y)

def read_data(forwhat: str) -> Tuple:
    filename: str = input('Введите имя файла: ')
    match forwhat:
        case 'newton':
            read = read_data_newton(filename)
        case 'hermite':
            read = read_data_hermite(filename)
        case _:
            print('???')
            exit(1)
            
    read = my_sort(read)
    return read
            
    
def my_sort(data: tuple) -> Tuple:
    sort_indices = np.argsort(data[0])
    data = list(data)
    for i in range(len(data)):
        data[i] = data[i][sort_indices]
    return tuple(data)