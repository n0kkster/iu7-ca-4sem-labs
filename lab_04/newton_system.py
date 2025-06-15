from math import sqrt
from gauss import Gauss

def NewtonSystem(Jfunc, funcs, start_root_approx, iter_limit = 10, eps = 1e-6):
    def f(x):
        return [f(*x) for f in funcs]

    xk = start_root_approx
    n = 1
    
    while True:
        dx = Gauss(Jfunc(*xk), [-y for y in f(xk)])
        
        xnext = [xk[i] + dx[i] for i in range(len(xk))]
        
        if sqrt(sum([x**2 for x in dx])) < eps or n == iter_limit:
            return xnext, n
        
        xk = xnext
        n += 1