import os

def save_results_to_file(results):
    while True:
        save_choice = input("\nЗберегти результати розв'язання до файлу? (так/ні): ").strip().lower()
        if save_choice in ['так', 'ні']:
            break
        print("Будь ласка, введіть 'так' або 'ні'!")
    
    if save_choice == 'ні':
        return
    
    while True:
        filename = input("Введіть назву файлу (наприклад, example.txt): ").strip()
        if not filename:
            print("Назва файлу не може бути порожньою!")
            continue
        
        if not os.path.exists('results/'+filename):
            while True:
                create_choice = input(f"Створити файл {filename}? (так/ні): ").strip().lower()
                if create_choice in ['так', 'ні']:
                    break
                print("Будь ласка, введіть 'так' або 'ні'!")
            
            if create_choice == 'ні':
                continue
            try:
                with open('results/'+filename, 'w', encoding='utf-8') as f:
                    f.write(results)
                print(f"Результати збережено до {filename}")
                break
            except Exception as e:
                print(f"Помилка при записі до файлу: {str(e)}")
                continue
        else:
            while True:
                overwrite_choice = input("Файл уже існує. Перезаписати? (так/ні): ").strip().lower()
                if overwrite_choice in ['так', 'ні']:
                    break
                print("Будь ласка, введіть 'так' або 'ні'!")
            
            if overwrite_choice == 'ні':
                continue
            try:
                with open('results/'+filename, 'w', encoding='utf-8') as f:
                    f.write(results)
                print(f"Результати збережено до {filename}")
                break
            except Exception as e:
                print(f"Помилка при записі до файлу: {str(e)}")
                continue