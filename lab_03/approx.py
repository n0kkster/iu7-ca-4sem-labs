# Модуль для задач одномерной и двумерной аппроксимации
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from random import random
from copy import deepcopy

# Константы
SIZE_TABLE = 7  # Количество точек в таблице
BASE_WEIGHT = 1  # Базовый вес точек
EPS = 0.01  # Шаг для графика

# Генерация таблицы для одномерной аппроксимации
def generate_table():
    table = []
    x = random() * 5
    
    i = 0
    while i < SIZE_TABLE:
        table.append([x + i, random() * 5, BASE_WEIGHT])
        i += 1
    
    return table

# Изменение веса точки в таблице
def change_weight(table):
    try:
        index = int(input("\nВведите номер точки в таблице: "))
    except:
        print("\nОшибка: некорректно введён номер точки!")
        return table
    
    if (index > len(table)) or (index < 1):
        print("\nОшибка: в таблице нет точки с таким номером!")
        return table
    
    try:
        weight = float(input("\nВведите новый вес точки: "))
    except:
        print("\nОшибка: некорректно введён вес точки!")
        return table
    
    table[index - 1][2] = weight
    return table

# Вывод таблицы
def print_table(table):
    print("\n\tСгенерированная таблица\n\n" +
          "  №    |     X     |     Y    |    W \n" + 40 * "-")
    
    size = len(table)
    
    for i in range(size):
        print("  %-3d  |   %-5.2f   |   %-4.2f   |   %-5.2f   "
              % (i + 1, table[i][0], table[i][1], table[i][2]))

# Инициализация матрицы
def init_matrix(size):
    matrix = []
    for _ in range(size + 1):
        row = []
        for _ in range(size + 2):
            row.append(0)
        matrix.append(row)
    
    return matrix

# Создание СЛАУ для одномерной аппроксимации
def make_slau_matrix(table, n):
    size = len(table)
    # Создаём матрицу размером (n + 1) x (n + 2)
    matrix = init_matrix(n)
    
    for i in range(n + 1):
        for j in range(n + 1):
            # Инициализируем элементы матрицы и правую часть
            matrix[i][j] = 0.0
            matrix[i][n + 1] = 0.0

            for k in range(size):
                weight = table[k][2]
                x = table[k][0]
                y = table[k][1]

                # Добавляем вклад в матрицу: p_k * x_k^(i+j)
                matrix[i][j] += weight * pow(x, (i + j))
                
                # Добавляем вклад в правую часть: p_k * y_k * x_k^i
                matrix[i][n + 1] += weight * y * pow(x, i)
    
    return matrix

# Решение СЛАУ методом Гаусса
def solve_matrix_gauss(matrix):
    size = len(matrix)
    
    # Прямой ход
    for i in range(size):
        # Перебираем строки ниже текущей
        for j in range(i + 1, size):
            if (i == j):
                continue
            # Вычисляем коэффициент для обнуления элемента matrix[j][i]
            k = matrix[j][i] / matrix[i][i]
            # Обновляем элементы строки j
            for q in range(i, size + 1):
                matrix[j][q] -= k * matrix[i][q]
    
    # Создаём список для результатов (коэффициентов)
    result = [0 for _ in range(size)]
    
    # Обратный ход
    for i in range(size - 1, -1, -1):
        # Вычитаем вклад уже найденных коэффициентов
        for j in range(size - 1, i, -1):
            matrix[i][size] -= result[j] * matrix[i][j]
        # Находим коэффициент a_i
        result[i] = matrix[i][size] / matrix[i][i]
    
    # Возвращаем коэффициенты
    return result

# Нахождение точек для построения графика
def find_graph_dots(table, n):
    matrix = make_slau_matrix(table, n)
    result = solve_matrix_gauss(matrix)
    
    x_arr, y_arr = [], []
    k = table[0][0] - EPS
    
    size = len(table)
    while (k <= table[size - 1][0] + EPS):
        y = 0
        for j in range(0, n + 1):
            y += result[j] * pow(k, j)
        x_arr.append(k)
        y_arr.append(y)
        k += EPS
    
    return x_arr, y_arr

# Проверка, изменены ли веса
def table_changed(table):
    for i in table:
        if i[2] != 1:
            return True
    return False

# Получение базовой таблицы
def get_base_table(table):
    base_table = deepcopy(table)
    size = len(base_table)
    
    for i in range(size):
        base_table[i][2] = 1
    
    return base_table

# Построение графиков
def plot_graphs(table, n, type_graph, type_dots):
    for i in range(1, n + 1):
        if (i > 2 and i < n):
            continue
        x_arr, y_arr = find_graph_dots(table, i)
        plt.plot(x_arr, y_arr, type_graph, label="%s\nn = %d" % (type_dots, i))

# Решение задачи одномерной аппроксимации
def solve_task_1d(table):
    try:
        n = int(input("\nВведите степень аппроксимирующего полинома: "))
    except:
        print("\nОшибка: некорректно введена степень полинома!")
        return table
    
    if n >= SIZE_TABLE or n <= 0:
        print("\nОшибка: некорректно введена степень полинома!")
        return table
    
    if table_changed(table):
        # Если веса изменены, создаём таблицу с равными весами
        base_table = get_base_table(table)
        type_dots = "Diff weights"
        type_graph = "-."
        # Строим графики для равных весов
        plot_graphs(base_table, n, "-", "Equal weights")
    else:
        # Если веса не изменены, используем стандартные параметры
        type_dots = "Equal weights"
        type_graph = "-"
    
    # Строим графики для текущей таблицы
    plot_graphs(table, n, type_graph, type_dots)
    
    x_arr = [i[0] for i in table]
    y_arr = [i[1] for i in table]
    
    plt.plot(x_arr, y_arr, 'o', label="dots")
    plt.legend()
    plt.grid()
    plt.xlabel("Axis X")
    plt.ylabel("Axis Y")
    plt.show()
    
    return table

# Генерация таблицы для двумерной аппроксимации
def generate_table_2d():
    table = []
    x = random() * 5
    y = random() * 5
    
    i = 0
    while i < SIZE_TABLE:
        table.append([random() * 5, random() * 5, random() * 5, random() * 5])
        i += 1
    
    return table

# Вывод таблицы для двумерной аппроксимации
def print_table_2d(table):
    print("\n\tСгенерированная таблица (двумерная аппроксимация)\n\n" +
          "  №    |     X     |     Y     |     Z     |    W \n" + 50 * "-")
    
    size = len(table)
    
    for i in range(size):
        print("  %-3d  |   %-5.2f   |   %-5.2f   |   %-5.2f   |   %-5.2f   "
              % (i + 1, table[i][0], table[i][1], table[i][2], table[i][3]))

# Решение задачи двумерной аппроксимации
def solve_task_2d(table):
    x = np.array([i[0] for i in table])
    y = np.array([i[1] for i in table])
    z = np.array([i[2] for i in table])
    weights = np.array([i[3] for i in table])
    
    # Вычисляем суммы для нормальных уравнений
    sum_rho = np.sum(weights)           
    sum_rho_x = np.sum(weights * x)       
    sum_rho_y = np.sum(weights * y)       
    sum_rho_z = np.sum(weights * z)       
    sum_rho_x2 = np.sum(weights * x**2)   
    sum_rho_y2 = np.sum(weights * y**2)   
    sum_rho_xy = np.sum(weights * x * y)  
    sum_rho_xz = np.sum(weights * x * z)  
    sum_rho_yz = np.sum(weights * y * z)  
    
    # Формируем матрицу СЛАУ
    matrix = [
        [sum_rho_x2, sum_rho_xy, sum_rho_x, sum_rho_xz],
        [sum_rho_xy, sum_rho_y2, sum_rho_y, sum_rho_yz],
        [sum_rho_x, sum_rho_y, sum_rho, sum_rho_z]
    ]
    
    # Решаем СЛАУ методом Гаусса
    coefficients = solve_matrix_gauss(matrix)
    
    a, b, c = coefficients
    
    # Создаём сетку для построения плоскости
    xx = np.linspace(min(x), max(x), 100)
    yy = np.linspace(min(y), max(y), 100)
    xx, yy = np.meshgrid(xx, yy)
    # Вычисляем z = ax + by + c для сетки
    zz = a * xx + b * yy + c
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Размер точки пропорционален весу
    ax.scatter(x, y, z, c='r', marker='o', s=weights*10, label='Исходные точки (размер = вес)')
    ax.plot_surface(xx, yy, zz, alpha=0.5, color='b')
    
    surf_proxy = Patch(color='b', alpha=0.5, label='Аппроксимирующая поверхность')
    
    # Подписываем оси
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    # Добавляем легенду с прокси-объектом и точками
    ax.legend(handles=[surf_proxy, ax.collections[0]])
    # Показываем график
    plt.show()