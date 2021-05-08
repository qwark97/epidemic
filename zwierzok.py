class Zwierzok:
    def __init__(self, age, is_sick):
        self.__age = age
        self.__is_sick = is_sick
        self.__sickness_phase_a = True if is_sick else False
        self.__sickness_phase_b = False
        self.__is_immune = False
        self.__is_alive = True

    def __str__(self):
        return f"Wiek: {self.__age}, {'chory' if self.__is_sick else 'zdrowy'}"

    @property
    def age(self):
        return self.__age

    @property
    def is_sick(self):
        return self.__is_sick

    @property
    def is_alive(self):
        return self.__is_alive

    @is_alive.setter
    def is_alive(self, died):
        self.__is_alive = died
