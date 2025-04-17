from typing import Callable

def HalfDivision(
    func: Callable[..., float | int],
    target: float | int,
    start: float | int,
    end: float | int,
    iter_limit: int = 10,
    eps: float = 1e-6,
) -> tuple[float, int]:
    """
    Находит корень уравнения func(x) = target методом деления пополам (бисекции).

    Args:
        func (Callable[..., float | int]): Функция, корень которой ищется.
                                          Принимает числовой аргумент и возвращает число.
        target (float | int): Целевое значение функции, для которого ищется x (func(x) = target).
        start (float | int): Начало интервала поиска.
        end (float | int): Конец интервала поиска.
        iter_limit (int, optional): Максимальное количество итераций. По умолчанию 10.
        eps (float, optional): Точность сходимости (критерий остановки). По умолчанию 1e-6.

    Returns:
        tuple[float, int]: Кортеж, содержащий:
                           - Приближённое значение корня x.
                           - Количество выполненных итераций.

    Note:
        Предполагается, что func непрерывна на [start, end], и значения func(start) и func(end)
        имеют противоположные знаки относительно target (т.е. (func(start) - target) * (func(end) - target) < 0).
    """
    # Итерационный процесс метода бисекции
    for iter in range(1, iter_limit + 1):
        # Вычисление середины интервала
        center = (start + end) / 2

        # Проверка критерия остановки:
        # 1. Если |func(center) - target| < eps (достигнута требуемая точность)
        # 2. Или достигнуто максимальное количество итераций
        if abs(func(center) - target) < eps or iter == iter_limit:
            return center, iter

        # Проверка, в какой половине интервала находится корень
        # Если (func(start) - target) * (func(center) - target) < 0,
        # корень находится в левой половине [start, center]
        if (func(start) - target) * (func(center) - target) < 0:
            end = center
        # Иначе корень находится в правой половине [center, end]
        else:
            start = center