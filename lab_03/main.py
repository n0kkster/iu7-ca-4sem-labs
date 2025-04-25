import numpy as np
from random import random
from approx import generate_table, change_weight, print_table, solve_task_1d, generate_table_2d, print_table_2d, solve_task_2d
from diffeq import solve_diff_eq

SIZE_TABLE = 7  # Количество точек в таблице
BASE_WEIGHT = 1  # Базовый вес точек
EPS = 0.01  # Шаг для графика

def print_menu():
    print("\n1. Распечатать таблицу (одномерная аппроксимация)\n"
          "2. Изменить вес точки (одномерная аппроксимация)\n"
          "3. Вывести результаты одномерной аппроксимации\n"
          "4. Вывести результаты двумерной аппроксимации\n"
          "5. Распечатать таблицу (двумерная аппроксимация)\n"
          "6. Решить дифференциальное уравнение\n"
          "0. Выйти\n")

def main():
    table = generate_table()
    table_2d = generate_table_2d()
    
    action = 1
    while action != 0:
        print_menu()
        
        try:
            action = int(input("Выберите действие: "))
        except:
            print("\nОшибка: ожидался ввод целого числа!")
            continue
        
        if action == 1:
            print_table(table)
        elif action == 2:
            table = change_weight(table)
        elif action == 3:
            table = solve_task_1d(table)
        elif action == 4:
            solve_task_2d(table_2d)
        elif action == 5:
            print_table_2d(table_2d)
        elif action == 6:
            solve_diff_eq()
        elif action > 6:
            print("\nОшибка: ожидался ввод целого числа от 0 до 6!")

if __name__ == "__main__":
    main()