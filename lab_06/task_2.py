from shooting_method import solve_boundary_problem


def solve():
    # Задание 2
    print("\nРешение краевой задачи:")
    # Параметры задачи
    alpha = 1.0  # u'(0) = α
    beta = 0.5  # коэффициент в правом краевом условии
    gamma = 0.2  # константа в правом краевом условии

    # Решение краевой задачи
    x, u = solve_boundary_problem(alpha, beta, gamma)

    # Вывод результатов
    print("\nРезультаты решения краевой задачи:")
    for i in range(len(x)):
        print(f"x = {x[i]:.2f}, u = {u[i]:.6f}")


solve()