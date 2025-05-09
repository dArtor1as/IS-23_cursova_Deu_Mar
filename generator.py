import math
import random

def generate_tunnels(n, l_avg, delta_l, W, H):
    a, b, c, d = [], [], [], []
    j = 0
    while j < n:
        at = random.uniform(0, W)
        bt = random.uniform(0, H)
        ct = random.uniform(0, W)
        dt = random.uniform(0, H)
        length = math.sqrt((ct - at) ** 2 + (dt - bt) ** 2)
        if l_avg - delta_l <= length <= l_avg + delta_l:
            a.append(at)
            b.append(bt)
            c.append(ct)
            d.append(dt)
            j += 1
    return a, b, c, d

def manual_input_tunnels(n):
    a, b, c, d = [], [], [], []
    print(f"\nВведіть координати для {n} тунелів (формат: a b c d):")
    for i in range(n):
        while True:
            try:
                coords = input(f"Координати тунелю {i+1} (a b c d): ").split()
                if len(coords) != 4:
                    raise ValueError("Будь ласка, введіть рівно 4 координати (a b c d)!")
                at = float(coords[0])
                bt = float(coords[1])
                ct = float(coords[2])
                dt = float(coords[3])
                a.append(at)
                b.append(bt)
                c.append(ct)
                d.append(dt)
                break
            except ValueError as e:
                print(f"Невірне введення: {str(e)}. Будь ласка, введіть 4 дійсні числа!")
    return a, b, c, d