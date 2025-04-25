# Модуль для решения дифференциального уравнения методом Галёркина
import numpy as np
import matplotlib.pyplot as plt
from approx import solve_matrix_gauss

# Решение дифференциального уравнения
def solve_diff_eq():
    # Определение базисных функций
    def u0(x):
        """Базисная функция u0(x) = 1 - x, удовлетворяет краевым условиям."""
        return 1 - x
    
    def u1(x):
        """Базисная функция u1(x) = x(1 - x)."""
        return x * (1 - x)
    
    def u2(x):
        """Базисная функция u2(x) = x^2(1 - x)."""
        return x**2 * (1 - x)
    
    def u3(x):
        """Базисная функция u3(x) = x^3(1 - x)."""
        return x**3 * (1 - x)
    
    # Производные базисных функций
    def du0(x):
        """Производная u0: du0/dx = -1."""
        return -1
    
    def du1(x):
        """Производная u1: du1/dx = 1 - 2x."""
        return 1 - 2 * x
    
    def du2(x):
        """Производная u2: du2/dx = 2x - 3x^2."""
        return 2 * x - 3 * x**2
    
    def du3(x):
        """Производная u3: du3/dx = 3x^2 - 4x^3."""
        return 3 * x**2 - 4 * x**3
    
    # Вторые производные базисных функций
    def d2u0(x):
        """Вторая производная u0: d^2u0/dx^2 = 0."""
        return 0
    
    def d2u1(x):
        """Вторая производная u1: d^2u1/dx^2 = -2."""
        return -2
    
    def d2u2(x):
        """Вторая производная u2: d^2u2/dx^2 = 2 - 6x."""
        return 2 - 6 * x
    
    def d2u3(x):
        """Вторая производная u3: d^2u3/dx^2 = 6x - 12x^2."""
        return 6 * x - 12 * x**2
    
    def f(x):
        """Правая часть уравнения: f(x) = 2x."""
        return 2 * x
    
    # Метод трапеций для численного интегрирования
    def trapezoidal_integral(f, a, b, n=1000):
        
        # Шаг разбиения
        h = (b - a) / n

        # Инициализируем интеграл половинной суммой значений на границах
        integral = 0.5 * (f(a) + f(b))
        
        for i in range(1, n):
            integral += f(a + i * h)
        
        integral *= h
        
        return integral
    
    # Формирование системы уравнений для коэффициентов
    def solve_for_m(m):
        # Создаём матрицу A размером m x m и вектор B размером m
        A = [[0 for _ in range(m)] for _ in range(m)]
        B = [0 for _ in range(m)]
        
        # Цикл по индексам базисных функций (i = 1, ..., m)
        for i in range(1, m + 1):
            # Цикл по индексам для формирования матрицы A
            for j in range(1, m + 1):
                # Определяем подынтегральное выражение для левой части
                def integrand_left(x):
                    # Выбираем базисную функцию и её производные в зависимости от i
                    if i == 1:
                        ui, dui, d2ui = u1, du1, d2u1
                    elif i == 2:
                        ui, dui, d2ui = u2, du2, d2u2
                    elif i == 3:
                        ui, dui, d2ui = u3, du3, d2u3
                    
                    # Выбираем базисную функцию uj в зависимости от j
                    if j == 1:
                        uj = u1
                    elif j == 2:
                        uj = u2
                    elif j == 3:
                        uj = u3
                    
                    # Вычисляем (u_i'' + x u_i' + u_i) * u_j
                    # Это соответствует левой части уравнения y'' + xy' + y
                    return (d2ui(x) + x * dui(x) + ui(x)) * uj(x)
                
                # Интегрируем подынтегральное выражение на [0, 1]
                A[i - 1][j - 1] = trapezoidal_integral(integrand_left, 0, 1)
            
            # Определяем подынтегральное выражение для правой части
            def integrand_right(x):
                # Выбираем базисную функцию ui в зависимости от i
                if i == 1:
                    ui = u1
                elif i == 2:
                    ui = u2
                elif i == 3:
                    ui = u3
                
                # Вычисляем (f(x) - (u0'' + x u0' + u0)) * u_i
                # Это соответствует правой части уравнения
                return (f(x) - (d2u0(x) + x * du0(x) + u0(x))) * ui(x)
            
            # Интегрируем подынтегральное выражение на [0, 1]
            B[i - 1] = trapezoidal_integral(integrand_right, 0, 1)
        
        # Формируем расширенную матрицу [A | B]
        matrix = [row + [B[idx]] for idx, row in enumerate(A)]
        
        # Пытаемся решить СЛАУ методом Гаусса
        try:
            C = solve_matrix_gauss(matrix)
            # Возвращаем коэффициенты c_i
            return C
        except ValueError as e:
            # Если возникает ошибка (например, деление на ноль), выводим сообщение
            print(f"Ошибка при решении системы для m={m}: {e}")
            return None
    
    C_m2 = solve_for_m(2)
    if C_m2 is not None:
        print("Коэффициенты для m=2:", C_m2)
    
    C_m3 = solve_for_m(3)
    if C_m3 is not None:
        print("Коэффициенты для m=3:", C_m3)
    
    x = np.linspace(0, 1, 100)
    if C_m2 is not None:
        y_m2 = u0(x) + C_m2[0] * u1(x) + C_m2[1] * u2(x)
        plt.plot(x, y_m2, label='m=2')
    if C_m3 is not None:
        y_m3 = u0(x) + C_m3[0] * u1(x) + C_m3[1] * u2(x) + C_m3[2] * u3(x)
        plt.plot(x, y_m3, label='m=3')
    
    plt.legend()
    plt.grid()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Сравнение решений для m=2 и m=3')
    plt.show()