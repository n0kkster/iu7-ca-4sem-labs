from math import sqrt
from gauss import Gauss
from typing import Callable

def NewtonSystem(
    Jfunc: Callable[..., float | int],
    funcs: list[Callable[..., float | int]],
    start_root_approx: list[float | int],
    iter_limit: int = 10,
    eps: float = 1e-6,
) -> tuple[list[float], int]:
    """
    Решает систему нелинейных уравнений методом Ньютона.

    Args:
        Jfunc (Callable[..., float | int]): Функция, возвращающая матрицу Якоби системы.
                                           Принимает аргументы переменных (x, y, z, ...) и
                                           возвращает матрицу производных [df_i/dx_j].
        funcs (list[Callable[..., float | int]]): Список функций, определяющих систему уравнений.
                                                 Каждая функция принимает переменные (x, y, z, ...)
                                                 и возвращает значение уравнения f_i(x, y, z, ...).
        start_root_approx (list[float | int]): Начальное приближение корня системы (список значений).
        iter_limit (int, optional): Максимальное количество итераций. По умолчанию 10.
        eps (float, optional): Точность сходимости (критерий остановки). По умолчанию 1e-6.

    Returns:
        tuple[list[float], int]: Кортеж, содержащий:
                                 - Список приближённых значений корня (x, y, z, ...).
                                 - Количество выполненных итераций.
    """
    def f(x: list[float | int]) -> list[float | int]:
        """
        Вычисляет значения всех функций системы для текущего набора переменных.

        Args:
            x (list[float | int]): Текущие значения переменных (x, y, z, ...).

        Returns:
            list[float | int]: Список значений функций системы f_i(x, y, z, ...).
        """
        return [f(*x) for f in funcs]

    # Инициализация начального приближения
    xk = start_root_approx
    # Счётчик итераций
    n = 1
    
    # Итерационный процесс метода Ньютона
    while True:
        # Вычисление приращения dx путём решения системы J(xk) * dx = -f(xk)
        # Jfunc(*xk) возвращает матрицу Якоби, [-y for y in f(xk)] — правую часть
        dx = Gauss(Jfunc(*xk), [-y for y in f(xk)])
        
        # Обновление приближения: x_{k+1} = x_k + dx
        xnext = [xk[i] + dx[i] for i in range(len(xk))]
        
        # Проверка критерия остановки:
        # 1. Если норма приращения ||dx|| < eps
        # 2. Или достигнуто максимальное количество итераций
        if sqrt(sum([x**2 for x in dx])) < eps or n == iter_limit:
            return xnext, n
        
        # Переход к следующей итерации
        xk = xnext
        n += 1