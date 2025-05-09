import matplotlib.pyplot as plt
import os
from generator import generate_tunnels, manual_input_tunnels
from algorithms import greedy_algorithm, probabilistic_algorithm, compute_distances, create_adjacency_matrix, floyd_warshall_modified
from experiments import run_experiments
from utils import save_results_to_file

def plot_tunnels(a, b, c, d, n, W=None, H=None):
    plt.figure(figsize=(8, 6))
    for i in range(n):
        plt.plot([a[i], c[i]], [b[i], d[i]], 'b-', label=f'Тунель {i+1}' if i == 0 else "")
        mid_x = (a[i] + c[i]) / 2
        mid_y = (b[i] + d[i]) / 2
        plt.text(mid_x, mid_y, f'{i+1}', fontsize=9, color='red', ha='center', va='center')
    plt.title('Тунелі')
    plt.xlabel('X')
    plt.ylabel('Y')
    if W is not None and H is not None:
        plt.xlim(0, W)
        plt.ylim(0, H)
    else:
        plt.autoscale()
    plt.grid(True)
    plt.legend()
    plt.savefig('results/tunnels_plot.png')
    plt.close()
    print("\nГрафік тунелів збережено як 'tunnels_plot.png'")

def load_task_from_file():
    while True:
        filename = input("Введіть назву файлу для завантаження даних (наприклад, task_data.txt): ").strip()
        if not filename:
            print("Назва файлу не може бути порожньою!")
            continue
        
        if not os.path.exists('inputs/'+filename):
            while True:
                retry_choice = input(f"Файл '{'inputs/'+filename}' не знайдено. Спробувати ще раз? (так/ні): ").strip().lower()
                if retry_choice in ['так', 'ні']:
                    break
                print("Будь ласка, введіть 'так' або 'ні'!")
            
            if retry_choice == 'ні':
                print("Завантаження даних скасовано.")
                return None
            continue
        
        try:
            with open('inputs/'+filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                if len(lines) < 2:
                    raise ValueError("Файл має містити щонайменше 2 рядки: n, m, а потім n рядків координат!")
                
                n = int(lines[0].strip())
                m = int(lines[1].strip())
                
                if len(lines) != n + 2:
                    raise ValueError(f"Файл має містити рівно {n + 2} рядків: n, m і {n} рядків координат!")
                
                if n <= 0:
                    raise ValueError("Кількість тунелів (n) має бути додатною!")
                if m <= 0:
                    raise ValueError("Кількість ітерацій (m) має бути додатною!")
                
                a, b, c, d = [], [], [], []
                for i in range(n):
                    coords = lines[i + 2].strip().split()
                    if len(coords) != 4:
                        raise ValueError(f"Рядок {i + 3} має містити рівно 4 координати (a b c d)!")
                    at = float(coords[0])
                    bt = float(coords[1])
                    ct = float(coords[2])
                    dt = float(coords[3])
                    a.append(at)
                    b.append(bt)
                    c.append(ct)
                    d.append(dt)
                
                print(f"Дані успішно завантажено з файлу '{filename}'")
                return n, m, a, b, c, d
        except ValueError as e:
            print(f"Помилка: {str(e)}")
            while True:
                retry_choice = input("Спробувати ще раз? (так/ні): ").strip().lower()
                if retry_choice in ['так', 'ні']:
                    break
                print("Будь ласка, введіть 'так' або 'ні'!")
            
            if retry_choice == 'ні':
                print("Завантаження даних скасовано.")
                return None
        except Exception as e:
            print(f"Помилка при читанні файлу: {str(e)}")
            while True:
                retry_choice = input("Спробувати ще раз? (так/ні): ").strip().lower()
                if retry_choice in ['так', 'ні']:
                    break
                print("Будь ласка, введіть 'так' або 'ні'!")
            
            if retry_choice == 'ні':
                print("Завантаження даних скасовано.")
                return None

def run_task(n, a, b, c, d, m, W=None, H=None):
    lengths = compute_distances(a, b, c, d, n)
    result_lines = ["Тунелі та їхні довжини:\n"]
    for i in range(n):
        line = f"Тунель {i+1}: ({a[i]:.2f}, {b[i]:.2f}, {c[i]:.2f}, {d[i]:.2f}), Довжина: {lengths[i]:.2f}\n"
        result_lines.append(line)
    print("".join(result_lines))
    
    P = create_adjacency_matrix(a, b, c, d, n)
    result_lines.append("\nМатриця суміжності P:\n")
    print("\nМатриця суміжності P:")
    for i in range(n):
        row = " ".join(f"{val}" for val in P[i])
        line = f"{row}\n"
        result_lines.append(line)
        print(row)
    
    R = floyd_warshall_modified(P, n)
    result_lines.append("\nМатриця досяжності R:\n")
    print("\nМатриця досяжності R:")
    for i in range(n):
        row = " ".join(f"{val}" for val in R[i])
        line = f"{row}\n"
        result_lines.append(line)
        print(row)
    
    print("\nОберіть опцію:")
    print("1. Виконати жадібний алгоритм")
    print("2. Виконати імовірнісний алгоритм")
    print("3. Виконати обидва алгоритми")
    while True:
        try:
            choice = int(input("Введіть ваш вибір (1-3): "))
            break
        except ValueError:
            print("Будь ласка, введіть коректне число від 1 до 3!")
    
    if choice == 1:
        x, L = greedy_algorithm(n, a, b, c, d)
        result_lines.append("\nРезультати жадібного алгоритму:\n")
        result_lines.append(f"Вибрані тунелі: {x}\n")
        result_lines.append(f"Загальна довжина: {L:.2f}\n")
        print("\nРезультати жадібного алгоритму:")
        print(f"Вибрані тунелі: {x}")
        print(f"Загальна довжина: {L:.2f}")
        plot_tunnels(a, b, c, d, n, W, H)
    elif choice == 2:
        x, L = probabilistic_algorithm(n, a, b, c, d, m)
        result_lines.append("\nРезультати імовірнісного алгоритму:\n")
        result_lines.append(f"Вибрані тунелі: {x}\n")
        result_lines.append(f"Загальна довжина: {L:.2f}\n")
        print("\nРезультати імовірнісного алгоритму:")
        print(f"Вибрані тунелі: {x}")
        print(f"Загальна довжина: {L:.2f}")
        plot_tunnels(a, b, c, d, n, W, H)
    elif choice == 3:
        x_greedy, L_greedy = greedy_algorithm(n, a, b, c, d)
        x_prob, L_prob = probabilistic_algorithm(n, a, b, c, d, m)
        result_lines.append("\nРезультати жадібного алгоритму:\n")
        result_lines.append(f"Вибрані тунелі: {x_greedy}\n")
        result_lines.append(f"Загальна довжина: {L_greedy:.2f}\n")
        result_lines.append("\nРезультати імовірнісного алгоритму:\n")
        result_lines.append(f"Вибрані тунелі: {x_prob}\n")
        result_lines.append(f"Загальна довжина: {L_prob:.2f}\n")
        print("\nРезультати жадібного алгоритму:")
        print(f"Вибрані тунелі: {x_greedy}")
        print(f"Загальна довжина: {L_greedy:.2f}")
        print("\nРезультати імовірнісного алгоритму:")
        print(f"Вибрані тунелі: {x_prob}")
        print(f"Загальна довжина: {L_prob:.2f}")
        plot_tunnels(a, b, c, d, n, W, H)
    else:
        result_lines.append("\nНевірний вибір!\n")
        print("Невірний вибір!")
        plot_tunnels(a, b, c, d, n, W, H)
    
    results = "".join(result_lines)
    save_results_to_file(results)

def main_menu():
    while True:
        print("\nГоловне меню.")
        print("Статус задачі: Задача не встановлена")
        print("\nДоступні опції:")
        print("1. Згенерувати дані випадковим чином")
        print("2. Ввести дані вручну")
        print("3. Завантажити дані задачі з файлу")
        print("4. Провести експерименти")
        print("0. Вихід")
        choice = input("\nВведіть ваш вибір: ")
        
        try:
            choice = int(choice)
        except ValueError:
            print("Будь ласка, введіть коректне число!")
            continue
        
        if choice == 1:
            while True:
                try:
                    n = int(input("Введіть кількість тунелів (n): "))
                    if n <= 0:
                        raise ValueError("Кількість тунелів має бути додатною!")
                    break
                except ValueError as e:
                    print(f"Невірне введення: {str(e)}. Введіть додатне ціле число!")
            
            while True:
                try:
                    l_avg = float(input("Введіть середню довжину тунелю (l̅): "))
                    if l_avg <= 0:
                        raise ValueError("Середня довжина тунелю має бути додатною!")
                    break
                except ValueError as e:
                    print(f"Невірне введення: {str(e)}. Введіть додатне число!")
            
            while True:
                try:
                    delta_l = float(input("Введіть відхилення довжини (Δl): "))
                    if delta_l < 0:
                        raise ValueError("Відхилення довжини не може бути від'ємним!")
                    if delta_l > l_avg:
                        raise ValueError("Відхилення довжини не може бути більшим за середню довжину!")
                    break
                except ValueError as e:
                    print(f"Невірне введення: {str(e)}. Введіть невід'ємне число, не більше за l̅!")
            
            while True:
                try:
                    W = float(input("Введіть ширину області генерації (W): "))
                    if W <= 0:
                        raise ValueError("Ширина має бути додатною!")
                    break
                except ValueError as e:
                    print(f"Невірне введення: {str(e)}. Введіть додатне число!")
            
            while True:
                try:
                    H = float(input("Введіть висоту області генерації (H): "))
                    if H <= 0:
                        raise ValueError("Висота має бути додатною!")
                    break
                except ValueError as e:
                    print(f"Невірне введення: {str(e)}. Введіть додатне число!")
            
            while True:
                try:
                    m = int(input("Введіть кількість ітерацій для імовірнісного алгоритму (m): "))
                    if m <= 0:
                        raise ValueError("Кількість ітерацій має бути додатною!")
                    break
                except ValueError as e:
                    print(f"Невірне введення: {str(e)}. Введіть додатне ціле число!")
            
            print("\nГенерація тунелів...")
            a, b, c, d = generate_tunnels(n, l_avg, delta_l, W, H)
            run_task(n, a, b, c, d, m, W, H)
            break
        elif choice == 2:
            while True:
                try:
                    n = int(input("Введіть кількість тунелів (n): "))
                    if n <= 0:
                        raise ValueError("Кількість тунелів має бути додатною!")
                    break
                except ValueError as e:
                    print(f"Невірне введення: {str(e)}. Введіть додатне ціле число!")
            
            a, b, c, d = manual_input_tunnels(n)
            
            while True:
                try:
                    m = int(input("Введіть кількість ітерацій для імовірнісного алгоритму (m): "))
                    if m <= 0:
                        raise ValueError("Кількість ітерацій має бути додатною!")
                    break
                except ValueError as e:
                    print(f"Невірне введення: {str(e)}. Введіть додатне ціле число!")
            
            run_task(n, a, b, c, d, m)
            break
        elif choice == 3:
            result = load_task_from_file()
            if result is not None:
                n, m, a, b, c, d = result
                print("\nДані задачі успішно завантажено:")
                print(f"n: {n}, m: {m}")
                print("Координати тунелів:")
                for i in range(n):
                    print(f"Тунель {i+1}: ({a[i]:.2f}, {b[i]:.2f}, {c[i]:.2f}, {d[i]:.2f})")
                run_task(n, a, b, c, d, m)
                break
            else:
                print("Не вдалося завантажити дані задачі. Спробуйте ще раз.")
        elif choice == 4:
            run_experiments()
            continue
        elif choice == 0:
            print("Завершення програми.")
            break
        else:
            print("Невірна опція! Оберіть 0, 1, 2, 3 або 4.")