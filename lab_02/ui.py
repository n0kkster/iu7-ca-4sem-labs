def print_table_newton(x, y):
    xs = 'x'
    ys = 'y'
    
    print('-' * 44)
    print(f'|{"#":^10}|{xs:^15}|{ys:^15}|')
    print('-' * 44)
    
    for i in range(len(x)):
        print(f'|{(i + 1):^10}|{x[i]:^15.6f}|{y[i]:^15.6f}|')
    print('-' * 44)
    
def print_table(*args: tuple):
    match args:
        case [x, y]:
            print_table_newton(x, y)
    
def print_menu():
    print('1. Найти значение функции с помощью полинома Ньютона.') 
    print('2. Найти значение функции с помощью сплайна.') 
    print('3. Найти значение функции с помощью смешанной интерполяции.') 
    print('0. Выход')
    
def read_choice():
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