from half_division import HalfDivision
from newton_system import NewtonSystem
from sympson import SympsonIntegral
from numpy import linspace, exp, sqrt
from math import pi
import matplotlib.pyplot as plt

SHOW_GRAPHS = True

def f1(x, y, z):
    return x**2 + y**2 + z**2 - 1

def f2(x, y, z):
    return 2 * x**2 + y**2 - 4 * z

def f3(x, y, z):
    return 3 * x**2 - 4 * y + z**2

def jacobian(x, y, z):
    return [
        [2 * x, 2 * y, 2 * z],
        [4 * x, 2 * y, -4],
        [6 * x, -4, 2 * z],
    ]

def solve_system():
    initial_guesses = [
        (1, 1, 1),
        (42, 88, 14),
        (-100500, 69420, 2281337)
    ]
    
    for x0, y0, z0 in initial_guesses:
        res, iters = NewtonSystem(jacobian, [f1, f2, f3], [x0, y0, z0], iter_limit=666)
        xres, yres, zres = res
        
        print("\n" + "="*50)
        print(f"{'Решение системы уравнений':^50}")
        print("="*50)
        print(f"{'Начальные значения':<30} | {'Значение':>15}")
        print("-"*50)
        print(f"{'x0':<30} | {x0:>15.6f}")
        print(f"{'y0':<30} | {y0:>15.6f}")
        print(f"{'z0':<30} | {z0:>15.6f}")
        print("-"*50)
        print(f"{'Полученное решение':<30} | {'Значение':>15}")
        print("-"*50)
        print(f"{'x':<30} | {xres:>15.6f}")
        print(f"{'y':<30} | {yres:>15.6f}")
        print(f"{'z':<30} | {zres:>15.6f}")
        print(f"{'Итераций':<30} | {iters:>15}")
        print("-"*50)
        print(f"{'Проверка уравнений':<30} | {'Значение':>15}")
        print("-"*50)
        print(f"{'f1(x, y, z)':<30} | {f1(xres, yres, zres):>15.6f}")
        print(f"{'f2(x, y, z)':<30} | {f2(xres, yres, zres):>15.6f}")
        print(f"{'f3(x, y, z)':<30} | {f3(xres, yres, zres):>15.6f}")
        print("="*50)

def Laplas(x, integralCount = 10, integralCallback = SympsonIntegral):
    def underIntegralFunc(t):
        return exp(-(t**2) / 2)
    
    linspace_to_x = list(linspace(0, x, integralCount))
    return 2 / sqrt(2 * pi) * integralCallback(linspace_to_x, underIntegralFunc)

def find_laplace_argument():
    x = linspace(-5, 5, 100)
    y = Laplas(x)
    
    target_y = [0, 0.3, -0.42, 0.96]
    found_x = [HalfDivision(Laplas, y_val, min(x), max(x), iter_limit=30)[0] for y_val in target_y]
    
    print("\n" + "="*40)
    print(f"{'Аргументы функции Лапласа':^40}")
    print("="*40)
    print(f"{'Заданное y':<20} | {'Найденное x':>15}")
    print("-"*40)
    for y_val, x_val in zip(target_y, found_x):
        print(f"{y_val:<20.6f} | {x_val:>15.6f}")
    print("="*40)
    
    if SHOW_GRAPHS:
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, label='Функция Лапласа')
        plt.scatter(found_x, target_y, color='red', label='Найденные точки')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Функция Лапласа и найденные точки')
        plt.legend()
        plt.grid(True)
        plt.show()

x0, y0 = 0, 1
x1, y1 = 1, 3
N = 100 
step = (x1 - x0) / N

def jacobian_diff(*y):
    n = len(y)
    res = []
    
    res.append([1] + [0] * (n - 1)) 
    
    for i in range(1, n - 1):
        row = [0] * (i - 1) + [1 / step**2] + [-2 / step**2 - 3 * y[i] ** 2] + [1 / step**2] + [0] * (n - i - 2)
        res.append(row)
    
    res.append([0] * (n - 1) + [1])  
    return res

def f(n, x):
    if n == 0:
        def resf(*y):
            return y[0] - y0
    elif n == N:
        def resf(*y):
            return y[n] - y1
    else:
        def resf(*y):
            return (y[n - 1] + -2 * y[n] + y[n + 1]) / step**2 - y[n] ** 3 - x[n] ** 2
    return resf

def starty(x):
    return 2 * x + 1

def solve_boundary_problem():
    x = linspace(x0, x1, N + 1)
    y = [starty(xp) for xp in x]
    
    funcs = [f(n, x) for n in range(N + 1)]
    
    res, iters = NewtonSystem(jacobian_diff, funcs, y, iter_limit=30, eps=1e-15)
    
    print("\n" + "="*40)
    print(f"{'Решение краевой задачи':^40}")
    print("="*40)
    print(f"{'Параметр':<20} | {'Значение':>15}")
    print("-"*40)
    print(f"{'Количество итераций':<20} | {iters:>15}")
    print("="*40)
    
    if SHOW_GRAPHS:
        plt.figure(figsize=(10, 6))
        plt.plot(x, res, label='Решение краевой задачи')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Численное решение краевой задачи y\'\' - y^3 = x^2')
        plt.legend()
        plt.grid(True)
        plt.show()

def main():
    while True:
        print("\n" + "="*40)
        print(f"{'МЕНЮ':^40}")
        print("="*40)
        print("1 - Решить систему уравнений")
        print("2 - Найти аргумент функции Лапласа")
        print("3 - Решить краевую задачу")
        print("0 - Выход")
        print("="*40)
        
        choice = input("Введите пункт меню: ")
        
        if choice == '1':
            print("\nРешение системы уравнений...")
            solve_system()
        elif choice == '2':
            print("\nПоиск аргументов функции Лапласа...")
            find_laplace_argument()
        elif choice == '3':
            print("\nРешение краевой задачи...")
            solve_boundary_problem()
        elif choice == '0':
            print("Выход...")
            break
        else:
            print("Неверный выбор. Пожалуйста, введите 0, 1, 2 или 3.")

if __name__ == "__main__":
    main()