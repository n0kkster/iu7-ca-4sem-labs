import numpy as np
from numpy.typing import NDArray
from typing import Tuple

def select_closest_points(x: float, x_data: NDArray[np.float64], num_points: int) -> NDArray[np.int64]:
    distances: NDArray[np.float64] = np.abs(x - x_data)
    indices: NDArray[np.int64] = np.argsort(distances)
    return indices[:num_points]

def newton_divided_differences(x_points: NDArray[np.float64], y_points: NDArray[np.float64]) -> NDArray[np.float64]:
    n: int = len(x_points)
    dd: NDArray[np.float64] = np.zeros((n, n))
    dd[:, 0] = y_points
    for k in range(1, n):
        for i in range(n - k):
            dd[i, k] = (dd[i + 1, k - 1] - dd[i, k - 1]) / (x_points[i + k] - x_points[i])
    return dd

def newton_eval(x_eval: float, x_points: NDArray[np.float64], dd: NDArray[np.float64]) -> float:
    n: int = len(x_points) 
    p: float = dd[0, 0] 
    for k in range(1, n):
        term: float = dd[0, k]
        for j in range(k):
            term *= (x_eval - x_points[j])
        p += term
    return p

def hermite_divided_differences(x_hermite: NDArray[np.float64], y_hermite: NDArray[np.float64], 
                               yp_hermite: NDArray[np.float64], ypp_hermite: NDArray[np.float64]) \
                               -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
    m: int = len(x_hermite)
    z: NDArray[np.float64] = np.repeat(x_hermite, 3) 
    dd: NDArray[np.float64] = np.zeros((3 * m, 3 * m))

    for i in range(3 * m):
        dd[i, 0] = y_hermite[i // 3]

    for k in range(1, 3 * m):
        for i in range(3 * m - k):
            if k == 1 and i % 3 < 2:
                dd[i, k] = yp_hermite[i // 3]
            elif k == 2 and i % 3 == 0:
                dd[i, k] = ypp_hermite[i // 3] / 2 
            else:
                dd[i, k] = (dd[i + 1, k - 1] - dd[i, k - 1]) / (z[i + k] - z[i])
    return dd, z

def hermite_eval(x_eval: float, z: NDArray[np.float64], dd: NDArray[np.float64]) -> float:
    n: int = len(z) - 1
    p: float = dd[0, n]
    for k in range(n - 1, -1, -1):
        p = dd[0, k] + (x_eval - z[k]) * p
    return p

def invert_derivs(yp: NDArray[np.float64], ypp: NDArray[np.float64]) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
    rev_yp = 1 / yp  # g'(y) = 1 / f'(x)
    rev_ypp = -ypp / (yp ** 3)  # g''(y) = -f''(x) / (f'(x))^3
    
    return rev_yp, rev_ypp

def newton_interp(x: NDArray[np.float64], y: NDArray[np.float64], x_inp: float, n: int) -> float:
    indices: NDArray[np.int64] = select_closest_points(x_inp, x, n + 1)
    x_: NDArray[np.float64] = x[indices]
    y_: NDArray[np.float64] = y[indices]
    dd: NDArray[np.float64] = newton_divided_differences(x_, y_)
    res: float = newton_eval(x_inp, x_, dd)
    return res

def hermite_interp(x: NDArray[np.float64], y: NDArray[np.float64], yp: NDArray[np.float64], ypp: NDArray[np.float64], x_inp: float, n: int) -> float:
    indices: NDArray[np.int64] = select_closest_points(x_inp, x, n)
    x_: NDArray[np.float64] = x[indices]
    y_: NDArray[np.float64] = y[indices]
    yp_: NDArray[np.float64] = yp[indices]
    ypp_: NDArray[np.float64] = ypp[indices]
    dd, z = hermite_divided_differences(x_, y_, yp_, ypp_)
    res: float = hermite_eval(x_inp, z, dd)    
    return res

def solve_system(
    x1: NDArray[np.float64], y1: NDArray[np.float64], x2: NDArray[np.float64], y2: NDArray[np.float64],
    n_interp: int) -> Tuple[float]:

    x_common = x1
    y_diff = np.array([newton_interp(x1, y1, x, n_interp) - newton_interp(x2, y2, x, n_interp) for x in x_common])
    
    y_indices = np.argsort(y_diff)
    y_diff = y_diff[y_indices]
    x_common = x_common[y_indices]
    
    y_diff = y_diff[:6]
    x_common = x_common[:6]
        
    for i in range(len(x_common) - 1):
        if y_diff[i] * y_diff[i + 1] < 0:
            x = newton_interp(y_diff, x_common, 0, n_interp)
            y = newton_interp(x2, y2, x, n_interp)
            return x, y