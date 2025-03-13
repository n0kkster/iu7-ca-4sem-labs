def select_closest_points(x: float, x_data: list[float], num_points: int) -> list[int]:
    # Вычисляем расстояния от x до всех точек x_data
    distances = [abs(x - x_point) for x_point in x_data]
    # Сортируем индексы по расстояниям
    indices = sorted(range(len(distances)), key=lambda i: distances[i])
    # Возвращаем первые num_points индексов
    return indices[:num_points]

def newton_divided_differences(x_points: list[float], y_points: list[float]) -> list[list[float]]:
    n = len(x_points)
    # Создаем двумерный список для разделенных разностей
    dd = [[0.0] * n for _ in range(n)]
    # Первая колонка — значения y
    for i in range(n):
        dd[i][0] = y_points[i]
    # Вычисляем разделенные разности
    for k in range(1, n):
        for i in range(n - k):
            dd[i][k] = (dd[i + 1][k - 1] - dd[i][k - 1]) / (x_points[i + k] - x_points[i])
    return dd

def newton_eval(x_eval: float, x_points: list[float], dd: list[list[float]]) -> float:
    n = len(x_points)
    # Начальное значение — первая разделенная разность нулевого порядка
    p = dd[0][0]
    # Вычисляем полином по схеме Горнера
    for k in range(1, n):
        term = dd[0][k]
        for j in range(k):
            term *= (x_eval - x_points[j])
        p += term
    return p

def newton_interp(x: list[float], y: list[float], x_inp: float, n: int) -> float:
    # Выбираем ближайшие точки
    indices = select_closest_points(x_inp, x, n + 1)
    # Формируем подмножества x и y
    x_ = [x[i] for i in indices]
    y_ = [y[i] for i in indices]
    # Вычисляем разделенные разности
    dd = newton_divided_differences(x_, y_)
    # Оцениваем значение полинома в точке x_inp
    res = newton_eval(x_inp, x_, dd)
    return res

def spline_interp(x: list[float], y: list[float], x_val: float):
    """
    Создает функцию кубической сплайн-интерполяции для заданных точек (x, y).
    
    Аргументы:
        x (list[float]): Список координат x, отсортированный по возрастанию.
        y (list[float]): Список соответствующих значений y.
    
    Возвращает:
        function: Функция, вычисляющая значение сплайна в заданной точке.
    """
    
    n = len(x) - 1  # Количество интервалов
    h = [x[i + 1] - x[i] for i in range(n)]  # Шаги между узлами
    
    # Шаг 1: Построение системы уравнений для второй производной m_i
    A = [h[i] for i in range(n - 1)]  # Поддиагональ
    B = [2 * (h[i] + h[i + 1]) for i in range(n - 1)]  # Главная диагональ
    C = [h[i + 1] for i in range(n - 1)]  # Наддиагональ
    D = [6 * ((y[i + 2] - y[i + 1]) / h[i + 1] - (y[i + 1] - y[i]) / h[i]) for i in range(n - 1)]  # Правая часть
    
    # Шаг 2: Решение системы методом прогонки (Thomas algorithm)
    m = [0.0] * (n + 1)  # Вектор вторых производных, m_0 = m_n = 0 для естественного сплайна
    
    # Прямой ход
    for i in range(1, n - 1):
        factor = A[i - 1] / B[i - 1]
        B[i] -= factor * C[i - 1]
        D[i] -= factor * D[i - 1]
        
    # Обратный ход
    if n > 1:
        m[n - 1] = D[n - 2] / B[n - 2]
        for i in range(n - 3, -1, -1):
            m[i + 1] = (D[i] - C[i] * m[i + 2]) / B[i]

    # Шаг 3: Вычисление коэффициентов сплайна
    a = y[:-1]  # a_i = y_i
    b = [(y[i + 1] - y[i]) / h[i] - h[i] * (m[i + 1] + 2 * m[i]) / 6 for i in range(n)]
    c = [m[i] / 2 for i in range(n)]
    d = [(m[i + 1] - m[i]) / (6 * h[i]) for i in range(n)]
            
    for i in range(n):
        if x[i] <= x_val <= x[i + 1]:
            dx = x_val - x[i]
            return a[i] + b[i] * dx + c[i] * dx**2 + d[i] * dx**3
    

def interp_point(line, x, n, method):
    x_arr = list(range(len(line)))
    y_arr = line

    if method == 'newton':
        res = newton_interp(x_arr, y_arr, x, n)
    elif method == 'spline':
        res = spline_interp(x_arr, y_arr, x)
    else:
        res = None
    return res

def interp_line(plane, y, n, method):
    line = []
    for x in range(len(plane)):
        t = [plane[i][x] for i in range(len(plane))]
        line.append(interp_point(t, y, n, method))
    return line

def interp_plane(body, z, n, method):
    plane = []
    for y in range(len(body)):
        t = [body[i][y] for i in range(len(body))]
        plane.append(interp_line(t, z, n, method))
    return plane

def interp_newton_3d(body, x, y, z, nx, ny, nz):
    plane = interp_plane(body, z, nz, 'newton')
    line = interp_line(plane, y, ny, 'newton')
    point = interp_point(line, x, nx, 'newton')
    return point

def interp_spline_3d(body, x, y, z):
    plane = interp_plane(body, z, 0, 'spline')
    line = interp_line(plane, y, 0, 'spline')
    point = interp_point(line, x, 0, 'spline')
    return point

def interp_mixed_3d(body, x, y, z, nx, ny, nz):
    plane = interp_plane(body, z, nz, 'newton' if nz != -1 else 'spline')
    line = interp_line(plane, y, ny, 'newton' if ny != -1 else 'spline')
    point = interp_point(line, x, nx, 'newton' if nx != -1 else 'spline')
    return point