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

    @property
    def age(self):
        return self.__age

    def age_up(self):
        self.__age += 1

    @property
    def is_sick(self):
        return self.__is_sick

    def become_sick(self):
        self.__is_sick = True
        self.is_in_first_phase = True

    def get_well(self):
        self.__is_sick = False
        self.__is_immune = True

    @property
    def is_in_first_phase(self):
        return self.__sickness_phase_a

    @is_in_first_phase.setter
    def is_in_first_phase(self, new_value):
        self.__sickness_phase_a = new_value

    @property
    def is_in_second_phase(self):
        return self.__sickness_phase_b

    @is_in_second_phase.setter
    def is_in_second_phase(self, new_value):
        self.__sickness_phase_b = new_value

    @property
    def is_immune(self):
        return self.__is_immune

    def lost_immunity(self):
        self.__is_immune = False

    @property
    def is_alive(self):
        return self.__is_alive

    def die(self):
        self.__is_alive = False
