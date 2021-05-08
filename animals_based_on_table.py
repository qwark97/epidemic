"""
Wiek w u.j.c    Liczba zwierząt zdrowych    Liczba zwierząt chorych
---------------------------------------------------------------------
1               80 (20 czasowa odporność)   20 (10 faza 1, 10 faza 2)
---------------------------------------------------------------------
2               90 (30 czasowa odporność)   30 (10 faza 1, 20 faza 2)
---------------------------------------------------------------------
3               80 (10 czasowa odporność)   15 (5 faza 1, 10 faza 2)
---------------------------------------------------------------------
4               70 (10 czasowa odporność)   15 (10 faza 1, 5 faza 2)
---------------------------------------------------------------------
5               40 (20 czasowa odporność)   10 (7 faza 1, 3 faza 2)
---------------------------------------------------------------------
6               15 (5 czasowa odporność)    10 (6 faza 1, 4 faza 2)
---------------------------------------------------------------------
7               10                          3 ( 3 faza 2)
---------------------------------------------------------------------
"""
from epidemic.zwierzok import Zwierzok


def provide_animals():
    animals = []
    data = [
        (60, 20, 10, 10),
        (60, 30, 10, 20),
        (70, 10, 5, 10),
        (60, 10, 10, 5),
        (20, 20, 7, 3),
        (10, 5, 6, 4),
        (10, 0, 0, 3)
    ]
    for age in range(1, 8):
        healthy, immune, phase_one, phase_two = data[age-1]
        for _ in range(healthy):
            animals.append(Zwierzok(
                age=age,
                is_sick=False,
                phase_one=False,
                phase_two=False,
                is_immune=False
            ))
        for _ in range(immune):
            animals.append(Zwierzok(
                age=age,
                is_sick=False,
                phase_one=False,
                phase_two=False,
                is_immune=True
            ))
        for _ in range(phase_one):
            animals.append(Zwierzok(
                age=age,
                is_sick=True,
                phase_one=True,
                phase_two=False,
                is_immune=False
            ))
        for _ in range(phase_two):
            animals.append(Zwierzok(
                age=age,
                is_sick=True,
                phase_one=False,
                phase_two=True,
                is_immune=False
            ))
    return animals
