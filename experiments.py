import time
import matplotlib.pyplot as plt
import math
from generator import generate_tunnels
from algorithms import greedy_algorithm, probabilistic_algorithm
from utils import save_results_to_file

def run_experiment_iterations():
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
            if W <= l_avg:
                raise ValueError("Ширина має бути більшою за середню довжину тунелю!")
            break
        except ValueError as e:
            print(f"Невірне введення: {str(e)}. Введіть додатне число!")
    
    while True:
        try:
            H = float(input("Введіть висоту області генерації (H): "))
            if H <= l_avg:
                raise ValueError("Висота має бути більшою за середню довжину тунелю!")
            break
        except ValueError as e:
            print(f"Невірне введення: {str(e)}. Введіть додатне число!")
    
    while True:
        try:
            K = int(input("Введіть кількість прогонів експерименту (K): "))
            if K <= 0:
                raise ValueError("Кількість прогонів експерименту має бути додатною!")
            break
        except ValueError as e:
            print(f"Невірне введення: {str(e)}. Введіть додатне ціле число!")
    
    while True:
        try:
            m_values_input = input("Введіть список значень m (через пробіл, наприклад, 0.5 1 2 5): ").split()
            m_valuescef = [float(m) for m in m_values_input]
            m_values = [int(math.ceil(round(mcef*n,5))) for mcef in m_valuescef]
            if not m_values:
                raise ValueError("Ви маєте вказати хоча б одне значення m!")
            if any(m <= 0 for m in m_values):
                raise ValueError("Усі значення m мають бути додатними!")
            break
        except ValueError as e:
            print(f"Невірне введення: {str(e)}. Введіть додатні числа через пробіл!")

    results = {m: [] for m in m_values}

    print("\nВиконання експерименту (вплив m)...")
    experiment_lines = ["Виконання експерименту (вплив m)...\n"]
    for i in range(1, K + 1):
        run_line = f"\nПрогін експерименту {i}/{K}:\n"
        print(run_line, end="")
        experiment_lines.append(run_line)
        a, b, c, d = generate_tunnels(n, l_avg, delta_l, W, H)
        for m in m_values:
            _, L = probabilistic_algorithm(n, a, b, c, d, m)
            results[m].append(L)
            result_line = f"  m={m}: Значення цільової функції (ЦФ) = {L:.2f}\n"
            print(result_line, end="")
            experiment_lines.append(result_line)

    result_lines = ["\nРезультати експерименту (вплив m):\n", "m\tСереднє ЦФ\n", "-" * 20 + "\n"]
    print("\nРезультати експерименту (вплив m):")
    print("m\tСереднє ЦФ")
    print("-" * 20)
    avg_results = []
    for m in m_values:
        avg_L = sum(results[m]) / K
        avg_results.append(avg_L)
        line = f"{m}\t{avg_L:.2f}\n"
        print(line, end="")
        result_lines.append(line)

    plt.figure(figsize=(8, 5))
    plt.plot(m_values, avg_results, marker='o', linestyle='-', color='blue')
    plt.title("Залежність значення цільової функції від m")
    plt.xlabel("Кількість ітерацій (m)")
    plt.ylabel("Середнє значення цільової функції (L̅)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    results = "".join(experiment_lines) + "".join(result_lines)
    save_results_to_file(results)

def run_experiment_delta_l():
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
            W = float(input("Введіть ширину області генерації (W): "))
            if W <= l_avg:
                raise ValueError("Ширина має бути більшою за середню довжину тунелю!")
            break
        except ValueError as e:
            print(f"Невірне введення: {str(e)}. Введіть додатне число!")
    
    while True:
        try:
            H = float(input("Введіть висоту області генерації (H): "))
            if H <= l_avg:
                raise ValueError("Висота має бути більшою за середню довжину тунелю!")
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
    
    while True:
        try:
            K = int(input("Введіть кількість прогонів експерименту (K): "))
            if K <= 0:
                raise ValueError("Кількість прогонів експерименту має бути додатною!")
            break
        except ValueError as e:
            print(f"Невірне введення: {str(e)}. Введіть додатне ціле число!")
    
    while True:
        try:
            delta_l_values_input = input("Введіть список значень Δl від 0 до 1 (через пробіл, наприклад, 0.1 0.2 0.3 1.0): ").split()
            delta_l_valuescef = [float(dl) for dl in delta_l_values_input]
            delta_l_values = [(round(dlcef*l_avg, 5)) for dlcef in delta_l_valuescef]
            if not delta_l_values:
                raise ValueError("Ви маєте вказати хоча б одне значення Δl!")
            if any(dl < 0 for dl in delta_l_values):
                raise ValueError("Усі значення Δl мають бути невід'ємними!")
            if any(dl > l_avg for dl in delta_l_values):
                raise ValueError("Усі значення Δl мають бути не більшими за l̅!")
            break
        except ValueError as e:
            print(f"Невірне введення: {str(e)}. Введіть невід'ємні числа від 0 до 1 через пробіл!")

    results_greedy = {dl: [] for dl in delta_l_values}
    results_prob = {dl: [] for dl in delta_l_values}

    print("\nВиконання експерименту (вплив Δl)...")
    experiment_lines = ["Виконання експерименту (вплив Δl)...\n"]
    for i in range(1, K + 1):
        run_line = f"\nПрогін експерименту {i}/{K}:\n"
        print(run_line, end="")
        experiment_lines.append(run_line)
        for dl in delta_l_values:
            a, b, c, d = generate_tunnels(n, l_avg, dl, W, H)
            _, L_greedy = greedy_algorithm(n, a, b, c, d)
            results_greedy[dl].append(L_greedy)
            _, L_prob = probabilistic_algorithm(n, a, b, c, d, m)
            results_prob[dl].append(L_prob)
            result_line = f"  Δl={dl}: Жадібний ЦФ = {L_greedy:.2f}, Імовірнісний ЦФ = {L_prob:.2f}\n"
            print(result_line, end="")
            experiment_lines.append(result_line)

    result_lines = ["\nРезультати експерименту (вплив Δl):\n",
                    "Δl\tСереднє ЦФ (Жадібний)\tСереднє ЦФ (Імовірнісний)\tВідносне відхилення (%)\n",
                    "-" * 80 + "\n"]
    print("\nРезультати експерименту (вплив Δl):")
    print("Δl\tСереднє ЦФ (Жадібний)\tСереднє ЦФ (Імовірнісний)\tВідносне відхилення (%)")
    print("-" * 80)
    avg_L_greedy_list = []
    avg_L_prob_list = []
    for dl in delta_l_values:
        avg_L_greedy = sum(results_greedy[dl]) / K
        avg_L_prob = sum(results_prob[dl]) / K
        avg_L_greedy_list.append(avg_L_greedy)
        avg_L_prob_list.append(avg_L_prob)
        if avg_L_greedy == 0:
            rel_dev = "Н/Д"
        else:
            rel_dev = ((avg_L_prob - avg_L_greedy) / avg_L_greedy) * 100
            rel_dev = f"{rel_dev:.2f}"
        line = f"{dl}\t{avg_L_greedy:.2f}\t\t\t{avg_L_prob:.2f}\t\t\t{rel_dev}\n"
        print(line, end="")
        result_lines.append(line)

    plt.figure(figsize=(8, 5))
    plt.plot(delta_l_values, avg_L_greedy_list, marker='o', linestyle='-', color='blue', label='Жадібний алгоритм')
    plt.plot(delta_l_values, avg_L_prob_list, marker='s', linestyle='--', color='red', label='Імовірнісний алгоритм')
    plt.title("Залежність значення цільової функції від Δl")
    plt.xlabel("Відхилення довжини (Δl)")
    plt.ylabel("Середнє значення цільової функції (L̅)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    results = "".join(experiment_lines) + "".join(result_lines)
    save_results_to_file(results)

def run_experiment_n():
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
            if W <= l_avg:
                raise ValueError("Ширина має бути більшою за середню довжину тунелю!")
            break
        except ValueError as e:
            print(f"Невірне введення: {str(e)}. Введіть додатне число!")
    
    while True:
        try:
            H = float(input("Введіть висоту області генерації (H): "))
            if H <= l_avg:
                raise ValueError("Висота має бути більшою за середню довжину тунелю!")
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
    
    while True:
        try:
            K = int(input("Введіть кількість прогонів експерименту (K): "))
            if K <= 0:
                raise ValueError("Кількість прогонів експерименту має бути додатною!")
            break
        except ValueError as e:
            print(f"Невірне введення: {str(e)}. Введіть додатне ціле число!")
    
    while True:
        try:
            n_values_input = input("Введіть список значень n (через пробіл, наприклад, 5 10 15): ").split()
            n_values = [int(n) for n in n_values_input]
            if not n_values:
                raise ValueError("Ви маєте вказати хоча б одне значення n!")
            if any(n <= 0 for n in n_values):
                raise ValueError("Усі значення n мають бути додатними!")
            break
        except ValueError as e:
            print(f"Невірне введення: {str(e)}. Введіть додатні цілі числа через пробіл!")

    results_greedy_cf = {n: [] for n in n_values}
    results_greedy_time = {n: [] for n in n_values}
    results_prob_cf = {n: [] for n in n_values}
    results_prob_time = {n: [] for n in n_values}

    print("\nВиконання експерименту (вплив n)...")
    experiment_lines = ["Виконання експерименту (вплив n)...\n"]
    for n in n_values:
        run_line = f"\nТестування з n={n}:\n"
        print(run_line, end="")
        experiment_lines.append(run_line)
        for i in range(1, K + 1):
            a, b, c, d = generate_tunnels(n, l_avg, delta_l, W, H)
            
            start_time = time.perf_counter()
            _, L_greedy = greedy_algorithm(n, a, b, c, d)
            end_time = time.perf_counter()
            greedy_time = end_time - start_time
            results_greedy_cf[n].append(L_greedy)
            results_greedy_time[n].append(greedy_time)
            
            start_time = time.perf_counter()
            _, L_prob = probabilistic_algorithm(n, a, b, c, d, m)
            end_time = time.perf_counter()
            prob_time = end_time - start_time
            results_prob_cf[n].append(L_prob)
            results_prob_time[n].append(prob_time)
            
            result_line = f"  Прогін {i}/{K}: Жадібний ЦФ = {L_greedy:.2f}, Час = {greedy_time:.4f}с; Імовірнісний ЦФ = {L_prob:.2f}, Час = {prob_time:.4f}с\n"
            print(result_line, end="")
            experiment_lines.append(result_line)

    result_lines = ["\nРезультати експерименту (вплив n):\n",
                    "n\tСр. ЦФ (Жадібний)\tСр. Час (Жадібний, с)\tСр. ЦФ (Імовірнісний)\tСр. Час (Імовірнісний, с)\n",
                    "-" * 90 + "\n"]
    print("\nРезультати експерименту (вплив n):")
    print("n\tСр. ЦФ (Жадібний)\tСр. Час (Жадібний, с)\tСр. ЦФ (Імовірнісний)\tСр. Час (Імовірнісний, с)")
    print("-" * 90)
    avg_L_greedy_list = []
    avg_L_prob_list = []
    avg_time_greedy_list = []
    avg_time_prob_list = []
    for n in n_values:
        avg_L_greedy = sum(results_greedy_cf[n]) / K
        avg_time_greedy = sum(results_greedy_time[n]) / K
        avg_L_prob = sum(results_prob_cf[n]) / K
        avg_time_prob = sum(results_prob_time[n]) / K
        avg_L_greedy_list.append(avg_L_greedy)
        avg_L_prob_list.append(avg_L_prob)
        avg_time_greedy_list.append(avg_time_greedy)
        avg_time_prob_list.append(avg_time_prob)
        line = f"{n}\t{avg_L_greedy:.2f}\t\t{avg_time_greedy:.4f}\t\t\t{avg_L_prob:.2f}\t\t\t{avg_time_prob:.4f}\n"
        print(line, end="")
        result_lines.append(line)

    # Графік для цільової функції
    plt.figure(figsize=(8, 5))
    plt.plot(n_values, avg_L_greedy_list, marker='o', linestyle='-', color='blue', label='Жадібний алгоритм')
    plt.plot(n_values, avg_L_prob_list, marker='s', linestyle='--', color='red', label='Імовірнісний алгоритм')
    plt.title("Залежність значення цільової функції від n")
    plt.xlabel("Кількість тунелів (n)")
    plt.ylabel("Середнє значення цільової функції (L̅)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Графік для часу виконання
    plt.figure(figsize=(8, 5))
    plt.plot(n_values, avg_time_greedy_list, marker='o', linestyle='-', color='blue', label='Жадібний алгоритм')
    plt.plot(n_values, avg_time_prob_list, marker='s', linestyle='--', color='red', label='Імовірнісний алгоритм')
    plt.title("Залежність часу виконання від n")
    plt.xlabel("Кількість тунелів (n)")
    plt.ylabel("Середній час виконання (с)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    results = "".join(experiment_lines) + "".join(result_lines)
    save_results_to_file(results)

def run_experiments():
    while True:
        print("\nМеню експериментів:")
        print("1. Експеримент 1: Вплив кількості ітерацій (m)")
        print("2. Експеримент 2: Вплив відхилення довжини (Δl)")
        print("3. Експеримент 3: Вплив кількості тунелів (n)")
        print("0. Повернутися до головного меню")
        choice = input("\nВведіть ваш вибір: ")
        
        try:
            choice = int(choice)
        except ValueError:
            print("Будь ласка, введіть коректне число!")
            continue
        
        if choice == 1:
            run_experiment_iterations()
            continue
        elif choice == 2:
            run_experiment_delta_l()
            continue
        elif choice == 3:
            run_experiment_n()
            continue
        elif choice == 0:
            print("Повернення до головного меню.")
            return
        else:
            print("Невірна опція! Оберіть 0, 1, 2 або 3.")