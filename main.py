import sys
from menu import main_menu, run_task , load_task_from_file


def main():
    if not sys.stdin.isatty():
        print("Виявлено неінтерактивне середовище. Спроба завантажити дані задачі з файлу...")
        result = load_task_from_file()
        if result is not None:
            n, m, a, b, c, d = result
            print("\nДані задачі успішно завантажено:")
            print(f"n: {n}, m: {m}")
            print("Координати тунелів:")
            for i in range(n):
                print(f"Тунель {i+1}: ({a[i]:.2f}, {b[i]:.2f}, {c[i]:.2f}, {d[i]:.2f})")
            run_task(n, a, b, c, d, m)
        else:
            print("Не вдалося завантажити дані задачі. Завершення роботи.")
        return

    main_menu()

if __name__ == "__main__":
    main()