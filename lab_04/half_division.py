def HalfDivision(func, target, start, end, iter_limit = 10, eps = 1e-6):
    for iter in range(1, iter_limit + 1):
        center = (start + end) / 2

        if abs(func(center) - target) < eps or iter == iter_limit:
            return center, iter

        if (func(start) - target) * (func(center) - target) < 0:
            end = center
        else:
            start = center