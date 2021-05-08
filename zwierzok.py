class Zwierzok:
    def __init__(self,
                 age: int,
                 is_sick: bool,
                 phase_one: bool,
                 phase_two: bool,
                 is_immune: bool
                 ):
        self.__age = age
        self.__is_sick = is_sick
        self.__sickness_phase_a = phase_one
        self.__sickness_phase_b = phase_two
        self.__is_immune = is_immune
        self.__is_alive = True

    def __str__(self):
        return f"Wiek: {self.__age}, {'chory' if self.__is_sick else 'zdrowy'}"

    @property
    def age(self):
        return self.__age

    def age_up(self):
        self.__age += 1

    @property
    def is_sick(self):
        return self.__is_sick

    @property
    def is_first_phase(self):
        return self.__sickness_phase_a

    @property
    def is_second_phase(self):
        return self.__sickness_phase_b

    @property
    def is_immune(self):
        return self.__is_immune

    @property
    def is_alive(self):
        return self.__is_alive

    def die(self):
        self.__is_alive = False
