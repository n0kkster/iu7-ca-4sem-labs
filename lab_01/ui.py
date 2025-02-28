def print_table_newton(x, y) -> None:
    xs = 'x'
    ys = 'y'
    
    print('-' * 44)
    print(f'|{"#":^10}|{xs:^15}|{ys:^15}|')
    print('-' * 44)
    
    for i in range(len(x)):
        print(f'|{(i + 1):^10}|{x[i]:^15.6f}|{y[i]:^15.6f}|')
    print('-' * 44)
    
def print_table_hermite(x, y, yp, ypp) -> None:
    xs = 'x'
    ys = 'y'
    yps = 'y\''
    ypps = 'y\'\''
    
    print('-' * 76)
    print(f'|{"#":^10}|{xs:^15}|{ys:^15}|{yps:^15}|{ypps:^15}|')
    print('-' * 76)
    
    for i in range(len(x)):
        print(f'|{(i + 1):^10}|{x[i]:^15.6f}|{y[i]:^15.6f}|{yp[i]:^15.6f}|{ypp[i]:^15.6f}|')
    print('-' * 76)
    
def print_table(*args: tuple) -> None:
    match args:
        case [x, y]:
            print_table_newton(x, y)
        case [x, y, yp, ypp]:
            print_table_hermite(x, y, yp, ypp)
    
def print_menu() -> None:
    print('1. Найти y(x) с помощью полинома Ньютона')     
    print('2. Найти y(x) с помощью полинома Эрмита')
    print('3. Получить таблицу значений y(x) для ряда значений степеней полиномов Ньютона и Эрмита')
    print('4. Найти корень табличной функции')
    print('5. Решить систему двух уравнений')
    print('0. Выход')
    
def read_choice() -> int:
    try:
        choice = int(input())
        if (choice < 0 or choice > 5):
            raise IndexError('Некорректный пункт меню!')
        return choice

    except IndexError as e:
        print(e)
        exit(1)
                
    except Exception:
        print('\nДоедешь - пиши..')
        exit(1)