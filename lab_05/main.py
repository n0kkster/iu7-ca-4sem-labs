import numpy as np
from scipy.special import roots_legendre
from math import fabs


def integrate_trapezoid(f, a, b, n=100):
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    integral = h * (0.5 * y[0] + 0.5 * y[-1] + np.sum(y[1:-1]))
    return integral


def integrate_simpson(f, a, b, n=100):
    if n % 2 != 0:
        n += 1
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    integral = h / 3 * (y[0] + y[-1] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-2:2]))
    return integral


def integrate_gauss(f, a, b, n=3):
    nodes, weights = roots_legendre(n)
    transformed_nodes = 0.5 * (b - a) * nodes + 0.5 * (a + b)
    integral = 0.5 * (b - a) * np.sum(weights * f(transformed_nodes))
    return integral

def task1():
    def func_k1(x):
        return abs(x)

    def func_k2(x):
        return abs(x) ** 2

    exact_k1 = 1.0
    exact_k2 = 2 / 3

    a, b = -1, 1
    n = 3

    print("\nРезультаты для k=1 (функция |x|):")
    print(f"Точное значение: {exact_k1:.6f}")
    print(
        f"Метод трапеций: {integrate_trapezoid(func_k1, a, b, n):.6f}, ошибка: {fabs(integrate_trapezoid(func_k1, a, b, n) - exact_k1):.6f}")
    print(
        f"Метод Симпсона: {integrate_simpson(func_k1, a, b, n):.6f}, ошибка: {fabs(integrate_simpson(func_k1, a, b, n) - exact_k1):.6f}")
    print(
        f"Метод Гаусса: {integrate_gauss(func_k1, a, b, n):.6f}, ошибка: {fabs(integrate_gauss(func_k1, a, b, n) - exact_k1):.6f}")

    print("\nРезультаты для k=2 (функция x^2):")
    print(f"Точное значение: {exact_k2:.6f}")
    print(
        f"Метод трапеций: {integrate_trapezoid(func_k2, a, b, n):.6f}, ошибка: {fabs(integrate_trapezoid(func_k2, a, b, n) - exact_k2):.6f}")
    print(
        f"Метод Симпсона: {integrate_simpson(func_k2, a, b, n):.6f}, ошибка: {fabs(integrate_simpson(func_k2, a, b, n) - exact_k2):.6f}")
    print(
        f"Метод Гаусса: {integrate_gauss(func_k2, a, b, n):.6f}, ошибка: {fabs(integrate_gauss(func_k2, a, b, n) - exact_k2):.6f}")


def read_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    x_line = lines[0].strip().split('\t')
    x_values = [float(val) for val in x_line[1:] if val]

    y_values = []
    z_matrix = []
    for line in lines[1:]:
        parts = line.strip().split('\t')
        if (len(parts) == 0):
            continue
        if (parts[0] == ''):
            continue
        y_values.append(float(parts[0]))
        z_row = [float(val) for val in parts[1:] if val]
        z_matrix.append(z_row)

    return np.array(x_values), np.array(y_values), np.array(z_matrix)


def bilinear_interpolation(x, y, x_grid, y_grid, z_matrix):
    i = np.searchsorted(x_grid, x) - 1
    j = np.searchsorted(y_grid, y) - 1

    # Ограничиваем индексы в пределах массива
    i = max(0, min(i, len(x_grid) - 2))
    j = max(0, min(j, len(y_grid) - 2))

    # Координаты соседних точек
    x0, x1 = x_grid[i], x_grid[i + 1]
    y0, y1 = y_grid[j], y_grid[j + 1]

    # Значения функции в соседних точках
    f00 = z_matrix[j][i]
    f01 = z_matrix[j][i + 1]
    f10 = z_matrix[j + 1][i]
    f11 = z_matrix[j + 1][i + 1]

    # Вычисляем веса
    dx = x1 - x0 if x1 != x0 else 1.0
    dy = y1 - y0 if y1 != y0 else 1.0
    wx = (x - x0) / dx
    wy = (y - y0) / dy

    # Билинейная интерполяция
    return (f00 * (1 - wx) * (1 - wy) +
            f01 * wx * (1 - wy) +
            f10 * (1 - wx) * wy +
            f11 * wx * wy)


def double_integrate(x_grid, y_grid, z_matrix, phi, psi, a, b, n_x=100, n_y=100):
    x_nodes = np.linspace(a, b, n_x)
    integral = 0.0

    for x in x_nodes:
        y_a = phi(x)
        y_b = psi(x)
        if y_a >= y_b:
            continue

        y_nodes = np.linspace(y_a, y_b, n_y)
        f_values = np.array([bilinear_interpolation(x, y, x_grid, y_grid, z_matrix)
                             for y in y_nodes])

        h_y = (y_b - y_a) / (n_y - 1)
        integral_y = h_y * (0.5 * f_values[0] + 0.5 * f_values[-1] + np.sum(f_values[1:-1]))
        integral += integral_y

    h_x = (b - a) / (n_x - 1)
    integral *= h_x

    return integral


if __name__ == "__main__":
    print("Задание 1:")
    task1()

    file_path = "data.txt"
    x_values, y_values, z_matrix = read_data(file_path)

    alpha = 1.0
    beta = 4.0
    a = 0.0
    b = 2.0

    def phi(x):
        return alpha * x ** 2

    def psi(x):
        return beta * x ** 2

    print("\nЗадание 2:")
    integral = double_integrate(x_values, y_values, z_matrix, phi, psi, a, b)
    print(f"Двойной интеграл: {integral}")